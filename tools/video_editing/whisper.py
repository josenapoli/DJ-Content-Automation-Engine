import json
import re
import shlex
import subprocess
from pathlib import Path
from typing import ClassVar, List

from tools.common.base_model import BaseModelTool
from tools.video_editing.whisper_schemas import (
    WhisperTranscription,
    WhisperTranscriptionSegment,
    WhisperWord,
)


class WhisperTool(BaseModelTool):
    """
    Tool for transcribing audio using whisper-cpp and generating SRT files.
    """
    DEFAULT_MODEL: ClassVar[str] = "models/whisper/ggml-small.bin"

    def _run(self, cmd_args: List[str]) -> None:
        p = subprocess.run(cmd_args)
        if p.returncode != 0:
            raise RuntimeError(f"Whisper Error: {' '.join(cmd_args)}")

    def _get_transcription_json(
        self,
        audio_path: Path,
    ) -> WhisperTranscription:
        """
        Runs whisper-cli (if needed) and returns the parsed JSON content.
        """
        json_path = audio_path.with_name(audio_path.name + ".json")
        # -ojf: output json full (tokens with timestamps)
        whisper_executable = "whisper-cli"
        local_whisper = Path("whisper-bin/whisper-cli.exe").absolute()
        if local_whisper.exists():
            whisper_executable = str(local_whisper)

        if not json_path.exists():
                
            # Whisper-cpp requires 16kHz WAV.
            # We resample using ffmpeg first.
            resampled_path = audio_path.with_name(audio_path.name + ".16k.wav")
            resample_cmd = [
                "ffmpeg", "-y", "-i", str(audio_path),
                "-ar", "16000", "-ac", "1", str(resampled_path), "-v", "error"
            ]
            subprocess.run(resample_cmd)

            cmd_args = [
                whisper_executable,
                "-m", self.DEFAULT_MODEL,
                "-l", "es",
                "-ojf",
                "-f", str(resampled_path)
            ]
            self._run(cmd_args)
            
            # The JSON is saved as resampled_path + ".json"
            generated_json = resampled_path.with_name(resampled_path.name + ".json")
            if generated_json.exists():
                generated_json.replace(json_path)

            # Clean up resampled file
            resampled_path.unlink(missing_ok=True)

        def load_json():
            try:
                with open(json_path, 'rb') as f:
                    content = f.read().decode('utf-8', errors='ignore')
                return WhisperTranscription.model_validate(json.loads(content))
            except (json.JSONDecodeError, UnicodeDecodeError):
                return None

        data = load_json()
        if data is None:
            # If JSON is corrupted or has encoding issues, delete and regenerate
            Messenger.warning(f"Corrupted JSON detected: {json_path}. Regenerating...")
            json_path.unlink(missing_ok=True)
            
            # Re-run transcription logic
            resampled_path = audio_path.with_name(audio_path.name + ".16k.wav")
            resample_cmd = [
                "ffmpeg", "-y", "-i", str(audio_path),
                "-ar", "16000", "-ac", "1", str(resampled_path), "-v", "error"
            ]
            subprocess.run(resample_cmd)

            cmd_args = [
                whisper_executable,
                "-m", self.DEFAULT_MODEL,
                "-l", "es",
                "-ojf",
                "-f", str(resampled_path)
            ]
            self._run(cmd_args)
            
            generated_json = resampled_path.with_name(resampled_path.name + ".json")
            if generated_json.exists():
                generated_json.replace(json_path)
            resampled_path.unlink(missing_ok=True)
            
            data = load_json()
            if data is None:
                raise RuntimeError(f"❌ Failed to generate valid JSON for: {audio_path}")

        return data

    def get_transcription_segments(
        self,
        audio_path: Path
    ) -> List[WhisperTranscriptionSegment]:
        """
        Transcribes audio and returns a list of segments with text and timestamps.
        Each segment: {"text": str, "start": float, "end": float} (times in seconds)
        """
        data = self._get_transcription_json(audio_path)
        segments: List[WhisperTranscriptionSegment] = []
        for s in data.transcription:
            text = s.text.strip()
            # Fix common transcription errors
            text = text.replace("DG", "DJ").replace("dg", "dj").replace("D.G.", "DJ")
            text = text.replace("transe", "trance").replace("Transe", "Trance")
            text = text.replace("polectivo", "colectivo").replace("Polectivo", "Colectivo")
            text = text.replace("lusto", "listo").replace("Lusto", "Listo")
            
            # Specific fix for the 'Únete' issue (handles potential corruption characters and missing spaces)
            text = re.sub(r'([.?!])nete\b', r'\1 Únete', text)
            text = re.sub(r'(^|\s)nete\b', r'\1Únete', text)
            
            segments.append(WhisperTranscriptionSegment(
                text=text,
                start=s.offsets.from_ms / 1000.0,
                end=s.offsets.to_ms / 1000.0
            ))

        return segments

    def generate_srt(
        self,
        audio_path: Path,
        output_srt: Path,
    ) -> None:
        """
        Generates SRT file from audio file.
        """
        data = self._get_transcription_json(audio_path)

        # 1. Extract and merge tokens into words
        tokens = [
            t
            for s in data.transcription
            for t in s.tokens
            if not t.text.startswith("[_") and t.text.strip()
        ]

        words: List[WhisperWord] = []
        for t in tokens:
            text, t_from, t_to = t.text, t.offsets.from_ms, t.offsets.to_ms
            if text.startswith(" ") or not words:
                word_text = text.strip()
                # Fix common transcription errors
                word_text = word_text.replace("DG", "DJ").replace("dg", "dj").replace("D.G.", "DJ")
                word_text = word_text.replace("transe", "trance").replace("Transe", "Trance")
                word_text = word_text.replace("polectivo", "colectivo").replace("Polectivo", "Colectivo")
                word_text = word_text.replace("lusto", "listo").replace("Lusto", "Listo")
                
                words.append(WhisperWord(text=word_text, start=t_from, end=t_to))
            else:
                words[-1].text += text
                # Re-fix the merged word if it now contains errors
                words[-1].text = words[-1].text.replace("DG", "DJ").replace("dg", "dj").replace("D.G.", "DJ")
                words[-1].text = words[-1].text.replace("transe", "trance").replace("Transe", "Trance")
                words[-1].text = words[-1].text.replace("polectivo", "colectivo").replace("Polectivo", "Colectivo")
                words[-1].text = words[-1].text.replace("lusto", "listo").replace("Lusto", "Listo")
                
                # Fix 'Únete' in merged words
                words[-1].text = re.sub(r'(\.|\s|^)nete', r'\1Únete', words[-1].text)
                
                words[-1].end = t_to

        # 2. Group words into blocks (max 3 words or pause > 0.4s)
        blocks: List[List[WhisperWord]] = []
        current: List[WhisperWord] = []
        for w in words:
            pause = (float(w.start) - float(current[-1].end)) / 1000.0 if current else 0.0
            if len(current) >= 3 or pause > 0.4:
                blocks.append(current)
                current = []
            current.append(w)
        if current:
            blocks.append(current)

        def fmt(ms: int) -> str:
            s, ms = divmod(ms, 1000)
            m, s = divmod(s, 60)
            h, m = divmod(m, 60)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        # 3. Write SRT
        with open(output_srt, 'w', encoding='utf-8') as f:
            for i, block in enumerate(blocks):
                start_time = block[0].start
                end_time = block[-1].end
                
                # If it's the last block, extend it slightly to ensure the last word is visible
                if i == len(blocks) - 1:
                    end_time += 1000 # Add 1 second
                
                f.write(f"{i+1}\n{fmt(start_time)} --> {fmt(end_time)}\n")
                f.write(" ".join(w.text for w in block) + "\n\n")
