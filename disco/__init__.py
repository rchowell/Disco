from __future__ import annotations

from daft import DataFrame

from disco.stream import Stream, Context, read_stream, read_frame
from disco.catalog import Catalog
from disco.object import Tokenizer, Volume, Model, LSP, Validator


class Disco:
    _catalog: Catalog

    def __init__(self):
        self._catalog = Catalog()

    @staticmethod
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
        self._catalog._save(path)

    def resolve(self, path: str) -> str:
        # volume prefix is required for now
        if "://" not in path:
            raise ValueError("path must include volume name e.g. 'volume://glob'")
        # get the volume
        volume_name, tail = path.split("://", 1)
        volume = self._catalog.get_volume(volume_name)
        # resolve absolute glob using the volume
        return volume.resolve(tail)

    def stream(self, path: str, codec: str | None = None) -> Stream:
        # resolve absolute glob using the volume
        glob = self.resolve(path)
        # build the stream context and read a frame
        return read_stream(glob, codec, Context(glob, self._catalog))

    def read(self, path: str, codec: str | None = None, **options) -> DataFrame:
        # resolve absolute glob using the volume
        glob = self.resolve(path)
        # build the dataframe using daft's read methods
        return read_stream(glob, codec, **options)


__all__ = [
    "Disco",
]
