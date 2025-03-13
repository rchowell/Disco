from openai import OpenAI
from openai.types.shared import ChatModel

from disco.model import Model


class OpenAIModel(Model):
    def __init__(self):
        raise ValueError("Cannot instantiate directly.")

    @staticmethod
    def inferencer(model: ChatModel, prompt: str, role: str | None = None):
        m = OpenAIModel.__new__(OpenAIModel)
        m._client = OpenAI()
        m._model = model
        m._role = role
        m._prompt = prompt
        return m

    def infer(self, text: str) -> str:
        res = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": self._role or "You are a helpful assistant."},
                {"role": "user", "content": f"{self._prompt}: {text}"},
            ],
            temperature=0.0,
        )
        return res.choices[0].message.content.strip()
