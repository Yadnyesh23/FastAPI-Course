# Phase 2.9 – Headers & Cookies

## Objectives

By the end of this phase, you should understand:

- What Headers are
- Why Headers are used
- Request Headers
- Response Headers
- Custom Headers
- Header()
- What Cookies are
- Why Cookies are used
- Cookie()
- Setting Cookies
- Deleting Cookies
- Difference Between Headers and Cookies
- Real-world Authentication Usage

---

# What Are Headers?

Headers are metadata sent along with an HTTP request or response.

Think of them as additional information about the request.

Example:

```http
GET /students

Host: example.com
User-Agent: Chrome
Authorization: Bearer xyz123
```

Headers provide information without being part of the URL or request body.

---

# Why Are Headers Used?

Headers are commonly used for:

- Authentication Tokens
- API Keys
- Content Type
- User Information
- Language Preferences
- Caching Information

Examples:

```http
Authorization: Bearer token
```

```http
Content-Type: application/json
```

```http
Accept-Language: en-US
```

---

# Request Headers

Headers sent by the client to the server.

Example:

```http
GET /profile

Authorization: Bearer abc123
User-Agent: Chrome
```

The server reads these headers and uses the information.

---

# Reading Headers in FastAPI

FastAPI provides:

```python
from fastapi import Header
```

Example:

```python
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/user-agent")
def get_user_agent(
    user_agent: str = Header()
):
    return {
        "user_agent": user_agent
    }
```

FastAPI automatically reads the header value.

---

# Optional Headers

Sometimes headers may not exist.

Example:

```python
from typing import Optional

@app.get("/")
def root(
    user_agent: Optional[str] = Header(
        default=None
    )
):
    return {
        "user_agent": user_agent
    }
```

If the header is missing:

```json
{
  "user_agent": null
}
```

---

# Custom Headers

Developers can create their own headers.

Example:

```http
X-Student-Id: 101
```

Reading it:

```python
@app.get("/student")
def get_student(
    student_id: str = Header(
        alias="X-Student-Id"
    )
):
    return {
        "student_id": student_id
    }
```

---

# Why Use alias= ?

Headers often contain hyphens:

```http
X-API-Key
```

Python variables cannot contain hyphens.

Incorrect:

```python
X-API-Key
```

Correct:

```python
api_key: str = Header(
    alias="X-API-Key"
)
```

FastAPI maps the header to the Python variable.

---

# Common Headers

## Authorization

Used for authentication.

```http
Authorization: Bearer xyz123
```

---

## User-Agent

Information about the client.

```http
User-Agent: Chrome
```

---

## Content-Type

Type of request body.

```http
Content-Type: application/json
```

---

## Accept

Types of responses accepted.

```http
Accept: application/json
```

---

## Host

Target server domain.

```http
Host: example.com
```

---

# Response Headers

Headers can also be sent by the server.

Example:

```python
from fastapi import Response

@app.get("/")
def root(response: Response):

    response.headers["X-App"] = "TesLearn"

    return {
        "message": "Hello"
    }
```

Response:

```http
X-App: TesLearn
```

---

# What Are Cookies?

Cookies are small pieces of data stored inside the user's browser.

Example:

```text
session_id=abc123
```

The browser automatically sends cookies back to the server on future requests.

---

# Why Are Cookies Used?

Cookies are commonly used for:

- Login Sessions
- User Preferences
- Theme Settings
- Language Preferences
- Shopping Carts

Examples:

```text
theme=dark
```

```text
session_id=abc123
```

---

# Reading Cookies

FastAPI provides:

```python
from fastapi import Cookie
```

Example:

```python
from fastapi import Cookie

@app.get("/profile")
def profile(
    session_id: str = Cookie()
):
    return {
        "session_id": session_id
    }
```

Request:

```http
Cookie: session_id=abc123
```

Response:

```json
{
  "session_id": "abc123"
}
```

---

# Optional Cookies

Example:

```python
from typing import Optional

@app.get("/")
def root(
    session_id: Optional[str] = Cookie(
        default=None
    )
):
    return {
        "session_id": session_id
    }
```

---

# Setting Cookies

To create cookies, use the Response object.

Example:

```python
from fastapi import Response

@app.get("/login")
def login(response: Response):

    response.set_cookie(
        key="session_id",
        value="abc123"
    )

    return {
        "message": "Logged in"
    }
```

Browser receives:

```http
Set-Cookie: session_id=abc123
```

and stores it.

---

# Deleting Cookies

Example:

```python
@app.get("/logout")
def logout(response: Response):

    response.delete_cookie(
        key="session_id"
    )

    return {
        "message": "Logged out"
    }
```

The browser removes the cookie.

---

# Authentication Example

Client Request:

```http
Authorization: Bearer xyz123
```

FastAPI:

```python
token: str = Header(
    alias="Authorization"
)
```

The server validates the token and identifies the user.

This forms the basis of JWT Authentication.

---

# Session Example

Login:

```python
response.set_cookie(
    key="session_id",
    value="abc123"
)
```

Browser stores:

```text
session_id=abc123
```

Future requests:

```http
Cookie: session_id=abc123
```

Server identifies the user.

---

# Headers vs Cookies

| Headers | Cookies |
|----------|----------|
| Sent with requests/responses | Stored in browser |
| Used for API communication | Used for sessions/preferences |
| Authorization Tokens | Session IDs |
| Managed by client/server code | Managed automatically by browser |
| Often used in REST APIs | Often used in web applications |

---

# Real TesLearn Examples

## JWT Authentication

Use:

```http
Authorization: Bearer token
```

Stored in:

```text
Header
```

---

## User Theme Preference

Use:

```text
theme=dark
```

Stored in:

```text
Cookie
```

---

## Session Login

Use:

```text
session_id=abc123
```

Stored in:

```text
Cookie
```

---

## API Key

Use:

```http
X-API-Key: abc123
```

Stored in:

```text
Header
```

---

# Common Mistakes

## ❌ Forgetting alias=

Bad:

```python
api_key: str = Header()
```

For:

```http
X-API-Key
```

Better:

```python
api_key: str = Header(
    alias="X-API-Key"
)
```

---

## ❌ Using Cookies for API Keys

Bad:

```text
Cookie: api_key=abc123
```

Better:

```http
X-API-Key: abc123
```

---

## ❌ Storing Authentication Data Incorrectly

JWT Tokens are usually sent using:

```http
Authorization: Bearer token
```

Not query parameters.

---

# Interview Questions

1. What are HTTP Headers?
2. Why are Headers used?
3. What is Header()?
4. What is a custom header?
5. Why is alias= used with headers?
6. What are Cookies?
7. Why are Cookies used?
8. What is Cookie()?
9. How do you set a cookie in FastAPI?
10. How do you delete a cookie?
11. Difference between Headers and Cookies?
12. Where is a cookie stored?

---

# Quick Cheat Sheet

```python
from fastapi import Header
```

Read Headers

---

```python
from fastapi import Cookie
```

Read Cookies

---

```python
from fastapi import Response
```

Set/Delete Cookies

---

```python
Header(alias="X-API-Key")
```

Custom Header

---

```python
response.set_cookie()
```

Create Cookie

---

```python
response.delete_cookie()
```

Delete Cookie

---

# Key Takeaways

- Headers contain metadata about requests and responses.
- Header() is used to read request headers.
- alias= maps header names to Python variables.
- Cookies are small pieces of data stored in the browser.
- Cookie() is used to read cookies.
- Response.set_cookie() creates cookies.
- Response.delete_cookie() removes cookies.
- Headers are commonly used for JWT tokens and API keys.
- Cookies are commonly used for sessions and preferences.
- Headers and Cookies are fundamental to authentication systems.