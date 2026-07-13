# Phase 5.6 – Database Relationships

## Objectives

By the end of this phase, you should understand:

- Why database relationships are needed
- Primary Key vs Foreign Key
- What is a Foreign Key?
- Types of Database Relationships
- One-to-One
- One-to-Many
- Many-to-One
- Many-to-Many
- `ForeignKey()`
- `relationship()`
- `back_populates`
- Accessing Related Objects
- Relationship Flow
- Common Mistakes

---

# 1. Why Do We Need Relationships?

In real-world applications, storing all data in a single table is not practical. Different types of data are stored in separate tables to avoid redundancy, improve organization, and maintain data integrity.

Example:

Instead of storing everything in one table:

```text
Users

id | name | note1 | note2 | note3 | note4
```

We separate the data:

```text
Users

id | name

1  | Yadnyesh
```

```text
Notes

id | title | user_id

1  | OS    | 1
2  | DBMS  | 1
3  | CN    | 1
```

Here, the `Notes` table stores only note-related information, while the `Users` table stores user information. The relationship between them is maintained using a **Foreign Key**.

---

# 2. What is a Foreign Key?

A **Foreign Key (FK)** is a column in one table that references the **Primary Key (PK)** of another table.

Example:

```text
Users

id | name

1  | Yadnyesh
2  | Rahul
```

```text
Notes

id | title | user_id

1  | OS    | 1
2  | DBMS  | 1
3  | CN    | 2
```

Here:

```text
Notes.user_id

↓

Users.id
```

The `user_id` column is the Foreign Key.

---

# 3. Primary Key vs Foreign Key

| Primary Key | Foreign Key |
|--------------|-------------|
| Uniquely identifies each row | References a Primary Key in another table |
| Must contain unique values | Can contain duplicate values |
| Usually cannot be NULL | Can be NULL if allowed |
| Generally one per table | A table can have multiple Foreign Keys |

---

# 4. Types of Database Relationships

## One-to-One (1:1)

One record in the first table is related to exactly one record in the second table.

Example:

```text
Person

↓

Passport
```

One person has one passport.

---

## One-to-Many (1:N)

One record in the parent table is related to multiple records in the child table.

Example:

```text
User

↓

Many Notes
```

One user can create many notes.

---

## Many-to-One (N:1)

Multiple records in one table belong to a single record in another table.

Example:

```text
Many Notes

↓

One User
```

Many notes belong to one user.

---

## Many-to-Many (N:N)

Multiple records from one table are related to multiple records in another table.

Example:

```text
Students

⇄

Courses
```

One student can enroll in many courses, and one course can have many students.

This relationship requires a **junction (association) table**.

---

# 5. What is `ForeignKey()`?

`ForeignKey()` is a SQLAlchemy function that creates the relationship **at the database level**.

Example:

```python
student_id = mapped_column(
    ForeignKey("students.id")
)
```

Meaning:

```text
student_id

↓

students.id
```

The database now knows that `student_id` references the `id` column of the `students` table.

Without `ForeignKey()`, the column is treated as a normal integer column.

---

# 6. What is `relationship()`?

`relationship()` creates the relationship **at the Python (ORM) level**.

It allows SQLAlchemy to automatically navigate between related objects without writing SQL queries manually.

Example:

```python
student.notes
```

Instead of writing:

```sql
SELECT *
FROM notes
WHERE student_id = student.id;
```

SQLAlchemy automatically fetches the related notes.

Similarly:

```python
note.student
```

automatically returns the student who owns that note.

---

# 7. Why Do We Need Both `ForeignKey()` and `relationship()`?

They have different responsibilities.

### `ForeignKey()`

- Works at the **database level**
- Creates the actual relationship between tables
- Enforces referential integrity

### `relationship()`

- Works at the **Python (ORM) level**
- Lets us navigate between related objects
- Eliminates the need to manually write JOIN queries in many cases

Together they provide both:

- Database-level relationships
- Python object relationships

---

# 8. Implementing a One-to-Many Relationship

## Student Model

```python
class Student(Base):

    __tablename__ = "students"

    id = mapped_column(Integer, primary_key=True)

    name = mapped_column(String)

    notes = relationship(
        "Note",
        back_populates="student"
    )
```

---

## Note Model

```python
class Note(Base):

    __tablename__ = "notes"

    id = mapped_column(Integer, primary_key=True)

    title = mapped_column(String)

    student_id = mapped_column(
        ForeignKey("students.id")
    )

    student = relationship(
        "Student",
        back_populates="notes"
    )
```

---

# 9. What is `back_populates`?

`back_populates` connects two `relationship()` definitions together.

Example:

Student:

```python
notes = relationship(
    "Note",
    back_populates="student"
)
```

Note:

```python
student = relationship(
    "Student",
    back_populates="notes"
)
```

SQLAlchemy now understands that:

```text
Student.notes

⇄

Note.student
```

are two sides of the same relationship.

Without `back_populates`, SQLAlchemy cannot properly synchronize both sides of the relationship.

---

# 10. Accessing Related Objects

Once the relationship is created:

### Get all notes of a student

```python
student.notes
```

Returns:

```python
[
    Note(...),
    Note(...),
    Note(...)
]
```

---

### Get the owner of a note

```python
note.student
```

Returns:

```python
Student(...)
```

No manual SQL queries are required.

---

# 11. Relationship Flow

```text
Student Object

↓

student.notes

↓

SQLAlchemy

↓

Database

↓

Returns Related Notes
```

Reverse:

```text
Note Object

↓

note.student

↓

SQLAlchemy

↓

Database

↓

Returns Related Student
```

---

# 12. Common Mistakes

### Forgetting `ForeignKey()`

Incorrect:

```python
student_id = mapped_column(Integer)
```

This is only an integer column.

Correct:

```python
student_id = mapped_column(
    ForeignKey("students.id")
)
```

---

### Confusing `ForeignKey()` and `relationship()`

Remember:

- `ForeignKey()` creates the relationship in the database.
- `relationship()` creates the relationship between Python objects.

---

### Incorrect `back_populates`

Both sides must reference each other's relationship attribute.

Correct:

```python
Student.notes

↓

back_populates="student"
```

```python
Note.student

↓

back_populates="notes"
```

---

### Incorrect Table Name

Incorrect:

```python
ForeignKey("student.id")
```

Correct:

```python
ForeignKey("students.id")
```

Format:

```text
tablename.column
```

---

# 13. Real TesLearn Examples

## User → Lectures

```text
User

↓

Many Lectures
```

Access:

```python
user.lectures
```

---

## Lecture → User

```python
lecture.user
```

Returns the lecture owner.

---

## Lecture → Note

```text
Lecture

↓

One Note
```

Access:

```python
lecture.note
```

---

## Lecture → Mindmap

```text
Lecture

↓

One Mindmap
```

Access:

```python
lecture.mindmap
```

---

# 14. Interview Questions

1. Why are database relationships needed?
2. What is a Foreign Key?
3. Difference between Primary Key and Foreign Key?
4. What are the four types of database relationships?
5. What does `ForeignKey()` do?
6. What does `relationship()` do?
7. Why do we need both `ForeignKey()` and `relationship()`?
8. What is `back_populates`?
9. What does `student.notes` return?
10. What does `note.student` return?
11. Which table contains the Foreign Key in a One-to-Many relationship?
12. What happens if `ForeignKey()` is omitted?
13. What happens if `relationship()` is omitted?

---

# 15. Quick Cheat Sheet

| Feature | Purpose |
|----------|---------|
| Primary Key | Uniquely identifies each row |
| Foreign Key | Links one table to another |
| One-to-One | One record ↔ One record |
| One-to-Many | One parent ↔ Many children |
| Many-to-One | Many children ↔ One parent |
| Many-to-Many | Many records ↔ Many records |
| `ForeignKey()` | Creates the database-level relationship |
| `relationship()` | Creates the Python object relationship |
| `back_populates` | Links both ORM relationships together |
| `student.notes` | Returns all notes of a student |
| `note.student` | Returns the owner of the note |

---

# 16. Key Takeaways

- Relationships connect related data stored in different tables.
- A Foreign Key references the Primary Key of another table.
- One-to-One, One-to-Many, Many-to-One, and Many-to-Many are the four common relationship types.
- `ForeignKey()` creates the relationship at the database level.
- `relationship()` creates the relationship at the Python ORM level.
- Both `ForeignKey()` and `relationship()` are usually used together.
- `back_populates` connects both sides of a relationship, allowing SQLAlchemy to keep them synchronized.
- Relationships allow easy navigation between related objects using expressions like `student.notes` and `note.student` without manually writing SQL queries.