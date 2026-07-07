# Phase 2.4 – Request Body

## Objectives

By the end of this phase, you should understand:

- What a Request Body is
- Why Request Bodies are used
- JSON Request Bodies
- Pydantic Models
- Automatic Validation
- Automatic Type Conversion
- Required Fields
- Optional Fields
- Default Values
- Request Body vs Query Parameters
- Internal Working

---

# What is a Request Body?

A Request Body is the data sent by the client to the server inside an HTTP request.

Example:

POST /students

Body:

```json
{
  "name": "Yadnyesh",
  "age": 20,
  "branch": "AIDS"
}
```

The server receives this data and processes it.

---

# Why Do We Need Request Bodies?

Small pieces of information can be sent using Query Parameters:

```text
/students?branch=AIDS
```

But complex data becomes difficult:

```json
{
  "name": "Yadnyesh",
  "age": 20,
  "branch": "AIDS",
  "skills": [
    "Python",
    "FastAPI",
    "Machine Learning"
  ]
}
```

For structured data, Request Bodies are preferred.

---

# Common Uses of Request Bodies

Creating Data

```http
POST /students
```

Updating Data

```http
PUT /students/1
```

Partial Updates

```http
PATCH /students/1
```

Examples:

- User Registration
- Login
- Creating Notes
- Creating Products
- Updating Profiles
- Posting Comments

---

# JSON

Most modern APIs use JSON.

Example:

```json
{
  "title": "Binary Trees",
  "subject": "DSA",
  "duration": 45
}
```

JSON is the standard format for communication between frontend and backend.

---

# Pydantic

FastAPI uses Pydantic for:

- Data Validation
- Type Conversion
- Error Handling
- Automatic Documentation

Pydantic ensures incoming data follows predefined rules.

---

# Creating a Pydantic Model

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    branch: str
```

This class is called a Pydantic Model.

---

# Using a Model in a Route

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    branch: str

@app.post("/students")
def create_student(student: Student):
    return student
```

FastAPI automatically expects a JSON Request Body matching the model.

---

# Sending Data

Request:

```json
{
  "name": "Yadnyesh",
  "age": 20,
  "branch": "AIDS"
}
```

Response:

```json
{
  "name": "Yadnyesh",
  "age": 20,
  "branch": "AIDS"
}
```

---

# How FastAPI Detects a Request Body

Example:

```python
def create_student(student: Student):
```

Since Student is a Pydantic Model, FastAPI understands:

```text
This parameter should come from the Request Body.
```

---

# Automatic Validation

Model:

```python
class Student(BaseModel):
    name: str
    age: int
```

Request:

```json
{
  "name": "Yadnyesh",
  "age": "abc"
}
```

Result:

```text
422 Unprocessable Entity
```

FastAPI automatically validates data types.

---

# Automatic Type Conversion

Request:

```json
{
  "name": "Yadnyesh",
  "age": "20"
}
```

Pydantic automatically converts:

```text
"20"
```

to

```python
20
```

---

# Required Fields

Model:

```python
class Student(BaseModel):
    name: str
    age: int
    branch: str
```

All fields are required.

Request:

```json
{
  "name": "Yadnyesh"
}
```

Result:

```text
422 Unprocessable Entity
```

because age and branch are missing.

---

# Optional Fields

Python 3.10+

```python
class Student(BaseModel):
    name: str
    age: int
    branch: str | None = None
```

Now branch becomes optional.

Valid Request:

```json
{
  "name": "Yadnyesh",
  "age": 20
}
```

---

# Default Values

```python
class Course(BaseModel):
    name: str
    duration: int = 30
```

Request:

```json
{
  "name": "FastAPI"
}
```

Result:

```json
{
  "name": "FastAPI",
  "duration": 30
}
```

---

# Accessing Request Body Data

Model:

```python
class Student(BaseModel):
    name: str
    age: int
```

Route:

```python
@app.post("/students")
def create_student(student: Student):
    return {
        "message": f"{student.name} created"
    }
```

Access fields using:

```python
student.name
student.age
```

---

# Internal Working

Request:

```json
{
  "name": "Yadnyesh",
  "age": 20,
  "branch": "AIDS"
}
```

FastAPI conceptually performs:

```python
student = Student(
    name="Yadnyesh",
    age=20,
    branch="AIDS"
)

create_student(student)
```

If validation fails, FastAPI automatically returns an error.

---

# Request Body vs Query Parameters

## Query Parameters

Used for:

- Searching
- Filtering
- Sorting
- Pagination

Example:

```text
/students?branch=AIDS
```

---

## Request Body

Used for:

- Creating Data
- Updating Data

Example:

```json
{
  "name": "Yadnyesh",
  "age": 20,
  "branch": "AIDS"
}
```

---

# Best Practices

- Use Request Bodies for creating and updating resources.
- Use Query Parameters for filtering and searching.
- Use Pydantic Models for all Request Bodies.
- Add proper type hints.
- Use default values when appropriate.
- Make fields optional only when necessary.

---

# Common Mistakes

## ❌ Using Query Parameters for Complex Data

Bad:

```text
/students?name=Yadnyesh&age=20&branch=AIDS
```

Better:

```json
{
  "name": "Yadnyesh",
  "age": 20,
  "branch": "AIDS"
}
```

---

## ❌ Forgetting Default Value for Optional Fields

Bad:

```python
bio: str | None
```

Better:

```python
bio: str | None = None
```

---

## ❌ Not Using Pydantic Models

Bad:

```python
@app.post("/students")
def create_student(name: str, age: int):
```

Better:

```python
class Student(BaseModel):
    name: str
    age: int

@app.post("/students")
def create_student(student: Student):
```

---

# Interview Questions

1. What is a Request Body?
2. Why are Request Bodies preferred over Query Parameters for complex data?
3. What is a Pydantic Model?
4. How does FastAPI know data should come from the Request Body?
5. What happens if a required field is missing?
6. What happens if "20" is sent for an integer field?
7. What is the difference between Query Parameters and Request Bodies?
8. How do you make a field optional in a Pydantic Model?

---

# Key Takeaways

- Request Bodies send data from client to server.
- Most APIs use JSON Request Bodies.
- FastAPI uses Pydantic Models to define data structure.
- Pydantic provides validation and type conversion.
- Missing required fields result in a 422 error.
- Optional fields require a default value.
- Request Bodies are used for creating and updating resources.
- Query Parameters are used for filtering and searching.