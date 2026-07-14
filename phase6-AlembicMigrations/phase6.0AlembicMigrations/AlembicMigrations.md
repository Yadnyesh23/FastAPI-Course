# Phase 6.0 – Alembic (Database Migrations)

## Objectives

By the end of this phase, you should understand:

- Why database migrations are needed
- Limitations of `Base.metadata.create_all()`
- What Alembic is
- Database Migrations
- Migration History
- `upgrade()` and `downgrade()`
- Real Development Workflow
- Best Practices

---

# 1. Why Are Database Migrations Needed?

During development, database models continuously evolve.

Example:

Initial model:

```python
class Student(Base):
    __tablename__ = "students"

    id = mapped_column(primary_key=True)
    name = mapped_column(String)
```

Database:

```text
students

id
name
```

Later, a new requirement arrives:

```python
class Student(Base):
    __tablename__ = "students"

    id = mapped_column(primary_key=True)
    name = mapped_column(String)
    email = mapped_column(String)
```

The database schema must now be updated without losing the existing data.

This process is called a **database migration**.

---

# 2. Limitation of `Base.metadata.create_all()`

`Base.metadata.create_all()` creates database tables that do not already exist.

Example:

```python
Base.metadata.create_all(bind=engine)
```

However, if a table already exists, `create_all()` **does not modify it**.

For example, after adding:

```python
email = mapped_column(String)
```

Running:

```python
Base.metadata.create_all(bind=engine)
```

will **not** add the `email` column to the existing table.

Therefore, `create_all()` is suitable only for creating new tables, **not for updating existing database schemas**.

---

# 3. Why Not Recreate the Database?

Deleting and recreating the database whenever the schema changes would permanently remove all existing data.

Example:

```text
Users
Notes
Lectures
Mindmaps
Videos
```

All production data would be lost.

Real-world applications such as:

- Instagram
- Amazon
- Banking systems
- TesLearn

cannot afford to lose user data whenever a schema changes.

---

# 4. What is a Database Migration?

A **database migration** is a version-controlled change that updates an existing database schema while preserving existing data.

Instead of:

```text
Delete Database

↓

Create Database Again
```

we perform:

```text
Existing Database

↓

Apply Migration

↓

Updated Database
```

Only the required schema changes are applied.

Examples:

- Add a new column
- Remove a column
- Rename a table
- Create a new table
- Modify constraints

---

# 5. What is Alembic?

Alembic is SQLAlchemy's official **database migration tool**.

It helps keep:

```text
Python Models

↓

Database Schema
```

synchronized.

Alembic generates migration scripts whenever models change.

It supports:

- Schema upgrades
- Schema downgrades
- Version history
- Automatic migration generation

---

# 6. How Alembic Works

Whenever a model changes:

```python
email = mapped_column(String)
```

Alembic compares:

```text
Current Database Schema

↓

Current SQLAlchemy Models
```

and generates a migration describing the required changes.

Example migration:

```text
Add column "email" to students table
```

---

# 7. Migration History

Every database change is stored as a migration file.

Example:

```text
alembic/

└── versions/

    ├── 001_create_students.py

    ├── 002_add_email.py

    ├── 003_create_notes.py

    └── 004_add_phone.py
```

Each migration represents one version of the database schema.

Migration history works similarly to **Git commits**, but for the database.

---

# 8. Why is Migration History Important?

Migration history provides:

### Version Control

Every schema change is recorded.

---

### Team Collaboration

Every developer can apply the same migrations and maintain identical database schemas.

---

### Easy Deployment

Production databases can be updated automatically by applying new migrations.

---

### Rollback Support

If a deployment fails, previous migrations can be restored.

---

### Audit Trail

Developers can determine:

- What changed
- When it changed
- Which migration introduced the change

---

# 9. `upgrade()` and `downgrade()`

Every Alembic migration contains two functions:

```python
def upgrade():
```

and

```python
def downgrade():
```

## `upgrade()`

Applies new database changes.

Example:

```text
Add email column
```

---

## `downgrade()`

Reverts the migration.

Example:

```text
Remove email column
```

This allows the database to safely return to its previous version.

---

# 10. Why Are Downgrades Useful?

Downgrades are mainly used when:

- A deployment introduces bugs.
- A migration causes unexpected issues.
- The application must be rolled back to a previous stable version.

Instead of manually modifying the database, Alembic automatically restores the previous schema.

---

# 11. Real Development Workflow

Professional FastAPI projects generally follow this workflow:

```text
Modify SQLAlchemy Model

↓

Generate Alembic Migration

↓

Review Migration Script

↓

Apply Migration

↓

Database Updated
```

This ensures that:

- Models remain synchronized with the database.
- Database changes are version-controlled.
- Existing data remains safe.

---

# 12. Why Is This Workflow Better?

Compared to manually editing the database, this workflow provides:

- Safer deployments
- Consistent database schemas across environments
- Easy collaboration between developers
- Rollback capability
- Version-controlled database changes

---

# 13. Example Scenario

Version 1:

```python
class Student(Base):

    id = mapped_column(primary_key=True)

    name = mapped_column(String)
```

Migration:

```text
001_create_students.py
```

---

Later:

```python
email = mapped_column(String)
```

Migration:

```text
002_add_email.py
```

---

Later:

```python
phone = mapped_column(String)
```

Migration:

```text
003_add_phone.py
```

Each migration updates the existing database without affecting existing records.

---

# 14. Best Practices

- Never modify production databases manually.
- Always generate migrations after changing models.
- Review migration scripts before applying them.
- Keep migration files under version control (Git).
- Never delete migration history.
- Test migrations before deploying to production.
- Use `create_all()` only for initial table creation or small experiments, not for production schema updates.

---

# 15. Interview Questions

1. What is a database migration?
2. Why are migrations needed?
3. What are the limitations of `Base.metadata.create_all()`?
4. What is Alembic?
5. Why is Alembic used with SQLAlchemy?
6. What is migration history?
7. Why is migration history important?
8. What is the purpose of `upgrade()`?
9. What is the purpose of `downgrade()`?
10. Why would you downgrade a database?
11. Why is manually editing production databases discouraged?
12. What is the typical workflow when modifying a SQLAlchemy model?

---

# 16. Quick Cheat Sheet

| Feature | Purpose |
|----------|---------|
| Database Migration | Update database schema without losing data |
| `create_all()` | Create new tables only |
| Alembic | SQLAlchemy migration tool |
| Migration File | Stores one database schema change |
| Migration History | Tracks all schema versions |
| `upgrade()` | Apply new schema changes |
| `downgrade()` | Revert schema changes |
| Version History | Database equivalent of Git commits |

---

# 17. Key Takeaways

- Database schemas change as applications evolve.
- `Base.metadata.create_all()` only creates missing tables and does not modify existing ones.
- Database migrations update schemas while preserving existing data.
- Alembic is SQLAlchemy's official migration tool.
- Alembic automatically generates migration scripts based on model changes.
- Every migration is stored as a versioned migration file.
- Migration history enables version control, collaboration, auditing, and rollback.
- `upgrade()` applies schema changes, while `downgrade()` reverts them.
- Professional projects use Alembic to safely manage database schema changes throughout the application's lifecycle.