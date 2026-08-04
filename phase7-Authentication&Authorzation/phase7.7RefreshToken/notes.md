# Phase 7.6 — Refresh Tokens

## Objective

Implement a secure authentication mechanism where users can stay logged in without having to enter their credentials repeatedly.

Instead of keeping one long-lived JWT, we use:

- **Access Token** → Short-lived
- **Refresh Token** → Long-lived

---

# Why do we need Refresh Tokens?

Suppose a user logs in.

```text
Login
   │
   ▼
Access Token (15 min)
```

After 15 minutes:

```text
Access Token
     │
     ▼
Expired
     │
     ▼
401 Unauthorized
```

Without Refresh Tokens, the user would need to log in again every time the Access Token expires.

This creates a poor user experience.

---

# Solution

Return **two tokens** during login.

```text
Login
   │
   ▼
Access Token
Refresh Token
```

The Access Token is used for authentication.

The Refresh Token is only used to generate a new Access Token.

---

# Access Token vs Refresh Token

| Access Token | Refresh Token |
|--------------|---------------|
| Short-lived | Long-lived |
| Sent with every request | Sent only to `/auth/refresh` |
| Used for authentication | Used to generate a new Access Token |
| Expires quickly | Expires after days/weeks |

Typical values:

```text
Access Token  → 15 minutes

Refresh Token → 30 days
```

---

# Authentication Flow

```text
             Login
               │
     ┌─────────┴─────────┐
     ▼                   ▼
Access Token       Refresh Token
 (15 min)            (30 days)
     │
     ▼
Protected APIs
     │
     ▼
Expires
     │
     ▼
POST /auth/refresh
     │
     ▼
Verify Refresh Token
     │
     ▼
Generate NEW Access Token
     │
     ▼
Continue using application
```

---

# Why not keep Access Token valid for 30 days?

Suppose an attacker steals the token.

If the token expires in:

```text
30 days
```

The attacker has access for 30 days.

Instead:

```text
15 minutes
```

The attack window becomes very small.

Short-lived Access Tokens improve security.

---

# Why not use Refresh Token for every request?

Refresh Tokens are more valuable.

If an attacker steals a Refresh Token, they can continuously generate new Access Tokens.

Therefore:

Access Token:

```text
Every API request
```

Refresh Token:

```text
Only when Access Token expires
```

---

# JWT Payload

Access Token:

```json
{
    "sub": "user_id",
    "email": "abc@gmail.com",
    "type": "access",
    "exp": "..."
}
```

Refresh Token:

```json
{
    "sub": "user_id",
    "type": "refresh",
    "exp": "..."
}
```

---

# Why include "type"?

Imagine someone sends an Access Token to:

```http
POST /auth/refresh
```

Without checking the token type, the server might incorrectly issue a new Access Token.

Adding:

```json
"type": "access"
```

and

```json
"type": "refresh"
```

allows the server to distinguish between the two.

---

# JWTHelper Responsibilities

Instead of one generic method:

```python
encode(payload)
```

Create dedicated methods:

```python
create_access_token()

create_refresh_token()

decode_access_token()

decode_refresh_token()
```

Advantages:

- Automatically sets token type
- Automatically sets expiration
- Prevents mistakes
- Cleaner service layer

---

# Access Token Creation

Responsibilities:

- Copy payload
- Add:

```python
"type": "access"
```

- Add expiration
- Encode JWT

---

# Refresh Token Creation

Responsibilities:

- Copy payload
- Add:

```python
"type": "refresh"
```

- Add longer expiration
- Encode JWT

---

# Token Validation

Access Token:

```python
payload = decode(token)

if payload.get("type") != "access":
    raise HTTPException(...)
```

Refresh Token:

```python
payload = decode(token)

if payload.get("type") != "refresh":
    raise HTTPException(...)
```

Using `payload.get()` avoids `KeyError` if the claim is missing.

---

# Login Flow

```text
Login Request
      │
      ▼
Find User
      │
      ▼
Verify Password
      │
      ▼
Create Access Token
      │
      ▼
Create Refresh Token
      │
      ▼
Return Both Tokens
```

Response:

```json
{
    "access_token": "...",
    "refresh_token": "...",
    "token_type": "bearer"
}
```

---

# Refresh Endpoint

Endpoint:

```http
POST /auth/refresh
```

Request:

```json
{
    "refresh_token": "..."
}
```

Flow:

```text
Receive Refresh Token
        │
        ▼
Decode Refresh Token
        │
        ▼
Verify token type
        │
        ▼
Extract sub
        │
        ▼
Find User in Database
        │
        ▼
Generate NEW Access Token
        │
        ▼
Return Access Token
```

Response:

```json
{
    "access_token": "...",
    "token_type": "bearer"
}
```

---

# Why query the database again?

Even if the Refresh Token is valid:

```text
User logs in

↓

Refresh Token created

↓

Admin deletes user

↓

User sends Refresh Token
```

The token is still valid.

However, the user no longer exists.

Always verify that the user still exists in the database before issuing a new Access Token.

The database is the source of truth.

---

# Clean Architecture

## Router

Responsibilities:

- Receive request
- Call service
- Return response

---

## Service

Responsibilities:

- Decode Refresh Token
- Find user
- Generate new Access Token

---

## Repository

Responsibilities:

- Database operations only

---

## JWTHelper

Responsibilities:

- Create Access Token
- Create Refresh Token
- Decode JWT
- Validate Access Token
- Validate Refresh Token

---

# Configuration

Recommended:

```env
JWT_SECRET_KEY=your-secret

JWT_ALGORITHM=HS256

JWT_ACCESS_TOKEN_EXPIRY_MINUTES=15

JWT_REFRESH_TOKEN_EXPIRY_DAYS=30
```

---

# Refresh Token Flow Diagram

```text
                  Login
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 Access Token             Refresh Token
   (15 min)                 (30 days)
        │
        ▼
Protected APIs
        │
        ▼
Expired
        │
        ▼
POST /auth/refresh
        │
        ▼
Verify Refresh Token
        │
        ▼
Find User
        │
        ▼
Create NEW Access Token
        │
        ▼
Return New Access Token
```

---

# Key Takeaways

- Use **Access Tokens** for authentication.
- Use **Refresh Tokens** only to generate new Access Tokens.
- Access Tokens should expire quickly.
- Refresh Tokens should have a longer lifetime.
- Include a `"type"` claim to distinguish token types.
- Verify the token type before using it.
- Always check that the user still exists in the database.
- Keep JWT-related logic inside `JWTHelper`.
- Keep routers thin and move business logic to the service layer.
- Returning both tokens during login provides a secure and seamless user experience.