import streamlit as st
import requests
import time

# --- Configuration ---
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

def create_task_api(payload):
    requests.post(f"{API_URL}/tasks/create_task", json=payload)

# --- Sidebar: Detailed Add ---
with st.sidebar:
    st.title("🚀 TaskFlow Pro")
    st.markdown("---")
    st.subheader("📝 Detailed Task")
    with st.form("new_task_form", clear_on_submit=True):
        t_id = int(time.time()) 
        t_title = st.text_input("Title")
        t_desc = st.text_area("Details")
        t_priority = st.select_slider("Priority", options=["low", "medium", "high"], value="medium")
        if st.form_submit_button("Add to List"):
            if t_title:
                create_task_api({"id": t_id, "title": t_title, "description": t_desc, "completed": False, "priority": t_priority})
                st.toast("Task added!", icon="✅")
                time.sleep(0.5)
                st.rerun()

# --- Main Dashboard ---
st.title("Control Center")

# 1. THE LAZY INPUT BAR (The fix you needed)
st.markdown("### ⚡ Quick Add")
lazy_val = st.text_input("Type 'Task + Priority' and hit Enter", placeholder="e.g. Call the bank high", label_visibility="collapsed")

if lazy_val:
    parts = lazy_val.split()
    # Check if the last word is a priority keyword
    if parts[-1].lower() in ["high", "medium", "low"]:
        prio = parts[-1].lower()
        title = " ".join(parts[:-1])
    else:
        prio = "medium"
        title = lazy_val
    
    # Auto-generate ID and hit the API
    create_task_api({
        "id": int(time.time()), 
        "title": title, 
        "description": "Quick add", 
        "completed": False, 
        "priority": prio
    })
    st.toast(f"Added: {title}", icon="🚀")
    time.sleep(0.5)
    st.rerun()

st.divider()

# 2. Metrics & Data Fetching
raw_tasks = fetch_tasks()
if raw_tasks is None:
    st.error("⚠️ Backend Offline. Waking up server...")
    if st.button("🔄 Refresh Now"): st.rerun()
    st.stop()

tasks = [t for t in raw_tasks if isinstance(t, dict)]
total, completed = len(tasks), len([t for t in tasks if t.get('completed')])

m1, m2, m3 = st.columns(3)
m1.metric("Total", total)
m2.metric("Done", completed)
m3.metric("Pending", total - completed)

prog_val = (completed / total) if total > 0 else 0
st.progress(prog_val, text=f"Productivity: {int(prog_val * 100)}%")

# 3. Filters
st.markdown("### 🔍 Filter")
c1, c2 = st.columns([2, 1])
search = c1.text_input("Search tasks...", placeholder="Find a task...")
prio_filter = c2.multiselect("Priority", ["low", "medium", "high"], default=["low", "medium", "high"])

# 4. Display Logic
st.markdown("---")
if not tasks:
    st.info("No tasks yet. Use the quick-add bar above!")
else:
    # Sort: Incomplete tasks first
    tasks.sort(key=lambda x: x.get('completed', False))

    for i, task in enumerate(tasks):
        if search.lower() not in task['title'].lower(): continue
        if task['priority'] not in prio_filter: continue

        is_done = task.get('completed', False)
        prio_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task['priority'], "⚪")

        with st.container():
            col_check, col_txt, col_btn = st.columns([0.5, 4, 1.5])
            
            with col_check:
                if st.checkbox("", value=is_done, key=f"c_{task['id']}_{i}"):
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
                st.caption(f"{prio_icon} {task['priority'].upper()} | {task['description']}")

            with col_btn:
                if st.button("🗑️ Delete", key=f"d_{task['id']}_{i}"):
                    delete_task_api(task['id'])
                    st.toast("Removed!")
                    time.sleep(0.5)
                    st.rerun()
            st.markdown("---")
