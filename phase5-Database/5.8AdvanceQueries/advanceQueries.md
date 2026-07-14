# Phase 5.8 – Advanced SQLAlchemy Queries

## Objectives

By the end of this phase, you should understand:

- Filtering Records (`where()`)
- Multiple Conditions
- `and_()`
- `or_()`
- `IN`
- `LIKE`
- `order_by()`
- `limit()`
- `offset()`
- Aggregate Functions
- `func`
- Best Practices

---

# 1. Filtering Records (`where()`)

The `where()` method is used to filter records based on one or more conditions.

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

Another example:

```python
query = select(Student).where(
    Student.email == "abc@gmail.com"
)
```

Equivalent SQL:

```sql
SELECT *
FROM students
WHERE email = 'abc@gmail.com';
```

---

# 2. Multiple Conditions

Multiple conditions can be passed inside `where()`.

Example:

```python
query = select(Student).where(
    Student.age == 20,
    Student.is_active == True
)
```

Equivalent SQL:

```sql
SELECT *
FROM students
WHERE age = 20
AND is_active = TRUE;
```

---

# 3. Using `and_()`

`and_()` explicitly combines multiple conditions using the SQL `AND` operator.

Example:

```python
from sqlalchemy import and_

query = select(Student).where(
    and_(
        Student.age >= 18,
        Student.age <= 25
    )
)
```

Equivalent SQL:

```sql
SELECT *
FROM students
WHERE age >= 18
AND age <= 25;
```

### Difference between multiple conditions and `and_()`

Both generate the same SQL.

Example:

```python
.where(
    Student.age == 20,
    Student.is_active == True
)
```

and

```python
.where(
    and_(
        Student.age == 20,
        Student.is_active == True
    )
)
```

are functionally equivalent.

`and_()` is useful when dynamically building queries.

---

# 4. Using `or_()`

`or_()` combines conditions using the SQL `OR` operator.

Example:

```python
from sqlalchemy import or_

query = select(Student).where(
    or_(
        Student.age == 18,
        Student.age == 20
    )
)
```

Equivalent SQL:

```sql
SELECT *
FROM students
WHERE age = 18
OR age = 20;
```

---

# 5. Using `IN`

`IN` checks whether a value exists within a collection.

Example:

```python
query = select(Student).where(
    Student.id.in_([1, 5, 9])
)
```

Equivalent SQL:

```sql
SELECT *
FROM students
WHERE id IN (1, 5, 9);
```

---

# 6. Using `LIKE`

`LIKE` performs pattern matching on text columns.

Example:

```python
query = select(Student).where(
    Student.name.like("%yan%")
)
```

Matches:

```text
Yan
Aryan
Yadnyesh
```

## Wildcards

### Starts with

```python
Student.name.like("A%")
```

Examples:

```text
Amit
Akash
Aryan
```

---

### Ends with

```python
Student.name.like("%sh")
```

Examples:

```text
Yogesh
Ritesh
```

---

### Contains

```python
Student.name.like("%yan%")
```

Examples:

```text
Aryan
Yan
```

---

# 7. Sorting with `order_by()`

Sort records in ascending order.

Example:

```python
query = select(Student).order_by(
    Student.age
)
```

Equivalent SQL:

```sql
ORDER BY age ASC;
```

---

## Descending Order

```python
from sqlalchemy import desc

query = select(Student).order_by(
    desc(Student.age)
)
```

Equivalent SQL:

```sql
ORDER BY age DESC;
```

---

# 8. Limiting Results (`limit()`)

`limit()` restricts the number of rows returned.

Example:

```python
query = select(Student).limit(10)
```

Equivalent SQL:

```sql
LIMIT 10;
```

Useful for:

- Dashboards
- Recent records
- Pagination

---

# 9. Skipping Rows (`offset()`)

`offset()` skips a specified number of rows.

Example:

```python
query = select(Student).offset(20)
```

Equivalent SQL:

```sql
OFFSET 20;
```

Usually combined with:

```python
.limit(10)
```

Example:

```python
query = select(Student).offset(20).limit(10)
```

Returns:

```text
Rows 21–30
```

This is commonly used for **pagination**.

---

# 10. Aggregate Functions (`func`)

SQLAlchemy provides SQL aggregate functions through `func`.

Import:

```python
from sqlalchemy import func
```

---

## Count

Returns the total number of records.

```python
query = select(
    func.count(Student.id)
)
```

Equivalent SQL:

```sql
SELECT COUNT(id)
FROM students;
```

---

## Average

```python
query = select(
    func.avg(Student.age)
)
```

Equivalent SQL:

```sql
SELECT AVG(age)
FROM students;
```

---

## Maximum

```python
query = select(
    func.max(Student.age)
)
```

Equivalent SQL:

```sql
SELECT MAX(age)
FROM students;
```

---

## Minimum

```python
query = select(
    func.min(Student.age)
)
```

Equivalent SQL:

```sql
SELECT MIN(age)
FROM students;
```

---

## Sum

```python
query = select(
    func.sum(Student.age)
)
```

Equivalent SQL:

```sql
SELECT SUM(age)
FROM students;
```

---

# 11. Common Query Examples

## Get all active students

```python
query = select(Student).where(
    Student.is_active == True
)
```

---

## Get students between ages 18 and 25

```python
query = select(Student).where(
    Student.age.between(18, 25)
)
```

---

## Get students whose names start with "A"

```python
query = select(Student).where(
    Student.name.like("A%")
)
```

---

## Get the 10 youngest students

```python
query = select(Student).order_by(
    Student.age
).limit(10)
```

---

## Count total students

```python
query = select(
    func.count(Student.id)
)
```

---

# 12. Best Practices

- Use `where()` to filter records.
- Use `and_()` and `or_()` when combining complex conditions.
- Use `IN` for matching multiple values.
- Use `LIKE` for text searching.
- Use `order_by()` to sort results.
- Use `limit()` to reduce unnecessary data retrieval.
- Combine `offset()` and `limit()` for pagination.
- Use aggregate functions (`count`, `avg`, `max`, `min`, `sum`) for calculations in the database instead of Python.
- Let the database perform filtering and aggregation whenever possible for better performance.

---

# 13. Interview Questions

1. What is the purpose of `where()`?
2. How can multiple conditions be applied in SQLAlchemy?
3. What is the difference between multiple `where()` conditions and `and_()`?
4. What does `or_()` do?
5. What is the purpose of `IN`?
6. How does `LIKE` work?
7. Difference between `"A%"`, `"%A"` and `"%A%"`?
8. What does `order_by()` do?
9. Difference between ascending and descending sorting?
10. What is `limit()`?
11. What is `offset()`?
12. Why are `limit()` and `offset()` commonly used together?
13. What is `func`?
14. Which aggregate functions are commonly used in SQLAlchemy?
15. Why should aggregation be performed in the database instead of Python?

---

# 14. Quick Cheat Sheet

| Feature | Purpose |
|----------|---------|
| `where()` | Filter records |
| Multiple Conditions | Apply multiple filters |
| `and_()` | Combine conditions using `AND` |
| `or_()` | Combine conditions using `OR` |
| `in_()` | Match values from a list |
| `like()` | Pattern matching for text |
| `order_by()` | Sort records |
| `desc()` | Descending sorting |
| `limit()` | Restrict number of rows |
| `offset()` | Skip rows |
| `func.count()` | Count records |
| `func.avg()` | Calculate average |
| `func.max()` | Find maximum value |
| `func.min()` | Find minimum value |
| `func.sum()` | Calculate sum |

---

# 15. Key Takeaways

- `where()` filters records based on conditions.
- Multiple conditions can be passed directly to `where()` or explicitly combined using `and_()`.
- `or_()` returns records that satisfy any of the specified conditions.
- `IN` checks whether a value exists in a collection.
- `LIKE` is used for text pattern matching.
- `order_by()` sorts query results in ascending or descending order.
- `limit()` restricts the number of returned rows.
- `offset()` skips rows and is commonly used for pagination.
- SQLAlchemy provides aggregate functions through `func`, such as `count`, `avg`, `max`, `min`, and `sum`.
- Performing filtering, sorting, and aggregation in the database is more efficient than processing data in Python.