# Phase 4.2 – Professional FastAPI Project Structure

## Objectives

By the end of this phase, you should understand:

- Why large FastAPI projects are divided into multiple folders
- Purpose of each folder
- `routers/`
- `schemas/`
- `models/`
- `services/`
- `database/`
- `dependencies/`
- `core/`
- `utils/`
- `tests/`
- Complete request flow in a professional FastAPI project

---

# 1. Why Do We Need a Project Structure?

As a project grows, keeping everything inside routers or `main.py` becomes difficult.

Example:

```python
@router.post("/students")
def create_student(student: Student):
    # Validate input
    # Connect to database
    # Check permissions
    # Insert data
    # Send email
    # Log activity
    # Return response
```

This route may eventually become hundreds of lines long.

A better approach is to separate responsibilities into dedicated folders.

### Benefits

- Better organization
- Easier maintenance
- Easier debugging
- Better scalability
- Easier collaboration
- Cleaner code

---

# 2. Typical Professional Project Structure

```text
app/
│
├── main.py
│
├── routers/
├── schemas/
├── models/
├── services/
├── database/
├── dependencies/
├── core/
├── utils/
└── tests/
```

Each folder has a single responsibility.

---

# 3. `routers/`

Contains API endpoints.

Example:

```text
routers/
├── students.py
├── teachers.py
├── auth.py
└── notes.py
```

Example:

```python
@router.post("/students")
def create_student(student: StudentCreate):
    return student_service.create_student(student)
```

### Responsibilities

- Receive HTTP requests
- Call dependencies
- Call service layer
- Return responses

### Should NOT Contain

- Business logic
- Database logic
- Complex processing

---

# 4. `schemas/`

Contains **Pydantic models**.

Example:

```python
from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    age: int
```

Example Response Model:

```python
class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
```

### Responsibilities

- Request Body Models
- Response Models
- Validation Rules
- Data Serialization

Think of schemas as:

> **The data format exchanged between client and server.**

---

# 5. `models/`

Contains **Database Models** (usually SQLAlchemy models).

Example:

```python
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
```

### Responsibilities

- Database table definitions
- Relationships
- ORM mapping

### Important

Pydantic Schemas and Database Models are **different**.

| Schema | Database Model |
|----------|----------------|
| API Validation | Database Table |
| Request & Response | Database Representation |

---

# 6. `services/`

Contains the application's **business logic**.

Instead of:

```python
@router.post("/students")
def create_student(student):
    # 100 lines of logic
```

Use:

```python
@router.post("/students")
def create_student(student):
    return student_service.create_student(student)
```

Inside:

```python
services/student_service.py
```

```python
def create_student(student):
    # Business logic
    # Validation
    # Calculations
    # Database operations
```

### Responsibilities

- Business rules
- Calculations
- Processing
- Calling multiple components
- Coordinating application logic

---

# 7. `database/`

Contains everything related to the database.

Example:

```text
database/
├── connection.py
├── session.py
└── base.py
```

### Responsibilities

- Database URL
- Database Engine
- Sessions
- Base Class
- Database Configuration

Example:

```python
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
```

---

# 8. `dependencies/`

Contains reusable dependencies used with `Depends()`.

Examples:

```python
def get_db():
    ...

def get_current_user():
    ...

def verify_admin():
    ...
```

### Responsibilities

- Database sessions
- Authentication
- Authorization
- Shared reusable dependencies

### Benefits

- Code reuse
- Cleaner routers
- Easier testing
- Centralized dependency management

---

# 9. `core/`

Contains application configuration and security.

Example:

```text
core/
├── config.py
├── security.py
└── settings.py
```

### Responsibilities

- Environment variables
- Application settings
- JWT configuration
- Password hashing
- Security utilities

---

# 10. `utils/`

Contains generic helper functions.

Examples:

```python
def send_email():
    ...

def format_date():
    ...

def generate_uuid():
    ...
```

### Responsibilities

- Utility functions
- Formatting helpers
- Reusable generic functions

### Note

Authentication-specific logic such as JWT verification usually belongs in `core/` or `dependencies/`, not `utils/`.

---

# 11. `tests/`

Contains automated tests.

Example:

```text
tests/
├── test_students.py
├── test_auth.py
└── test_notes.py
```

Usually written using:

- pytest
- FastAPI TestClient

Purpose:

- Verify correctness
- Prevent bugs
- Ensure future changes don't break existing functionality

---

# 12. Complete Request Flow

A professional FastAPI application processes a request like this:

```text
Client
   │
   ▼
Router
   │
   ▼
Schema Validation
   │
   ▼
Dependencies
(Authentication, Database Session, etc.)
   │
   ▼
Service Layer
   │
   ▼
Database Model
   │
   ▼
Database
   │
   ▼
Response Model
   │
   ▼
Client
```

---

# 13. Real Project Example

```text
app/
│
├── main.py
│
├── routers/
│   ├── auth.py
│   ├── users.py
│   ├── notes.py
│   ├── lectures.py
│   └── quizzes.py
│
├── schemas/
│   ├── user.py
│   ├── note.py
│   └── lecture.py
│
├── models/
│   ├── user.py
│   ├── note.py
│   └── lecture.py
│
├── services/
│   ├── auth_service.py
│   ├── note_service.py
│   └── ai_service.py
│
├── database/
│   ├── base.py
│   ├── connection.py
│   └── session.py
│
├── dependencies/
│   ├── auth.py
│   └── database.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   └── settings.py
│
├── utils/
│   ├── email.py
│   └── helpers.py
│
└── tests/
```

---

# 14. Best Practices

- Keep routers lightweight.
- Store all business logic inside services.
- Use schemas for validation.
- Keep database configuration inside the database folder.
- Store reusable dependencies separately.
- Keep configuration inside `core/`.
- Use `utils/` only for generic helper functions.
- Follow the Single Responsibility Principle (SRP).
- Organize code feature-wise as the project grows.

---

# 15. Interview Questions

1. Why shouldn't business logic be placed inside routers?
2. What is the purpose of the `schemas/` folder?
3. What is stored inside the `models/` folder?
4. Are Pydantic schemas and database models the same?
5. What belongs inside the `services/` folder?
6. What belongs inside the `database/` folder?
7. What kind of functions belong in `utils/`?
8. Why do we keep dependencies in a separate folder?
9. Where is JWT configuration usually stored?
10. Explain the request flow in a professional FastAPI application.

---

# 16. Quick Cheat Sheet

| Folder | Purpose |
|----------|---------|
| `routers/` | API endpoints |
| `schemas/` | Pydantic request/response models |
| `models/` | Database models (ORM) |
| `services/` | Business logic |
| `database/` | Database connection and sessions |
| `dependencies/` | Reusable dependencies (`Depends`) |
| `core/` | Configuration and security |
| `utils/` | Generic helper functions |
| `tests/` | Automated tests |

---

# 17. Key Takeaways

- Professional FastAPI projects follow a modular architecture.
- Each folder has a single responsibility.
- Routers should only handle requests and responses.
- Schemas validate API data.
- Models represent database tables.
- Services contain business logic.
- Dependencies provide reusable logic through `Depends()`.
- Core stores configuration and security settings.
- Utilities contain generic helper functions.
- A well-structured project is easier to maintain, test, and scale.