"""SEMANTIC CODE PROCESSING EXAMPLE.

Setup:

    We have some python scripts in a directory.

Goal:

    We want to extract the function names into a DataFrame.

"""

import os

from disco import Disco
from disco.stream import Transform

# 1. initalize a disco instance
disco = Disco()

# 2. mount a volume which contains the stories
disco.mount("pond", os.environ["POND"])

# 3. create a grammar for semantic processing of code streams
disco.create_grammar("python")

# 3. read our scripts as a text stream
stream = disco.stream("pond://code/python/*.py")


# 4. create a stream transform backed by a grammar
class ListFunctionsTransform(Transform):
    def __init__(self):
        self._grammar = disco.get_grammar("python")

    def type(self) -> dict[str, type]:
        return {"functions": list[str]}

    def apply(self, stream: bytes, metadata: dict[str, any] | None) -> dict:
        return {"functions": self._grammar.list_functions(stream)}


# 5. apply transform to the stream to produce a dataframe
df = stream.transform(ListFunctionsTransform())

df.explode("functions").show()
