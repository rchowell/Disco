# %%
import daft
from daft import col

# hack, we don't actually have a way to read in a text file,
# so i'm using the csv reader and using a delimiter that is unlikely to be used so it reads each line as a column
df = daft.read_csv('./data/sample.text', delimiter='¦', has_headers=False).select(col("column_1").alias("text"))
# tokenize_encode isnt showing up in docstrings
df = df.select(col("text").str.tokenize_encode("cl100k_base")).collect()
# shouldn't tokenize_encode return a fixedsizelist instead of a list?
df.show()



