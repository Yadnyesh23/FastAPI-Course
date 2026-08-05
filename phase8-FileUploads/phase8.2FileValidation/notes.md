# Phase 8.2 – File Validation (Production Ready Uploads)

## Objective

Learn how to secure a file upload endpoint by validating uploaded files before saving them to the server.

In this phase, we make our upload API production-ready by preventing invalid, malicious, or oversized files from being stored.

---

# Why Do We Need File Validation?

Without validation, anyone can upload:

- Executable files (`.exe`)
- Malicious scripts
- Huge files (GBs in size)
- Fake file types
- Duplicate filenames

This can lead to:

- Security vulnerabilities
- Disk space exhaustion
- File overwriting
- Poor application performance

Therefore, **never trust the client**.

Always validate the uploaded file before saving it.

---

# Production Upload Validation Checklist

A secure upload endpoint should validate:

- File Extension
- MIME Type
- File Size
- Unique Filename
- Destination Path

---

# 1. File Extension Validation

The file extension is extracted using:

```python
extension = Path(file.filename).suffix.lower()
```

Example:

| Uploaded File | Extracted Extension |
|--------------|---------------------|
| notes.pdf | .pdf |
| image.PNG | .png |
| report.final.pdf | .pdf |

We then compare it against a whitelist.

```python
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".txt"
}
```

Validation:

```python
if extension not in ALLOWED_EXTENSIONS:
    raise HTTPException(
        status_code=400,
        detail="Invalid file extension."
    )
```

Only approved extensions are accepted.

---

# Why `.lower()`?

Users may upload:

```
IMAGE.JPG
```

or

```
image.jpg
```

Both should be treated as:

```
.jpg
```

Hence:

```python
suffix.lower()
```

---

# 2. MIME Type Validation

A user can rename:

```
virus.exe
```

to

```
notes.pdf
```

Extension now looks valid.

Therefore we also validate the MIME type.

```python
file.content_type
```

Example MIME types:

| File | MIME Type |
|------|-----------|
| PDF | application/pdf |
| PNG | image/png |
| JPG | image/jpeg |
| TXT | text/plain |

Allowed MIME types:

```python
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/jpg",
    "image/png",
    "text/plain",
}
```

Validation:

```python
if file.content_type not in ALLOWED_MIME_TYPES:
    raise HTTPException(
        status_code=400,
        detail="Invalid MIME type."
    )
```

---

# Why Validate Both Extension and MIME Type?

Extension alone is not trustworthy.

```
virus.exe
```

↓

Rename

↓

```
virus.pdf
```

Extension becomes:

```
.pdf
```

But MIME type remains different.

Checking both provides better security.

> **Note:** MIME type is also sent by the client, so it can be spoofed. For very high-security systems, libraries such as `python-magic` inspect the actual file contents ("magic numbers").

---

# 3. File Size Validation

Large uploads consume:

- Memory
- Disk space
- Bandwidth

Suppose our limit is:

```python
MAX_FILE_SIZE = 10 * 1024 * 1024
```

(10 MB)

We calculate the size **before saving**.

```python
file.file.seek(0, 2)
size = file.file.tell()
file.file.seek(0)
```

Explanation:

```
seek(0, 2)
```

Move the pointer to the end of the file.

```
tell()
```

Returns the current position of the pointer.

Current position equals file size.

```
seek(0)
```

Moves the pointer back to the beginning.

Without resetting the pointer, the file would be saved empty.

Validation:

```python
if size > MAX_FILE_SIZE:
    raise HTTPException(
        status_code=400,
        detail="File size exceeds 10 MB."
    )
```

---

# Understanding `seek()`

The second argument is called **whence**.

| Value | Meaning |
|--------|---------|
| 0 | Beginning of file (`SEEK_SET`) |
| 1 | Current position (`SEEK_CUR`) |
| 2 | End of file (`SEEK_END`) |

Examples:

```python
file.seek(0, 0)    # Beginning
file.seek(10, 0)   # Move to byte 10
file.seek(5, 1)    # Move 5 bytes forward
file.seek(0, 2)    # Move to end
```

---

# Why Validate Before Saving?

Incorrect approach:

```
Save File

↓

Check Size

↓

Delete File
```

Problems:

- Wastes disk space
- Wastes I/O
- Slower
- Vulnerable to abuse

Correct approach:

```
Validate

↓

Save
```

---

# 4. UUID Filenames

Suppose two users upload:

```
notes.pdf
```

Without UUID:

```
uploads/
    notes.pdf
```

Second upload overwrites the first.

Solution:

```python
unique_filename = f"{uuid.uuid4()}{extension}"
```

Example:

```
3fd8c55e-ae16-4b38-bad5-65f3c2c9a16f.pdf
```

Every uploaded file receives a unique name.

Benefits:

- No overwriting
- No filename collisions
- Better security
- Easier storage management

---

# Original vs Stored Filename

User uploads:

```
Machine Learning Notes.pdf
```

Stored on disk:

```
7c4d9b34-ae1b-42ef-9c11-8d7f1d9f3a66.pdf
```

We keep both.

```python
{
    "original_filename": file.filename,
    "stored_filename": unique_filename
}
```

### Original Filename

Used for:

- UI
- Downloads
- Search
- Display

### Stored Filename

Used for:

- File storage
- Prevent collisions
- Security

---

# Creating File Path

```python
file_path = UPLOAD_DIR / unique_filename
```

Example:

```
uploads/
    3fd8c55e.pdf
```

This creates the destination path for the uploaded file.

---

# Saving the File

```python
with open(file_path, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
```

Explanation:

- Open destination file in binary write mode.
- Create destination file if it doesn't exist.
- Copy uploaded file stream to disk.

`copyfileobj()` copies the file efficiently in chunks instead of loading everything into RAM.

---

# Returning Metadata

```python
return {
    "original_filename": file.filename,
    "stored_filename": unique_filename,
    "content_type": file.content_type,
    "path": str(file_path),
    "size": size,
}
```

Useful metadata includes:

- Original filename
- Stored filename
- MIME type
- File path
- File size

---

# Complete Upload Flow

```
Client Upload
      │
      ▼
Receive UploadFile
      │
      ▼
Extract File Extension
      │
      ▼
Validate Extension
      │
      ▼
Validate MIME Type
      │
      ▼
Calculate File Size
      │
      ▼
Validate File Size
      │
      ▼
Generate UUID Filename
      │
      ▼
Create Destination Path
      │
      ▼
Save File
      │
      ▼
Return File Metadata
```

---

# Security Benefits

Our upload API now protects against:

- Invalid file extensions
- Invalid MIME types
- Oversized uploads
- Duplicate filenames
- Accidental overwriting

---

# Best Practices

- Never trust client input.
- Validate extension using a whitelist.
- Validate MIME type in addition to extension.
- Reject oversized files before saving them.
- Generate UUID-based filenames.
- Keep the original filename for UI purposes.
- Store files using unique server-generated names.
- Use `Path` instead of string concatenation.
- Use `copyfileobj()` for efficient file copying.
- Return useful metadata after successful uploads.

---

# Key Takeaways

- File uploads should always be validated before being saved.
- Extension validation alone is insufficient.
- MIME type adds another layer of security.
- File size should be checked before writing to disk.
- UUID filenames prevent collisions and overwriting.
- Keep separate original and stored filenames.
- Production upload APIs prioritize security, performance, and reliability.