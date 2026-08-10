from pathlib import Path
import uuid

from fastapi import HTTPException, UploadFile

from app.core.imagekit import imagekit


# Allowed file extensions
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".txt",
}

# Allowed MIME types
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/jpg",
    "image/png",
    "text/plain",
}

# Maximum allowed file size (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


def upload_file(file: UploadFile):
    """
    Validate and upload a file to ImageKit.
    """

    # -------------------------------
    # Validate Extension
    # -------------------------------
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file extension."
        )

    # -------------------------------
    # Validate MIME Type
    # -------------------------------
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid MIME type."
        )

    # -------------------------------
    # Validate File Size
    # -------------------------------
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10 MB."
        )

    # -------------------------------
    # Generate Unique Filename
    # -------------------------------
    unique_filename = f"{uuid.uuid4()}{extension}"

    try:
        # -------------------------------
        # Upload to ImageKit
        # -------------------------------
        result = imagekit.upload_file(
            file=file.file,
            file_name=unique_filename,
            options={
                "folder": "/uploads"
            }
        )

        # -------------------------------
        # Return Upload Metadata
        # -------------------------------
        return {
            "original_filename": file.filename,
            "stored_filename": unique_filename,
            "content_type": file.content_type,
            "size": size,
            "file_id": result.file_id,
            "url": result.url,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ImageKit upload failed: {str(e)}"
        )