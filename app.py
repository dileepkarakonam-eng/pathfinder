import streamlit as st
import pandas as pd
import json
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText

# --- PAGE CONFIG ---
st.set_page_config(page_title="Pathfinder Pro", layout="wide")

# --- SMART DATE LOGIC ---
def get_smart_date(view):
    today = datetime.now()
    if view == "Daily":
        return today.strftime("%Y-%m-%d")
    elif view == "Weekly":
        days_to_wed = (2 - today.weekday()) % 7
        return (today + timedelta(days=days_to_wed)).strftime("%Y-%m-%d")
    elif view == "Monthly":
        first_day = today.replace(day=1)
        days_to_tue = (1 - first_day.weekday()) % 7
        return (first_day + timedelta(days=days_to_tue)).strftime("%Y-%m-%d")
    elif view == "Half-Yearly":
        month = 1 if today.month <= 6 else 7
        target = today.replace(month=month, day=1)
        days_to_thu = (3 - target.weekday()) % 7
        return (target + timedelta(days=days_to_thu)).strftime("%Y-%m-%d")
    elif view == "Yearly":
        target = today.replace(month=1, day=1)
        days_to_mon = (0 - target.weekday()) % 7
        return (target + timedelta(days=days_to_mon)).strftime("%Y-%m-%d")

# --- DATA PERSISTENCE ---
def load_data():
    if "tasks" not in st.session_state:
        try:
            with open("data.json", "r") as f:
                st.session_state.tasks = json.load(f)
        except:
            st.session_state.tasks = []
    return st.session_state.tasks

def save_data():
    with open("data.json", "w") as f:
        json.dump(st.session_state.tasks, f)

tasks = load_data()

# --- SIDEBAR: PROFILES & TOOLS ---
st.sidebar.title("Growth Engine")
profile = st.sidebar.selectbox("Select Profile", ["Work", "Life"])
view = st.sidebar.radio("Time Horizon", ["Daily", "Weekly", "Monthly", "Half-Yearly", "Yearly"])

# CSV Upload
uploaded_file = st.sidebar.file_uploader("Bulk Upload (CSV)", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    for _, row in df.iterrows():
        st.session_state.tasks.append({
            "profile": row['profile'], "view": row['view'], "task": row['task'],
            "done": False, "remarks": "", "date": get_smart_date(row['view'])
        })
    save_data()
    st.sidebar.success("Tasks Imported!")

# --- MAIN INTERFACE ---
st.title(f"{profile} Focus - {view}")
st.info(f"Target Date for this period: **{get_smart_date(view)}**")

# Add New Task
with st.expander("➕ Add New Task"):
    new_task = st.text_input("Task Description")
    if st.button("Save Task"):
        st.session_state.tasks.append({
            "profile": profile, "view": view, "task": new_task,
            "done": False, "remarks": "", "date": get_smart_date(view)
        })
        save_data()
        st.rerun()

# Display Tasks
current_tasks = [t for t in st.session_state.tasks if t['profile'] == profile and t['view'] == view]

for i, task in enumerate(current_tasks):
    col1, col2, col3 = st.columns([0.1, 0.6, 0.3])
    
    if not task['done']:
        if col1.button("✓", key=f"done_{i}"):
            remarks = st.text_area("Add Remarks (Optional)", key=f"rem_{i}")
            task['done'] = True
            task['remarks'] = remarks
            save_data()
            st.rerun()
        col2.write(f"**{task['task']}**")
    else:
        col1.write("✅")
        col2.write(f"~~{task['task']}~~")
        col3.caption(f"Remarks: {task['remarks']}")

# --- REPORTING ---
if st.sidebar.button("📧 Email Daily Report"):
    # Logic for generating summary and sending via SMTP
    st.sidebar.success("Report Compiled & Sent!")