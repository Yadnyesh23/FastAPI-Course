# Phase 7.5 — Protected Routes

## Objective

After a user logs in, they receive a JWT. Every protected endpoint should verify this JWT before allowing access.

Protected Routes ensure that **only authenticated users** can access specific endpoints.

---

# Why Protected Routes?

Without Protected Routes:

```http
GET /user/me
```

Anyone can call this endpoint.

---

With Protected Routes:

```http
GET /user/me
Authorization: Bearer <JWT>
```

Server verifies the JWT before executing the endpoint.

---

# Authentication Flow

```text
User Login
     │
     ▼
Receive JWT
     │
     ▼
Store JWT (Frontend)
     │
     ▼
Send JWT in every request
     │
     ▼
Authorization Header
     │
     ▼
Extract Token
     │
     ▼
Verify JWT
     │
     ▼
Extract User ID
     │
     ▼
Find User in Database
     │
     ▼
Return Current User
     │
     ▼
Execute Protected Route
```

---

# Authorization Header

JWT is sent using the HTTP Authorization Header.

```http
Authorization: Bearer eyJhbGc...
```

Where:

- Authorization → HTTP Header
- Bearer → Authentication Scheme
- eyJhbGc... → JWT Token

---

# What does "Bearer" mean?

Bearer means:

> "The holder (bearer) of this token is requesting access."

FastAPI removes the `Bearer` prefix and extracts only the JWT.

---

# OAuth2PasswordBearer

FastAPI provides:

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)
```

Its responsibility is ONLY:

✅ Extract JWT from Authorization Header

It DOES NOT:

- Verify JWT
- Decode JWT
- Find User
- Authenticate User

---

# OAuth2PasswordRequestForm

For OAuth2-compatible login, FastAPI provides:

```python
from fastapi.security import OAuth2PasswordRequestForm
```

Instead of accepting JSON:

```json
{
    "email": "...",
    "password": "..."
}
```

OAuth2 expects Form Data:

```text
username=abc@gmail.com
password=123456
```

Even when logging in using email, OAuth2 still uses the field name:

```text
username
```

---

# Why OAuth2PasswordRequestForm uses Depends()

```python
form_data: OAuth2PasswordRequestForm = Depends()
```

Reason:

FastAPI has to:

- Read Form Data
- Parse it
- Validate it
- Create OAuth2PasswordRequestForm object

Then inject it into the endpoint.

---

# Clean Architecture

Router should know about FastAPI.

Service should NOT.

Correct:

```python
result = await auth_service.login_user(
    email=form_data.username,
    password=form_data.password
)
```

Incorrect:

```python
await auth_service.login_user(form_data)
```

Reason:

Service should work with plain Python values instead of FastAPI-specific classes.

---

# get_current_user()

The heart of authentication.

Responsibilities:

1. Extract JWT
2. Decode JWT
3. Extract User ID
4. Find User
5. Return User

Example:

```python
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = jwt_helper.decode(token)

    user_id = payload["sub"]

    user = repository.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user
```

---

# Why use "sub"?

JWT has standard claims.

Common claims:

- sub → Subject (User ID)
- exp → Expiration Time
- iat → Issued At
- nbf → Not Before
- iss → Issuer
- aud → Audience

Instead of:

```python
{
    "user_id": user.id
}
```

Prefer:

```python
{
    "sub": str(user.id)
}
```

Reason:

`sub` is the JWT standard for identifying the token owner.

---

# Why Find User Again?

Even if JWT is valid:

```text
Monday:
User logs in

↓

JWT generated

↓

Tuesday:
Admin deletes user

↓

Wednesday:
User sends old JWT
```

JWT is still valid.

But user no longer exists.

Therefore:

Always query the database after decoding the token.

Database is always the source of truth.

---

# Protected Endpoint

```python
@router.get("/me")
async def get_me(
    current_user: UserModel = Depends(get_current_user)
):
    return current_user
```

Notice:

The route never:

- Decodes JWT
- Verifies JWT
- Finds User

It simply receives:

```python
current_user
```

Dependency Injection keeps routes clean.

---

# Authentication Pipeline

```text
HTTP Request
      │
      ▼
Authorization Header
      │
      ▼
OAuth2PasswordBearer
      │
Extract Token
      │
      ▼
JWTHelper.decode()
      │
Decode JWT
      │
      ▼
Extract sub
      │
      ▼
UserRepository.get_user_by_id()
      │
      ▼
Return UserModel
      │
      ▼
Protected Route Executes
```

---

# Common Mistakes

### 1. Using old JWT

If payload changes (e.g., from `user_id` to `sub`), generate a new JWT by logging in again.

---

### 2. Forgetting `await`

Incorrect:

```python
user = repo.get_user_by_id(user_id)
```

Correct:

```python
user = await repo.get_user_by_id(user_id)
```

(Only when using async repository.)

---

### 3. Using `user_id` instead of `sub`

Preferred:

```python
payload = {
    "sub": str(user.id),
    "email": user.email,
}
```

---

### 4. Passing FastAPI classes to Service

Incorrect:

```python
service.login_user(form_data)
```

Correct:

```python
service.login_user(
    email=form_data.username,
    password=form_data.password,
)
```

---

# Responsibilities

## OAuth2PasswordBearer

- Extract Token

---

## JWTHelper

- Encode JWT
- Decode JWT
- Verify Signature
- Verify Expiration

---

## get_current_user()

- Decode JWT
- Extract User ID
- Query Database
- Return Current User

---

## Router

- Receive Request
- Call Dependency
- Return Response

---

## Repository

- Database Operations Only

---

# HTTP Status Codes

| Status Code | Meaning |
|-------------|----------|
| 200 | Success |
| 401 | Invalid/Expired Token |
| 404 | User Not Found (or 401 depending on API design) |

---

# Key Takeaways

- Protected Routes require authentication.
- JWT is sent using the Authorization Header.
- OAuth2PasswordBearer only extracts the token.
- OAuth2PasswordRequestForm parses login form data.
- JWT should store User ID inside the `sub` claim.
- Always verify JWT before accessing protected resources.
- Always query the database after decoding JWT.
- `Depends(get_current_user)` keeps routes clean.
- Router handles FastAPI-specific logic.
- Service handles business logic.
- Repository handles database operations.