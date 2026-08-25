import os
import time
import shutil
import urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from PIL import Image, ImageDraw

class ImageGenerator:
    def __init__(self, api_key: str = "", default_style: str = "detailed 2D anime graphic novel illustration, modern webtoon aesthetic, sharp inked line art, cinematic moody lighting, dramatic shadows, muted color palette, highly detailed background environment, serious tone, 8k resolution"):
        self.api_key = api_key
        self.default_style = default_style
        self.base_url = "https://image.pollinations.ai/prompt/"

    def _clean_prompt(self, prompt: str) -> str:
        words = prompt.replace("\n", " ").strip().split()
        return " ".join(words[:22])

    def _download_single_image(self, prompt: str, out_path: Path, scene_num: int, style: str = None) -> str:
        style_desc = style or self.default_style
        clean_p = self._clean_prompt(prompt)
        full_prompt = f"{clean_p}, {style_desc}"
        encoded = urllib.parse.quote(full_prompt)
        
        seed = (int(time.time() * 1000) % 900000) + (scene_num * 37) + 101

        urls = [
            f"{self.base_url}{encoded}?width=1920&height=1080&nologo=true&seed={seed}&model=turbo",
            f"{self.base_url}{encoded}?width=1280&height=720&nologo=true&seed={seed}&model=turbo",
            f"{self.base_url}{urllib.parse.quote(clean_p + ', anime webtoon graphic novel 8k')}?width=1920&height=1080&nologo=true&seed={seed}"
        ]

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        for url in urls:
            for attempt in range(3):
                try:
                    res = requests.get(url, headers=headers, timeout=35)
                    if res.status_code == 200 and len(res.content) > 6000:
                        with open(out_path, "wb") as f:
                            f.write(res.content)
                        with Image.open(out_path) as img:
                            img.verify()
                        return str(out_path)
                except Exception:
                    time.sleep(1.5)

        prev_scene_path = out_path.parent / f"scene_{max(1, scene_num - 1):03d}.jpg"
        if prev_scene_path.exists() and prev_scene_path != out_path:
            shutil.copy(prev_scene_path, out_path)
            return str(out_path)

        self._create_aesthetic_fallback(out_path, scene_num)
        return str(out_path)

    def _create_aesthetic_fallback(self, out_path: Path, scene_num: int):
        img = Image.new("RGB", (1920, 1080), color=(24, 30, 48))
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 50, 1870, 1030], outline=(70, 130, 240), width=8)
        img.save(out_path, quality=95)

    def batch_generate_images(self, scenes: list, output_dir: Path, style: str = None, max_workers: int = 3) -> list:
        output_dir.mkdir(parents=True, exist_ok=True)
        results = [None] * len(scenes)

        print(f"[ImageGenerator] Generating {len(scenes)} distinct visual scenes...")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {}
            for idx, scene in enumerate(scenes):
                s_num = scene.get("scene_number", idx + 1)
                prompt = scene.get("visual_prompt", "Dramatic anime graphic novel scene")
                img_p = output_dir / f"scene_{s_num:03d}.jpg"
                
                time.sleep(0.1)
                fut = executor.submit(self._download_single_image, prompt, img_p, s_num, style)
                future_map[fut] = idx

            for fut in as_completed(future_map):
                i = future_map[fut]
                results[i] = fut.result()

        return results

    def generate_thumbnail(self, prompt: str, text_overlay: str, output_path: Path, style: str = None) -> str:
        """
        Generates an eye-catching 1080p YouTube Thumbnail with bold stylized text overlay.
        """
        style_desc = style or self.default_style
        thumb_prompt = f"{prompt}, close-up expressive face, high contrast, dramatic lighting, {style_desc}"
        encoded = urllib.parse.quote(thumb_prompt)
        seed = int(time.time() * 1000) % 999999
        url = f"{self.base_url}{encoded}?width=1920&height=1080&nologo=true&seed={seed}&model=turbo"

        temp_bg = output_path.parent / "thumb_raw.jpg"
        headers = {"User-Agent": "Mozilla/5.0"}
        downloaded = False

        for _ in range(3):
            try:
                res = requests.get(url, headers=headers, timeout=40)
                if res.status_code == 200 and len(res.content) > 5000:
                    with open(temp_bg, "wb") as f:
                        f.write(res.content)
                    downloaded = True
                    break
            except Exception:
                time.sleep(2)

        if not downloaded or not temp_bg.exists():
            img = Image.new("RGB", (1920, 1080), color=(18, 22, 35))
        else:
            img = Image.open(temp_bg).convert("RGB")
            img = img.resize((1920, 1080))

        draw = ImageDraw.Draw(img)
        display_text = (text_overlay or "THE TRUTH EXPOSED").upper()
        
        draw.rectangle([20, 20, 1900, 1060], outline=(255, 60, 60), width=12)

        tx, ty = 140, 840
        shadow_color = (0, 0, 0)
        main_color = (255, 225, 0)

        for dx in range(-8, 9):
            for dy in range(-8, 9):
                draw.text((tx + dx, ty + dy), display_text, fill=shadow_color)
        draw.text((tx, ty), display_text, fill=main_color)

        img.save(output_path, quality=95)
        if temp_bg.exists():
            temp_bg.unlink()

        print(f"[ImageGenerator] Custom YouTube Thumbnail created at: {output_path}")
        return str(output_path)
