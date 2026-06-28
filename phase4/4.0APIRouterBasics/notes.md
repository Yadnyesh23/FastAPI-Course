# Phase 4.0 – APIRouter & Project Structure

## Objectives

By the end of this phase, you should understand:

- Why `main.py` shouldn't contain everything
- What `APIRouter` is
- Why we use `APIRouter`
- How to create routers
- How to include routers
- Route Prefixes
- Tags
- Project Structure
- Benefits of modular applications

---

# 1. Why Not Put Everything in `main.py`?

For small projects, having all routes in `main.py` is fine.

As the project grows, `main.py` can become thousands of lines long, making it:

- Difficult to read
- Difficult to maintain
- Difficult to debug
- Difficult to collaborate on

### Example

```python
@app.get("/students")

@app.post("/students")

@app.put("/students/{id}")

@app.get("/teachers")

@app.post("/teachers")

@app.get("/notes")

@app.post("/notes")

...
```

A better approach is to split related routes into separate files.

---

# 2. What is APIRouter?

`APIRouter` is a FastAPI class used to group related API endpoints.

Think of it as a **mini FastAPI application**.

Instead of placing all routes in one file, we organize them into multiple routers.

### Example

```text
students.py
teachers.py
auth.py
notes.py
```

Each file contains only related routes.

---

# 3. Creating an APIRouter

Instead of creating a FastAPI application:

```python
from fastapi import FastAPI

app = FastAPI()
```

Create a router:

```python
from fastapi import APIRouter

router = APIRouter()
```

Define routes using `router` instead of `app`.

### Example

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_students():
    return ["Rahul", "Yadnyesh"]
```

---

# 4. Including Routers

Routers must be registered with the main FastAPI application.

### main.py

```python
from fastapi import FastAPI
from routers.students import router as student_router

app = FastAPI()

app.include_router(student_router)
```

`include_router()` tells FastAPI to include all routes defined inside that router.

---

# 5. Route Prefixes

Many endpoints begin with the same path.

Without prefixes:

```python
@router.get("/students")

@router.post("/students")

@router.put("/students/{id}")

@router.delete("/students/{id}")
```

Using a prefix:

```python
router = APIRouter(
    prefix="/students"
)
```

Now define routes like:

```python
@router.get("/")
```

```python
@router.post("/")
```

```python
@router.put("/{id}")
```

Actual URLs become:

```text
GET    /students
POST   /students
PUT    /students/{id}
DELETE /students/{id}
```

### Benefits

- Reduces repetition
- Cleaner code
- Easier maintenance

---

# 6. Tags

Tags organize APIs inside Swagger UI.

Example:

```python
router = APIRouter(
    prefix="/students",
    tags=["Students"]
)
```

Swagger Documentation:

```text
▼ Students

GET  /students
POST /students
PUT  /students/{id}
```

Without tags, all endpoints appear in one long list.

---

# 7. Basic Project Structure

Small Project

```text
project/
│
├── main.py
├── students.py
├── teachers.py
└── auth.py
```

Production Project

```text
app/
│
├── main.py
│
├── routers/
│   ├── students.py
│   ├── teachers.py
│   ├── auth.py
│   ├── notes.py
│   └── lectures.py
│
├── models/
├── schemas/
├── services/
├── dependencies/
├── database/
└── core/
```

---

# 8. Purpose of Common Folders

| Folder | Purpose |
|----------|----------|
| `routers/` | API endpoints |
| `models/` | Database models |
| `schemas/` | Pydantic models |
| `services/` | Business logic |
| `database/` | Database connection and session |
| `dependencies/` | Reusable dependencies |
| `core/` | Configuration, security, settings |

---

# 9. FastAPI vs APIRouter

| FastAPI | APIRouter |
|----------|-----------|
| Creates the main application | Creates a group of related routes |
| Usually one per project | Multiple routers can exist |
| Starts the application | Included inside the main application |
| Uses `FastAPI()` | Uses `APIRouter()` |

---

# 10. Benefits of APIRouter

- Organizes code
- Improves readability
- Easier debugging
- Easier maintenance
- Better scalability
- Easier team collaboration
- Promotes modular design
- Reusable route groups

---

# 11. Best Practices

- Keep related endpoints in the same router.
- Use meaningful prefixes.
- Use tags for Swagger documentation.
- Keep `main.py` clean.
- Follow a modular project structure.
- Use one router per feature (Students, Teachers, Auth, Notes, etc.).

---

# 12. Example Structure

```text
app/
│
├── main.py
│
└── routers/
    ├── students.py
    ├── teachers.py
    ├── auth.py
    └── notes.py
```

**students.py**

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.get("/")
def get_students():
    return {"message": "Students API"}
```

**main.py**

```python
from fastapi import FastAPI
from routers.students import router as student_router

app = FastAPI()

app.include_router(student_router)
```

---

# 13. Interview Questions

1. Why shouldn't all routes be placed inside `main.py`?
2. What is `APIRouter`?
3. How is `APIRouter` different from `FastAPI`?
4. What does `include_router()` do?
5. Why are route prefixes useful?
6. What are tags used for?
7. What are the advantages of splitting routes into multiple files?
8. Name some common folders in a production FastAPI project.

---

# 14. Quick Cheat Sheet

| Feature | Purpose |
|----------|----------|
| `APIRouter()` | Create a router |
| `router.get()` | Define GET route |
| `router.post()` | Define POST route |
| `include_router()` | Register router with FastAPI |
| `prefix` | Common URL prefix |
| `tags` | Group APIs in Swagger |

---

# 15. Key Takeaways

- `APIRouter` helps organize related API routes.
- Large applications should not keep all routes inside `main.py`.
- `include_router()` registers routers with the FastAPI application.
- `prefix` removes repetitive route paths.
- `tags` improve API documentation in Swagger UI.
- Modular project structures are easier to maintain and scale.
- Production FastAPI applications separate routers, models, schemas, services, and database logic into dedicated folders.