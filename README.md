# 🎬 YouTube Automation Agent (100% Free & Autonomous)

An end-to-end autonomous YouTube content creation and daily publishing pipeline. This agent discovers trending topics in your niche, writes long-form scripts (1500–1600 words), generates voice-overs, creates 100–120 visual images, edits video with dynamic animations, optimizes SEO, and publishes directly to YouTube on a daily schedule.

---

## ✨ Features

- **🔍 Automated Topic Discovery:** Uses Google Gemini API to analyze your niche and find high-CTR trending topics.
- **✍️ Long-Form Scriptwriting:** Writes immersive 1500–1600 word documentary-style scripts divided into ~110 visual scenes.
- **🎙️ Neural Text-to-Speech:** Generates natural human-like voice-overs (Male & Female voices) via Microsoft Edge Neural TTS.
- **🎨 Batch Visual Generation:** Produces 100–120 high-definition 16:9 images per video matching your chosen art style (FLUX engine).
- **🎞️ Dynamic Video Editing:** Syncs images to narration, applies Ken Burns pan/zoom motion effects, and adds crossfade transitions.
- **📈 Complete SEO Optimization:** Generates click-worthy titles, full descriptions with chapter timestamps, search tags, and hashtags.
- **🚀 Automated YouTube Upload:** Connects via YouTube Data API v3 to upload scheduled videos with custom privacy settings.
- **⏰ Daily Background Scheduler:** Set-and-forget automation that triggers every day at your specified time.
- **💻 Streamlit Web UI:** Clean, intuitive dashboard to manage API keys, select styles, preview videos, and track logs.

---

## 🛠️ Zero-Cost Tech Stack

| Module | Engine / Tool | Pricing |
| :--- | :--- | :--- |
| **Topic & Script Engine** | Google Gemini 1.5 Flash API | **Free Tier** |
| **Voice-Over (TTS)** | Edge Neural TTS (`edge-tts`) | **100% Free** (No API Key Required) |
| **Visual Generator** | Pollinations / FLUX AI | **100% Free** (No API Key Required) |
| **Video Processing** | Python (`MoviePy` + `FFmpeg`) | **100% Free** (Runs Locally) |
| **SEO Generator** | Google Gemini API | **Free Tier** |
| **YouTube Publishing** | YouTube Data API v3 | **Free** (10,000 daily quota units) |
| **Control Dashboard** | Streamlit | **Open Source** |

---

## 📁 Repository Structure

```text
youtube-automation-agent/
├── app.py                     # Streamlit Web UI Dashboard
├── config.py                  # Settings & Paths Manager
├── requirements.txt           # Python Dependencies
├── .env.example               # Template Environment Variables
├── .gitignore                 # Git ignore rules
├── README.md                  # Project Documentation
├── core/
│   ├── topic_researcher.py    # Trending Topic Research Module
│   ├── script_writer.py       # 1500-Word Script Generator
│   ├── tts_engine.py          # Edge-TTS Audio Generator
│   ├── image_generator.py     # Batch Image Generator (FLUX Engine)
│   ├── video_editor.py        # MoviePy & FFmpeg Video Assembly
│   ├── seo_optimizer.py       # Title, Description, & Tag Generator
│   ├── youtube_uploader.py    # YouTube Data API v3 OAuth Uploader
│   └── scheduler.py           # Background Automation Scheduler
├── data/                      # Run history and credentials
└── output/                    # Local renders, audio, and images