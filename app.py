import streamlit as st
import requests
import time

# --- Configuration ---
API_URL = "https://fastapi-project-2-task-manager-backend.onrender.com"

st.set_page_config(page_title="SimpleTask", page_icon="✅", layout="centered")

# --- CSS for Stability & Visibility ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .task-row {
        display: flex;
        align-items: center;
        padding: 10px;
        border-bottom: 1px solid #eee;
    }
    .done-text { text-decoration: line-through; color: #a0aec0; }
    </style>
    """, unsafe_allow_html=True)

# --- Robust API Helper ---
def call_api(method, path, data=None):
    try:
        url = f"{API_URL}{path}"
        if method == "GET": return requests.get(url, timeout=5)
        if method == "POST": return requests.post(url, json=data, timeout=5)
        if method == "PUT": return requests.put(url, json=data, timeout=5)
        if method == "DELETE": return requests.delete(url, timeout=5)
    except:
        return None

# --- UI Header ---
st.title("✅ Task Manager")

# 1. THE QUICK INPUT (Super Simplified)
# No more parsing or sliders. Just type and enter.
new_title = st.text_input("", placeholder="Type a task and hit Enter...", key="new_task_input")

if new_title:
    # Auto-generate a unique ID based on the exact microsecond
    payload = {
        "id": int(time.time() * 1000), 
        "title": new_title, 
        "description": "", 
        "completed": False,
        "priority": "none"  # Hardcoded so the backend doesn't crash
    }
    if call_api("POST", "/tasks/create_task", payload):
        st.toast("Added!")
        time.sleep(0.2)
        st.rerun()

st.divider()

# 2. Fetch & Display Data
response = call_api("GET", "/tasks")

if response is None or response.status_code != 200:
    st.warning("📡 Server is waking up... hang tight.")
    if st.button("Refresh"): st.rerun()
    st.stop()

# Filter out any weird backend responses
raw_data = response.json()
tasks = [t for t in raw_data if isinstance(t, dict)]

if not tasks:
    st.info("Your list is empty. Type something above!")
else:
    # Show stats simply
    done_count = len([t for t in tasks if t.get('completed')])
    st.caption(f"📊 {done_count} of {len(tasks)} tasks completed")
    
    # Sort: Newest at top
    tasks.reverse()

    for i, task in enumerate(tasks):
        t_id = task.get('id')
        t_title = task.get('title', 'Untitled')
        is_done = task.get('completed', False)

        # Unique container for each task
        with st.container():
            col1, col2, col3 = st.columns([1, 8, 1])
            
            # Checkbox Logic
            with col1:
                # Key combined with ID and index for absolute uniqueness
                if st.checkbox("", value=is_done, key=f"cb_{t_id}_{i}"):
                    if not is_done:
                        task['completed'] = True
                        call_api("PUT", f"/tasks/update_task/{t_id}", task)
                        st.rerun()
                elif is_done:
                    task['completed'] = False
                    task['priority'] = "none" # Keeping payload consistent
                    call_api("PUT", f"/tasks/update_task/{t_id}", task)
                    st.rerun()

            # Task Title
            with col2:
                if is_done:
                    st.markdown(f"<p class='done-text'>{t_title}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**{t_title}**")

            # Delete Button
            with col3:
                if st.button("🗑️", key=f"del_{t_id}_{i}"):
                    call_api("DELETE", f"/tasks/delete_task/{t_id}")
                    st.rerun()
