# Phase 7.7 - Middleware (FastAPI)

---

# What is Middleware?

Middleware is a piece of code that executes **before and after every HTTP request**.

It sits between the **client** and your FastAPI application.

```text
Client
   │
   ▼
Middleware
   │
   ▼
FastAPI Route
   │
   ▼
Middleware
   │
   ▼
Client
```

Instead of writing common logic inside every API, we write it once in a middleware.

Examples:

- Logging requests
- Measuring response time
- CORS
- Compression
- Rate Limiting
- Maintenance Mode
- Security Headers

---

# Why do we need Middleware?

Imagine an application having 100 APIs.

```text
GET  /users
POST /users
GET  /notes
POST /notes
DELETE /notes/{id}
...
```

Suppose we want to

- Measure response time
- Log every request

Without middleware we would have to write the same code inside every route.

```python
@router.get("/users")
async def get_users():
    start = time.perf_counter()
    ...
```

```python
@router.post("/notes")
async def create_note():
    start = time.perf_counter()
    ...
```

This is repetitive and difficult to maintain.

Middleware solves this problem by running automatically for every request.

---

# Request Lifecycle

The complete request lifecycle in FastAPI is

```text
Client
   │
   ▼
Middleware (Before Request)
   │
   ▼
Dependencies
   │
   ▼
Route
   │
   ▼
Service
   │
   ▼
Repository
   │
   ▼
Database
   │
   ▼
Response
   │
   ▼
Middleware (After Response)
   │
   ▼
Client
```

Notice that middleware runs twice:

- Before the request reaches the route.
- After the route returns a response.

---

# Custom Middleware

FastAPI provides

```python
@app.middleware("http")
```

to create custom middleware.

Structure:

```python
@app.middleware("http")
async def my_middleware(request: Request, call_next):

    # Before request

    response = await call_next(request)

    # After request

    return response
```

---

# Understanding call_next()

The most important line inside middleware is

```python
response = await call_next(request)
```

Think of it as:

> Continue processing this request.

Execution flow:

```text
Middleware
      │
      ▼
call_next(request)
      │
      ▼
Dependency
      │
      ▼
Route
      │
      ▼
Service
      │
      ▼
Repository
      │
      ▼
Database
      │
      ▼
Response
```

After the response is generated, execution returns back to the middleware.

---

# request Object

The incoming request is available through

```python
request
```

Useful properties:

```python
request.method
```

Returns

```text
GET
POST
PUT
DELETE
PATCH
```

---

```python
request.url.path
```

Returns

```text
/auth/login

/user/me

/notes
```

---

```python
request.headers
```

Returns request headers.

---

```python
request.client.host
```

Returns client IP address.

---

# response Object

The response object is available only after

```python
await call_next(request)
```

Useful property:

```python
response.status_code
```

Examples:

```text
200

201

400

401

404

500
```

---

# Process Time Middleware

Purpose:

Measure how long every request takes.

Implementation:

```python
import time

from fastapi import FastAPI, Request

def register_middlewares(app: FastAPI):

    @app.middleware("http")
    async def process_time_middleware(
        request: Request,
        call_next,
    ):

        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        response.headers["X-Process-Time"] = f"{process_time:.6f}"

        return response
```

---

# Why use time.perf_counter()?

Python provides

```python
time.time()
```

and

```python
time.perf_counter()
```

For benchmarking and response time measurement,

```python
time.perf_counter()
```

is preferred because

- Higher precision
- Monotonic (never goes backwards)
- Ideal for measuring elapsed time

---

# X-Process-Time Header

The middleware adds

```text
X-Process-Time
```

to every response.

Example:

```text
X-Process-Time: 0.018245
```

Meaning

```text
18.245 milliseconds
```

---

# Request Logging Middleware

Purpose:

Log every incoming request.

Example implementation:

```python
import time

from fastapi import FastAPI, Request
from loguru import logger

def register_middlewares(app: FastAPI):

    @app.middleware("http")
    async def logging(
        request: Request,
        call_next,
    ):

        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        logger.info(
            f"{request.method} "
            f"{request.url.path} -> "
            f"{response.status_code} "
            f"({process_time * 1000:.2f} ms)"
        )

        response.headers["X-Process-Time"] = f"{process_time:.6f}"

        return response
```

Example log:

```text
GET /user/me -> 200 (12.41 ms)

POST /auth/login -> 200 (21.53 ms)

GET /notes -> 401 (3.28 ms)
```

---

# Why use Loguru?

Instead of

```python
print(...)
```

use

```python
logger.info(...)
```

Advantages:

- Log levels
- Better formatting
- Log files
- Rotation
- Easier production debugging

---

# Built-in Middleware

FastAPI already provides several middleware classes.

Examples:

- CORSMiddleware
- GZipMiddleware
- HTTPSRedirectMiddleware
- TrustedHostMiddleware

They are added using

```python
app.add_middleware(...)
```

instead of

```python
@app.middleware("http")
```

---

# CORS Middleware

CORS stands for

> Cross-Origin Resource Sharing

It allows browsers to access your backend from trusted frontend origins.

---

# What is an Origin?

An origin consists of

```text
Protocol
+
Domain
+
Port
```

Example:

```text
http://localhost:8000
```

Protocol

```text
http
```

Domain

```text
localhost
```

Port

```text
8000
```

Changing any one of these creates a different origin.

Examples:

```text
http://localhost:3000
```

Different port.

---

```text
https://localhost:8000
```

Different protocol.

---

```text
http://127.0.0.1:8000
```

Different host.

---

# Same Origin

```text
http://localhost:8000

↓

http://localhost:8000
```

Allowed.

---

# Cross Origin

```text
http://localhost:3000

↓

http://localhost:8000
```

Different origin.

Browser blocks it by default.

---

# Who blocks CORS?

Not FastAPI.

Not PostgreSQL.

Not Uvicorn.

The **Browser** blocks cross-origin JavaScript requests if the required CORS headers are missing.

This is why:

```text
Postman -> Works

Swagger -> Works

React -> CORS Error
```

---

# Why does CORS exist?

CORS is a browser security feature.

It prevents malicious websites from making unauthorized cross-origin requests through the user's browser.

Without CORS, a malicious website could try to access another website's resources using the user's authenticated session.

---

# Configuring CORSMiddleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)
```

---

# Understanding the Parameters

## allow_origins

Allowed frontend origins.

Development:

```python
allow_origins=[
    "http://localhost:3000"
]
```

Production:

```python
allow_origins=[
    "https://teslearn.com"
]
```

Avoid using

```python
allow_origins=["*"]
```

in production.

---

## allow_credentials

Allows cookies and Authorization headers.

```python
allow_credentials=True
```

Required for authenticated applications.

---

## allow_methods

Allowed HTTP methods.

```python
allow_methods=["*"]
```

Allows:

- GET
- POST
- PUT
- PATCH
- DELETE
- OPTIONS

---

## allow_headers

Allowed request headers.

```python
allow_headers=["*"]
```

---

# Middleware vs Dependency

| Middleware | Dependency |
|------------|------------|
| Runs for every request | Runs only where attached |
| Executes before and after route | Executes before route only |
| Good for logging | Good for authentication |
| Good for timing | Good for DB session |
| Good for CORS | Good for permissions |

---

# Custom Middleware vs Built-in Middleware

Custom Middleware:

```python
@app.middleware("http")
```

Examples:

- Logging
- Response Time
- Custom Headers

---

Built-in Middleware:

```python
app.add_middleware(...)
```

Examples:

- CORS
- GZip
- HTTPS Redirect
- Trusted Host

---

# Middleware Best Practices

- Keep middleware lightweight.
- Do not put business logic inside middleware.
- Use middleware only for request/response level concerns.
- Prefer logging libraries over print().
- Measure execution time using time.perf_counter().
- Keep allowed origins specific in production.
- Combine related middleware (e.g., logging + process time) to avoid duplicate work.

---

# Summary

In this phase, we learned:

- What middleware is
- Request lifecycle
- request and response objects
- call_next()
- Custom middleware
- Process Time Middleware
- Logging Middleware
- Loguru logging
- Built-in middleware
- CORSMiddleware
- Same Origin Policy
- Cross-Origin Resource Sharing (CORS)
- Origin = Protocol + Domain + Port
- Browser's role in enforcing CORS
- Middleware vs Dependency
- Custom vs Built-in Middleware

---

# Project Structure

```text
app/
│
├── api/
├── core/
│   ├── config.py
│   ├── jwt.py
│   ├── security.py
│   └── middleware.py
│
├── models/
├── repository/
├── services/
└── main.py
```

Example `middleware.py`

```python
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger


def register_middlewares(app: FastAPI):

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def logging(
        request: Request,
        call_next,
    ):
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        logger.info(
            f"{request.method} {request.url.path} -> "
            f"{response.status_code} "
            f"({process_time * 1000:.2f} ms)"
        )

        response.headers["X-Process-Time"] = f"{process_time:.6f}"

        return response
```
