# Phase 4.1 – Python Packages & `__init__.py`

## Objectives

By the end of this phase, you should understand:

- What is a Python module?
- What is a Python package?
- Why packages are used
- What is `__init__.py`?
- Absolute vs Relative Imports
- How Python finds modules
- Common Import Errors
- Best Practices

---

# 1. What is a Python Module?

A **module** is simply a Python file (`.py`) containing Python code such as variables, functions, classes, etc.

### Example

```text
students.py
teachers.py
database.py
```

Each of these files is a Python module.

Example:

```python
# students.py

def get_students():
    return ["Rahul", "Yadnyesh"]
```

Importing a function from a module:

```python
from students import get_students
```

---

# 2. What is a Python Package?

A **package** is a directory (folder) that contains one or more Python modules.

Example:

```text
project/
│
└── routers/
    ├── students.py
    ├── teachers.py
    └── auth.py
```

Here:

- `routers` → Package
- `students.py` → Module
- `teachers.py` → Module
- `auth.py` → Module

---

# 3. Why Do We Use Packages?

Packages help organize large projects.

Instead of placing every Python file in one directory:

```text
project/
│
├── student.py
├── teacher.py
├── notes.py
├── auth.py
├── payment.py
├── email.py
├── database.py
├── ai.py
└── ...
```

We organize them:

```text
project/
│
├── routers/
├── models/
├── schemas/
├── services/
├── database/
└── utils/
```

### Benefits

- Better organization
- Easier maintenance
- Better readability
- Easier collaboration
- Better scalability
- Creates namespaces (`routers.students`, `models.student`, etc.)

---

# 4. What is `__init__.py`?

`__init__.py` is a special Python file that marks a directory as a package (traditionally).

Example:

```text
routers/
│
├── __init__.py
├── students.py
└── teachers.py
```

Most of the time, it is simply empty.

```python
# __init__.py
```

---

## Modern Python

Since Python 3.3, `__init__.py` is optional because Python supports **namespace packages**.

However, most professional Python and FastAPI projects still include it because:

- It clearly indicates that the folder is a package.
- It improves compatibility with tools and older Python code.
- It can contain initialization code.
- It can re-export commonly used objects.

---

# 5. What Can `__init__.py` Contain?

It can be empty:

```python
# __init__.py
```

Or it can export commonly used objects.

Example:

```python
from .students import router as student_router
from .teachers import router as teacher_router
```

Then elsewhere:

```python
from routers import student_router, teacher_router
```

---

# 6. Absolute Imports

Absolute imports start from the project/package root.

Example:

```python
from routers.students import router
```

Python interprets this as:

```text
routers
    ↓
students
    ↓
router
```

### Advantages

- Easy to understand
- Explicit
- Preferred in large FastAPI projects

---

# 7. Relative Imports

Relative imports use dots (`.`) to refer to packages relative to the current module.

### Current Package

```python
from .students import router
```

`.` means:

> Look inside the current package.

### Parent Package

```python
from ..database import SessionLocal
```

`..` means:

> Go one package up.

Example:

```text
app/
│
├── database.py
│
└── routers/
    ├── students.py
```

Inside `students.py`:

```python
from ..database import SessionLocal
```

---

# 8. Absolute vs Relative Imports

| Absolute Import | Relative Import |
|-----------------|-----------------|
| `from routers.students import router` | `from .students import router` |
| Starts from the project/package root | Starts from the current package |
| Easier to understand | Shorter inside packages |
| Preferred in FastAPI projects | Useful within the same package |

---

# 9. How Python Finds Modules

When Python sees:

```python
from routers.students import router
```

It searches for:

```text
project/
│
└── routers/
    └── students.py
```

If the module exists, Python imports it.

Otherwise, it raises an error.

---

# 10. Common Import Errors

## ModuleNotFoundError

Occurs when Python cannot find the module.

Example:

```python
from routers.student import router
```

But the file is:

```text
students.py
```

Error:

```text
ModuleNotFoundError
```

---

## ImportError

Occurs when the module exists but the object being imported does not.

Example:

```python
from routers.students import student_router
```

But inside:

```python
router = APIRouter()
```

There is no object named `student_router`.

Error:

```text
ImportError
```

---

## Circular Imports

Occurs when two modules import each other.

Example:

```text
students.py
    ↓
imports teachers.py

teachers.py
    ↓
imports students.py
```

This creates a circular dependency and causes import problems.

---

# 11. Typical FastAPI Project Structure

```text
app/
│
├── main.py
│
├── routers/
│   ├── __init__.py
│   ├── students.py
│   ├── teachers.py
│   └── auth.py
│
├── models/
├── schemas/
├── services/
├── database/
├── dependencies/
└── core/
```

---

# 12. Best Practices

- Keep related modules inside the same package.
- Use meaningful package names (`routers`, `models`, `schemas`, etc.).
- Prefer **absolute imports** in FastAPI projects.
- Avoid circular imports.
- Keep `__init__.py` even though it is optional.
- Organize code logically to improve maintainability.

---

# 13. Interview Questions

1. What is a Python module?
2. What is a Python package?
3. Why do we use packages?
4. What is the purpose of `__init__.py`?
5. Is `__init__.py` mandatory in modern Python?
6. What is an absolute import?
7. What is a relative import?
8. What does `.` mean in a relative import?
9. What does `..` mean in a relative import?
10. What is the difference between `ModuleNotFoundError` and `ImportError`?
11. What are circular imports?
12. Which import style is preferred in FastAPI projects?

---

# 14. Quick Cheat Sheet

| Concept | Meaning |
|----------|---------|
| Module | A Python file (`.py`) |
| Package | A folder containing Python modules |
| `__init__.py` | Marks a directory as a package (traditionally) and can initialize or re-export package contents |
| Absolute Import | `from routers.students import router` |
| Relative Import | `from .students import router` |
| `.` | Current package |
| `..` | Parent package |
| `ModuleNotFoundError` | Module cannot be found |
| `ImportError` | Imported object does not exist |

---

# 15. Key Takeaways

- A **module** is a Python file.
- A **package** is a folder containing Python modules.
- Packages organize large projects and create namespaces.
- `__init__.py` traditionally marks a directory as a package and is still commonly used in professional projects.
- Absolute imports are generally preferred in FastAPI applications.
- Relative imports are useful within the same package.
- Python raises `ModuleNotFoundError` when it cannot locate a module.
- Python raises `ImportError` when the requested object does not exist in the module.
- Good package organization makes projects easier to maintain, scale, and collaborate on.