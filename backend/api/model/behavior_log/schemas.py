from pydantic import BaseModel, Field, validator
from pydantic import ConfigDict
from datetime import datetime
from typing import Optional, List

class BehaviorLogCreate(BaseModel):
    employee_id: str
    pc_id: str
    timestamp: datetime
    event_type: str = Field(..., max_length=10)

    class Config:
        extra = "allow"

class BehaviorLogRead(BaseModel):
    event_id: str
    employee_id: str
    pc_id: str
    event_type: str
    timestamp: datetime

    class Config:
        orm_mode = True

class HttpLogCreate(BaseModel):
    url: str

class EmailLogCreate(BaseModel):
    to: List[str]
    cc: Optional[List[str]] = []
    bcc: Optional[List[str]] = []
    from_addr: str
    size: int
    attachment: int

    @validator("to", "cc", "bcc", pre=True)
    def convert_list_to_str(cls, value):
        if isinstance(value, list):
            return ",".join(value)
        return value

class DeviceLogCreate(BaseModel):
    activity: str

class LogonLogCreate(BaseModel):
    activity: str

class FileLogCreate(BaseModel):
    filename: str