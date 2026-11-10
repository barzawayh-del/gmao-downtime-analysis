import logging
import os
import smtplib
import subprocess
import sys
from email.message import EmailMessage
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("gmao")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("pipeline.log", maxBytes=200_000, backupCount=3, encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)


def run_step(script):
    """Run one script; raise an error with its output if it fails."""
    logger.info("Starting %s", script)
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        tail = result.stderr[-1500:]
        logger.error("%s failed (code %s): %s", script, result.returncode, tail)
        raise RuntimeError(f"{script} failed with code {result.returncode}\n\n{tail}")
    logger.info("%s finished OK", script)


def send_alert(text):
    user = os.environ["GMAIL_USER"]
    password = os.environ["GMAIL_APP_PASSWORD"]
    msg = EmailMessage()
    msg["Subject"] = "ALERT: GMAO report failed"
    msg["From"] = user
    msg["To"] = user
    msg.set_content(text)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(user, password)
        server.send_message(msg)


try:
    run_step("report_day9.py")
    run_step("send_report.py")
    logger.info("Pipeline OK")
except Exception as error:
    logger.exception("Pipeline failed")
    try:
        send_alert(str(error))
    except Exception:
        logger.exception("Could not send alert")
    sys.exit(1)