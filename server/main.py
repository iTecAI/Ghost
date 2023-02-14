from util.dependencies import provide_state
from util.constants import *
from util.exceptions import *
from tinydb import TinyDB
from starlite import Starlite, Provide, get, State
import dotenv
import os
import logging

dotenv.load_dotenv()

# Setup logging
logging.basicConfig(format=LOG_FMT, level=os.getenv("LOG_LEVEL", "INFO"))


def startup(state: State):
    logging.info("Initializing application...")
    # Get working directory
    workdir = os.getenv("WORKING_DIRECTORY", "ghost_data")
    logging.debug(f"Set working directory to {workdir}")

    # Setup working directory
    os.makedirs(workdir, exist_ok=True)
    os.makedirs(os.path.join(workdir, "data"), exist_ok=True)
    os.makedirs(os.path.join(workdir, "config"), exist_ok=True)
    logging.debug("Checked existence of required folders")

    # Setup app state
    state.cache = TinyDB(os.path.join(workdir, "data", "cache.json"))
    state.sessions = TinyDB(os.path.join(workdir, "data", "sessions.json"))
    logging.debug("Setup application state")


@get("/")
async def get_app_info() -> dict:
    return {"version": VERSION, "app": APP_NAME, "repository": APP_REPOSITORY}


app = Starlite(
    on_startup=[startup],
    dependencies={"gstate": Provide(provide_state)},
    route_handlers=[get_app_info],
    exception_handlers={
        Exception: HTTPExceptionHandler,
        ApplicationException: ApplicationExceptionHandler,
    },
)
