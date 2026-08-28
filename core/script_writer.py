import json
import google.generativeai as genai
from core.topic_researcher import get_best_model

class ScriptWriter:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_full_script(self, topic_info: dict, target_word_count: int = 1550, num_scenes: int = 75) -> dict:
        model = get_best_model(self.api_key)
        prompt = f"""
You are a documentary producer. Write a script on: {topic_info.get('topic_title')}

Divide the {target_word_count} words into exactly {num_scenes} sequential scenes.
For EVERY scene, provide:
- `scene_number`: 1 to {num_scenes}
- `narration`: The exact spoken dialogue.
- `visual_prompt`: A HIGHLY DETAILED prompt. If a character is visible, you MUST include: "close-up portrait, perfectly symmetrical face, highly detailed eyes, hyper-realistic facial features, flawless anatomy, sharp focus."

Format strictly as JSON:
{{
    "full_title": "Final Video Title",
    "scenes": [
        {{
            "scene_number": 1,
            "narration": "...",
            "visual_prompt": "..."
        }}
    ]
}}
"""
        response = model.generate_content(prompt)
        text = response.text.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        
        full_text = " ".join([s.get("narration", "") for s in data.get("scenes", [])])
        data["full_narration_text"] = full_text
        return data
