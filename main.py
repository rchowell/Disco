# %%
import daft
from daft import col
import tiktoken

# hack, we don't actually have a way to read in a text file,
# so i'm using the csv reader and using a delimiter that is unlikely to be used so it reads each line as a column
df = daft.read_csv('./data/sample.text', delimiter='¦', has_headers=False).select(col("column_1").alias("text"))
# tokenize_encode isnt showing up in docstrings
# df = df.select(col("text").str.tokenize_encode("cl100k_base")).collect()
# shouldn't tokenize_encode return a fixedsizelist instead of a list?


@daft.udf(return_dtype=daft.DataType.list(daft.DataType.int32()))
def tokenize(text: daft.Series, encoder:str):
    enc = tiktoken.get_encoding(encoder)
    items = [enc.encode(t) for t in text.to_pylist()]
    return items


df.select(tokenize(col("text"), encoder="o200k_base")).show()
