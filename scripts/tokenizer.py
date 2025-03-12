# %%
import daft
import disco
from disco import Disco
import tiktoken
from daft import col

# todo: add a way to register a tokenizer using a decorator
# @disco.register("my_tokenizer")
class MyTokenizer(disco.Tokenizer):
    def __init__(self, id: str):
        self.id = id
        self.encoder = tiktoken.get_encoding("o200k_base")

    def encode(self, data: str) -> list:
        return self.encoder.encode(data)

    def decode(self, data: list) -> str:
        return self.encoder.decode(data)


# example usage
# cat = Disco()
# cat.put_object("my_tokenizer", MyTokenizer)

# cat.put_volume("data", "./data")
# df = disco.read("data://sample.text").transform("my_tokenizer")

