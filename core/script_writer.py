import json
import google.generativeai as genai
from core.topic_researcher import get_best_model

class ScriptWriter:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_full_script(self, topic_info: dict, target_word_count: int = 1550, num_scenes: int = 40) -> dict:
        model = get_best_model(self.api_key)
        prompt = f"""
You are a master documentary YouTube scriptwriter.
Write an engaging, immersive 1500-1600 word narrative video essay script on:
Title: {topic_info.get('topic_title')}
Hook: {topic_info.get('hook')}

Divide the entire 1500-word narration into exactly {num_scenes} continuous sequential scenes (each around 35-45 words).
For each scene, provide:
1. `narration`: The exact natural spoken sentence(s).
2. `visual_prompt`: A detailed, descriptive 2D anime graphic novel / dark webtoon illustration prompt.

Respond strictly in JSON format:
{{
    "full_title": "Final Catchy Video Title",
    "scenes": [
        {{
            "scene_number": 1,
            "narration": "Exact spoken narration text...",
            "visual_prompt": "Detailed dark anime graphic novel scene, atmospheric lighting..."
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
