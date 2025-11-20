"""
filter_api.py
Advanced filtering functions for job data.
"""

from datetime import datetime, timedelta


# =====================================================
# 1. Filter by SKILL (tags)
# =====================================================
def filter_by_skill(jobs, skill):
    skill = skill.lower()
    filtered = []

    for job in jobs:
        tags = job.get("tags") or []
        tags = [t.lower() for t in tags]

        if skill in tags:
            filtered.append(job)

    return filtered


# =====================================================
# 2. Filter by KEYWORD in TITLE
# =====================================================
def filter_by_keyword(jobs, keyword):
    keyword = keyword.lower()
    return [job for job in jobs if keyword in (job.get("title") or "").lower()]


# =====================================================
# 3. Filter by SENIORITY
# =====================================================
def filter_by_seniority(jobs, level):
    level = level.lower()  # 'junior' / 'mid' / 'senior'
    return [job for job in jobs if level in (job.get("title") or "").lower()]


# =====================================================
# 4. Filter by LOCATION
# =====================================================
def filter_by_location(jobs, location):
    """
    Filters jobs by location tag:
    'india', 'usa', 'europe', 'remote', 'worldwide'
    """
    location = location.lower()
    filtered = []

    for job in jobs:
        # RemoteOK stores locations inside "location" or "tags"
        job_loc = (job.get("location") or "").lower()
        tags = [t.lower() for t in (job.get("tags") or [])]

        if location in job_loc or location in tags:
            filtered.append(job)

    return filtered


# =====================================================
# 5. Filter by DATE (fresh jobs)
# =====================================================
def filter_by_date(jobs, days=1):
    """
    Returns jobs posted in the last 'days' number of days.
    Many APIs include 'epoch' timestamp.
    """
    filtered = []
    now = datetime.utcnow()

    for job in jobs:
        epoch = job.get("epoch")
        if not epoch:
            continue

        job_date = datetime.utcfromtimestamp(epoch)
        delta = now - job_date

        if delta.days <= days:
            filtered.append(job)

    return filtered


# =====================================================
# 6. Filter by SALARY TAG
# =====================================================
def filter_by_salary_tag(jobs):
    """
    Filters jobs that have any salary-related tags:
    e.g., '$', 'k', 'USD', 'EUR'
    """
    salary_keywords = ["$", "k", "usd", "eur", "salary"]

    filtered = []
    for job in jobs:
        tags = " ".join(job.get("tags") or []).lower()

        if any(keyword in tags for keyword in salary_keywords):
            filtered.append(job)

    return filtered


# =====================================================
# 7. MULTI-SKILL FILTER
# =====================================================
def filter_multi_skill(jobs, skills):
    """
    skills = ['python', 'backend']
    Job must contain ALL listed skills.
    """
    skills = [s.lower() for s in skills]
    filtered = []

    for job in jobs:
        tags = [t.lower() for t in (job.get("tags") or [])]

        # all required skills must exist in tags
        if all(skill in tags for skill in skills):
            filtered.append(job)

    return filtered
