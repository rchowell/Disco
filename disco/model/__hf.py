from transformers import Pipeline, pipeline

from disco.model import Model


class HuggingFaceModel(Model):
    _pipeline: Pipeline

    def __init__(self):
        raise ValueError("Cannot instantiate directly.")

    @staticmethod
    def zero_shot_classification(model: str):
        m = HuggingFaceModel.__new__(HuggingFaceModel)
        m._pipeline = pipeline("zero-shot-classification", model=model)
        return m

    @staticmethod
    def zero_shot_image_classification(model: str):
        m = HuggingFaceModel.__new__(HuggingFaceModel)
        m._pipeline = pipeline("zero-shot-image-classification", model=model)
        return m

    def classify(self, text: str, labels: list[str]) -> str:
        return self._pipeline(text, labels)["labels"][0]
