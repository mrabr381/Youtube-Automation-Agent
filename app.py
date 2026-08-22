import sys
import os
from pathlib import Path

# Streamlit Cloud Path Fix
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Pillow 10+ Compatibility Fix
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = getattr(PIL.Image, 'LANCZOS', getattr(PIL.Image.Resampling, 'LANCZOS', None))

import json
import time
import streamlit as st

from config import load_config, save_config, CLIENT_SECRETS_FILE, TOKEN_FILE
from core.scheduler import AutomationPipeline, LOG_FILE
from core.tts_engine import VOICE_MAP

st.set_page_config(
    page_title="AI YouTube Automation Agent",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "pipeline" not in st.session_state:
    p = AutomationPipeline()
    p.start_scheduler()
    st.session_state["pipeline"] = p

pipeline = st.session_state["pipeline"]
config = load_config()

st.title("🎬 AI YouTube Automation Agent")
st.caption("Autonomous Daily YouTube Video Production & Publishing Pipeline")

tab1, tab2, tab3 = st.tabs(["🚀 Control Panel", "⚙️ Settings & Configuration", "📜 History & Logs"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Niche", config.get("channel_niche", "Technology")[:15] + "...")
    col2.metric("Scheduled Time", config.get("schedule_time", "10:00"))
    col3.metric("Voice", config.get("voice_gender", "Male"))
    yt_connected = "Linked ✅" if TOKEN_FILE.exists() else "Not Linked ⚠️"
    col4.metric("YouTube Channel", yt_connected)

    st.divider()
    if st.button("🚀 Generate & Publish Video Now", type="primary", disabled=pipeline.is_running):
        pbar = st.progress(0)
        stext = st.empty()
        def callback(msg, val):
            stext.write(f"**{msg}**")
            pbar.progress(val)

        with st.spinner("Processing full video pipeline..."):
            res = pipeline.run_daily_pipeline(progress_callback=callback)
            if res.get("status") == "completed":
                st.success("✅ Video Generation Finished Successfully!")
                if os.path.exists(res.get("video_path", "")):
                    st.video(res.get("video_path"))
                
                upload_res = res.get("steps", {}).get("upload", {})
                if upload_res.get("status") == "success":
                    st.success(f"🎬 **Uploaded to YouTube:** [Watch Video]({upload_res.get('video_url')})")
                else:
                    st.info(f"ℹ️ {upload_res.get('note', 'Video rendered and saved on server.')}")
            else:
                st.error(f"Error: {res.get('error')}")

with tab2:
    st.subheader("⚙️ Agent Settings & Customization")
    with st.form("cfg_form"):
        gemini_key = st.text_input("Gemini API Key (Google AI Studio - Free):", value=config.get("gemini_api_key", ""), type="password")
        
        col_a, col_b = st.columns(2)
        with col_a:
            niche = st.text_input("Channel Niche / Topic Domain:", value=config.get("channel_niche", "Artificial Intelligence & Future Tech"))
            
            voice_options = list(VOICE_MAP.keys())
            current_voice = config.get("voice_gender", "Male")
            v_idx = voice_options.index(current_voice) if current_voice in voice_options else 0
            voice = st.selectbox("Voice-Over Gender & Accent:", voice_options, index=v_idx)
            
            time_run = st.text_input("Daily Run Time (HH:MM 24h format):", value=config.get("schedule_time", "10:00"))

        with col_b:
            image_style_presets = [
                "Cinematic, Photorealistic, 8k, Octane render, Dramatic lighting",
                "Hyper-realistic National Geographic Documentary style, 4k",
                "Dark Cyberpunk, Neon Glow, Highly Detailed Sci-Fi Art",
                "Vintage Retro 1970s Film Grain, Moody Aesthetic",
                "Studio Ghibli Anime style, Vibrant Watercolor scenery",
                "3D Pixar Animation style, Clean Character Render",
                "Dark Gothic Comic Book Illustration, High Contrast",
                "Custom (Type below)"
            ]
            current_style = config.get("image_style", image_style_presets[0])
            s_idx = image_style_presets.index(current_style) if current_style in image_style_presets else 0
            
            selected_preset = st.selectbox("Image Art Style Preset:", image_style_presets, index=s_idx)
            
            custom_style_input = st.text_input(
                "Custom Image Style Prompt / Modifier:",
                value=current_style if selected_preset == "Custom (Type below)" else "",
                help="Type any custom aesthetic or details for FLUX image generator."
            )
            
            final_style = custom_style_input.strip() if selected_preset == "Custom (Type below)" and custom_style_input.strip() else selected_preset

            privacy = st.selectbox("YouTube Privacy Status:", ["public", "unlisted", "private"], index=["public", "unlisted", "private"].index(config.get("youtube_privacy_status", "public")))

        auto = st.checkbox("Enable Daily Automated Scheduling", value=config.get("auto_run_enabled", True))

        if st.form_submit_button("💾 Save Settings", type="primary"):
            save_config({
                "gemini_api_key": gemini_key.strip(),
                "channel_niche": niche.strip(),
                "voice_gender": voice,
                "voice_name": VOICE_MAP[voice],
                "image_style": final_style,
                "schedule_time": time_run.strip(),
                "youtube_privacy_status": privacy,
                "auto_run_enabled": auto
            })
            pipeline.start_scheduler()
            st.success("✅ Configuration saved & Scheduler updated successfully!")
            st.rerun()

    st.divider()
    st.subheader("🔐 YouTube Channel Connection (`token.json`)")
    
    if TOKEN_FILE.exists():
        st.success("✅ YouTube Channel Linked Successfully!")
    else:
        st.warning("⚠️ YouTube Channel not connected yet. Upload or paste your `token.json` below.")

    col_up1, col_up2 = st.columns(2)
    with col_up1:
        st.markdown("**Option 1: Upload `token.json` File**")
        uploaded_token = st.file_uploader("Upload token.json:", type=["json"], key="token_upload")
        if uploaded_token:
            with open(TOKEN_FILE, "wb") as f:
                f.write(uploaded_token.getbuffer())
            st.success("✅ `token.json` saved!")
            st.rerun()

    with col_up2:
        st.markdown("**Option 2: Paste `token.json` Content Directly**")
        with st.form("paste_token_form"):
            token_text = st.text_area("Paste token.json content here:", height=100, placeholder='{"token": "...", "refresh_token": "...", ...}')
            if st.form_submit_button("💾 Save Token Text"):
                if token_text.strip():
                    try:
                        parsed = json.loads(token_text.strip())
                        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                            json.dump(parsed, f, indent=4)
                        st.success("✅ `token.json` saved!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Invalid JSON: {e}")

with tab3:
    st.subheader("📜 Generation History & Logs")
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r") as f:
                st.json(json.load(f))
        except Exception as e:
            st.error(f"Error loading logs: {e}")
    else:
        st.info("No runs recorded yet.")
