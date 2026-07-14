# Phase 6.2 – Creating Your First Migration

## Objectives

By the end of this phase, you should understand:

- Why migrations are generated
- `alembic revision --autogenerate`
- Migration Files
- `upgrade()`
- `downgrade()`
- `alembic upgrade head`
- Migration Revision IDs
- Complete Alembic Workflow
- Best Practices

---

# 1. Why Generate a Migration?

Suppose the current SQLAlchemy model is:

```python
class Student(Base):
    __tablename__ = "students"

    id = mapped_column(primary_key=True)
    name = mapped_column(String)
```

Later, the model is updated:

```python
class Student(Base):
    __tablename__ = "students"

    id = mapped_column(primary_key=True)
    name = mapped_column(String)
    email = mapped_column(String)
```

Although the Python model has changed, the database schema remains unchanged.

The database does **not** automatically detect changes made to SQLAlchemy models.

To synchronize the database schema with the updated models, a migration must be generated.

---

# 2. Generating a Migration

Alembic compares:

```text
SQLAlchemy Models (Base.metadata)

↓

Current Database Schema
```

and generates the required migration.

Command:

```bash
alembic revision --autogenerate -m "Add email to students"
```

### Command Breakdown

- `revision` → Create a new migration.
- `--autogenerate` → Automatically compare SQLAlchemy models with the database schema and generate migration operations.
- `-m` → Add a descriptive message to the migration.

Example:

```bash
alembic revision --autogenerate -m "Create notes table"
```

---

# 3. Migration File

After generating a migration:

```text
alembic/

└── versions/

    8f2d7b91c8_add_email_to_students.py
```

A new migration file is created inside the `versions/` directory.

Each migration file contains the database operations needed to update or revert the schema.

---

# 4. Structure of a Migration File

Every migration contains two important functions:

```python
def upgrade():
    ...
```

```python
def downgrade():
    ...
```

These functions describe how the database schema should change.

---

# 5. `upgrade()`

The `upgrade()` function applies new database changes.

Typical operations include:

- Create table
- Add column
- Create index
- Add foreign key
- Add constraints

Example:

```python
def upgrade():
    op.add_column(...)
```

Running an upgrade modifies the database to the newer schema version.

---

# 6. `downgrade()`

The `downgrade()` function reverses the operations performed in `upgrade()`.

Typical operations include:

- Drop table
- Remove column
- Remove index
- Remove foreign key

Example:

```python
def downgrade():
    op.drop_column(...)
```

Downgrades allow the database to return safely to a previous version.

---

# 7. Applying a Migration

Generating a migration **does not** modify the database.

To apply pending migrations:

```bash
alembic upgrade head
```

This command executes all pending migrations until the latest version.

---

# 8. What Does `head` Mean?

`head` represents the **latest migration version**.

Example migration history:

```text
001_create_students

↓

002_add_email

↓

003_create_notes

↓

004_add_phone
```

Here:

```text
head = 004_add_phone
```

Running:

```bash
alembic upgrade head
```

updates the database to the newest schema version.

---

# 9. Migration Revision IDs

Every migration file begins with a unique revision ID.

Example:

```text
8f2d7b91c8_add_email_to_students.py
```

The first part:

```text
8f2d7b91c8
```

is the **Revision ID**.

Revision IDs uniquely identify each migration.

They allow Alembic to:

- Track migration history
- Maintain the correct migration order
- Identify the current database version
- Support upgrades and downgrades

---

# 10. Why Review a Migration Before Applying It?

Alembic automatically generates migration scripts, but they are not always perfect.

Example:

Suppose:

```python
name
```

is renamed to:

```python
full_name
```

Alembic may generate:

```text
Drop Column "name"

↓

Add Column "full_name"
```

instead of:

```text
Rename Column
```

Applying such a migration could delete existing data.

Therefore, developers should always review generated migration files before applying them.

---

# 11. Complete Alembic Workflow

The standard development workflow is:

```text
Modify SQLAlchemy Model

↓

Generate Migration

↓

Review Migration

↓

Apply Migration

↓

Database Updated
```

Commands used:

```bash
alembic revision --autogenerate -m "Your message"
```

↓

```bash
alembic upgrade head
```

---

# 12. Example Workflow

Current model:

```python
class Student(Base):
    id = mapped_column(primary_key=True)
    name = mapped_column(String)
```

Developer adds:

```python
phone = mapped_column(String)
```

Generate migration:

```bash
alembic revision --autogenerate -m "Add phone column"
```

Review the generated migration.

Apply it:

```bash
alembic upgrade head
```

The database now contains the new `phone` column without losing existing data.

---

# 13. Best Practices

- Generate a migration after every model change.
- Use meaningful migration messages.
- Always review autogenerated migrations before applying them.
- Never assume autogenerated migrations are always correct.
- Apply migrations only after verification.
- Keep migration files under version control (Git).
- Use `alembic upgrade head` to apply the latest migrations.

---

# 14. Interview Questions

1. Why are migrations generated?
2. What does `--autogenerate` do?
3. Which command generates a migration?
4. Which command applies pending migrations?
5. What is the purpose of `upgrade()`?
6. What is the purpose of `downgrade()`?
7. What does `head` mean in Alembic?
8. What is a Revision ID?
9. Why are Revision IDs important?
10. Why should autogenerated migrations be reviewed?
11. Does generating a migration update the database?
12. Where are migration files stored?

---

# 15. Quick Cheat Sheet

| Command / Feature | Purpose |
|-------------------|---------|
| `alembic revision --autogenerate -m "message"` | Generate a new migration |
| `--autogenerate` | Compare models with the database and create migration operations |
| `-m` | Add a descriptive migration message |
| `alembic upgrade head` | Apply all pending migrations |
| `head` | Latest migration version |
| `upgrade()` | Apply schema changes |
| `downgrade()` | Revert schema changes |
| Revision ID | Unique identifier for each migration |
| `alembic/versions/` | Stores migration files |

---

# 16. Key Takeaways

- SQLAlchemy model changes do **not** automatically update the database.
- Alembic generates migration files by comparing `Base.metadata` with the current database schema.
- `alembic revision --autogenerate -m "message"` creates a new migration file.
- Migration files are stored inside the `alembic/versions/` directory.
- Every migration contains `upgrade()` and `downgrade()` functions.
- `upgrade()` applies schema changes, while `downgrade()` reverts them.
- `alembic upgrade head` applies all pending migrations to the latest version.
- Every migration has a unique Revision ID that maintains migration history and execution order.
- Always review autogenerated migrations before applying them to avoid unintended schema changes or data loss.