import json
import google.generativeai as genai

class ScriptWriter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)

    def generate_full_script(self, topic_info: dict, target_word_count: int = 1550, num_scenes: int = 110) -> dict:
        if not self.api_key:
            raise ValueError("Gemini API Key is missing.")

        model = genai.GenerativeModel("gemini-1.5-flash")
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