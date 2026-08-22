import os
from pathlib import Path
import numpy as np
from PIL import Image
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

class VideoEditor:
    def __init__(self, fps: int = 24, resolution: tuple = (1920, 1080)):
        self.fps = fps
        self.width, self.height = resolution

    def apply_ken_burns(self, clip: ImageClip, duration: float, zoom_in: bool = True) -> ImageClip:
        def zoom_func(get_frame, t):
            frame = get_frame(t)
            h, w, _ = frame.shape
            prog = t / duration if duration > 0 else 0
            scale = 1.0 + 0.07 * prog if zoom_in else 1.07 - 0.07 * prog

            new_w, new_h = int(w * scale), int(h * scale)
            img = Image.fromarray(frame).resize((new_w, new_h), Image.Resampling.BILINEAR)
            arr = np.array(img)
            x1, y1 = (new_w - w) // 2, (new_h - h) // 2
            return arr[y1:y1 + h, x1:x1 + w]

        return clip.fl(zoom_func)

    def assemble_video(self, scenes_data: list, image_paths: list, audio_paths: list, output_video_path: Path) -> str:
        clips = []
        for i in range(len(scenes_data)):
            img_file = image_paths[i]
            aud_file = audio_paths[i]
            if not os.path.exists(img_file) or not os.path.exists(aud_file):
                continue

            audio_clip = AudioFileClip(str(aud_file))
            dur = max(audio_clip.duration, 1.5)

            img_clip = ImageClip(str(img_file)).set_duration(dur).set_fps(self.fps)
            img_clip = img_clip.resize(newsize=(self.width, self.height))

            animated = self.apply_ken_burns(img_clip, duration=dur, zoom_in=(i % 2 == 0))
            animated = animated.set_audio(audio_clip)

            if i > 0:
                animated = animated.crossfadein(0.3)
            clips.append(animated)

        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile(
            str(output_video_path),
            fps=self.fps,
            codec="libx264",
            audio_codec="aac",
            threads=4,
            preset="medium",
            logger=None
        )
        return str(output_video_path)