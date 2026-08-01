from sqlalchemy import text
from sqlalchemy.orm import Session


class HealthCheckService:
    def __init__(self, db: Session):
        self.db = db

    def get_database(self) -> bool:
        try:
            self.db.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Error : {e}")
            return False