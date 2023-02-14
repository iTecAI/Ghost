from tinydb import TinyDB
from dataclasses import dataclass
from typing import TypedDict

@dataclass
class GState:
    cache: TinyDB
    sessions: TinyDB

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