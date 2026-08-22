import json
import google.generativeai as genai

class TopicResearcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)

    def find_trending_topic(self, niche: str) -> dict:
        if not self.api_key:
            raise ValueError("Gemini API Key is missing. Please enter it in Settings.")

        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
You are an expert YouTube strategist.
Analyze the niche: "{niche}".
Identify the single most compelling, high-CTR, trending, and viral topic for today.

Respond strictly in JSON:
{{
    "topic_title": "Video title concept",
    "hook": "1-sentence hook",
    "angle": "Storytelling angle",
    "key_takeaways": ["Point 1", "Point 2", "Point 3", "Point 4"]
}}
"""
        response = model.generate_content(prompt)
        text = response.text.strip().replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(text)
        except Exception:
            return {
                "topic_title": f"The Evolution of {niche}",
                "hook": f"What if everything you thought you knew about {niche} was completely wrong?",
                "angle": "Investigative breakdown",
                "key_takeaways": ["Core Shift", "Hidden Factors", "Future Impact"]
            }