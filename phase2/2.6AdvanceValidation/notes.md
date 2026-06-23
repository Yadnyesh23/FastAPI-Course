# Phase 2.6 – Validation & Advanced Constraints

## Objectives

By the end of this phase, you should understand:

- Why validation is important
- Field()
- Numeric Constraints
- String Constraints
- Email Validation
- URL Validation
- List Constraints
- Pattern (Regex) Validation
- Custom Validators
- Validation Errors
- Real-world Validation Design

---

# Why Validation Is Important

Validation ensures that only valid data enters your application.

Without validation:

```json
{
  "title": "",
  "duration": -20
}
```

Problems:

- Empty title
- Negative duration
- Corrupted database records
- Unexpected application behavior

Validation protects:

- Database
- Business Logic
- API Integrity

---

# Field()

Pydantic provides:

```python
from pydantic import Field
```

Field() is used for:

- Validation Rules
- Metadata
- Default Values
- Swagger Documentation

Example:

```python
class Student(BaseModel):
    age: int = Field(
        ge=18,
        le=30
    )
```

Meaning:

```text
18 <= age <= 30
```

---

# Numeric Constraints

## Greater Than (gt)

```python
price: float = Field(
    gt=0
)
```

Meaning:

```text
price > 0
```

Valid:

```json
{
  "price": 100
}
```

Invalid:

```json
{
  "price": 0
}
```

---

## Greater Than or Equal (ge)

```python
age: int = Field(
    ge=18
)
```

Meaning:

```text
age >= 18
```

---

## Less Than (lt)

```python
discount: int = Field(
    lt=100
)
```

Meaning:

```text
discount < 100
```

---

## Less Than or Equal (le)

```python
score: int = Field(
    le=100
)
```

Meaning:

```text
score <= 100
```

---

## Range Validation

```python
age: int = Field(
    ge=18,
    le=30
)
```

Meaning:

```text
18 <= age <= 30
```

---

# Quick Comparison

| Constraint | Meaning |
|------------|---------|
| gt | > |
| ge | >= |
| lt | < |
| le | <= |

Example:

```python
Field(gt=0)
```

means:

```text
value > 0
```

---

# String Constraints

## Minimum Length

```python
username: str = Field(
    min_length=3
)
```

---

## Maximum Length

```python
username: str = Field(
    max_length=20
)
```

---

## Combined

```python
username: str = Field(
    min_length=3,
    max_length=20
)
```

Valid:

```text
Yadnyesh
```

Invalid:

```text
Yo
```

---

# Pattern Validation (Regex)

Used to control which characters are allowed.

Example:

```python
username: str = Field(
    pattern=r"^[a-zA-Z0-9_]+$"
)
```

Allowed:

- Letters
- Numbers
- Underscore

Valid:

```text
yadnyesh_123
```

Invalid:

```text
yadnyesh@123
```

---

# Email Validation

Instead of:

```python
email: str
```

Use:

```python
from pydantic import EmailStr

email: EmailStr
```

Valid:

```text
abc@gmail.com
```

Invalid:

```text
abc
```

Pydantic automatically validates the email format.

---

# URL Validation

```python
from pydantic import AnyUrl

website: AnyUrl
```

Valid:

```text
https://teslearn.com
```

Invalid:

```text
teslearn
```

Useful for:

- Website URLs
- Portfolio Links
- Social Links

---

# List Constraints

Example:

```python
tags: list[str] = Field(
    min_length=1
)
```

Meaning:

```text
At least one tag required
```

Valid:

```json
{
  "tags": ["python"]
}
```

Invalid:

```json
{
  "tags": []
}
```

---

# Combining Multiple Constraints

Example:

```python
class User(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_]+$"
    )

    age: int = Field(
        ge=18,
        le=60
    )
```

Production APIs commonly combine multiple constraints.

---

# Validation Errors

Model:

```python
class User(BaseModel):
    age: int = Field(
        ge=18
    )
```

Request:

```json
{
  "age": 10
}
```

FastAPI Response:

```text
422 Unprocessable Entity
```

Error response contains:

- Field Name
- Invalid Value
- Validation Rule Violated

Example:

```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": ["body", "age"],
      "msg": "Input should be greater than or equal to 18"
    }
  ]
}
```

---

# Custom Validators

Sometimes built-in validation is not enough.

Pydantic v2 provides:

```python
from pydantic import field_validator
```

Example:

```python
from pydantic import BaseModel
from pydantic import field_validator

class User(BaseModel):

    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if len(value) < 8:
            raise ValueError(
                "Password too short"
            )

        return value
```

---

# Password Validation Example

Requirement:

- Minimum length 8
- Must contain a digit

```python
from pydantic import BaseModel
from pydantic import field_validator

class User(BaseModel):

    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if len(value) < 8:
            raise ValueError(
                "Password must be at least 8 characters"
            )

        if not any(
            char.isdigit()
            for char in value
        ):
            raise ValueError(
                "Password must contain a digit"
            )

        return value
```

---

# When To Use Custom Validators

Use custom validators when built-in constraints are insufficient.

Examples:

- Password Rules
- Confirm Password Logic
- Username Restrictions
- Business Rules
- Date Comparisons
- Cross-field Validation

---

# FastAPI Validation Flow

Incoming Request

```json
{
  "username": "ya",
  "age": 10
}
```

FastAPI:

1. Parses JSON
2. Creates Pydantic Model
3. Applies Field Constraints
4. Runs Custom Validators
5. Returns 422 if validation fails

Only valid data reaches your route function.

---

# TesLearn Example

```python
from pydantic import (
    BaseModel,
    Field,
    EmailStr
)

class UserRegister(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=20
    )

    email: EmailStr

    password: str = Field(
        min_length=8
    )
```

Benefits:

- Clean API
- Strong Validation
- Better Security
- Less Manual Code

---

# Best Practices

- Always validate user input.
- Use Field() whenever constraints are needed.
- Use EmailStr for emails.
- Use AnyUrl for URLs.
- Use pattern= for username rules.
- Keep custom validators focused and simple.
- Return clear validation errors.

---

# Common Mistakes

## ❌ No Validation

Bad:

```python
age: int
```

Better:

```python
age: int = Field(
    ge=18,
    le=30
)
```

---

## ❌ Using str For Emails

Bad:

```python
email: str
```

Better:

```python
email: EmailStr
```

---

## ❌ Complex Logic Without Validators

Bad:

```python
password: str
```

Better:

```python
@field_validator("password")
```

Add custom password rules.

---

# Interview Questions

1. Why is validation important?
2. What is the purpose of Field()?
3. Difference between gt and ge?
4. Difference between lt and le?
5. What is EmailStr?
6. What is pattern= used for?
7. What happens when validation fails?
8. What is a custom validator?
9. When should custom validators be used?
10. What status code does FastAPI return for validation errors?

---

# Key Takeaways

- Validation protects your application from invalid data.
- Field() is used for constraints and metadata.
- gt, ge, lt, le control numeric ranges.
- min_length and max_length control string length.
- pattern= uses regex for advanced string validation.
- EmailStr validates email addresses.
- AnyUrl validates URLs.
- Custom validators handle business-specific rules.
- FastAPI automatically returns 422 Unprocessable Entity on validation failure.
- Only validated data reaches your route functions.