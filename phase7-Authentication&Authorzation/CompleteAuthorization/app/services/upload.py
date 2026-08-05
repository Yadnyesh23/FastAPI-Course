from pathlib import Path
from fastapi import UploadFile, HTTPException
import shutil

UPLOAD_PATH = Path("uploads")
UPLOAD_PATH.mkdir(exist_ok=True)


def upload_file(file : UploadFile):
    try:
        file_path = UPLOAD_PATH / file.filename

        with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        return {
                "filename" : file.filename,
                "filetype" : file.content_type,
                "path" : file_path,
                "size" : round(file_path.stat().st_size / (1024 * 1024), 2),
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
