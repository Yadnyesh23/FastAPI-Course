# Phase 9.3 — Redis Fundamentals

## 1. What is Redis?

Redis stands for **REmote DIctionary Server**.

Redis is an **in-memory data store** that is commonly used for:

- Caching  
- Temporary data  
- Sessions  
- Rate limiting  
- Counters  
- Queues  
- Background jobs  
- Pub/Sub  
- Distributed locks  

Redis primarily stores data in **RAM**, which makes it extremely fast for read/write operations.

---

## 2. Why is Redis Fast?

Traditional database:

```text
Application
     │
     ▼
PostgreSQL
     │
     ▼
    Disk
```

Redis:

```text
Application
     │
     ▼
   Redis
     │
     ▼
    RAM
```

RAM access is much faster than disk-based access.  
Therefore Redis is useful when an application needs very fast temporary data access.

---

## 3. Redis is More Than a Cache

A common misconception is:

```text
Redis = Cache
```

This is incomplete.

Redis can be used for:

```text
Redis
 │
 ├── Caching
 ├── Sessions
 ├── Temporary data
 ├── Counters
 ├── Rate limiting
 ├── Queues
 ├── Pub/Sub
 └── Background jobs
```

In Phase 9, the main purpose we care about is:

```text
FastAPI
   │
   ▼
Redis
   │
   ▼
Task Queue
   │
   ▼
Celery Worker
```

---

## 4. Key-Value Storage

The simplest way to understand Redis is:

```text
KEY → VALUE
```

Examples:

```text
"user:101"      → "Yadnyesh"
"session:abc123" → "logged_in"
"otp:user101"    → "583921"
```

It can be mentally understood like a Python dictionary:

```python
redis_data = {
    "user:101": "Yadnyesh",
    "session:abc123": "logged_in",
    "otp:user101": "583921"
}
```

Redis supports many data structures, but the key-value model is the simplest starting point.

---

## 5. Basic Redis Commands

### SET

Stores a value.

```text
SET key value
```

Example:

```text
SET name Yadnyesh
```

Now:

```text
name → Yadnyesh
```

### GET

Retrieves a value.

```text
GET name
```

Result:

```text
"Yadnyesh"
```

If the key doesn't exist:

```text
GET unknown
```

Result:

```text
(nil)
```

### DEL

Deletes a key.

```text
DEL name
```

After deletion:

```text
GET name
```

Result:

```text
(nil)
```

### EXISTS

Checks whether a key exists.

```text
EXISTS name
```

Possible results:

- `1` → exists  
- `0` → does not exist  

---

## 6. TTL — Time To Live

TTL stands for **Time To Live**.  
TTL specifies how long a key should remain in Redis.

Example (OTP):

```text
OTP
 │
 ▼
Stored in Redis
 │
 ▼
5 minutes
 │
 ▼
Automatically expires
```

Example command:

```text
SET otp:user101 583921 EX 300
```

Here:

```text
300 seconds = 5 minutes
```

After 5 minutes, Redis automatically expires the key.

---

## 7. Checking TTL

Use:

```text
TTL otp:user101
```

Example result:

```text
245
```

This means approximately:

```text
245 seconds remaining
```

When the key expires:

```text
GET otp:user101
```

returns:

```text
(nil)
```

---

## 8. Why TTL is Useful

TTL is useful for data that should exist only temporarily.

Examples:

```text
OTP
otp:user101
     │
     ▼
 5 minutes
     │
     ▼
  Expired
```

```text
Session
session:abc123
       │
       ▼
   30 minutes
       │
       ▼
    Expired
```

```text
Cache
cache:user:101
       │
       ▼
    10 minutes
       │
       ▼
    Expired
```

```text
Seat Reservation
seat:A12
   │
   ▼
reserved
   │
   ▼
TTL = 10 minutes
   │
   ▼
expired
   │
   ▼
seat available
```

---

## 9. Redis vs PostgreSQL

Redis and PostgreSQL are designed for different purposes.

**PostgreSQL** — Best suited for:

- Permanent data  
- Relational data  
- Complex queries  
- Transactions  
- Data integrity  
- Relationships  
- Durable storage  

**Redis** — Best suited for:

- Extremely fast access  
- Temporary data  
- Caching  
- Sessions  
- Counters  
- Queues  
- Expiring data  

---

## 10. Redis vs PostgreSQL Comparison

| Feature                    | PostgreSQL             | Redis                  |
|----------------------------|------------------------|------------------------|
| Primary purpose            | Persistent database    | In-memory data store   |
| Storage                    | Mainly disk-based      | Mainly memory-based    |
| Speed                      | Fast                   | Extremely fast         |
| SQL                        | Yes                    | No                     |
| Relational model           | Yes                    | No traditional model   |
| Complex queries            | Yes                    | Limited                |
| Relationships              | Yes                    | No traditional         |
| TTL                        | Not its main feature   | Yes                    |
| Caching                    | Possible               | Excellent              |
| Queue use                  | Possible               | Excellent building block |
| Sessions                   | Possible               | Excellent              |
| Permanent application data | Excellent              | Usually not first choice |
| Temporary data             | Possible               | Excellent              |

---

## 11. Redis Does Not Replace PostgreSQL

Suppose an application has a user:

```text
User
-------------------------
id       = 101
name     = Yadnyesh
email    = user@gmail.com
```

This permanent information should normally be stored in PostgreSQL:

```text
FastAPI
   │
   ▼
PostgreSQL
   │
   ▼
Users Table
```

Redis can store temporary information related to the user:

```text
session:101       → abc123
cache:user:101    → user data
```

Therefore:

```text
PostgreSQL
 │
 ├── Users
 ├── Orders
 ├── Payments
 └── Products

Redis
 │
 ├── Cache
 ├── Sessions
 ├── Temporary data
 └── Task queues
```

---

## 12. Redis as a Cache

Suppose FastAPI frequently requests user information.

Without Redis:

```text
Client
   │
   ▼
FastAPI
   │
   ▼
PostgreSQL
   │
   ▼
User Data
   │
   ▼
Client
```

Repeated requests may repeatedly query PostgreSQL:

```text
Request 1 → PostgreSQL
Request 2 → PostgreSQL
Request 3 → PostgreSQL
Request 4 → PostgreSQL
```

Redis can reduce these database queries.

---

## 13. Cache Hit

Suppose Redis contains:

```text
user:101 → Yadnyesh
```

Request:

```text
GET /users/101
```

Flow:

```text
Client
   │
   ▼
FastAPI
   │
   ▼
Redis
   │
   ▼
Cache HIT
   │
   ▼
Return Data
```

PostgreSQL does not need to be queried.  
A **cache hit** means the requested data was found in the cache.

---

## 14. Cache Miss

Suppose Redis does not contain `user:101`.

Flow:

```text
Client
   │
   ▼
FastAPI
   │
   ▼
Redis
   │
   ▼
Cache MISS
   │
   ▼
PostgreSQL
   │
   ▼
User Data
   │
   ├──────────► Redis
   │
   ▼
Client
```

The application can store the result in Redis so that future requests can be faster.

---

## 15. Redis for Background Processing

This is the most important concept for Phase 9.

Suppose an endpoint performs a heavy operation:

```text
POST /generate-report
```

The operation takes:

```text
30 seconds
```

Doing everything inside FastAPI:

```text
Client
   │
   ▼
FastAPI
   │
   ▼
Generate Report
   │
   │ 30 seconds
   ▼
Response
```

This is undesirable for long-running work.

Instead:

```text
Client
   │
   ▼
FastAPI
   │
   ▼
Create Task
   │
   ▼
Redis Queue
   │
   ▼
Return Response
```

Then a worker processes the task:

```text
Redis Queue
     │
     ▼
Celery Worker
     │
     ▼
Generate Report
```

---

## 16. Redis as a Task Queue

Think of Redis as a waiting room for tasks.

```text
             Redis
       ┌──────────────┐
Task 1 │              │
Task 2 │    QUEUE     │
Task 3 │              │
Task 4 │              │
       └──────────────┘
              │
              ▼
        Celery Worker
```

FastAPI submits the task:

```text
FastAPI
   │
   │ "Generate report"
   ▼
Redis
   │
   │ Task waiting
   ▼
Celery Worker
   │
   ▼
Execute Task
```

---

## 17. BackgroundTasks vs Redis + Celery

**FastAPI BackgroundTasks:**

```text
FastAPI
   │
   ▼
Background Task
   │
   ▼
Execute
```

The task is associated with the application process.  
If the process crashes:

```text
FastAPI ❌
   │
   ▼
Background Task may be lost
```

**Redis + Celery:**

```text
FastAPI
   │
   ▼
Redis
   │
   ▼
Celery Worker
```

If FastAPI crashes *after* the task has been placed in the queue:

```text
FastAPI ❌

Redis
  │
  ▼
Task remains queued
  │
  ▼
Celery Worker
  │
  ▼
Execute Task
```

This provides a much more robust architecture for background processing.

---

## 18. Redis + Celery Architecture

The architecture we will build later is:

```text
                  Client
                     │
                     ▼
                  FastAPI
                     │
                     │ Submit Task
                     ▼
               ┌───────────┐
               │   Redis   │
               │   Queue   │
               └───────────┘
                     │
                     ▼
              Celery Worker
                     │
                     ▼
                Execute Task
```

With multiple workers:

```text
                  Redis
                    │
             ┌──────┼──────┐
             ▼      ▼      ▼
          Worker  Worker  Worker
             1      2      3
```

This allows background work to scale independently from the FastAPI application.

---

## 19. Redis for Task Status

Redis can also temporarily store task information.

Example:

```text
task:abc123 → processing
task:abc123 → completed
task:abc123 → failed
```

FastAPI can expose an endpoint:

```text
GET /tasks/abc123
```

and return:

```json
{
  "task_id": "abc123",
  "status": "processing"
}
```

Task status can also have a TTL so that old task information is automatically removed.

---

## 20. Redis + TTL + Background Jobs

Redis TTL is useful for temporary task metadata.

Example:

```text
task:abc123
status = completed
TTL = 3600 seconds
```

After one hour:

```text
task:abc123
      │
      ▼
   expired
```

This prevents temporary task information from accumulating indefinitely.

---

## 21. Redis in a Seat Reservation System

Suppose a user temporarily reserves seat A12.

Redis can store:

```text
seat:A12 → user:101
TTL = 600 seconds
```

Architecture:

```text
User
 │
 ▼
FastAPI
 │
 ▼
Redis
 │
 ├── seat:A12 → user:101
 │       TTL = 600 sec
 │
 ▼
PostgreSQL
 │
 ▼
Permanent Reservation Data
```

Redis handles temporary state.  
PostgreSQL handles permanent state.

---

## 22. Important Redis Commands

- Store a value:  
  ```text
  SET key value
  ```

- Retrieve a value:  
  ```text
  GET key
  ```

- Delete a key:  
  ```text
  DEL key
  ```

- Check if key exists:  
  ```text
  EXISTS key
  ```

- Check remaining TTL:  
  ```text
  TTL key
  ```

- Store with expiration:  
  ```text
  SET key value EX 300
  ```
  Here `300` seconds = `5` minutes.

---

## 23. Redis Mental Model

Think of Redis as:

> A very fast shared in-memory data store that can hold temporary information and can also be used for caching, queues, counters, sessions, and other high-speed operations.

The three major concepts for this phase are:

```text
Redis
 │
 ├── Key → Value
 │
 ├── TTL → Automatic expiration
 │
 └── Queue → Tasks waiting for workers
```

---

## 24. When to Use Redis

Redis is a good choice when you need:

- Very fast reads/writes  
- Temporary data  
- Automatic expiration  
- Caching  
- Session storage  
- Rate limiting  
- Counters  
- Task queues  
- Background processing infrastructure  
- Pub/Sub  
- Distributed locks  

---

## 25. When Not to Use Redis as the Main Database

Don't automatically use Redis for permanent relational application data.

For example, these are usually better suited to PostgreSQL:

- Users  
- Orders  
- Payments  
- Products  
- Transactions  

A common architecture is:

```text
              FastAPI
                 │
        ┌────────┴────────┐
        ▼                 ▼
   PostgreSQL           Redis
   Permanent            Temporary
      Data                Data
                          │
                          ▼
                     Task Queue
                          │
                          ▼
                    Celery Worker
```

---

## 26. Key Takeaways

- Redis is an in-memory data store.  
- Redis is extremely fast because it primarily works with data in memory.  
- Redis uses a key-value model.  
- Basic commands include: `SET`, `GET`, `DEL`, `EXISTS`, `TTL`.  
- TTL means **Time To Live** and allows Redis keys to automatically expire.  
- Redis is excellent for temporary data.  
- PostgreSQL is better suited for permanent relational application data.  
- Redis can be used as a cache.  
- Redis can also act as infrastructure for a task queue.  
- Redis is commonly used with Celery for background processing.  
- BackgroundTasks and Celery + Redis solve different levels of background-processing requirements.

---

## 27. Core Architecture to Remember

```text
                    FastAPI
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
         PostgreSQL           Redis
        Permanent Data     Temporary/Fast Data
                                │
                                ▼
                           Task Queue
                                │
                                ▼
                         Celery Worker
                                │
                                ▼
                           Heavy Task
```

**One-Line Mental Model**

> Redis = Fast temporary data storage + a building block for caching and task queues.