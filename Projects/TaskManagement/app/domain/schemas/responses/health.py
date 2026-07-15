from pydantic import BaseModel
from datetime import datetime

class HealthCheckResponse(BaseModel):
    status : str
    database : str
    message : str
    timestamp : datetime
    