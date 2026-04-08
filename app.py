import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Pathfinder Pro", 
    page_icon="🚀",
    initial_sidebar_state="collapsed"  # Better for mobile start
)

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

load_data()

# --- SIDEBAR (Mobile Nav) ---
with st.sidebar:
    st.title("Settings")
    profile = st.selectbox("Profile", ["Work", "Life"])
    view = st.radio("Horizon", ["Daily", "Weekly", "Monthly", "Half-Yearly", "Yearly"])
    
    st.divider()
    
    with st.expander("📥 Bulk Upload CSV"):
        uploaded_file = st.file_uploader("Choose File", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            for _, row in df.iterrows():
                st.session_state.tasks.append({
                    "profile": row['profile'], "view": row['view'], "task": row['task'],
                    "done": False, "remarks": "", "date": get_smart_date(row['view'])
                })
            save_data()
            st.success("Imported!")

    if st.button("🧹 Clear Completed", use_container_width=True):
        st.session_state.tasks = [t for t in st.session_state.tasks if not t['done']]
        save_data()
        st.rerun()
        
    if st.button("📧 Send Report", use_container_width=True):
        st.toast("Report Sent!")

# --- MAIN UI ---
# Compact Header for Mobile
col_header, col_date = st.columns([1, 1])
col_header.subheader(f"{profile}: {view}")
col_date.metric("Target", get_smart_date(view))

# Add New Task (Full Width for thumb-tapping)
with st.container(border=True):
    new_task = st.text_input("New Task", placeholder="What's the goal?", label_visibility="collapsed")
    if st.button("➕ Add Task", use_container_width=True):
        if new_task:
            st.session_state.tasks.append({
                "profile": profile, "view": view, "task": new_task,
                "done": False, "remarks": "", "date": get_smart_date(view)
            })
            save_data()
            st.rerun()

st.divider()

# --- TASK LIST (Optimized for tap targets) ---
current_tasks = [t for t in st.session_state.tasks if t['profile'] == profile and t['view'] == view]

if not current_tasks:
    st.caption("No tasks for this period. Add one above! 🚀")

for i, task in enumerate(st.session_state.tasks):
    if task['profile'] == profile and task['view'] == view:
        with st.container(border=True):
            # Row 1: The Task Name
            if task['done']:
                st.markdown(f"✅ ~~{task['task']}~~")
                if task['remarks']:
                    st.caption(f"💬 {task['remarks']}")
            else:
                st.markdown(f"**{task['task']}**")
            
            # Row 2: Action Buttons (Large tap targets)
            c1, c2 = st.columns(2)
            
            if not task['done']:
                with c1:
                    if st.button("Finish", key=f"f_{i}", use_container_width=True):
                        # Simple remark logic within the flow
                        st.session_state[f"show_rem_{i}"] = True
                
                if st.session_state.get(f"show_rem_{i}", False):
                    rem = st.text_input("Remarks", key=f"input_{i}")
                    if st.button("Confirm Done", key=f"conf_{i}", use_container_width=True):
                        task['done'] = True
                        task['remarks'] = rem
                        save_data()
                        st.rerun()
            
            with c2:
                if st.button("🗑️ Delete", key=f"d_{i}", use_container_width=True):
                    st.session_state.tasks.pop(i)
                    save_data()
                    st.rerun()
