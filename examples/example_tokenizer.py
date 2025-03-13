"""TOKENIZE TEXT INPUTS DEMO.

Setup:

    We have a short story as raw text.

Goal:

    We want to tokenize this information.
"""

import os

import tiktoken

from disco import Disco
from disco.object import Tokenizer


# todo: add a way to register a tokenizer using a decorator
# @disco.register("my_tokenizer")
class o200k_base(Tokenizer):
    def __init__(self):
        self._encoding = tiktoken.get_encoding("o200k_base")

    def encode(self, input: bytes) -> any:
        return self._encoding.encode(str(input))

    def decode(self, input: any) -> bytes:
        return self._encoding.decode(input)


# initalize a disco instance
disco = Disco()

# mount a volume
disco.mount("pond", os.environ["POND"])

# register a tokenizer
disco.put_object("o200k_base", o200k_base())

# apply the tokenizer
disco.stream("pond://alice.text").encode("o200k_base").show()
