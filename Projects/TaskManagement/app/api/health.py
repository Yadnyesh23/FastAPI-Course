from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.database.database import get_db
from app.services.health import HealthCheckService

router = APIRouter(
    prefix="/health",
    tags=['health']
)

    
@router.get("/")
def health_check(db: Session = Depends(get_db)):
    """
    Health check for database connection and
    api flow.
    """
    result = HealthCheckService.check_db(db)

    if result.status == "unhealthy":
        raise HTTPException(
            status_code=503,
            detail=result
        )

    return result