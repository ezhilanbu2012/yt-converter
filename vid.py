import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Video Downloader", page_icon="📹")

st.title("🎬 YouTube Video Downloader")
st.caption("Paste any YouTube URL to download the full video with audio!")

# inputs
url = st.text_input("🎥 YouTube URL", placeholder="Paste video link here...")
save_dir = st.text_input("📁 Save Directory", value="./videos")

# ensure directory exists
if save_dir and not os.path.exists(save_dir):
    try:
        os.makedirs(save_dir)
        st.info(f"Created directory: {save_dir}")
    except Exception as e:
        st.error(f"Couldn't create directory: {e}")

download_button = st.button("⬇️ Download Video")

if download_button:
    if not url.strip():
        st.warning("⚠️ Please enter a valid YouTube URL first!")
    else:
        try:
            st.info("Downloading... please wait ⏳")

            # yt-dlp config for video
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',  # combine video + audio
                'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),
                'quiet': True,
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                title = info_dict.get("title", "Unknown Video")

            video_path = os.path.join(save_dir, f"{title}.mp4")

            st.success(f"✅ '{title}' downloaded successfully!")
            st.video(video_path)
            st.download_button(
                label="🎥 Download Video",
                data=open(video_path, "rb").read(),
                file_name=f"{title}.mp4",
                mime="video/mp4"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")
