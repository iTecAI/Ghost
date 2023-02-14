from typing import Any, Callable
from ._types import GState

PluginHook_Search = Callable[["PluginTemplate", str, list[Any]], list[Any]]
PluginHook_Download = Callable[["PluginTemplate", Any, GState], dict[str, Any]]
PluginHook_Progress = Callable[["PluginTemplate", Any, GState], dict[str, Any]]

class PluginTemplate:
    def __init__(self, config: dict) -> None:
        pass
    def search(self, search: str, filters: list, state: GState) -> list[Any]:
        raise NotImplementedError
    def download(self, identifier: Any, state: GState) -> Any:
        raise NotImplementedError
    def progress(self, download_id: Any, state: GState) -> float:
        raise NotImplementedError