import streamlit as st
import requests
import pandas as pd

API_URL = "https://fastapi-project-2-task-manager-backend.onrender.com/"

st.set_page_config(page_title="TaskFlow Pro", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; }
    .task-card {
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #6c757d;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)


# --- API Helper Functions ---
def fetch_tasks():
    try:
        res = requests.get(f"{API_URL}/tasks")
        return res.json() if res.status_code == 200 else []
    except:
        st.error("⚠️ Backend Offline. Please start your FastAPI server.")
        return []


def update_task_api(task):
    requests.put(f"{API_URL}/tasks/update_task/{task['id']}", json=task)


def delete_task_api(tid):
    requests.delete(f"{API_URL}/tasks/delete_task/{tid}")


# --- Sidebar: Add New Task ---
with st.sidebar:
    st.title("🚀 TaskFlow Pro")
    st.markdown("---")
    st.subheader("🆕 Create Task")
    with st.form("new_task_form", clear_on_submit=True):
        t_id = st.number_input("Task ID", min_value=1, step=1)
        t_title = st.text_input("Title", placeholder="e.g. Finish Project")
        t_desc = st.text_area("Details")
        t_priority = st.select_slider("Priority", options=["low", "medium", "high"])

        if st.form_submit_button("Add to List"):
            payload = {"id": t_id, "title": t_title, "description": t_desc, "completed": False, "priority": t_priority}
            requests.post(f"{API_URL}/tasks/create_task", json=payload)
            st.toast("Task added successfully!", icon="✅")
            st.rerun()

# --- Main Dashboard Logic ---
tasks = fetch_tasks()
total = len(tasks)
completed = len([t for t in tasks if isinstance(t, dict) and t.get('completed')])

# 1. Top Metrics & Progress
st.title("Control Center")
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Total Tasks", total)
col_m2.metric("Completed", completed)
col_m3.metric("Pending", total - completed)

progress = (completed / total) if total > 0 else 0
st.progress(progress, text=f"Completion Progress: {int(progress * 100)}%")

# 2. Filters and Search
st.markdown("### 🔍 Filter Tasks")
c1, c2 = st.columns([2, 1])
search = c1.text_input("Search by title...", placeholder="Type to filter...")
prio_filter = c2.multiselect("Filter Priority", ["low", "medium", "high"], default=["low", "medium", "high"])

# 3. Task Display Logic
st.markdown("---")
if not tasks:
    st.info("No tasks found. Use the sidebar to add your first one!")
else:
    for task in tasks:
        if not isinstance(task, dict): continue  # Handle API error strings

        # Apply Search & Filter
        if search.lower() not in task['title'].lower(): continue
        if task['priority'] not in prio_filter: continue

        # Visual Priority Badge
        color = {"high": "#ff4b4b", "medium": "#ffa421", "low": "#28a745"}[task['priority']]

        with st.container():
            # Create a card layout
            col_check, col_txt, col_btn = st.columns([0.5, 4, 1.5])

            with col_check:
                # Toggle Status
                is_done = st.checkbox("", value=task['completed'], key=f"check_{task['id']}")
                if is_done != task['completed']:
                    task['completed'] = is_done
                    update_task_api(task)
                    st.rerun()

            with col_txt:
                st.markdown(f"**{task['title']}**")
                st.caption(f"{task['description']} | Priority: :{task['priority']}[{task['priority'].upper()}]")

            with col_btn:
                if st.button("🗑️ Delete", key=f"del_{task['id']}", use_container_width=True):
                    delete_task_api(task['id'])
                    st.toast(f"Deleted: {task['title']}")
                    st.rerun()
            st.markdown("---")
