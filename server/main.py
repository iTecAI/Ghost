from util.dependencies import provide_state
from util.constants import *
from util.exceptions import *
from util._types import PluginManifest
from util.plugin import PluginLoad
from tinydb import TinyDB
from starlite import Starlite, Provide, get, State
import dotenv
import os
import logging
import json
from controllers import *

dotenv.load_dotenv()

# Setup logging
logging.basicConfig(format=LOG_FMT, level=os.getenv("LOG_LEVEL", "INFO"))

def load_plugins(state: State):
    logging.info("Loading plugins...")

    with open(os.path.join(state.root, "config", "plugins.config.json")) as f:
        plugin_config = json.load(f)

    state.plugins = {}

    plugin_directories = os.listdir(os.path.join(state.root, "plugins"))
    for directory in plugin_directories:
        if os.path.exists(os.path.join(state.root, "plugins", directory, "manifest.json")):
            with open(os.path.join(state.root, "plugins", directory, "manifest.json"), "r") as f:
                manifest: PluginManifest = json.load(f)
            
            if manifest["name"] in plugin_config.keys():
                pconf = plugin_config[manifest["name"]]
            else:
                pconf = {}
            try:
                state.plugins[manifest["name"]] = PluginLoad(manifest, pconf, state, directory)
            except:
                logging.exception(f"Failed to load {manifest['name']} from {directory}")
        else:
            logging.warning(f"Plugin directory {directory} does not have a manifest.json, skipping")
            
def default_plugin_config(workdir: str):
    cpath = os.path.join(workdir, "config", "plugins.config.json")
    if not os.path.exists(cpath):
        with open(cpath, "w") as f:
            f.write("{}")
        

def startup(state: State):
    logging.info("Initializing application...")
    # Get working directory
    workdir = os.getenv("WORKING_DIRECTORY", "ghost_data")
    logging.debug(f"Set working directory to {workdir}")

    # Setup working directory
    os.makedirs(workdir, exist_ok=True)
    os.makedirs(os.path.join(workdir, "data"), exist_ok=True)
    os.makedirs(os.path.join(workdir, "data", "downloads"), exist_ok=True)
    os.makedirs(os.path.join(workdir, "config"), exist_ok=True)
    os.makedirs(os.path.join(workdir, "plugins"), exist_ok=True)
    logging.debug("Checked existence of required folders")

    # Write default config
    default_plugin_config(workdir)

    # Setup app state
    state.cache = TinyDB(os.path.join(workdir, "data", "cache.json"))
    state.sessions = TinyDB(os.path.join(workdir, "data", "sessions.json"))
    state.downloads = TinyDB(os.path.join(workdir, "data", "downloads.json"))
    state.root = workdir

    load_plugins(state)

    logging.debug("Setup application state")


@get("/")
async def get_app_info() -> dict:
    return {"version": VERSION, "app": APP_NAME, "repository": APP_REPOSITORY}


app = Starlite(
    on_startup=[startup],
    dependencies={"gstate": Provide(provide_state)},
    route_handlers=[get_app_info, SearchController],
    exception_handlers={
        Exception: HTTPExceptionHandler,
        ApplicationException: ApplicationExceptionHandler,
    },
)
