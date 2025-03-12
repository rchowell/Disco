from typing import Dict

import toml

from disco.object import LSP, Model, Tokenizer, Validator, Volume


class Catalog:
    def __init__(self):
        self.volumes: Dict[str, Volume] = {}
        self.models: Dict[str, Model] = {}
        self.tokenizers: Dict[str, Tokenizer] = {}
        self.lsps: Dict[str, LSP] = {}
        self.validators: Dict[str, Validator] = {}

    def get_volume(self, name: str) -> Volume:
        if name not in self.volumes:
            raise ValueError(f"Volume '{name}' not found")
        return self.volumes[name]

    def put_volume(self, volume: Volume) -> None:
        self.volumes[volume.name] = volume

    def get_model(self, model_id: str) -> Model:
        if model_id not in self.models:
            raise ValueError(f"Model '{model_id}' not found")
        return self.models[model_id]

    def put_model(self, model_id: str, model: Model) -> None:
        self.models[model_id] = model

    def get_tokenizer(self, tokenizer_id: str) -> Tokenizer:
        if tokenizer_id not in self.tokenizers:
            raise ValueError(f"Tokenizer '{tokenizer_id}' not found")
        return self.tokenizers[tokenizer_id]

    def put_tokenizer(self, tokenizer_id: str, tokenizer: Tokenizer) -> None:
        self.tokenizers[tokenizer_id] = tokenizer

    def get_lsp(self, lsp_id: str) -> LSP:
        if lsp_id not in self.lsps:
            raise ValueError(f"LSP '{lsp_id}' not found")
        return self.lsps[lsp_id]

    def put_lsp(self, lsp_id: str, lsp: LSP) -> None:
        self.lsps[lsp_id] = lsp

    def get_validator(self, validator_id: str) -> Validator:
        if validator_id not in self.validators:
            raise ValueError(f"Validator '{validator_id}' not found")
        return self.validators[validator_id]

    def put_validator(self, validator_id: str, validator: Validator) -> None:
        self.validators[validator_id] = validator

    def _save(self, filename: str) -> None:
        serialize_catalog(self, filename)

    @staticmethod
    def _from_config(filename: str):
        return deserialize_catalog(filename)


def serialize_catalog(catalog: Catalog, filename: str) -> None:
    data = {
        "volumes": {name: vol.__dict__ for name, vol in catalog.volumes.items()},
        "models": {id: model.__dict__ for id, model in catalog.models.items()},
        "tokenizers": {id: tok.__dict__ for id, tok in catalog.tokenizers.items()},
        "lsps": {id: lsp.__dict__ for id, lsp in catalog.lsps.items()},
        "validators": {id: val.__dict__ for id, val in catalog.validators.items()},
    }

    with open(filename, "w") as f:
        toml.dump(data, f)


def deserialize_catalog(filename: str) -> Catalog:
    with open(filename) as f:
        data = toml.load(f)

    catalog = Catalog()

    for oid, vol_data in data.get("volumes", {}).items():
        catalog.put_volume(Volume(**vol_data))

    for oid, model_data in data.get("models", {}).items():
        catalog.put_model(oid, Model(**model_data))

    for oid, tok_data in data.get("tokenizers", {}).items():
        catalog.put_tokenizer(oid, Tokenizer(**tok_data))

    for oid, lsp_data in data.get("lsps", {}).items():
        catalog.put_lsp(oid, LSP(**lsp_data))

    for oid, val_data in data.get("valoidators", {}).items():
        catalog.put_validator(oid, Validator(**val_data))

    return catalog
