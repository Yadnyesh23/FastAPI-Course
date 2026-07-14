# Phase 5.9 – SQLAlchemy Joins

## Objectives

By the end of this phase, you should understand:

- What is a JOIN?
- Why JOINs are needed
- INNER JOIN
- LEFT OUTER JOIN
- SQLAlchemy `join()`
- SQLAlchemy `outerjoin()`
- Selecting specific columns
- Joining multiple tables
- `relationship()` vs `join()`
- Best Practices

---

# 1. What is a JOIN?

A **JOIN** combines rows from two or more related tables based on a common column, usually a **Foreign Key**.

Suppose we have two tables:

## Students

```text
id | name
-----------
1  | Yadnyesh
2  | Rahul
3  | Priya
```

## Notes

```text
id | title | student_id
-------------------------
1  | OS    | 1
2  | DBMS  | 1
3  | CN    | 2
```

If we want to display:

```text
Yadnyesh → OS
Yadnyesh → DBMS
Rahul → CN
```

The data comes from **both tables**, so we use a **JOIN**.

---

# 2. Why Are JOINs Needed?

In real-world applications, data is normalized and stored across multiple related tables.

Examples:

- User → Notes
- User → Orders
- Student → Courses
- Lecture → Notes
- Lecture → Mindmaps

To retrieve related data together, JOINs are used.

Without JOINs, multiple separate queries would be required.

---

# 3. INNER JOIN

An **INNER JOIN** returns **only the rows that have matching records in both tables**.

Example:

Students:

```text
1 | Yadnyesh
2 | Rahul
3 | Priya
```

Notes:

```text
OS → Student 1
DBMS → Student 1
CN → Student 2
```

Result:

```text
Yadnyesh → OS
Yadnyesh → DBMS
Rahul → CN
```

Notice:

Priya has no notes, so she is **not included**.

Equivalent SQL:

```sql
SELECT *
FROM students
INNER JOIN notes
ON students.id = notes.student_id;
```

---

# 4. INNER JOIN in SQLAlchemy

Example:

```python
query = (
    select(Student, Note)
    .join(Note)
)
```

SQLAlchemy automatically understands how to join the tables using the defined `ForeignKey` and `relationship()`.

---

# 5. LEFT OUTER JOIN

A **LEFT OUTER JOIN** returns:

- All rows from the **left table**
- Only matching rows from the **right table**

If there is no matching record, the right-side columns contain `NULL`.

Example:

```text
Yadnyesh → OS
Yadnyesh → DBMS
Rahul → CN
Priya → NULL
```

Priya appears even though she has no notes.

Equivalent SQL:

```sql
SELECT *
FROM students
LEFT JOIN notes
ON students.id = notes.student_id;
```

---

# 6. LEFT OUTER JOIN in SQLAlchemy

Example:

```python
query = (
    select(Student, Note)
    .outerjoin(Note)
)
```

SQLAlchemy's `outerjoin()` performs a **LEFT OUTER JOIN** by default.

---

# 7. Selecting Specific Columns

Sometimes we only need a few columns instead of entire model objects.

Example:

```python
query = select(
    Student.name,
    Note.title
).join(Note)
```

Result:

```text
name       title
-------------------
Yadnyesh   OS
Yadnyesh   DBMS
Rahul      CN
```

### Why Select Specific Columns?

Instead of retrieving every column from both tables:

```python
select(Student, Note)
```

you can retrieve only the required fields:

```python
select(Student.name, Note.title)
```

Benefits:

- Less data transferred from the database
- Faster query execution
- Lower memory usage
- Better API performance

---

# 8. Joining Multiple Tables

JOINs are not limited to two tables.

Example:

```text
User

↓

Lecture

↓

Note
```

SQLAlchemy:

```python
query = (
    select(User, Lecture, Note)
    .join(Lecture)
    .join(Note)
)
```

This joins all three related tables into a single query.

---

# 9. `relationship()` vs `join()`

Many beginners confuse these concepts.

## `relationship()`

`relationship()` defines how Python objects are related and allows navigation between them.

Example:

```python
student.notes
```

This accesses the related notes for a student.

It is used in the ORM layer.

---

## `join()`

`join()` generates a SQL JOIN query to retrieve related data from multiple tables.

Example:

```python
select(Student, Note).join(Note)
```

It is used while constructing SQL queries.

---

## Difference

| `relationship()` | `join()` |
|------------------|-----------|
| ORM feature | SQL query feature |
| Used for Python object navigation | Used to combine tables in SQL |
| Defined inside models | Used while writing queries |
| Does not itself create a SQL JOIN | Generates a SQL JOIN |

---

# 10. Common Examples

## Get all students with their notes

```python
query = (
    select(Student, Note)
    .join(Note)
)
```

---

## Get all students, even those without notes

```python
query = (
    select(Student, Note)
    .outerjoin(Note)
)
```

---

## Get only student names and note titles

```python
query = (
    select(Student.name, Note.title)
    .join(Note)
)
```

---

## Get all notes belonging to "Yadnyesh"

```python
query = (
    select(Note)
    .join(Student)
    .where(Student.name == "Yadnyesh")
)
```

---

# 11. When Should You Use JOINs?

Use JOINs when:

- Retrieving data from multiple related tables.
- Building dashboards.
- Creating reports.
- Displaying related records.
- Avoiding multiple database queries.

---

# 12. Best Practices

- Use INNER JOIN when only matching records are required.
- Use LEFT OUTER JOIN when all parent records should be returned.
- Select only the required columns whenever possible.
- Use `relationship()` for navigating related Python objects.
- Use `join()` when constructing SQL queries.
- Prefer JOINs over multiple separate queries when fetching related data.
- Ensure proper Foreign Keys and relationships are defined for clean joins.

---

# 13. Interview Questions

1. What is a JOIN?
2. Why are JOINs needed?
3. What is an INNER JOIN?
4. What is a LEFT OUTER JOIN?
5. Difference between INNER JOIN and LEFT OUTER JOIN?
6. What does `join()` do in SQLAlchemy?
7. What does `outerjoin()` do?
8. What is the difference between `relationship()` and `join()`?
9. Why should you select only required columns?
10. Can SQLAlchemy join more than two tables?
11. When would you use a LEFT OUTER JOIN instead of an INNER JOIN?
12. Why are JOINs important in real-world applications?

---

# 14. Quick Cheat Sheet

| Feature | Purpose |
|----------|---------|
| JOIN | Combine related tables |
| INNER JOIN | Return only matching rows |
| LEFT OUTER JOIN | Return all rows from left table and matching rows from right table |
| `join()` | Perform an INNER JOIN |
| `outerjoin()` | Perform a LEFT OUTER JOIN |
| `relationship()` | Navigate related Python objects |
| `select(Student, Note)` | Return complete model objects |
| `select(Student.name, Note.title)` | Return only required columns |

---

# 15. Key Takeaways

- A JOIN combines related data from multiple database tables.
- INNER JOIN returns only rows that exist in both tables.
- LEFT OUTER JOIN returns all rows from the left table and matching rows from the right table.
- SQLAlchemy provides `join()` for INNER JOINs and `outerjoin()` for LEFT OUTER JOINs.
- Selecting only required columns improves performance by reducing data transfer and memory usage.
- Multiple tables can be joined in a single query.
- `relationship()` is used for ORM object navigation, while `join()` generates SQL JOIN queries.
- JOINs are widely used in dashboards, reports, analytics, and APIs that combine data from multiple related tables.