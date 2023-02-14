from typing import Any, Callable, TypedDict, Optional, Literal, Union
from ._types import GState, PluginManifest
from .exceptions import ApplicationException
from starlite.status_codes import *
import os, uuid
from tinydb import where

class PluginFeatureNotImplemented(ApplicationException):
    def __init__(self, error_message: Optional[str] = "An unknown error occurred.") -> None:
        super().__init__(HTTP_501_NOT_IMPLEMENTED, "error.plugin.featureNotImplemented", error_message)

class DownloadNotFound(ApplicationException):
    def __init__(self, id: str) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "error.download.not_found", f"Download {id} not found")

class DownloadStateInvalid(ApplicationException):
    def __init__(self, reason: str) -> None:
        super().__init__(HTTP_405_METHOD_NOT_ALLOWED, "error.download.complete", reason)

class DownloadEntity(TypedDict):
    download_id: str
    state: Literal["downloading", "processing", "complete"]
    metadata: dict[str, Any]
    root_file: str

class PluginResult(TypedDict):
    id: str
    title: str
    thumbnail: Union[str, None]

# Search Hook : (self, search_term: str, filters: {filter: value}) -> PluginResult[]
PluginHook_Search = Callable[["PluginTemplate", str, list[Any]], dict[str, Any]]

# Download Hook : (self, result: PluginResult, state: GState, target_directory: str) -> {metadata}
PluginHook_Download = Callable[["PluginTemplate", PluginResult, GState, str], dict[str, Any]]

# Progress Hook : (self, download: DownloadEntity, state: GState) -> float progress (0-100)
PluginHook_Progress = Callable[["PluginTemplate", DownloadEntity, GState], float]

# DownloadComplete Hook : (self, download: DownloadEntity, state: GState) -> DownloadEntity (root_file or metadata possibly modified)
PluginHook_DownloadComplete = Callable[["PluginTemplate", DownloadEntity, GState], DownloadEntity]

class PluginTemplate:
    hook_search: PluginHook_Search = None
    hook_download: PluginHook_Download = None
    hook_progress: PluginHook_Progress = None
    hook_download_complete: PluginHook_DownloadComplete = None
    def __init__(self, config: dict, manifest: PluginManifest) -> None:
        self.config = config
        self.manifest = manifest
    def search(self, search: str, filters: dict) -> list[PluginResult]:
        if not self.hook_search:
            raise PluginFeatureNotImplemented(error_message=f"Search is not implemented for plugin {self.manifest['name']}")
        return self.hook_search(search, filters)
    def download(self, result: PluginResult, state: GState) -> DownloadEntity:
        if not self.hook_download:
            raise PluginFeatureNotImplemented(error_message=f"Download is not implemented for plugin {self.manifest['name']}")
        download_id = uuid.uuid4().hex
        download_path = os.path.join(state.root, "data", "downloads", download_id)
        metadata = self.hook_download(result, state, download_path)
        return DownloadEntity(download_id=download_id, metadata=metadata, root_file=download_path, state="downloading")
    def progress(self, download_id: Any, state: GState) -> float:
        if not self.hook_progress:
            raise PluginFeatureNotImplemented(error_message=f"Progress is not implemented for plugin {self.manifest['name']}")
        results: list[DownloadEntity] = state.downloads.search(where("download_id") == download_id)
        if len(results) == 0:
            raise DownloadNotFound(download_id)
        if results[0]["state"] != "downloading":
            raise DownloadStateInvalid(f"Cannot get progress of non-downloading file {download_id}")
        return self.hook_progress(results[0], state)
    def download_complete(self, download_id: Any, state: GState) -> DownloadEntity:
        if not self.hook_progress:
            raise PluginFeatureNotImplemented(error_message=f"DownloadComplete is not implemented for plugin {self.manifest['name']}")
        results: list[DownloadEntity] = state.downloads.search(where("download_id") == download_id)
        if len(results) == 0:
            raise DownloadNotFound(download_id)
        if results[0]["state"] != "downloading":
            raise DownloadStateInvalid(f"Cannot postprocess non-downloading file {download_id}")
        results[0]["state"] = "processing"
        results[0] = self.hook_download_complete(results[0], state)
        results[0]["state"] = "complete"
        return results[0]