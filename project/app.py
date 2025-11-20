import sys, os, io, json
from datetime import datetime
import pandas as pd
import streamlit as st

# Fix module import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapper.fetch_api import fetch_jobs_api
from scrapper.parse_api import parse_data
from scrapper.filter import (
    filter_by_skill, filter_by_keyword, filter_by_seniority,
    filter_by_location, filter_by_date, filter_by_salary_tag, filter_multi_skill
)

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(page_title="Job Finder", layout="wide")

# ----------------------------------------------------
# SESSION STATE (KEEP DATA PERSISTENT)
# ----------------------------------------------------
if "jobs" not in st.session_state:
    st.session_state["jobs"] = []

# ----------------------------------------------------
# HELPERS
# ----------------------------------------------------
def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")

def to_excel_bytes(df):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    buf.seek(0)
    return buf.read()

@st.cache_data(ttl=300)
def fetch_and_parse():
    data = fetch_jobs_api()
    if not data:
        return []
    return parse_data(data)

def jobs_to_df(jobs):
    return pd.DataFrame([{
        "title": job["title"],
        "company": job["company"],
        "tags": ", ".join(job["tags"]),
        "url": job["url"]
    } for job in jobs])

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------
st.sidebar.header("📁 Data Loading")

if st.sidebar.button("🔥 Fetch Latest Jobs (API)"):
    with st.spinner("Fetching jobs..."):
        st.session_state["jobs"] = fetch_and_parse()
    st.sidebar.success(f"Loaded {len(st.session_state['jobs'])} jobs")

st.sidebar.markdown("---")
st.sidebar.header("🔍 Filters")

skill = st.sidebar.text_input("Skill / Tag")
keyword = st.sidebar.text_input("Keyword in Title")
seniority = st.sidebar.selectbox("Seniority", ("None", "junior", "mid", "senior"))
location = st.sidebar.text_input("Location")
days = st.sidebar.slider("Posted in last X days", 0, 30, 30)
salary_only = st.sidebar.checkbox("Salary Tagged Only")
multi = st.sidebar.text_input("Multi-skill (comma separated)")

# ----------------------------------------------------
# FILTERING LOGIC
# ----------------------------------------------------
jobs = st.session_state["jobs"][:]
filtered = jobs

if skill.strip():
    filtered = filter_by_skill(filtered, skill)

if keyword.strip():
    filtered = filter_by_keyword(filtered, keyword)

if seniority != "None":
    filtered = filter_by_seniority(filtered, seniority)

if location.strip():
    filtered = filter_by_location(filtered, location)

if days:
    filtered = filter_by_date(filtered, days)

if salary_only:
    filtered = filter_by_salary_tag(filtered)

if multi.strip():
    skills = [x.strip() for x in multi.split(",")]
    filtered = filter_multi_skill(filtered, skills)

# ----------------------------------------------------
# SEARCH BAR (TOP)
# ----------------------------------------------------
st.title("🧭 Job Finder Dashboard")

search = st.text_input("Search (title / company / tags)")

if search.strip():
    q = search.lower()
    filtered = [
        job for job in filtered
        if q in job["title"].lower()
        or q in job["company"].lower()
        or any(q in tag.lower() for tag in job["tags"])
    ]

# ----------------------------------------------------
# STATS
# ----------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Loaded", len(jobs))
col2.metric("After Filters", len(filtered))
col3.metric("Companies", len({j["company"] for j in filtered}))

st.markdown("---")

# ----------------------------------------------------
# TABLE VIEW
# ----------------------------------------------------
df = jobs_to_df(filtered)
st.subheader("📄 Table View")
st.dataframe(df, use_container_width=True)

# ----------------------------------------------------
# SIMPLE CARD VIEW (MINIMAL NICE BOXES)
# ----------------------------------------------------
st.markdown("---")
st.subheader("💼 Job Cards")

for job in filtered:
    with st.container(border=True):
        st.markdown(f"### {job['title']}")
        st.markdown(f"**{job['company']}**")
        st.markdown(f"📝 *Tags:* `{', '.join(job['tags'])}`")
        st.markdown(f"[🌐 Apply Link]({job['url']})")

# ----------------------------------------------------
# DOWNLOADS
# ----------------------------------------------------
st.markdown("---")
st.subheader("📥 Download")

c1, c2, c3 = st.columns(3)

with c1:
    st.download_button("CSV", to_csv_bytes(df), "jobs.csv", "text/csv")

with c2:
    st.download_button("Excel", to_excel_bytes(df), "jobs.xlsx")

with c3:
    st.download_button(
        "JSON",
        json.dumps(filtered, indent=2).encode("utf-8"),
        "jobs.json",
        "application/json"
    )
