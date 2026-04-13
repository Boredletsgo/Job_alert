# 🚀 Job Alert Agent

A fully automated job intelligence system that continuously monitors multiple government and private job portals, filters relevant opportunities, and delivers real-time alerts directly to your Telegram and email — all without requiring any server or paid infrastructure.

Built with a focus on automation, modularity, and zero-cost deployment, this system runs entirely on GitHub Actions and operates as a daily job pipeline.

---

## Overview

Searching for jobs across multiple platforms is repetitive, time-consuming, and inefficient. Important opportunities are often missed simply because they are scattered across different websites.

Job Alert Agent solves this by acting as a centralized monitoring system. It aggregates job listings from multiple trusted sources, processes and filters them, and ensures that only new and relevant opportunities are delivered to the user automatically.

Once configured, the system runs independently — no manual intervention required.

---

## How It Works

At its core, the system follows a simple but effective pipeline:

Job sources are scraped → data is processed and filtered → duplicates are removed → previously seen jobs are tracked → alerts are sent to the user.

The entire workflow is executed on a scheduled basis using GitHub Actions, making it completely serverless and maintenance-free.

---

## Key Capabilities

The system is designed to behave like a lightweight production pipeline rather than a standalone script.

It supports aggregation from multiple job sources, including both government and private platforms, ensuring broader coverage of opportunities. A deduplication mechanism prevents repeated alerts by tracking previously seen jobs, while a keyword-based filtering system allows basic personalization.

Notifications are delivered through both Telegram and Gmail, providing flexibility in how updates are consumed. Since the entire workflow runs on GitHub Actions, there is no need for hosting, making the system cost-efficient and easy to scale.

---

## Data Sources

The agent currently monitors a mix of official and high-traffic job platforms:

- Sarkari Result (Government job aggregator)  
- National Career Service (Government of India portal)  
- Employment News (official weekly publication)  
- TimesJobs (corporate and IT roles)  
- Freshersworld (entry-level opportunities)  

The architecture is extensible, allowing additional sources to be integrated with minimal changes.

---

## Setup 

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/job-alert-agent
cd job-alert-agent
pip install -r requirements.txt


##  Configure the required environment variables:

TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
ALERT_EMAIL=recipient_email

##   Run the project locally:
python main.py


## Automation

The system is designed to run automatically using GitHub Actions.
By default, it executes once every day at 8:00 AM IST using a cron schedule. This can be modified in the workflow configuration file depending on your preference.
This approach eliminates the need for dedicated servers, background processes, or manual execution.

##  Project Structure

The codebase follows a modular design to separate responsibilities clearly:

- scrapers/ handles data collection from different sources
- notifiers/ manages Telegram and email alerts
- main.py orchestrates the workflow
- seen_jobs.json maintains state for deduplication
- .github/workflows/ defines the automation pipeline

This structure makes the system easy to extend, maintain, and scale.


##  Extending the System

New job sources can be added by implementing a scraper function and integrating it into the aggregation pipeline.
The modular design also allows additional notification channels or filtering strategies to be introduced without affecting the core workflow.

##  Engineering Notes

The system is designed with practical constraints in mind. It uses a persistent JSON-based approach to track previously seen jobs, ensuring idempotent execution across runs.
Since it relies on web scraping, it is inherently dependent on the structure of external websites, which may require periodic updates. Additionally, the current filtering mechanism is keyword-based and can be further enhanced for better personalization.

##   Future Direction

- This project is intentionally designed to be extensible toward more intelligent features.

- Planned improvements include integrating NLP-based job matching, personalized recommendation systems, skill gap analysis, and LLM-based summarization of job descriptions.

- These additions would transform the system from a rule-based alerting tool into a more adaptive and intelligent job discovery platform.

##  Cost

The system is completely free to run:

- GitHub Actions (within free usage limits)
- Telegram Bot API
- Gmail SMTP

No hosting or paid services are required.

##   Summary

Job Alert Agent demonstrates how a simple idea can be turned into a practical, automated system using clean architecture and serverless tools.

It reflects an approach focused not just on writing code, but on building reliable, extensible, and real-world usable systems.

Author

Built by Mahima Sahu

If you found this useful, consider starring the repository.