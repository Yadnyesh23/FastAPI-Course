# Phase 2.5 – Pydantic Models Deep Dive

## Objectives

By the end of this phase, you should understand:

- Why FastAPI uses Pydantic
- BaseModel
- Common Field Types
- Optional Fields
- Default Values
- Lists
- Dictionaries
- Nested Models
- Lists of Models
- Field Metadata
- Validation Constraints
- model_dump()
- model_validate()
- How FastAPI uses Pydantic internally

---

# Why Does FastAPI Use Pydantic?

FastAPI uses Pydantic for:

- Data Validation
- Type Conversion
- Parsing
- Serialization
- Error Handling
- API Documentation

Without Pydantic:

```python
data = request.json()

name = data["name"]
age = int(data["age"])
```

You must manually validate and convert data.

With Pydantic:

```python
class User(BaseModel):
    name: str
    age: int
```

Pydantic handles validation automatically.

---

# BaseModel

Every Pydantic model inherits from:

```python
BaseModel
```

Example:

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
```

BaseModel provides:

- Validation
- Parsing
- Serialization
- Type Conversion
- Error Handling

---

# Common Field Types

```python
class User(BaseModel):
    name: str
    age: int
    cgpa: float
    active: bool
```

Common types:

| Type | Example |
|--------|----------|
| str | "Yadnyesh" |
| int | 20 |
| float | 8.5 |
| bool | True |
| list | ["Python"] |
| dict | {"views": 100} |

---

# Optional Fields

Python 3.10+

```python
class User(BaseModel):
    username: str
    bio: str | None = None
```

Important:

```python
bio: str | None = None
```

The `= None` makes the field optional.

Valid Request:

```json
{
  "username": "Yadnyesh"
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

# Lists

Models can accept lists.

```python
class Student(BaseModel):
    name: str
    skills: list[str]
```

Request:

```json
{
  "name": "Yadnyesh",
  "skills": [
    "Python",
    "FastAPI",
    "Machine Learning"
  ]
}
```

---

# Dictionary Fields

```python
class Analytics(BaseModel):
    stats: dict[str, int]
```

Request:

```json
{
  "stats": {
    "views": 100,
    "likes": 20
  }
}
```

---

# Nested Models

A Nested Model is a Pydantic model used inside another model.

Example:

```python
class Address(BaseModel):
    city: str
    state: str


class Student(BaseModel):
    name: str
    address: Address
```

Request:

```json
{
  "name": "Yadnyesh",
  "address": {
    "city": "Mumbai",
    "state": "Maharashtra"
  }
}
```

Pydantic validates both models automatically.

---

# Lists of Models

You can store multiple models inside a list.

```python
class Skill(BaseModel):
    name: str
    level: str


class Student(BaseModel):
    name: str
    skills: list[Skill]
```

Request:

```json
{
  "name": "Yadnyesh",
  "skills": [
    {
      "name": "Python",
      "level": "Advanced"
    },
    {
      "name": "FastAPI",
      "level": "Intermediate"
    }
  ]
}
```

---

# Field Metadata

Pydantic provides:

```python
from pydantic import Field
```

Example:

```python
class Student(BaseModel):
    name: str = Field(
        description="Student Name",
        examples=["Yadnyesh"]
    )
```

Uses:

- Description
- Examples
- Documentation
- Validation Rules

Swagger automatically displays this information.

---

# Validation Constraints

## Numeric Constraints

```python
from pydantic import Field

class Student(BaseModel):
    age: int = Field(
        ge=18,
        le=30
    )
```

Meaning:

```text
18 <= age <= 30
```

---

## Greater Than

```python
class Product(BaseModel):
    price: float = Field(
        gt=0
    )
```

Meaning:

```text
price > 0
```

---

## Less Than

```python
class Product(BaseModel):
    discount: int = Field(
        lt=100
    )
```

Meaning:

```text
discount < 100
```

---

# model_dump()

Pydantic v2 uses:

```python
model_dump()
```

Purpose:

Convert a Pydantic model into a Python dictionary.

Example:

```python
student = Student(
    name="Yadnyesh",
    age=20
)

student.model_dump()
```

Result:

```python
{
    "name": "Yadnyesh",
    "age": 20
}
```

---

# model_validate()

Purpose:

Convert raw data into a validated Pydantic model.

Example:

```python
data = {
    "name": "Yadnyesh",
    "age": 20
}

student = Student.model_validate(data)
```

Result:

```python
Student(
    name="Yadnyesh",
    age=20
)
```

---

# model_dump() vs model_validate()

| Method | Purpose |
|----------|----------|
| model_validate() | Dictionary → Pydantic Model |
| model_dump() | Pydantic Model → Dictionary |

Think:

```text
model_validate()
Raw Data → Model
```

```text
model_dump()
Model → Dictionary
```

They are opposite operations.

---

# Accessing Model Data

Example:

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
        "name": student.name,
        "age": student.age
    }
```

Access fields using:

```python
student.name
student.age
```

---

# Internal Working in FastAPI

Request:

```json
{
  "name": "Yadnyesh",
  "age": 20
}
```

FastAPI conceptually performs:

```python
student = Student.model_validate(
    request_data
)

create_student(student)
```

If validation fails:

```text
422 Unprocessable Entity
```

is returned automatically.

---

# What Happens If Nested Data Is Invalid?

Model:

```python
class Address(BaseModel):
    city: str


class Student(BaseModel):
    name: str
    address: Address
```

Invalid Request:

```json
{
  "name": "Yadnyesh",
  "address": {
    "city": 123
  }
}
```

Result:

```text
422 Unprocessable Entity
```

Pydantic validates nested models as well.

---

# Real-World Example

TesLearn Note:

```json
{
  "title": "Binary Trees",
  "subject": "DSA",
  "author": {
    "name": "Yadnyesh",
    "email": "abc@gmail.com"
  },
  "tags": [
    "trees",
    "dsa",
    "algorithms"
  ]
}
```

Pydantic Models:

```python
class Author(BaseModel):
    name: str
    email: str


class Note(BaseModel):
    title: str
    subject: str
    author: Author
    tags: list[str]
```

Benefits:

- Organized Structure
- Better Validation
- Reusability
- Easier Maintenance
- Matches Real-World Data

---

# Best Practices

- Always inherit from BaseModel.
- Use Nested Models for structured data.
- Use Lists for collections.
- Use Field() for validation and metadata.
- Keep models small and reusable.
- Use model_dump() when converting models to dictionaries.
- Use model_validate() when converting raw data into models.

---

# Common Mistakes

## ❌ Forgetting = None

Bad:

```python
bio: str | None
```

Good:

```python
bio: str | None = None
```

---

## ❌ Using One Giant Model

Bad:

```python
class Student(BaseModel):
    name: str
    city: str
    state: str
    country: str
```

Better:

```python
class Address(BaseModel):
    city: str
    state: str


class Student(BaseModel):
    name: str
    address: Address
```

---

## ❌ Ignoring Validation Rules

Bad:

```python
age: int
```

Better:

```python
age: int = Field(
    ge=18,
    le=30
)
```

---

# Interview Questions

1. Why does FastAPI use Pydantic?
2. What is BaseModel?
3. What is the purpose of Field()?
4. Difference between list[str] and dict[str, int]?
5. What is a Nested Model?
6. What does model_dump() do?
7. What does model_validate() do?
8. Why are Nested Models useful?
9. How would you restrict age between 18 and 30?
10. What happens if nested JSON is invalid?

---

# Key Takeaways

- Pydantic is responsible for validation and type conversion in FastAPI.
- Every model inherits from BaseModel.
- Nested Models represent structured real-world data.
- Lists and Dictionaries are fully supported.
- Field() adds metadata and validation constraints.
- model_validate() converts raw data into models.
- model_dump() converts models into dictionaries.
- FastAPI automatically uses Pydantic for request validation.
- Invalid data results in a 422 Unprocessable Entity response.