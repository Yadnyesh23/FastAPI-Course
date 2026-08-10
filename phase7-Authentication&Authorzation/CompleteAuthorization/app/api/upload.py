from app.services.upload import upload_file
from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/uploadfile")
async def upload(file: UploadFile = File(...)):
    return upload_file(file)


# @router.post("/multiple")
# async def upload_multiple_files(
#     files: list[UploadFile] = File(...)
# ):
#     uploaded_files = []

#     for file in files:
#         result = upload_file(file)
#         uploaded_files.append(result)

#     return {
#         "message": "Files uploaded successfully.",
#         "files": uploaded_files
#     }

# @router.post('/download')
# async def download(filename: str):
#     return download_file(filename)
    
# @router.post('/delete')
# async def delete(filename: str):
#     return delete_file(filename)