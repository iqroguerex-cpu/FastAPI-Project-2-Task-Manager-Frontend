import streamlit as st
import requests
import time

# --- Configuration ---
# Removed trailing slash to prevent double-slash API errors
API_URL = "https://fastapi-project-2-task-manager-backend.onrender.com"

st.set_page_config(page_title="TaskFlow Pro", page_icon="🚀", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; transition: 0.3s; }
    .stButton>button:hover { border: 1px solid #6366f1; color: #6366f1; }
    .task-container {
        padding: 1rem;
        border-radius: 10px;
        background-color: white;
        border-left: 5px solid #6366f1;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .done-text { text-decoration: line-through; color: #9ca3af; }
    </style>
    """, unsafe_allow_html=True)

# --- API Helper Functions ---
def fetch_tasks():
    try:
        res = requests.get(f"{API_URL}/tasks", timeout=10)
        return res.json() if res.status_code == 200 else []
    except Exception:
        return None

def update_task_api(task):
    requests.put(f"{API_URL}/tasks/update_task/{task['id']}", json=task)

def delete_task_api(tid):
    requests.delete(f"{API_URL}/tasks/delete_task/{tid}")

# --- Sidebar: Smart Add ---
with st.sidebar:
    st.title("🚀 TaskFlow Pro")
    st.markdown("---")
    st.subheader("🆕 Quick Create")
    
    with st.form("new_task_form", clear_on_submit=True):
        # Auto-generate ID using timestamp to prevent duplicate key errors
        t_id = int(time.time()) 
        t_title = st.text_input("What needs doing?", placeholder="e.g. Finish project")
        t_desc = st.text_area("Details (Optional)")
        t_priority = st.select_slider("Priority", options=["low", "medium", "high"], value="medium")

        if st.form_submit_button("Add Task"):
            if t_title:
                payload = {
                    "id": t_id, 
                    "title": t_title, 
                    "description": t_desc if t_desc else "No description", 
                    "completed": False, 
                    "priority": t_priority
                }
                requests.post(f"{API_URL}/tasks/create_task", json=payload)
                st.toast("Task added!", icon="✅")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Please enter a title!")

# --- Main Dashboard ---
st.title("Control Center")
raw_tasks = fetch_tasks()

if raw_tasks is None:
    st.error("⚠️ Backend Offline or Sleeping.")
    st.info("Render's free tier takes ~1 minute to wake up. Please refresh in a moment.")
    if st.button("🔄 Refresh Now"):
        st.rerun()
    st.stop()

# Filter out non-dictionary items (like "Task Not Found" strings)
tasks = [t for t in raw_tasks if isinstance(t, dict)]

# 1. Metrics Section
total = len(tasks)
completed = len([t for t in tasks if t.get('completed')])
pending = total - completed

m1, m2, m3 = st.columns(3)
m1.metric("Total", total)
m2.metric("Done", completed)
m3.metric("To-Do", pending)

prog_val = (completed / total) if total > 0 else 0
st.progress(prog_val, text=f"Progress: {int(prog_val * 100)}%")

# 2. Search & Filters
st.markdown("### 🔍 Filter")
c1, c2 = st.columns([2, 1])
search = c1.text_input("Search tasks...", placeholder="Type to filter...")
prio_filter = c2.multiselect("Priority", ["low", "medium", "high"], default=["low", "medium", "high"])

# 3. Task Display
st.markdown("---")
if not tasks:
    st.info("No tasks found. Add one in the sidebar!")
else:
    # Sort: Incomplete tasks first
    tasks.sort(key=lambda x: x.get('completed', False))

    for i, task in enumerate(tasks):
        # Filter Logic
        if search.lower() not in task['title'].lower(): continue
        if task['priority'] not in prio_filter: continue

        is_done = task.get('completed', False)
        prio_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task['priority'], "⚪")

        # Visual Card Container
        with st.container():
            col_check, col_txt, col_btn = st.columns([0.5, 4, 1.5])

            with col_check:
                # Key is unique using ID + Index
                check_key = f"check_{task['id']}_{i}"
                if st.checkbox("", value=is_done, key=check_key):
                    if not is_done:
                        task['completed'] = True
                        update_task_api(task)
                        st.rerun()
                elif is_done:
                    task['completed'] = False
                    update_task_api(task)
                    st.rerun()

            with col_txt:
                title_style = "done-text" if is_done else ""
                st.markdown(f"<span class='{title_style}'>**{task['title']}**</span>", unsafe_allow_html=True)
                st.caption(f"{prio_color} {task['priority'].upper()} | {task['description']}")

            with col_btn:
                # Key is unique using ID + Index
                if st.button("🗑️ Delete", key=f"del_{task['id']}_{i}"):
                    delete_task_api(task['id'])
                    st.toast("Deleted!")
                    time.sleep(0.5)
                    st.rerun()
            st.markdown("---")
