from __future__ import annotations

import daft
from daft import DataFrame

from disco.catalog import Catalog
from disco.object import Tokenizer, Volume, Model, LSP, Validator

import os


class Disco:
    catalog: Catalog

    def __init__(self):
        self.catalog = Catalog()

    def from_config(path_to_config: str) -> Disco:
        slf = Disco()
        slf.catalog = Catalog._from_config(path_to_config)
        return slf

    def mount(self, volume: str, location: str):
        v = Volume(volume, location)
        self.catalog.put_volume(v)

    def put_object(self, name: str, obj: object):
        if isinstance(obj, Tokenizer):
            self.catalog.put_tokenizer(name, obj)
        elif isinstance(obj, Model):
            self.catalog.put_model(name, obj)
        elif isinstance(obj, LSP):
            self.catalog.put_lsp(obj)
        elif isinstance(obj, Validator):
            self.catalog.put_validator(obj)
        else:
            raise ValueError(f"Unsupported object type: {type(obj)}")


    def save(self, path: str):
        self.catalog._save(path)
        
    def read(self, path: str, **options) -> DataFrame:
        if "://" not in path:
            raise ValueError("path must include volume name in format 'volume://glob'")

        # get the volume
        volume_name, tail = path.split("://", 1)
        volume = self.catalog.get_volume(volume_name)

        # use explicit format or infer
        fmt = options.pop("format", None)
        if fmt is None:
            _, ext = os.path.splitext(tail)
            if ext:
                fmt = ext[1:]  # remove leading dot

        # resolve absolute glob using the volume
        glob = volume.resolve(tail)

        # Call appropriate daft reader based on format
        if fmt == "csv":
            return daft.read_csv(glob, **options)
        if fmt == "txt" or fmt == "txt":
            return daft.read_csv(glob, delimiter="¦", has_headers=False).select(daft.col("column_1").alias("text"))
        elif fmt == "parquet":
            return daft.read_parquet(glob, **options)
        elif fmt == "json" or fmt == "jsonl":
            return daft.read_json(glob, **options)
        elif fmt == "delta":
            return daft.read_deltalake(glob, **options)
        elif fmt == "hudi":
            return daft.read_hudi(glob, **options)
        elif fmt == "iceberg":
            return daft.read_iceberg(glob, **options)
        elif fmt == "sql":
            return daft.read_sql(glob, **options)
        elif fmt == "lance":
            return daft.read_lance(glob, **options)
        elif fmt == "warc":
            return daft.read_warc(glob, **options)
        else:
            raise ValueError(f"Unsupported format: {fmt}")


__all__ = [
    "Disco",
    "Tokenizer",
]
