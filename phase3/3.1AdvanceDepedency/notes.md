# Phase 3.1 – Advanced Dependencies

## Objectives

By the end of this phase, you should understand:

Dependency Graph

Dependency Resolution Order

Dependency Caching

use_cache=False

yield Dependencies

Database Session Pattern

Classes as Dependencies

Dependency Overrides

Best Practices

1. Dependency Graph

FastAPI builds a dependency graph before executing a route.

Example:

Python

Code

def get_token():

return "abc123"

def get_user(token: str = Depends(get_token)):

return {"name": "Yadnyesh"}

@app.get("/")

def root(user=Depends(get_user)):

return user

Dependency Graph:

root()

↑

get_user()

↑

get_token()

Execution Order:

Request

↓

get_token()

↓

get_user()

↓

root()

↓

Response

2. Dependency Caching

FastAPI executes the same dependency only once per request.

Example:

def get_user():

print("Running...")

return {"name": "Yadnyesh"}

@app.get("/")

def root(

user1=Depends(get_user),

user2=Depends(get_user)

):

return {"u1": user1, "u2": user2}

Output:

Running...

Printed only once.

3. Cache Scope

The cache is per request, not global.

Request 1:

get_user() ← executed

Request 2:

get_user() ← executed again

4. Disabling Cache

Use use_cache=False.

Depends(get_time, use_cache=False)

This forces the dependency to run every time it is requested within the same request.

5. yield Dependencies

This is one of the most important FastAPI patterns.

Problem with return:

def get_db():

db = SessionLocal()

return db

The database connection is never closed.

Correct Pattern:

def get_db():

db = SessionLocal()

try:

yield db

finally:

db.close()

6. How yield Works

Flow:

Open Resource

↓

yield Resource

↓

Route Executes

↓

Resume Dependency

↓

Cleanup Resource

FastAPI pauses the dependency at yield, runs the route, then resumes the dependency to execute cleanup code.

7. Why yield Is Used for Database Sessions

Database connections must be:

Opened

Used

Closed

If connections are never closed, the application suffers from connection leaks and eventually the database refuses new connections.

8. return vs yield

return

	

yield




Ends the function

	

Pauses the function




Never resumes

	

Can resume later




No cleanup after returning

	

Cleanup possible after route execution




Used for simple values

	

Used for resources needing cleanup

9. Classes as Dependencies

Dependencies can be classes.

Example:

class Pagination:

def init(self, limit: int = 10, skip: int = 0):

self.limit = limit

self.skip = skip

Use it:

@app.get("/students")

def students(query: Pagination = Depends()):

return {"limit": query.limit, "skip": query.skip}

Request:

/students?limit=5&skip=15

Response:

{"limit": 5, "skip": 15}

10. Why Use Classes as Dependencies?

Useful for grouping related parameters such as:

Pagination

Filters

Search options

Sorting

Configuration

11. Dependency Overrides

Used mainly for testing.

Real dependency:

def get_db():

return RealDatabase()

Fake dependency:

def fake_db():

return FakeDatabase()

Override:

app.dependency_overrides[get_db] = fake_db

Now every route using Depends(get_db) receives FakeDatabase().

12. Why Dependency Overrides Are Useful

They make tests:

Faster

Safer

Independent of real databases

Predictable

13. Best Practices

Keep dependencies focused.

Bad:

def do_everything():

Good:

def get_current_user():

def get_db():

def verify_admin():

Use yield for cleanup.

Use yield whenever a resource must be closed or cleaned up.

Reuse dependencies.

Write authentication, database, and permission logic once and reuse it across routes.

Keep business logic out of dependencies.

Dependencies should prepare resources or validate access, not implement core business rules.

14. Real TesLearn Pattern

def get_current_user():

...

def get_db():

yield db

@app.post("/notes")

def create_note(

user=Depends(get_current_user),

db=Depends(get_db)

):

...

Execution Flow:

Request

↓

Verify User

↓

Open DB Connection

↓

Execute Route

↓

Close DB Connection

↓

Response

15. Interview Questions

What is a Dependency Graph?

How does FastAPI resolve dependencies?

What is Dependency Caching?

When is the cache cleared?

What does use_cache=False do?

What is a yield dependency?

Why is yield used for database sessions?

Difference between return and yield?

Can classes be dependencies?

What are Dependency Overrides?

Why are Dependency Overrides useful during testing?

What are the benefits of Dependency Injection?

16. Quick Cheat Sheet

Feature

	

Purpose




Depends()

	

Inject dependency




use_cache=False

	

Disable per-request caching




yield

	

Setup + Cleanup




get_db()

	

Database session dependency




Class Dependency

	

Group related parameters




dependency_overrides

	

Replace dependencies during tests

17. Key Takeaways

FastAPI builds a dependency graph automatically.

Dependencies are executed in the correct order.

Dependency results are cached per request.

yield dependencies support setup and cleanup.

Database sessions should use yield.

Classes can be used as dependencies.

Dependency Overrides make testing easy.

Small, reusable dependencies are a core FastAPI best practice.