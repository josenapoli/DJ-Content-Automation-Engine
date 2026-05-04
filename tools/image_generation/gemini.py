import time
from pathlib import Path
from typing import Any, List, Optional, cast

from google.genai import types
from PIL import Image

from tools.common.gemini_base import GeminiBase
from tools.common.messenger import Messenger
from tools.image_generation.midjourney import ImageTask


class GeminiImageGenerator(GeminiBase):
    image_model: str = "gemini-3.1-flash-image-preview"
    aspect_ratio: str
    style_references: List[Path] = []

    def __init__(
        self,
        aspect_ratio: str,
        reference_dir: Optional[Path] = None,
        **kwargs: Any
    ) -> None:
        style_refs = []
        if reference_dir and reference_dir.exists():
            style_refs = sorted(reference_dir.glob("*.png"))

        super().__init__(
            aspect_ratio=aspect_ratio,
            style_references=style_refs,
            **kwargs
        )

    def generate_image(
        self,
        prompt: str,
        output_path: Path,
        style_references: List[Path] = [],
        sequence_reference: Optional[Path] = None
    ) -> None:
        """Generates an image with Gemini and saves it to disk."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        contents = self._prepare_contents(prompt, style_references, sequence_reference)
        config = types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE'],
            image_config=types.ImageConfig(aspect_ratio=self.aspect_ratio, image_size="1K")
        )

        max_retries = 5
        backoff_delay = 30 # Base delay for retries after failure

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.image_model,
                    contents=contents,
                    config=config
                )

                if not response or not response.parts:
                    raise RuntimeError("❌ Gemini Image no devolvió partes")

                self._extract_usage(response, self.image_model)
                image = self._extract_image(response)
                image.save(output_path)

                is_ref = style_references or sequence_reference
                msg = f"Imagen generada ({'img2img' if is_ref else 'txt2img'}): {output_path}"
                Messenger.image(msg)
                return  # Success!

            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    if attempt < max_retries - 1:
                        # Exponential backoff: 30s, 60s, 90s...
                        wait_time = backoff_delay * (attempt + 1)
                        Messenger.warning(
                            f"⚠️ Cuota agotada (429). "
                            f"Esperando {wait_time}s para reintentar... (Intento {attempt + 1}/{max_retries})"
                        )
                        time.sleep(wait_time)
                        continue
                    else:
                        Messenger.error("❌ Se agotaron los reintentos por límite de cuota (429).")
                        raise e
                raise e

    def generate_images(self, tasks: List[ImageTask]) -> None:
        """
        Generates images in batch for a list of ImageTask objects.
        Processes sequentially (Gemini API is synchronous).
        """
        total = len(tasks)
        Messenger.info(f"Batch Processing: {total} images via Gemini")

        for i, task in enumerate(tasks, start=1):
            if i > 1:
                # Wait 15s between images to avoid RPM limits
                Messenger.info(f"Esperando 15s antes de la siguiente imagen...")
                time.sleep(15)

            Messenger.info(f"Generating image {i}/{total}: {task.output_path.name}")
            self.generate_image(
                prompt=task.prompt,
                output_path=task.output_path,
                style_references=self.style_references,
            )

        Messenger.step_success(f"Batch complete: {total} images generated.")

    def _prepare_contents(
        self,
        prompt: str,
        style_references: List[Path],
        sequence_reference: Optional[Path]
    ) -> List[Any]:
        """Prepares the contents list for the Gemini API call."""
        contents: List[Any] = [f"Primary Prompt: {prompt}"]

        if style_references:
            contents.append("--- STYLE REFERENCES (Maintain this visual aesthetic) ---")
            for ref_path in style_references:
                if ref_path.exists():
                    contents.append(Image.open(ref_path))

        if sequence_reference and sequence_reference.exists():
            contents.append("--- SEQUENCE REFERENCE (Maintain consistency) ---")
            contents.append(Image.open(sequence_reference))

        return contents

    def _extract_image(self, response: Any) -> Image.Image:
        """Extracts the image from the Gemini response."""
        image: Optional[Image.Image] = None
        for part in response.parts:
            if part.text:
                Messenger.info(f"Gemini thoughts: {part.text}")
            elif part.inline_data:
                image = cast(Image.Image, part.as_image())
                break

        if image is None:
            raise RuntimeError("❌ No se encontró imagen en la respuesta de Gemini")
        return image
