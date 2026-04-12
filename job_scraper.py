"""
Job Alert Agent - Complete Job Scraper (Updated)
Sources:
  GOVT  → SarkariResult, NCS Portal, Employment News, FreeJobAlert,
           RojgarResult, UPSC, SSC, RRB, IBPS
  PRIVATE → TimesJobs, Freshersworld, Naukri, Indeed India, Shine
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import hashlib
import time
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
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
    key = f"{job['title']}|{job['company']}|{job['source']}"
    return hashlib.md5(key.encode()).hexdigest()


# ═════════════════════════════════════════════════════════════════
# GOVT SOURCES
# ═════════════════════════════════════════════════════════════════

def scrape_sarkari_result():
    jobs = []
    try:
        url = "https://www.sarkariresult.com/"
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
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
    jobs = []
    try:
        url = "https://www.ncs.gov.in/JobSearch/SearchJobs"
        res = requests.get(url, headers=HEADERS, timeout=15)
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


def scrape_free_job_alert():
    """FreeJobAlert.com — updated multiple times daily, very comprehensive."""
    jobs = []
    try:
        url = "https://www.freejobalert.com/latest-notifications/"
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
        for row in soup.select("table.tablesorter tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 3:
                title_tag = cols[0].find("a")
                if title_tag:
                    jobs.append({
                        "title": title_tag.get_text(strip=True)[:120],
                        "company": cols[1].get_text(strip=True) if len(cols) > 1 else "Govt Organization",
                        "link": title_tag.get("href", "https://www.freejobalert.com"),
                        "source": "FreeJobAlert",
                        "type": "GOVT",
                        "date": cols[2].get_text(strip=True) if len(cols) > 2 else "N/A",
                    })
    except Exception as e:
        print(f"[FreeJobAlert] Error: {e}")
    return jobs[:20]


def scrape_rojgar_result():
    """RojgarResult — strong coverage of state-level jobs (UP, Bihar, MP, Rajasthan)."""
    jobs = []
    try:
        url = "https://rojgarresult.com/latest-jobs/"
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
        for card in soup.select("div.post-box, article.post, div.entry-title, h2.entry-title"):
            title_tag = card.find("a")
            if title_tag:
                text = title_tag.get_text(strip=True)
                if len(text) > 10:
                    jobs.append({
                        "title": text[:120],
                        "company": "State / Central Govt",
                        "link": title_tag.get("href", "https://rojgarresult.com"),
                        "source": "RojgarResult",
                        "type": "GOVT",
                        "date": datetime.today().strftime("%d %b %Y"),
                    })
    except Exception as e:
        print(f"[RojgarResult] Error: {e}")
    return jobs[:15]


def scrape_upsc():
    """UPSC official — upsc.gov.in active recruitments."""
    jobs = []
    try:
        url = "https://www.upsc.gov.in/recruitments/active-recruitments"
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
        for row in soup.select("table tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 2:
                title_tag = cols[1].find("a") or cols[0].find("a")
                title_text = cols[1].get_text(strip=True) if len(cols) > 1 else cols[0].get_text(strip=True)
                if title_text:
                    jobs.append({
                        "title": title_text[:120],
                        "company": "UPSC — Union Public Service Commission",
                        "link": title_tag.get("href", "https://www.upsc.gov.in") if title_tag else "https://www.upsc.gov.in",
                        "source": "UPSC Official",
                        "type": "GOVT",
                        "date": cols[2].get_text(strip=True) if len(cols) > 2 else "N/A",
                    })
    except Exception as e:
        print(f"[UPSC] Error: {e}")
    return jobs[:10]


def scrape_ssc():
    """SSC official — ssc.nic.in latest notifications."""
    jobs = []
    try:
        url = "https://ssc.nic.in/Portal/LatestNews"
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
        for link_tag in soup.select("div.whatsnew a, ul.list-group a, div.news-list a, td a")[:20]:
            text = link_tag.get_text(strip=True)
            href = link_tag.get("href", "")
            if text and len(text) > 10:
                full_link = f"https://ssc.nic.in{href}" if href.startswith("/") else href
                jobs.append({
                    "title": text[:120],
                    "company": "SSC — Staff Selection Commission",
                    "link": full_link,
                    "source": "SSC Official",
                    "type": "GOVT",
                    "date": datetime.today().strftime("%d %b %Y"),
                })
    except Exception as e:
        print(f"[SSC] Error: {e}")
    return jobs[:10]


def scrape_rrb():
    """RRB — Railway Recruitment Board, one of India's largest employers."""
    jobs = []
    try:
        url = "https://www.rrbcdg.gov.in/"
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
        recruitment_keywords = ["recruitment", "vacancy", "notification", "apply", "CEN", "RRB"]
        for link_tag in soup.select("a[href]"):
            text = link_tag.get_text(strip=True)
            href = link_tag.get("href", "")
            if any(k.lower() in text.lower() for k in recruitment_keywords) and len(text) > 15:
                full_link = href if href.startswith("http") else f"https://www.rrbcdg.gov.in/{href}"
                jobs.append({
                    "title": text[:120],
                    "company": "Indian Railways — Railway Recruitment Board",
                    "link": full_link,
                    "source": "RRB Official",
                    "type": "GOVT",
                    "date": datetime.today().strftime("%d %b %Y"),
                })
    except Exception as e:
        print(f"[RRB] Error: {e}")
    return jobs[:8]


def scrape_ibps():
    """IBPS — banking jobs (PO, Clerk, SO, RRB) — very high demand."""
    jobs = []
    try:
        url = "https://www.ibps.in/"
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
        banking_keywords = ["recruitment", "notification", "vacancy", "apply", "CRP"]
        for link_tag in soup.select("div.views-row a, div.view-content a, td a, li a"):
            text = link_tag.get_text(strip=True)
            href = link_tag.get("href", "")
            if any(k.lower() in text.lower() for k in banking_keywords) and len(text) > 10:
                full_link = href if href.startswith("http") else f"https://www.ibps.in{href}"
                jobs.append({
                    "title": text[:120],
                    "company": "IBPS — Institute of Banking Personnel Selection",
                    "link": full_link,
                    "source": "IBPS Official",
                    "type": "GOVT",
                    "date": datetime.today().strftime("%d %b %Y"),
                })
    except Exception as e:
        print(f"[IBPS] Error: {e}")
    return jobs[:8]


# ═════════════════════════════════════════════════════════════════
# PRIVATE / IT SOURCES
# ═════════════════════════════════════════════════════════════════

def scrape_naukri():
    """Naukri.com — India's #1 private job portal."""
    jobs = []
    try:
        keywords = os.getenv("JOB_KEYWORDS", "python developer,data analyst,software engineer").split(",")
        location = os.getenv("JOB_LOCATION", "Bengaluru")

        for keyword in keywords[:3]:
            keyword_slug = keyword.strip().lower().replace(" ", "-")
            location_slug = location.lower().replace(" ", "-")
            url = f"https://www.naukri.com/{keyword_slug}-jobs-in-{location_slug}"

            res = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.text, "html.parser")

            for card in soup.select("article.jobTuple"):
                title_tag = card.select_one("a.title")
                company_tag = card.select_one("a.subTitle")
                exp_tag = card.select_one("li.experience span.ellipsis")
                loc_tag = card.select_one("li.location span.ellipsis")
                date_tag = card.select_one("span.fleft.postedDate")

                if title_tag:
                    jobs.append({
                        "title": title_tag.get_text(strip=True),
                        "company": company_tag.get_text(strip=True) if company_tag else "N/A",
                        "location": loc_tag.get_text(strip=True) if loc_tag else location,
                        "experience": exp_tag.get_text(strip=True) if exp_tag else "N/A",
                        "link": title_tag.get("href", "https://www.naukri.com"),
                        "source": "Naukri",
                        "type": "PRIVATE",
                        "date": date_tag.get_text(strip=True) if date_tag else datetime.today().strftime("%d %b %Y"),
                    })
            time.sleep(1)

    except Exception as e:
        print(f"[Naukri] Error: {e}")
    return jobs[:20]


def scrape_indeed_india():
    """Indeed India — broad coverage across sectors."""
    jobs = []
    try:
        keywords = os.getenv("JOB_KEYWORDS", "software developer,data analyst").split(",")
        location = os.getenv("JOB_LOCATION", "Bengaluru")

        for keyword in keywords[:2]:
            url = (
                f"https://in.indeed.com/jobs"
                f"?q={keyword.strip().replace(' ', '+')}"
                f"&l={location.replace(' ', '+')}"
            )
            res = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.text, "html.parser")

            for card in soup.select("div.job_seen_beacon"):
                title_tag = card.select_one("h2.jobTitle a")
                company_tag = card.select_one("span.companyName")
                loc_tag = card.select_one("div.companyLocation")
                date_tag = card.select_one("span.date")

                if title_tag:
                    href = title_tag.get("href", "")
                    full_link = f"https://in.indeed.com{href}" if href.startswith("/") else href
                    jobs.append({
                        "title": title_tag.get_text(strip=True).replace("new", "").strip(),
                        "company": company_tag.get_text(strip=True) if company_tag else "N/A",
                        "location": loc_tag.get_text(strip=True) if loc_tag else location,
                        "link": full_link,
                        "source": "Indeed India",
                        "type": "PRIVATE",
                        "date": date_tag.get_text(strip=True) if date_tag else "N/A",
                    })
            time.sleep(1)

    except Exception as e:
        print(f"[Indeed India] Error: {e}")
    return jobs[:15]


def scrape_shine():
    """Shine.com — strong in IT, BPO, and management roles."""
    jobs = []
    try:
        keywords = os.getenv("JOB_KEYWORDS", "software developer").split(",")
        location = os.getenv("JOB_LOCATION", "Bengaluru")

        for keyword in keywords[:2]:
            url = (
                f"https://www.shine.com/job-search/"
                f"{keyword.strip().lower().replace(' ', '-')}-jobs-in-"
                f"{location.lower().replace(' ', '-')}"
            )
            res = requests.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.text, "html.parser")

            for card in soup.select("div.jobCard"):
                title_tag = card.select_one("h3 a")
                company_tag = card.select_one("span.company-name")
                loc_tag = card.select_one("span.location")
                exp_tag = card.select_one("span.experience")

                if title_tag:
                    href = title_tag.get("href", "")
                    jobs.append({
                        "title": title_tag.get_text(strip=True),
                        "company": company_tag.get_text(strip=True) if company_tag else "N/A",
                        "location": loc_tag.get_text(strip=True) if loc_tag else location,
                        "experience": exp_tag.get_text(strip=True) if exp_tag else "N/A",
                        "link": f"https://www.shine.com{href}" if href.startswith("/") else href,
                        "source": "Shine",
                        "type": "PRIVATE",
                        "date": datetime.today().strftime("%d %b %Y"),
                    })
            time.sleep(1)

    except Exception as e:
        print(f"[Shine] Error: {e}")
    return jobs[:15]


def scrape_timesjobs():
    jobs = []
    try:
        keywords = os.getenv("JOB_KEYWORDS", "software developer,data analyst,python").split(",")
        location = os.getenv("JOB_LOCATION", "Bengaluru")

        for keyword in keywords[:3]:
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


# ═════════════════════════════════════════════════════════════════
# AGGREGATOR — runs all scrapers
# ═════════════════════════════════════════════════════════════════

def get_all_jobs():
    print("🔍 Scraping job sources...")
    all_jobs = []

    scrapers = [
        # ── GOVT ──────────────────────────────────────────
        ("SarkariResult",       scrape_sarkari_result),
        ("NCS Portal",          scrape_ncs_portal),
        ("Employment News",     scrape_employment_news),
        ("FreeJobAlert",        scrape_free_job_alert),
        ("RojgarResult",        scrape_rojgar_result),
        ("UPSC Official",       scrape_upsc),
        ("SSC Official",        scrape_ssc),
        ("RRB Railways",        scrape_rrb),
        ("IBPS Banking",        scrape_ibps),
        # ── PRIVATE ───────────────────────────────────────
        ("Naukri",              scrape_naukri),
        ("Indeed India",        scrape_indeed_india),
        ("Shine",               scrape_shine),
        ("TimesJobs",           scrape_timesjobs),
        ("Freshersworld",       scrape_freshersworld),
    ]

    for name, scraper in scrapers:
        print(f"  ↳ {name}...", end=" ", flush=True)
        try:
            jobs = scraper()
            all_jobs.extend(jobs)
            print(f"✅ {len(jobs)} jobs")
        except Exception as e:
            print(f"❌ failed ({e})")

    return all_jobs


def get_new_jobs(all_jobs):
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
    govt = [j for j in new if j.get("type") == "GOVT"]
    pvt  = [j for j in new if j.get("type") == "PRIVATE"]
    print(f"   🏛️  Govt: {len(govt)}  |  🏢 Private: {len(pvt)}")
