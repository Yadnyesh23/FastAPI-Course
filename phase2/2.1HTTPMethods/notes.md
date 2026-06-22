# Phase 2.1 – HTTP Methods

## Objectives

Learn:

- HTTP
- HTTP Request
- HTTP Response
- REST
- GET
- POST
- PUT
- PATCH
- DELETE
- CRUD
- Safe Methods
- Idempotency

---

# HTTP

HTTP (HyperText Transfer Protocol) is the communication protocol used between clients and servers.

Example flow:

Client → HTTP Request → Server → HTTP Response → Client

---

# HTTP Request

An HTTP request contains:

- Method
- URL
- Headers
- Body (optional)

Example:

GET /students HTTP/1.1

---

# HTTP Response

A response contains:

- Status Code
- Headers
- Body

Example:

```json
{
  "id": 1,
  "name": "Yadnyesh"
}
```

---

# REST

REST treats application data as resources.

Examples:

- /students
- /users
- /books
- /products

The HTTP method defines the action to perform on the resource.

---

# GET

Purpose:

Retrieve data.

Characteristics:

- Reads data
- Safe
- Idempotent
- Usually has no request body

Example:

```python
@app.get("/students")
def get_students():
    return students
```

---

# POST

Purpose:

Create a new resource.

Characteristics:

- Creates data
- Not safe
- Not idempotent

Example:

```python
@app.post("/students")
def create_student():
    ...
```

---

# PUT

Purpose:

Replace an entire resource.

Characteristics:

- Updates the complete object
- Not safe
- Idempotent

Example:

```python
@app.put("/students/{student_id}")
def update_student(student_id: int):
    ...
```

---

# PATCH

Purpose:

Update only selected fields of a resource.

Characteristics:

- Partial update
- Not safe
- Not guaranteed to be idempotent

Example:

```python
@app.patch("/students/{student_id}")
def partially_update_student(student_id: int):
    ...
```

---

# DELETE

Purpose:

Delete a resource.

Characteristics:

- Removes data
- Not safe
- Idempotent

Example:

```python
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    ...
```

---

# CRUD Mapping

| CRUD Operation | HTTP Method |
|----------------|-------------|
| Create | POST |
| Read | GET |
| Update (Full) | PUT |
| Update (Partial) | PATCH |
| Delete | DELETE |

---

# Safe Methods

A safe method does not modify server data.

Safe:

- GET

Not Safe:

- POST
- PUT
- PATCH
- DELETE

---

# Idempotency

A request is idempotent if repeating it multiple times results in the same final state.

| Method | Idempotent |
|----------|------------|
| GET | Yes |
| PUT | Yes |
| DELETE | Yes |
| POST | No |
| PATCH | Usually No |

---

# REST Best Practices

Use nouns in URLs:

Good:

- /students
- /users
- /products

Avoid verbs:

- /getStudents
- /createStudent
- /deleteStudent

---

# FastAPI Routing

A route is identified by both:

- HTTP Method
- URL Path

Example:

```python
@app.get("/students")
@app.post("/students")
```

These are two different routes because the HTTP methods are different.

---

# Key Takeaways

- HTTP defines communication between clients and servers.
- REST organizes APIs around resources.
- GET retrieves data.
- POST creates data.
- PUT replaces an entire resource.
- PATCH updates part of a resource.
- DELETE removes a resource.
- GET is safe and idempotent.
- POST is not idempotent.
- FastAPI routes are matched using both the URL and the HTTP method.