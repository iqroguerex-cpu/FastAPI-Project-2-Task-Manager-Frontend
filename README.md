# 🎯 TaskFlow Frontend — Serverless Task Manager UI

<p align="center">

[![Live App](https://img.shields.io/badge/Live%20App-Frontend-success?style=for-the-badge)](https://staging.d3b7v2fqtuw73g.amplifyapp.com/)
[![Backend API](https://img.shields.io/badge/API-AWS%20Lambda-blue?style=for-the-badge\&logo=amazonaws)](https://89djj7pnai.execute-api.ap-south-1.amazonaws.com/default/)
![HTML](https://img.shields.io/badge/HTML-5-orange?style=for-the-badge\&logo=html5)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-UI-blue?style=for-the-badge\&logo=tailwindcss)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge\&logo=javascript)
![AWS](https://img.shields.io/badge/Hosted%20on-AWS%20Amplify-purple?style=for-the-badge\&logo=amazonaws)

</p>

---

## 🚀 Overview

**TaskFlow Frontend** is a modern, responsive **task management dashboard** built with **HTML, Tailwind CSS, and JavaScript**, designed to interact with a **serverless FastAPI backend deployed on AWS Lambda**.

The backend is packaged and deployed via **Amazon S3**, enabling a fully scalable cloud-based architecture.

---

## 🌐 Live Application

👉 https://staging.d3b7v2fqtuw73g.amplifyapp.com/

---

## ✨ Features

* 📋 View all tasks
* ➕ Create new tasks
* ✏️ Update tasks
* ❌ Delete tasks
* 🔄 Refresh task list
* 🎨 Modern dark UI (Tailwind CSS)
* ⚡ Real-time API integration
* ☁️ Fully serverless backend integration

---

## 🛠 Tech Stack

### Frontend

* HTML5
* Tailwind CSS
* JavaScript (Fetch API)

### Backend Integration

* FastAPI (via AWS Lambda + Mangum)
* API Gateway
* DynamoDB
* Amazon S3 (deployment package)

### Hosting

* AWS Amplify

---

## 📂 Project Structure

```bash id="tfui1"
.
├── index.html
├── README.md
```

---

## ⚙️ Running Locally

Clone the repository:

```bash id="tfui2"
git clone https://github.com/your-username/taskflow-frontend.git
cd taskflow-frontend
```

Open:

```bash id="tfui3"
index.html
```

in your browser.

---

## 🔗 API Integration

Base URL:

```bash id="tfui4"
https://89djj7pnai.execute-api.ap-south-1.amazonaws.com/default
```

### Endpoints Used

* `GET /tasks` → Fetch all tasks
* `GET /tasks/{id}` → Get task
* `POST /tasks/create_task` → Create task
* `PUT /tasks/update_task/{id}` → Update task
* `DELETE /tasks/delete_task/{id}` → Delete task

---

## ☁️ Architecture

```bash id="tfui5"
Frontend (Amplify)
        ↓
API Gateway
        ↓
Lambda (FastAPI via Mangum)
        ↓
DynamoDB
        ↑
Deployment package stored in S3
```

---

## 🎨 UI Highlights

* 🌙 Dark theme
* 📱 Fully responsive design
* ⚡ Fast and lightweight
* 🎯 Clean task management workflow

---

## 🔮 Future Improvements

* 🔐 Authentication (Cognito / JWT)
* 📅 Task deadlines & reminders
* 🏷 Task categories
* 🔍 Search & filtering
* 📊 Analytics dashboard

---

## 👨‍💻 Author

**Chinmay V Chatradamath**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
