import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field


class SimulationRequest(SQLModel, table=True):
    id: str = Field(default=str(uuid.uuid4()), primary_key=True)
    horizon: int = Field(default=10)
    created_at: datetime = Field(default=datetime.now())


class SimulationResult(SQLModel, table=True):
    id: str = Field(default=str(uuid.uuid4()), primary_key=True)
    sharpe: float = Field(default=0)