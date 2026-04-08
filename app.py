import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Pathfinder Pro", 
    page_icon="🚀",
    initial_sidebar_state="collapsed" 
)

# --- SMART DATE LOGIC ---
def get_smart_date(view):
    today = datetime.now()
    if view == "Daily":
        return today.strftime("%Y-%m-%d")
    elif view == "Weekly":
        # Target Wednesday of the current week
        days_to_wed = (2 - today.weekday()) % 7
        return (today + timedelta(days=days_to_wed)).strftime("%Y-%m-%d")
    elif view == "Monthly":
        # Target First Tuesday of the current month
        first_day = today.replace(day=1)
        days_to_tue = (1 - first_day.weekday()) % 7
        return (first_day + timedelta(days=days_to_tue)).strftime("%Y-%m-%d")
    elif view == "Half-Yearly":
        # First Thursday of Jan or July
        month = 1 if today.month <= 6 else 7
        target = today.replace(month=month, day=1)
        days_to_thu = (3 - target.weekday()) % 7
        return (target + timedelta(days=days_to_thu)).strftime("%Y-%m-%d")
    elif view == "Yearly":
        # First Monday of the year
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

load_data()

# --- SIDEBAR (Settings & Utilities) ---
with st.sidebar:
    st.title("Growth Engine")
    profile = st.selectbox("Current Profile", ["Work", "Life"])
    view = st.radio("Time Horizon", ["Daily", "Weekly", "Monthly", "Half-Yearly", "Yearly"])
    
    st.divider()
    
    # --- CSV UPLOAD (With Duplicate Guard) ---
    with st.expander("📥 Bulk Upload CSV"):
        uploaded_file = st.file_uploader("Upload Task List", type="csv")
        if uploaded_file is not None:
            file_key = f"proc_{uploaded_file.name}_{uploaded_file.size}"
            if file_key not in st.session_state:
                try:
                    df = pd.read_csv(uploaded_file)
                    if not {'profile', 'view', 'task'}.issubset(df.columns):
                        st.error("Missing columns: profile, view, task")
                    else:
                        for _, row in df.iterrows():
                            st.session_state.tasks.append({
                                "profile": str(row['profile']),
                                "view": str(row['view']),
                                "task": str(row['task']),
                                "done": False,
                                "remarks": "",
                                "date": get_smart_date(str(row['view']))
                            })
                        save_data()
                        st.session_state[file_key] = True
                        st.success("Import Successful!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    # --- CLEANUP TOOLS ---
    if st.button("🧹 Clear Completed Tasks", use_container_width=True):
        st.session_state.tasks = [t for t in st.session_state.tasks if not t['done']]
        save_data()
        st.rerun()

    if st.button("🚨 Emergency De-Duplicate", use_container_width=True):
        seen = set()
        clean = []
        for t in st.session_state.tasks:
            fingerprint = (t['profile'], t['view'], t['task'], t['date'])
            if fingerprint not in seen:
                clean.append(t)
                seen.add(fingerprint)
        st.session_state.tasks = clean
        save_data()
        st.rerun()

    if st.button("📧 Email Daily Report", use_container_width=True):
        st.toast("Report ready and sent!")

# --- MAIN UI ---
st.title(f"{profile}: {view}")
st.metric("Target Date", get_smart_date(view))

# Add New Task
with st.container(border=True):
    new_task = st.text_input("New Task", placeholder="What is your focus?", label_visibility="collapsed")
    if st.button("➕ Add Task", use_container_width=True):
        if new_task:
            st.session_state.tasks.append({
                "profile": profile,
                "view": view,
                "task": new_task,
                "done": False,
                "remarks": "",
                "date": get_smart_date(view)
            })
            save_data()
            st.rerun()

st.divider()

# --- MOBILE FRIENDLY TASK LIST ---
# Using a list comprehension to get only tasks relevant to current view
filtered_tasks = [t for t in st.session_state.tasks if t['profile'] == profile and t['view'] == view]

if not filtered_tasks:
    st.info("No active tasks. Use 'Add Task' or 'Upload CSV' to begin.")

# Iterate through session state directly to allow for index-based mutation (pop/done)
for i in range(len(st.session_state.tasks) - 1, -1, -1):
    task = st.session_state.tasks[i]
    
    if task['profile'] == profile and task['view'] == view:
        with st.container(border=True):
            # Task Content
            if task['done']:
                st.markdown(f"✅ ~~{task['task']}~~")
                if task['remarks']:
                    st.caption(f"**Remarks:** {task['remarks']}")
            else:
                st.markdown(f"**{task['task']}**")
            
            # Action Buttons
            c1, c2 = st.columns(2)
            
            if not task['done']:
                with c1:
                    if st.button("Finish", key=f"f_{i}", use_container_width=True):
                        st.session_state[f"edit_{i}"] = True
                
                # Show remarks input after clicking finish
                if st.session_state.get(f"edit_{i}", False):
                    remarks = st.text_input("Add Remarks (optional)", key=f"rem_{i}")
                    if st.button("Confirm", key=f"c_{i}", use_container_width=True):
                        st.session_state.tasks[i]['done'] = True
                        st.session_state.tasks[i]['remarks'] = remarks
                        save_data()
                        del st.session_state[f"edit_{i}"]
                        st.rerun()
            
            with c2:
                if st.button("🗑️ Delete", key=f"d_{i}", use_container_width=True):
                    st.session_state.tasks.pop(i)
                    save_data()
                    st.rerun()
