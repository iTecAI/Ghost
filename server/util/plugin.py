from ._types import PluginManifest, PluginEntrypoint
from .exceptions import ApplicationException
from typing import Any
    

def load_entrypoint(entrypoint: PluginEntrypoint):
    pass

class Plugin:
    def __init__(self, manifest: PluginManifest):
        self.manifest = manifest
    
    @property
    def name(self):
        return self.manifest['name']