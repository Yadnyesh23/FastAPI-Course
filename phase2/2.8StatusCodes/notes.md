# Phase 2.8 – Status Codes

## Objectives

By the end of this phase, you should understand:

- What Status Codes are
- Why they are important
- Status Code Categories
- 200 OK
- 201 Created
- 204 No Content
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 422 Unprocessable Entity
- 500 Internal Server Error
- status_code=
- HTTPException
- Production API Conventions

---

# What is a Status Code?

A status code is a number sent by the server to the client that tells the client what happened with the request.

Example:

```text
Client Request
      ↓
Server
      ↓
Response + Status Code
```

Status codes help answer questions like:

- Was the request successful?
- Was a resource created?
- Is the user authenticated?
- Was the requested data found?
- Did the server crash?

---

# Why Are Status Codes Important?

Without status codes:

```json
{
  "message": "Student created"
}
```

The client cannot reliably know whether the request succeeded.

With status codes:

```text
201 Created
```

The client immediately knows a resource was created successfully.

---

# Status Code Categories

## 1xx – Informational

Rarely used in FastAPI applications.

Examples:

```text
100 Continue
101 Switching Protocols
```

---

## 2xx – Success

Request was successfully processed.

Examples:

```text
200 OK
201 Created
204 No Content
```

---

## 3xx – Redirects

Client should perform another request to a different URL.

Examples:

```text
301 Moved Permanently
302 Found
```

Mostly browser-related.

---

## 4xx – Client Errors

The client made a mistake.

Examples:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
422 Unprocessable Entity
```

---

## 5xx – Server Errors

The server encountered an error.

Examples:

```text
500 Internal Server Error
502 Bad Gateway
503 Service Unavailable
```

---

# 200 OK

Most common success code.

Meaning:

```text
Request processed successfully.
```

Example:

```python
@app.get("/students")
def get_students():
    return students
```

Response:

```text
200 OK
```

Commonly used with:

```http
GET
```

---

# 201 Created

Used when creating a new resource.

Example:

```python
@app.post(
    "/students",
    status_code=201
)
def create_student():
    return {
        "message": "Student created"
    }
```

Response:

```text
201 Created
```

Commonly used with:

```http
POST
```

---

# 204 No Content

Request succeeded but there is no response body.

Example:

```python
@app.delete(
    "/students/{id}",
    status_code=204
)
def delete_student(id: int):
    pass
```

Response:

```text
204 No Content
```

Response Body:

```text
(empty)
```

Commonly used with:

```http
DELETE
```

---

# 400 Bad Request

The client sent an invalid request.

Example:

```python
raise HTTPException(
    status_code=400,
    detail="Invalid input"
)
```

Response:

```json
{
  "detail": "Invalid input"
}
```

Examples:

- Missing required data
- Invalid query combinations
- Malformed requests

---

# 401 Unauthorized

Authentication is required.

Meaning:

```text
You are not logged in.
```

Example:

```python
raise HTTPException(
    status_code=401,
    detail="Login required"
)
```

Examples:

- Missing JWT token
- Invalid token
- Expired token

---

# 403 Forbidden

User is authenticated but lacks permission.

Meaning:

```text
I know who you are,
but you cannot access this resource.
```

Example:

```python
raise HTTPException(
    status_code=403,
    detail="Access denied"
)
```

Examples:

- Student accessing admin route
- Free user accessing premium content

---

# Difference Between 401 and 403

## 401 Unauthorized

```text
Who are you?
```

User not authenticated.

Examples:

- Not logged in
- Invalid token

---

## 403 Forbidden

```text
I know who you are,
but you are not allowed.
```

User authenticated but lacks permission.

Examples:

- Non-admin accessing admin panel
- Free user accessing premium content

---

# 404 Not Found

Requested resource does not exist.

Example:

```python
raise HTTPException(
    status_code=404,
    detail="Student not found"
)
```

Response:

```json
{
  "detail": "Student not found"
}
```

Examples:

```http
GET /students/999
```

when student 999 does not exist.

---

# 422 Unprocessable Entity

FastAPI automatically returns this when request validation fails.

Example:

Model:

```python
class Student(BaseModel):
    age: int = Field(
        ge=18
    )
```

Request:

```json
{
  "age": 10
}
```

Response:

```text
422 Unprocessable Entity
```

Examples:

- Invalid email
- Negative age
- Missing required field
- Wrong data type

---

# 500 Internal Server Error

Unexpected server-side failure.

Example:

```python
1 / 0
```

Response:

```text
500 Internal Server Error
```

Meaning:

```text
Backend bug or server failure.
```

Not the client's fault.

---

# HTTPException

FastAPI provides:

```python
from fastapi import HTTPException
```

Used to raise custom HTTP errors.

Example:

```python
raise HTTPException(
    status_code=404,
    detail="Student not found"
)
```

Response:

```json
{
  "detail": "Student not found"
}
```

---

# detail=

Used to send a human-readable error message to the client.

Example:

```python
raise HTTPException(
    status_code=403,
    detail="Access denied"
)
```

Response:

```json
{
  "detail": "Access denied"
}
```

---

# status_code=

Used in route decorators to define the success status code.

Example:

```python
@app.post(
    "/students",
    status_code=201
)
def create_student():
    return {
        "message": "Student created"
    }
```

Response:

```text
201 Created
```

---

# Real Student API Example

```python
from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()

students = {
    1: "Yadnyesh",
    2: "Rahul"
}

@app.get("/students/{id}")
def get_student(id: int):

    if id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "name": students[id]
    }
```

---

# TesLearn Example

```python
@app.get("/notes/{id}")
def get_note(id: int):

    note = find_note(id)

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note
```

---

# Production Convention

| Operation | Status Code |
|------------|------------|
| GET Success | 200 |
| POST Success | 201 |
| PUT Success | 200 |
| PATCH Success | 200 |
| DELETE Success | 204 |
| Invalid Request | 400 |
| Login Required | 401 |
| Permission Denied | 403 |
| Resource Not Found | 404 |
| Validation Failure | 422 |
| Backend Failure | 500 |

---

# Common Mistakes

## ❌ Returning 200 for Everything

Bad:

```python
{
    "success": False
}
```

with:

```text
200 OK
```

Use appropriate error codes.

---

## ❌ Confusing 401 and 403

Wrong:

```text
403 when user isn't logged in
```

Correct:

```text
401 when user isn't logged in
403 when user lacks permission
```

---

## ❌ Manually Returning Error Responses

Bad:

```python
return {
    "error": "Student not found"
}
```

Good:

```python
raise HTTPException(
    status_code=404,
    detail="Student not found"
)
```

---

# Interview Questions

1. What is a status code?
2. Why are status codes important?
3. Difference between 200 and 201?
4. When should 204 be used?
5. Difference between 401 and 403?
6. When is 404 returned?
7. What causes a 422 error in FastAPI?
8. What is 500 Internal Server Error?
9. What is HTTPException?
10. What is the purpose of detail=?
11. What is status_code=?
12. Why shouldn't every API return 200?

---

# Quick Cheat Sheet

```text
200 OK
Request successful
```

```text
201 Created
Resource created
```

```text
204 No Content
Deleted successfully
```

```text
400 Bad Request
Client request invalid
```

```text
401 Unauthorized
Not logged in
```

```text
403 Forbidden
No permission
```

```text
404 Not Found
Resource missing
```

```text
422 Unprocessable Entity
Validation failed
```

```text
500 Internal Server Error
Backend bug
```

---

# Key Takeaways

- Status codes tell the client what happened.
- 2xx codes represent success.
- 4xx codes represent client mistakes.
- 5xx codes represent server failures.
- Use status_code= for successful responses.
- Use HTTPException for custom errors.
- Use detail= to provide meaningful error messages.
- FastAPI automatically returns 422 on validation failures.
- Proper status codes make APIs professional and predictable.