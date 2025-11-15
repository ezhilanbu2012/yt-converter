import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", page_icon="🎥")

st.title("🎧 YouTube Downloader — MP3 / MP4")
st.caption("Paste a YouTube URL, choose a format, and download it instantly!")

# user inputs
url = st.text_input("🎥 YouTube URL", placeholder="Paste the video link here...")
option = st.radio("Choose format:", ["Audio (MP3)", "Video (MP4)"])
save_dir = st.text_input("📁 Save Directory", value="./downloads")

# ensure directory exists
if save_dir and not os.path.exists(save_dir):
    try:
        os.makedirs(save_dir)
        st.info(f"Created directory: {save_dir}")
    except Exception as e:
        st.error(f"Couldn't create directory: {e}")

download_button = st.button("⬇️ Download")

if download_button:
    if not url.strip():
        st.warning("⚠️ Please enter a valid YouTube URL!")
    else:
        try:
            st.info("Downloading... please wait ⏳")

            # yt-dlp setup
            ydl_opts = {
                'quiet': True,
                'noplaylist': True,
            }

            if option == "Audio (MP3)":
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts.update({
                    'format': 'bestvideo+bestaudio/best',
                    'merge_output_format': 'mp4',
                })

            # store files by video ID in cache
            ydl_opts['outtmpl'] = os.path.join(save_dir, '%(id)s.%(ext)s')

            # download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "Unknown Title")
                vid_id = info.get("id", "unknown")

            ext = "mp3" if option == "Audio (MP3)" else "mp4"
            file_path = os.path.join(save_dir, f"{vid_id}.{ext}")

            # success
            if option == "Audio (MP3)":
                st.success(f"✅ '{title}' downloaded as MP3!")
                st.audio(file_path)
                st.download_button(
                    label="🎧 Download MP3",
                    data=open(file_path, "rb").read(),
                    file_name=f"{title}.mp3",  # pretty name for client
                    mime="audio/mpeg"
                )
            else:
                st.success(f"✅ '{title}' downloaded as MP4!")
                st.video(file_path)
                st.download_button(
                    label="🎥 Download MP4",
                    data=open(file_path, "rb").read(),
                    file_name=f"{title}.mp4",  # pretty name for client
                    mime="video/mp4"
                )

        except Exception as e:
            st.error(f"❌ Error: {e}")
