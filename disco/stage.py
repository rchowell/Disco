from __future__ import annotations

from daft import DataFrame, col

from disco.catalog import Catalog

Context = Catalog


class Stage:
    """Stages have multiple columns and are effectively just DataFrames."""

    _context: Context
    _frame: DataFrame

    def __init__(self, context: Context, frame: DataFrame):
        self._context = context
        self._frame = frame

    def stream(self, column: str | None = None) -> Stream:
        if column is None:
            cols = self._frame.column_names
            if len(cols) != 1:
                raise ValueError(f"Stage has more than one column: {', '.join(cols)}")
            column = cols[0]
        return Stream(self._context, self._frame.select(col(column).alias("stream")))

    def show(self):
        self._inner.show()


class Stream:
    """Streams have a single column defined by the alias, eventually we want row-values."""

    _context: Context
    _frame: DataFrame

    def __init__(self, context: Context, frame: DataFrame):
        self._context = context
        self._frame = frame

    def show(self):
        self._frame.show()
