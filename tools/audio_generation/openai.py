from pathlib import Path
from typing import Any

from tools.common.messenger import Messenger
from tools.common.openai_base import OpenAIBase


class OpenAIAudioGenerator(OpenAIBase):
    tts_model: str = "tts-1"
    voice_name: str = "onyx"  # Options: alloy, echo, fable, onyx, nova, shimmer

    def __init__(self, voice_name: str = "onyx", **kwargs: Any):
        super().__init__(voice_name=voice_name, **kwargs)

    def text_to_speech(
        self,
        text: str,
        audio_path: Path,
    ) -> None:
        """
        Generates audio using OpenAI TTS and saves it to disk.
        """
        audio_path.parent.mkdir(parents=True, exist_ok=True)

        response = self._execute_with_retry(
            self.client.audio.speech.create,
            model=self.tts_model,
            voice=self.voice_name,
            input=text,
            response_format="wav",
        )

        # Response.content contains the raw audio bytes
        response.stream_to_file(audio_path)
        
        Messenger.audio(f"Audio generado con OpenAI: {audio_path}")
