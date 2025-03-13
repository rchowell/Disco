from abc import ABC, abstractmethod

from disco.tokenizer import Tokenizer
from disco.validator import Validator
from disco.volume import Volume


class Model(ABC):
    def __init__(self, id: str):
        self.id = id

    @abstractmethod
    def classify(self, text: str, labels: list[str]) -> str: ...


class LSP:
    def __init__(self, id: str, language: str):
        self.id = id
        self.language = language


__all__ = [
    "Tokenizer",
    "Validator",
    "Volume",
]
