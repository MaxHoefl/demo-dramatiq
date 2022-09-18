import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse
from pydantic import UUID4
from sqlmodel import Session
from loguru import logger

from src.api.db import create_db_and_tables, engine
from src.domain.simulation import SimulationRequest, SimulationResult
from src.api.worker import run_simulation

app = FastAPI()


@app.post("/sim", status_code=status.HTTP_202_ACCEPTED, response_model=SimulationRequest)
def submit_simulation_request(sim_request: SimulationRequest):
    logger.info("Creating new simulation request")
    run_simulation.send(sim_request.json())
    return sim_request


@app.get("/sim/{id}", response_model=SimulationResult)
def get_simulation_result(id: str):
    logger.info("Retrieving simulation result")
    with Session(engine) as session:
        result = session.get(SimulationResult, id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return result


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


if __name__ == '__main__':
    uvicorn.run("src.api.server:app", port=5000, log_level="info")
