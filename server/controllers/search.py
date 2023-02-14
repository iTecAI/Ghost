from starlite import Controller, get
from util._types import GState

class SearchController(Controller):
    path = "/search"

    @get("")
    async def search(self, gstate: GState, q: str) -> list:
        results = []
        for p in gstate.plugins.values():
            results.extend(p.downloader.search(q, {}))
        return results