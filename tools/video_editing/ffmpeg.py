import shlex
import subprocess
import tempfile
from pathlib import Path
from typing import List

from tools.common.base_model import BaseModelTool
from tools.common.messenger import Messenger


class FFmpegTool(BaseModelTool):
    """
    Tool for basic video editing operations using FFmpeg.
    """

    def _run(self, cmd_args: List[str]) -> None:
        p = subprocess.run(cmd_args)
        if p.returncode != 0:
            raise RuntimeError(f"FFmpeg falló: {' '.join(cmd_args)}")

    def split_audio(
        self,
        audio_in: Path,
        audio_out: Path,
        start_time: float,
        duration: float
    ) -> None:
        """
        Splits an audio file into a segment starting at start_time with duration.
        """
        cmd_args = [
            "ffmpeg", "-y", "-i", str(audio_in),
            "-ss", str(start_time), "-t", str(duration),
            str(audio_out), "-v", "error"
        ]
        self._run(cmd_args)

    def make_transition_video(
        self,
        img_a: Path,
        img_b: Path,
        out_path: Path,
        seconds: int = 4
    ) -> None:
        offset = max(0, seconds - 1)
        xfade_filter = f"[0:v][1:v]xfade=transition=fade:duration=1:offset={offset},format=yuv420p"
        cmd_args = [
            "ffmpeg", "-y",
            "-loop", "1", "-t", str(seconds), "-i", str(img_a),
            "-loop", "1", "-t", str(seconds), "-i", str(img_b),
            "-filter_complex", xfade_filter,
            "-t", str(seconds), str(out_path)
        ]
        self._run(cmd_args)

    def concat_videos(
        self,
        video_list: List[Path],
        out_path: Path,
    ) -> None:
        with tempfile.TemporaryDirectory() as td_str:
            td = Path(td_str)
            list_path = td / "files.txt"
            with open(list_path, "w", encoding="utf-8") as f:
                for v in video_list:
                    abs_v = v.absolute()
                    f.write(f"file '{abs_v}'\n")

            cmd_args = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", str(list_path), "-c", "copy", str(out_path)
            ]
            self._run(cmd_args)

    def get_audio_duration(self, audio_path: Path) -> float:
        """
        Retrieves the duration of an audio file using ffprobe.
        """
        cmd_args = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ]
        output = subprocess.check_output(cmd_args).decode("utf-8").strip()
        return float(output)

    def get_video_duration(self, video_path: Path) -> float:
        """
        Retrieves the duration of a video file using ffprobe.
        """
        cmd_args = [
            "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
        ]
        output = subprocess.check_output(cmd_args).decode("utf-8").strip()
        return float(output)

    def sync_video_and_audio(
        self,
        video_in: Path,
        audio_in: Path,
        video_out: Path
    ) -> None:
        """
        Synchronizes a video file to an audio file's duration.
        """
        audio_dur = self.get_audio_duration(audio_in)
        video_dur = self.get_video_duration(video_in)

        if video_dur <= 0:
            raise RuntimeError(f"Invalid video duration: {video_dur} for {video_in}")

        scale = audio_dur / video_dur
        cmd_args = [
            "ffmpeg", "-y", "-i", str(video_in),
            "-i", str(audio_in),
            "-filter_complex", f"[0:v]setpts={scale:.6f}*PTS[v]",
            "-map", "[v]", "-map", "1:a",
            "-c:v", "libx264", "-c:a", "aac", "-pix_fmt", "yuv420p",
            str(video_out), "-v", "error"
        ]
        self._run(cmd_args)

    def get_video_height(self, video_path: Path) -> int:
        """
        Retrieves the height of a video file using ffprobe.
        """
        cmd_args = [
            "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=height",
            "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
        ]
        output = subprocess.check_output(cmd_args).decode("utf-8").strip()
        return int(output)

    def get_video_width(self, video_path: Path) -> int:
        """
        Retrieves the width of a video file using ffprobe.
        """
        cmd_args = [
            "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width",
            "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
        ]
        output = subprocess.check_output(cmd_args).decode("utf-8").strip()
        return int(output)

    def create_composite_scene_video(
        self,
        img_path: Path,
        audio_path: Path,
        out_path: Path
    ) -> None:
        """
        Creates a video with a 3-part dynamic sequence.
        """
        duration = self.get_audio_duration(audio_path)
        fps = 25
        total_frames = int(duration * fps)
        f1 = total_frames * 0.3
        f2 = total_frames * 0.7

        width = self.get_video_width(img_path)
        height = self.get_video_height(img_path)

        z_expr = (
            f"if(lt(on,{f1}), 1.0+0.2*(on/{f1}), "
            f"if(lt(on,{f2}), 1.2, "
            f"1.2-0.2*((on-{f2})/({total_frames}-{f2}))))"
        )
        pos_filter = "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        zoom_filter = f"zoompan=z='{z_expr}':d=1:{pos_filter}:s={width}x{height},format=yuv420p"
        rotate_filter = "rotate='1*PI/180*sin(2*PI*t/3)'"

        cmd_args = [
            "ffmpeg", "-y", "-loop", "1", "-i", str(img_path),
            "-i", str(audio_path),
            "-vf", f"{zoom_filter},{rotate_filter}",
            "-shortest",
            "-c:v", "libx264", "-c:a", "aac", "-pix_fmt", "yuv420p",
            str(out_path)
        ]
        self._run(cmd_args)

    def extract_audio(self, video_in: Path, audio_out: Path) -> None:
        """
        Extracts audio from a video file, optimized for Whisper STT.
        """
        cmd_args = [
            "ffmpeg", "-y", "-i", str(video_in),
            "-vn", "-ac", "1", "-ar", "16000",
            str(audio_out)
        ]
        self._run(cmd_args)

    def add_subtitles_to_video(
        self,
        video_in: Path,
        srt_path: Path,
        video_out: Path,
        font_size: int = 64
    ) -> None:
        """
        Adds subtitles to a video.
        """
        width = self.get_video_width(video_in)
        height = self.get_video_height(video_in)
        margin_v = int(height * 0.15)

        Messenger.info(f"Subtitling: {width}x{height}, MarginV={margin_v}px")

        # For subtitles filter on Windows, we need to escape the path carefully
        # Even when using list arguments, the filter string itself is parsed by ffmpeg
        safe_srt = str(srt_path).replace("\\", "/").replace(":", "\\:")
        
        style = (
            f"PlayResX={width},PlayResY={height},"
            f"FontName=Impact,FontSize={font_size},PrimaryColour=&H00FFFF,"
            f"OutlineColour=&H000000,BorderStyle=1,Outline=2,"
            f"Alignment=2,MarginV={margin_v}"
        )
        sub_filter = f"subtitles={safe_srt}:force_style='{style}'"

        cmd_args = [
            "ffmpeg", "-y", "-i", str(video_in),
            "-vf", sub_filter,
            "-c:a", "copy", str(video_out)
        ]
        self._run(cmd_args)

    def add_background_music(
        self,
        video_in: Path,
        audio_bg: Path,
        video_out: Path,
        bg_volume: float = 0.15
    ) -> None:
        """
        Mixes a background audio track into a video.
        """
        filter_complex = (
            f"[0:a]volume=1.0[v_a]; "
            f"[1:a]volume={bg_volume}[bg_a]; "
            "[v_a][bg_a]amix=inputs=2:duration=first[fixed_a]"
        )

        cmd_args = [
            "ffmpeg", "-y", "-i", str(video_in),
            "-stream_loop", "-1", "-i", str(audio_bg),
            "-filter_complex", filter_complex,
            "-map", "0:v", "-map", "[fixed_a]",
            "-c:v", "copy", "-c:a", "aac", str(video_out)
        ]
        self._run(cmd_args)
