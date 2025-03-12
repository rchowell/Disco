# %%
import daft
from daft import col
import tiktoken

df = daft.read_csv('./data/sample.text', delimiter='¦', has_headers=False).select(col("column_1").alias("text"))

@daft.udf(return_dtype=daft.DataType.list(daft.DataType.int32()))
def tokenize(text: daft.Series, encoder:str):
    enc = tiktoken.get_encoding(encoder)
    items = [enc.encode(t) for t in text.to_pylist()]
    return items


df.select(tokenize(col("text"), encoder="o200k_base")).show()
