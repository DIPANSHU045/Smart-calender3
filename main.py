import streamlit as st
import sqlite3
import pandas as pd
from streamlit_calendar import calendar
from logic import extract_event_details
from email_notif import send_today_event_notification

# 1. Page Config
st.set_page_config(page_title="Smart Event Calendar", layout="wide")

# 2. Session Check (Redirect if not logged in)
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.info("Please log in to manage your events.")
    st.stop()

user = st.session_state["username"]
db_name = f"data_{user}.db"

# 3. Database Functions
def init_db():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events 
                 (title TEXT, start TEXT, end TEXT, location TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 4. Sidebar: NLP Input
st.sidebar.title(f"Welcome, {user}")
event_text = st.sidebar.text_area("Type your event (e.g. 'Lunch with Dev on Friday at 2pm')")

if st.sidebar.button("Add to Calendar"):
    details = extract_event_details(event_text)
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO events VALUES (?, ?, ?, ?)", 
              (details['summary'], details['start'], details['end'], details['location']))
    conn.commit()
    conn.close()
    st.sidebar.success("Event Added!")
    st.rerun()

# 5. Main UI: Calendar Display
st.title("📅 My Smart Schedule")

conn = sqlite3.connect(db_name)
df = pd.read_sql_query("SELECT title, start, end FROM events", conn)
conn.close()

calendar_options = {
    "headerToolbar": {"left": "prev,next today", "center": "title", "right": "dayGridMonth,timeGridWeek"},
    "initialView": "dayGridMonth",
}

state = calendar(events=df.to_dict(orient='records'), options=calendar_options)