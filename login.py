import streamlit as st
import hashlib
import sqlite3

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

st.title("🔐 User Access")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab2:
    new_user = st.text_input("Choose Username")
    new_pw = st.text_input("Choose Password", type="password")
    if st.button("Sign Up"):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (user TEXT PRIMARY KEY, pw TEXT)")
        try:
            c.execute("INSERT INTO users VALUES (?,?)", (new_user, hash_pw(new_pw)))
            conn.commit()
            st.success("Account created! Go to Login tab.")
        except:
            st.error("User already exists.")
        conn.close()

with tab1:
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT pw FROM users WHERE user=?", (user,))
        result = c.fetchone()
        if result and result[0] == hash_pw(pw):
            st.session_state["logged_in"] = True
            st.session_state["username"] = user
            st.success("Logged in!")
            st.switch_page("main.py")
        else:
            st.error("Invalid credentials")
        conn.close()