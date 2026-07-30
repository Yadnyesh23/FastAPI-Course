# Phase 7.4 — Login API

## Objective

The Login API authenticates an existing user and returns a JWT (JSON Web Token).

Unlike the Register API, Login **does not create a new user**. It simply verifies the user's credentials and issues an access token.

---

# Endpoint

```http
POST /auth/login
```

---

# Request Body

```json
{
    "email": "yadnyesh@gmail.com",
    "password": "MyPassword123"
}
```

---

# Successful Response

```json
{
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

# Complete Login Flow

```text
Client
    │
    ▼
POST /auth/login
    │
    ▼
Router
    │
    ▼
AuthService.login()
    │
    ▼
UserRepository.get_user_by_email()
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
Find User By Email
        │
        ▼
User Exists?
      /     \
    No       Yes
    │         │
    ▼         ▼
 Return 401   Verify Password
                │
          Wrong / \ Correct
              │      │
              ▼      ▼
         Return 401  Generate JWT
                        │
                        ▼
                 Return Response
```

---

# Step 1 — Validate Request

FastAPI automatically validates the request using Pydantic.

```python
class LoginRequestModel(BaseModel):
    email: EmailStr
    password: str
```

Validation includes:

- Required fields
- Correct data types
- Valid email format

---

# Step 2 — Find User by Email

Repository responsibility:

```python
user = repository.get_user_by_email(request.email)
```

Repository only queries the database.

It does **not**:

- Verify passwords
- Generate JWT
- Perform business logic

---

# Step 3 — Check User Exists

If no user is found:

```python
raise HTTPException(
    status_code=401,
    detail="Invalid email or password"
)
```

Never return:

```text
Email not found
```

because it helps attackers discover valid email addresses.

---

# Step 4 — Verify Password

The database stores:

```text
$2b$12$abcdefgh...
```

The user enters:

```text
MyPassword123
```

Do **not** compare hashes manually.

❌ Wrong

```python
hash(password) == stored_hash
```

Because bcrypt generates a different hash every time due to salting.

✅ Correct

```python
password_hash.verify(
    request.password,
    user.password
)
```

The password hashing library extracts the salt from the stored hash and performs the verification.

---

# Why Doesn't `==` Work?

Example:

```
Password: Hello123

↓

Hash #1

$2b$12$abc...

↓

Hash #2

$2b$12$xyz...
```

Same password.

Different hashes.

This is why `verify()` must be used.

---

# Step 5 — Generate JWT

Only after successful password verification.

```python
token = create_access_token(
    {
        "sub": str(user.id),
        "email": user.email
    }
)
```

JWT should contain only the claims needed for authentication.

Common claims:

- sub
- email
- role (optional)
- exp
- iat

Never include:

- Password
- OTP
- Credit card
- API keys

---

# Step 6 — Return Response

Return:

```json
{
    "access_token": "...",
    "token_type": "Bearer",
    "user": {
        "id": "...",
        "name": "...",
        "email": "..."
    }
}
```

Do not return the complete database model.

---

# Why Use the Same Error Message?

Suppose the login fails.

Instead of:

```
Email not found
```

or

```
Wrong password
```

Always return:

```
Invalid email or password
```

Reason:

This prevents **User Enumeration Attacks**.

Attackers cannot determine whether an email exists in your system.

---

# Responsibilities of Each Layer

## Router

Responsibilities:

- Receive HTTP request
- Inject dependencies
- Call Service
- Return HTTP response

Should not contain business logic.

---

## Service

Responsibilities:

- Find user
- Verify password
- Generate JWT
- Return response

Service contains the business logic.

---

## Repository

Responsibilities:

- Execute SQL queries

Examples:

```python
get_user_by_email()

create_user()

update_user()

delete_user()
```

Repository should never:

- Hash passwords
- Verify passwords
- Generate JWT
- Raise authentication errors

---

# Login Flow Diagram

```text
POST /auth/login
        │
        ▼
Validate Request
        │
        ▼
Find User By Email
        │
        ▼
User Found?
     /        \
   No          Yes
   │            │
   ▼            ▼
401      Verify Password
               │
        Wrong / \ Correct
            │      │
            ▼      ▼
          401   Generate JWT
                    │
                    ▼
             Return Token
```

---

# HTTP Status Codes

| Situation | Status Code |
|-----------|------------|
| Login Successful | 200 OK |
| Invalid Credentials | 401 Unauthorized |
| Invalid Request Body | 422 Unprocessable Entity |
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
│   └── auth.py
│
├── repository/
│   └── user.py
│
├── domain/
│   ├── models/
│   ├── schemas/
│   │   ├── request/
│   │   └── response/
│
├── core/
│   ├── jwt.py
│   └── security.py
│
└── db/
```

---

# Best Practices

✅ Validate requests using Pydantic.

✅ Always verify passwords using `password_hash.verify()`.

✅ Never compare bcrypt hashes using `==`.

✅ Return the same error message for invalid email and invalid password.

✅ Generate JWT only after successful authentication.

✅ Keep Repository limited to database operations.

✅ Keep authentication logic inside the Service layer.

✅ Return only the required user information.

---

# Common Mistakes

❌ Comparing password hashes manually.

❌ Returning "Email not found".

❌ Returning "Wrong password".

❌ Storing plain passwords.

❌ Generating JWT before password verification.

❌ Putting authentication logic inside Repository.

❌ Returning the complete UserModel.

---

# Login vs Register

| Register | Login |
|----------|-------|
| Creates new user | Authenticates existing user |
| Hashes password | Verifies password |
| Saves user to database | Reads user from database |
| Commits transaction | No database changes |
| Generates JWT | Generates JWT |

---

# Key Takeaways

- Login authenticates an existing user.
- Validate requests using Pydantic.
- Find the user by email using the Repository.
- Always verify passwords using `password_hash.verify()`.
- Never compare bcrypt hashes manually.
- Return a generic error message for authentication failures.
- Generate JWT only after successful authentication.
- Repository handles database operations only.
- Service handles authentication logic.
- Return only the token and minimal user information.

---

# Authentication Roadmap

```text
Phase 7.0 Authentication & Authorization ✅

Phase 7.1 Password Hashing ✅

Phase 7.2 JWT ✅

Phase 7.3 Register API ✅

Phase 7.4 Login API ✅

Phase 7.5 Protected Routes
        ↓
Phase 7.6 Current User Dependency
        ↓
Phase 7.7 Role-Based Authorization (RBAC)
```