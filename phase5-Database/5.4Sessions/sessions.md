# Phase 5.4 – SQLAlchemy Sessions

## Objectives

By the end of this phase, you should understand:

- What is a Session?
- Why do we need a Session?
- Engine vs Session
- `sessionmaker`
- Creating a Session
- Session Lifecycle
- `add()`
- `commit()`
- `rollback()`
- `refresh()`
- `close()`
- Using Sessions with FastAPI Dependency Injection
- `autocommit`
- `autoflush`

---

# 1. What is a Session?

A **Session** is a workspace (or conversation) between your application and the database.

It is responsible for managing all database operations during a request.

Using a Session, we can:

- Create data
- Read data
- Update data
- Delete data
- Manage transactions

Without a Session, SQLAlchemy cannot perform CRUD operations.

---

# 2. Why Do We Need a Session?

The Engine only knows **how to connect** to the database.

It does not keep track of objects or database changes.

The Session:

- Tracks ORM objects
- Executes database queries
- Manages transactions
- Coordinates with the Engine

Architecture:

```text
FastAPI
    │
    ▼
Session
    │
    ▼
Engine
    │
    ▼
PostgreSQL
```

---

# 3. Engine vs Session

| Engine | Session |
|---------|---------|
| Creates and manages database connections | Performs CRUD operations |
| Manages the connection pool | Manages transactions |
| Created once when the application starts | Created for every request |
| Does not track ORM objects | Tracks ORM objects and their changes |
| Handles communication with the database | Uses the Engine to communicate with the database |

---

# 4. What is `sessionmaker`?

Creating Sessions manually every time would be repetitive.

SQLAlchemy provides **`sessionmaker`**, which acts as a factory for creating Session objects.

Example:

```python
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)
```

Flow:

```text
sessionmaker
      │
      ▼
Creates Session Objects
```

---

# 5. Creating a Session

A new Session is created using:

```python
db = SessionLocal()
```

Every incoming request gets its own Session.

Example:

```text
Request 1
    │
    ▼
Session 1

Request 2
    │
    ▼
Session 2
```

Sessions should never be shared between requests.

---

# 6. Session Lifecycle

Typical workflow:

```text
Request
    │
    ▼
Create Session
    │
    ▼
Perform CRUD Operations
    │
    ▼
Commit or Rollback
    │
    ▼
Close Session
    │
    ▼
Response
```

---

# 7. `add()`

`add()` tells SQLAlchemy to start tracking an object that should be inserted into the database.

Example:

```python
student = Student(
    name="Yadnyesh",
    age=20
)

db.add(student)
```

### Important

At this stage, the object is **not yet saved** in the database.

It is only added to the current Session.

---

# 8. `commit()`

`commit()` permanently saves all pending changes to the database.

Example:

```python
db.commit()
```

Flow:

```text
Create Object
      │
      ▼
db.add()
      │
      ▼
db.commit()
      │
      ▼
Saved in Database
```

Without `commit()`, the changes are discarded when the Session ends.

---

# 9. `rollback()`

If an error occurs before committing, the Session can roll back the transaction.

Example:

```python
db.rollback()
```

Purpose:

- Undo all uncommitted changes
- Restore the database to its previous consistent state

Flow:

```text
Insert Student
      │
      ▼
Insert Teacher
      │
      ▼
Error Occurs
      │
      ▼
Rollback
      │
      ▼
Nothing is Saved
```

---

# 10. `refresh()`

After committing, the database may generate new values automatically (such as an auto-incremented primary key).

`refresh()` reloads the object from the database.

Example:

```python
db.commit()
db.refresh(student)
```

Before Refresh:

```text
student.id = None
```

After Refresh:

```text
student.id = 1
```

This ensures the Python object contains the latest values stored in the database.

---

# 11. `close()`

When all operations are complete, the Session should be closed.

Example:

```python
db.close()
```

Purpose:

- Closes the Session
- Returns the database connection to the connection pool
- Prevents connection leaks

If Sessions are never closed:

- Database connections remain occupied
- Connection pool becomes exhausted
- New requests may fail

---

# 12. Using Sessions in FastAPI

Instead of manually creating and closing Sessions inside every route, FastAPI uses Dependency Injection.

Example:

```python
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

This is the recommended pattern for FastAPI applications.

---

# 13. Using the Session in Routes

Example:

```python
from fastapi import Depends

@app.get("/students")
def get_students(db = Depends(get_db)):
    ...
```

Flow:

```text
Request
    │
    ▼
Depends(get_db)
    │
    ▼
Create Session
    │
    ▼
Inject Session into Route
    │
    ▼
Execute Route
    │
    ▼
Close Session
    │
    ▼
Response
```

---

# 14. Complete CRUD Flow

```text
Client
    │
    ▼
FastAPI Route
    │
    ▼
Depends(get_db)
    │
    ▼
SessionLocal()
    │
    ▼
Session
    │
    ▼
Engine
    │
    ▼
PostgreSQL
    │
    ▼
Response
```

---

# 15. Example

```python
student = Student(
    name="Yadnyesh",
    age=20
)

db.add(student)

db.commit()

db.refresh(student)

return student
```

Execution:

```text
Create Student Object
        │
        ▼
Add to Session
        │
        ▼
Commit Transaction
        │
        ▼
Refresh Object
        │
        ▼
Return Response
```

---

# 16. `autocommit=False`

Example:

```python
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False
)
```

Meaning:

Changes are **not automatically saved**.

The developer must explicitly call:

```python
db.commit()
```

Benefits:

- Better transaction control
- Prevents accidental data changes

---

# 17. `autoflush=False`

Example:

```python
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False
)
```

Meaning:

SQLAlchemy does not automatically send pending changes to the database before executing queries.

Instead, changes are sent when you explicitly call:

- `commit()`
- `flush()`

Benefits:

- More predictable behavior
- Greater control over database operations

---

# 18. Project Structure

```text
app/
│
├── database/
│   ├── connection.py
│   ├── base.py
│   └── session.py
│
├── models/
├── routers/
├── services/
└── main.py
```

Example `session.py`:

```python
from sqlalchemy.orm import sessionmaker

from app.database.connection import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

# 19. Best Practices

- Create one Session per request.
- Never share a Session across multiple requests.
- Always close the Session after use.
- Use Dependency Injection with `yield`.
- Call `commit()` only after successful operations.
- Call `rollback()` when an exception occurs.
- Call `refresh()` after `commit()` if you need database-generated values.
- Keep `autocommit=False` to control transactions explicitly.

---

# 20. Interview Questions

1. What is a Session in SQLAlchemy?
2. Why do we need a Session if we already have an Engine?
3. What is `sessionmaker`?
4. Why is a new Session created for every request?
5. What does `add()` do?
6. What does `commit()` do?
7. What is `rollback()`?
8. Why do we use `refresh()`?
9. Why should Sessions always be closed?
10. Why do we use `yield` inside `get_db()`?
11. Difference between Engine and Session.
12. What is `autocommit=False`?
13. What is `autoflush=False`?

---

# 21. Quick Cheat Sheet

| Feature | Purpose |
|----------|---------|
| Session | Workspace for interacting with the database |
| `sessionmaker` | Factory that creates Session objects |
| `SessionLocal()` | Creates a new Session |
| `add()` | Adds an object to the current Session |
| `commit()` | Saves changes permanently |
| `rollback()` | Undoes uncommitted changes |
| `refresh()` | Reloads the object with the latest database values |
| `close()` | Closes the Session and returns the connection to the pool |
| `yield` | Ensures setup before the route and cleanup after the route |
| `autocommit=False` | Requires explicit commits |
| `autoflush=False` | Prevents automatic flushing before queries |

---

# 22. Key Takeaways

- A Session is the workspace used by SQLAlchemy to perform database operations.
- The Engine manages database connections, while the Session manages CRUD operations and transactions.
- `sessionmaker` creates Session objects.
- Every request should use its own Session.
- `add()` stages an object for insertion.
- `commit()` permanently saves changes.
- `rollback()` undoes uncommitted changes if an error occurs.
- `refresh()` reloads an object with the latest values from the database.
- `close()` releases resources and returns the connection to the pool.
- FastAPI uses Dependency Injection with `yield` to automatically create and close Sessions.
- `autocommit=False` and `autoflush=False` provide explicit control over database transactions and flushing.