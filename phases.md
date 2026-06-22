# FastAPI Learning Roadmap

## Phase 1 — First Steps

**Topics**
- What is FastAPI & why use it
- ASGI & Uvicorn
- Installing FastAPI & project structure
- Running the server
- Swagger UI, ReDoc & automatic docs

**Build:** Library API
- `GET /`
- `GET /books`
- `GET /authors`

---

## Phase 2 — Path Operations

**Topics**
- HTTP methods: `GET` `POST` `PUT` `PATCH` `DELETE`
- Path parameters: `int` `str` `float` `UUID`
- Enums & status codes
- Tags, summary & description

**Build:** Student Management API

---

## Phase 3 — Query Parameters

**Topics**
- Optional & required params
- Default values
- Pagination, searching & filtering

**Build:** Movie Search API

---

## Phase 4 — Request Body

**Topics**
- JSON & nested JSON
- Lists & dicts
- Optional fields & default values

**Build:** Restaurant API

---

## Phase 5 — Pydantic

**Topics**
- `BaseModel` & `model_config`
- `Field`, `Annotated` & validation
- Examples & computed fields
- Model inheritance & nested models

**Build:** Amazon Product API

---

## Phase 6 — Response Models

**Topics**
- `response_model`
- include / exclude fields
- Aliases & custom responses

**Build:** Bank API — hide passwords from responses

---

## Phase 7 — Validation

**Topics**
- Path, query & body validation
- Regex, length & range constraints

**Build:** User Registration API

---

## Phase 8 — Error Handling

**Topics**
- `HTTPException` & validation errors
- Custom exceptions & exception handlers

**Build:** Hospital API

---

## Phase 9 — Dependencies

> Probably the most important FastAPI concept.

**Topics**
- `Depends()` & nested dependencies
- Classes as dependencies
- Shared & global dependencies

**Build:** Authentication Middleware Simulation

---

## Phase 10 — Security

**Topics**
- OAuth2 & JWT
- Password hashing
- Login, access tokens & refresh tokens
- Scopes

**Build:** Complete Authentication System

---

## Phase 11 — File Uploads

**Topics**
- `UploadFile`, `File`, `Form`
- Multipart & image upload

**Build:** Portfolio Backend — upload profile picture

---

## Phase 12 — Cookies & Headers

**Topics**
- Cookies & response cookies
- Request & custom headers

**Build:** Session API

---

## Phase 13 — CORS

**Topics**
- `CORSMiddleware`
- Origins & credentials

**Build:** Connect a React frontend

---

## Phase 14 — Middleware

**Topics**
- Custom middleware
- Logging, timing & authentication

**Build:** API Logger

---

## Phase 15 — Background Tasks

**Topics**
- `BackgroundTasks`
- Long-running jobs

**Build:** Email Sender

---

## Phase 16 — Database

**Topics**
- SQLAlchemy: sessions, models & relationships
- CRUD operations
- Alembic migrations

**Build:** Complete Blog Backend

---

## Phase 17 — Async Database

**Topics**
- Async SQLAlchemy & `AsyncSession`
- `asyncpg`

**Build:** Convert a backend to async

---

## Phase 18 — WebSockets

**Topics**
- Live communication
- Connection manager, rooms & broadcast

**Build:** Live Chat API

---

## Phase 19 — Testing

**Topics**
- `pytest` & `TestClient`
- Mocking & dependency override

**Build:** Test suite for the Blog API

---

## Phase 20 — Project Structure

**Topics**
routers/

models/

schemas/

crud/

services/

utils/

config/

database/

middlewares/

dependencies/

**Build:** Refactor Blog API into production structure

---

## Phase 21 — Advanced FastAPI

**Topics**
- Custom `APIRoute` & lifespan events (startup & shutdown)
- `StreamingResponse`, `FileResponse`, `HTMLResponse`, `RedirectResponse`
- GZip & Trusted Host middleware
- WSGI apps, sub-applications & static files
- OpenAPI customization, additional responses & API versioning
- Callbacks, webhooks & custom OpenAPI
- Dependency caching, dataclasses & advanced security
- Custom JSON encoders, background processing & proxy config
- Request state, context variables & custom exception classes
- Async tests, server workers & deployment

**Build:** Production-grade E-Commerce Backend

---

## Phase 22 — Deployment

**Topics**
- Docker & Docker Compose
- Nginx & HTTPS
- Environment variables
- Gunicorn / Uvicorn workers
- Railway, Render & VPS

**Build:** Deploy your API publicly