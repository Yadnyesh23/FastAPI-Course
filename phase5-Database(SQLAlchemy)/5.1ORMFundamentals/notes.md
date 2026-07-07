# Phase 5.1 – SQLAlchemy ORM Fundamentals

## Objectives

By the end of this phase, you should understand:

- What is a Database?
- What is SQL?
- What is an ORM?
- Why ORMs exist
- What is SQLAlchemy?
- Engine
- Session
- Model
- SQLAlchemy Architecture
- SQLAlchemy Workflow
- SQLAlchemy vs Raw SQL

---

# 1. What is a Database?

A **Database** is a software system used to store and organize data permanently.

Unlike Python variables or lists, data stored in a database remains even after the application or server is stopped.

Example:

```python
students = [
    {"id": 1, "name": "Yadnyesh"}
]
```

The above data disappears when the program stops.

Database:

```text
students

id | name
------------
1  | Yadnyesh
2  | Rahul
```

The data remains stored permanently.

### Benefits

- Permanent storage
- Organized data
- Fast searching
- Supports multiple users
- Easy updates and deletion

---

# 2. What is SQL?

SQL stands for **Structured Query Language**.

It is the standard language used to communicate with relational databases.

Examples:

Create data:

```sql
INSERT INTO students(name)
VALUES ('Yadnyesh');
```

Read data:

```sql
SELECT * FROM students;
```

Update data:

```sql
UPDATE students
SET name='Rahul'
WHERE id=1;
```

Delete data:

```sql
DELETE FROM students
WHERE id=1;
```

---

# 3. Problems with Raw SQL

Writing SQL manually for every database operation can become difficult in large projects.

Example:

```python
cursor.execute("""
SELECT *
FROM students
WHERE age > 18
ORDER BY name
""")
```

### Problems

- Lots of SQL strings
- Harder to maintain
- More chances of syntax errors
- Less Pythonic
- Database-specific syntax

---

# 4. What is an ORM?

ORM stands for **Object Relational Mapper**.

An ORM acts as a bridge between Python objects and relational databases.

Instead of writing SQL queries manually, you work with Python classes and objects.

Example:

Instead of:

```sql
SELECT * FROM students;
```

You can write:

```python
students = session.query(Student).all()
```

Or in SQLAlchemy 2.0 style:

```python
students = session.execute(
    select(Student)
).scalars().all()
```

SQLAlchemy automatically converts the Python code into SQL.

---

# 5. Why Do We Use an ORM?

Without ORM:

```text
Python
   │
   ▼
Raw SQL
   │
   ▼
Database
```

With ORM:

```text
Python Objects
      │
      ▼
SQLAlchemy ORM
      │
      ▼
Generated SQL
      │
      ▼
Database
```

### Benefits

- Write Python instead of SQL
- Cleaner code
- Better readability
- Easier maintenance
- Better integration with FastAPI
- Reduces manual SQL writing

---

# 6. What is SQLAlchemy?

SQLAlchemy is the most popular ORM library for Python.

It provides:

- ORM
- SQL Expression Language
- Connection management
- Transactions
- Relationships
- Database abstraction

FastAPI commonly uses SQLAlchemy to interact with relational databases.

---

# 7. Core Components of SQLAlchemy

## Engine

The **Engine** establishes and manages the connection between the FastAPI application and the database.

Example:

```text
FastAPI
   │
   ▼
Engine
   │
   ▼
Database
```

The engine is the entry point for all database communication.

---

## Session

A **Session** is your conversation with the database.

It is responsible for:

- Creating data
- Reading data
- Updating data
- Deleting data
- Committing transactions

Example:

```python
session.add(student)
session.commit()
```

---

## Model

A **Model** is a Python class that represents a database table.

Example:

```python
class Student(Base):
    ...
```

One model generally represents one table.

Example:

```text
Student Model
        │
        ▼
students Table
```

---

# 8. SQLAlchemy Architecture

```text
FastAPI
    │
    ▼
Route
    │
    ▼
Service
    │
    ▼
Session
    │
    ▼
Engine
    │
    ▼
Database
```

The **Model** acts as the Python representation of the database table and is used by the Session to perform operations.

---

# 9. Typical SQLAlchemy Workflow

Suppose a user creates a student.

```text
Client
   │
   ▼
POST /students
   │
   ▼
FastAPI Route
   │
   ▼
Schema Validation
   │
   ▼
Service
   │
   ▼
Create Student Model Object
   │
   ▼
Session.add(student)
   │
   ▼
Session.commit()
   │
   ▼
Engine
   │
   ▼
Database
   │
   ▼
Response
```

---

# 10. SQLAlchemy vs Raw SQL

| Raw SQL | SQLAlchemy ORM |
|----------|----------------|
| Write SQL manually | Write Python code |
| More verbose | Cleaner and more readable |
| More chances of syntax mistakes | Pythonic and easier to maintain |
| Database-specific queries | Abstracts many database operations |
| Harder to maintain | Easier to scale and maintain |

---

# 11. Real FastAPI Example

```python
student = Student(
    name="Yadnyesh",
    age=20
)

session.add(student)
session.commit()
```

Equivalent SQL:

```sql
INSERT INTO students(name, age)
VALUES ('Yadnyesh', 20);
```

SQLAlchemy automatically generates the SQL query.

---

# 12. Best Practices

- Use an ORM for most application logic.
- Learn SQL even when using SQLAlchemy.
- Keep database logic separate from routers.
- Use models to represent database tables.
- Use sessions to interact with the database.
- Close database sessions properly (you'll learn this in the next phases).

---

# 13. Interview Questions

1. What is a database?
2. What does SQL stand for?
3. What is an ORM?
4. Why do ORMs exist?
5. What is SQLAlchemy?
6. What is the purpose of the Engine?
7. What is the purpose of the Session?
8. What is a Model in SQLAlchemy?
9. Explain the SQLAlchemy architecture.
10. What are the advantages of SQLAlchemy over raw SQL?

---

# 14. Quick Cheat Sheet

| Component | Purpose |
|-----------|---------|
| Database | Stores data permanently |
| SQL | Language used to communicate with relational databases |
| ORM | Maps Python objects to database tables |
| SQLAlchemy | Python ORM library |
| Engine | Connects the application to the database |
| Session | Performs CRUD operations and manages transactions |
| Model | Python class representing a database table |

---

# 15. Key Takeaways

- A database stores data permanently.
- SQL is the language used to communicate with relational databases.
- An ORM lets you work with databases using Python objects instead of writing raw SQL for every operation.
- SQLAlchemy is the most widely used ORM in Python.
- The **Engine** manages the connection between the application and the database.
- The **Session** is used to create, read, update, and delete data.
- A **Model** is a Python class that represents a database table.
- SQLAlchemy converts Python operations into SQL queries automatically.
- Using SQLAlchemy makes FastAPI applications cleaner, easier to maintain, and more scalable.