import streamlit as st
import requests
import time

# --- Configuration ---
API_URL = "https://fastapi-project-2-task-manager-backend.onrender.com"

st.set_page_config(page_title="TaskFlow Pro", page_icon="🚀", layout="wide")

# --- Styling ---
st.markdown("""
<style>
.main { background-color: #f8f9fa; }
.stButton>button { width: 100%; border-radius: 8px; height: 3em; }
.task-container {
    padding: 1rem;
    border-radius: 10px;
    background-color: white;
    border-left: 5px solid #6366f1;
    margin-bottom: 10px;
}
.done-text { text-decoration: line-through; color: #9ca3af; }
</style>
""", unsafe_allow_html=True)

# --- API Helpers ---

def fetch_tasks():
    try:
        res = requests.get(f"{API_URL}/tasks", timeout=10)
        if res.status_code == 200:
            return res.json()
        return []
    except:
        return None

def update_task_api(task):
    try:
        requests.put(
            f"{API_URL}/tasks/update_task/{task['id']}",
            json=task,
            timeout=10
        )
    except:
        st.error("Failed to update task")

def delete_task_api(tid):
    try:
        requests.delete(
            f"{API_URL}/tasks/delete_task/{tid}",
            timeout=10
        )
    except:
        st.error("Failed to delete task")

def create_task_api(payload):
    try:
        requests.post(
            f"{API_URL}/tasks/create_task",
            json=payload,
            timeout=10
        )
    except:
        st.error("Failed to create task")

# --- Sidebar Add Task ---

with st.sidebar:

    st.title("🚀 TaskFlow Pro")
    st.markdown("---")

    st.subheader("📝 Detailed Task")

    with st.form("task_form", clear_on_submit=True):

        t_id = int(time.time())

        title = st.text_input("Title")

        desc = st.text_area("Details")

        priority = st.select_slider(
            "Priority",
            options=["low", "medium", "high"],
            value="medium"
        )

        if st.form_submit_button("Add Task"):

            if title.strip():

                create_task_api({
                    "id": t_id,
                    "title": title.strip(),
                    "description": desc,
                    "completed": False,
                    "priority": priority
                })

                st.toast("Task added!", icon="✅")

                time.sleep(0.5)

                st.rerun()

# --- Main UI ---

st.title("Control Center")

# --- Quick Add Fix (No Loop) ---

if "quick_add_value" not in st.session_state:
    st.session_state.quick_add_value = ""

st.markdown("### ⚡ Quick Add")

lazy_val = st.text_input(
    "Type 'Task + Priority' and press Enter",
    placeholder="e.g. Call bank high",
    label_visibility="collapsed",
    key="quick_add_value"
)

if lazy_val.strip():

    parts = lazy_val.strip().split()

    if len(parts) > 0 and parts[-1].lower() in ["high", "medium", "low"]:
        prio = parts[-1].lower()
        title = " ".join(parts[:-1])
    else:
        prio = "medium"
        title = lazy_val.strip()

    create_task_api({
        "id": int(time.time()),
        "title": title,
        "description": "Quick add",
        "completed": False,
        "priority": prio
    })

    st.session_state.quick_add_value = ""   # FIX

    st.toast(f"Added: {title}", icon="🚀")

    time.sleep(0.3)

    st.rerun()

st.divider()

# --- Fetch Tasks ---

raw_tasks = fetch_tasks()

if raw_tasks is None:
    st.error("⚠️ Backend offline. Try refresh.")
    if st.button("Refresh"):
        st.rerun()
    st.stop()

tasks = [t for t in raw_tasks if isinstance(t, dict)]

# --- Metrics ---

total = len(tasks)
completed = len([t for t in tasks if t.get("completed")])

m1, m2, m3 = st.columns(3)

m1.metric("Total", total)
m2.metric("Done", completed)
m3.metric("Pending", total - completed)

progress = completed / total if total else 0

st.progress(progress, text=f"Productivity {int(progress*100)}%")

# --- Filters ---

st.markdown("### 🔍 Filter")

c1, c2 = st.columns([2,1])

search = c1.text_input("Search tasks")

prio_filter = c2.multiselect(
    "Priority",
    ["low","medium","high"],
    default=["low","medium","high"]
)

# --- Display Tasks ---

st.markdown("---")

if not tasks:

    st.info("No tasks yet. Use quick add above.")

else:

    priority_order = {"high":0,"medium":1,"low":2}

    tasks.sort(
        key=lambda x: (
            x.get("completed", False),
            priority_order.get(x.get("priority","medium"),1)
        )
    )

    for i, task in enumerate(tasks):

        title = task.get("title","")
        desc = task.get("description","")
        priority = task.get("priority","medium")
        done = task.get("completed",False)

        if search.lower() not in title.lower():
            continue

        if priority not in prio_filter:
            continue

        prio_icon = {
            "high":"🔴",
            "medium":"🟡",
            "low":"🟢"
        }.get(priority,"⚪")

        with st.container():

            col1, col2, col3 = st.columns([0.5,4,1.5])

            with col1:

                new_state = st.checkbox(
                    "",
                    value=done,
                    key=f"check_{task['id']}_{i}"
                )

                if new_state != done:

                    task["completed"] = new_state

                    update_task_api(task)

                    st.rerun()

            with col2:

                style = "done-text" if done else ""

                st.markdown(
                    f"<span class='{style}'>**{title}**</span>",
                    unsafe_allow_html=True
                )

                st.caption(f"{prio_icon} {priority.upper()} | {desc}")

            with col3:

                if st.button("🗑 Delete", key=f"del_{task['id']}_{i}"):

                    delete_task_api(task["id"])

                    st.toast("Removed")

                    time.sleep(0.3)

                    st.rerun()

            st.markdown("---")
