# Phase 3.1 – Advanced Dependencies

## Objectives

By the end of this phase, you should understand:

- Dependency Graph
- Dependency Resolution Order
- Dependency Caching
- `use_cache=False`
- yield Dependencies
- Database Session Pattern
- Classes as Dependencies
- Dependency Overrides
- Best Practices

---

## 1. Dependency Graph

FastAPI builds a dependency graph before executing a route.

```python
def get_token():
    return "abc123"

def get_user(token: str = Depends(get_token)):
    return {"name": "Yadnyesh"}

@app.get("/")
def root(user=Depends(get_user)):
    return user
```

**Dependency Graph:**

```
root()
  ↑
get_user()
  ↑
get_token()
```

**Execution Order:**

```
Request
  ↓
get_token()
  ↓
get_user()
  ↓
root()
  ↓
Response
```

---

## 2. Dependency Caching

FastAPI executes the same dependency only once per request.

```python
def get_user():
    print("Running...")
    return {"name": "Yadnyesh"}

@app.get("/")
def root(
    user1=Depends(get_user),
    user2=Depends(get_user)
):
    return {"u1": user1, "u2": user2}
```

**Output:** `Running...` — printed only once.

---

## 3. Cache Scope

The cache is **per request**, not global.

```
Request 1:  get_user() ← executed
Request 2:  get_user() ← executed again
```

---

## 4. Disabling Cache

Use `use_cache=False` to force the dependency to run every time it is requested within the same request.

```python
Depends(get_time, use_cache=False)
```

---

## 5. yield Dependencies

This is one of the most important FastAPI patterns.

**Problem with `return`:**

```python
def get_db():
    db = SessionLocal()
    return db  # ❌ connection is never closed
```

**Correct Pattern:**

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 6. How yield Works

```
Open Resource
  ↓
yield Resource
  ↓
Route Executes
  ↓
Resume Dependency
  ↓
Cleanup Resource
```

FastAPI **pauses** the dependency at `yield`, runs the route, then **resumes** the dependency to execute cleanup code.

---

## 7. Why yield Is Used for Database Sessions

Database connections must be:

1. Opened
2. Used
3. Closed

If connections are never closed, the application suffers from **connection leaks** and eventually the database refuses new connections.

---

## 8. return vs yield

| Feature | `return` | `yield` |
|---|---|---|
| Ends the function | ✅ | ❌ |
| Can resume later | ❌ | ✅ |
| Cleanup after route | ❌ | ✅ |
| Use case | Simple values | Resources needing cleanup |

---

## 9. Classes as Dependencies

Dependencies can be classes.

```python
class Pagination:
    def __init__(self, limit: int = 10, skip: int = 0):
        self.limit = limit
        self.skip = skip

@app.get("/students")
def students(query: Pagination = Depends()):
    return {"limit": query.limit, "skip": query.skip}
```

**Request:** `/students?limit=5&skip=15`

**Response:** `{"limit": 5, "skip": 15}`

---

## 10. Why Use Classes as Dependencies?

Useful for grouping related parameters such as:

- Pagination
- Filters
- Search options
- Sorting
- Configuration

---

## 11. Dependency Overrides

Used mainly for **testing**.

```python
# Real dependency
def get_db():
    return RealDatabase()

# Fake dependency
def fake_db():
    return FakeDatabase()

# Override
app.dependency_overrides[get_db] = fake_db
```

Now every route using `Depends(get_db)` receives `FakeDatabase()`.

---

## 12. Why Dependency Overrides Are Useful

They make tests:

- ⚡ Faster
- 🔒 Safer
- 🔗 Independent of real databases
- 🎯 Predictable

---

## 13. Best Practices

**Keep dependencies focused.**

```python
# ❌ Bad
def do_everything(): ...

# ✅ Good
def get_current_user(): ...
def get_db(): ...
def verify_admin(): ...
```

**Use `yield` for cleanup** — whenever a resource must be closed or cleaned up.

**Reuse dependencies** — write authentication, database, and permission logic once and reuse it across routes.

**Keep business logic out of dependencies** — dependencies should prepare resources or validate access, not implement core business rules.

---

## 14. Real-World Pattern

```python
def get_current_user():
    ...

def get_db():
    yield db

@app.post("/notes")
def create_note(
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    ...
```

**Execution Flow:**

```
Request
  ↓
Verify User
  ↓
Open DB Connection
  ↓
Execute Route
  ↓
Close DB Connection
  ↓
Response
```

---

## 15. Interview Questions

1. What is a Dependency Graph?
2. How does FastAPI resolve dependencies?
3. What is Dependency Caching?
4. When is the cache cleared?
5. What does `use_cache=False` do?
6. What is a yield dependency?
7. Why is `yield` used for database sessions?
8. Difference between `return` and `yield`?
9. Can classes be dependencies?
10. What are Dependency Overrides?
11. Why are Dependency Overrides useful during testing?
12. What are the benefits of Dependency Injection?

---

## 16. Quick Cheat Sheet

| Feature | Purpose |
|---|---|
| `Depends()` | Inject dependency |
| `use_cache=False` | Disable per-request caching |
| `yield` | Setup + Cleanup |
| `get_db()` | Database session dependency |
| Class Dependency | Group related parameters |
| `dependency_overrides` | Replace dependencies during tests |

---

## 17. Key Takeaways

- FastAPI builds a dependency graph automatically.
- Dependencies are executed in the correct order.
- Dependency results are **cached per request**.
- `yield` dependencies support setup and cleanup.
- Database sessions should use `yield`.
- Classes can be used as dependencies.
- Dependency Overrides make testing easy.
- Small, reusable dependencies are a core FastAPI best practice.