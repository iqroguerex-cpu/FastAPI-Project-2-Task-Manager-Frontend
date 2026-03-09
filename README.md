# 🚀 TaskFlow Pro UI — Streamlit Frontend

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![Requests](https://img.shields.io/badge/Requests-2.31-orange?style=for-the-badge)](https://pypi.org/project/requests/)
[![Live Demo](https://img.shields.io/badge/Live-Demo-red?style=for-the-badge\&logo=streamlit)](https://taskmanagerfrontend.streamlit.app/)

**TaskFlow Pro UI** is the interactive frontend dashboard for the TaskFlow ecosystem.

Built with **Streamlit**, this interface allows users to efficiently manage tasks with a focus on **speed, simplicity, and productivity-oriented design**.

The UI communicates with a **FastAPI backend hosted on Render**, creating a complete full-stack task management application.

---

# 🌐 Live Application

**Streamlit Frontend**

https://taskmanagerfrontend.streamlit.app/

**FastAPI Backend**

https://fastapi-project-2-task-manager-backend.onrender.com

**API Documentation**

https://fastapi-project-2-task-manager-backend.onrender.com/docs

---

# ✨ Key Features

### ⚡ Quick Task Entry

A **lazy-add workflow** that allows users to rapidly create tasks with minimal typing.

Example:

```
Call bank high
```

Automatically parses:

```
Title → Call bank  
Priority → High
```

---

### 📊 Real-Time Progress Tracking

The dashboard automatically calculates:

* total tasks
* completed tasks
* pending tasks
* productivity percentage

Displayed using interactive metrics and progress bars.

---

### 🔍 Dynamic Filtering

Powerful filtering tools:

* live search
* priority filtering
* instant updates

This allows users to quickly locate specific tasks.

---

### 🎯 Priority Visualization

Tasks are visually categorized by priority:

| Priority | Indicator |
| -------- | --------- |
| High     | 🔴        |
| Medium   | 🟡        |
| Low      | 🟢        |

This helps users identify urgent work instantly.

---

### 🎉 Completion Feedback

Completing a task triggers visual feedback:

* strike-through animation
* progress updates
* confirmation toast

This improves the overall UX and productivity flow.

---

# 🏗 Architecture

```
Streamlit Frontend
        │
        ▼
 FastAPI Backend (Render)
        │
        ▼
   In-Memory Task Store
```

The system architecture allows the backend to be easily upgraded with:

* PostgreSQL
* MongoDB
* Redis caching
* authentication systems

---

# 🔌 API Integration

The frontend communicates with the backend using the **Requests library**.

Example configuration:

```python
API_URL = "https://fastapi-project-2-task-manager-backend.onrender.com"
```

Example request:

```python
requests.get(f"{API_URL}/tasks")
```

---

# 📂 Project Structure

```
taskflow-frontend
│
├── app.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Local Setup

Clone the repository

```
git clone https://github.com/iqroguerex-cpu/fastapi-project-2-task-manager-frontend
```

Navigate into the project

```
cd fastapi-project-2-task-manager-frontend
```

Install dependencies

```
pip install -r requirements.txt
```

Run the application

```
streamlit run app.py
```

---

# ☁️ Deployment

The UI is deployed using **Streamlit Community Cloud**.

Deployment automatically:

* pulls code from GitHub
* installs dependencies
* launches the Streamlit app

---

# 🔗 Backend Repository

FastAPI backend source code:

https://github.com/iqroguerex-cpu/fastapi-project-2-task-manager-backend

---

# 📄 License

This project is released under the **MIT License**.

---

# 👨‍💻 Author

**Chinmay V Chatradamath**

GitHub
https://github.com/iqroguerex-cpu

---

⭐ If you found this project useful, consider **starring the repository**.
