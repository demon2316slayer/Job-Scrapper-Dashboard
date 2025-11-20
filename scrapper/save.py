"""
save.py
Handles saving extracted job data to JSON, CSV, and Excel files.
"""

import json
import csv
from openpyxl import Workbook


# ===============================
#   SAVE TO JSON
# ===============================
def save_to_json(jobs, filename="jobs.json"):
    """
    Save job list to a JSON file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=4, ensure_ascii=False)
        print(f"[OK] Saved JSON to {filename}")
    except Exception as e:
        print(f"[ERROR] Failed to save JSON: {e}")


# ===============================
#   SAVE TO CSV
# ===============================
def save_to_csv(jobs, filename="jobs.csv"):
    """
    Save job list to a CSV file.
    """
    try:
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)

            # Header row
            writer.writerow(["title", "company", "tags", "url"])

            # Data rows
            for job in jobs:
                writer.writerow([
                    job.get("title"),
                    job.get("company"),
                    ", ".join(job.get("tags") or []),
                    job.get("url")
                ])

        print(f"[OK] Saved CSV to {filename}")

    except Exception as e:
        print(f"[ERROR] Failed to save CSV: {e}")


# ===============================
#   SAVE TO EXCEL (.xlsx)
# ===============================
def save_to_excel(jobs, filename="jobs.xlsx"):
    """
    Save job list to an Excel (.xlsx) file.
    """
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Jobs"

        # Header row
        ws.append(["Title", "Company", "Tags", "URL"]) #Adding new row

        # Data rows
        for job in jobs:
            ws.append([
                job.get("title"),
                job.get("company"),
                ", ".join(job.get("tags") or []),
                job.get("url")
            ])

        wb.save(filename)
        print(f"[OK] Saved Excel file to {filename}")

    except Exception as e:
        print(f"[ERROR] Failed to save Excel: {e}")
