"""Using daft (disco) to label pizza reviews and write to parquet."""

from transformers import Pipeline, pipeline

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
        return self._pipeline(text, labels)
