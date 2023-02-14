from tinydb import TinyDB
from dataclasses import dataclass
from typing import TypedDict, Any

@dataclass
class GState:
    root: str
    cache: TinyDB
    sessions: TinyDB
    downloads: TinyDB
    plugins: dict[str, Any]

class PluginEntrypoint(TypedDict):
    file: str
    downloader: str

class PluginManifest(TypedDict):
    name: str
    icon: dict
    version: str
    author: str
    source: str
    filters: list
    downloadOptions: list
    entrypoint: PluginEntrypoint
    requirements: list[str]