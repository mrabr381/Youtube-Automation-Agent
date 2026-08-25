import json
import google.generativeai as genai
from core.topic_researcher import get_best_model

class ScriptWriter:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_full_script(self, topic_info: dict, target_word_count: int = 1550, num_scenes: int = 75) -> dict:
        model = get_best_model(self.api_key)
        prompt = f"""
You are a master viral YouTube story writer and documentary producer.
Write a gripping, suspenseful, emotionally intense video script on:
Title: {topic_info.get('topic_title')}
Hook: {topic_info.get('hook')}

CRITICAL PACING REQUIREMENT:
1. Divide the entire 1500-1600 words into exactly {num_scenes} sequential scene segments (each scene roughly 18-22 words, corresponding to 6-8 seconds of speech).
2. For EVERY scene, provide:
   - `scene_number`: 1 to {num_scenes}
   - `narration`: The exact spoken dialogue or narration sentence.
   - `visual_prompt`: A unique, detailed anime graphic novel / dark webtoon illustration description (describe the characters, action, emotional expression, environment, lighting).

Format strictly as JSON:
{{
    "full_title": "Final Viral Video Title",
    "scenes": [
        {{
            "scene_number": 1,
            "narration": "First spoken line...",
            "visual_prompt": "Dark anime graphic novel scene of..."
        }}
    ]
}}
"""
        response = model.generate_content(prompt)
        text = response.text.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        
        full_text = " ".join([s.get("narration", "") for s in data.get("scenes", [])])
        data["full_narration_text"] = full_text
        data["actual_word_count"] = len(full_text.split())
        return data
