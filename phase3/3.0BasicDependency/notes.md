# Phase 3.0 – Dependency Injection

## Objectives

By the end of this phase, you should understand:

- What Dependency Injection is
- Why Dependency Injection is used
- What `Depends()` is
- Creating Dependencies
- Reusing Dependencies
- Nested Dependencies
- Dependency Chains
- Authentication Dependencies
- Database Dependencies
- Benefits of Dependency Injection

---

# What is Dependency Injection?

Dependency Injection (DI) is a design pattern where FastAPI automatically executes a reusable function (called a **dependency**) and injects its returned value into a route or another dependency.

Instead of manually calling helper functions inside every route, FastAPI does it for you.

Without Dependency Injection:

```python
def get_name():
    return "Yadnyesh"

@app.get("/")
def root():
    name = get_name()

    return {
        "name": name
    }
```

With Dependency Injection:

```python
from fastapi import Depends

def get_name():
    return "Yadnyesh"

@app.get("/")
def root(
    name: str = Depends(get_name)
):
    return {
        "name": name
    }
```

In this case, FastAPI automatically calls `get_name()` and injects its return value into the `name` parameter.

---

# Why Do We Need Dependency Injection?

Without Dependency Injection, the same logic is repeated in multiple routes.

Example:

```python
@app.get("/profile")
def profile():

    token = verify_token()

    return {
        "message": "Profile"
    }


@app.get("/notes")
def notes():

    token = verify_token()

    return {
        "message": "Notes"
    }


@app.get("/videos")
def videos():

    token = verify_token()

    return {
        "message": "Videos"
    }
```

The same authentication logic appears everywhere.

Instead, create one dependency:

```python
def verify_user():
    return {
        "id": 1,
        "name": "Yadnyesh"
    }
```

Use it everywhere:

```python
@app.get("/profile")
def profile(
    user=Depends(verify_user)
):
    return user


@app.get("/notes")
def notes(
    user=Depends(verify_user)
):
    return user
```

Write once, reuse everywhere.

---

# What is Depends()?

`Depends()` is FastAPI's built-in function used for Dependency Injection.

It tells FastAPI:

> "Execute this dependency before running the route and inject its return value."

Import:

```python
from fastapi import Depends
```

Example:

```python
@app.get("/")
def root(
    name: str = Depends(get_name)
):
    return {
        "name": name
    }
```

---

# Creating Your First Dependency

Dependency:

```python
def get_name():
    return "Yadnyesh"
```

Using the dependency:

```python
from fastapi import Depends

@app.get("/")
def root(
    name: str = Depends(get_name)
):
    return {
        "name": name
    }
```

Response:

```json
{
    "name": "Yadnyesh"
}
```

---

# How Dependency Injection Works

Flow:

```text
Client Request
      ↓
FastAPI
      ↓
Execute Dependency
      ↓
Return Value
      ↓
Inject Into Route
      ↓
Execute Route
      ↓
Response
```

---

# Dependencies Can Return Any Python Object

A dependency is just a Python function.

It can return:

- String
- Integer
- Float
- Boolean
- Dictionary
- List
- Pydantic Model
- Custom Class Object
- Database Session
- User Object

Example:

```python
def get_user():

    return {
        "id": 1,
        "name": "Yadnyesh",
        "role": "Admin"
    }
```

Route:

```python
@app.get("/profile")
def profile(
    user=Depends(get_user)
):
    return user
```

---

# Multiple Dependencies

A route can use multiple dependencies.

Example:

```python
def get_name():
    return "Yadnyesh"


def get_role():
    return "Admin"


@app.get("/")
def root(
    name=Depends(get_name),
    role=Depends(get_role)
):
    return {
        "name": name,
        "role": role
    }
```

Response:

```json
{
    "name": "Yadnyesh",
    "role": "Admin"
}
```

---

# Nested Dependencies

One dependency can depend on another dependency.

Example:

```python
def get_token():
    return "abc123"
```

Second dependency:

```python
from fastapi import Depends

def get_user(
    token: str = Depends(get_token)
):
    return {
        "token": token,
        "name": "Yadnyesh"
    }
```

Route:

```python
@app.get("/")
def root(
    user=Depends(get_user)
):
    return user
```

Flow:

```text
Request
   ↓
get_token()
   ↓
get_user()
   ↓
Route
```

This is called a **Dependency Chain**.

---

# Authentication Example

Instead of verifying a token inside every route:

```python
token = verify_token()
```

Create one dependency:

```python
def get_current_user():
    return {
        "id": 1,
        "name": "Yadnyesh"
    }
```

Use it everywhere:

```python
@app.get("/profile")
def profile(
    user=Depends(get_current_user)
):
    return user


@app.get("/notes")
def notes(
    user=Depends(get_current_user)
):
    return user


@app.get("/videos")
def videos(
    user=Depends(get_current_user)
):
    return user
```

Authentication logic is written only once.

---

# Database Dependency Example

Without Dependency Injection:

```python
@app.get("/students")
def students():

    db = Session()

    return db.query(Student).all()
```

With Dependency Injection:

```python
def get_db():
    return db_session
```

Route:

```python
@app.get("/students")
def students(
    db=Depends(get_db)
):
    return db.query(Student).all()
```

The same database session dependency can be reused across all routes.

---

# Real TesLearn Example

Dependency:

```python
def get_current_user():
    return {
        "id": 1,
        "name": "Yadnyesh"
    }
```

Routes:

```python
@app.post("/lectures")
def create_lecture(
    user=Depends(get_current_user)
):
    pass
```

```python
@app.post("/notes")
def create_note(
    user=Depends(get_current_user)
):
    pass
```

```python
@app.post("/mindmap")
def create_mindmap(
    user=Depends(get_current_user)
):
    pass
```

One authentication function protects every endpoint.

---

# Benefits of Dependency Injection

## Reusability

Write logic once.

Use it everywhere.

---

## Cleaner Code

Routes stay small and focused.

---

## Better Code Organization

Authentication, permissions, logging, validation, and database logic remain separate from business logic.

---

## Easier Testing

Dependencies can be replaced with mock implementations during testing.

---

## Scalability

Large projects become easier to maintain.

---

# Common Use Cases

Dependency Injection is commonly used for:

- Authentication
- Authorization
- Database Sessions
- Logging
- Configuration
- API Keys
- Permissions
- Current User
- Rate Limiting
- Common Validation

---

# Common Mistakes

## ❌ Manually Calling Dependency

Wrong:

```python
@app.get("/")
def root():

    user = get_current_user()

    return user
```

Correct:

```python
@app.get("/")
def root(
    user=Depends(get_current_user)
):
    return user
```

---

## ❌ Putting Business Logic Inside Every Route

Wrong:

```python
@app.get("/profile")
def profile():

    verify_token()

    verify_permissions()

    db = Session()

    ...
```

Better:

```python
@app.get("/profile")
def profile(
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    ...
```

Routes become much cleaner.

---

# Interview Questions

1. What is Dependency Injection?
2. Why is Dependency Injection needed?
3. What is `Depends()`?
4. What does a dependency return?
5. Can dependencies return objects?
6. Can one dependency depend on another?
7. What is a nested dependency?
8. What is a Dependency Chain?
9. Give a real-world use case of Dependency Injection.
10. Why is Dependency Injection useful for authentication?
11. Why is it useful for database sessions?
12. What are the benefits of Dependency Injection?

---

# Quick Cheat Sheet

```python
from fastapi import Depends
```

Import Dependency Injection.

---

```python
Depends(get_user)
```

Execute `get_user()` and inject its return value.

---

```python
def get_user():
    return user
```

Simple dependency.

---

```python
user=Depends(get_user)
```

Use dependency inside a route.

---

```python
db=Depends(get_db)
```

Database dependency.

---

```python
token=Depends(get_token)
```

Nested dependency.

---

# Key Takeaways

- Dependency Injection is a design pattern used by FastAPI to execute reusable logic automatically.
- `Depends()` tells FastAPI to execute a dependency and inject its return value.
- Dependencies can return any Python object.
- A route can have multiple dependencies.
- Dependencies can depend on other dependencies (Nested Dependencies).
- Dependency Injection reduces code duplication.
- It is heavily used for authentication, database sessions, permissions, logging, and validation.
- Dependency Injection makes FastAPI applications cleaner, scalable, and easier to maintain.