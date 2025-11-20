# parse_api.py
"""
Updated parser for the new RemoteOK API format.
Handles missing fields safely, adds fallbacks, and normalizes job data.
"""

def parse_data(json_data):
    """
    Extract job info from the RemoteOK API response.
    Handles missing fields gracefully.
    """

    if not json_data or len(json_data) < 2:
        return []

    jobs = []

    # Skip index 0 (API metadata)
    for job in json_data[1:]:

        title = (
            job.get("position")
            or job.get("title")
            or "Untitled Job"
        )

        company = (
            job.get("company")
            or job.get("company_name")
            or "Unknown Company"
        )

        tags = job.get("tags") or []

        url = (
            job.get("url")
            or job.get("apply_url")
            or "#"
        )

        epoch = job.get("epoch")

        description = (
            job.get("description")
            or job.get("body")
            or ""
        )

        jobs.append({
            "title": title,
            "company": company,
            "tags": tags,
            "url": url,
            "epoch": epoch,
            "description": description,
            "location": job.get("location") or "",
            "logo": job.get("company_logo") or job.get("logo") or "",
        })

    return jobs
