import os
import time
import shutil
import urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from PIL import Image, ImageDraw

class ImageGenerator:
    def __init__(self, default_style: str = "Cinematic, Photorealistic, 8k, Octane render, Dramatic lighting"):
        self.default_style = default_style
        self.base_url = "https://image.pollinations.ai/prompt/"

    def _clean_prompt(self, prompt: str) -> str:
        words = prompt.replace("\n", " ").strip().split()
        return " ".join(words[:25])

    def _download_image(self, prompt: str, out_path: Path, scene_num: int, style: str = None) -> str:
        style_desc = style or self.default_style
        clean_p = self._clean_prompt(prompt)
        full_prompt = f"{clean_p}, {style_desc}"
        encoded = urllib.parse.quote(full_prompt)
        
        seed = (int(time.time() * 1000) % 900000) + (scene_num * 17)
        
        urls_to_try = [
            f"{self.base_url}{encoded}?width=1920&height=1080&nologo=true&seed={seed}&model=turbo",
            f"{self.base_url}{encoded}?width=1920&height=1080&nologo=true&seed={seed}",
            f"{self.base_url}{urllib.parse.quote(clean_p)}?width=1920&height=1080&nologo=true&seed={seed}&model=turbo"
        ]

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        for url in urls_to_try:
            for attempt in range(3):
                try:
                    res = requests.get(url, headers=headers, timeout=50)
                    if res.status_code == 200 and len(res.content) > 5000:
                        with open(out_path, "wb") as f:
                            f.write(res.content)
                        with Image.open(out_path) as img:
                            img.verify()
                        return str(out_path)
                except Exception:
                    time.sleep(2)

        prev_scene_path = out_path.parent / f"scene_{max(1, scene_num - 1):03d}.jpg"
        if prev_scene_path.exists() and prev_scene_path != out_path:
            shutil.copy(prev_scene_path, out_path)
            return str(out_path)

        self._create_cinematic_fallback(out_path, scene_num)
        return str(out_path)

    def _create_cinematic_fallback(self, out_path: Path, scene_num: int):
        img = Image.new("RGB", (1920, 1080), color=(15, 23, 42))
        draw = ImageDraw.Draw(img)
        draw.rectangle([60, 60, 1860, 1020], outline=(56, 189, 248), width=6)
        img.save(out_path, quality=95)

    def batch_generate_images(self, scenes: list, output_dir: Path, style: str = None, max_workers: int = 3) -> list:
        output_dir.mkdir(parents=True, exist_ok=True)
        results = [None] * len(scenes)

        print(f"[ImageGenerator] Generating {len(scenes)} images with reliable rate-limiting...")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {}
            for idx, scene in enumerate(scenes):
                s_num = scene.get("scene_number", idx + 1)
                prompt = scene.get("visual_prompt", "Cinematic documentary visual")
                img_p = output_dir / f"scene_{s_num:03d}.jpg"
                
                time.sleep(0.15)
                fut = executor.submit(self._download_image, prompt, img_p, s_num, style)
                future_map[fut] = idx

            for fut in as_completed(future_map):
                i = future_map[fut]
                results[i] = fut.result()

        return results
