import sys
import os
import json
from pathlib import Path
import streamlit as st

# Streamlit Cloud Path Fix
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import load_config, save_config, CLIENT_SECRETS_FILE, TOKEN_FILE
from core.scheduler import AutomationPipeline, LOG_FILE
from core.tts_engine import VOICE_MAP

st.set_page_config(page_title="YouTube Automation Agent", page_icon="🎬", layout="wide")

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
    col1, col2, col3 = st.columns(3)
    col1.metric("Niche", config.get("channel_niche"))
    col2.metric("Scheduled Time", config.get("schedule_time"))
    col3.metric("Voice", config.get("voice_gender"))

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
                st.success("✅ Video Generation Finished!")
                if os.path.exists(res.get("video_path", "")):
                    st.video(res.get("video_path"))
            else:
                st.error(f"Error: {res.get('error')}")

with tab2:
    with st.form("cfg_form"):
        gemini_key = st.text_input("Gemini API Key (Free):", value=config.get("gemini_api_key"), type="password")
        niche = st.text_input("Channel Niche:", value=config.get("channel_niche"))
        voice = st.selectbox("Voice:", list(VOICE_MAP.keys()), index=list(VOICE_MAP.keys()).index(config.get("voice_gender", "Male")))
        time_run = st.text_input("Daily Run Time (HH:MM 24h):", value=config.get("schedule_time"))
        privacy = st.selectbox("YouTube Privacy:", ["public", "unlisted", "private"])
        auto = st.checkbox("Enable Daily Auto Run", value=config.get("auto_run_enabled"))

        if st.form_submit_button("💾 Save Settings"):
            save_config({
                "gemini_api_key": gemini_key.strip(),
                "channel_niche": niche.strip(),
                "voice_gender": voice,
                "voice_name": VOICE_MAP[voice],
                "schedule_time": time_run.strip(),
                "youtube_privacy_status": privacy,
                "auto_run_enabled": auto
            })
            pipeline.start_scheduler()
            st.success("Settings updated!")

    st.divider()
    st.subheader("YouTube API (`client_secret.json`)")
    uploaded = st.file_uploader("Upload client_secret.json", type=["json"])
    if uploaded:
        with open(CLIENT_SECRETS_FILE, "wb") as f:
            f.write(uploaded.getbuffer())
        st.success("Credentials saved!")

with tab3:
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            st.json(json.load(f))
    else:
        st.info("No runs recorded yet.")