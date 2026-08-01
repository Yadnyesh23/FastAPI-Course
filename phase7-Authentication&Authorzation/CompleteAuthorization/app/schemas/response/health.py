from datetime import datetime

from pydantic import BaseModel
from pydantic.fields import Field


class HealthResponse(BaseModel):
    message: str = Field(description="Health check response")
    database : str = Field(description="database response")
    status : int = Field(description="Status code")
    timestamp : datetime = Field(description="Timestamp")

