import os
import time
import base64
import shutil
import urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from PIL import Image

class ImageGenerator:
    def __init__(self, api_key: str = "", default_style: str = "detailed 2D anime graphic novel illustration, modern webtoon aesthetic, sharp inked line art, cinematic moody lighting, dramatic shadows, muted color palette, highly detailed background, 8k"):
        self.api_key = api_key
        self.default_style = default_style

    def _generate_with_google_imagen(self, prompt: str, out_path: Path) -> bool:
        if not self.api_key:
            return False

        url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={self.api_key}"
        payload = {
            "instances": [{"prompt": f"{prompt}, {self.default_style}"}],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": "16:9",
                "outputMimeType": "image/jpeg"
            }
        }

        try:
            res = requests.post(url, json=payload, timeout=40)
            if res.status_code == 200:
                data = res.json()
                predictions = data.get("predictions", [])
                if predictions and "bytesBase64Encoded" in predictions[0]:
                    img_data = base64.b64decode(predictions[0]["bytesBase64Encoded"])
                    with open(out_path, "wb") as f:
                        f.write(img_data)
                    return True
        except Exception:
            pass
        return False

    def _generate_with_flux_turbo(self, prompt: str, out_path: Path, scene_num: int, style: str = None) -> bool:
        style_desc = style or self.default_style
        words = prompt.replace("\n", " ").strip().split()
        clean_p = " ".join(words[:22])
        full_p = f"{clean_p}, {style_desc}"
        encoded = urllib.parse.quote(full_p)
        seed = (int(time.time() * 1000) % 800000) + (scene_num * 23)

        urls = [
            f"https://image.pollinations.ai/prompt/{encoded}?width=1920&height=1080&nologo=true&seed={seed}&model=turbo",
            f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&nologo=true&seed={seed}"
        ]

        headers = {"User-Agent": "Mozilla/5.0"}
        for url in urls:
            for _ in range(2):
                try:
                    res = requests.get(url, headers=headers, timeout=25)
                    if res.status_code == 200 and len(res.content) > 10000:
                        with open(out_path, "wb") as f:
                            f.write(res.content)
                        return True
                except Exception:
                    time.sleep(1)
        return False

    def _download_single_image(self, prompt: str, out_path: Path, scene_num: int, style: str = None) -> str:
        if self._generate_with_google_imagen(prompt, out_path):
            return str(out_path)

        if self._generate_with_flux_turbo(prompt, out_path, scene_num, style):
            return str(out_path)

        prev_scene_path = out_path.parent / f"scene_{max(1, scene_num - 1):03d}.jpg"
        if prev_scene_path.exists() and prev_scene_path != out_path:
            shutil.copy(prev_scene_path, out_path)
            return str(out_path)

        return str(out_path)

    def batch_generate_images(self, scenes: list, output_dir: Path, style: str = None, max_workers: int = 3) -> list:
        output_dir.mkdir(parents=True, exist_ok=True)
        results = [None] * len(scenes)

        print(f"[ImageGenerator] Generating {len(scenes)} visual scenes with high-res engines...")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {}
            for idx, scene in enumerate(scenes):
                s_num = scene.get("scene_number", idx + 1)
                prompt = scene.get("visual_prompt", "Graphic novel drama scene")
                img_p = output_dir / f"scene_{s_num:03d}.jpg"
                
                time.sleep(0.1)
                fut = executor.submit(self._download_single_image, prompt, img_p, s_num, style)
                future_map[fut] = idx

            for fut in as_completed(future_map):
                i = future_map[fut]
                results[i] = fut.result()

        valid_fallback = None
        for r in results:
            if r and os.path.exists(r) and os.path.getsize(r) > 1000:
                valid_fallback = r
                break

        if valid_fallback:
            for idx, r in enumerate(results):
                if not r or not os.path.exists(r) or os.path.getsize(r) < 1000:
                    shutil.copy(valid_fallback, results[idx])

        return results
