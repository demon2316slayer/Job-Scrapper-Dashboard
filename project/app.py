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
st.set_page_config(page_title="RemoteFeed Lite", layout="wide")

# ----------------------------------------------------
# BRANDING HEADER
# ----------------------------------------------------
st.markdown("""
<div style="text-align: center;">
    <h1 style="color:#0066FF; margin-bottom:0;">RemoteFeed Lite</h1>
    <p style="font-size:18px; margin-top:0;">
        Fresh curated remote jobs for your skills.<br>
        <span style="color:gray;">Your data stays private and is never shared.</span>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------------------
# SESSION STATE
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
# SIDEBAR BRANDING & PRIVACY
# ----------------------------------------------------
# NOTE: use project/logo.png so Streamlit Cloud can locate it when app is run from repo root
st.sidebar.image("project/logo.png", width=120)
st.sidebar.markdown("### RemoteFeed Lite")
st.sidebar.markdown("Your personalized remote job dashboard.")
st.sidebar.markdown(
    "<span style='color:gray;'>🔒 Your data is private and never shared.</span>",
    unsafe_allow_html=True
)
st.sidebar.markdown("---")

# ----------------------------------------------------
# SIDEBAR SUPPORT SECTION
# ----------------------------------------------------
st.sidebar.markdown("### 📬 Support")
st.sidebar.markdown("""
If you need help or have questions:

**Email:**  
📧 ay007bat@gmail.com
""")
st.sidebar.markdown("---")

# ----------------------------------------------------
# SIDEBAR CONTROLS
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
# FILTERING
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
# DASHBOARD TITLE
# ----------------------------------------------------
st.title("🧭 Job Finder Dashboard")

# ----------------------------------------------------
# PREMIUM CTA SECTION (India-only)
# ----------------------------------------------------
st.markdown("""
### 🔥 Want a Personalized Job Feed?

Get remote job listings curated exactly for **your skills**,  
**your experience level**, and **your preferred roles**.

💰 **Pricing (India Only):**  
- 🇮🇳 **₹149 / month**

👉 Pay using UPI: **7052647114@kotak811**  
Upload the payment screenshot inside the signup form.

🔒 **Your data stays private and never shared.**
""")

if st.button("Get Premium Feed"):
    st.markdown("[👉 Click here to join the Premium Feed](https://forms.gle/eAtPYDcNfgKbQxAD7)")

# ----------------------------------------------------
# SEARCH BAR
# ----------------------------------------------------
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
# CARD VIEW
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
# DOWNLOAD OPTIONS
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

# ----------------------------------------------------
# SUPPORT / CONTACT SECTION (BOTTOM OF PAGE)
# ----------------------------------------------------
st.markdown("---")
st.subheader("📬 Need Help? Contact Support")

st.markdown("""
If you have any questions about your subscription, premium feed,
payment, or want to request a **refund**, feel free to reach out.

**📧 Email:** ay007bat@gmail.com  
I usually reply within **24 hours**.
""")

# ----------------------------------------------------
# POLICIES (EXPANDERS: Refund / Terms / Privacy)
# ----------------------------------------------------
with st.expander("Refund Policy"):
    st.markdown("""
**Simple Refund Policy**

- If you receive an empty (0 match) premium feed for your exact requested filters, you may request a full refund within **7 days** of the feed delivery.
- If you are unsatisfied for any other reason, email **ay007bat@gmail.com** and we'll review your case — partial refunds or free extensions may be offered at our discretion.
- To request a refund, provide: (a) your name/email, (b) payment screenshot, (c) brief reason. We'll respond within 48 hours.
- Refunds are normally processed within 3–7 business days after approval.
""")

with st.expander("Terms of Service"):
    st.markdown("""
**Terms of Service (Summary)**

- **Service**: RemoteFeed Lite provides curated job lists based on publicly posted remote job data sources.
- **Subscription**: Monthly subscription (₹149/month) grants you personalized curated feeds. You must provide payment proof to activate.
- **Content & Liability**: Jobs are collected from third-party sources. RemoteFeed Lite is not responsible for employer actions, job offers, or hiring decisions.
- **Cancellation**: To cancel your subscription, email ay007bat@gmail.com. Cancellation will stop future curated deliveries.
- **Changes**: RemoteFeed Lite may update features or pricing; active users will be notified.
""")

with st.expander("Privacy Policy"):
    st.markdown("""
**Privacy Policy (Short & Clear)**

- **What we collect**: name, email, skills/preferences, country, and payment screenshot (only to validate subscription).
- **Where data is stored**: user signup responses are stored in your Google Form / Google Sheet. No other external storage is used.
- **How we use it**: solely to provide personalized job feeds and communicate with you regarding the service.
- **Sharing**: we DO NOT sell or share personal information with third parties.
- **Deletion**: you may request data deletion at any time by emailing ay007bat@gmail.com. We'll remove your data from the form/sheet and confirm deletion.
- **Security**: We follow reasonable practices; data is stored on Google servers via Forms/Sheets.
""")

# ----------------------------------------------------
# END
# ----------------------------------------------------
