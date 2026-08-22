import asyncio
import base64
import requests
from pathlib import Path
import edge_tts

VOICE_MAP = {
    "Male": "en-US-GuyNeural",
    "Female": "en-US-JennyNeural",
    "Male_US_Deep": "en-US-ChristopherNeural",
    "Female_US_Engaging": "en-US-AriaNeural",
    "Male_UK": "en-GB-RyanNeural",
    "Female_UK": "en-GB-SoniaNeural",
    "Male_Urdu": "ur-PK-AsadNeural",
    "Female_Urdu": "ur-PK-UzmaNeural"
}

class TTSEngine:
    def __init__(self, voice: str = "Female_US_Engaging", api_key: str = ""):
        self.voice = voice
        self.api_key = api_key

    def _generate_with_google_ai_studio(self, text: str, output_path: str) -> bool:
        if not self.api_key:
            return False

        google_voices = {
            "Male": "Puck",
            "Female": "Kore",
            "Male_US_Deep": "Fenrir",
            "Female_US_Engaging": "Aoede",
            "Male_UK": "Charon",
            "Female_UK": "Aoede"
        }
        selected_voice = google_voices.get(self.voice, "Aoede")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": f"Read this text naturally as a narrator: {text}"}]}],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {
                            "voiceName": selected_voice
                        }
                    }
                }
            }
        }

        try:
            res = requests.post(url, json=payload, timeout=25)
            if res.status_code == 200:
                data = res.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    for part in parts:
                        if "inlineData" in part and part["inlineData"].get("mimeType", "").startswith("audio"):
                            audio_bytes = base64.b64decode(part["inlineData"]["data"])
                            with open(output_path, "wb") as f:
                                f.write(audio_bytes)
                            return True
        except Exception:
            pass
        return False

    async def _generate_edge_tts(self, text: str, output_path: str):
        edge_voice = VOICE_MAP.get(self.voice, "en-US-JennyNeural")
        communicate = edge_tts.Communicate(text=text, voice=edge_voice)
        await communicate.save(output_path)

    def generate_scene_audio(self, text: str, output_path: str) -> str:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        if self._generate_with_google_ai_studio(text, output_path):
            return output_path

        asyncio.run(self._generate_edge_tts(text, output_path))
        return output_path
