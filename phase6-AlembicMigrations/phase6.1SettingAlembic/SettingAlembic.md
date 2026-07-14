# Phase 6.1 – Setting Up Alembic

## Objectives

By the end of this phase, you should understand:

- Installing Alembic
- Initializing Alembic
- Alembic Folder Structure
- `alembic.ini`
- `env.py`
- `target_metadata`
- Registering SQLAlchemy Models
- Connecting Alembic with SQLAlchemy
- Migration Workflow

---

# 1. Installing Alembic

Alembic is SQLAlchemy's official database migration tool.

Install it using pip:

```bash
pip install alembic
```

Or, if using **uv**:

```bash
uv add alembic
```

### Why Install Alembic Inside the Project?

Installing Alembic as a project dependency ensures:

- Every project has its own Alembic version.
- Dependency conflicts between projects are avoided.
- Alembic tracks migrations for the current project only.
- The project remains reproducible for other developers.

---

# 2. Initializing Alembic

Initialize Alembic inside the project:

```bash
alembic init alembic
```

This command creates the complete Alembic setup.

---

# 3. Alembic Folder Structure

After initialization:

```text
project/

│

├── alembic/

│   ├── versions/

│   ├── env.py

│   ├── script.py.mako

│

├── alembic.ini

├── app/

├── database/

├── models/

└── main.py
```

---

## Folder Explanation

### `alembic/`

Contains all migration-related files.

---

### `versions/`

Stores every migration file.

Example:

```text
001_create_students.py

002_add_email.py

003_create_notes.py
```

Each file represents one database schema change.

---

### `env.py`

The most important Alembic configuration file.

It tells Alembic:

- How to connect to the database.
- Which SQLAlchemy models exist.
- Which metadata should be compared.
- How migrations should run.

---

### `script.py.mako`

A template used by Alembic whenever a new migration file is generated.

Normally, developers do not modify this file.

---

### `alembic.ini`

Alembic's main configuration file.

It contains:

- Database URL
- Migration script location
- Logging configuration
- Alembic settings

Example:

```ini
sqlalchemy.url = postgresql+psycopg://postgres:password@localhost:5432/student_db
```

---

# 4. Why Does Alembic Need Our Models?

Alembic generates migrations by comparing:

```text
SQLAlchemy Models

↓

Current Database Schema
```

If Alembic does not know about the models, it cannot detect any schema changes.

---

# 5. `target_metadata`

Inside `env.py`:

Initially:

```python
target_metadata = None
```

This should be changed to:

```python
from database.base import Base

target_metadata = Base.metadata
```

---

## What is `Base.metadata`?

Every SQLAlchemy model inherits from the same Base class.

Example:

```python
class Student(Base):
```

```python
class Note(Base):
```

Whenever a model inherits from `Base`, SQLAlchemy registers it inside:

```python
Base.metadata
```

`Base.metadata` contains information about:

- Tables
- Columns
- Constraints
- Relationships
- Indexes

Alembic compares this metadata with the current database schema to determine what has changed.

---

# 6. Why Can't `target_metadata` Be `None`?

If:

```python
target_metadata = None
```

Alembic has no information about the application's models.

As a result:

- No tables are detected.
- No schema changes are found.
- Migration generation fails or produces empty migrations.

Therefore:

```python
target_metadata = Base.metadata
```

is required.

---

# 7. Importing Models

Suppose the project contains:

```text
models/

student.py

note.py
```

Even after setting:

```python
target_metadata = Base.metadata
```

Alembic still needs the model files to be imported.

Example:

```python
from models.student import Student
from models.note import Note
```

---

## Why Import Models?

Importing a model executes its class definition.

Example:

```python
class Student(Base):
```

During execution, SQLAlchemy registers the model inside:

```python
Base.metadata
```

Without importing the models:

```python
Base.metadata.tables
```

would be empty.

Alembic would think the project contains no tables.

---

# 8. Connecting Alembic to SQLAlchemy

The essential setup inside `env.py` is:

```python
from database.base import Base

from models.student import Student
from models.note import Note

target_metadata = Base.metadata
```

Now Alembic knows:

- All models
- Their tables
- Their columns
- Their relationships

and can generate migrations correctly.

---

# 9. Development Workflow

Whenever a model changes:

```text
Modify SQLAlchemy Model

↓

Generate Alembic Migration

↓

Review Migration

↓

Apply Migration

↓

Database Updated
```

This keeps the Python models and database schema synchronized.

---

# 10. Best Practices

- Initialize Alembic once per project.
- Keep migration files inside the `versions/` directory.
- Always set `target_metadata = Base.metadata`.
- Import all SQLAlchemy models in `env.py`.
- Keep `alembic.ini` under version control.
- Review generated migration files before applying them.
- Never manually edit production databases when migrations can be used.

---

# 11. Interview Questions

1. What is Alembic?
2. Why do we initialize Alembic?
3. Which command initializes Alembic?
4. What is the purpose of `alembic.ini`?
5. What is the purpose of `env.py`?
6. What is `target_metadata`?
7. Why do we use `Base.metadata`?
8. Why can't `target_metadata` remain `None`?
9. Why are SQLAlchemy models imported in `env.py`?
10. Where are migration files stored?
11. What is the purpose of the `versions/` folder?
12. What is the typical Alembic workflow?

---

# 12. Quick Cheat Sheet

| Feature | Purpose |
|----------|---------|
| `pip install alembic` | Install Alembic |
| `uv add alembic` | Install Alembic using uv |
| `alembic init alembic` | Initialize Alembic |
| `alembic.ini` | Alembic configuration file |
| `env.py` | Connects Alembic with SQLAlchemy |
| `versions/` | Stores migration files |
| `Base.metadata` | Contains metadata of all registered models |
| `target_metadata` | Metadata Alembic compares with the database |
| Import Models | Registers models with `Base.metadata` |

---

# 13. Key Takeaways

- Alembic is SQLAlchemy's official migration tool.
- `alembic init alembic` creates the migration environment.
- `alembic.ini` stores Alembic configuration, including the database URL.
- `env.py` connects Alembic to SQLAlchemy models.
- `Base.metadata` contains metadata for all registered database tables.
- `target_metadata` must be set to `Base.metadata` so Alembic can detect schema changes.
- SQLAlchemy models must be imported in `env.py` to register them with `Base.metadata`.
- Migration files are stored in the `alembic/versions/` directory.
- The standard workflow is: **Modify Model → Generate Migration → Review → Apply Migration**.