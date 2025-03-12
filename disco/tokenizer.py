from abc import ABC, abstractmethod

from daft import DataType as dt
from daft import Series, udf


class Tokenizer(ABC):
    @abstractmethod
    def encode(self, input: str) -> list: ...

    @abstractmethod
    def decode(self, input: list) -> str: ...

    def encoder(self) -> object:
        @udf(return_dtype=dt.list(dt.int64()))
        def closure(series: Series):
            return [self.encode(b) for b in series.to_pylist()]

        return closure
