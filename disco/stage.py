from __future__ import annotations

from daft import DataFrame, Expression, col

from disco.catalog import Catalog

Context = Catalog


class Stage:
    """Stages have multiple columns and are effectively just DataFrames."""

    _context: Context
    _frame: DataFrame

    def __init__(self, context: Context, frame: DataFrame):
        self._context = context
        self._frame = frame

    def frame(self) -> DataFrame:
        return self._frame

    def stream(self, column: str | None = None) -> Stream:
        if column is None:
            cols = self._frame.column_names
            if len(cols) != 1:
                raise ValueError(f"Stage has more than one column: {', '.join(cols)}")
            column = cols[0]
        return Stream(self._context, self._frame.select(col(column).alias("stream")))

    def show(self):
        self._frame.show()


class Stream:
    """Streams have a single column defined by the alias, eventually we want row-values."""

    _col: Expression
    _context: Context
    _frame: DataFrame

    def __init__(self, context: Context, frame: DataFrame):
        self._col = col("stream")
        self._context = context
        self._frame = frame

    def _map(self, expr: Expression) -> Stream:
        frame = self._frame.select(expr.alias("stream"))
        return Stream(self._context, frame)

    def encode(self, codec: str) -> Stream:
        encoder = None
        try:
            encoder = self._context.get_tokenizer(codec).encoder()(self._col)
        except ValueError:
            encoder = Expression.encode(self._col, codec)
        return self._map(encoder)

    def decode(self, codec: str) -> Stream:
        return self._map(Expression.decode(self._col, codec))

    def show(self):
        self._frame.show()
