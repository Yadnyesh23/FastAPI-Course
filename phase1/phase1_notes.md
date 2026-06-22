# Phase 1 — FastAPI First Steps

## Objectives

By the end of this phase, you should understand:

- What FastAPI is
- Why FastAPI is popular
- ASGI
- Uvicorn
- Project structure
- Creating your first API
- Running the server
- Automatic API documentation

---

# What is FastAPI?

FastAPI is a modern Python web framework used to build APIs.

It helps developers:

- Build REST APIs quickly
- Validate request data automatically
- Generate API documentation automatically
- Return JSON responses easily
- Build high-performance asynchronous applications

---

# Why FastAPI?

## Advantages

- High performance
- Easy to learn
- Automatic request validation
- Automatic API documentation
- Built-in type hints
- Async support
- Excellent developer experience

---

# Request Flow

```
Client
   │
   ▼
Internet
   │
   ▼
Uvicorn Server
   │
   ▼
FastAPI Application
   │
   ▼
Router
   │
   ▼
Matching Function
   │
   ▼
Return Python Object
   │
   ▼
FastAPI converts it to JSON
   │
   ▼
Client
```

---

# ASGI

ASGI stands for:

**Asynchronous Server Gateway Interface**

It is a standard interface between asynchronous Python web applications and web servers.

Benefits:

- Handles many requests efficiently
- Supports async programming
- Enables WebSockets
- Better scalability

---

# Uvicorn

Uvicorn is an ASGI web server.

Responsibilities:

- Listens for incoming HTTP requests
- Passes requests to the FastAPI application
- Returns responses to the client

FastAPI **requires** an ASGI server such as Uvicorn to run.

---

# Installing FastAPI

```bash
pip install fastapi "uvicorn[standard]"
```

---

# Creating the Application

```python
from fastapi import FastAPI

app = FastAPI()
```

`FastAPI()` creates the application instance.

---

# Creating a Route

```python
@app.get("/")
def root():
    return {
        "message": "Hello FastAPI"
    }
```

Explanation:

- `@app.get("/")` registers a GET endpoint.
- `root()` is executed when a GET request is sent to `/`.
- Returning a Python dictionary automatically produces a JSON response.

---

# Running the Server

```bash
uvicorn main:app --reload
```

Meaning:

- `main` → filename (`main.py`)
- `app` → FastAPI application object
- `--reload` → automatically restarts the server when code changes

---

# Automatic API Documentation

## Swagger UI

```
http://127.0.0.1:8000/docs
```

Features:

- Interactive testing
- Request/response schemas
- API exploration

---

## ReDoc

```
http://127.0.0.1:8000/redoc
```

Features:

- Documentation-focused interface
- Easier to read
- Better for reference

---

# JSON Responses

Returning

```python
return {
    "message": "Hello"
}
```

automatically becomes

```json
{
    "message": "Hello"
}
```

FastAPI also sets the appropriate response headers (for example, `Content-Type: application/json`).

---

# Best Practices

- Use meaningful endpoint names.
- Return JSON-compatible data types.
- Prefer lists over sets in API responses.
- Use descriptive function names (e.g., `get_skills()`).
- Keep code clean and organized.

---

# Key Terms

| Term | Meaning |
|------|---------|
| API | Interface for communication between applications |
| FastAPI | Python framework for building APIs |
| ASGI | Standard interface for asynchronous Python web apps |
| Uvicorn | ASGI web server |
| Route | URL mapped to a Python function |
| Endpoint | A specific API URL |
| JSON | Data format commonly used in APIs |
| Swagger UI | Interactive API documentation |
| ReDoc | Documentation-focused API reference |

---

# Summary

- FastAPI builds APIs efficiently.
- Uvicorn runs the FastAPI application.
- `FastAPI()` creates the application instance.
- Route decorators map URLs and HTTP methods to functions.
- Python dictionaries are automatically serialized to JSON.
- `/docs` provides Swagger UI.
- `/redoc` provides ReDoc.