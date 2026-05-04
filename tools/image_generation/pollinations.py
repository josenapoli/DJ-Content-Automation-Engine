import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, List
import time

from tools.common.messenger import Messenger
from tools.image_generation.midjourney import ImageTask


class PollinationsImageGenerator:
    """
    Free image generation using Pollinations.ai
    No API Key required.
    """
    base_url: str = "https://image.pollinations.ai/prompt/"
    aspect_ratio: str  # "9:16" or "16:9"

    def __init__(self, aspect_ratio: str, **kwargs: Any) -> None:
        self.aspect_ratio = aspect_ratio

    def generate_image(self, prompt: str, output_path: Path) -> None:
        """Generates an image with Pollinations.ai and saves it to disk."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Map aspect ratio to pixels
        width, height = 1024, 1024
        if self.aspect_ratio == "9:16":
            width, height = 1080, 1920
        elif self.aspect_ratio == "16:9":
            width, height = 1920, 1080

        # Encode prompt
        encoded_prompt = urllib.parse.quote(prompt)
        
        # Build URL
        # We use model=flux for better quality if available, or default
        url = f"{self.base_url}{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true&seed=42"

        try:
            Messenger.info(f"Solicitando imagen a Pollinations: {output_path.name}")
            
            # Set a user-agent to avoid being blocked
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            # Retry logic
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    with urllib.request.urlopen(req, timeout=30) as response:
                        data = response.read()
                        with open(output_path, "wb") as f:
                            f.write(data)
                    Messenger.image(f"Imagen generada con Pollinations: {output_path}")
                    return # Success
                except urllib.error.HTTPError as e:
                    if e.code == 429 and attempt < max_retries - 1:
                        wait_time = 10 * (attempt + 1)
                        Messenger.warning(f"Pollinations Rate Limit (429). Esperando {wait_time}s... (Intento {attempt+1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    elif attempt < max_retries - 1:
                        Messenger.warning(f"Reintentando Pollinations ({attempt + 1}/{max_retries})...")
                        time.sleep(2)
                    else:
                        raise e
                except Exception as e:
                    if attempt < max_retries - 1:
                        Messenger.warning(f"Reintentando Pollinations ({attempt + 1}/{max_retries})...")
                        time.sleep(2)
                    else:
                        raise e

        except Exception as e:
            Messenger.error(f"❌ Error en Pollinations: {str(e)}")
            raise e

    def generate_images(self, tasks: List[ImageTask]) -> None:
        """
        Generates images in batch for a list of ImageTask objects.
        """
        total = len(tasks)
        Messenger.info(f"Batch Processing: {total} images via Pollinations.ai")

        for i, task in enumerate(tasks, start=1):
            Messenger.info(f"Generating image {i}/{total}: {task.output_path.name}")
            self.generate_image(
                prompt=task.prompt,
                output_path=task.output_path
            )

        Messenger.step_success(f"Batch complete: {total} images generated.")
