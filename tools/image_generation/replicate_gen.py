import os
import urllib.request
from pathlib import Path
from typing import Any, List

import replicate
import time

from tools.common.messenger import Messenger
from tools.image_generation.midjourney import ImageTask


class ReplicateImageGenerator:
    """
    Image generation using Replicate API
    Uses the black-forest-labs/flux-1.1-pro model
    """
    aspect_ratio: str  # "9:16" or "16:9"

    def __init__(self, aspect_ratio: str, **kwargs: Any) -> None:
        self.aspect_ratio = aspect_ratio
        if not os.environ.get("REPLICATE_API_TOKEN"):
            raise ValueError("REPLICATE_API_TOKEN not set in environment variables")

    def generate_image(self, prompt: str, output_path: Path) -> None:
        """Generates an image with Replicate and saves it to disk."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            Messenger.info(f"Solicitando imagen a Replicate (Flux 1.1 Pro): {output_path.name}")
            
            # Map aspect ratio to string format expected by Replicate Flux
            # Flux 1.1 Pro expects aspect ratios like "16:9", "9:16", "1:1", etc.
            ar = self.aspect_ratio if self.aspect_ratio in ["16:9", "9:16", "1:1", "4:3", "3:4", "21:9", "9:21"] else "9:16"

            max_api_retries = 5
            for api_attempt in range(max_api_retries):
                try:
                    output = replicate.run(
                        "black-forest-labs/flux-1.1-pro",
                        input={
                            "prompt": prompt,
                            "aspect_ratio": ar,
                            "output_format": "png",
                            "output_quality": 100,
                            "seed": 424242
                        }
                    )
                    break
                except replicate.exceptions.ReplicateError as e:
                    error_msg = str(e)
                    if "rate limit" in error_msg.lower() or "throttled" in error_msg.lower():
                        if api_attempt < max_api_retries - 1:
                            wait_time = 10 * (api_attempt + 1)
                            Messenger.warning(f"Replicate Rate Limit alcanzado. Esperando {wait_time}s... (Intento {api_attempt+1}/{max_api_retries})")
                            time.sleep(wait_time)
                            continue
                        else:
                            raise e
                    else:
                        raise e
            
            # output is a FileOutput object which is a string URL
            image_url = str(output)
            
            # Download the image
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            
            # Retry logic for download
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    with urllib.request.urlopen(req, timeout=30) as response:
                        data = response.read()
                        with open(output_path, "wb") as f:
                            f.write(data)
                    Messenger.image(f"Imagen generada con Replicate: {output_path}")
                    return # Success
                except Exception as e:
                    if attempt < max_retries - 1:
                        Messenger.warning(f"Reintentando descarga de Replicate ({attempt + 1}/{max_retries})...")
                    else:
                        raise e

        except replicate.exceptions.ReplicateError as e:
            error_msg = str(e)
            if "out of free time" in error_msg.lower() or "payment method" in error_msg.lower():
                Messenger.error(f"❌ Límite de saldo de Replicate alcanzado. No se gastará más.")
            else:
                Messenger.error(f"❌ Error en Replicate API: {error_msg}")
            raise e
        except Exception as e:
            Messenger.error(f"❌ Error general en Replicate: {str(e)}")
            raise e

    def generate_images(self, tasks: List[ImageTask]) -> None:
        """
        Generates images in batch for a list of ImageTask objects.
        """
        total = len(tasks)
        Messenger.info(f"Batch Processing: {total} images via Replicate (Flux-1.1-Pro)")

        for i, task in enumerate(tasks, start=1):
            Messenger.info(f"Generating image {i}/{total}: {task.output_path.name}")
            self.generate_image(
                prompt=task.prompt,
                output_path=task.output_path
            )

        Messenger.step_success(f"Batch complete: {total} images generated.")
