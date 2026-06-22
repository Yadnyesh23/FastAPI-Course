# Phase 2.3 – Query Parameters

## Objectives

By the end of this phase, you should understand:

- What Query Parameters are
- Why Query Parameters are used
- Required Query Parameters
- Optional Query Parameters
- Default Values
- Multiple Query Parameters
- Boolean Query Parameters
- Combining Path & Query Parameters
- Internal Working
- Best Practices
- Common Mistakes

---

# What are Query Parameters?

A **Query Parameter** is a key-value pair added to the URL after the `?`.

It provides additional information to the server without changing the resource being accessed.

General Syntax:

```
/resource?key=value
```

Example:

```
/students?city=Mumbai
```

Here,

- `city` → Key
- `Mumbai` → Value

---

# Why do we use Query Parameters?

Query Parameters are mainly used for:

- Searching
- Filtering
- Sorting
- Pagination
- Optional configuration

Examples:

Search:

```
/notes?search=binary+tree
```

Filter:

```
/students?branch=AIDS
```

Sort:

```
/students?sort=name
```

Pagination:

```
/students?page=2
```

---

# Path Parameters vs Query Parameters

## Path Parameter

Used to identify a specific resource.

Example:

```
/students/10
```

Meaning:

> Give me Student 10.

---

## Query Parameter

Used to modify or filter the request.

Example:

```
/students?city=Mumbai
```

Meaning:

> Give me students from Mumbai.

---

# Easy Rule

Ask yourself:

**"Can this request exist without this value?"**

If **No**

→ Path Parameter

If **Yes**

→ Query Parameter

Examples:

```
/users/15
```

Without `15`, the request is incomplete.

Use a Path Parameter.

---

```
/users?city=Pune
```

Without `city`, the request is still valid.

Use a Query Parameter.

---

# First Query Parameter

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/students")
def get_students(city: str):
    return {
        "city": city
    }
```

Request:

```
/students?city=Mumbai
```

Response:

```json
{
    "city": "Mumbai"
}
```

---

# How FastAPI Detects Query Parameters

Example:

```python
@app.get("/students")
def get_students(city: str):
```

Notice:

The route path contains no `{city}`.

Therefore, FastAPI automatically treats `city` as a Query Parameter.

---

# Required Query Parameters

Example:

```python
@app.get("/search")
def search(q: str):
    return {
        "query": q
    }
```

Valid Request:

```
/search?q=FastAPI
```

Invalid Request:

```
/search
```

Response:

```
422 Unprocessable Entity
```

Reason:

`q` has no default value, so it is required.

---

# Optional Query Parameters

Using Python 3.10+

```python
@app.get("/search")
def search(q: str | None = None):
    return {
        "query": q
    }
```

Or using `Optional`

```python
from typing import Optional

@app.get("/search")
def search(q: Optional[str] = None):
```

Both are valid.

Request:

```
/search
```

Response:

```json
{
    "query": null
}
```

---

# Default Values

Example:

```python
@app.get("/students")
def get_students(page: int = 1):
    return {
        "page": page
    }
```

Request:

```
/students
```

Response:

```json
{
    "page": 1
}
```

Request:

```
/students?page=5
```

Response:

```json
{
    "page": 5
}
```

Providing a default value automatically makes the parameter optional.

---

# Multiple Query Parameters

Example:

```python
@app.get("/movies")
def get_movies(
    year: int,
    genre: str,
    language: str
):
    return {
        "year": year,
        "genre": genre,
        "language": language
    }
```

Request:

```
/movies?year=2025&genre=action&language=english
```

Multiple Query Parameters are separated using:

```
&
```

---

# Boolean Query Parameters

Example:

```python
@app.get("/users")
def get_users(active: bool = False):
    return {
        "active": active
    }
```

Request:

```
/users?active=true
```

Response:

```json
{
    "active": true
}
```

Request:

```
/users?active=false
```

Response:

```json
{
    "active": false
}
```

FastAPI automatically converts the string value into a Python boolean.

---

# Combining Path & Query Parameters

Example:

```python
@app.get("/students/{student_id}")
def get_student(
    student_id: int,
    include_marks: bool = False
):
    return {
        "student_id": student_id,
        "include_marks": include_marks
    }
```

Request:

```
/students/10?include_marks=true
```

Response:

```json
{
    "student_id": 10,
    "include_marks": true
}
```

FastAPI automatically identifies:

- `student_id` → Path Parameter
- `include_marks` → Query Parameter

---

# Internal Working

Request:

```
/students/15?include_marks=true
```

Conceptually, FastAPI performs:

```python
student_id = int("15")

include_marks = True

get_student(
    student_id=student_id,
    include_marks=include_marks
)
```

FastAPI automatically:

- Extracts values
- Converts data types
- Validates values
- Calls the route function

---

# Common Use Cases

Searching

```
/notes?search=sorting
```

Filtering

```
/students?branch=AIDS
```

Sorting

```
/products?sort=price
```

Pagination

```
/students?page=3
```

Boolean Filters

```
/users?active=true
```

Multiple Filters

```
/movies?year=2025&genre=action
```

---

# Best Practices

- Use Path Parameters to identify resources.
- Use Query Parameters for searching, filtering, sorting, and pagination.
- Give optional Query Parameters sensible default values.
- Use descriptive names such as:
  - page
  - limit
  - search
  - sort
  - order
  - active

---

# Common Mistakes

## ❌ Using Path Parameters for Filters

Bad:

```
/products/electronics
```

Better:

```
/products?category=electronics
```

---

## ❌ Forgetting Default Values

Bad:

```python
page: int
```

This makes the parameter required.

Better:

```python
page: int = 1
```

---

## ❌ Thinking All Query Parameters Are Optional

Not true.

A Query Parameter becomes optional only when it has a default value.

---

# Path vs Query Summary

| Path Parameter | Query Parameter |
|---------------|-----------------|
| Identifies a specific resource | Modifies or filters a request |
| Required | Can be required or optional |
| Appears inside `{}` | Appears after `?` |
| Example: `/students/5` | Example: `/students?page=2` |

---

# Interview Questions

1. What is a Query Parameter?
2. How does FastAPI distinguish between Path and Query Parameters?
3. What is the difference between required and optional Query Parameters?
4. When should you use a Path Parameter instead of a Query Parameter?
5. Why is `page: int = 1` preferred for pagination?
6. Can an endpoint contain both Path and Query Parameters?
7. What symbol separates multiple Query Parameters?

---

# Key Takeaways

- Query Parameters provide additional information about a request.
- They are commonly used for filtering, searching, sorting, and pagination.
- Parameters without default values are required.
- Parameters with default values are optional.
- FastAPI automatically performs type conversion and validation.
- Multiple Query Parameters are separated by `&`.
- Path Parameters identify resources, while Query Parameters modify how resources are returned.