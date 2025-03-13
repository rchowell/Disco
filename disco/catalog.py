from typing import Dict

import toml

from disco.object import Grammar, Model, Tokenizer, Validator, Volume


class Catalog:
    def __init__(self):
        self.volumes: Dict[str, Volume] = {}
        self.models: Dict[str, Model] = {}
        self.tokenizers: Dict[str, Tokenizer] = {}
        self.grammars: Dict[str, Grammar] = {}
        self.validators: Dict[str, Validator] = {}

    def get_volume(self, name: str) -> Volume:
        if name not in self.volumes:
            raise ValueError(f"Volume '{name}' not found")
        return self.volumes[name]

    def put_volume(self, volume: Volume) -> None:
        self.volumes[volume.name] = volume

    def get_model(self, oid: str) -> Model:
        if oid not in self.models:
            raise ValueError(f"Model '{oid}' not found")
        return self.models[oid]

    def put_model(self, oid: str, model: Model) -> None:
        self.models[oid] = model

    def get_tokenizer(self, oid: str) -> Tokenizer:
        if oid not in self.tokenizers:
            raise ValueError(f"Tokenizer '{oid}' not found")
        return self.tokenizers[oid]

    def put_tokenizer(self, oid: str, tokenizer: Tokenizer) -> None:
        self.tokenizers[oid] = tokenizer

    def get_grammar(self, oid: str) -> Grammar:
        if oid not in self.grammars:
            raise ValueError(f"Grammar '{oid}' not found")
        return self.grammars[oid]

    def put_grammar(self, oid: str, grammar: Grammar) -> None:
        self.grammars[oid] = grammar

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
        "grammars": {id: grammar.__dict__ for id, grammar in catalog.grammars.items()},
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

    for oid, grammar_data in data.get("grammars", {}).items():
        catalog.put_grammar(oid, Grammar(**grammar_data))

    for oid, val_data in data.get("validators", {}).items():
        catalog.put_validator(oid, Validator(**val_data))

    return catalog
