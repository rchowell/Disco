"""TEXT STREAM DEMO.

A "stream" is produced from unstructured data (with related metadata) which we can transform into a somethign structured.

Setup:

    We have compressed text files containing short stories.

Goal:

    We want to produce a list of unique characters (by name).

"""

import os

from disco import Disco
from disco.model.__openai import OpenAIModel
from disco.stream import Transform

# 1. initalize a disco instance
disco = Disco()

# 2. mount a volume which contains the stories
disco.mount("pond", os.environ["POND"])

# 3. read our stories as a text stream.
stream = disco.stream("pond://stories/*.txt")


# 4. write our transform on the unstructured data
class ExtractCharacters(Transform):
    def __init__(self):
        self._model = OpenAIModel.inferencer(
            model="gpt-4o-mini",
            prompt="Please return the names of the characters mentioned in this short story as a comma-separated list with NO additional output",
        )

    def type(self) -> dict[str, type]:
        return {"characters": list[str]}

    def apply(self, stream: bytes, metadata: dict[str, any] | None) -> dict:
        story = stream.decode()
        characters_csv = self._model.infer(story)
        characters = [name.strip() for name in characters_csv.split(",")]
        return {"characters": characters}


# 5. apply transform to the stream to produce a dataframe
df = stream.transform(ExtractCharacters())

# 6. select distinct characters
df.explode("characters").distinct().show()
