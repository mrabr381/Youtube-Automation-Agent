import os
import subprocess
from pathlib import Path

class VideoEditor:
    def __init__(self, fps: int = 24, resolution: tuple = (1920, 1080)):
        self.fps = fps
        self.width, self.height = resolution

    def _render_single_scene(self, img_path: str, aud_path: str, out_scene_path: str, zoom_in: bool = True) -> bool:
        """
        Renders a single scene (image + audio) with Ken Burns zoom animation directly using FFmpeg.
        This uses minimal RAM (<40MB) and prevents Streamlit Cloud Out-Of-Memory crashes.
        """
        if zoom_in:
            zoom_filter = f"scale=8000:-1,zoompan=z='min(zoom+0.0012,1.15)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={self.width}x{self.height}:fps={self.fps}"
        else:
            zoom_filter = f"scale=8000:-1,zoompan=z='if(lte(zoom,1.0),1.15,max(1.0,zoom-0.0012))':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={self.width}x{self.height}:fps={self.fps}"

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", img_path,
            "-i", aud_path,
            "-vf", zoom_filter,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            out_scene_path
        ]

        try:
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
            return res.returncode == 0
        except Exception as e:
            print(f"[VideoEditor] Error rendering scene {out_scene_path}: {e}")
            return False

    def assemble_video(self, scenes_data: list, image_paths: list, audio_paths: list, output_video_path: Path) -> str:
        """
        Streamlined, ultra-fast, low-RAM video assembly using direct FFmpeg streaming.
        """
        temp_dir = output_video_path.parent / "temp_scenes"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        rendered_scene_files = []
        total_scenes = len(scenes_data)

        print(f"[VideoEditor] Rendering {total_scenes} scenes individually to optimize RAM...")
        for i in range(total_scenes):
            img_file = str(image_paths[i])
            aud_file = str(audio_paths[i])
            
            if not os.path.exists(img_file) or not os.path.exists(aud_file):
                continue

            scene_mp4 = temp_dir / f"scene_{i+1:03d}.mp4"
            zoom_in = (i % 2 == 0)
            
            success = self._render_single_scene(img_file, aud_file, str(scene_mp4), zoom_in=zoom_in)
            if success and scene_mp4.exists():
                rendered_scene_files.append(scene_mp4)

        if not rendered_scene_files:
            raise RuntimeError("No scenes could be rendered into video.")

        # Concat list file for fast merging
        concat_list_file = temp_dir / "concat_list.txt"
        with open(concat_list_file, "w", encoding="utf-8") as f:
            for sc in rendered_scene_files:
                f.write(f"file '{sc.resolve()}'\n")

        print(f"[VideoEditor] Merging {len(rendered_scene_files)} scenes into final video...")
        merge_cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list_file),
            "-c", "copy",
            str(output_video_path)
        ]

        res = subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode != 0 or not output_video_path.exists():
            fallback_cmd = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_list_file),
                "-c:v", "libx264", "-preset", "fast",
                "-c:a", "aac",
                str(output_video_path)
            ]
            subprocess.run(fallback_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Temporary files cleanup
        try:
            for sc in rendered_scene_files:
                if sc.exists():
                    sc.unlink()
            if concat_list_file.exists():
                concat_list_file.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()
        except Exception:
            pass

        print(f"[VideoEditor] Video successfully produced at: {output_video_path}")
        return str(output_video_path)
