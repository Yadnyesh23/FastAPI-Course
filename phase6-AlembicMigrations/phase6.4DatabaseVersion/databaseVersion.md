# Phase 6.4 – Database Version Management

## Objectives

By the end of this phase, you should understand:

- Viewing the current database version
- Viewing migration history
- Upgrading the database
- Downgrading the database
- `head`
- `base`
- Relative revisions (`+1`, `-1`)
- Practical Alembic workflow
- Best Practices

---

# 1. Why Database Version Management?

As a project grows, multiple migrations are created over time.

Example:

```text
001_create_students

↓

002_add_email

↓

003_create_notes

↓

004_add_phone
```

Alembic keeps track of which migration version the database is currently using.

This allows developers to:

- Upgrade to newer versions.
- Downgrade to previous versions.
- View migration history.
- Keep databases synchronized across different environments.

---

# 2. Viewing the Current Database Version

Command:

```bash
alembic current
```

Example Output:

```text
003_create_notes
```

This command displays the migration revision currently applied to the database.

### Purpose

- Verify the current database version.
- Confirm successful upgrades or downgrades.
- Check which migration is active.

---

# 3. Viewing Migration History

Command:

```bash
alembic history
```

Example:

```text
004_add_phone

↓

003_create_notes

↓

002_add_email

↓

001_create_students
```

This command displays all migration revisions in order.

### Purpose

- View migration history.
- Understand migration order.
- Find specific revision IDs.

---

# 4. Upgrading the Database

To apply all pending migrations:

```bash
alembic upgrade head
```

Example:

Current version:

```text
002_add_email
```

Available migrations:

```text
003_create_notes

↓

004_add_phone
```

After running:

```bash
alembic upgrade head
```

Database version becomes:

```text
004_add_phone
```

---

# 5. What is `head`?

`head` represents the **latest available migration revision**.

Example:

```text
001

↓

002

↓

003

↓

004
```

Here:

```text
head = 004
```

Running:

```bash
alembic upgrade head
```

moves the database to the newest schema version.

---

# 6. Upgrading to a Specific Revision

Instead of upgrading to the latest migration, you can upgrade to a specific revision.

Example:

```bash
alembic upgrade a1b2c3d4
```

The database will stop at that particular migration.

### Why Upgrade to a Specific Revision?

Useful for:

- Testing a particular database version.
- Debugging migration issues.
- Reproducing older environments.
- Controlled deployments.

---

# 7. Downgrading the Database

To move back one migration:

```bash
alembic downgrade -1
```

Example:

Before:

```text
004_add_phone
```

After:

```text
003_create_notes
```

Downgrading executes the `downgrade()` function of the current migration.

---

# 8. What Does `-1` Mean?

`-1` means:

> Move backward by **one migration**.

Similarly:

```bash
alembic downgrade -2
```

moves backward two migrations.

---

# 9. Downgrading to Base

Command:

```bash
alembic downgrade base
```

`base` represents the database state **before any migrations were applied**.

Example:

```text
base

↓

001_create_students

↓

002_add_email

↓

003_create_notes

↓

004_add_phone
```

Running:

```bash
alembic downgrade base
```

removes all applied migrations and returns the database to its initial state.

---

# 10. Relative Revisions

Alembic allows movement relative to the current database version.

### Upgrade One Revision

```bash
alembic upgrade +1
```

Move forward one migration.

---

### Upgrade Two Revisions

```bash
alembic upgrade +2
```

Move forward two migrations.

---

### Downgrade One Revision

```bash
alembic downgrade -1
```

Move backward one migration.

---

### Downgrade Two Revisions

```bash
alembic downgrade -2
```

Move backward two migrations.

---

# 11. Difference Between `head` and `+1`

Suppose the current version is:

```text
001
```

Available migrations:

```text
002

↓

003

↓

004
```

### Upgrade to Head

```bash
alembic upgrade head
```

Result:

```text
004
```

All pending migrations are applied.

---

### Upgrade One Revision

```bash
alembic upgrade +1
```

Result:

```text
002
```

Only one migration is applied.

---

# 12. Typical Development Workflow

### Normal Workflow

```text
Modify SQLAlchemy Model

↓

Generate Migration

↓

Review Migration

↓

Upgrade Database

↓

Continue Development
```

### If Something Goes Wrong

```text
Downgrade Database

↓

Fix Model

↓

Generate New Migration

↓

Upgrade Again
```

---

# 13. Best Practices

- Use `alembic current` before applying migrations to verify the current database version.
- Use `alembic history` to inspect migration history.
- Prefer `alembic upgrade head` to keep the database fully updated.
- Use specific revisions only when testing or debugging.
- Always review migrations before applying them.
- Downgrade carefully, as removing migrations may delete schema changes and potentially affect data.
- Keep migration history consistent across all team members.

---

# 14. Interview Questions

1. What does `alembic current` do?
2. What does `alembic history` display?
3. What does `head` represent?
4. What is the purpose of `alembic upgrade head`?
5. What is the purpose of `alembic downgrade -1`?
6. What does `base` represent?
7. What is the difference between `head` and `+1`?
8. Why would a developer upgrade to a specific revision?
9. Why is downgrading useful?
10. What are relative revisions in Alembic?

---

# 15. Quick Cheat Sheet

| Command | Purpose |
|----------|---------|
| `alembic current` | Show the current database version |
| `alembic history` | Show migration history |
| `alembic upgrade head` | Upgrade to the latest migration |
| `alembic upgrade <revision>` | Upgrade to a specific revision |
| `alembic upgrade +1` | Upgrade one migration |
| `alembic upgrade +2` | Upgrade two migrations |
| `alembic downgrade -1` | Downgrade one migration |
| `alembic downgrade -2` | Downgrade two migrations |
| `alembic downgrade base` | Remove all migrations and return to the initial database state |
| `head` | Latest migration revision |
| `base` | Database state before any migrations |

---

# 16. Key Takeaways

- Alembic tracks the current database version using migration revisions.
- `alembic current` shows the migration currently applied to the database.
- `alembic history` displays the complete migration history.
- `alembic upgrade head` upgrades the database to the latest migration.
- `head` represents the newest available migration.
- `alembic upgrade <revision>` upgrades to a specific revision.
- `alembic downgrade -1` moves the database back by one migration.
- `base` represents the database state before any migrations were applied.
- Relative revisions (`+1`, `-1`) allow incremental upgrades and downgrades.
- Database version management enables safe schema evolution, debugging, testing, and rollback during development.