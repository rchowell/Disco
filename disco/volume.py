import os


class Volume:
    """Volume is used as an alias to form an absolute path."""

    name: str
    location: str

    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location

    def resolve(self, glob: str) -> str:
        return os.path.join(self.location, glob)
