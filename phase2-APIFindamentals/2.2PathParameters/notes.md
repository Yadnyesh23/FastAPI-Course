# Phase 2.2 – Path Parameters

## Objectives

By the end of this phase, you should understand:

- What Path Parameters are
- Why Path Parameters are needed
- Dynamic URLs
- Type Hints
- Automatic Type Conversion
- Automatic Validation
- Supported Data Types
- Multiple Path Parameters
- Route Order
- Path Parameters vs Query Parameters
- Enum Path Parameters

---

# What are Path Parameters?

A **Path Parameter** is a dynamic part of a URL that identifies a specific resource.

Instead of creating multiple hardcoded URLs like:

```
/students/1
/students/2
/students/3
```

we create one dynamic URL:

```
/students/{student_id}
```

FastAPI extracts the value from the URL and passes it to the function.

---

# Why do we need Path Parameters?

Without Path Parameters, we would need a separate route for every resource.

Example:

```python
@app.get("/students/1")
def student1():
    ...

@app.get("/students/2")
def student2():
    ...
```

This is not scalable.

Instead:

```python
@app.get("/students/{student_id}")
def get_student(student_id: int):
    ...
```

One route can handle thousands or even millions of students.

---

# Dynamic URL

```
/students/{student_id}
```

Here,

```
student_id
```

is a placeholder.

Example:

```
/students/15
```

FastAPI extracts:

```python
student_id = 15
```

and passes it to the route function.

---

# Basic Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {
        "student_id": student_id
    }
```

Request:

```
GET /students/5
```

Response:

```json
{
    "student_id": 5
}
```

---

# Type Hints

FastAPI heavily uses Python Type Hints.

Example:

```python
student_id: int
```

Type hints help FastAPI:

- Validate data
- Convert data automatically
- Generate documentation
- Improve IDE support

---

# Automatic Type Conversion

URL:

```
/students/25
```

The value `"25"` is received as a string.

FastAPI automatically converts it to:

```python
25
```

because we specified:

```python
student_id: int
```

---

# Automatic Validation

Request:

```
/students/abc
```

Since `"abc"` cannot be converted to an integer,

FastAPI automatically returns:

```
422 Unprocessable Entity
```

along with a detailed validation error.

No manual validation code is required.

---

# Supported Path Parameter Types

## Integer

```python
student_id: int
```

Example:

```
/students/10
```

---

## String

```python
username: str
```

Example:

```
/users/Yadnyesh
```

---

## Float

```python
price: float
```

Example:

```
/products/99.99
```

---

## Boolean

```python
active: bool
```

Example:

```
/status/true
```

---

## UUID

```python
from uuid import UUID

user_id: UUID
```

Example:

```
/users/550e8400-e29b-41d4-a716-446655440000
```

Useful in production systems where resources are identified by UUIDs instead of integers.

---

# Multiple Path Parameters

You can define multiple dynamic values in the same URL.

Example:

```python
@app.get("/students/{student_id}/subjects/{subject}")
def get_subject(student_id: int, subject: str):
    return {
        "student_id": student_id,
        "subject": subject
    }
```

Request:

```
/students/5/subjects/python
```

Response:

```json
{
    "student_id": 5,
    "subject": "python"
}
```

---

# Route Order (Very Important)

Consider:

```python
@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"user": user_id}


@app.get("/users/me")
def current_user():
    return {"user": "Current User"}
```

Request:

```
/users/me
```

FastAPI matches:

```
/users/{user_id}
```

Result:

```json
{
    "user": "me"
}
```

### Correct Order

Always place fixed routes before dynamic routes.

```python
@app.get("/users/me")
def current_user():
    return {"user": "Current User"}


@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"user": user_id}
```

---

# Variable Name Matching

The variable inside `{}` **must exactly match** the function parameter.

Correct:

```python
@app.get("/students/{student_id}")
def get_student(student_id: int):
```

Incorrect:

```python
@app.get("/students/{student_id}")
def get_student(id: int):
```

FastAPI will not know what value to pass because the names do not match.

---

# Internal Working

When a request arrives:

```
GET /students/15
```

FastAPI conceptually performs:

```python
value = "15"

student_id = int(value)

get_student(student_id)
```

If conversion fails:

```python
int("abc")
```

FastAPI catches the exception and returns a validation error (`422 Unprocessable Entity`).

---

# Path Parameters vs Query Parameters

## Path Parameter

Identifies **which resource**.

Example:

```
/students/5
```

Here:

```
5
```

identifies Student 5.

---

## Query Parameter

Provides additional information such as filtering, searching, sorting, or pagination.

Example:

```
/students?city=Mumbai
```

Here:

```
city=Mumbai
```

filters the students.

---

# Enum Path Parameters

Enums restrict a path parameter to predefined values.

Example:

```python
from enum import Enum

class ProgrammingLanguage(str, Enum):
    python = "python"
    javascript = "javascript"
    cpp = "cpp"

@app.get("/languages/{language}")
def get_language(language: ProgrammingLanguage):
    return {
        "language": language
    }
```

Valid:

```
/languages/python
```

Invalid:

```
/languages/java
```

FastAPI automatically returns a validation error.

---

# Best Practices

- Use meaningful path parameter names.
- Keep the placeholder name and function parameter name identical.
- Use appropriate type hints (`int`, `str`, `UUID`, etc.).
- Use path parameters to identify resources.
- Place static routes before dynamic routes.
- Use Enums when only predefined values are allowed.

---

# Common Mistakes

❌ Hardcoding resource IDs:

```python
@app.get("/students/1")
```

✅ Use dynamic routes:

```python
@app.get("/students/{student_id}")
```

---

❌ Different parameter names:

```python
@app.get("/students/{student_id}")
def get_student(id: int):
```

✅ Correct:

```python
@app.get("/students/{student_id}")
def get_student(student_id: int):
```

---

❌ Placing dynamic routes before static routes:

```python
@app.get("/users/{user_id}")
@app.get("/users/me")
```

✅ Correct:

```python
@app.get("/users/me")
@app.get("/users/{user_id}")
```

---

# Interview Questions

1. What is a Path Parameter?
2. Why do we use Path Parameters?
3. Why does FastAPI use Python Type Hints?
4. What happens if an invalid value is passed to an `int` Path Parameter?
5. Why should `/users/me` be declared before `/users/{user_id}`?
6. What is the difference between a Path Parameter and a Query Parameter?
7. Why are Enums useful in Path Parameters?

---

# Key Takeaways

- Path Parameters create dynamic URLs.
- They identify specific resources.
- FastAPI automatically extracts values from the URL.
- Type hints enable automatic conversion and validation.
- FastAPI returns `422 Unprocessable Entity` for invalid path parameter values.
- Multiple Path Parameters can be used in a single route.
- Static routes should be declared before dynamic routes.
- Path Parameter names must match the function parameter names.
- Enums restrict Path Parameters to predefined values.