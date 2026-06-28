# Phase 4.3 – Advanced APIRouter Features

## Objectives

By the end of this phase, you should understand:

- Router-Level Dependencies
- Router-Level Responses
- Default Status Codes
- Nested Routers
- API Versioning
- Route Naming
- `include_router()` Options
- Best Practices

---

# 1. Router-Level Dependencies

Instead of adding the same dependency to every route, FastAPI allows you to apply a dependency to the entire router.

### Without Router-Level Dependency

```python
@router.get("/")
def get_students(user=Depends(get_current_user)):
    ...

@router.post("/")
def create_student(
    student: StudentCreate,
    user=Depends(get_current_user)
):
    ...
```

The same dependency is repeated for every route.

### With Router-Level Dependency

```python
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/students",
    tags=["Students"],
    dependencies=[Depends(get_current_user)]
)
```

Now every route inside this router automatically executes:

```python
get_current_user()
```

before the route function runs.

### Benefits

- Reduces code duplication
- Cleaner routers
- Easier maintenance
- Follows the DRY (Don't Repeat Yourself) principle

---

# 2. Route-Level vs Router-Level Dependencies

## Route-Level Dependency

Applied only to a specific route.

```python
@router.get("/")
def get_students(
    user=Depends(get_current_user)
):
    ...
```

Only this endpoint requires authentication.

---

## Router-Level Dependency

Applied to the entire router.

```python
router = APIRouter(
    dependencies=[Depends(get_current_user)]
)
```

Every endpoint inside the router requires authentication.

---

# 3. Router-Level Responses

Sometimes every endpoint can return the same response.

Example:

- 401 Unauthorized
- 403 Forbidden

Instead of repeating:

```python
responses={
    401: {
        "description": "Unauthorized"
    }
}
```

for every route,

define it once:

```python
router = APIRouter(
    responses={
        401: {
            "description": "Unauthorized"
        }
    }
)
```

Swagger automatically shows this response for all routes in the router.

### Benefits

- Consistent documentation
- Less repetition
- Cleaner code

---

# 4. Default Status Codes

Status codes can be defined directly on routes.

Example:

```python
@router.post(
    "/",
    status_code=201
)
def create_student(student: StudentCreate):
    return student
```

Common Status Codes:

| Status Code | Meaning |
|-------------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

# 5. Nested Routers

Nested routers organize related APIs hierarchically.

Example:

```text
/users
/users/{id}
/users/{id}/notes
/users/{id}/notes/{note_id}
```

Instead of placing every endpoint in one large router, related resources are grouped together.

Example:

```python
users_router.include_router(notes_router)
```

### Benefits

- Better organization
- Easier navigation
- Logical API hierarchy

---

# 6. API Versioning

When an API changes significantly, older clients should continue working.

Versioning allows multiple API versions to exist.

Example:

```text
/api/v1/students
/api/v2/students
```

Including routers:

```python
app.include_router(
    student_router,
    prefix="/api/v1"
)

app.include_router(
    student_router_v2,
    prefix="/api/v2"
)
```

### Benefits

- Backward compatibility
- Easier upgrades
- No breaking changes for existing clients

---

# 7. Route Naming

Routes can be given an internal name.

Example:

```python
@router.get(
    "/students",
    name="Get All Students"
)
def get_students():
    ...
```

### Uses

- Better documentation
- URL generation
- Logging
- Debugging

---

# 8. `include_router()` Options

Basic usage:

```python
app.include_router(student_router)
```

Advanced usage:

```python
app.include_router(
    student_router,
    prefix="/api/v1",
    tags=["Students"],
    dependencies=[Depends(get_current_user)],
    responses={
        404: {
            "description": "Not Found"
        }
    }
)
```

### Common Options

| Option | Purpose |
|---------|---------|
| `prefix` | Adds a common URL prefix |
| `tags` | Groups endpoints in Swagger |
| `dependencies` | Applies dependencies to all routes |
| `responses` | Defines common responses |

---

# 9. Real Project Example

```python
students_router = APIRouter(
    prefix="/students",
    tags=["Students"],
    dependencies=[Depends(get_current_user)],
    responses={
        401: {
            "description": "Unauthorized"
        }
    }
)

@students_router.get("/")
def get_students():
    ...

@students_router.post(
    "/",
    status_code=201
)
def create_student(student: StudentCreate):
    return student
```

Main application:

```python
from fastapi import FastAPI
from routers.students import students_router

app = FastAPI()

app.include_router(
    students_router,
    prefix="/api/v1"
)
```

Final URLs:

```text
GET  /api/v1/students
POST /api/v1/students
```

---

# 10. When Should You Use Each Feature?

### Use Router-Level Dependencies When

- Every route requires authentication.
- Every route needs a database session.
- Every route requires admin access.

### Use Route-Level Dependencies When

- Only specific routes need authentication or permissions.

### Use Router-Level Responses When

- All endpoints share common error responses.

### Use API Versioning When

- Releasing a new version of the API without breaking existing clients.

### Use Nested Routers When

- APIs represent parent-child relationships.

---

# 11. Best Practices

- Keep routers focused on one resource.
- Apply common dependencies at the router level.
- Use meaningful tags for Swagger documentation.
- Use API versioning for breaking changes.
- Keep consistent response documentation.
- Organize related routes using nested routers.
- Avoid duplicating dependencies across routes.

---

# 12. Interview Questions

1. What are router-level dependencies?
2. What is the difference between route-level and router-level dependencies?
3. Why use router-level responses?
4. What is API versioning?
5. Why is API versioning important?
6. What are nested routers?
7. What is the purpose of the `name` parameter in a route?
8. Name four commonly used `include_router()` options.
9. When should router-level dependencies be preferred?
10. What are the advantages of router-level dependencies?

---

# 13. Quick Cheat Sheet

| Feature | Purpose |
|----------|---------|
| Router-Level Dependency | Apply the same dependency to all routes in a router |
| Route-Level Dependency | Apply a dependency to one specific route |
| Router-Level Responses | Define common responses once for all routes |
| `status_code` | Set the HTTP status code returned by a route |
| Nested Routers | Organize related routes hierarchically |
| API Versioning | Support multiple API versions simultaneously |
| `name` | Assign an internal name to a route |
| `include_router()` | Register routers with the FastAPI application |

---

# 14. Key Takeaways

- Router-level dependencies eliminate repeated `Depends()` calls.
- Route-level dependencies apply only to individual endpoints.
- Router-level responses keep API documentation consistent.
- `status_code` helps follow proper HTTP standards.
- Nested routers create a clean hierarchy for related resources.
- API versioning allows new API versions without breaking existing clients.
- Route names improve documentation and debugging.
- `include_router()` supports options like `prefix`, `tags`, `dependencies`, and `responses`.
- Using these features results in cleaner, more scalable, and production-ready FastAPI applications.