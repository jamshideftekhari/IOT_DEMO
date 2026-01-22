from datetime import datetime

from pydantic import BaseModel


class MeasurementCreate(BaseModel):
    device_id: str
    temperature: float
    humidity: float


class MeasurementResponse(BaseModel):
    id: int
    device_id: str
    temperature: float
    humidity: float
    timestamp: datetime

    model_config = {"from_attributes": True}
