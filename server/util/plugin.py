from ._types import PluginManifest, PluginEntrypoint, GState
from .exceptions import ApplicationException
from typing import Any
from .plugin_tools import PluginTemplate
import importlib
from types import ModuleType
import os
import subprocess
import sys
import logging


def normalize_plugin_name(name: str) -> str:
    allowed = "qwertyuiopasdfghjklzxcvbnm_"
    return [i if i in allowed else "_" for i in name.lower()]


class PluginLoadError(ImportError):
    pass


class PluginLoad:
    def __init__(self, manifest: PluginManifest, config: Any, state: GState, plugin_dir: str):
        logging.info(f"Loading plugin {manifest['name']}:{manifest['version']}")
        self.manifest = manifest
        self.config = config
        self.directory = plugin_dir
        self._install_deps()
        dlClass: type[PluginTemplate] = self._load(state)
        self.downloader = dlClass(self.config, self.manifest)
    
    def _install_deps(self):
        logging.debug(f"Loading requirements for plugin {self.name} : [{', '.join(self.manifest['requirements'])}]")
        if len(self.manifest["requirements"]) > 0:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", *self.manifest["requirements"]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                raise PluginLoadError(
                    f"Failed to load plugin due to dependency error; Skipping plugin {self.name}"
                )

    def _load(self, state: GState):
        logging.debug(f"Loading entrypoint code for plugin {self.name} : {self.manifest['entrypoint']['file']}:{self.manifest['entrypoint']['downloader']}")
        entrypoint = self.manifest["entrypoint"]
        internal_name = normalize_plugin_name(self.name)
        try:
            loader = importlib.machinery.SourceFileLoader(
                f"{internal_name}.{entrypoint['downloader']}",
                os.path.join(state.root, "plugins", self.directory, entrypoint["file"]),
            )
            spec = importlib.util.spec_from_loader(
                f"{internal_name}.{entrypoint['downloader']}", loader
            )
            module: ModuleType = importlib.util.module_from_spec(spec)
            loader.exec_module(module)
        except:
            raise PluginLoadError(
                f"Failed to load {entrypoint['downloader']} from {entrypoint['file']}; Skipping plugin {self.name}"
            )
        return getattr(module, entrypoint["downloader"])

    @property
    def name(self):
        return self.manifest["name"]
