import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

user = os.environ["GMAIL_USER"]
password = os.environ["GMAIL_APP_PASSWORD"]
report = Path("gmao_report.xlsx")

msg = EmailMessage()
msg["Subject"] = "GMAO daily report"
msg["From"] = user
msg["To"] = user
msg.set_content("Hello,\n\nPlease find attached today's GMAO downtime report.\n")
msg.add_attachment(
    report.read_bytes(),
    maintype="application",
    subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    filename=report.name,
)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(user, password)
    server.send_message(msg)

print("Report sent to", user)