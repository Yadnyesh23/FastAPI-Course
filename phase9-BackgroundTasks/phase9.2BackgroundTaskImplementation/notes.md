# Phase 9.2 — FastAPI BackgroundTasks Implementation

## 1. Import `BackgroundTasks`

FastAPI provides `BackgroundTasks` for running small tasks after the main request processing.

```python
from fastapi import FastAPI, BackgroundTasks
```

Create the FastAPI application:

```python
app = FastAPI()
```

## 2. Create the Background Task Function

First, define the function that should run in the background.

```python
def send_email(email: str, message: str):
    print(f"To: {email}")
    print(f"Message: {message}")
```

This function contains the work that we want to execute in the background.

## 3. Inject `BackgroundTasks` into the Endpoint

Add `BackgroundTasks` as a parameter in the endpoint.

```python
@app.post("/create-user")
def create_user(background_tasks: BackgroundTasks):
    ...
```

FastAPI automatically provides the `BackgroundTasks` object.

## 4. Add a Background Task

Use:

```python
background_tasks.add_task()
```

### Syntax

```python
background_tasks.add_task(function, *args, **kwargs)
```

### Example

```python
background_tasks.add_task(
    send_email,
    "yadnyesh@gmail.com",
    "Welcome to our platform"
)
```

This means:

```python
send_email(
    "yadnyesh@gmail.com",
    "Welcome to our platform"
)
```

The function will run as a background task.

## 5. Complete Example

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


def send_email(email: str, message: str):
    print(f"To: {email}")
    print(f"Message: {message}")


@app.post("/create-user")
def create_user(background_tasks: BackgroundTasks):

    # Main request work
    print("User saved in DB")

    # Schedule background task
    background_tasks.add_task(
        send_email,
        "yadnyesh@gmail.com",
        "Welcome to our platform"
    )

    print("Response is ready")

    return {
        "message": "User created successfully"
    }
```

## 6. Execution Flow

The conceptual flow is:

```text
Client
  │
  │ POST /create-user
  ▼
FastAPI
  │
  ├── Save user
  │
  ├── Add send_email() as background task
  │
  ├── Prepare response
  │
  ▼
Response ───────────────► Client
  │
  ▼
Background Task
  │
  ▼
send_email()
```

The important idea is that the email does not need to be completed before the client receives the response.

## 7. Simulating a Slow Background Task

To understand the behavior clearly, simulate a slow operation using `time.sleep()`.

```python
from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()


def send_email(email: str, message: str):

    print("Background task started...")

    # Simulate a slow operation
    time.sleep(5)

    print(f"To: {email}")
    print(f"Message: {message}")

    print("Background task completed.")


@app.post("/create-user")
def create_user(background_tasks: BackgroundTasks):

    print("User saved in DB")

    background_tasks.add_task(
        send_email,
        "yadnyesh@gmail.com",
        "Welcome to our platform"
    )

    print("Response is ready")

    return {
        "message": "User created successfully"
    }
```

## 8. Expected Execution

When the endpoint is called:

```text
User saved in DB
Response is ready
Background task started...
```

The client receives:

```json
{
  "message": "User created successfully"
}
```

Then the background task continues.

After five seconds:

```text
To: yadnyesh@gmail.com
Message: Welcome to our platform
Background task completed.
```

## 9. Passing Arguments

Arguments can be passed directly to `add_task()`.

```python
def send_email(email: str, message: str):
    print(email)
    print(message)
```

Add the task:

```python
background_tasks.add_task(
    send_email,
    "user@gmail.com",
    "Welcome!"
)
```

FastAPI will execute the equivalent of:

```python
send_email(
    "user@gmail.com",
    "Welcome!"
)
```

## 10. Passing Multiple Arguments

Example:

```python
def send_notification(
    username: str,
    email: str,
    message: str
):
    print(username)
    print(email)
    print(message)
```

Add the task:

```python
background_tasks.add_task(
    send_notification,
    "Yadnyesh",
    "yadnyesh@gmail.com",
    "Welcome!"
)
```

## 11. Keyword Arguments

Keyword arguments can also be used.

```python
background_tasks.add_task(
    send_notification,
    username="Yadnyesh",
    email="yadnyesh@gmail.com",
    message="Welcome!"
)
```

This executes:

```python
send_notification(
    username="Yadnyesh",
    email="yadnyesh@gmail.com",
    message="Welcome!"
)
```

## 12. Important Mistake

### Incorrect

```python
background_tasks.add_task(
    send_email(email)
)
```

This calls the function immediately.

```python
send_email(email)
```

means:

> Execute the function now.

### Correct

```python
background_tasks.add_task(
    send_email,
    email
)
```

Here:

- `send_email` is passed as the function.
- `email` is passed as its argument.

Remember:

```text
send_email      → function reference
send_email()    → execute function
```

## 13. Multiple Background Tasks

Multiple tasks can be added to the same request.

```python
@app.post("/register")
def register(background_tasks: BackgroundTasks):

    background_tasks.add_task(
        send_email,
        "user@gmail.com",
        "Welcome!"
    )

    background_tasks.add_task(
        write_log,
        "User registered"
    )

    background_tasks.add_task(
        send_notification,
        "user@gmail.com",
        "Account created"
    )

    return {
        "message": "Registration successful"
    }
```

Conceptually:

```text
                FastAPI
                   │
                   ▼
             Process Request
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
    Send Email   Write Log   Notification
        │          │          │
        └──────────┼──────────┘
                   ▼
               Response
```

## 14. Real-World Example — File Upload

`BackgroundTasks` can be useful after uploading a file.

### Flow

```text
Upload File
     ↓
Validate File
     ↓
Save File
     ↓
Return Response
     ↓
Write Upload Log
```

### Implementation

```python
def log_upload(filename: str):
    with open("uploads.log", "a") as file:
        file.write(
            f"Uploaded: {filename}\n"
        )


@app.post("/upload")
def upload(
    file: UploadFile,
    background_tasks: BackgroundTasks
):

    result = upload_file(file)

    background_tasks.add_task(
        log_upload,
        result["stored_filename"]
    )

    return result
```

The logging operation does not need to delay the upload response.

## 15. BackgroundTasks with Dependencies

`BackgroundTasks` can also be used with FastAPI dependencies.

```python
from fastapi import Depends


def get_current_user():
    return {
        "id": 123,
        "email": "user@gmail.com"
    }


def create_audit_log(
    user_id: int,
    action: str
):
    print(
        f"User {user_id}: {action}"
    )


@app.post("/profile")
def update_profile(
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user)
):

    # Main operation
    update_user_profile(user["id"])

    # Background operation
    background_tasks.add_task(
        create_audit_log,
        user["id"],
        "Updated profile"
    )

    return {
        "message": "Profile updated"
    }
```

This is useful for:

```text
Authenticated User
       ↓
Main Operation
       ↓
Response
       ↓
Audit Log
```

## 16. Async Background Task

The background function can also be asynchronous.

```python
async def send_notification(email: str):
    await some_async_operation()
```

Add the task:

```python
background_tasks.add_task(
    send_notification,
    email
)
```

FastAPI and Starlette can handle both synchronous and asynchronous tasks:

```python
def task():
    ...
```

```python
async def task():
    ...
```

## 17. BackgroundTasks Are Not Celery

This is very important.

`BackgroundTasks` is a simple mechanism provided by FastAPI and Starlette.

It is **not** the same as a distributed task queue.

### BackgroundTasks

```text
FastAPI
   │
   └── BackgroundTasks
           │
           ▼
        Function
```

### Celery

```text
FastAPI
   ↓
Redis
   ↓
Celery
   ↓
Worker
```

`BackgroundTasks` is associated with the FastAPI application process.

## 18. Limitations

### 18.1 No Dedicated Persistent Queue

`BackgroundTasks` does not provide a proper external task queue.

There is no Redis-backed queue by default:

```text
FastAPI
   ↓
Redis
   ↓
Queue
```

### 18.2 No Built-in Reliable Retries

Suppose an email fails:

```text
Send Email
    ↓
Failed
```

`BackgroundTasks` does not automatically provide:

```text
Retry 1
   ↓
Retry 2
   ↓
Retry 3
```

For advanced retry handling, use a task queue such as Celery.

### 18.3 Tasks Can Be Lost

If the FastAPI application process crashes, the background task may be lost.

```text
FastAPI ❌
   ↓
Background Task ❌
```

### 18.4 Not Designed for Long-Running Jobs

Avoid using `BackgroundTasks` for tasks such as:

- Video processing.
- Large file conversion.
- Large report generation.
- Long-running data processing.

### 18.5 Not Designed for Distributed Workers

Do not use `BackgroundTasks` as a replacement for distributed workers:

```text
Worker 1
Worker 2
Worker 3
Worker 4
```

For distributed workers, use a task queue.

## 19. When Not to Use BackgroundTasks

Avoid `BackgroundTasks` when the task is:

- Long-running, such as video processing or large report generation.
- Critical, such as payment processing or financial operations.
- Required to support reliable retries.
- Required to run on a schedule.
- Required to use multiple workers.
- Required to support advanced failure handling.

### Examples of Scheduled Tasks

```text
Run tomorrow at 10 AM
```

```text
Run every hour
```

### Suitable Alternatives

Consider using:

```text
Celery + Redis
```

## 20. BackgroundTasks vs Celery

| Feature | BackgroundTasks | Celery |
|---|---:|---:|
| Simple tasks | ✅ | ✅ |
| Small emails | ✅ | ✅ |
| Logging | ✅ | ✅ |
| Notifications | ✅ | ✅ |
| Task queue | ❌ | ✅ |
| Redis integration | ❌ | ✅ |
| Built-in retries | ❌ | ✅ |
| Multiple workers | ❌ | ✅ |
| Distributed processing | ❌ | ✅ |
| Long-running jobs | ❌ Not ideal | ✅ |
| Scheduling | ❌ | ✅ |
| Advanced failure handling | ❌ | ✅ |

## 21. Rule of Thumb

Use `BackgroundTasks` for:

```text
Small + Simple + Non-critical
            ↓
      BackgroundTasks
```

Use Celery with Redis for:

```text
Heavy + Long-running + Reliable
            ↓
       Celery + Redis
```

## 22. SeatLock Example

Suppose a user reserves a seat for 10 minutes.

```text
User
 ↓
Reserve Seat
 ↓
Payment
```

If payment is not completed:

```text
Reservation Expires
       ↓
Release Seat
```

### Simple Prototype

For a simple prototype, FastAPI `BackgroundTasks` might be enough.

### Production-Style System

```text
FastAPI
   ↓
Redis
   ↓
Celery
   ↓
Worker
   ↓
Check Expired Reservations
   ↓
Release Seats
```

This architecture allows us to later add:

- Retries.
- Task queues.
- Multiple workers.
- Scheduling.
- Failure handling.

## 23. Complete Mental Model

### BackgroundTasks

```text
                FastAPI Request
                       │
                       ▼
                Process Request
                       │
                       ▼
              Add Background Task
                       │
                       ▼
                    Response
                       │
                       ▼
                 Execute Task
```

### Celery + Redis

```text
                 FastAPI
                    │
                    ▼
               Submit Task
                    │
                    ▼
                  Redis
               Task Queue
                    │
                    ▼
              Celery Worker
                    │
                    ▼
               Execute Task
```

## 24. Key Takeaways

`BackgroundTasks` is FastAPI's built-in mechanism for simple background work.

Import it using:

```python
from fastapi import BackgroundTasks
```

Inject it into the endpoint:

```python
def endpoint(background_tasks: BackgroundTasks):
    ...
```

Add a task using:

```python
background_tasks.add_task(
    function,
    arguments
)
```

Pass the function itself, not the result of calling it.

### Correct

```python
background_tasks.add_task(
    send_email,
    email
)
```

### Incorrect

```python
background_tasks.add_task(
    send_email(email)
)
```

Multiple background tasks can be added to one request.

Background tasks can receive positional and keyword arguments.

### Suitable Use Cases

`BackgroundTasks` is suitable for:

- Sending emails.
- Logging.
- Sending notifications.
- Small cleanup tasks.
- Small post-processing tasks.

### Unsuitable Use Cases

Avoid `BackgroundTasks` for:

- Long-running jobs.
- Critical operations.
- Large workloads.
- Jobs requiring reliable retries.
- Distributed processing.
- Scheduled jobs.

### Advanced Background Processing

```text
FastAPI
   ↓
Redis
   ↓
Celery
   ↓
Workers
```

## 25. One-Line Mental Model

> `BackgroundTasks` means:  
> “Run this small piece of work after the request is processed, without making the client wait for it.”