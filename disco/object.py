from abc import ABC, abstractmethod

from disco.tokenizer import Tokenizer
from disco.volume import Volume


class Model:
    def __init__(self, id: str):
        self.id = id


class LSP:
    def __init__(self, id: str, language: str):
        self.id = id
        self.language = language


class Validator(ABC):
    def __init__(self, id: str, domain: str):
        self.id = id
        self.domain = domain

    @abstractmethod
    def validate(self) -> bool: ...


__all__ = [
    "Tokenizer",
    "Volume",
]
