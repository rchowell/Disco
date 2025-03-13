from __future__ import annotations

from disco.stream import Stream, Context, from_path
from disco.catalog import Catalog
from disco.object import Tokenizer, Volume, Model, LSP, Validator

import os


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

    def stream(self, path: str, codec: str | None = None) -> Stream:
        # volume prefix is required for now
        if "://" not in path:
            raise ValueError("path must include volume name e.g. 'volume://glob'")
        # get the volume
        volume_name, tail = path.split("://", 1)
        volume = self._catalog.get_volume(volume_name)
        #
        # use explicit format or infer
        if codec is None:
            _, ext = os.path.splitext(tail)
            if ext:
                codec = ext[1:]  # remove leading dot
        #
        # resolve absolute glob using the volume
        glob = volume.resolve(tail)
        #
        # build the stream context and read a frame
        ctx = Context(glob, codec, self._catalog)
        #
        return Stream(ctx, from_path(glob))


__all__ = [
    "Disco",
]
