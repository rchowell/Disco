from disco.model import Model
from disco.tokenizer import Tokenizer
from disco.validator import Validator
from disco.volume import Volume


class LSP:
    def __init__(self, id: str, language: str):
        self.id = id
        self.language = language


__all__ = [
    "Model",
    "Tokenizer",
    "Validator",
    "Volume",
]
