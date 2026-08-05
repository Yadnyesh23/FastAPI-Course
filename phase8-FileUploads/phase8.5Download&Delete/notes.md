# Phase 8.5 – File Download & Deletion

## Objective

Learn how to:

- Download uploaded files securely.
- Delete uploaded files from the server.
- Understand the difference between **StaticFiles** and **FileResponse**.
- Manage uploaded files like a production backend.

---

# Part 1 – Download Files using FileResponse

## Why do we need FileResponse?

Previously we learned StaticFiles:

```python
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)
```

This makes every file inside the uploads folder publicly accessible.

Example:

```
uploads/
    notes.pdf
```

Accessible at:

```
http://localhost:8000/uploads/notes.pdf
```

This is useful for public assets, but not for private files.

---

# Problem with StaticFiles

Suppose two users upload files.

```
User A

↓

report.pdf

↓

abc123.pdf
```

```
User B

↓

resume.pdf

↓

xyz456.pdf
```

If someone knows:

```
/uploads/abc123.pdf
```

they can access the file directly.

There are no:

- Authentication checks
- Ownership checks
- Permission checks

---

# Solution

Instead of exposing the folder directly, create a download endpoint.

Example:

```
GET /upload/download/{filename}
```

Flow:

```
Client

↓

GET /download/file.pdf

↓

API

↓

Service

↓

Check file exists

↓

Return FileResponse
```

---

# FileResponse

Import:

```python
from fastapi.responses import FileResponse
```

FileResponse sends a file from disk back to the client.

Instead of returning JSON:

```python
return {
    "message": "Success"
}
```

we return:

```python
return FileResponse(...)
```

---

# Download Service

```python
from fastapi import HTTPException
from fastapi.responses import FileResponse

def download_file(filename: str):
    file_path = UPLOAD_PATH / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    return FileResponse(
        path=file_path,
        filename=filename
    )
```

---

# Step-by-Step Explanation

## Step 1

Receive filename.

Example:

```
notes.pdf
```

---

## Step 2

Create complete path.

```python
file_path = UPLOAD_PATH / filename
```

Result:

```
uploads/notes.pdf
```

---

## Step 3

Check whether the file exists.

```python
if not file_path.exists():
```

If missing:

```python
raise HTTPException(
    status_code=404,
    detail="File not found."
)
```

---

## Step 4

Return the file.

```python
return FileResponse(
    path=file_path,
    filename=filename
)
```

The browser downloads or opens the file.

---

# Why don't we specify media_type?

FileResponse automatically detects the MIME type.

Examples:

| File | MIME Type |
|------|-----------|
| .pdf | application/pdf |
| .png | image/png |
| .jpg | image/jpeg |
| .txt | text/plain |

---

# filename Parameter

```python
FileResponse(
    path=file_path,
    filename="Lecture Notes.pdf"
)
```

The file stored on disk may be:

```
7d8c9f1a.pdf
```

But the browser downloads it as:

```
Lecture Notes.pdf
```

Useful when storing UUID filenames internally.

---

# Download API

```python
@router.get("/download/{filename}")
async def download(filename: str):
    return download_file(filename)
```

---

# Download Flow

```
Client

↓

GET /download/abc.pdf

↓

Create Path

↓

File Exists?

↓

Yes

↓

Return FileResponse

↓

Browser Downloads File
```

---

# Part 2 – Delete Files

## Objective

Allow users to permanently remove uploaded files from the server.

Example:

```
DELETE /upload/delete/{filename}
```

---

# Why Delete Files?

Without deletion:

```
uploads/

lecture1.pdf
lecture2.pdf
lecture3.pdf
wrong_file.pdf
old_notes.pdf
```

Storage keeps increasing.

Benefits:

- Saves storage
- Removes unused files
- Prevents orphan files
- Keeps uploads clean

---

# Delete Flow

```
Client

↓

DELETE /delete/file.pdf

↓

API

↓

Service

↓

Create Path

↓

Check Exists

↓

Delete File

↓

Return Success
```

---

# Path.unlink()

To delete a file:

```python
file_path.unlink()
```

`unlink()` permanently removes the file from the filesystem.

---

# Delete Service

```python
from fastapi import HTTPException

def delete_file(filename: str):
    file_path = UPLOAD_PATH / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    file_path.unlink()

    return {
        "message": "File deleted successfully."
    }
```

---

# Step-by-Step Explanation

## Step 1

Receive filename.

---

## Step 2

Create full path.

```python
file_path = UPLOAD_PATH / filename
```

---

## Step 3

Check whether the file exists.

```python
if not file_path.exists():
```

Return:

```
404 File not found
```

if missing.

---

## Step 4

Delete the file.

```python
file_path.unlink()
```

The file is permanently removed.

---

## Step 5

Return success message.

```python
return {
    "message": "File deleted successfully."
}
```

---

# Delete API

```python
@router.delete("/delete/{filename}")
async def delete(filename: str):
    return delete_file(filename)
```

---

# Common Path Methods

| Method | Purpose |
|---------|----------|
| exists() | Check whether file exists |
| mkdir() | Create directory |
| stat() | Get metadata (size, timestamps, etc.) |
| unlink() | Delete file |

---

# StaticFiles vs FileResponse

## StaticFiles

Advantages:

- Automatically serves an entire folder.
- Very simple.
- No routes required.

Disadvantages:

- Public access.
- No authentication.
- No authorization.

Best for:

- Images
- CSS
- JavaScript
- Public documents

---

## FileResponse

Advantages:

- Authentication possible.
- Authorization possible.
- Ownership checks.
- Download logging.
- Custom filenames.

Disadvantages:

- Requires an API route.

Best for:

- User uploads
- Private documents
- Secure downloads
- Production applications

---

# Best Practices

- Always check if the file exists before downloading or deleting.
- Use UUID filenames to avoid filename collisions.
- Store uploaded files in a dedicated uploads folder.
- Use StaticFiles only for publicly accessible assets.
- Use FileResponse for authenticated downloads.
- Delete unnecessary files to prevent storage waste.
- Return meaningful HTTP status codes (404 for missing files).

---

# Key Takeaways

- StaticFiles exposes an entire folder publicly.
- FileResponse sends a specific file through an API endpoint.
- FileResponse allows authentication and permission checks.
- Use `Path.exists()` to verify file existence.
- Use `Path.unlink()` to permanently delete a file.
- Use the DELETE HTTP method for file deletion.
- Secure download APIs are preferred for real-world applications like Google Drive, Dropbox, and TesLearn.
```