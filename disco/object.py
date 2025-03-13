from abc import ABC, abstractmethod

from daft import DataType as dt
from daft import Series, udf

from disco.tokenizer import Tokenizer
from disco.validator import Validator
from disco.volume import Volume


class Model(ABC):
    def __init__(self, id: str):
        self.id = id

    @abstractmethod
    def classify(self, text: str, labels: list[str]) -> str: ...

    def make_classifier(self, labels: list[str]) -> object:
        @udf(return_dtype=dt.string())
        def closure(series: Series):
            return [self.classify(t, labels) for t in series.to_pylist()]

        return closure


class LSP:
    def __init__(self, id: str, language: str):
        self.id = id
        self.language = language


__all__ = [
    "Tokenizer",
    "Validator",
    "Volume",
]
