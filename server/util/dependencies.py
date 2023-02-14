from starlite.datastructures import State
from ._types import GState

def provide_state(state: State) -> GState:
    return GState(**state.dict())