import os
import json
from pathlib import Path

try:
    from dotenv import load_dotenv
    has_dotenv = True
except ImportError:
    has_dotenv = False

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
CLIENT_SECRETS_FILE = BASE_DIR / "client_secret.json"
TOKEN_FILE = BASE_DIR / "token.json"
CONFIG_FILE = BASE_DIR / "config.json"

DATA_DIR.mkdir(exist_ok=True, parents=True)
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

if has_dotenv and (BASE_DIR / ".env").exists():
    load_dotenv(BASE_DIR / ".env")

DEFAULT_CONFIG = {
    "gemini_api_key": os.getenv("GEMINI_API_KEY", ""),
    "channel_niche": os.getenv("CHANNEL_NICHE", "Artificial Intelligence & Future Tech"),
    "voice_gender": os.getenv("VOICE_GENDER", "Male"),
    "voice_name": os.getenv("VOICE_NAME", "en-US-GuyNeural"),
    "image_style": os.getenv("IMAGE_STYLE", "Cinematic, Photorealistic, 8k, Octane render, Dramatic lighting"),
    "images_per_video": int(os.getenv("IMAGES_PER_VIDEO", "110")),
    "schedule_time": os.getenv("SCHEDULE_TIME", "10:00"),
    "auto_run_enabled": os.getenv("AUTO_RUN_ENABLED", "true").lower() == "true",
    "youtube_privacy_status": os.getenv("YOUTUBE_PRIVACY_STATUS", "public"),
    "target_word_count": 1550
}

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                cfg = DEFAULT_CONFIG.copy()
                cfg.update(saved)
                return cfg
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(new_config: dict):
    cfg = load_config()
    cfg.update(new_config)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)
    return cfg