"""Using daft (disco) to label pizza reviews and write to parquet."""

import os

from daft import col
from transformers import Pipeline, pipeline

from disco import Disco
from disco.object import Model


class HuggingFace(Model):
    _pipeline: Pipeline

    def __init__(self):
        raise ValueError("Cannot instantiate directly.")

    @staticmethod
    def zero_shot_classification(model: str):
        m = HuggingFace.__new__(HuggingFace)
        m._pipeline = pipeline("zero-shot-classification", model=model)
        return m

    def classify(self, text: str, labels: list[str]) -> str:
        return self._pipeline(text, labels)["labels"][0]


# initalize a disco instance
disco = Disco()

# mount a volume
disco.mount("comments", os.environ["POND"] + "/comments")

# register our model
disco.use_model("bart", HuggingFace.zero_shot_classification("facebook/bart-large-mnli"))

# read the csv as a daft dataframe
df = disco.read("comments://pizza_reviews.csv")

# label each row by building a udf from the model
classify = disco.get_model("bart").make_classifier(["happy", "neutral", "sad"])

# classify each thing
df.with_column("sentiment", classify(col("message"))).show()
