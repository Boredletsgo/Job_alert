"""
Job Alert Agent — Main Entry Point
Run manually: python main.py
Auto-run: GitHub Actions (see .github/workflows/job_alert.yml)
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from job_scraper import get_all_jobs, get_new_jobs
from telegram_notifier import notify_telegram
from email_notifier import notify_email


def main():
    print("=" * 50)
    print("🤖 JOB ALERT AGENT STARTING")
    print("=" * 50)

    # 1. Scrape all sources
    all_jobs = get_all_jobs()

    # 2. Filter only new (unseen) jobs
    new_jobs = get_new_jobs(all_jobs)

    print(f"\n📊 Results:")
    print(f"   Total scraped : {len(all_jobs)}")
    print(f"   New jobs      : {len(new_jobs)}")

    if new_jobs:
        govt = [j for j in new_jobs if j.get("type") == "GOVT"]
        pvt  = [j for j in new_jobs if j.get("type") == "PRIVATE"]
        print(f"   Govt jobs     : {len(govt)}")
        print(f"   Private jobs  : {len(pvt)}")

    print("\n📤 Sending notifications...")

    # 3. Send via Telegram
    notify_telegram(new_jobs)

    # 4. Send via Email
    notify_email(new_jobs)

    print("\n✅ Job Alert Agent finished!")
    print("=" * 50)


if __name__ == "__main__":
    main()
