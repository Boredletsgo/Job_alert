"""
Job Alert Agent - Complete Job Scraper (Updated)
Sources:
  GOVT  → SarkariResult, NCS Portal, Employment News, FreeJobAlert,
           RojgarResult, UPSC, SSC, RRB, IBPS
  PRIVATE → TimesJobs, Freshersworld, Naukri, Indeed India, Shine
"""
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import json
import os
import hashlib
import time
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        soup = BeautifulSoup(res.content, "html.parser")
        for item in soup.find_all("item"):
            title = item.find("title").get_text(strip=True) if item.find("title") else ""
            link = item.find("link").get_text(strip=True) if item.find("link") else ""
            company = item.find("company").get_text(strip=True) if item.find("company") else "Government of India"
            date = item.find("pubDate").get_text(strip=True) if item.find("pubDate") else "N/A"
            jobs.append({
                "title": title,
                "company": company,
                "link": link,
                "source": "SarkariResult",
                "type": "GOVT",
                "date": date,
            })
    except Exception as e:
        print(f"[SarkariResult] Error: {e}")
    return jobs[:15]


def scrape_ncs_portal():
    jobs = []
    try:
        url = "https://www.ncs.gov.in/JobSearch/SearchJobs"
        res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        soup = BeautifulSoup(res.content, "html.parser")
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
        res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        soup = BeautifulSoup(res.content, "html.parser")
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
        res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        soup = BeautifulSoup(res.content, "html.parser")
        for row in soup.find_all("item"):
            title = row.find("title").get_text(strip=True) if row.find("title") else ""
            link = row.find("link").get_text(strip=True) if row.find("link") else ""
            company = row.find("company").get_text(strip=True) if row.find("company") else "Govt Organization"
            date = row.find("pubDate").get_text(strip=True) if row.find("pubDate") else "N/A"
            jobs.append({
                "title": title,
                "company": company,
                "link": link,
                "source": "FreeJobAlert",
                "type": "GOVT",
                "date": date,
            })
    except Exception as e:
        print(f"[FreeJobAlert] Error: {e}")
    return jobs[:20]


def scrape_rojgar_result():
    """RojgarResult — strong coverage of state-level jobs (UP, Bihar, MP, Rajasthan)."""
    jobs = []
    try:
        url = "https://rojgarresult.com/latest-jobs/"
        res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        soup = BeautifulSoup(res.content, "html.parser")
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
        res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        soup = BeautifulSoup(res.content, "html.parser")
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
        res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        soup = BeautifulSoup(res.content, "html.parser")
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
        res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        soup = BeautifulSoup(res.content, "html.parser")
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
        res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
        soup = BeautifulSoup(res.content, "html.parser")
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
    """
    Scrapes Naukri via RSS feeds — bypasses all bot detection.
    Naukri provides RSS for any keyword/location search.
    Feed URL format:
      https://www.naukri.com/rss/jobsearch/it-jobs?src=directSearch&k=<keyword>&l=<location>&...
    """
    jobs = []
    keywords = os.getenv("JOB_KEYWORDS", "python developer,data analyst,software engineer").split(",")
    location  = os.getenv("JOB_LOCATION", "Bengaluru")

    # Build one RSS feed URL per keyword
    rss_urls = []
    for keyword in keywords[:4]:  # max 4 to avoid rate limits
        kw = keyword.strip().replace(" ", "%20")
        loc = location.strip().replace(" ", "%20")
        rss_urls.append(
            f"https://www.naukri.com/rss/jobsearch/it-jobs"
            f"?src=directSearch&k={kw}&l={loc}&experience=0&afdlc=0"
        )

    for url in rss_urls:
        try:
            res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
            if res.status_code != 200:
                print(f"[Naukri RSS] HTTP {res.status_code} for {url}")
                continue

            # Parse the RSS/XML
            root = ET.fromstring(res.content)
            channel = root.find("channel")
            if channel is None:
                continue

            for item in channel.findall("item"):
                title   = item.findtext("title", "").strip()
                link    = item.findtext("link", "").strip()
                company = item.findtext("company", "").strip()
                pubdate = item.findtext("pubDate", "").strip()
                loc_tag = item.findtext("location", location).strip()
                exp_tag = item.findtext("experience", "").strip()

                # Naukri RSS puts company inside description sometimes
                if not company:
                    desc = item.findtext("description", "")
                    # Try to pull company from description text
                    if "Company:" in desc:
                        company = desc.split("Company:")[1].split("<")[0].strip()

                if title and link:
                    jobs.append({
                        "title":      title,
                        "company":    company or "N/A",
                        "location":   loc_tag,
                        "experience": exp_tag,
                        "link":       link,
                        "source":     "Naukri",
                        "type":       "PRIVATE",
                        "date":       pubdate or datetime.today().strftime("%d %b %Y"),
                    })

        except ET.ParseError as e:
            print(f"[Naukri RSS] XML parse error: {e}")
        except Exception as e:
            print(f"[Naukri RSS] Error: {e}")

    print(f"[Naukri RSS] Found {len(jobs[:25])} jobs")
    return jobs[:25]


if __name__ == "__main__":
    print("Testing Naukri RSS...")
    jobs = scrape_naukri()
    print(f"Naukri: {len(jobs)} jobs found")
    for j in jobs[:3]:
        print(f"  → {j['title']} @ {j['company']} | {j['location']}")


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
            res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
            soup = BeautifulSoup(res.text, "html.parser")

            for card in soup.select("div[data-card-index]"):

                # For child elements, use partial class match:
                title_tag = card.select_one("a[class*='jobCardNova']")
                company_tag = card.select_one("[class*='companyName']")  # inspect to confirm
                loc_tag = card.select_one("[class*='bigCardLocation']")
                exp_tag = card.select_one("[class*='bigCardExperience']")

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
            res = requests.get(url, headers=HEADERS, timeout=15, verify=False)
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
        ("Shine",               scrape_shine),
        ("TimesJobs",           scrape_timesjobs),
        ("LinkedIn",            scrape_linkedin),
        ("Internshala",         scrape_internshala),
        ("RemoteOK",            scrape_remoteok),
        ("Wellfound",           scrape_wellfound),
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

def scrape_linkedin():
    """LinkedIn Jobs — public job listings (no login required)."""
    jobs = []
    keywords = os.getenv("JOB_KEYWORDS", "software developer,data analyst").split(",")
    location = os.getenv("JOB_LOCATION", "Bengaluru")

    for keyword in keywords[:3]:
        kw = keyword.strip().replace(" ", "%20")
        loc = location.strip().replace(" ", "%20")
        url = (
            f"https://www.linkedin.com/jobs/search/"
            f"?keywords={kw}&location={loc}&f_TPR=r86400&position=1&pageNum=0"
        )
        # f_TPR=r86400 = last 24 hours

        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            if res.status_code != 200:
                print(f"[LinkedIn] HTTP {res.status_code}")
                continue

            soup = BeautifulSoup(res.text, "html.parser")

            for card in soup.select("div.base-card"):
                title_tag = card.select_one("h3.base-search-card__title")
                company_tag = card.select_one("h4.base-search-card__subtitle a")
                location_tag = card.select_one("span.job-search-card__location")
                link_tag = card.select_one("a.base-card__full-link")
                date_tag = card.select_one("time")

                if title_tag:
                    jobs.append({
                        "title": title_tag.get_text(strip=True),
                        "company": company_tag.get_text(strip=True) if company_tag else "N/A",
                        "location": location_tag.get_text(strip=True) if location_tag else location,
                        "link": link_tag.get("href", "").split("?")[0] if link_tag else url,
                        "source": "LinkedIn",
                        "type": "PRIVATE",
                        "date": date_tag.get("datetime", "")[:10] if date_tag else datetime.today().strftime("%d %b %Y"),
                    })
            time.sleep(1)

        except Exception as e:
            print(f"[LinkedIn] Error: {e}")

    return jobs[:25]


def scrape_internshala():
    """Internshala — internships + fresher jobs, clean HTML structure."""
    jobs = []
    keywords = os.getenv("JOB_KEYWORDS", "software developer,data analyst").split(",")

    for keyword in keywords[:3]:
        kw = keyword.strip().replace(" ", "-").lower()
        url = f"https://internshala.com/jobs/{kw}-jobs"

        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            if res.status_code != 200:
                print(f"[Internshala] HTTP {res.status_code}")
                continue

            soup = BeautifulSoup(res.text, "html.parser")

            for card in soup.select("div.individual_internship, div.job-internship-listing"):
                title_tag = card.select_one("h3 a, a.job-title-href")
                company_tag = card.select_one("p.company-name, a.company-name")
                location_tag = card.select_one("p.location_link a, span.location_link")
                stipend_tag = card.select_one("span.desktop-text, span.stipend")

                if title_tag:
                    href = title_tag.get("href", "")
                    jobs.append({
                        "title": title_tag.get_text(strip=True),
                        "company": company_tag.get_text(strip=True) if company_tag else "N/A",
                        "location": location_tag.get_text(strip=True) if location_tag else "India",
                        "link": f"https://internshala.com{href}" if href.startswith("/") else href,
                        "source": "Internshala",
                        "type": "PRIVATE",
                        "date": datetime.today().strftime("%d %b %Y"),
                    })
            time.sleep(1)

        except Exception as e:
            print(f"[Internshala] Error: {e}")

    return jobs[:20]


def scrape_remoteok():
    """RemoteOK — remote tech jobs with a public JSON API."""
    jobs = []
    try:
        url = "https://remoteok.com/api"
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code != 200:
            print(f"[RemoteOK] HTTP {res.status_code}")
            return jobs

        data = res.json()

        # First item is metadata, skip it
        for item in data[1:]:
            title = item.get("position", "").strip()
            company = item.get("company", "").strip()
            link = item.get("url", "").strip()
            date = item.get("date", "")[:10]
            tags = ", ".join(item.get("tags", []))

            if title and link:
                jobs.append({
                    "title": title,
                    "company": company or "N/A",
                    "location": "Remote",
                    "skills": tags,
                    "link": link,
                    "source": "RemoteOK",
                    "type": "PRIVATE",
                    "date": date or datetime.today().strftime("%d %b %Y"),
                })

    except Exception as e:
        print(f"[RemoteOK] Error: {e}")

    return jobs[:25]


def scrape_wellfound():
    """Wellfound (AngelList) — startup jobs, public listings."""
    jobs = []
    keywords = os.getenv("JOB_KEYWORDS", "software developer").split(",")

    for keyword in keywords[:2]:
        kw = keyword.strip().replace(" ", "-").lower()
        url = f"https://wellfound.com/role/r/{kw}"

        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            if res.status_code != 200:
                print(f"[Wellfound] HTTP {res.status_code}")
                continue

            soup = BeautifulSoup(res.text, "html.parser")

            for card in soup.select("div.styles_jobListing____, div[data-test='StartupResult']"):
                title_tag = card.select_one("a[class*='jobTitle'], h4 a, a[data-test='job-link']")
                company_tag = card.select_one("a[class*='company'], h2 a, a[data-test='startup-link']")
                location_tag = card.select_one("span[class*='location']")

                if title_tag:
                    href = title_tag.get("href", "")
                    jobs.append({
                        "title": title_tag.get_text(strip=True),
                        "company": company_tag.get_text(strip=True) if company_tag else "N/A",
                        "location": location_tag.get_text(strip=True) if location_tag else "Remote / India",
                        "link": f"https://wellfound.com{href}" if href.startswith("/") else href,
                        "source": "Wellfound",
                        "type": "PRIVATE",
                        "date": datetime.today().strftime("%d %b %Y"),
                    })
            time.sleep(1)

        except Exception as e:
            print(f"[Wellfound] Error: {e}")

    return jobs[:20]
