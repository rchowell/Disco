from abc import ABC, abstractmethod


class Volume:
    name: str

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def resolve(self, glob: str) -> str:
        return self.path + glob


class Model:
    def __init__(self, id: str):
        self.id = id



class LSP:
    def __init__(self, id: str, language: str):
        self.id = id
        self.language = language


class Validator(ABC):
    def __init__(self, id: str, domain: str):
        self.id = id
        self.domain = domain

    @abstractmethod
    def validate(self) -> bool: ...
