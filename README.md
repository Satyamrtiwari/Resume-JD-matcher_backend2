# 🚀 Resume-JD Matcher AI System

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-REST-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![AI](https://img.shields.io/badge/AI-HuggingFace-orange)

An AI-powered full-stack application that evaluates semantic similarity between candidate resumes and job descriptions using transformer-based embeddings.

---

## 🌐 Live Demo
👉 [https://your-link.com](https://resume-jb-matcher-satyam1.netlify.app/)

## 📌 Overview

Resume-JD Matcher helps recruiters and candidates quickly assess compatibility by analyzing resumes against job descriptions using advanced NLP models from HuggingFace.

---

## 🎯 Key Features

### 🧠 AI Matching Engine

* Transformer-based semantic similarity (HuggingFace)
* Accurate match scoring with intelligent verdicts:

  * ✅ Strong Match (≥ 75%)
  * ⚖️ Moderate Match (≥ 50%)
  * ❌ Low Match (< 50%)

### 🔐 Authentication System

* JWT-based secure login & registration
* Protected API routes

### 📄 Resume Management

* Upload PDF resumes
* Text extraction using `pypdf`
* Resume storage & management

### 💼 Job Description Handling

* Create, view, and delete job listings
* Structured job tracking

### 📊 Match History Dashboard

* Track all previous matches
* View similarity scores and results

---

## 🛠️ Tech Stack

### Backend

* Python 3
* Django & Django REST Framework
* JWT Authentication (`simplejwt`)
* PostgreSQL / SQLite
* HuggingFace Transformers

### Frontend

* React 18
* Vite
* TailwindCSS
* React Router DOM

---

## 📂 Project Structure

```text
RESUME_JD/
│
├── Resume_ML(backend)/
│   ├── project/
│   │   ├── app/
│   │   ├── project/
│   │   ├── manage.py
│   │   └── requirements.txt
│   └── resume_ml/
│
├── Resume_ML(frontend)/
│   └── resume-jd-frontend/
│       ├── src/
│       ├── public/
│       ├── package.json
│       ├── tailwind.config.js
│       └── vite.config.js
│
└── README.md
```

---

## ⚙️ Setup & Installation

### 🔧 Backend Setup

```bash
cd "Resume_ML(backend)/project"
../resume_ml/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

### 🌐 Frontend Setup

```bash
cd "Resume_ML(frontend)/resume-jd-frontend"
npm install
npm run dev
```

---

## 🔌 API Endpoints

| Endpoint                 | Method    | Description           |
| ------------------------ | --------- | --------------------- |
| `/api/login/`            | POST      | Login & get JWT token |
| `/api/register/`         | POST      | Register user         |
| `/api/job-descriptions/` | GET, POST | Manage jobs           |
| `/api/resumes/`          | GET, POST | Manage resumes        |
| `/api/match/`            | POST      | Run AI matching       |
| `/api/match-history/`    | GET       | View match history    |

---

## 🚀 Future Improvements

* 🌍 Deploy to cloud (AWS / Render)
* 📊 Advanced analytics dashboard
* 🤖 Fine-tuned ML models
* 📱 Mobile responsiveness

---

## 👤 Author

**Satyam Tiwari**

---

⭐ If you like this project, give it a star!
