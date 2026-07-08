# Phase 5.3 – SQLAlchemy Models

## Objectives

By the end of this phase, you should understand:

- What is a SQLAlchemy Model?
- Declarative Mapping
- DeclarativeBase
- Base Class
- `__tablename__`
- `mapped_column()`
- Common SQLAlchemy Data Types
- Primary Key
- Autoincrement
- Nullable
- Unique
- Default
- Index
- SQLAlchemy Models vs Pydantic Models

---

# 1. What is a SQLAlchemy Model?

A **SQLAlchemy Model** is a Python class that represents a table in the database.

Each model generally maps to one database table.

Example:

Database Table:

```text
students

id | name | age
---------------
1  | Yadnyesh | 20
2  | Rahul    | 19
```

SQLAlchemy Model:

```python
class Student(Base):
    ...
```

One model = One database table.

---

# 2. What is Declarative Mapping?

Declarative Mapping is the process of creating database tables by writing Python classes instead of SQL statements.

Instead of writing:

```sql
CREATE TABLE students (
    id INTEGER,
    name VARCHAR(100)
);
```

We write:

```python
class Student(Base):
    ...
```

SQLAlchemy automatically maps the Python class to the database table.

Flow:

```text
Python Class
      │
      ▼
SQLAlchemy ORM
      │
      ▼
Database Table
```

---

# 3. What is `DeclarativeBase`?

`DeclarativeBase` is the base class provided by SQLAlchemy.

Every SQLAlchemy model must inherit from it.

Example:

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

Purpose:

- Identifies database models
- Stores metadata
- Enables ORM mapping

---

# 4. Why Do We Create Base Only Once?

The Base class is created once and shared by all models.

Example:

```python
class Student(Base):
    ...

class Teacher(Base):
    ...

class User(Base):
    ...
```

Benefits:

- Shared metadata
- Common configuration
- Easier maintenance

---

# 5. What is `__tablename__`?

`__tablename__` specifies the name of the database table.

Example:

```python
class Student(Base):
    __tablename__ = "students"
```

Result:

```text
students
```

### Best Practices

- Use lowercase
- Use plural names
- Use snake_case if needed

Examples:

```python
__tablename__ = "students"
__tablename__ = "teachers"
__tablename__ = "blog_posts"
```

---

# 6. What is `mapped_column()`?

`mapped_column()` is used to define columns of a database table.

Syntax:

```python
mapped_column(datatype, options...)
```

Example:

```python
name = mapped_column(String)
```

You can also define:

- Data type
- Constraints
- Default values
- Indexes

---

# 7. Common SQLAlchemy Data Types

| Data Type | Description |
|------------|-------------|
| Integer | Integer values |
| String | Text with limited length |
| Text | Large text |
| Boolean | True / False |
| Float | Decimal numbers |
| Date | Date |
| DateTime | Date and Time |
| Time | Time only |

Example:

```python
age = mapped_column(Integer)

name = mapped_column(String)

description = mapped_column(Text)

price = mapped_column(Float)

is_active = mapped_column(Boolean)
```

---

# 8. Primary Key

A Primary Key uniquely identifies every row in a table.

Example:

```python
id = mapped_column(
    Integer,
    primary_key=True
)
```

Properties:

- Unique
- Cannot be NULL
- One primary key per table (typically)

Example:

```text
id | name
----------
1  | Yadnyesh
2  | Rahul
```

---

# 9. Autoincrement

Autoincrement automatically increases the value of the primary key.

Example:

```python
id = mapped_column(
    Integer,
    primary_key=True,
    autoincrement=True
)
```

Rows:

```text
1
2
3
4
5
```

Usually, SQLAlchemy automatically enables autoincrement for integer primary keys.

---

# 10. Nullable

Determines whether a column can store `NULL`.

Nullable:

```python
phone = mapped_column(
    String,
    nullable=True
)
```

Possible value:

```text
NULL
```

Required field:

```python
name = mapped_column(
    String,
    nullable=False
)
```

The value must be provided.

---

# 11. Unique

Ensures duplicate values are not allowed.

Example:

```python
email = mapped_column(
    String,
    unique=True
)
```

Allowed:

```text
abc@gmail.com

xyz@gmail.com
```

Not Allowed:

```text
abc@gmail.com

abc@gmail.com
```

Common Uses:

- Email
- Username
- Aadhaar Number
- Employee ID

---

# 12. Default

Assigns a value when the user does not provide one.

Example:

```python
is_active = mapped_column(
    Boolean,
    default=True
)
```

If omitted:

```text
True
```

is automatically stored.

---

# 13. Index

An Index improves the speed of searching and filtering data.

Example:

```python
email = mapped_column(
    String,
    index=True
)
```

Without Index:

```text
Database

↓

Check every row

↓

Find record
```

With Index:

```text
Database

↓

Use Index

↓

Find record quickly
```

### Advantages

- Faster searching
- Faster filtering
- Faster sorting (in many cases)

### Disadvantages

- Uses extra storage
- Slightly slower INSERT and UPDATE operations because the index must also be maintained

---

# 14. Complete Example

```python
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = mapped_column(
        String,
        nullable=False
    )

    email = mapped_column(
        String,
        unique=True,
        index=True
    )

    age = mapped_column(Integer)

    is_active = mapped_column(
        Boolean,
        default=True
    )
```

---

# 15. SQLAlchemy Models vs Pydantic Models

| SQLAlchemy Model | Pydantic Model |
|------------------|----------------|
| Represents a database table | Represents request and response data |
| Used with SQLAlchemy ORM | Used with FastAPI validation |
| Stored in `models/` | Stored in `schemas/` |
| Uses `mapped_column()` | Uses Python type hints (`str`, `int`) |
| Defines database structure | Validates API data |

Flow:

```text
Client
    │
    ▼
Pydantic Model
    │
    ▼
Validation
    │
    ▼
SQLAlchemy Model
    │
    ▼
Database
```

---

# 16. Project Structure

```text
app/
│
├── database/
│   └── base.py
│
├── models/
│   ├── student.py
│   ├── teacher.py
│   └── user.py
│
├── schemas/
├── routers/
├── services/
└── main.py
```

---

# 17. Best Practices

- Create the `Base` class only once.
- Keep one model per file.
- Use singular class names (`Student`, `Teacher`).
- Use plural, lowercase table names (`students`, `teachers`).
- Use `nullable=False` for required fields.
- Use `unique=True` only where uniqueness is required.
- Use `index=True` for columns frequently searched or filtered.
- Follow Python naming conventions (`snake_case`) for attribute names.

---

# 18. Interview Questions

1. What is a SQLAlchemy Model?
2. What is Declarative Mapping?
3. What is `DeclarativeBase`?
4. Why is the Base class created only once?
5. What is the purpose of `__tablename__`?
6. What is `mapped_column()`?
7. Name some common SQLAlchemy data types.
8. What is a Primary Key?
9. What is `autoincrement=True`?
10. Difference between `nullable=True` and `nullable=False`.
11. Why do we use `unique=True`?
12. What is the purpose of `default=`?
13. Why do we use `index=True`?
14. Difference between SQLAlchemy Models and Pydantic Models.

---

# 19. Quick Cheat Sheet

| Feature | Purpose |
|----------|---------|
| `DeclarativeBase` | Base class for all models |
| `Base` | Parent class inherited by every model |
| `__tablename__` | Database table name |
| `mapped_column()` | Defines database columns |
| `primary_key=True` | Unique identifier |
| `autoincrement=True` | Automatically increments IDs |
| `nullable=False` | Field is required |
| `unique=True` | Prevents duplicate values |
| `default=` | Sets a default value |
| `index=True` | Creates a database index for faster searches |

---

# 20. Key Takeaways

- A SQLAlchemy Model is a Python class that represents a database table.
- Declarative Mapping allows us to create database tables using Python classes instead of SQL statements.
- Every model inherits from a common `Base` class created using `DeclarativeBase`.
- `__tablename__` specifies the database table name.
- `mapped_column()` is used to define columns, data types, and constraints.
- Common constraints include `primary_key`, `autoincrement`, `nullable`, `unique`, `default`, and `index`.
- SQLAlchemy Models define how data is stored in the database, while Pydantic Models validate request and response data.
- In production FastAPI applications, SQLAlchemy Models and Pydantic Models are typically used together.