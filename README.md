# 🎬 AI YouTube Automation Agent
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
- **💻 Clean Streamlit Web UI:** Password-protected control dashboard to customize styles, select voices, manage keys, and track live generation logs.

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

### 1. Clone the Repository
Clone this repository to your local computer and navigate into the project directory:
```bash
git clone [https://github.com/your-username/youtube-automation-agent.git](https://github.com/your-username/youtube-automation-agent.git)
cd youtube-automation-agent

```

---

### 2. Create and Activate Virtual Environment

Set up an isolated Python virtual environment to manage dependencies cleanly:

* **On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate

```


* **On Windows (Command Prompt / PowerShell):**
```cmd
python -m venv venv
venv\Scripts\activate

```



---

### 3. Install Required Dependencies

Upgrade `pip` to the latest version and install all required Python libraries:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt

```

---

### 4. Configure Environment Variables

Create your local environment configuration file from the provided template:

* **On macOS / Linux:**
```bash
cp .env.example .env

```


* **On Windows:**
```cmd
copy .env.example .env

```



Open the `.env` file in your text editor and configure your preferences:

```env
# Gemini API Key (Get free from [https://aistudio.google.com/](https://aistudio.google.com/))
GEMINI_API_KEY=your_gemini_api_key_here

# Channel Niche & Topic Domain
CHANNEL_NICHE=AITA Stories & Drama

# Voice-Over Selection (Options: Female_US_Engaging, Male_US_Deep, Male, Female, Male_UK, Female_UK, Male_Urdu, Female_Urdu)
VOICE_GENDER=Female_US_Engaging

# Visual Art Style Modifier
IMAGE_STYLE=detailed 2D anime graphic novel illustration, modern webtoon aesthetic, sharp inked line art, cinematic moody lighting, dramatic shadows, muted color palette, highly detailed background environment, serious tone, 8k resolution

# Target Scenes & Schedule Time
IMAGES_PER_VIDEO=40
SCHEDULE_TIME=10:00
AUTO_RUN_ENABLED=true
YOUTUBE_PRIVACY_STATUS=public

```

---

### 5. 🔐 One-Time YouTube Channel Authorization

To enable the agent to automatically upload scheduled videos to your YouTube channel:

#### Step A: Obtain Google Cloud OAuth Client ID

1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g. `YouTube-Automation-Bot`).
3. Navigate to **APIs & Services > Library**, search for **YouTube Data API v3**, and click **Enable**.
4. Go to **APIs & Services > Credentials** > **Create Credentials** > **OAuth Client ID**.
5. Set the Application Type to **Desktop App** and name it `YouTube Uploader`.
6. Download the generated JSON credentials file, rename it to `client_secret.json`, and place it in your local project root folder.

#### Step B: Generate `token.json`

Run the included token generation script in your terminal:

```bash
python get_youtube_token.py

```

1. Your default web browser will open displaying the Google login screen.
2. Select your Google account that owns the target YouTube channel.
3. Click **Continue / Allow** to grant YouTube upload permissions.
4. The script will save a **`token.json`** file in your project directory.

#### Step C: Link with Web Dashboard

* Open the Streamlit Web UI, navigate to the **⚙️ Settings & Configuration** tab.
* Upload your **`token.json`** file (or paste its content directly into the text box) and click **Save Token**.
* Your channel is now authenticated forever with automated background token refresh!

---

### 6. 💻 Running the Web Dashboard

Launch the Streamlit interactive control center:

```bash
streamlit run app.py

```

Once running, open your web browser at:

```
http://localhost:8501

```

#### Dashboard Controls:

* **🚀 Control Panel:** Click **"Generate & Publish Video Now"** for instant on-demand video creation with real-time progress updates and built-in video preview.
* **⚙️ Settings & Configuration:** Update your Gemini API key, change art styles, switch voices, modify schedules, and connect your YouTube token.
* **📜 History & Logs:** View records of past automated runs, generated scripts, titles, and direct YouTube video URLs.



---

## 📁 Project Architecture & File Directory

```text
youtube-automation-agent/
├── app.py                     # Streamlit Web Control Dashboard (Password Protected)
├── config.py                  # Environment & Settings Configuration Manager
├── requirements.txt           # Python Dependency Specifications
├── packages.txt               # System Linux Dependencies (FFmpeg for Streamlit Cloud)
├── get_youtube_token.py       # Local One-Time OAuth Token Generator
├── .env.example               # Configuration Template
├── .gitignore                 # Git Ignore Security Rules
├── README.md                  # Comprehensive Documentation
├── core/
│   ├── __init__.py            # Python Package Initializer
│   ├── topic_researcher.py    # Gemini Trending Topic Discovery Engine
│   ├── script_writer.py       # 1500-Word Script Generator (40 Scenes)
│   ├── tts_engine.py          # Google AI Studio & Edge-TTS Voice Generator
│   ├── image_generator.py     # Google Imagen 3 & FLUX 1080p Visual Engine
│   ├── video_editor.py        # FFmpeg Low-RAM Video Assembly Engine
│   ├── seo_optimizer.py       # YouTube SEO & Metadata Generator
│   ├── youtube_uploader.py    # YouTube Data API v3 OAuth Uploader
│   └── scheduler.py           # Background Daily Automation Scheduler
├── data/                      # Run history logs and credentials
└── output/                    # Rendered videos, audio files, and images

```

---

## 📄 License

This project is open-source software licensed under the **MIT License**. See the `LICENSE` file for details.

```

```
