import json
import google.generativeai as genai

def get_best_model(api_key: str):
    if not api_key:
        raise ValueError("Gemini API Key is missing. Please add your key in Settings.")
    
    genai.configure(api_key=api_key)
    
    try:
        supported_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        # New Google Gemini model priority
        for preferred in [
            "models/gemini-3.6-flash",
            "models/gemini-2.0-flash",
            "models/gemini-1.5-flash",
            "models/gemini-1.5-pro",
            "models/gemini-pro"
        ]:
            if preferred in supported_models:
                return genai.GenerativeModel(preferred)
        
        if supported_models:
            return genai.GenerativeModel(supported_models[0])
    except Exception as e:
        print(f"[Model Loader] Note: {e}")

    return genai.GenerativeModel("gemini-3.6-flash")

class TopicResearcher:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def find_trending_topic(self, niche: str) -> dict:
        model = get_best_model(self.api_key)
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
                "topic_title": f"The Untold Truth of {niche}",
                "hook": f"What if everything you thought you knew about {niche} was completely wrong?",
                "angle": "Deep-dive documentary breakdown",
                "key_takeaways": ["Core Shift", "Hidden Realities", "Future Impact"]
            }
