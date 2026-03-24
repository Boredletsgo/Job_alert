"""
Gmail Notifier - Send job alerts via Gmail (FREE)
Uses Gmail SMTP with App Password (no OAuth needed)
Setup: Enable 2FA → Generate App Password → Set as secret
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


GMAIL_USER = os.getenv("GMAIL_USER")         # your@gmail.com
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # 16-char app password
ALERT_EMAIL = os.getenv("ALERT_EMAIL", GMAIL_USER)    # where to send alerts


def build_html_email(jobs: list) -> str:
    """Build a beautiful HTML email for job alerts."""
    govt_jobs = [j for j in jobs if j.get("type") == "GOVT"]
    private_jobs = [j for j in jobs if j.get("type") == "PRIVATE"]

    def job_card(job, color="#1a73e8"):
        return f"""
        <div style="border-left:4px solid {color}; padding:12px 16px; margin:10px 0;
                    background:#f8f9fa; border-radius:0 8px 8px 0;">
            <h3 style="margin:0 0 4px; color:#202124; font-size:15px;">{job['title']}</h3>
            <p style="margin:2px 0; color:#5f6368; font-size:13px;">
                🏢 {job.get('company','N/A')} &nbsp;|&nbsp;
                📅 {job.get('date','N/A')} &nbsp;|&nbsp;
                📡 {job['source']}
            </p>
            {"<p style='margin:2px 0; color:#5f6368; font-size:12px;'>🔧 " + job.get('skills','') + "</p>" if job.get('skills') else ""}
            <a href="{job.get('link','#')}" style="display:inline-block; margin-top:6px;
               padding:5px 14px; background:{color}; color:white; border-radius:4px;
               text-decoration:none; font-size:12px; font-weight:600;">Apply →</a>
        </div>
        """

    govt_section = ""
    if govt_jobs:
        cards = "".join(job_card(j, "#1557b0") for j in govt_jobs[:20])
        govt_section = f"""
        <h2 style="color:#1557b0; border-bottom:2px solid #1557b0; padding-bottom:6px;">
            🏛️ Government Jobs ({len(govt_jobs)})
        </h2>
        {cards}
        """

    private_section = ""
    if private_jobs:
        cards = "".join(job_card(j, "#0f9d58") for j in private_jobs[:15])
        private_section = f"""
        <h2 style="color:#0f9d58; border-bottom:2px solid #0f9d58; padding-bottom:6px; margin-top:24px;">
            🏢 Private / IT Jobs ({len(private_jobs)})
        </h2>
        {cards}
        """

    today = datetime.today().strftime("%d %B %Y")
    return f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family:'Segoe UI',Arial,sans-serif; max-width:680px; margin:0 auto;
                 background:#fff; color:#202124;">
        <div style="background:linear-gradient(135deg,#1a73e8,#0f9d58); padding:24px; border-radius:12px 12px 0 0;">
            <h1 style="color:white; margin:0; font-size:22px;">🚨 Job Alert Report</h1>
            <p style="color:rgba(255,255,255,0.85); margin:4px 0 0;">{today} — {len(jobs)} new jobs found</p>
        </div>
        <div style="padding:20px; border:1px solid #e8eaed; border-top:none; border-radius:0 0 12px 12px;">
            {govt_section}
            {private_section}
            <hr style="border:none; border-top:1px solid #e8eaed; margin-top:24px;">
            <p style="color:#9aa0a6; font-size:12px; text-align:center;">
                Sent by your Job Alert Agent • <a href="https://github.com">View on GitHub</a>
            </p>
        </div>
    </body>
    </html>
    """


def notify_email(jobs: list):
    """Send job alerts via Gmail SMTP."""
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("[Gmail] ⚠️  GMAIL_USER or GMAIL_APP_PASSWORD not set.")
        return

    if not jobs:
        print("[Gmail] No new jobs. Skipping email.")
        return

    today = datetime.today().strftime("%d %b %Y")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🚨 Job Alert: {len(jobs)} New Jobs Found — {today}"
    msg["From"] = GMAIL_USER
    msg["To"] = ALERT_EMAIL

    html_content = build_html_email(jobs)
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, ALERT_EMAIL, msg.as_string())
        print(f"[Gmail] ✅ Email sent to {ALERT_EMAIL} with {len(jobs)} jobs")
    except Exception as e:
        print(f"[Gmail] ❌ Error: {e}")
