from urllib.parse import urlparse
from datetime import datetime

from dramatiq.cli import main, make_argument_parser
from loguru import logger
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from sqlmodel import Session
from time import sleep
from uuid import uuid4
import random

from src.api.db import engine
from src.api.settings import settings
from src.domain.simulation import SimulationRequest, SimulationResult

redis_parameters = urlparse(settings.REDIS_URL)
redis_broker = RedisBroker(
    host=redis_parameters.hostname,
    port=redis_parameters.port,
    username=redis_parameters.username,
    password=redis_parameters.password,
    # Heroku Redis with TLS use self-signed certs, so we need to tinker a bit
    ssl=redis_parameters.scheme == "rediss",
    ssl_cert_reqs=None,
)
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def run_simulation(request_json: str):
    logger.info(f"Got new simulation request: {request_json}")
    request: SimulationRequest = SimulationRequest.parse_raw(request_json)
    request.created_at = datetime.now()
    sleep(3)
    result = SimulationResult(id=request.id, sharpe=random.random())
    logger.info(f"Simulation result ready: {result.json()}")
    with Session(engine) as session:
        session.add(request)
        session.add(result)
        session.commit()


if __name__ == '__main__':
    parser = make_argument_parser()
    command = [
        "--processes", "2",
        "--threads", "1",
        #"--verbose",
        "src.api.worker:redis_broker"
    ]
    args = parser.parse_args(command)
    main(args)
