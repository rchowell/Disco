from disco.tokenizer import Tokenizer
from disco.validator import Validator
from disco.volume import Volume


class Model:
    def __init__(self, id: str):
        self.id = id


class LSP:
    def __init__(self, id: str, language: str):
        self.id = id
        self.language = language


__all__ = [
    "Tokenizer",
    "Validator",
    "Volume",
]
