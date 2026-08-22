import asyncio
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
    def __init__(self, voice: str = "en-US-GuyNeural"):
        self.voice = voice if voice in VOICE_MAP.values() else VOICE_MAP.get(voice, "en-US-GuyNeural")

    async def _generate_async(self, text: str, output_path: str):
        communicate = edge_tts.Communicate(text=text, voice=self.voice)
        await communicate.save(output_path)

    def generate_scene_audio(self, text: str, output_path: str) -> str:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        asyncio.run(self._generate_async(text, output_path))
        return output_path