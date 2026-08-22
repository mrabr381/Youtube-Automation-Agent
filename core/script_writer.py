import json
import google.generativeai as genai
from core.topic_researcher import get_best_model

class ScriptWriter:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_full_script(self, topic_info: dict, target_word_count: int = 1550, num_scenes: int = 110) -> dict:
        model = get_best_model(self.api_key)
        prompt = f"""
You are a documentary YouTube scriptwriter.
Write an engaging, immersive 1500-1600 word script on:
Title: {topic_info.get('topic_title')}
Hook: {topic_info.get('hook')}

Divide the entire narration into approximately {num_scenes} continuous sequential scenes.
For each scene, provide the exact spoken narration text and a matching visual image prompt.

Respond strictly in JSON format:
{{
    "full_title": "Final Video Title",
    "scenes": [
        {{
            "scene_number": 1,
            "narration": "Spoken sentence...",
            "visual_prompt": "Detailed cinematic visual scene description..."
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
