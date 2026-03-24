"""
Telegram Notifier - Send job alerts via Telegram Bot (FREE)
Setup: Create a bot via @BotFather, get TOKEN + CHAT_ID
"""

import requests
import os


TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(text: str) -> bool:
    """Send a message via Telegram Bot API."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[Telegram] ⚠️  TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        res = requests.post(url, json=payload, timeout=10)
        if res.status_code == 200:
            return True
        else:
            print(f"[Telegram] Error: {res.text}")
            return False
    except Exception as e:
        print(f"[Telegram] Exception: {e}")
        return False


def format_job_message(jobs: list) -> list:
    """Format jobs into Telegram-friendly chunks (max 4096 chars each)."""
    if not jobs:
        return ["✅ No new job alerts today. All caught up!"]

    govt_jobs = [j for j in jobs if j.get("type") == "GOVT"]
    private_jobs = [j for j in jobs if j.get("type") == "PRIVATE"]

    messages = []

    # Header
    header = (
        f"🚨 <b>Job Alert — {len(jobs)} New Jobs Found!</b>\n"
        f"🏛️ Govt: {len(govt_jobs)} | 🏢 Private: {len(private_jobs)}\n"
        f"{'─'*30}\n"
    )

    chunks = [header]
    current_chunk = header

    def flush():
        nonlocal current_chunk
        if current_chunk.strip():
            messages.append(current_chunk)
        current_chunk = ""

    # Govt jobs section
    if govt_jobs:
        section = "\n🏛️ <b>GOVERNMENT JOBS</b>\n"
        current_chunk += section

        for job in govt_jobs[:20]:
            entry = (
                f"\n📌 <b>{job['title']}</b>\n"
                f"   🏢 {job.get('company', 'N/A')}\n"
                f"   📅 {job.get('date', 'N/A')}\n"
                f"   🌐 <a href='{job.get('link', '#')}'>Apply Here</a>\n"
                f"   📡 Source: {job['source']}\n"
            )
            if len(current_chunk) + len(entry) > 4000:
                flush()
                current_chunk = entry
            else:
                current_chunk += entry

    # Private jobs section
    if private_jobs:
        section = "\n🏢 <b>PRIVATE / IT JOBS</b>\n"
        if len(current_chunk) + len(section) > 4000:
            flush()
            current_chunk = section
        else:
            current_chunk += section

        for job in private_jobs[:15]:
            entry = (
                f"\n💼 <b>{job['title']}</b>\n"
                f"   🏢 {job.get('company', 'N/A')}\n"
                f"   📍 {job.get('location', 'India')}\n"
                f"   🔧 {job.get('skills', '')}\n"
                f"   🌐 <a href='{job.get('link', '#')}'>Apply Here</a>\n"
                f"   📡 Source: {job['source']}\n"
            )
            if len(current_chunk) + len(entry) > 4000:
                flush()
                current_chunk = entry
            else:
                current_chunk += entry

    flush()
    return messages


def notify_telegram(jobs: list):
    """Send all job alerts via Telegram."""
    messages = format_job_message(jobs)
    print(f"[Telegram] Sending {len(messages)} message(s)...")
    for i, msg in enumerate(messages):
        success = send_telegram_message(msg)
        if success:
            print(f"  ✅ Message {i+1}/{len(messages)} sent")
        else:
            print(f"  ❌ Message {i+1}/{len(messages)} failed")
