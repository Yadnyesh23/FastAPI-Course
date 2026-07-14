# Phase 5.8 – Advanced Relationships

## Objectives

By the end of this phase, you should understand:

- Cascading Deletes
- Orphan Records
- `cascade`
- `delete-orphan`
- Lazy Loading
- Eager Loading
- `joinedload()`
- `selectinload()`
- N+1 Query Problem
- Best Practices

---

# Part A – Cascading Deletes

## 1. What is Cascade?

Cascade tells SQLAlchemy **what should happen to child objects when an operation is performed on the parent object**.

Example:

```text
Student

↓

Notes
```

If the student is deleted, should the notes:

- Be deleted?
- Remain in the database?
- Prevent the student from being deleted?

The answer is determined by the **cascade** configuration.

---

## 2. Why is Cascade Needed?

Suppose we have:

```text
Students

id | name

1  | Yadnyesh
```

```text
Notes

id | title | student_id

1  | OS    | 1
2  | DBMS  | 1
3  | CN    | 1
```

Now the student is deleted:

```python
db.delete(student)

db.commit()
```

Without proper cascade rules, the notes may remain in the database, pointing to a student that no longer exists.

This creates **orphan records**.

---

## 3. What is an Orphan Record?

An orphan record is a **child record whose parent record no longer exists**.

Example:

```text
Students

(empty)
```

```text
Notes

id | title | student_id

1  | OS    | 1
2  | DBMS  | 1
```

Here, `student_id = 1` no longer exists.

These notes are orphan records.

---

## 4. Configuring Cascade

Cascade is usually defined on the **parent side** of the relationship.

Example:

```python
notes = relationship(
    "Note",
    back_populates="student",
    cascade="all, delete-orphan"
)
```

---

## 5. What Does `cascade="all"` Mean?

`all` tells SQLAlchemy to propagate most operations performed on the parent to its child objects.

Examples:

- Save parent → Save children
- Update parent → Update children (when appropriate)
- Delete parent → Delete children

Think of it as:

```text
Parent Operation

↓

Automatically applied to Child Objects
```

---

## 6. What Does `delete-orphan` Mean?

Suppose:

```text
Student

↓

OS Note

↓

DBMS Note
```

Now:

```python
student.notes.remove(os_note)
```

Without `delete-orphan`:

- The note is simply disconnected.
- It may still remain in the database.

With `delete-orphan`:

- SQLAlchemy automatically deletes the note because it no longer belongs to any parent.

This prevents orphan records.

---

## 7. Complete Example

```python
class Student(Base):

    __tablename__ = "students"

    id = mapped_column(Integer, primary_key=True)

    notes = relationship(
        "Note",
        back_populates="student",
        cascade="all, delete-orphan"
    )
```

```python
class Note(Base):

    __tablename__ = "notes"

    id = mapped_column(Integer, primary_key=True)

    student_id = mapped_column(
        ForeignKey("students.id")
    )

    student = relationship(
        "Student",
        back_populates="notes"
    )
```

---

## 8. Best Practices for Cascade

- Define cascade on the parent model.
- Use `delete-orphan` when child objects should not exist without a parent.
- Avoid orphan records unless your application explicitly requires them.
- Choose cascade behavior carefully because deleting a parent may delete many child records.

---

# Part B – Lazy Loading & Eager Loading

## 1. Why Do Loading Strategies Matter?

Suppose you fetch a student:

```python
student = db.execute(
    select(Student)
).scalar()
```

Should SQLAlchemy also load the student's notes?

There are two common approaches:

- Lazy Loading
- Eager Loading

---

## 2. Lazy Loading

Lazy Loading means:

> Related data is loaded **only when it is accessed**.

Example:

```python
student = db.execute(
    select(Student)
).scalar()
```

At this point:

- Student is loaded.
- Notes are **not** loaded.

Later:

```python
student.notes
```

SQLAlchemy executes another query to fetch the notes.

Flow:

```text
Load Student

↓

Student Loaded

↓

Access student.notes

↓

Fetch Notes
```

---

## 3. Advantages of Lazy Loading

- Loads only the data that is actually needed.
- Reduces unnecessary database queries when related data is never accessed.
- Saves memory for unused relationships.

---

## 4. Disadvantages of Lazy Loading

- Can generate many additional SQL queries.
- May lead to the **N+1 Query Problem**.

---

## 5. Eager Loading

Eager Loading means:

> Related data is loaded **immediately along with the parent object**.

The related data is available without executing additional queries later.

---

## 6. `joinedload()`

`joinedload()` performs eager loading using a SQL JOIN.

Example:

```python
from sqlalchemy.orm import joinedload

students = db.execute(
    select(Student).options(
        joinedload(Student.notes)
    )
).scalars().all()
```

Flow:

```text
One SQL Query

↓

JOIN

↓

Students + Notes
```

Use when:

- Related data is definitely required.
- The relationship size is relatively small.

---

## 7. `selectinload()`

`selectinload()` also performs eager loading but uses **two optimized queries**.

Example:

```python
from sqlalchemy.orm import selectinload

students = db.execute(
    select(Student).options(
        selectinload(Student.notes)
    )
).scalars().all()
```

Flow:

```text
Query 1

↓

Students

↓

Query 2

↓

All Related Notes
```

Use when:

- Fetching many parent records.
- Each parent has many related child records.
- Large JOINs would become inefficient.

---

## 8. `joinedload()` vs `selectinload()`

| `joinedload()` | `selectinload()` |
|---------------|------------------|
| Uses a SQL JOIN | Uses two SQL queries |
| Usually one query | Usually two queries |
| Best for smaller relationships | Best for larger collections |
| May duplicate parent rows in JOIN results | Avoids large JOIN result sets |

---

## 9. N+1 Query Problem

Suppose:

```python
students = db.execute(
    select(Student)
).scalars().all()
```

This executes:

```text
1 Query
```

Then:

```python
for student in students:
    print(student.notes)
```

If there are 100 students:

```text
1 Query

↓

Fetch Students

↓

100 Additional Queries

↓

Fetch Notes
```

Total:

```text
101 Queries
```

This is called the **N+1 Query Problem**.

It increases latency and database load.

---

## 10. Solving the N+1 Problem

Using:

```python
students = db.execute(
    select(Student).options(
        selectinload(Student.notes)
    )
).scalars().all()
```

SQLAlchemy performs:

```text
Query 1

↓

Fetch Students

↓

Query 2

↓

Fetch All Related Notes
```

Total:

```text
2 Queries
```

This is much more efficient.

---

## 11. When to Use Each Strategy

### Lazy Loading

Use when:

- Related data may not always be needed.
- Avoiding unnecessary data loading.

---

### `joinedload()`

Use when:

- Related data is always required.
- Relationship size is relatively small.
- A JOIN is efficient.

---

### `selectinload()`

Use when:

- Loading many parent records.
- Each parent has many child records.
- You want to avoid huge JOIN result sets.

---

## 12. Best Practices

- Use Lazy Loading when related data is optional.
- Use Eager Loading when related data is always required.
- Prefer `joinedload()` for small relationships.
- Prefer `selectinload()` for large One-to-Many relationships.
- Watch out for the N+1 Query Problem.
- Optimize loading strategies based on application requirements.

---

# 13. Interview Questions

1. What is Cascade?
2. Why is Cascade used?
3. What is an orphan record?
4. What does `cascade="all"` do?
5. What does `delete-orphan` do?
6. Where is `cascade` usually defined?
7. What is Lazy Loading?
8. What is Eager Loading?
9. Difference between Lazy Loading and Eager Loading?
10. What is `joinedload()`?
11. What is `selectinload()`?
12. Difference between `joinedload()` and `selectinload()`?
13. What is the N+1 Query Problem?
14. How can you avoid the N+1 Query Problem?
15. When would you choose Lazy Loading over Eager Loading?

---

# 14. Quick Cheat Sheet

| Feature | Purpose |
|----------|---------|
| `cascade` | Defines how parent operations affect child objects |
| `delete-orphan` | Deletes child objects that lose their parent |
| Orphan Record | Child record without a valid parent |
| Lazy Loading | Loads related data only when accessed |
| Eager Loading | Loads related data immediately |
| `joinedload()` | Eager loading using a SQL JOIN |
| `selectinload()` | Eager loading using two optimized queries |
| N+1 Query Problem | One parent query + N child queries |

---

# 15. Key Takeaways

- Cascade controls how operations on parent objects affect child objects.
- `delete-orphan` automatically removes child records that no longer have a parent.
- Orphan records are child records without a valid parent.
- Lazy Loading fetches related data only when it is accessed.
- Eager Loading fetches related data upfront.
- `joinedload()` performs eager loading using a SQL JOIN.
- `selectinload()` performs eager loading using two optimized SQL queries.
- The N+1 Query Problem occurs when one query fetches parent records and additional queries fetch each parent's related data individually.
- Choosing the appropriate loading strategy improves application performance and reduces unnecessary database queries.