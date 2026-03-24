"""
Job Alert Agent - Multi-source Job Scraper
Scrapes: Sarkari Result, NCS Portal, Freshersworld, LinkedIn (public), TimesJobs
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import hashlib
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

SEEN_JOBS_FILE = "seen_jobs.json"


def load_seen_jobs():
    if os.path.exists(SEEN_JOBS_FILE):
        with open(SEEN_JOBS_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen_jobs(seen_jobs):
    with open(SEEN_JOBS_FILE, "w") as f:
        json.dump(list(seen_jobs), f)


def job_id(job):
    """Create a unique hash for a job to avoid duplicate alerts."""
    key = f"{job['title']}|{job['company']}|{job['source']}"
    return hashlib.md5(key.encode()).hexdigest()


# ─────────────────────────────────────────────
# GOVT JOB SOURCES
# ─────────────────────────────────────────────

def scrape_sarkari_result():
    """Scrapes latest govt job listings from SarkariResult."""
    jobs = []
    try:
        url = "https://www.sarkariresult.com/"
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        # Latest jobs table
        for row in soup.select("table#table1 tr"):
            cols = row.find_all("td")
            if len(cols) >= 2:
                title_tag = cols[0].find("a")
                if title_tag:
                    jobs.append({
                        "title": title_tag.get_text(strip=True),
                        "company": "Government of India",
                        "link": title_tag.get("href", url),
                        "source": "SarkariResult",
                        "type": "GOVT",
                        "date": cols[1].get_text(strip=True) if len(cols) > 1 else "N/A",
                    })
    except Exception as e:
        print(f"[SarkariResult] Error: {e}")
    return jobs[:15]


def scrape_ncs_portal():
    """Scrapes NCS (National Career Service) Portal - Official Govt job portal."""
    jobs = []
    try:
        # NCS public job search API
        url = "https://www.ncs.gov.in/JobSearch/SearchJobs"
        params = {
            "Keywords": "",
            "Location": "",
            "Sector": "0",
            "pageNo": 1,
        }
        res = requests.get(url, headers=HEADERS, params=params, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        for card in soup.select(".job-detail-left"):
            title = card.select_one("h4 a")
            company = card.select_one(".comp-name")
            location = card.select_one(".loc")
            link_tag = card.select_one("h4 a")

            if title:
                jobs.append({
                    "title": title.get_text(strip=True),
                    "company": company.get_text(strip=True) if company else "Govt Organization",
                    "location": location.get_text(strip=True) if location else "India",
                    "link": "https://www.ncs.gov.in" + link_tag.get("href", "") if link_tag else "https://www.ncs.gov.in",
                    "source": "NCS Portal",
                    "type": "GOVT",
                    "date": datetime.today().strftime("%d %b %Y"),
                })
    except Exception as e:
        print(f"[NCS Portal] Error: {e}")
    return jobs[:15]


def scrape_employment_news():
    """Scrapes Employment News - Official GOI weekly job paper."""
    jobs = []
    try:
        url = "https://www.employmentnews.gov.in/NewVer/Pages/JobsinGovernment.aspx"
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        for row in soup.select("table tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 3:
                title_tag = cols[0].find("a")
                jobs.append({
                    "title": cols[0].get_text(strip=True),
                    "company": cols[1].get_text(strip=True),
                    "link": title_tag.get("href", url) if title_tag else url,
                    "source": "Employment News (GOI)",
                    "type": "GOVT",
                    "date": cols[2].get_text(strip=True) if len(cols) > 2 else "N/A",
                })
    except Exception as e:
        print(f"[Employment News] Error: {e}")
    return jobs[:15]


# ─────────────────────────────────────────────
# PRIVATE / IT JOB SOURCES
# ─────────────────────────────────────────────

def scrape_timesjobs():
    """Scrapes TimesJobs for IT and private sector jobs."""
    jobs = []
    try:
        # Read keywords from config
        keywords = os.getenv("JOB_KEYWORDS", "software developer,data analyst,python").split(",")
        location = os.getenv("JOB_LOCATION", "Bengaluru")

        for keyword in keywords[:3]:  # Limit to avoid rate limiting
            url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={keyword.strip()}&txtLocation={location}"
            res = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.text, "html.parser")

            for card in soup.select("li.clearfix.job-bx"):
                title = card.select_one("h2 a")
                company = card.select_one("h3.joblist-comp-name")
                skills = card.select_one("span.srp-skills")
                date = card.select_one("span.sim-posted")

                if title:
                    jobs.append({
                        "title": title.get_text(strip=True),
                        "company": company.get_text(strip=True) if company else "N/A",
                        "skills": skills.get_text(strip=True) if skills else "",
                        "link": title.get("href", "https://www.timesjobs.com"),
                        "source": "TimesJobs",
                        "type": "PRIVATE",
                        "date": date.get_text(strip=True) if date else "N/A",
                    })
    except Exception as e:
        print(f"[TimesJobs] Error: {e}")
    return jobs[:20]


def scrape_freshersworld():
    """Scrapes Freshersworld for fresher jobs."""
    jobs = []
    try:
        url = "https://www.freshersworld.com/jobs/freshers"
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")

        for card in soup.select(".job-container"):
            title = card.select_one("h3 a")
            company = card.select_one(".company-name")
            location = card.select_one(".location")

            if title:
                jobs.append({
                    "title": title.get_text(strip=True),
                    "company": company.get_text(strip=True) if company else "N/A",
                    "location": location.get_text(strip=True) if location else "India",
                    "link": "https://www.freshersworld.com" + title.get("href", ""),
                    "source": "Freshersworld",
                    "type": "PRIVATE",
                    "date": datetime.today().strftime("%d %b %Y"),
                })
    except Exception as e:
        print(f"[Freshersworld] Error: {e}")
    return jobs[:15]


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def get_all_jobs():
    """Aggregate jobs from all sources."""
    print("🔍 Scraping job sources...")
    all_jobs = []

    scrapers = [
        ("Sarkari Result", scrape_sarkari_result),
        ("NCS Portal", scrape_ncs_portal),
        ("Employment News", scrape_employment_news),
        ("TimesJobs", scrape_timesjobs),
        ("Freshersworld", scrape_freshersworld),
    ]

    for name, scraper in scrapers:
        print(f"  ↳ {name}...", end=" ")
        jobs = scraper()
        all_jobs.extend(jobs)
        print(f"✅ {len(jobs)} jobs found")

    return all_jobs


def get_new_jobs(all_jobs):
    """Filter out already-seen jobs."""
    seen = load_seen_jobs()
    new_jobs = []

    for job in all_jobs:
        jid = job_id(job)
        if jid not in seen:
            new_jobs.append(job)
            seen.add(jid)

    save_seen_jobs(seen)
    return new_jobs


if __name__ == "__main__":
    jobs = get_all_jobs()
    new = get_new_jobs(jobs)
    print(f"\n📋 Total: {len(jobs)} | 🆕 New: {len(new)}")
    for j in new[:5]:
        print(f"  [{j['type']}] {j['title']} @ {j['company']} — {j['source']}")
