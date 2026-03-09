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
    .stButton>button { width: 100%; border-radius: 8px; transition: 0.3s; height: 3em; }
    .task-card {
        padding: 1rem; border-radius: 10px; background-color: white;
        border-left: 5px solid #6366f1; margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .done-text { text-decoration: line-through; color: #9ca3af; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- API Wrapper with Error Handling ---
def api_call(method, endpoint, json=None):
    try:
        url = f"{API_URL}{endpoint}"
        if method == "GET": return requests.get(url, timeout=10)
        if method == "POST": return requests.post(url, json=json, timeout=10)
        if method == "PUT": return requests.put(url, json=json, timeout=10)
        if method == "DELETE": return requests.delete(url, timeout=10)
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

# --- Main Dashboard Logic ---
st.title("🚀 TaskFlow Control Center")

# 1. THE LAZY INPUT (Improved)
with st.container():
    lazy_val = st.text_input("⚡ Quick Add (e.g., 'Buy Milk high')", key="lazy_input", placeholder="Type here and press Enter...")
    if lazy_val:
        parts = lazy_val.split()
        prio = parts[-1].lower() if parts[-1].lower() in ["high", "medium", "low"] else "medium"
        title = " ".join(parts[:-1]) if prio != "medium" or parts[-1].lower() == "medium" else lazy_val
        
        payload = {"id": int(time.time()*1000), "title": title, "description": "Quick add", "completed": False, "priority": prio}
        res = api_call("POST", "/tasks/create_task", payload)
        if res:
            st.toast(f"Task Added: {title}")
            time.sleep(0.5)
            st.rerun()

st.divider()

# 2. Data Fetching
res = api_call("GET", "/tasks")
if not res or res.status_code != 200:
    st.warning("📡 Backend is waking up... hang tight.")
    if st.button("Retry Connection"): st.rerun()
    st.stop()

raw_tasks = res.json()
tasks = [t for t in raw_tasks if isinstance(t, dict)]

# 3. Stats & Metrics
col1, col2, col3 = st.columns(3)
total = len(tasks)
done = len([t for t in tasks if t.get('completed')])
col1.metric("Total Tasks", total)
col2.metric("Work Done", done)
col3.metric("Pending", total - done)

if total > 0:
    st.progress(done/total, text=f"Progress: {int((done/total)*100)}%")

# 4. Filter Bar
st.markdown("### 🔍 Filter & Sort")
fc1, fc2 = st.columns([2, 1])
search = fc1.text_input("Search tasks...", placeholder="Search...")
prio_filter = fc2.multiselect("Priority", ["low", "medium", "high"], default=["low", "medium", "high"])

# 5. Task List Display
st.markdown("---")
if not tasks:
    st.info("Your task list is clean! Use the Quick Add bar above.")
else:
    # Sort: Incomplete tasks first, then by priority
    prio_map = {"high": 0, "medium": 1, "low": 2}
    tasks.sort(key=lambda x: (x.get('completed', False), prio_map.get(x.get('priority', 'medium'), 1)))

    for i, task in enumerate(tasks):
        if search.lower() not in task['title'].lower(): continue
        if task['priority'] not in prio_filter: continue

        is_done = task.get('completed', False)
        prio_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task['priority'], "⚪")

        with st.container():
            c1, c2, c3 = st.columns([0.5, 4, 1.5])
            
            # Checkbox: Logic updated to prevent double-rerun bugs
            with c1:
                new_status = st.checkbox("", value=is_done, key=f"check_{task['id']}_{i}")
                if new_status != is_done:
                    task['completed'] = new_status
                    api_call("PUT", f"/tasks/update_task/{task['id']}", task)
                    st.rerun()

            with c2:
                title_style = "done-text" if is_done else ""
                st.markdown(f"<span class='{title_style}'>**{task['title']}**</span>", unsafe_allow_html=True)
                st.caption(f"{prio_icon} {task['priority'].upper()} | {task['description']}")

            with c3:
                if st.button("🗑️ Delete", key=f"del_{task['id']}_{i}"):
                    api_call("DELETE", f"/tasks/delete_task/{task['id']}")
                    st.toast("Task Removed")
                    time.sleep(0.3)
                    st.rerun()
            st.markdown("---")
