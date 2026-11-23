# FastAPI Learning & Practice

## Overview
This repository contains my learning and practical implementation of **FastAPI**, a modern, high-performance Python web framework used for building RESTful APIs. The main objective of this repository is to understand API development, backend fundamentals, request handling, data validation, and HTTP operations through hands-on practice.

## 🚀 What I Learned

- **FastAPI Fundamentals:** Understanding FastAPI and its working.
- **REST APIs:** Creating and managing RESTful API endpoints.
- **HTTP Methods:** Implementing GET, POST, PUT, PATCH, and DELETE operations.
- **Path Parameters:** Passing dynamic values through API URLs.
- **Query Parameters:** Filtering and handling data through query strings.
- **Pydantic:** Validating request data and defining data models.
- **CRUD Operations:** Creating, reading, updating, and deleting records.
- **Pagination:** Managing large datasets using page and limit parameters.
- **API Documentation:** Exploring automatic interactive documentation using Swagger UI.
- **Request & Response Handling:** Understanding how APIs receive and return data.

## 🛠️ Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- REST API
- VS Code

## 📂 Project Structure

```text
FastAPI/
│
├── main.py
├── requirements.txt
├── README.md
└── venv/
```

## ⚙️ Installation & Setup

**1. Clone the repository**

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

**2. Navigate to the project directory**

```bash
cd FastAPI
```

**3. Create a virtual environment**

```bash
python -m venv venv
```

**4. Activate the virtual environment**

Windows:

```bash
venv\Scripts\activate
```

**5. Install dependencies**

```bash
pip install fastapi uvicorn
```

**6. Run the application**

```bash
uvicorn main:app --reload
```

## 📖 API Documentation

After running the application, open the following URL in your browser:

**Swagger UI:**
http://127.0.0.1:8000/docs

**ReDoc:**
http://127.0.0.1:8000/redoc

These interfaces allow you to explore and test API endpoints interactively.

## 🎯 Learning Objective

The purpose of this repository is to build a strong foundation in backend development and understand how real-world APIs are designed, developed, tested, and managed using Python.

## 📈 Future Improvements

- Database integration using SQLAlchemy.
- Authentication and authorization.
- JWT-based authentication.
- Exception handling and middleware.
- Deployment of FastAPI applications.

---

**Learning by Building | Exploring Backend Development with Python & FastAPI**
