import os

import tiktoken

from disco import Disco
from disco.object import Tokenizer


# todo: add a way to register a tokenizer using a decorator
# @disco.register("my_tokenizer")
class o200k_base(Tokenizer):
    def __init__(self):
        self._encoding = tiktoken.get_encoding("o200k_base")

    def encode(self, data: str) -> list:
        return self._encoding.encode(data)

    def decode(self, data: list) -> str:
        return self._encoding.decode(data)


# initalize a disco instance
disco = Disco()

# mount a volume
disco.mount("pond", os.environ["POND"])

# register a tokenizer
disco.put_object("o200k_base", o200k_base())

# apply the tokenizer
disco.stream("pond://alice.text").encode("o200k_base").show()
