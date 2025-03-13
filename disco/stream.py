from __future__ import annotations

import os
from abc import ABC, abstractmethod

import daft
from daft import DataFrame, Expression, Series, udf
from daft import DataType as dt

from disco.catalog import Catalog


def infer_mime(path: str) -> str:
    _, ext = os.path.splitext(path)
    if ext:
        return ext[1:]  # remove leading dot
    else:
        raise ValueError("Could not infer mimetype, no extension found.")


def read_stream(glob: str, mime: str | None, ctx: Context) -> Stream:
    """Returns a new DataFrame from the path."""
    mime = mime or infer_mime(glob)
    frame = daft.from_glob_path(glob).with_column("bytes", _read_blob(daft.col("path")))
    return Stream(ctx, mime, frame)


def read_frame(glob: str, mime: str | None = None, **options) -> DataFrame:
    mime = mime or infer_mime(glob)
    if mime == "csv":
        return daft.read_csv(glob, **options)
    elif mime == "txt" or mime == "text":
        return daft.read_csv(glob, delimiter="¦", has_headers=False).select(daft.col("column_1").alias("text"))
    elif mime == "parquet":
        return daft.read_parquet(glob, **options)
    elif mime == "json" or mime == "jsonl":
        return daft.read_json(glob, **options)
    elif mime == "delta":
        return daft.read_deltalake(glob, **options)
    elif mime == "hudi":
        return daft.read_hudi(glob, **options)
    elif mime == "iceberg":
        return daft.read_iceberg(glob, **options)
    elif mime == "sql":
        return daft.read_sql(glob, **options)
    elif mime == "lance":
        return daft.read_lance(glob, **options)
    elif mime == "warc":
        return daft.read_warc(glob, **options)
    else:
        raise ValueError(f"Reading `{mime}` as a daft DataFrame is currently not supported.")


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
    _catalog: Catalog

    def __init__(self, glob: str, catalog: Catalog):
        self._col = daft.col("bytes")
        self._glob = glob
        self._catalog = catalog


class Stream:
    """Streams are a special kind of daft frame with a bytes column."""

    _ctx: Context
    _mime: str
    _frame: DataFrame

    def __init__(self, ctx: Context, mime: str, frame: DataFrame):
        self._ctx = ctx
        self._mime = mime
        self._frame = frame

    def _transform(self, codec: str, expr: Expression) -> Stream:
        """Apply some stream transformation."""
        frame = self._frame.select(expr.alias("bytes"))
        return Stream(self._ctx, codec, frame)

    def encode(self, codec: str) -> Stream:
        """Encode this stream using the tokenizer or codec."""
        col = self._ctx._col
        catalog = self._ctx._catalog
        encoder = None
        try:
            encoder = catalog.get_tokenizer(codec).make_encoder()(col)
        except ValueError:
            encoder = Expression.encode(col, codec)
        return self._transform(codec, encoder)

    def decode(self, codec: str) -> Stream:
        """Decode this stream using the tokenizer or codec."""
        col = self._ctx._col
        catalog = self._ctx._catalog
        decoder = None
        try:
            decoder = catalog.get_tokenizer(codec).make_decoder()(col)
        except ValueError:
            decoder = Expression.decode(col, codec)
        return self._transform(codec, decoder)

    def map(self, f) -> DataFrame:
        """Apply the mapping function to produce a DataFrame."""

        @udf(return_dtype=dt.binary())
        def _func(series: Series):
            return [f(s) for s in series.to_pylist()]

        return self._frame.select(_func(self._ctx._col))

    def transform(self, transform: Transform) -> DataFrame:
        """Apply the transform function, producing a DataFrame."""
        # close over the transform with a new udf
        typ_: dict[str, any] = transform.type()

        @udf(return_dtype=dt._infer_type(typ_))
        def _func(series: Series):
            return [transform.apply(v, None) for v in series.to_pylist()]

        # invoke the transform on bytes, collecting additional metadata (todo)
        rc = daft.col("row")
        df = self._frame.select(_func(self._ctx._col).alias("row"))
        # project out all the struct fields for multi-column projectionpfor
        return df.select(*[rc.struct.get(field) for field in typ_.keys()])

    def raw(self) -> bytes:
        raise ValueError("Returning raw byte stream not supported.")

    def read(self, **options) -> DataFrame:
        """Read the stream bytes as a daft frame."""
        return read_frame(self._ctx._glob, self._mime, **options)

    def parse(self, pattern: str) -> DataFrame:
        raise ValueError("Parsing not yet supported.")

    def show(self):
        self._frame.show()


class Transform(ABC):
    """Transform is used for higher-level UDFs and multi-column projections from streams."""

    @abstractmethod
    def type(self) -> dict[str, type]: ...

    @abstractmethod
    def apply(self, stream: bytes, metadata: dict[str, any] | None) -> dict: ...


__all__ = [
    "Context",
    "Stream",
    "Transform",
    "read_frame",
    "read_stream",
]
