# Phase 8.1 – File Uploads (FastAPI)

## Objective

Learn how to accept files from clients, save them locally, and understand how FastAPI processes uploaded files.

---

# Why can't we use JSON for file uploads?

JSON is designed to transfer **text data**.

Example:

```json
{
    "username": "Yadnyesh",
    "age": 20
}
```

Files (PDFs, Images, Videos, ZIPs, etc.) are **binary data**, not plain text.

Therefore, file uploads use:

```
multipart/form-data
```

instead of

```
application/json
```

---

# multipart/form-data

When a client uploads a file, the request body is divided into multiple parts.

Example:

```
Part 1
-------
username

Yadnyesh

Part 2
-------
file

notes.pdf
```

Every HTML file upload form uses:

```
multipart/form-data
```

---

# UploadFile

FastAPI represents an uploaded file using the `UploadFile` class.

Example:

```python
from fastapi import UploadFile, File

async def upload(file: UploadFile = File(...)):
    ...
```

`UploadFile` contains information about the uploaded file and methods to interact with it.

---

# File(...)

`File(...)` tells FastAPI:

> "This parameter should come from the uploaded files in the multipart/form-data request."

Example:

```python
file: UploadFile = File(...)
```

Similar to:

```python
Query(...)
Path(...)
Body(...)
```

---

# Important UploadFile Properties

## filename

Returns the uploaded filename.

```python
file.filename
```

Example:

```
notes.pdf
```

---

## content_type

Returns the MIME type.

```python
file.content_type
```

Examples:

```
application/pdf
image/png
image/jpeg
```

Useful for validation.

---

## file

Returns the underlying file stream.

```python
file.file
```

This stream is used for efficient copying without loading the entire file into memory.

---

## read()

Reads the uploaded file.

```python
contents = await file.read()
```

Returns:

```python
bytes
```

Example:

```python
type(contents)
```

Output:

```python
<class 'bytes'>
```

---

# Creating Upload Directory

```python
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
```

## Path

`Path` is a Python standard library class (`pathlib`) that represents filesystem paths.

Instead of writing:

```python
"uploads/" + filename
```

we write:

```python
UPLOAD_DIR / filename
```

### Benefits

- Cleaner code
- Cross-platform
- Safer path handling
- Rich filesystem methods

---

## mkdir(exist_ok=True)

Creates the directory only if it doesn't already exist.

Behavior:

```
Folder exists
↓

Do nothing
```

```
Folder doesn't exist
↓

Create folder
```

---

# Creating Destination Path

```python
file_path = UPLOAD_DIR / file.filename
```

Suppose:

```
UPLOAD_DIR = uploads
```

and

```
file.filename = notes.pdf
```

Result:

```
uploads/notes.pdf
```

> **Important:** This does **not** create the file. It only creates a `Path` object representing where the file should be saved.

---

# Saving File

```python
with open(file_path, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
```

This is the core of the upload process.

---

## open(file_path, "wb")

Opens (or creates) the destination file.

### "w"

Write mode.

If the file exists, overwrite it.

### "b"

Binary mode.

Files such as PDFs, images, videos, ZIPs, etc. contain binary data.

Binary mode must be used for writing uploaded files.

---

## buffer

```python
with open(...) as buffer
```

`buffer` is simply a variable referring to the opened destination file.

It could also be named:

```python
f
output_file
destination
```

The name is not special.

---

# shutil.copyfileobj()

Syntax:

```python
shutil.copyfileobj(source, destination)
```

In our code:

```python
shutil.copyfileobj(
    file.file,
    buffer
)
```

Meaning:

Copy everything from the uploaded file stream into the destination file.

---

# Internal Working

Conceptually, `copyfileobj()` works like this:

```python
while True:
    chunk = source.read(16 * 1024)

    if not chunk:
        break

    destination.write(chunk)
```

Instead of loading the entire file into RAM, it copies the file in **small chunks**.

---

# Why use copyfileobj()?

### Efficient

```
Read 16 KB
↓

Write 16 KB
↓

Read next 16 KB
↓

Write next 16 KB
```

Memory usage stays low.

---

# Why not use await file.read()?

Example:

```python
contents = await file.read()

with open(file_path, "wb") as f:
    f.write(contents)
```

This loads the **entire file into RAM**.

If a user uploads a 2 GB file, your application attempts to load all 2 GB into memory.

`copyfileobj()` avoids this by streaming the file chunk-by-chunk.

Therefore, it is the preferred approach for production applications.

---

# Returning Response

Example:

```python
return {
    "filename": file.filename,
    "path": str(file_path),
    "size": file_path.stat().st_size
}
```

Possible response:

```json
{
    "filename": "notes.pdf",
    "path": "uploads/notes.pdf",
    "size": 482391
}
```

---

# Complete Upload Flow

```
Client
    │
Uploads File
    │
    ▼
FastAPI receives multipart/form-data
    │
    ▼
UploadFile object created
    │
    ▼
Ensure uploads/ directory exists
    │
    ▼
Create destination path
    │
    ▼
Open destination file
    │
    ▼
Copy uploaded file stream
    │
    ▼
Close file automatically
    │
    ▼
Return upload response
```

---

# Architecture Used

```
Client
    │
    ▼
Upload API
    │
    ▼
Upload Service
    │
    ▼
uploads/
```

The API handles HTTP requests, while the Service contains the business logic for saving files.

---

# Best Practices

- Use `UploadFile` instead of reading raw bytes.
- Always use `multipart/form-data` for uploads.
- Use `pathlib.Path` instead of string concatenation.
- Use `mkdir(exist_ok=True)` to ensure the upload directory exists.
- Open uploaded files using `"wb"` mode.
- Prefer `shutil.copyfileobj()` over `await file.read()` for large files.
- Keep upload logic inside the Service layer.
- Return file metadata after a successful upload.

---

# Key Takeaways

- Files cannot be uploaded using JSON.
- `multipart/form-data` is the standard format for file uploads.
- `UploadFile` represents the uploaded file.
- `File(...)` tells FastAPI to expect a file.
- `Path` provides a clean and platform-independent way to work with file paths.
- `copyfileobj()` efficiently streams data from the uploaded file to disk.
- Separating upload logic into a Service keeps the project clean and scalable.