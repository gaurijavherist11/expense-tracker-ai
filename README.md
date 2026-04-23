# 💰 Expense Tracker with AI Financial Advice

A full-stack web application built using Flask that helps users manage income, expenses, and budgets, along with an AI-powered financial assistant for basic guidance.

---

## 🚀 Features

* 🔐 User Authentication (Login / Signup)
* 💵 Add and manage income
* 💸 Track expenses with categories and feedback (regret / worth it)
* 📊 View financial summary (income, expense, balance)
* 🎯 Set and manage budgets
* 🤖 Generate financial advice using AI (Ollama)
* 💬 Chat-based financial assistant
* 📈 Basic expense analysis using Streamlit

---

## 🛠️ Tech Stack

### 🔹 Frontend

* HTML
* CSS
* Bootstrap

### 🔹 Backend

* Python (Flask)
* Flask Blueprints
* Flask-Login

### 🔹 Database

* SQLite
* SQLAlchemy ORM

### 🔹 AI Integration

* Ollama (Llama3 model - local LLM)
* Rule-based fallback system

### 🔹 Data Analysis

* Pandas
* Matplotlib
* Streamlit

---

## 📂 Project Structure

```
exp-main/
│
├── models/            # Database models (User, Income, Expense, Advice)
├── routes/            # Flask routes (auth, income, expense, advice)
├── templates/         # HTML templates
├── static/            # CSS files
├── streamlit_app.py   # Expense analysis dashboard
│
├── app.py             # Main Flask application
├── db.py              # Database setup
├── config.py          # Configuration
└── requirements.txt   # Dependencies
```

---

## ⚙️ How to Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/expense-tracker-ai.git
cd expense-tracker-ai
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run Flask app

```bash
python app.py
```

👉 Open:

```
http://127.0.0.1:5000
```

---

### 5️⃣ Run Streamlit dashboard (optional)

```bash
streamlit run streamlit_app.py
```

---

## 🤖 AI Functionality

* Uses **Ollama (local LLM)** to generate financial advice
* If AI is slow/unavailable → falls back to **rule-based advice**
* Chat system stores conversation using session

---

## 📊 What this project demonstrates

* Full-stack development using Flask
* Database design and CRUD operations
* User authentication and session handling
* Integration of AI into a web application
* Basic data analysis and visualization

---

## 💼 Resume Description

> Built a full-stack Expense Tracker web application using Flask, SQLite, and Bootstrap with AI-based financial advice using a local LLM (Ollama). Implemented user authentication, budgeting features, and a chat-based financial assistant.

---

## 👩‍💻 Author

**Gauri Milind Javheri**
GitHub: https://github.com/gaurijavherist11

---

## ⭐

If you find this project useful, feel free to star the repository!
