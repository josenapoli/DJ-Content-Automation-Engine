import base64
from pathlib import Path
from typing import Any, List, Optional

from tools.common.messenger import Messenger
from tools.common.openai_base import OpenAIBase
from tools.image_generation.midjourney import ImageTask


class OpenAIImageGenerator(OpenAIBase):
    image_model: str = "dall-e-3"
    aspect_ratio: str  # "9:16" or "16:9"

    def __init__(self, aspect_ratio: str, **kwargs: Any) -> None:
        super().__init__(aspect_ratio=aspect_ratio, **kwargs)

    def generate_image(self, prompt: str, output_path: Path) -> None:
        """Generates an image with DALL-E 3 and saves it to disk."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Map aspect ratio to DALL-E 3 sizes
        size = "1024x1024"
        if self.aspect_ratio == "9:16":
            size = "1024x1792"
        elif self.aspect_ratio == "16:9":
            size = "1792x1024"

        response = self._execute_with_retry(
            self.client.images.generate,
            model=self.image_model,
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
            response_format="b64_json",
        )

        image_data = response.data[0].b64_json
        if not image_data:
            raise RuntimeError("❌ DALL-E 3 no devolvió datos de imagen")

        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_data))

        Messenger.image(f"Imagen generada con DALL-E 3: {output_path}")

    def generate_images(self, tasks: List[ImageTask]) -> None:
        """
        Generates images in batch for a list of ImageTask objects.
        Processes sequentially.
        """
        total = len(tasks)
        Messenger.info(f"Batch Processing: {total} images via OpenAI (DALL-E 3)")

        for i, task in enumerate(tasks, start=1):
            Messenger.info(f"Generating image {i}/{total}: {task.output_path.name}")
            self.generate_image(
                prompt=task.prompt,
                output_path=task.output_path
            )

        Messenger.step_success(f"Batch complete: {total} images generated.")
