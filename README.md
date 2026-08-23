[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://youtube-automation-agent-1.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end, 100% free, fully autonomous YouTube content generation and daily publishing engine. Powered by Google Gemini AI, Google Imagen 3, FLUX, Edge-TTS, and FFmpeg.

🌐 **Live Web Dashboard:** [https://youtube-automation-agent-1.streamlit.app/](https://youtube-automation-agent-1.streamlit.app/)

---

## ✨ Features

- **🔍 Automated Topic Discovery:** Uses Google Gemini AI to analyze your niche daily and select viral, high-CTR topics.
- **✍️ Long-Form Scriptwriting:** Writes comprehensive 1500–1600 word scripts divided into ~40 visual scenes (~18s per scene).
- **🎙️ Studio-Quality Voice-Overs:** Generates natural male & female voice narration using Google AI Studio (Gemini 2.0 Flash Audio) and Microsoft Edge Neural TTS.
- **🎨 High-Definition 1080p Visuals:** Produces anime graphic novel / dark webtoon / cinematic artwork using Google Imagen 3 and FLUX engines.
- **🎞️ Dynamic Video Assembly:** Direct streaming FFmpeg engine applying crisp Ken Burns pan/zoom animations and seamless transitions.
- **📈 Complete SEO Optimization:** Generates click-worthy titles, full descriptions with chapter timestamps, search tags, and hashtags.
- **🚀 Automated YouTube Upload:** Uploads scheduled videos directly to your YouTube channel with custom privacy settings (Public, Unlisted, Private).
- **⏰ Set-and-Forget Scheduler:** Background daily automation running autonomously at your specified time.
- **💻 Clean Streamlit Web UI:** Intuitive control dashboard to customize styles, select voices, manage keys, and track live generation logs.

---

## 🛠️ Zero-Cost Tech Stack

| Module | Engine / Tool | Pricing |
| :--- | :--- | :--- |
| **Topic & Script Engine** | Google Gemini API (AI Studio) | **Free Tier** |
| **Voice-Over (TTS)** | Google AI Studio Audio & Edge-TTS | **100% Free** |
| **Visual Art Generation** | Google Imagen 3 & FLUX Engine | **100% Free** |
| **Video Processing** | Python + FFmpeg Streaming Engine | **100% Free** (Ultra-Low RAM) |
| **YouTube Publishing** | YouTube Data API v3 (OAuth2) | **100% Free** (10,000 daily quota units) |
| **Web Dashboard** | Streamlit Community Cloud | **100% Free** |

---

## 📋 Prerequisites & System Requirements

Before installing, ensure your environment meets the following requirements:

1. **Python 3.8 or higher** installed on your system.
2. **Git** installed on your machine.
3. **FFmpeg** installed (Required for video assembly and Ken Burns animation):
   - **macOS:**
     ```bash
     brew install ffmpeg
     ```
   - **Ubuntu / Debian Linux:**
     ```bash
     sudo apt update && sudo apt install -y ffmpeg
     ```
   - **Windows:**
     Download FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extract it, and add the `bin` folder to your System PATH variables.
4. **Google Gemini API Key** (Get a free key from [Google AI Studio](https://aistudio.google.com/)).

---

## 🚀 Complete Installation & Setup Guide

Follow these steps to set up and run the YouTube Automation Agent locally:

### 1. Clone the Repository
Clone this repository to your local computer and navigate into the project directory:
```bash
git clone [https://github.com/your-username/youtube-automation-agent.git](https://github.com/your-username/youtube-automation-agent.git)
```
```bash
cd youtube-automation-agent
```
### 2. Create and Activate Virtual Environment
Set up an isolated Python virtual environment to manage dependencies cleanly:

 - **On macOS / Linux:**
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
 - **On Windows (Command Prompt / PowerShell):**
 ```bash
     python -m venv venv
     ```
```bash
venv\Scripts\activate
```
