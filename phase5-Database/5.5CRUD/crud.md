# Phase 5.5 – CRUD Operations with SQLAlchemy

## Objectives

By the end of this phase, you should understand:

- CRUD Operations
- Create (INSERT)
- Read (SELECT)
- Update (UPDATE)
- Delete (DELETE)
- `select()`
- `where()`
- `execute()`
- `scalar()`
- `scalars()`
- `all()`
- `add()`
- `commit()`
- `refresh()`
- `delete()`
- CRUD Flow
- Handling "Not Found" Cases

---

# 1. What is CRUD?

CRUD represents the four basic database operations performed on a database.

| Letter | Meaning | SQL Command |
|---------|----------|-------------|
| C | Create | INSERT |
| R | Read | SELECT |
| U | Update | UPDATE |
| D | Delete | DELETE |

Almost every backend application performs these operations.

---

# 2. Create (INSERT)

Creating data means inserting a new record into the database.

Example Request:

```json
{
    "name": "Yadnyesh",
    "age": 20,
    "email": "yadnyesh@gmail.com"
}
```

Flow:

```text
Client
    │
    ▼
Pydantic Validation
    │
    ▼
Create SQLAlchemy Object
    │
    ▼
db.add()
    │
    ▼
db.commit()
    │
    ▼
db.refresh()
    │
    ▼
Response
```

Example:

```python
student = Student(
    name="Yadnyesh",
    age=20,
    email="yadnyesh@gmail.com"
)

db.add(student)

db.commit()

db.refresh(student)
```

---

# 3. Why do we use `refresh()`?

After `commit()`, the database may automatically generate values such as:

- Primary Key (`id`)
- Timestamp
- Default values

The Python object does not automatically know these updated values.

`refresh()` reloads the object from the database.

Example:

Before:

```text
student.id = None
```

After:

```python
db.commit()
db.refresh(student)
```

Result:

```text
student.id = 1
```

---

# 4. Reading Data (`select()`)

`select()` is used to **build a SELECT query**.

Example:

```python
from sqlalchemy import select

query = select(Student)
```

Equivalent SQL:

```sql
SELECT * FROM students;
```

> **Note:** `select()` only builds the query. It does not execute it.

---

# 5. Executing Queries (`execute()`)

`execute()` sends the SQL query to the database and retrieves the result.

Example:

```python
result = db.execute(query)
```

Flow:

```text
Build Query
    │
    ▼
Execute Query
    │
    ▼
Database Returns Result
```

---

# 6. Getting Multiple Objects (`scalars()`)

`scalars()` extracts ORM model objects from the query result.

Example:

```python
students = db.execute(query).scalars()
```

Usually followed by:

```python
students = db.execute(query).scalars().all()
```

Returns:

```python
[
    Student(...),
    Student(...),
    Student(...)
]
```

Use `scalars()` when expecting **multiple rows**.

---

# 7. Getting a Single Object (`scalar()`)

Use `scalar()` when expecting only one result.

Example:

```python
student = db.execute(
    select(Student).where(Student.id == 1)
).scalar()
```

Returns:

```python
Student(...)
```

or

```python
None
```

Use `scalar()` when expecting **a single row**.

---

# 8. Getting All Results (`all()`)

`.all()` converts the query result into a Python list.

Example:

```python
students = db.execute(query).scalars().all()
```

Returns:

```python
[
    Student(...),
    Student(...),
    Student(...)
]
```

---

# 9. Filtering Data (`where()`)

`where()` is used to apply conditions to a query.

Example:

```python
query = select(Student).where(
    Student.id == 1
)
```

Equivalent SQL:

```sql
SELECT *
FROM students
WHERE id = 1;
```

You can filter by:

- id
- email
- name
- age
- etc.

---

# 10. Updating Data

Steps:

### Step 1

Retrieve the object.

```python
student = db.execute(
    select(Student).where(Student.id == 1)
).scalar()
```

### Step 2

Check if it exists.

```python
if student is None:
    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )
```

### Step 3

Modify the object.

```python
student.age = 21
```

### Step 4

Commit changes.

```python
db.commit()
```

### Step 5

Refresh the object.

```python
db.refresh(student)
```

Flow:

```text
Find Object
    │
    ▼
Check None
    │
    ▼
Modify
    │
    ▼
Commit
    │
    ▼
Refresh
```

---

# 11. Deleting Data

### Step 1

Retrieve the object.

```python
student = db.execute(
    select(Student).where(Student.id == 1)
).scalar()
```

### Step 2

Check if it exists.

```python
if student is None:
    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )
```

### Step 3

Delete the object.

```python
db.delete(student)
```

### Step 4

Commit changes.

```python
db.commit()
```

> **Note:** `refresh()` is **not used** after deleting because the object no longer exists in the database.

Flow:

```text
Find Object
    │
    ▼
Check None
    │
    ▼
Delete
    │
    ▼
Commit
```

---

# 12. Handling "Not Found" Cases

Sometimes the requested record does not exist.

Example:

```python
student = db.execute(
    select(Student).where(Student.id == 100)
).scalar()
```

Result:

```python
None
```

Always check before updating or deleting.

Example:

```python
if student is None:
    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )
```

Without this check, attempting to access attributes like:

```python
student.age = 21
```

would raise:

```text
AttributeError:
'NoneType' object has no attribute 'age'
```

---

# 13. Complete CRUD Flow

## Create

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
db.refresh()
      │
      ▼
Response
```

---

## Read

```text
Build Query (select)
      │
      ▼
execute()
      │
      ▼
scalar()/scalars()
      │
      ▼
Response
```

---

## Update

```text
Find Object
      │
      ▼
Check None
      │
      ▼
Modify Object
      │
      ▼
db.commit()
      │
      ▼
db.refresh()
      │
      ▼
Response
```

---

## Delete

```text
Find Object
      │
      ▼
Check None
      │
      ▼
db.delete()
      │
      ▼
db.commit()
      │
      ▼
Response
```

---

# 14. Complete Example

```python
student = Student(
    name="Yadnyesh",
    email="y@gmail.com",
    age=20
)

db.add(student)

db.commit()

db.refresh(student)

return student
```

---

# 15. Best Practices

- Always use `add()` before `commit()` when inserting new objects.
- Always call `commit()` after INSERT, UPDATE, and DELETE operations.
- Use `refresh()` after `commit()` if you need updated database-generated values.
- Use `select()` to build queries.
- Always execute queries using `execute()`.
- Use `scalar()` when expecting one result.
- Use `scalars().all()` when expecting multiple results.
- Always check if an object is `None` before updating or deleting it.
- Return a `404 Not Found` error when a record does not exist.
- Do **not** call `refresh()` after `delete()`.

---

# 16. Interview Questions

1. What does CRUD stand for?
2. What is the purpose of `add()`?
3. Why do we call `commit()`?
4. Why do we use `refresh()`?
5. What does `select()` do?
6. Is `select()` enough to fetch data?
7. What does `execute()` do?
8. Difference between `scalar()` and `scalars()`?
9. What does `.all()` return?
10. What is the purpose of `where()`?
11. How do you update a record using SQLAlchemy?
12. How do you delete a record?
13. Why should we check if an object is `None`?
14. Why don't we call `commit()` after `SELECT`?
15. Why don't we call `refresh()` after `delete()`?

---

# 17. Quick Cheat Sheet

| Method | Purpose |
|----------|---------|
| `add()` | Add an object to the Session |
| `commit()` | Permanently save changes to the database |
| `refresh()` | Reload the object with the latest database values |
| `select()` | Build a SELECT query |
| `execute()` | Execute the SQL query |
| `scalar()` | Return a single ORM object |
| `scalars()` | Extract multiple ORM objects |
| `.all()` | Return all results as a list |
| `where()` | Add filtering conditions |
| `delete()` | Mark an object for deletion |

---

# 18. Key Takeaways

- CRUD consists of Create, Read, Update, and Delete operations.
- `add()` stages a new object for insertion.
- `commit()` permanently saves changes to the database.
- `refresh()` updates the Python object with the latest database values.
- `select()` builds a query, while `execute()` runs it.
- Use `scalar()` for a single result and `scalars().all()` for multiple results.
- `where()` filters records based on conditions.
- Always check if an object exists before updating or deleting it.
- Return a `404 Not Found` error when a record does not exist.
- `refresh()` should not be called after deleting an object.