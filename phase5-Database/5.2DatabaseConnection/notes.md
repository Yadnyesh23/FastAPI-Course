# Phase 5.2 – Database Connection

## Objectives

By the end of this phase, you should understand:

- Database URL
- PostgreSQL Database URL
- SQLite Database URL
- `create_engine()`
- Engine
- Connection Pool
- `connect_args`
- Lazy Connection
- Project Structure
- PostgreSQL vs SQLite

---

# 1. What is a Database URL?

A **Database URL** is a connection string that tells SQLAlchemy how to connect to a database.

Just like a website has a URL, a database also has its own URL.

It contains information such as:

- Database type (Dialect)
- Driver
- Username
- Password
- Host
- Port
- Database name

General Format:

```text
dialect+driver://username:password@host:port/database_name
```

Example:

```text
postgresql+psycopg://postgres:password@localhost:5432/student_db
```

---

# 2. PostgreSQL Database URL

Example:

```text
postgresql+psycopg://postgres:123456@localhost:5432/student_db
```

Explanation:

| Part | Meaning |
|------|---------|
| postgresql | Database Dialect |
| psycopg | PostgreSQL Driver |
| postgres | Username |
| 123456 | Password |
| localhost | Host |
| 5432 | Default PostgreSQL Port |
| student_db | Database Name |

---

# 3. SQLite Database URL

SQLite is different because it is a file-based database.

It does not require:

- Username
- Password
- Host
- Port

Example:

```python
DATABASE_URL = "sqlite:///students.db"
```

This creates a file named:

```text
students.db
```

inside the project.

---

# 4. What is `create_engine()`?

`create_engine()` is a SQLAlchemy function used to create an **Engine object**.

Example:

```python
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)
```

It does **not** immediately connect to the database.

Instead, it prepares the application to communicate with the database whenever required.

---

# 5. What is the Engine?

The **Engine** is the entry point for all communication between the FastAPI application and the database.

Responsibilities:

- Establish database connections
- Manage database connections
- Manage the connection pool
- Send SQL queries
- Receive results from the database

Architecture:

```text
FastAPI
    │
    ▼
Engine
    │
    ▼
Database
```

---

# 6. Lazy Connection

One common misconception is that `create_engine()` immediately opens a database connection.

This is **not true**.

SQLAlchemy uses **Lazy Connection**.

Flow:

```text
Application Starts
        │
        ▼
Engine Created
        │
        ▼
No Database Connection Yet
        │
        ▼
First SQL Query
        │
        ▼
Engine Opens Connection
```

The connection is created only when it is actually needed.

---

# 7. Connection Pool

Opening a new database connection is expensive.

Instead of creating a new connection for every request, SQLAlchemy maintains a **Connection Pool**.

Connection Pool:

```text
Connection Pool

Connection 1
Connection 2
Connection 3
Connection 4
Connection 5
```

Request Flow:

```text
Request
    │
    ▼
Borrow Connection
    │
    ▼
Execute Query
    │
    ▼
Return Connection to Pool
```

### Benefits

- Faster execution
- Better performance
- Less memory usage
- Efficient handling of multiple users
- Reuses existing connections

---

# 8. Why Should the Engine Be Created Only Once?

❌ Bad Practice

```python
@app.get("/")
def home():
    engine = create_engine(DATABASE_URL)
```

Problems:

- Creates a new Engine for every request
- Wastes memory
- Slower performance
- Creates unnecessary database connections

---

✅ Correct Practice

```python
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)
```

The Engine is created once when the application starts and reused throughout the project.

---

# 9. `connect_args`

SQLite is not fully thread-safe by default.

FastAPI can process requests using multiple threads.

Therefore, while using SQLite, we write:

```python
connect_args={"check_same_thread": False}
```

Example:

```python
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
```

This allows the SQLite connection to be used safely across different threads.

### Important

This argument is **only required for SQLite**.

PostgreSQL does **not** require `connect_args`.

---

# 10. PostgreSQL vs SQLite

| SQLite | PostgreSQL |
|----------|------------|
| File-based database | Server-based database |
| No installation required | Requires installation |
| Good for learning and small projects | Best for production |
| Limited concurrency | Excellent concurrency |
| Stores data in a single `.db` file | Stores data in a database server |

---

# 11. Professional Project Structure

A common structure for database-related files is:

```text
app/
│
├── database/
│   ├── connection.py
│   ├── session.py
│   └── base.py
│
├── models/
├── routers/
├── services/
└── main.py
```

---

# 12. Example – PostgreSQL Connection

```python
from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql+psycopg://postgres:123456@localhost:5432/fastapi_learning"
)

engine = create_engine(DATABASE_URL)
```

---

# 13. Database Connection Flow

```text
Application Starts
        │
        ▼
Read DATABASE_URL
        │
        ▼
Create Engine
        │
        ▼
Wait for First Query
        │
        ▼
Engine Opens Connection
        │
        ▼
Execute SQL Query
        │
        ▼
Return Connection to Pool
        │
        ▼
Response
```

---

# 14. Best Practices

- Create the Engine only once.
- Reuse the same Engine throughout the application.
- Store the database URL in environment variables (`.env`) for production.
- Use PostgreSQL for production applications.
- Use SQLite only for learning or small projects.
- Let SQLAlchemy manage the connection pool.
- Do not manually open a new Engine inside every route.

---

# 15. Interview Questions

1. What is a Database URL?
2. Explain the format of a PostgreSQL Database URL.
3. What does `create_engine()` do?
4. What is an Engine in SQLAlchemy?
5. What is Lazy Connection?
6. What is a Connection Pool?
7. Why is Connection Pooling important?
8. Why should the Engine be created only once?
9. What is `connect_args`?
10. Why is `connect_args={"check_same_thread": False}` used with SQLite?
11. Does PostgreSQL require `connect_args`?
12. Compare SQLite and PostgreSQL.

---

# 16. Quick Cheat Sheet

| Component | Purpose |
|-----------|---------|
| Database URL | Connection string used to connect to a database |
| `create_engine()` | Creates and returns an Engine object |
| Engine | Manages communication with the database |
| Lazy Connection | Opens a database connection only when the first query is executed |
| Connection Pool | Stores reusable database connections |
| `connect_args` | Additional connection settings (mainly for SQLite) |
| SQLite | File-based database, good for learning |
| PostgreSQL | Server-based database, best for production |

---

# 17. Key Takeaways

- A Database URL contains all the information required to connect to a database.
- PostgreSQL URLs include the dialect, driver, username, password, host, port, and database name.
- `create_engine()` creates an **Engine object**, which manages communication with the database.
- SQLAlchemy uses **Lazy Connection**, meaning the database connection is established only when the first query is executed.
- The Engine should be created only once and reused throughout the application.
- SQLAlchemy uses a **Connection Pool** to reuse database connections, improving performance and scalability.
- `connect_args={"check_same_thread": False}` is required only when using SQLite with FastAPI.
- PostgreSQL is the preferred database for production applications, while SQLite is ideal for learning and small projects.