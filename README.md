# 🚀 Job Alert Agent

**A serverless job intelligence pipeline that monitors 13+ government and private job portals, deduplicates listings, and delivers real-time alerts via Telegram and email — fully automated, zero-cost, zero-maintenance.**

[![Daily Job Scan](https://img.shields.io/badge/runs-daily%20at%208AM%20IST-blue)]()
[![Sources](https://img.shields.io/badge/sources-13%20portals-green)]()
[![Cost](https://img.shields.io/badge/cost-%240%2Fmonth-brightgreen)]()

---

## The Problem

Job seekers in India face a fragmented landscape — government vacancies are scattered across UPSC, SSC, RRB, IBPS, and state-level portals, while private opportunities live on LinkedIn, Naukri, Shine, and TimesJobs. Manually checking 13+ websites daily is unsustainable. Critical opportunities are missed not due to lack of qualification, but due to lack of visibility.

## The Solution

Job Alert Agent acts as a **centralized job monitoring system**. It aggregates, deduplicates, and delivers — so you never miss an opportunity.

```
┌─────────────────────────────────────────────────────┐
│              JOB ALERT AGENT PIPELINE               │
│                                                     │
│   13 Sources ──→ Scrape ──→ Deduplicate ──→ Alert   │
│   (Govt+Pvt)      │           │              │      │
│                    │      seen_jobs.json   Telegram  │
│                    │      (state store)    + Gmail   │
│                    │                                 │
│              GitHub Actions (cron)                   │
└─────────────────────────────────────────────────────┘
```

---

## Architecture & Engineering Decisions

### Why scraping over APIs?
Most Indian job portals (SarkariResult, FreeJobAlert, RojgarResult) don't offer public APIs. The system uses a **multi-strategy scraping approach** — HTML parsing via BeautifulSoup for traditional portals, and RSS/XML feed parsing for platforms that support it (Naukri). This hybrid approach maximizes coverage while respecting rate limits.

### Why JSON for state management?
The deduplication layer uses a hash-based approach — each job is fingerprinted using `MD5(title|company|source)` and stored in `seen_jobs.json`. This was a deliberate choice over a database:
- GitHub Actions can commit the state file back to the repo
- Zero infrastructure — no database provisioning needed
- Portable — the state travels with the codebase
- Idempotent — re-runs never produce duplicate alerts

### Why GitHub Actions over a server?
- **$0/month** — runs within GitHub's free tier (2,000 min/month)
- **Zero ops** — no server management, no uptime monitoring
- **Built-in secrets** — Telegram tokens and Gmail credentials stay encrypted
- **Git-native** — state persistence via auto-commit

### Why dual notification channels?
Telegram for **instant mobile push** (real-time awareness), Gmail for **structured HTML reports** (detailed review with apply links). Different consumption patterns, same data.

---

## Data Sources (13 Active Scrapers)

### Government (9 sources)

| Source | Coverage | Strategy |
|--------|----------|----------|
| [SarkariResult](https://sarkariresult.com) | India's #1 govt job aggregator | HTML parsing |
| [NCS Portal](https://ncs.gov.in) | Official Govt of India portal | HTML parsing |
| [Employment News](https://employmentnews.gov.in) | Official GOI weekly publication | HTML parsing |
| [FreeJobAlert](https://freejobalert.com) | Updated multiple times daily | HTML parsing |
| [RojgarResult](https://rojgarresult.com) | State-level jobs (UP, Bihar, MP, Rajasthan) | HTML parsing |
| [UPSC](https://upsc.gov.in) | Union Public Service Commission | HTML parsing |
| [SSC](https://ssc.nic.in) | Staff Selection Commission | HTML parsing |
| [RRB](https://rrbcdg.gov.in) | Railway Recruitment Board | Keyword filtering |
| [IBPS](https://ibps.in) | Banking — PO, Clerk, SO | Keyword filtering |

### Private / IT (4 sources)

| Source | Coverage | Strategy |
|--------|----------|----------|
| [LinkedIn](https://linkedin.com/jobs) | Largest professional network globally | HTML parsing (public listings) |
| [Naukri](https://naukri.com) | India's #1 private job portal | RSS/XML feed parsing |
| [Shine](https://shine.com) | IT, BPO, management roles | HTML parsing |
| [TimesJobs](https://timesjobs.com) | Corporate and IT roles | HTML parsing |

> The scraper registry is extensible — adding a new source requires implementing one function and registering it in the pipeline.

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Language** | Python 3.11+ | Rich ecosystem for scraping and automation |
| **Scraping** | BeautifulSoup4, Requests | Lightweight, no browser overhead |
| **Feed Parsing** | xml.etree.ElementTree | Stdlib — zero extra dependencies for RSS |
| **Scheduling** | GitHub Actions (cron) | Free, reliable, built-in secret management |
| **Notifications** | Telegram Bot API, Gmail SMTP | Free, instant, no third-party SaaS |
| **State** | JSON (hash-based dedup) | Portable, git-committable, zero infra |

**Total dependencies: 2** (`requests`, `beautifulsoup4`)

---

## Setup

### 1. Clone & Install

```bash
git clone https://github.com/Boredletsgo/Job_alert.git
cd Job_alert
pip install -r requirements.txt
```

### 2. Configure GitHub Secrets

Go to your repo → **Settings → Secrets and variables → Actions**

**Secrets** (required for notifications):

| Secret | Value |
|--------|-------|
| `TELEGRAM_BOT_TOKEN` | Bot token from [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_CHAT_ID` | Your chat ID ([how to find](https://api.telegram.org/bot<TOKEN>/getUpdates)) |
| `GMAIL_USER` | your.email@gmail.com |
| `GMAIL_APP_PASSWORD` | 16-char [app password](https://myaccount.google.com/apppasswords) |
| `ALERT_EMAIL` | Recipient email |

**Variables** (optional — customize search):

| Variable | Default | Example |
|----------|---------|---------|
| `JOB_KEYWORDS` | `software developer,data analyst,python developer` | `civil engineer,SSC,UPSC` |
| `JOB_LOCATION` | `Bengaluru` | `Delhi,Mumbai` |

### 3. Run

```bash
# Locally
python main.py

# Via GitHub Actions → Actions tab → Run workflow
```

The pipeline runs **daily at 8:00 AM IST** automatically.

---

## Project Structure

```
Job_alert/
├── main.py                 ← Pipeline orchestrator
├── job_scraper.py          ← Scraper registry (13 sources)
├── telegram_notifier.py    ← Telegram Bot integration
├── email_notifier.py       ← Gmail SMTP with HTML templates
├── job_alert.yml           ← GitHub Actions workflow (cron)
├── seen_jobs.json          ← Dedup state store (auto-generated, gitignored)
├── requirements.txt        ← Dependencies (2 packages)
└── README.md
```

---

## Sample Output

```
🤖 JOB ALERT AGENT STARTING
🔍 Scraping job sources...
  ↳ SarkariResult...  ✅ 12 jobs
  ↳ RRB Railways...   ✅ 8 jobs
  ↳ LinkedIn...       ✅ 25 jobs
  ↳ Naukri...         ✅ 18 jobs

📊 Results:
   Total scraped : 63
   New jobs      : 41
   Govt jobs     : 18
   Private jobs  : 23

📤 Sending notifications...
  ✅ Telegram: 2 messages sent
  ✅ Gmail: HTML report delivered
```

---

## Future Direction — Toward Intelligent Job Discovery

This system is intentionally designed as a **foundation for ML-powered enhancements**:

| Feature | Impact |
|---------|--------|
| **NLP-based job matching** | Move beyond keyword matching → semantic similarity between resume and job descriptions |
| **Skill gap analysis** | Compare user's skills against job requirements → recommend upskilling paths |
| **LLM-powered summarization** | Auto-generate concise job summaries from lengthy descriptions |
| **Personalized ranking** | Learn from user click/apply behavior → rank jobs by relevance |
| **Multi-language support** | Hindi/regional language job portals for broader coverage |

The modular scraper → processor → notifier pipeline makes these additions possible without architectural changes.

---

## Cost

| Component | Cost |
|-----------|------|
| GitHub Actions | Free (2,000 min/month) |
| Telegram Bot API | Free |
| Gmail SMTP | Free |
| **Total** | **$0/month** |

---

## Author

Built by **Mahima Sahu**

If this helped you, consider giving the repo a ⭐

[![GitHub](https://img.shields.io/github/stars/Boredletsgo/Job_alert?style=social)](https://github.com/Boredletsgo/Job_alert)