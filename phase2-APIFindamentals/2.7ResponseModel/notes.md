# Phase 2.7 – Response Models

## Objectives

By the end of this phase, you should understand:

- What Response Models are
- Why Response Models are needed
- response_model=
- Response Validation
- Data Filtering
- Security Benefits
- Request vs Response Models
- Lists as Responses
- Nested Response Models
- Real-world API Design

---

# What is a Response Model?

A Response Model defines:

```text
What data FastAPI is allowed to send back to the client.
```

Think:

```text
Request Model
Client → Server
```

```text
Response Model
Server → Client
```

Response Models control outgoing data.

---

# Why Do We Need Response Models?

Without Response Models:

```python
@app.get("/user")
def get_user():
    return {
        "username": "Yadnyesh",
        "email": "abc@gmail.com",
        "password": "123456"
    }
```

Response:

```json
{
  "username": "Yadnyesh",
  "email": "abc@gmail.com",
  "password": "123456"
}
```

Problem:

- Password exposed
- Sensitive data leaked
- Security issue

---

# Creating a Response Model

Instead of exposing everything:

```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    username: str
    email: str
```

Notice:

```python
password
```

is not included.

---

# response_model=

FastAPI provides:

```python
response_model=
```

Example:

```python
@app.get(
    "/user",
    response_model=UserResponse
)
def get_user():
    return {
        "username": "Yadnyesh",
        "email": "abc@gmail.com",
        "password": "123456"
    }
```

FastAPI automatically filters the response.

Returned:

```json
{
  "username": "Yadnyesh",
  "email": "abc@gmail.com"
}
```

Password is removed.

---

# Benefits of Response Models

## Security

Hide:

- Passwords
- Tokens
- Internal IDs
- Private Information

---

## Consistency

Every response follows the same structure.

---

## Validation

FastAPI validates outgoing responses.

---

## Documentation

Swagger automatically documents response schemas.

---

# Request Model vs Response Model

## Request Model

Used for:

```text
Client → Server
```

Example:

```python
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
```

---

## Response Model

Used for:

```text
Server → Client
```

Example:

```python
class UserResponse(BaseModel):
    username: str
    email: str
```

Password removed.

---

# Typical Production Pattern

```python
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
```

```python
class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
```

```python
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
```

Different models for different purposes.

---

# Response Validation

FastAPI validates outgoing data.

Example:

```python
class UserResponse(BaseModel):
    username: str
    email: str
```

Route:

```python
@app.get(
    "/user",
    response_model=UserResponse
)
def get_user():
    return {
        "username": "Yadnyesh"
    }
```

Problem:

```python
email
```

is missing.

FastAPI raises a validation error.

This usually results in:

```text
500 Internal Server Error
```

because the server returned invalid data.

---

# Response Filtering

Returned Data:

```python
{
    "username": "Yadnyesh",
    "email": "abc@gmail.com",
    "password": "secret",
    "token": "xyz"
}
```

Response Model:

```python
class UserResponse(BaseModel):
    username: str
    email: str
```

Client Receives:

```json
{
  "username": "Yadnyesh",
  "email": "abc@gmail.com"
}
```

Extra fields are automatically removed.

---

# Response Models with Lists

Very common.

Model:

```python
class Student(BaseModel):
    id: int
    name: str
```

Route:

```python
@app.get(
    "/students",
    response_model=list[Student]
)
def get_students():
    return [
        {
            "id": 1,
            "name": "Yadnyesh"
        },
        {
            "id": 2,
            "name": "Rahul"
        }
    ]
```

Response:

```json
[
  {
    "id": 1,
    "name": "Yadnyesh"
  },
  {
    "id": 2,
    "name": "Rahul"
  }
]
```

---

# Nested Response Models

Models can contain other models.

Example:

```python
class Address(BaseModel):
    city: str
    state: str
```

```python
class StudentResponse(BaseModel):
    name: str
    address: Address
```

Route:

```python
@app.get(
    "/student",
    response_model=StudentResponse
)
def get_student():
    return {
        "name": "Yadnyesh",
        "address": {
            "city": "Mumbai",
            "state": "Maharashtra"
        }
    }
```

Nested validation works automatically.

---

# Real TesLearn Example

Database Record:

```json
{
  "id": 1,
  "title": "Binary Trees",
  "content": "...",
  "author_email": "abc@gmail.com",
  "internal_version": 5,
  "created_at": "2026-06-24"
}
```

Client should NOT see:

```json
{
  "author_email": "...",
  "internal_version": 5
}
```

Response Model:

```python
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: str
```

Only safe fields are returned.

---

# Create vs Response Models

Example:

```python
class NoteCreate(BaseModel):
    title: str
    content: str
```

Client sends:

```json
{
  "title": "Binary Trees",
  "content": "..."
}
```

---

```python
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: str
```

Client receives:

```json
{
  "id": 1,
  "title": "Binary Trees",
  "content": "...",
  "created_at": "2026-06-24"
}
```

---

# FastAPI Internal Flow

Request:

```text
Client → FastAPI
```

Response:

```text
Route Function
        ↓
Returned Data
        ↓
Response Model Validation
        ↓
Extra Fields Removed
        ↓
JSON Response
        ↓
Client
```

---

# Best Practices

- Always use Response Models.
- Never return passwords.
- Never return authentication tokens unnecessarily.
- Create separate Request and Response models.
- Use list[Model] for collections.
- Use Nested Models for structured responses.
- Let FastAPI validate outgoing responses.

---

# Common Mistakes

## ❌ Using One Model Everywhere

Bad:

```python
class User(BaseModel):
    username: str
    email: str
    password: str
```

Used for both request and response.

---

Better:

```python
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
```

```python
class UserResponse(BaseModel):
    username: str
    email: str
```

---

## ❌ Returning Sensitive Data

Bad:

```python
{
    "password": "123456"
}
```

---

Good:

```python
{
    "username": "Yadnyesh"
}
```

---

## ❌ Not Using response_model

Bad:

```python
@app.get("/user")
```

---

Good:

```python
@app.get(
    "/user",
    response_model=UserResponse
)
```

---

# Interview Questions

1. What is a Response Model?
2. Why do we need Response Models?
3. What is response_model=?
4. How do Response Models improve security?
5. Difference between Request Model and Response Model?
6. What happens if returned data doesn't match the Response Model?
7. Can Response Models return lists?
8. Can Response Models be nested?
9. Why shouldn't passwords be included in Response Models?
10. What are the benefits of separate Create and Response models?

---

# Quick Cheat Sheet

```python
response_model=UserResponse
```

Response Validation + Filtering

---

```python
response_model=list[Student]
```

List Response

---

```python
class UserCreate(BaseModel)
```

Request Model

---

```python
class UserResponse(BaseModel)
```

Response Model

---

```python
500 Internal Server Error
```

Can occur if response validation fails.

---

# Key Takeaways

- Response Models define what the client receives.
- response_model= enables response validation and filtering.
- Sensitive data should never be exposed.
- Request and Response models should usually be separate.
- Response Models can return lists.
- Response Models can be nested.
- FastAPI validates outgoing responses.
- Swagger automatically documents response schemas.
- Response Models are essential for secure, production-grade APIs.