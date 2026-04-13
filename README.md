# 🤖 Job Alert Agent

Automatically scrapes **Govt + Private job listings** daily and sends you alerts via **Telegram** and **Gmail** — 100% free using GitHub Actions.

---

## 📡 Sources Scraped

### 🏛️ Government

| Source | Notes |
|---|---|
| [SarkariResult](https://sarkariresult.com) | Most popular govt job aggregator in India |
| [NCS Portal](https://ncs.gov.in) | Official Govt of India job portal |
| [Employment News](https://employmentnews.gov.in) | Official GOI weekly job paper |
| [FreeJobAlert](https://freejobalert.com) | Updated multiple times daily, very comprehensive |
| [RojgarResult](https://rojgarresult.com) | Strong coverage of state-level jobs (UP, Bihar, MP, Rajasthan) |
| [UPSC](https://upsc.gov.in) | Union Public Service Commission — active recruitments |
| [SSC](https://ssc.nic.in) | Staff Selection Commission — latest notifications |
| [RRB](https://rrbcdg.gov.in) | Railway Recruitment Board — one of India's largest employers |
| [IBPS](https://ibps.in) | Banking jobs — PO, Clerk, SO, RRB |

### 🏢 Private / IT

| Source | Notes |
|---|---|
| [LinkedIn](https://linkedin.com/jobs) | Public job listings — largest professional network |
| [Naukri](https://naukri.com) | India's #1 job portal (via RSS feeds) |
| [Shine](https://shine.com) | IT, BPO, and management roles |
| [TimesJobs](https://timesjobs.com) | IT and corporate jobs |

---

## ⚙️ How It Works

```
1. Scrape all sources (Govt + Private)
2. Compare against seen_jobs.json → filter only NEW jobs
3. Send alerts via Telegram + Gmail
4. Save seen jobs to avoid duplicates next run
```

Runs automatically every day at **8:00 AM IST** via GitHub Actions, or trigger it manually anytime.

---

## 🚀 Setup Guide

### Step 1 — Fork / Clone This Repo

```bash
git clone https://github.com/Boredletsgo/Job_alert.git
cd Job_alert
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Set Up Telegram Bot (Free)

1. Open Telegram → Search **@BotFather**
2. Send `/newbot` → give it a name like "My Job Alert Bot"
3. BotFather gives you a **TOKEN** like `123456:ABCdef...` → save it
4. Open your bot in Telegram, send `/start`
5. Go to: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
6. Find `"chat":{"id": 123456789}` → that's your **CHAT_ID**

### Step 4 — Set Up Gmail App Password (Free)

1. Go to your Google Account → **Security**
2. Enable **2-Step Verification** if not already done
3. Search **"App passwords"** → Create one for "Mail"
4. Save the **16-character password** shown (e.g., `abcd efgh ijkl mnop`)

### Step 5 — Add GitHub Secrets

In your GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID |
| `GMAIL_USER` | your.email@gmail.com |
| `GMAIL_APP_PASSWORD` | 16-char Gmail app password |
| `ALERT_EMAIL` | Email to receive alerts (can be same as GMAIL_USER) |

### Step 6 — Customize Job Search (Optional)

In **Settings → Variables → New repository variable**:

| Variable | Default | Example |
|---|---|---|
| `JOB_KEYWORDS` | `software developer,data analyst,python developer` | `civil engineer,SSC,UPSC` |
| `JOB_LOCATION` | `Bengaluru` | `Delhi,Mumbai` |

### Step 7 — Run It

**Locally:**
```bash
python main.py
```

**Via GitHub Actions:**
1. Go to **Actions tab** → **Job Alert Agent** → **Run workflow**
2. Check your Telegram and Email within 2 minutes!

The workflow also runs **automatically every day at 8:00 AM IST**.

---

## 📁 Project Structure

```
Job_alert/
├── job_alert.yml              ← GitHub Actions workflow (runs daily)
├── job_scraper.py             ← All website scrapers (Govt + Private)
├── telegram_notifier.py       ← Telegram Bot alerts
├── email_notifier.py          ← Gmail SMTP alerts
├── main.py                    ← Entry point
├── seen_jobs.json             ← Tracks already-seen jobs (auto-managed)
├── requirements.txt           ← Python dependencies
└── README.md
```

---

## 🛠️ Tech Stack

- **Python 3.11+** — core language
- **BeautifulSoup4** — HTML parsing for web scraping
- **Requests** — HTTP client
- **xml.etree.ElementTree** — RSS/XML feed parsing (Naukri)
- **GitHub Actions** — free daily scheduling (cron)
- **Telegram Bot API** — instant mobile notifications
- **Gmail SMTP** — email alerts with HTML formatting

---

## 🐛 Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'bs4'` | Dependencies not installed | Run `pip install -r requirements.txt` |
| `TELEGRAM_BOT_TOKEN not set` | Env vars missing locally | Set secrets in GitHub Actions; locally this is expected |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Corporate proxy intercepting HTTPS | Add `verify=False` to `requests.get()` calls |
| `XML parse error` (Naukri) | RSS feed format changed | Switch XML parsing to BeautifulSoup |
| A scraper returns 0 jobs | Website HTML structure changed | Inspect the site and update CSS selectors |

---

## 📜 License

This is a personal learning project. Feel free to fork and customize!

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
