"""TEXT STREAM DEMO.

A "stream" is produced from unstructured data (with related metadata) which we can transform into a somethign structured.

Setup:

    We have compressed text files containing short stories.

Goal:

    We want to produce a list of unique characters (by name).

"""

import os

from disco import Disco
from disco.stream import Transform

# 1. initalize a disco instance
disco = Disco()

# 2. mount a volume which contains the stories
disco.mount("pond", os.environ["POND"])

# 3. read our stories as a text stream.
stream = disco.stream("pond://stories/*.txt")


# 4. write our transform on the unstructured data
class ExtractCharacters(Transform):
    def type(self) -> dict[str, type]:
        return {"characters": list[str]}

    def apply(self, stream: bytes, metadata: dict[str, any] | None) -> dict:
        return {"characters": ["alice", "nemo"]}


# 5. apply to the stream
stream.transform(ExtractCharacters()).show()
