from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.response.health import HealthResponse
from app.services.health import HealthCheckService

router = APIRouter(
    prefix='/api/v1',
    tags=['health']
)

@router.get('/health', response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    database = HealthCheckService(db).get_database()
    if database:
        database_status = "database running"
    else:
        database_status = "database not running"

    return HealthResponse(
        message='OK',
        database=database_status,
        status=200,
        timestamp=datetime.now()
    )


        