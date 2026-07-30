# Phase 7.3 — Register API

## Objective

The Register API allows a new user to create an account.

It is the first endpoint where all previously learned concepts come together:

- Pydantic Schemas
- SQLAlchemy Models
- Repository Pattern
- Service Layer
- Password Hashing
- JWT
- Transactions

---

# Endpoint

```http
POST /auth/register
```

---

# Request Body

```json
{
    "name": "Yadnyesh",
    "email": "yadnyesh@gmail.com",
    "password": "MyPassword123"
}
```

---

# Successful Response

```json
{
    "message": "User registered successfully",
    "access_token": "<jwt-token>",
    "token_type": "Bearer",
    "user": {
        "id": "uuid",
        "name": "Yadnyesh",
        "email": "yadnyesh@gmail.com"
    }
}
```

---

# Complete Registration Flow

```text
Client
    │
    ▼
POST /auth/register
    │
    ▼
Router
    │
    ▼
UserService.register_user()
    │
    ▼
UserRepository
    │
    ▼
Database
```

---

# Internal Workflow

```text
Receive Request
        │
        ▼
Pydantic Validation
        │
        ▼
Check Email Already Exists
        │
        ▼
Hash Password
        │
        ▼
Create UserModel
        │
        ▼
Repository.create_user()
        │
        ▼
Commit Transaction
        │
        ▼
Refresh User
        │
        ▼
Generate JWT
        │
        ▼
Return Response
```

---

# Step 1 — Validate Request

FastAPI automatically validates incoming data using Pydantic.

Example:

```python
class RegisterUserRequestModel(BaseModel):
    name: str
    email: EmailStr
    password: str
```

No manual validation like:

```python
if name == "":
```

is required.

Pydantic ensures:

- Required fields exist
- Correct data types
- Email format is valid

---

# Step 2 — Check Duplicate Email

Before creating a user, check whether the email already exists.

```
Find User By Email
        │
        ▼
Exists?
      /   \
    Yes   No
     │      │
409 Conflict
            │
            ▼
Continue Registration
```

Why?

Every email should uniquely identify one account.

---

# Step 3 — Hash Password

Never store plain passwords.

❌ Wrong

```python
password = request.password
```

✅ Correct

```python
hashed_password = password_hash.hash(request.password)
```

Store only the hashed password inside the database.

---

# Step 4 — Create UserModel

Convert the request into a SQLAlchemy model.

```python
user = UserModel(
    name=request.name,
    email=request.email,
    password=hashed_password
)
```

Repositories should receive ORM models, **not dictionaries**.

---

# Step 5 — Repository Layer

Repository responsibility:

- INSERT
- SELECT
- UPDATE
- DELETE

Example:

```python
repository.create_user(user)
```

Repository should **not**:

- Hash passwords
- Generate JWT
- Validate business rules

---

# Step 6 — Commit Transaction

Adding an object:

```python
db.add(user)
```

does **not** permanently save it.

To save:

```python
db.commit()
```

Without commit:

```
Program Ends
        │
        ▼
Data Lost
```

---

# Step 7 — Refresh Object

After commit:

```python
db.refresh(user)
```

Refresh loads the latest database values into the SQLAlchemy object.

Useful for automatically generated values like:

- UUID
- created_at
- updated_at

---

# Step 8 — Generate JWT

After successful registration:

```python
token = create_access_token(
    {
        "sub": str(user.id),
        "email": user.email
    }
)
```

JWT should contain only the required claims.

Use standard claim names like:

- sub
- exp
- iat

---

# Step 9 — Return Response

Return:

- User information
- JWT
- Token type

Example:

```json
{
    "access_token": "...",
    "token_type": "Bearer"
}
```

---

# Responsibilities of Each Layer

## Router

Responsibilities:

- Receive HTTP request
- Dependency Injection
- Call Service
- Return HTTP response

Should **not** contain business logic.

---

## Service

Responsibilities:

- Check duplicate email
- Hash password
- Create UserModel
- Call Repository
- Commit transaction
- Refresh object
- Generate JWT

Service contains the application's business logic.

---

## Repository

Responsibilities:

- Database queries only

Examples:

```python
get_user_by_email()

create_user()

update_user()

delete_user()
```

Repository should never know about:

- Password hashing
- JWT
- HTTP
- Business rules

---

# Transaction Flow

```
Repository

db.add(user)

        │

(No database write yet)

        ▼

Service

db.commit()

        │

Database Updated

        ▼

db.refresh(user)

        │

User object now contains generated values
```

---

# Why Commit in Service Instead of Repository?

Suppose:

```
Register User
        │
        ├── Create User
        ├── Create Welcome Notification
        └── Send Welcome Email
```

If Repository commits immediately:

```
User Created ✅

Notification Failed ❌
```

Database becomes inconsistent.

Instead:

```
Repository
    │
    ├── add(user)
    ├── add(notification)

Service
    │
    ▼
Single commit()
```

Service controls the entire transaction.

---

# Why Generate JWT in Service?

JWT generation is business logic.

Repository should only interact with the database.

Correct:

```
Service
    │
    ├── Hash Password
    ├── Generate JWT
    └── Commit
```

Repository:

```
INSERT
SELECT
UPDATE
DELETE
```

---

# Status Codes

| Situation | Status Code |
|-----------|------------|
| Registration Successful | 201 Created |
| Email Already Exists | 409 Conflict |
| Invalid Request | 422 Unprocessable Entity |
| Internal Server Error | 500 Internal Server Error |

---

# Project Structure

```
app/
│
├── api/
│   └── auth.py
│
├── services/
│   └── user.py
│
├── repository/
│   └── user.py
│
├── domain/
│   ├── models/
│   └── schemas/
│
├── core/
│   ├── jwt.py
│   └── security.py
│
└── db/
```

---

# Best Practices

✅ Use Pydantic for request validation.

✅ Never manually validate required fields if Pydantic already does it.

✅ Store only hashed passwords.

✅ Repository should work with SQLAlchemy models.

✅ Generate JWT only after successful registration.

✅ Commit transactions in the Service layer.

✅ Refresh the object after commit.

✅ Return meaningful HTTP status codes.

✅ Keep Router, Service, and Repository responsibilities separate.

---

# Common Mistakes

❌ Storing plain passwords.

❌ Returning 200 when email already exists.

❌ Hashing passwords inside Repository.

❌ Generating JWT inside Repository.

❌ Committing inside every Repository method.

❌ Passing dictionaries to Repository instead of ORM models.

❌ Returning tuples like:

```python
return {"message": "Error"}, 400
```

Instead, raise appropriate HTTP exceptions or custom exceptions.

---

# Key Takeaways

- Register API is the first complete authentication endpoint.
- Request validation is handled by Pydantic.
- Always check for duplicate emails before creating a user.
- Passwords must be hashed before storing.
- Repository only performs database operations.
- Service contains all business logic.
- Commit transactions in the Service layer.
- Refresh the object after commit to retrieve generated values.
- Generate JWT only after successful registration.
- Return a JWT so the user is immediately authenticated after registering.

---


