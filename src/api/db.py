from sqlmodel import SQLModel, create_engine
from src.domain.simulation import SimulationResult, SimulationRequest
from src.api.settings import settings

engine = create_engine(settings.DB_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
