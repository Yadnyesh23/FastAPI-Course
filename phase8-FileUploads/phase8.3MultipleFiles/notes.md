# Phase 8.3 – Multiple File Uploads

## Objective

Learn how to upload **multiple files** in a single HTTP request instead of uploading one file at a time.

This improves user experience by allowing users to upload multiple documents simultaneously.

Example:

Instead of:

```
lecture1.pdf
```

Users can upload:

```
lecture1.pdf
lecture2.pdf
lecture3.pdf
lecture4.pdf
```

using a single API request.

---

# Why Multiple File Uploads?

Imagine TesLearn.

Instead of uploading:

```
Lecture 1.pdf

↓

Upload

↓

Lecture 2.pdf

↓

Upload

↓

Lecture 3.pdf

↓

Upload
```

The user can simply select:

```
Lecture1.pdf
Lecture2.pdf
Lecture3.pdf
Lecture4.pdf
```

and upload everything together.

Benefits:

- Better User Experience
- Fewer HTTP Requests
- Faster Upload Process
- Cleaner Frontend

---

# Single Upload vs Multiple Upload

## Single File

```python
file: UploadFile = File(...)
```

FastAPI expects exactly one uploaded file.

```
Client
    │
    ▼
UploadFile
```

---

## Multiple Files

```python
files: list[UploadFile] = File(...)
```

FastAPI expects a list of uploaded files.

```
Client
    │
    ▼
List[UploadFile]
```

Internally:

```python
[
    UploadFile(...),
    UploadFile(...),
    UploadFile(...)
]
```

---

# Upload Flow

```
Client
    │
    ▼
List[UploadFile]
    │
    ▼
Loop through each file
    │
    ▼
Validate File
    │
    ▼
Save File
    │
    ▼
Store Metadata
    │
    ▼
Return List of Uploaded Files
```

---

# Code Reusability

We already created:

```python
upload_file(file)
```

There is **no need to rewrite all validation logic again.**

Instead:

```
Receive List

↓

Loop

↓

upload_file(file)

↓

Next File

↓

upload_file(file)
```

This follows the **DRY Principle**.

> DRY = Don't Repeat Yourself

---

# API Endpoint

```python
@router.post("/multiple")
async def upload_multiple_files(
    files: list[UploadFile] = File(...)
):
    uploaded_files = []

    for file in files:
        result = upload_file(file)
        uploaded_files.append(result)

    return {
        "message": "Files uploaded successfully.",
        "files": uploaded_files
    }
```

---

# Step-by-Step Explanation

## Receive Multiple Files

```python
files: list[UploadFile] = File(...)
```

FastAPI converts the uploaded files into a list.

Example:

```
[
    UploadFile(notes.pdf),
    UploadFile(image.png),
    UploadFile(resume.pdf)
]
```

---

## Create Empty List

```python
uploaded_files = []
```

This stores metadata for every uploaded file.

---

## Loop Through Files

```python
for file in files:
```

Each iteration processes one uploaded file.

Iteration 1

```
notes.pdf
```

Iteration 2

```
image.png
```

Iteration 3

```
resume.pdf
```

---

## Reuse Existing Upload Logic

```python
result = upload_file(file)
```

Instead of duplicating validation code, reuse the existing upload service.

Each file is:

- Extension validated
- MIME validated
- Size validated
- UUID generated
- Saved to disk

---

## Store Metadata

```python
uploaded_files.append(result)
```

Example:

```python
[
    {
        "original_filename": "notes.pdf",
        "stored_filename": "abc.pdf"
    },
    {
        "original_filename": "image.png",
        "stored_filename": "xyz.png"
    }
]
```

---

## Return Response

```python
return {
    "message": "Files uploaded successfully.",
    "files": uploaded_files
}
```

Example Response:

```json
{
    "message": "Files uploaded successfully.",
    "files": [
        {
            "original_filename": "notes.pdf",
            "stored_filename": "abc123.pdf"
        },
        {
            "original_filename": "image.png",
            "stored_filename": "xyz456.png"
        }
    ]
}
```

---

# Error Handling Strategies

There are two common approaches.

---

## Strategy 1 – Stop on First Error

Example:

```
lecture1.pdf     ✅
lecture2.pdf     ✅
virus.exe        ❌
lecture3.pdf
lecture4.pdf
```

Processing stops immediately.

Response:

```
Error
```

Remaining files are never uploaded.

Advantages:

- Simple implementation
- Useful when all files must succeed together

Disadvantages:

- Poor user experience
- User must upload everything again

---

## Strategy 2 – Partial Success (Recommended)

Example:

```
lecture1.pdf     ✅
lecture2.pdf     ✅
virus.exe        ❌
lecture3.pdf     ✅
lecture4.pdf     ✅
```

Valid files are uploaded.

Invalid files are skipped.

Example Response:

```json
{
    "uploaded": [
        "lecture1.pdf",
        "lecture2.pdf",
        "lecture3.pdf",
        "lecture4.pdf"
    ],
    "failed": [
        {
            "filename": "virus.exe",
            "reason": "Invalid file extension."
        }
    ]
}
```

Advantages:

- Better user experience
- No need to re-upload successful files
- Used by cloud storage systems

Examples:

- Google Drive
- Dropbox
- OneDrive

---

# When to Use Stop-on-Error

Some systems require all uploads to succeed.

Examples:

- Banking
- Financial Transactions
- Database Imports
- Order Processing

In these cases:

```
One Failure

↓

Rollback Everything
```

---

# When to Use Partial Success

Applications like:

- Google Drive
- Dropbox
- TesLearn
- LMS Platforms

should continue uploading valid files and report failed ones.

---

# Best Practices

- Use `list[UploadFile]` for multiple uploads.
- Reuse existing upload logic instead of duplicating code.
- Return metadata for every uploaded file.
- Consider partial success for better user experience.
- Validate every file independently.
- Keep upload logic inside the service layer.

---

# Note About Our Project

While implementing this phase, Swagger UI incorrectly displayed:

```
array<string>
```

instead of a file picker (`array<binary>`), even in a minimal FastAPI application.

Since:

- The endpoint code was correct.
- `python-multipart` was installed.
- The issue persisted outside the project.

This appears to be an environment or dependency issue rather than a coding issue.

The concept and implementation remain correct, and this issue can be revisited later in a fresh virtual environment.

---

# Key Takeaways

- Multiple uploads use `list[UploadFile]`.
- FastAPI automatically converts uploaded files into a list.
- Reuse existing upload logic for every file.
- Loop through each uploaded file.
- Store metadata for every successful upload.
- Return a list of uploaded files.
- Partial success is preferred for user-facing applications like TesLearn.
- Avoid duplicating validation logic by following the DRY principle.