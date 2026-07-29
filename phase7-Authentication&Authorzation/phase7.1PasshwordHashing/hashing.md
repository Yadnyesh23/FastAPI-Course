# Phase 7.1 — Password Hashing (bcrypt)

## Why Should We Hash Passwords?

Passwords should **never** be stored in plain text.

If a database is compromised and passwords are stored as plain text, an attacker can immediately access every user's password.

Many users reuse the same password across multiple platforms (Email, GitHub, Banking, Social Media), making plain-text storage extremely dangerous.

**Bad Example**

| Email | Password |
|--------|----------|
| yadnyesh@gmail.com | myPassword123 |
| kevin@gmail.com | hello123 |

If the database leaks, every password is exposed.

---

# What is Password Hashing?

Password hashing is the process of converting a password into a fixed-length, irreversible string using a **hashing algorithm**.

```
Password
    │
    ▼
Hash Function
    │
    ▼
Hashed Password
```

Example:

```
hello123
    │
    ▼
$2b$12$B8xL9K...
```

Only the hashed password is stored in the database.

---

# Properties of Hashing

- One-way process
- Cannot be reversed (decrypted)
- Same input produces the same output **only if the same salt is used**
- Used for password storage

---

# Hashing vs Encryption

| Hashing | Encryption |
|----------|------------|
| One-way process | Two-way process |
| Cannot be decrypted | Can be decrypted using a key |
| Used for password storage | Used for protecting sensitive data |
| Used for verification | Used for recovering original data |

### Easy Way to Remember

- **Hashing → Verify**
- **Encryption → Recover**

---

# How Does Login Work?

Since hashes cannot be decrypted, the server never retrieves the original password.

Instead, during login:

1. User enters their password.
2. Server hashes the entered password using the same algorithm.
3. Server compares it with the stored hash.
4. If they match, authentication succeeds.

```
User Password
      │
      ▼
Hash Again
      │
      ▼
Compare With Stored Hash
      │
   Match?
   /    \
 Yes     No
 │        │
Login   Invalid Password
```

---

# Why Not SHA256?

Algorithms like:

- MD5
- SHA1
- SHA256

are **very fast**.

An attacker can try millions or even billions of password guesses per second using modern GPUs.

Passwords require a **slow hashing algorithm** to make brute-force attacks expensive.

Common password hashing algorithms:

- bcrypt ✅
- Argon2 ✅
- scrypt ✅

In this course, we use **bcrypt** (or an equivalent password hashing implementation such as `pwdlib`) because it is specifically designed for password security.

---

# What is Salt?

A **salt** is a randomly generated value that is combined with the password before hashing.

Purpose:

- Prevents identical passwords from producing identical hashes.
- Protects against rainbow table attacks.
- Makes password cracking significantly harder.

Without Salt:

```
User A
Password: hello123
Hash: ABC123

User B
Password: hello123
Hash: ABC123
```

Both hashes are identical.

---

With Salt:

```
User A
Password + Salt A
        │
        ▼
Hash X82KD...

User B
Password + Salt B
        │
        ▼
Hash P91LM...
```

Even though both users have the same password, their hashes are completely different.

---

# Does bcrypt Handle Salt Automatically?

Yes.

bcrypt automatically:

- Generates a random salt
- Combines the password with the salt
- Hashes the password
- Stores the salt inside the final hash

During verification, bcrypt automatically extracts the salt from the stored hash.

No manual salt management is required.

---

# Authentication Flow

## Registration

```
User Password
      │
      ▼
Hash Password
      │
      ▼
Store Hash in Database
```

---

## Login

```
User Password
      │
      ▼
Hash & Verify
      │
      ▼
Compare With Stored Hash
      │
      ▼
Authentication Success / Failure
```

---

# Practical Implementation

## Install Library

```bash
uv add pwdlib
```

---

## Security Utility

```python
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)
```

---

## Update User Model

```python
password: Mapped[str] = mapped_column(
    String(255),
    nullable=False
)
```

---

## Update Request Schema

```python
class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
```

---

## Hash Before Saving

```python
hashed_password = hash_password(request.password)

user = UserModel(
    name=request.name,
    email=request.email,
    password=hashed_password
)
```

Only the hashed password is stored in the database.

---

## Verify During Login

```python
if not verify_password(
    request.password,
    user.password
):
    raise HTTPException(...)
```

---

# Best Practices

- Never store plain-text passwords.
- Never log user passwords.
- Always hash passwords before saving them.
- Use a password hashing algorithm such as bcrypt or Argon2.
- Never implement your own hashing algorithm.
- Store only the hashed password in the database.
- Always verify passwords using the hashing library instead of comparing plain-text passwords.

---

# Key Takeaways

- Passwords should never be stored in plain text.
- Hashing converts a password into a one-way, irreversible value.
- Hashes cannot be decrypted.
- Login works by hashing the entered password and comparing it with the stored hash.
- Password hashing algorithms (bcrypt, Argon2, scrypt) are intentionally slow to resist brute-force attacks.
- Salt ensures that identical passwords produce different hashes.
- bcrypt automatically generates and manages salts.
- Password hashing should be performed **before** storing user data in the database.
- Password verification should always use the hashing library's verify function.

---

