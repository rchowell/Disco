from __future__ import annotations

import json
from abc import ABC, abstractmethod

from jsonschema.protocols import Validator as _JsonSchemaValidator
from jsonschema.validators import validator_for as _json_validator_for
from pydantic import BaseModel, PositiveInt

from typing import Type

class Validator(ABC):
    @staticmethod
    def from_json_schema(schema: str) -> Validator:
        return JsonSchemaValidator.from_str(schema)
        
    @staticmethod
    def from_pydantic_model(model: Type[BaseModel]) -> Validator:
        return PydanticValidator(model)

    @abstractmethod
    def validate(self, input: object) -> bool: ...


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

class PydanticValidator(Validator):
    
    def __init__(self, model: Type[BaseModel]):
        self.model = model
        
    def validate(self, input: object) -> bool:
        try:
            self.model.model_validate(input)
            return True
        except Exception as e:
            return False
        
    
__all__ = [
    "Validator",
]
