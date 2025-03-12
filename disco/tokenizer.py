from abc import ABC

class Tokenizer(ABC):
    def __init__(self, id: str):
        self.id = id

    def encode(self, data: str) -> list:
        ...
    
    def decode(self, data: list) -> str:
        ...