import os
import json
from datetime import datetime
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from config import load_config, DATA_DIR, OUTPUT_DIR, CLIENT_SECRETS_FILE, TOKEN_FILE
from core.topic_researcher import TopicResearcher
from core.script_writer import ScriptWriter
from core.tts_engine import TTSEngine
from core.image_generator import ImageGenerator
from core.video_editor import VideoEditor
from core.seo_optimizer import SEOOptimizer
from core.youtube_uploader import YouTubeUploader

LOG_FILE = DATA_DIR / "pipeline_history.json"

class AutomationPipeline:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False

    def log_run(self, entry: dict):
        history = []
        if LOG_FILE.exists():
            try:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                pass
        history.insert(0, entry)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(history[:50], f, indent=4)

    def run_daily_pipeline(self, progress_callback=None) -> dict:
        if self.is_running:
            return {"status": "error", "message": "Pipeline already active."}

        self.is_running = True
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_folder = OUTPUT_DIR / run_id
        run_folder.mkdir(parents=True, exist_ok=True)
        images_dir = run_folder / "images"
        audio_dir = run_folder / "audio"

        log_data = {"run_id": run_id, "status": "in_progress", "steps": {}}

        try:
            cfg = load_config()
            api_key = cfg.get("gemini_api_key", "")
            niche = cfg.get("channel_niche", "AITA Stories & Drama")
            voice_name = cfg.get("voice_gender", "Female_US_Engaging")
            image_style = cfg.get("image_style", "detailed 2D anime graphic novel illustration, modern webtoon aesthetic, sharp inked line art, cinematic moody lighting, dramatic shadows, muted color palette, highly detailed background environment, serious tone, 8k resolution")
            num_images = int(cfg.get("images_per_video", 40))
            target_words = int(cfg.get("target_word_count", 1550))

            # 1. Topic
            if progress_callback: progress_callback("Step 1/7: Researching Viral Topic with Gemini...", 10)
            topic_info = TopicResearcher(api_key).find_trending_topic(niche)
            log_data["steps"]["topic"] = topic_info

            # 2. Script
            if progress_callback: progress_callback(f"Step 2/7: Writing 1500+ Word Script ({num_images} Scenes)...", 25)
            script_data = ScriptWriter(api_key).generate_full_script(topic_info, target_words, num_images)
            scenes = script_data.get("scenes", [])

            # 3. Voice-Over
            if progress_callback: progress_callback("Step 3/7: Generating Studio-Quality Voice-Over...", 40)
            tts = TTSEngine(voice=voice_name, api_key=api_key)
            audio_paths = []
            for s in scenes:
                p = audio_dir / f"scene_{s['scene_number']:03d}.mp3"
                tts.generate_scene_audio(s["narration"], str(p))
                audio_paths.append(str(p))

            # 4. Images
            if progress_callback: progress_callback(f"Step 4/7: Generating {len(scenes)} High-Res Anime Graphic Novel Visuals...", 60)
            img_gen = ImageGenerator(api_key=api_key, default_style=image_style)
            img_paths = img_gen.batch_generate_images(scenes, images_dir, style=image_style)

            # 5. Video Assembly
            if progress_callback: progress_callback("Step 5/7: Rendering 1080p HD Video...", 80)
            v_path = run_folder / f"{run_id}_final.mp4"
            final_video = VideoEditor().assemble_video(scenes, img_paths, audio_paths, v_path)
            log_data["video_path"] = str(final_video)

            # 6. SEO
            if progress_callback: progress_callback("Step 6/7: Generating YouTube SEO Metadata...", 90)
            seo_data = SEOOptimizer(api_key).generate_metadata(topic_info, script_data["full_narration_text"], niche)
            log_data["steps"]["seo"] = seo_data

            # 7. Upload
            if progress_callback: progress_callback("Step 7/7: Uploading to YouTube Channel...", 95)
            if TOKEN_FILE.exists():
                try:
                    uploader = YouTubeUploader(CLIENT_SECRETS_FILE, TOKEN_FILE)
                    up_res = uploader.upload_video(
                        Path(final_video),
                        title=seo_data.get("primary_title", "Story Essay"),
                        description=seo_data.get("description", ""),
                        tags=seo_data.get("tags", []),
                        category_id=seo_data.get("category_id", "24"),
                        privacy_status=cfg.get("youtube_privacy_status", "public")
                    )
                except Exception as upload_err:
                    up_res = {"status": "failed", "error": str(upload_err)}
            else:
                up_res = {
                    "status": "saved_locally",
                    "note": "token.json not uploaded. Video saved locally on server."
                }

            log_data["steps"]["upload"] = up_res
            log_data["status"] = "completed"

            if progress_callback: progress_callback("Complete!", 100)
            return log_data

        except Exception as e:
            log_data["status"] = "failed"
            log_data["error"] = str(e)
            return log_data
        finally:
            self.is_running = False
            self.log_run(log_data)

    def start_scheduler(self):
        cfg = load_config()
        if not cfg.get("auto_run_enabled", True):
            return
        t = cfg.get("schedule_time", "10:00")
        try:
            h, m = map(int, t.split(":"))
        except Exception:
            h, m = 10, 0
        self.scheduler.remove_all_jobs()
        self.scheduler.add_job(self.run_daily_pipeline, CronTrigger(hour=h, minute=m), id="daily_run")
        if not self.scheduler.running:
            self.scheduler.start()
