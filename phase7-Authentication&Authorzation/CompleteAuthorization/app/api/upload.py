from app.services.upload import upload_file
from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/upload", tags=["Upload"])




@router.post("/uploadfile")
async def upload(file: UploadFile = File(...)):
    return upload_file(file)