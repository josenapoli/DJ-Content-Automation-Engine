from typing import Any, Type, TypeVar

from pydantic import BaseModel

from tools.common.openai_base import OpenAIBase

T = TypeVar("T", bound=BaseModel)


class OpenAITextGenerator(OpenAIBase):
    text_model: str = "gpt-4o"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def generate_text(self, prompt: str, schema: Type[T]) -> T:
        """
        Generates content with OpenAI and parses it into a Pydantic model.
        """
        completion = self._execute_with_retry(
            self.client.beta.chat.completions.parse,
            model=self.text_model,
            messages=[
                {"role": "system", "content": "You are a specialized content generator. Always respond in the requested JSON schema."},
                {"role": "user", "content": prompt},
            ],
            response_format=schema,
        )

        message = completion.choices[0].message
        if message.refusal:
            raise RuntimeError(f"❌ OpenAI rechazó generar el contenido: {message.refusal}")

        if not message.parsed:
            raise RuntimeError("❌ OpenAI no devolvió un objeto parseado correctamente")

        return message.parsed
