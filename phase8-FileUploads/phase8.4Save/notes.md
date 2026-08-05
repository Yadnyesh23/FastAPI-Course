# Phase 8.4 – Serving Uploaded Files (StaticFiles)

## Objective

Learn how to make uploaded files accessible through URLs so users can:

- View images
- Open PDFs
- Download files
- Share file links

Instead of only saving files to disk, we now allow clients to access them through HTTP.

---

# The Problem

After uploading a file:

```
uploads/
    2f6a9e71.pdf
```

The file exists on the server, but the browser has **no way to access it**.

Example:

```
uploads/
    notes.pdf
```

This is only a file stored on disk.

There is no API or URL to retrieve it.

---

# The Solution

FastAPI provides **StaticFiles**.

StaticFiles exposes an entire folder through a URL.

Example:

```
uploads/
    image.png
    notes.pdf
    resume.pdf
```

becomes

```
/uploads/image.png
/uploads/notes.pdf
/uploads/resume.pdf
```

No extra API endpoints are required.

---

# Import StaticFiles

```python
from fastapi.staticfiles import StaticFiles
```

StaticFiles is FastAPI's built-in static file server.

---

# Mount the Uploads Folder

```python
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)
```

---

# Understanding app.mount()

Think of `mount()` as:

> "Attach this folder to this URL."

Syntax:

```python
app.mount(
    url_path,
    StaticFiles(directory=folder_name),
    name=folder_name
)
```

---

# Parameters

## URL Prefix

```python
"/uploads"
```

The URL users will visit.

Example:

```
http://localhost:8000/uploads/image.png
```

---

## Directory

```python
directory="uploads"
```

The actual folder on your computer.

Example:

```
project/

uploads/
    image.png
```

---

## Name

```python
name="uploads"
```

A name for the mounted application.

Mostly useful for internal routing and URL generation.

---

# Project Structure

```
project/

│── app/
│── uploads/
│     ├── image.png
│     ├── notes.pdf
│     └── resume.pdf
│
│── main.py
```

---

# Request Flow

```
Browser

↓

GET /uploads/image.png

↓

FastAPI

↓

StaticFiles

↓

uploads/image.png

↓

Return File
```

---

# Browser Request

User opens:

```
http://localhost:8000/uploads/image.png
```

FastAPI:

1. Detects the `/uploads` prefix.
2. Looks inside the `uploads` folder.
3. Finds `image.png`.
4. Returns the file.

---

# StaticFiles vs API Endpoints

## API Endpoint

```python
@router.get("/user")
```

Appears in Swagger.

Requires a Python function.

```
Client

↓

Route

↓

Python Function

↓

Response
```

---

## StaticFiles

```python
app.mount("/uploads", StaticFiles(...))
```

Does **NOT** appear in Swagger.

No Python function is executed.

```
Client

↓

StaticFiles

↓

File

↓

Response
```

---

# Why Doesn't It Appear in Swagger?

Swagger documents **API endpoints** only.

Examples:

```
GET
POST
PUT
DELETE
```

StaticFiles is not an API endpoint.

It is a static file server.

Therefore, it is **not included in OpenAPI documentation**.

---

# Example

Suppose:

```
uploads/

cat.png
notes.pdf
resume.pdf
```

Accessible URLs:

```
http://localhost:8000/uploads/cat.png

http://localhost:8000/uploads/notes.pdf

http://localhost:8000/uploads/resume.pdf
```

---

# File Types

StaticFiles automatically returns the correct Content-Type.

Examples:

| File | Content-Type |
|------|--------------|
| .png | image/png |
| .jpg | image/jpeg |
| .pdf | application/pdf |
| .txt | text/plain |

The browser decides whether to display or download the file.

---

# StaticFiles vs FileResponse

## StaticFiles

Advantages:

- Very simple
- Automatically serves an entire folder
- No route required
- Fast

Disadvantages:

- Public access
- No authentication
- No permission checks

Use Cases:

- Images
- CSS
- JavaScript
- Public Documents

---

## FileResponse

Advantages:

- Can check JWT
- Can verify ownership
- Can log downloads
- Can restrict access

Disadvantages:

- Requires a route

Use Cases:

- Private documents
- User uploads
- Secure downloads
- Production applications

---

# Real-World Example

Suppose User A uploads:

```
resume.pdf

↓

8d71c3f1.pdf
```

If using StaticFiles:

```
/uploads/8d71c3f1.pdf
```

Anyone who knows the filename can access it.

A better solution is:

```
GET /download/{file_id}
```

Inside that route:

```
Authenticate User

↓

Verify Ownership

↓

Return FileResponse
```

This is how cloud storage platforms work.

---

# Best Practices

- Store uploaded files outside the application code.
- Use StaticFiles only for publicly accessible files.
- Use UUID filenames to prevent collisions.
- Use FileResponse for private files.
- Keep uploads organized in a dedicated folder.

---

# Key Takeaways

- StaticFiles serves an entire folder through HTTP.
- `app.mount()` connects a URL path to a directory.
- Mounted folders do not appear in Swagger because they are not API endpoints.
- Files become accessible through URLs like `/uploads/filename`.
- StaticFiles is ideal for public assets.
- FileResponse should be used for authenticated or protected downloads.