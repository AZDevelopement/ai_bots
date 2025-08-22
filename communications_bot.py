# communications_bot.py

import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def send_health_report(bot_name, issue, timestamp=None):
    if not timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""
    🚨 Health Alert 🚨
    Bot: {bot_name}
    Issue: {issue}
    Time: {timestamp}
    """

    print(report.strip())

    # Uncomment and configure this to enable real email alerts
    # send_email("your_email@example.com", "Health Alert", report)

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "your_email@example.com"
    msg["To"] = to

    try:
        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login("your_email@example.com", "your_password")
            server.send_message(msg)
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
