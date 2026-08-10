# Upload, download and delete the file locally
from pathlib import Path
import shutil
import uuid

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse

# Directory where uploaded files will be stored
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".txt",
}

# Allowed MIME (content) types
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
    """Validate and save an uploaded file."""

    # Extract the file extension
    extension = Path(file.filename).suffix.lower()

    # Validate file extension
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file extension."
        )

    # Validate MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid MIME type."
        )

    # Calculate file size without saving it
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    # Validate file size
    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10 MB."
        )

    # Generate a unique filename to avoid collisions
    unique_filename = f"{uuid.uuid4()}{extension}"

    # Create the complete destination path
    file_path = UPLOAD_DIR / unique_filename

    # Save the uploaded file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Return uploaded file metadata
    return {
        "original_filename": file.filename,
        "stored_filename": unique_filename,
        "content_type": file.content_type,
        "path": str(file_path),
        "size": size,
    }

    # Define directory where uploaded files will be stored
    # Define allowed file extensions
    # Define allowed MIME (content) types
    # Define maximum allowed file size 
    # Extract the file extension
    # Validate file extension
    # Validate MIME type
    # Calculate file size without saving it
    # Validate file size
    # Generate a unique filename to avoid collisions
    # Create the complete destination path
    # Save the uploaded file to disk
    # Return uploaded file metadata

def download_file(filename: str):
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )
        
    return FileResponse(
        path=file_path,
        filename=filename
    )

def delete_file(filename:str):
    file_path = UPLOAD_DIR/filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )
        
    file_path.unlink()
    
    return {
        "message": "File deleted successfully."
    }