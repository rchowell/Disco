from abc import ABC, abstractmethod

from daft import DataType as dt
from daft import Series, udf


class Model(ABC):
    @abstractmethod
    def classify(self, text: str, labels: list[str]) -> str: ...

    def make_classifier(self, labels: list[str]) -> object:
        @udf(return_dtype=dt.string())
        def closure(series: Series):
            return [self.classify(t, labels) for t in series.to_pylist()]

        return closure


__all__ = [
    "Model",
]
