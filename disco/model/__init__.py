from abc import ABC, abstractmethod

from daft import DataType as dt
from daft import Series, udf


class Model(ABC):
    def infer(self, text: str) -> str:
        raise ValueError("This model does not support `infer`")

    def classify(self, text: str, labels: list[str]) -> str:
        raise ValueError("This model does not support `classify`")

    ###
    # make_ methods
    ###

    def _make_inferencer(
        self,
    ) -> object:
        @udf(return_dtype=dt.string())
        def closure(series: Series):
            return [self.infert(t) for t in series.to_pylist()]

        return closure

    def _make_classifier(self, labels: list[str]) -> object:
        @udf(return_dtype=dt.string())
        def closure(series: Series):
            return [self.classify(t, labels) for t in series.to_pylist()]

        return closure


__all__ = [
    "Model",
]
