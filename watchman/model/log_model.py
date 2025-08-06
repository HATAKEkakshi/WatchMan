from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogRequest(BaseModel):
    service: Optional[str] = None
    level: str = "INFO"
    message: str
    metadata: Optional[str] = None

class LogResponse(BaseModel):
    id: str
    service: str
    level: str
    message: str
    timestamp: datetime
    metadata: Optional[str] = None

class QueryRequest(BaseModel):
    query: str
    service: Optional[str] = None
    limit: int = 10