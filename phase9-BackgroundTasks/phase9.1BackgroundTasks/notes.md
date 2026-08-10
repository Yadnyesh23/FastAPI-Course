# Phase 9.1 — Background Jobs Fundamentals

## 1. What is a Background Job?

A **background job** is a task that the application starts but does not need to complete before sending the response to the client.

### Normal request

```text
Client
  ↓
FastAPI
  ↓
Perform task
  ↓
Response
```

The client waits for the task to finish.

### Background job

```text
Client
  ↓
FastAPI
  ├──────────────→ Response
  │
  └──────────────→ Background Job
                         ↓
                       Task
```

The client receives the response without waiting for the background task to finish.

### Examples

- Sending emails
- Sending notifications
- Generating small reports
- Writing audit logs
- Cleaning temporary files
- Small image-processing tasks

## 2. Why Do We Need Background Processing?

The main reason is to reduce response time and prevent unnecessary work from delaying the user.

Suppose an endpoint performs:

```text
Create user        → 50 ms
Send email         → 2 sec
Generate report    → 5 sec
Update analytics   → 1 sec
```

If everything is synchronous:

```text
50 ms + 2 sec + 5 sec + 1 sec
≈ 8 seconds
```

The user waits for approximately 8 seconds.

Instead:

```text
Request
   ↓
Create user
   ↓
Response
   ↓
Background processing
   ├── Send email
   ├── Generate report
   └── Update analytics
```

The user may receive the response much faster.

## 3. Synchronous Processing

In synchronous processing, the request waits for the operation to complete before the response is returned.

```text
Request
   ↓
Work
   ↓
Wait
   ↓
Work completed
   ↓
Response
```

Example:

```python
@app.post("/report")
def generate_report():
    report = generate_report()
    return report
```

If the report takes 20 seconds:

```text
Request → 20 seconds → Response
```

The client must wait.

## 4. Background Processing

In background processing, the application starts the work without making the client wait for its completion.

```text
Request
   ↓
Start task
   ↓
Response
   ↓
Background work continues
```

Example:

```text
User registers
      ↓
Create account
      ↓
Return response
      ↓
Send welcome email
```

The email does not need to be sent before the registration response is returned.

## 5. Blocking

A blocking operation prevents the current execution flow from continuing until the operation finishes.

Example:

```python
import time

def task():
    time.sleep(5)
```

Flow:

```text
Start
  ↓
sleep(5)
  ↓
WAITING
  ↓
5 seconds
  ↓
Continue
```

During the blocking operation, that execution context cannot continue with other work.

## 6. Non-Blocking

A non-blocking operation allows the system to perform other work while waiting for an I/O operation.

Example:

```python
import asyncio

async def task():
    await asyncio.sleep(5)
```

Conceptually:

```text
Start
  ↓
await
  │
  ├────────→ Other work can run
  │
  └────────→ Resume when operation completes
```

The important concept is:

> **await = give control back while waiting for an async operation**

## 7. Async vs Background Processing

These concepts are related but not the same.

### Async / Non-Blocking

Async is about **how** the program waits.

Example:

```python
response = await client.get(url)
```

The client may still be waiting for the final response.

While waiting for the network operation, the event loop can handle other work.

```text
Request
   ↓
Async I/O
   ↓
await
   ↓
Other requests can be handled
   ↓
I/O completes
   ↓
Response
```

### Background Processing

Background processing is about **whether** the client needs to wait for the work at all.

```text
Request
   ↓
Start background task
   ↓
Response ─────────→ Client
   ↓
Task continues
```

**Remember:**

- **Async** = How we wait.
- **Background** = Whether the client waits.

## 8. Async Does NOT Automatically Mean Background

Consider:

```python
@app.get("/data")
async def get_data():
    response = await client.get("https://example.com")
    return response.json()
```

This is asynchronous.

But the client still waits for:

```text
External API
     ↓
Response
     ↓
FastAPI response
```

Therefore:

> **Async ≠ Background**

## 9. FastAPI BackgroundTasks

FastAPI provides `BackgroundTasks` for simple background operations.

Example:

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def send_email(email: str):
    print(f"Sending email to {email}")


@app.post("/register")
def register(
    email: str,
    background_tasks: BackgroundTasks
):
    # Main request work
    create_user(email)

    # Schedule background task
    background_tasks.add_task(send_email, email)

    return {
        "message": "Registration successful"
    }
```

Important line:

```python
background_tasks.add_task(send_email, email)
```

FastAPI schedules the task to run after the main request processing has completed.

## 10. When to Use BackgroundTasks

`BackgroundTasks` is suitable for small and simple tasks.

### Good use cases

**Email**

```text
Register
   ↓
Save user
   ↓
Response
   ↓
Send email
```

**Notifications**

```text
Order created
   ↓
Response
   ↓
Send notification
```

**Logging**

```text
Request
   ↓
Response
   ↓
Write audit log
```

**Cleanup**

```text
Delete resource
   ↓
Response
   ↓
Delete temporary files
```

## 11. When NOT to Use BackgroundTasks

Do not use FastAPI `BackgroundTasks` for heavy, long-running, or highly reliable jobs.

Avoid it for:

- Video processing
- Large file processing
- Large report generation
- ML model training
- Thousands of emails
- Long-running jobs
- Critical payment processing
- Jobs requiring reliable retries
- Jobs that must survive server crashes
- Large distributed workloads

## 12. Limitation of BackgroundTasks

FastAPI `BackgroundTasks` runs as part of the application process.

Conceptually:

```text
FastAPI
   │
   └── Background Task
           │
           ▼
         Task
```

If the application process crashes:

```text
FastAPI ❌
   │
   └── Background Task ❌
```

The task may be lost.

It does not provide the same reliability as a dedicated task queue.

## 13. Task Queues

For heavy and reliable background processing, we can use a task queue.

Architecture:

```text
FastAPI
   ↓
Task Queue
   ↓
Worker
   ↓
Execute Task
```

A common architecture is:

```text
FastAPI
   ↓
Redis
   ↓
Celery Worker
   ↓
Execute Task
```

This allows the API server and background workers to be separated.

## 14. Celery + Redis

### Redis

Redis can act as the message broker where tasks are placed into a queue.

### Celery

Celery manages background task execution using workers.

Architecture:

```text
             FastAPI
                │
                │ Submit task
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

Example:

```text
Generate report
       ↓
FastAPI
       ↓
Redis
       ↓
Celery Worker
       ↓
Generate report
```

## 15. Why Celery + Redis?

Compared with simple `BackgroundTasks`, Celery provides features such as:

- Dedicated workers
- Task queues
- Retries
- Scheduling
- Multiple workers
- Distributed processing
- Failure handling
- Task monitoring
- Better support for long-running jobs

## 16. Background Processing Decision Flow

Use this mental model:

```text
                Is the client required to wait?
                          │
                ┌─────────┴─────────┐
               YES                  NO
                │                    │
                ▼                    ▼
           Normal request      Background work
                │                    │
         Is waiting I/O?       Simple/short?
                │                    │
          ┌─────┴─────┐         ┌────┴────┐
         YES           NO       YES        NO
          │             │        │          │
          ▼             ▼        ▼          ▼
       async          sync   Background   Celery
                            Tasks          + Redis
```

## 17. Quick Comparison

| Concept | Main Purpose |
|---|---|
| Synchronous | Wait for operation to finish |
| Async | Avoid blocking while waiting for I/O |
| Background Task | Execute small work without making client wait |
| Task Queue | Store jobs until workers can process them |
| Celery | Distributed task processing |
| Redis | Can act as Celery's message broker |

## 18. Key Differences

### Synchronous

```text
Request → Work → Response
```

> "Do this and give me the result."

### Async

```text
Request → Async I/O → await → Response
```

> "I'm waiting, but don't block the event loop."

### Background

```text
Request → Response
             ↓
            Work
```

> "The client doesn't need to wait."

### Celery

```text
Request → Queue → Worker → Work
```

> "Put this job into a reliable worker-based processing system."

## 19. SeatLock Example

In our future SeatLock project, a user may reserve a seat for 10 minutes.

```text
User
 ↓
Reserve Seat
 ↓
Payment
```

If payment isn't completed:

```text
Reservation expires
       ↓
Release seat
```

This is a background-processing problem.

For a small prototype:

> FastAPI `BackgroundTasks` could be used.

But for a production-style system:

```text
FastAPI
   ↓
Redis
   ↓
Celery
   ↓
Check expired reservations
   ↓
Release seats
```

This is more appropriate.

## 20. Key Takeaways

- Background jobs allow work to continue without making the client wait.
- Synchronous processing waits for the operation before responding.
- Async programming is mainly about avoiding blocking while waiting for I/O.
- Async and background processing are different concepts.
- FastAPI's `BackgroundTasks` is useful for small, simple tasks.
- `BackgroundTasks` is not ideal for heavy, long-running, critical, or highly reliable jobs.
- For more advanced background processing, use: **Celery + Redis**
- A task queue separates the API request from task execution.
- Celery workers execute tasks independently from the FastAPI request.
- Background jobs are especially useful for:
  - Emails
  - Notifications
  - Reports
  - Cleanup
  - File processing
  - Scheduled jobs
  - Expiring reservations