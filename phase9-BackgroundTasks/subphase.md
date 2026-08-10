9.1 — Background jobs fundamentals
What is a background job?
Why do we need background processing?
Synchronous vs background processing
Blocking vs non-blocking
When to use BackgroundTasks

9.2 — FastAPI BackgroundTasks
BackgroundTasks
Adding tasks
Passing arguments
Limitations
When not to use it

9.3 — Redis fundamentals
What Redis is
Key-value storage
TTL
Redis vs PostgreSQL
Why Redis is useful for background processing

9.4 — Task queues
What is a task queue?
Producer → Queue → Worker
Message brokers
Why queues are needed
Job states

9.5 — Celery
Celery architecture
Broker
Worker
Tasks
Result backend
Celery + Redis

9.6 — Implement Celery with FastAPI

We'll build:

FastAPI
   ↓
Celery
   ↓
Redis
   ↓
Worker

and actually execute jobs.

9.7 — Job states & results
PENDING
   ↓
STARTED
   ↓
SUCCESS

and:

PENDING
   ↓
STARTED
   ↓
FAILURE

We'll learn how to check job status.

9.8 — Retries
Why jobs fail
Automatic retries
Retry delays
Maximum retries
Exponential backoff

Example:

Attempt 1 → FAIL
    ↓
5 sec
    ↓
Attempt 2 → FAIL
    ↓
30 sec
    ↓
Attempt 3 → SUCCESS

9.9 — Multiple workers & concurrency
             Redis
               ↓
       ┌───────┼───────┐
       ↓       ↓       ↓
   Worker 1 Worker 2 Worker 3

We'll understand how jobs are distributed.

9.10 — Production background jobs
Docker
Celery worker
Redis
graceful shutdown
logging
monitoring
failed jobs
idempotency
task design