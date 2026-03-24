# 🤖 Job Alert Agent

Automatically scrapes **Govt + Private job listings** daily and sends you alerts via **Telegram** and **Gmail** — 100% free using GitHub Actions.

---

## 📡 Sources Scraped

| Source | Type | Notes |
|---|---|---|
| [SarkariResult.com](https://sarkariresult.com) | 🏛️ Govt | Most popular govt job aggregator in India |
| [NCS Portal](https://ncs.gov.in) | 🏛️ Govt | Official Govt of India job portal |
| [Employment News](https://employmentnews.gov.in) | 🏛️ Govt | Official GOI weekly job paper |
| [TimesJobs](https://timesjobs.com) | 🏢 Private | IT and corporate jobs |
| [Freshersworld](https://freshersworld.com) | 🏢 Private | Entry-level and fresher jobs |

---

## 🚀 Setup Guide (Step-by-Step)

### Step 1 — Fork / Create GitHub Repo

1. Go to [github.com](https://github.com) → **New Repository**
2. Name it `job-alert-agent`
3. Upload all files from this project into the repo
4. Make sure the folder structure matches exactly

### Step 2 — Set Up Telegram Bot (Free)

1. Open Telegram → Search **@BotFather**
2. Send `/newbot` → give it a name like "My Job Alert Bot"
3. BotFather gives you a **TOKEN** like `123456:ABCdef...` → save it
4. Now open your bot in Telegram, send `/start`
5. Go to: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
6. Find `"chat":{"id": 123456789}` → that's your **CHAT_ID**

### Step 3 — Set Up Gmail App Password (Free)

1. Go to your Google Account → **Security**
2. Enable **2-Step Verification** if not already done
3. Search **"App passwords"** → Create one for "Mail"
4. Save the **16-character password** shown (e.g., `abcd efgh ijkl mnop`)

### Step 4 — Add GitHub Secrets

In your GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**

Add these secrets:

| Secret Name | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID |
| `GMAIL_USER` | your.email@gmail.com |
| `GMAIL_APP_PASSWORD` | 16-char Gmail app password |
| `ALERT_EMAIL` | Email to receive alerts (can be same) |

### Step 5 — Customize Job Search (Optional)

In **Settings → Variables → New repository variable**:

| Variable | Default | Example |
|---|---|---|
| `JOB_KEYWORDS` | `software developer,data analyst,python developer` | `civil engineer,SSC,UPSC` |
| `JOB_LOCATION` | `Bengaluru` | `Delhi,Mumbai` |

### Step 6 — Enable GitHub Actions

1. Go to **Actions tab** in your repo
2. Click **"I understand my workflows, go ahead and enable them"**
3. The agent runs **daily at 8:00 AM IST** automatically!

### Step 7 — Test It Now

1. Go to **Actions → Job Alert Agent → Run workflow**
2. Click **Run workflow** button
3. Check your Telegram and Email within 2 minutes!

---

## 📁 Project Structure

```
job-alert-agent/
├── .github/
│   └── workflows/
│       └── job_alert.yml      ← GitHub Actions (runs daily)
├── scrapers/
│   └── job_scraper.py         ← All website scrapers
├── notifiers/
│   ├── telegram_notifier.py   ← Telegram alerts
│   └── email_notifier.py      ← Gmail alerts
├── main.py                    ← Entry point
├── seen_jobs.json             ← Tracks seen jobs (auto-created)
├── requirements.txt
└── README.md
```

---

## ⏰ Schedule

The agent runs at **8:00 AM IST** every day. To change this, edit the cron in `.github/workflows/job_alert.yml`:

```yaml
- cron: "30 2 * * *"   # 2:30 AM UTC = 8:00 AM IST
```

Use [crontab.guru](https://crontab.guru) to create custom schedules.

---

## 🆓 Cost Breakdown

| Service | Cost |
|---|---|
| GitHub Actions | Free (2000 min/month free) |
| Telegram Bot | Free |
| Gmail SMTP | Free |
| Hosting | None needed |
| **Total** | **₹0 / month** |

---

## 🔧 Adding More Sources

To add a new job source, add a function in `scrapers/job_scraper.py`:

```python
def scrape_my_source():
    jobs = []
    # ... scrape logic ...
    return jobs
```

Then add it to the `scrapers` list in `get_all_jobs()`.

---

## 📬 Sample Alert (Telegram)

```
🚨 Job Alert — 23 New Jobs Found!
🏛️ Govt: 15 | 🏢 Private: 8
──────────────────────────────

🏛️ GOVERNMENT JOBS

📌 SSC CGL 2024
   🏢 Staff Selection Commission
   📅 15 Jan 2025
   🌐 Apply Here

📌 IBPS PO 2024
   🏢 Institute of Banking Personnel
   📅 20 Jan 2025
   🌐 Apply Here
```

---

## 🛠️ Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/job-alert-agent
cd job-alert-agent
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
export GMAIL_USER="your@gmail.com"
export GMAIL_APP_PASSWORD="your_app_password"

python main.py
```
