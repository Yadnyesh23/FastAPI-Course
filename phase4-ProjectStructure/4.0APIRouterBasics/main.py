from fastapi import FastAPI
from routers.student import router as students_router
from routers.teachers import router as teachers_router
app = FastAPI()

app.include_router(students_router)
app.include_router(teachers_router)