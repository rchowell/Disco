from __future__ import annotations

from disco.stage import Stage
from disco.catalog import Catalog
from disco.object import Tokenizer, Volume, Model, LSP, Validator

import os


class Disco:
    _catalog: Catalog

    def __init__(self):
        self._catalog = Catalog()

    def from_config(path_to_config: str) -> Disco:
        slf = Disco()
        slf.catalog = Catalog._from_config(path_to_config)
        return slf

    def mount(self, volume: str, location: str):
        v = Volume(volume, location)
        self._catalog.put_volume(v)

    def put_object(self, oid: str, obj: object):
        if isinstance(obj, Tokenizer):
            self._catalog.put_tokenizer(oid, obj)
        elif isinstance(obj, Model):
            self._catalog.put_model(oid, obj)
        elif isinstance(obj, LSP):
            self._catalog.put_lsp(obj)
        elif isinstance(obj, Validator):
            self._catalog.put_validator(obj)
        else:
            raise ValueError(f"Unsupported object type: {type(obj)}")

    def save(self, path: str):
        self.catalog._save(path)

    def read(self, path: str, **options) -> Stage:
        import daft

        if "://" not in path:
            raise ValueError("path must include volume name in format 'volume://glob'")

        # get the volume
        volume_name, tail = path.split("://", 1)
        volume = self._catalog.get_volume(volume_name)

        # use explicit format or infer
        fmt = options.pop("format", None)
        if fmt is None:
            _, ext = os.path.splitext(tail)
            if ext:
                fmt = ext[1:]  # remove leading dot

        # resolve absolute glob using the volume
        glob = volume.resolve(tail)

        # read into a daft DataFrame
        frame = None
        if fmt == "csv":
            frame = daft.read_csv(glob, **options)
        if fmt == "txt" or fmt == "text":
            frame = daft.read_csv(glob, delimiter="¦", has_headers=False).select(daft.col("column_1").alias("text"))
        elif fmt == "parquet":
            frame = daft.read_parquet(glob, **options)
        elif fmt == "json" or fmt == "jsonl":
            frame = daft.read_json(glob, **options)
        elif fmt == "delta":
            frame = daft.read_deltalake(glob, **options)
        elif fmt == "hudi":
            frame = daft.read_hudi(glob, **options)
        elif fmt == "iceberg":
            frame = daft.read_iceberg(glob, **options)
        elif fmt == "sql":
            frame = daft.read_sql(glob, **options)
        elif fmt == "lance":
            frame = daft.read_lance(glob, **options)
        elif fmt == "warc":
            frame = daft.read_warc(glob, **options)
        else:
            raise ValueError(f"Unsupported format: {fmt}")

        return Stage(self._catalog, frame)


__all__ = [
    "Disco",
]
