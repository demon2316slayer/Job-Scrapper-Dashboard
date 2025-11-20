# 🧭 Remote Job Finder – Python + Streamlit Dashboard  
A clean, minimal job search dashboard built using **Python**, **Streamlit**, and the **RemoteOK API**.  
Fetch remote jobs, apply filters, search by keywords/tags, and download results in CSV/Excel/JSON formats.

---

## 🔥 Features

### ✅ 1. API Fetching
- Fetches real-time job listings from the **RemoteOK** API.
- Clean parsing with fallbacks for missing fields.

### ✅ 2. Interactive Dashboard (Streamlit)
- Minimal, clean UI.
- Sidebar filtering:
  - Skill / Tag  
  - Keyword in title  
  - Location  
  - Seniority  
  - Posted in last X days  
  - Salary-tagged jobs  
  - Multi-skill filter  
- Search bar for full-text search (title, company, tags).

### ✅ 3. Job Cards + Table View
- Simple boxed card UI:
  - Title  
  - Company  
  - Tags  
  - Apply link  
- Table view for quick browsing.

### ✅ 4. Downloads
Export filtered job data into:
- CSV  
- Excel (.xlsx)  
- JSON  

### ✅ 5. Persistent State
- Jobs remain loaded even when UI updates.
- Streamlit reruns do NOT reset data.

---

## 🧱 Project Structure

```text
project/
│
├── scrapper/
│   ├── fetch_api.py       # API call logic
│   ├── parse_api.py       # Parse & normalize API response
│   ├── filter.py          # All filtering functions
│   └── save.py            # Optional: save jobs to local JSON
│
├── app.py                 # Streamlit dashboard (main app)
└── main.py                # Backend test runner (optional)
