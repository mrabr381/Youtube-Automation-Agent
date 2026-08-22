import json
import google.generativeai as genai
from core.topic_researcher import get_best_model

class SEOOptimizer:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_metadata(self, topic_info: dict, script_summary: str, niche: str) -> dict:
        model = get_best_model(self.api_key)
        prompt = f"""
You are a YouTube SEO Specialist.
Generate metadata for this video:
Niche: {niche}
Topic: {topic_info.get('topic_title')}
Summary: {script_summary[:800]}

Respond strictly in JSON:
{{
    "primary_title": "High CTR Clickable Title",
    "description": "Engaging description with timestamps and keywords...",
    "tags": ["tag1", "tag2", "tag3"],
    "hashtags": ["#Tag1", "#Tag2", "#Tag3"],
    "category_id": "28"
}}
"""
        response = model.generate_content(prompt)
        text = response.text.strip().replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(text)
        except Exception:
            return {
                "primary_title": topic_info.get("topic_title", "Documentary Feature"),
                "description": f"Exploring {niche} in depth.",
                "tags": [niche, "documentary", "explained", "breakdown"],
                "hashtags": ["#YouTube", "#Trends"],
                "category_id": "28"
            }
