from starlite import Controller, post
from util._types import GState, SearchModel

class SearchController(Controller):
    path = "/search"

    @post("/{plugin_name:str}")
    async def search(self, gstate: GState, data: SearchModel, plugin_name: str) -> list:
        return []