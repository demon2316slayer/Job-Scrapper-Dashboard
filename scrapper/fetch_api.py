"""
fetch_api.py
Handles API calls to fetch job data.
"""

import requests

def fetch_jobs_api():
    """
    Fetch job data from RemoteOK API.

    Returns:
        json: Parsed JSON data (list of job entries).
    """
    url = "https://remoteok.com/api"

    try:
        response = requests.get(url)
        response.raise_for_status()  # check for errors  (if this happens it will jump to except block)

        return response.json()  # return JSON data

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed: {e}")
        return None
