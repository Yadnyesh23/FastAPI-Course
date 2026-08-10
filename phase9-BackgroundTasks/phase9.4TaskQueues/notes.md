# Phase 9.4 — Task Queues

## 1. What is a Task Queue?

A **task queue** is a system that stores jobs/tasks and allows separate worker processes to execute them later.

Instead of executing a heavy task directly inside the API request, the task is placed into a queue and processed asynchronously.

### Without Queue

```text
Client
   │
   ▼
FastAPI
   │
   ▼
Heavy Task
   │
   │ 30 seconds
   ▼
Response
```

The client must wait.

### With Queue

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
Queue
   │
   ▼
Response
```

Worker processes it separately:

```text
Queue
   │
   ▼
Worker
   │
   ▼
Heavy Task
```

---

# 2. Why Do We Need Task Queues?

Suppose a user requests:

```http
POST /generate-report
```

Generating the report takes:

```text
30 seconds
```

Without a queue:

```text
Client
   │
   ▼
FastAPI
   │
   ▼
Generate Report
   │
   ▼
Response
```

Problems:

- User waits a long time
- API worker remains occupied
- Throughput decreases
- Heavy workloads can crash the server

With a queue:

```text
Client
   │
   ▼
FastAPI
   │
   ▼
Queue Task
   │
   ▼
Immediate Response
```

The actual work is performed later by workers.

---

# 3. Producer → Queue → Worker Architecture

Every task queue system follows:

```text
Producer
    │
    ▼
  Queue
    │
    ▼
 Worker
```

---

## Producer

Creates tasks.

In our architecture:

```text
FastAPI = Producer
```

Example:

```text
FastAPI
   │
   │ "Generate report"
   ▼
Queue
```

The producer does not execute the task.

It only submits the task.

---

## Queue

Stores tasks waiting to be processed.

Example:

```text
             Queue
      ┌───────────────┐
      │ Task 1        │
      │ Task 2        │
      │ Task 3        │
      │ Task 4        │
      └───────────────┘
```

The queue acts like a waiting line.

---

## Worker

A worker executes tasks.

```text
Queue
  │
  ▼
Worker
  │
  ▼
Execute Task
```

Example:

```text
Task:
Generate report for user 101
```

Worker:

```text
Worker
   │
   ├── Pick task
   ├── Process task
   └── Finish task
```

---

# 4. Complete Flow

```text
                 Client
                    │
                    ▼
                 FastAPI
                Producer
                    │
                    ▼
                  Queue
                    │
                    ▼
                 Worker
                    │
                    ▼
               Execute Task
```

FastAPI only submits work.

Workers perform work.

---

# 5. Multiple Tasks

Suppose 5 users submit jobs.

```text
FastAPI
   │
   ├── Task 1
   ├── Task 2
   ├── Task 3
   ├── Task 4
   └── Task 5
         │
         ▼
       Queue
```

Tasks wait until workers become available.

---

# 6. Multiple Workers

A major benefit of queues is horizontal scaling.

```text
                 Queue
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
      Worker1  Worker2  Worker3
          │        │        │
          ▼        ▼        ▼
        Task1    Task2    Task3
```

Benefits:

- Higher throughput
- Better scalability
- Parallel processing

---

# 7. Producer vs Worker

### Producer

Creates tasks.

```text
FastAPI
   │
   ▼
Submit Task
```

### Worker

Executes tasks.

```text
Worker
   │
   ▼
Execute Task
```

Important:

```text
Producer ≠ Worker
```

They are separate processes.

---

# 8. What is a Message Broker?

A **message broker** sits between producers and workers.

It receives tasks from producers and delivers them to workers.

```text
FastAPI
   │
   ▼
Message Broker
   │
   ▼
Worker
```

The task itself is a message.

Example:

```json
{
    "task": "generate_report",
    "user_id": 101
}
```

---

# 9. Redis as a Message Broker

Redis can act as a broker.

Architecture:

```text
FastAPI
   │
   ▼
 Redis
   │
   ▼
Worker
```

In our future setup:

```text
FastAPI
   │
   ▼
 Redis
   │
   ▼
Celery Worker
```

Redis stores tasks until workers consume them.

---

# 10. Why Not Execute Tasks Directly?

Suppose FastAPI directly calls:

```python
generate_report()
```

Flow:

```text
FastAPI
   │
   ▼
Generate Report
   │
   │ 30 seconds
   ▼
Response
```

Problems:

- Slow response
- Worker blocked
- Poor scalability

Using a queue:

```text
FastAPI
   │
   ▼
Queue
   │
   ▼
Worker
```

FastAPI remains free to serve more requests.

---

# 11. Why Queues Are Needed

Queues provide **decoupling**.

Without queue:

```text
FastAPI
   │
   ▼
Heavy Task
```

With queue:

```text
FastAPI
   │
   ▼
Queue
   │
   ▼
Worker
```

Now:

```text
FastAPI = Task Creation

Worker = Task Execution
```

Both can scale independently.

---

# 12. Queues Absorb Traffic Spikes

Suppose:

```text
1000 users
```

submit jobs simultaneously.

Without queue:

```text
FastAPI
   │
   ├── Job 1
   ├── Job 2
   ├── Job 3
   ├── ...
   └── Job 1000
```

The application can become overloaded.

With queue:

```text
            Queue
      ┌─────────────┐
      │ Job 1       │
      │ Job 2       │
      │ Job 3       │
      │ ...         │
      │ Job 1000    │
      └─────────────┘
             │
             ▼
          Workers
```

The queue acts as a buffer.

---

# 13. Queue as a Waiting Line

Think of a queue like customers waiting in a line.

```text
Customers
    │
    ▼
 ┌─────────┐
 │ Queue   │
 └─────────┘
     │
     ▼
 Service
```

Similarly:

```text
Tasks
   │
   ▼
 Queue
   │
   ▼
Worker
```

---

# 14. Job States

Tasks move through different states.

A simplified lifecycle:

```text
PENDING
   │
   ▼
STARTED
   │
   ├──────► SUCCESS
   │
   └──────► FAILURE
```

---

## PENDING

Task created.

Waiting in queue.

```json
{
    "task_id": "abc123",
    "status": "PENDING"
}
```

---

## STARTED

Worker has picked up the task.

```json
{
    "task_id": "abc123",
    "status": "STARTED"
}
```

---

## SUCCESS

Task completed successfully.

```json
{
    "task_id": "abc123",
    "status": "SUCCESS"
}
```

Example:

```json
{
    "task_id": "abc123",
    "status": "SUCCESS",
    "result": "report.pdf"
}
```

---

## FAILURE

Task execution failed.

```json
{
    "task_id": "abc123",
    "status": "FAILURE"
}
```

Example reasons:

- Network failure
- Database error
- External API failure
- Unhandled exception

---

## RETRY

Some failures are temporary.

Instead of failing permanently:

```text
STARTED
   │
   ▼
FAILURE
   │
   ▼
RETRY
   │
   ▼
STARTED
   │
   ▼
SUCCESS
```

This is one of Celery's most useful features.

---

# 15. Complete Job Lifecycle

```text
             Create Job
                  │
                  ▼
               PENDING
                  │
                  ▼
               STARTED
               /      \
              /        \
             ▼          ▼
         SUCCESS      FAILURE
                        │
                        ▼
                      RETRY
                        │
                        ▼
                     STARTED
```

Terminal states:

```text
SUCCESS
```

or

```text
FAILURE
```

---

# 16. Why Job States Matter

FastAPI usually returns:

```json
{
    "task_id": "abc123"
}
```

The client can later query:

```http
GET /tasks/abc123
```

Possible responses:

### Pending

```json
{
    "status": "PENDING"
}
```

### Running

```json
{
    "status": "STARTED"
}
```

### Finished

```json
{
    "status": "SUCCESS"
}
```

This enables asynchronous APIs.

---

# 17. BackgroundTasks vs Task Queue

## BackgroundTasks

```text
FastAPI
   │
   ▼
BackgroundTasks
   │
   ▼
Function
```

Good for:

- Logging
- Simple emails
- Short notifications
- Small background work

---

## Task Queue

```text
FastAPI
   │
   ▼
Message Broker
   │
   ▼
Worker
```

Good for:

- Long-running tasks
- Multiple workers
- Retries
- Monitoring
- Scalability
- Reliability

---

# 18. Redis + Celery Architecture

The architecture we will build:

```text
                   Client
                      │
                      ▼
                   FastAPI
                  Producer
                      │
                      ▼
                    Redis
                Message Broker
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
           ┌──────────┼──────────┐
           ▼          ▼          ▼
       Worker1    Worker2    Worker3
           │          │          │
           ▼          ▼          ▼
         Task1      Task2      Task3
```

---

# 19. Real-World Example

### Request

```http
POST /process-file
```

### FastAPI

Creates task:

```text
task_id = abc123
```

Stores task in Redis.

### Response

```json
{
    "task_id": "abc123",
    "status": "PENDING"
}
```

### Worker

```text
Redis
   │
   ▼
Worker
   │
   ▼
Process File
```

### Status Endpoint

```http
GET /tasks/abc123
```

Returns:

```json
{
    "task_id": "abc123",
    "status": "SUCCESS"
}
```

---

# 20. Four Components to Remember

```text
Producer
   ↓
Queue
   ↓
Worker
   ↓
Job State
```

### Producer

Creates tasks.

```text
FastAPI
```

### Queue

Stores tasks.

```text
Redis
```

### Worker

Executes tasks.

```text
Celery Worker
```

### Job State

Tracks task progress.

```text
PENDING
STARTED
SUCCESS
FAILURE
RETRY
```

---

# Key Takeaways

1. A task queue stores work for asynchronous execution.

2. Core architecture:

```text
Producer → Queue → Worker
```

3. FastAPI acts as the producer.

4. Redis commonly acts as the queue/message broker.

5. Celery workers execute tasks.

6. Queues decouple task creation from task execution.

7. Queues absorb traffic spikes.

8. Multiple workers enable parallel processing.

9. Job states track task progress.

10. Task queues are more scalable and reliable than simple BackgroundTasks.

---

# Mental Model

```text
                    Client
                       │
                       ▼
                    FastAPI
                    Producer
                       │
                       ▼
                      Redis
                      Queue
                       │
                       ▼
                  Celery Worker
                       │
                       ▼
                   Execute Job
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
          SUCCESS             FAILURE
                                  │
                                  ▼
                                RETRY
```

## One-Line Summary

> A task queue decouples task creation from task execution by allowing producers to submit jobs to a queue and workers to process them asynchronously.