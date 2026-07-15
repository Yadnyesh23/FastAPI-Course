from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.domain.schemas.responses.health import HealthCheckResponse

class HealthCheckService:

    @staticmethod
    def check_db(db: Session) -> dict:
        try:
            db.execute(text("SELECT 1"))

            return HealthCheckResponse(
                status = "Healthy",
                database = "Connected",
                message =  "Database connection is healthy.",
                timestamp=datetime.now(timezone.utc)
            )

        except Exception as e:
            return HealthCheckResponse(
                status = "unhealthy",
                database = "disconnected",
                message = str(e),
                timestamp=datetime.now(timezone.utc)
            )

