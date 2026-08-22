import time
import urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from PIL import Image, ImageDraw

class ImageGenerator:
    def __init__(self, default_style: str = "cinematic, photorealistic, 8k, dramatic lighting"):
        self.default_style = default_style
        self.base_url = "https://image.pollinations.ai/prompt/"

    def _download_image(self, prompt: str, out_path: Path, scene_num: int, style: str = None) -> str:
        style_desc = style or self.default_style
        full_prompt = f"{prompt}, {style_desc}"
        encoded = urllib.parse.quote(full_prompt)
        seed = int(time.time() * 1000) % 1000000 + scene_num
        url = f"{self.base_url}{encoded}?width=1920&height=1080&nologo=true&seed={seed}&model=flux"

        headers = {"User-Agent": "Mozilla/5.0"}
        for _ in range(3):
            try:
                res = requests.get(url, headers=headers, timeout=35)
                if res.status_code == 200 and len(res.content) > 1000:
                    with open(out_path, "wb") as f:
                        f.write(res.content)
                    return str(out_path)
            except Exception:
                time.sleep(2)

        # Fallback Graphic if connection drops
        img = Image.new("RGB", (1920, 1080), color=(20, 24, 35))
        draw = ImageDraw.Draw(img)
        draw.text((100, 500), f"Scene {scene_num}\n{prompt[:80]}...", fill=(240, 240, 240))
        img.save(out_path)
        return str(out_path)

    def batch_generate_images(self, scenes: list, output_dir: Path, style: str = None, max_workers: int = 5) -> list:
        output_dir.mkdir(parents=True, exist_ok=True)
        results = [None] * len(scenes)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {}
            for idx, scene in enumerate(scenes):
                s_num = scene.get("scene_number", idx + 1)
                prompt = scene.get("visual_prompt", "Cinematic Scene")
                img_p = output_dir / f"scene_{s_num:03d}.jpg"
                fut = executor.submit(self._download_image, prompt, img_p, s_num, style)
                future_map[fut] = idx

            for fut in as_completed(future_map):
                i = future_map[fut]
                results[i] = fut.result()

        return results