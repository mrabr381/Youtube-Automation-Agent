import os
import time
import urllib.parse
from pathlib import Path
import requests

class ImageGenerator:
    def __init__(self, api_key: str = "", default_style: str = "sharp focus, masterpiece, 8k resolution"):
        self.default_style = default_style
        self.base_url = "https://image.pollinations.ai/prompt/"

    def batch_generate_images(self, scenes: list, output_dir: Path, style: str = None, max_workers: int = 1) -> list:
        output_dir.mkdir(parents=True, exist_ok=True)
        results = []
        style_desc = style or self.default_style

        print(f"[ImageGenerator] Generating {len(scenes)} images sequentially to avoid rate limits...")
        
        for idx, scene in enumerate(scenes):
            s_num = scene.get("scene_number", idx + 1)
            raw_prompt = scene.get("visual_prompt", "Detailed scene")
            
            clean_p = " ".join(raw_prompt.replace("\n", " ").strip().split()[:30])
            full_prompt = f"{clean_p}, {style_desc}"
            encoded = urllib.parse.quote(full_prompt)
            seed = (int(time.time() * 1000) % 900000) + s_num
            
            url = f"{self.base_url}{encoded}?width=1920&height=1080&nologo=true&seed={seed}&model=turbo"
            out_path = output_dir / f"scene_{s_num:03d}.jpg"
            
            success = False
            headers = {"User-Agent": "Mozilla/5.0"}
            
            # 5 retries with delays to bypass rate limits
            for attempt in range(5):
                try:
                    res = requests.get(url, headers=headers, timeout=30)
                    if res.status_code == 200 and len(res.content) > 10000:
                        with open(out_path, "wb") as f:
                            f.write(res.content)
                        success = True
                        break
                    else:
                        print(f"Rate limited on scene {s_num}, retrying in 3 seconds...")
                        time.sleep(3)
                except Exception as e:
                    time.sleep(3)
            
            if success:
                results.append(str(out_path))
            else:
                # Use previous image if completely blocked
                prev = output_dir / f"scene_{max(1, s_num - 1):03d}.jpg"
                if prev.exists():
                    import shutil
                    shutil.copy(prev, out_path)
                results.append(str(out_path))
                
            time.sleep(1.5) # Forced delay between requests

        return results
