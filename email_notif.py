import smtplib
from email.mime.text import MIMEText

def send_notification(email, event_name):
    me = "your_bot_email@gmail.com"
    pw = "your_app_password_here" # Get this from Google Account Security
    
    msg = MIMEText(f"Reminder: {event_name} is happening soon!")
    msg['Subject'] = 'Event Reminder'
    msg['From'] = me
    msg['To'] = email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(me, pw)
        server.sendmail(me, [email], msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send: {e}")