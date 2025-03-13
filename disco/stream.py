from __future__ import annotations

import daft
from daft import DataFrame, Expression, Series, udf
from daft import DataType as dt

from disco.catalog import Catalog


def from_path(path: str) -> DataFrame:
    """Returns a new DataFrame form the path."""
    return daft.from_glob_path(path).with_column("bytes", _read_blob(daft.col("path")))


@udf(return_dtype=dt.binary())
def _read_blob(files: Series):
    output = []
    for file in files.to_pylist():
        file = file.replace("file://", "")
        with open(file, "rb") as f:
            output.append(f.read())
    return output


class Context:
    """Stream context is shared across composed streams."""

    _col: Expression
    _glob: str
    _codec: str
    _catalog: Catalog

    def __init__(self, glob: str, codec: str, catalog: Catalog):
        self._col = daft.col("bytes")
        self._glob = glob
        self._codec = codec
        self._catalog = catalog


class Stream:
    """Streams are a special kind of daft frame with a bytes column."""

    _ctx: Context
    _frame: DataFrame

    def __init__(self, ctx: Context, frame: DataFrame):
        self._ctx = ctx
        self._frame = frame

    def _map(self, expr: Expression) -> Stream:
        frame = self._frame.select(expr.alias("bytes"))
        return Stream(self._ctx, frame)

    def encode(self, codec: str) -> Stream:
        col = self._ctx._col
        catalog = self._ctx._catalog
        encoder = None
        try:
            encoder = catalog.get_tokenizer(codec).encoder()(col)
        except ValueError:
            encoder = Expression.encode(col, codec)
        return self._map(encoder)

    def decode(self, codec: str) -> Stream:
        return self._map(Expression.decode(self._col, codec))

    def raw(self) -> bytes:
        raise ValueError("Returning raw byte stream not supported.")

    def read(self, **options) -> DataFrame:
        """Read the stream bytes as a daft frame."""
        codec = self._ctx._codec
        glob = self._ctx._glob
        if codec == "csv":
            return daft.read_csv(glob, **options)
        elif codec == "parquet":
            return daft.read_parquet(glob, **options)
        elif codec == "json" or codec == "jsonl":
            return daft.read_json(glob, **options)
        elif codec == "delta":
            return daft.read_deltalake(glob, **options)
        elif codec == "hudi":
            return daft.read_hudi(glob, **options)
        elif codec == "iceberg":
            return daft.read_iceberg(glob, **options)
        elif codec == "sql":
            return daft.read_sql(glob, **options)
        elif codec == "lance":
            return daft.read_lance(glob, **options)
        elif codec == "warc":
            return daft.read_warc(glob, **options)
        else:
            raise ValueError(f"Reading `{codec}` as a daft DataFrame is currently not supported.")

    def show(self):
        self._frame.show()
