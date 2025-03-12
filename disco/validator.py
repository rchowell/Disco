from __future__ import annotations

import json
from abc import ABC, abstractmethod

from jsonschema.protocols import Validator as _JsonSchemaValidator
from jsonschema.validators import validator_for as _json_validator_for


class Validator(ABC):
    @staticmethod
    def from_json_schema(schema: str) -> Validator:
        return JsonSchemaValidator.from_str(schema)

    @abstractmethod
    def validate(self, input: str) -> bool: ...


class JsonSchemaValidator:
    _oid: str
    _validator: _JsonSchemaValidator

    def __init__(self):
        raise ValueError("Use from_str or from_path")

    @staticmethod
    def from_schema(schema: object) -> JsonSchemaValidator:
        v = JsonSchemaValidator.__new__(JsonSchemaValidator)
        v._validator = _json_validator_for(schema)(schema)
        return v

    @staticmethod
    def from_str(schema: str) -> JsonSchemaValidator:
        return JsonSchemaValidator.from_schema(json.loads(schema))

    @staticmethod
    def from_path(path: str) -> JsonSchemaValidator:
        with open(path) as f:
            schema = f.read()
        return JsonSchemaValidator.from_str(schema)

    @abstractmethod
    def validate(self, input: str) -> bool:
        document = json.loads(input)
        errors = list(self._validator.iter_errors(document))
        return len(errors) == 0


__all__ = [
    "Validator",
]
