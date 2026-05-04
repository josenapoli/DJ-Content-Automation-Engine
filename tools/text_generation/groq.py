import os
from typing import Any, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

from openai import OpenAI
from pydantic import PrivateAttr

from tools.text_generation.openai import OpenAITextGenerator


class GroqTextGenerator(OpenAITextGenerator):
    text_model: str = "llama-3.3-70b-versatile"

    def __init__(self, **kwargs: Any):
        api_key = os.getenv("GROQ_API_KEY")
        super().__init__(
            provider_name="Groq",
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            **kwargs
        )

    def generate_text(self, prompt: str, schema: Type[T]) -> T:
        """
        Generates content with Groq using json_object format and parses it.
        """
        completion = self._execute_with_retry(
            self.client.chat.completions.create,
            model=self.text_model,
            messages=[
                {"role": "system", "content": f"You are a specialized content generator. Always respond in valid JSON matching this schema: {schema.model_json_schema()}"},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )

        content = completion.choices[0].message.content
        if not content:
            raise RuntimeError("❌ Groq no devolvió contenido")

        return schema.model_validate_json(content)
