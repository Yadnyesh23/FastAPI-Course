from fastapi import FastAPI
from phase4.APIRouterBasics.routers.student import router as students_router
from phase4.APIRouterBasics.routers.teachers import router as teachers_router
app = FastAPI()

app.include_router(students_router)
app.include_router(teachers_router)