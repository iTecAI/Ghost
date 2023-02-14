from tinydb import TinyDB
from dataclasses import dataclass

@dataclass
class GState:
    cache: TinyDB
    sessions: TinyDB