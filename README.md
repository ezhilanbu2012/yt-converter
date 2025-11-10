# YouTube Downloader — MP3 / MP4

A simple Streamlit-based YouTube downloader that uses `yt-dlp` and `ffmpeg` to download and (for audio) convert YouTube videos to MP3 or MP4 files.

This repository contains a small UI in `main.py` (Streamlit) that accepts a YouTube URL and saves the downloaded file into the `downloads/` directory by default.

## Table of contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [How to run (development)](#how-to-run-development)
- [Web UI / API (what the app exposes)](#web-ui--api-what-the-app-exposes)
- [File layout](#file-layout)
- [Troubleshooting](#troubleshooting)
- [Development notes](#development-notes)
- [License](#license)

## Features

- Download audio as MP3 (uses `yt-dlp` + FFmpeg postprocessor).
- Download video as MP4 (merges best audio + video when needed).
- Simple Streamlit UI for input and playback.

## Prerequisites

- Python 3.8+ (3.10/3.11 recommended)
- pip
- FFmpeg (required for MP3 extraction / conversion)
- Network access to download from YouTube (or other supported sites)

On Debian/Ubuntu you can install system deps with:

```bash
sudo apt update
sudo apt install -y ffmpeg python3-venv python3-pip
```

## Installation

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install --upgrade pip
pip install streamlit yt-dlp
```

(If you prefer, pin versions in a `requirements.txt` file: `streamlit>=1.0.0` and `yt-dlp>=2023.12.01` — adjust as needed.)

## How to run (development)

Run the Streamlit app locally from the repository root:

```bash
streamlit run main.py
```

This will open a browser window (or show a local URL) with the web UI. The default Save Directory in the UI is `./downloads` which the app will create if missing.

Notes:
- For audio downloads, FFmpeg must be installed and available on PATH.
- If you get permission errors writing to the save directory, choose a directory you own or run Streamlit with a user that has access.

## Web UI / API (what the app exposes)

The app is a small UI (no separate HTTP API). The UI elements and their behavior are:

- Input fields (in `main.py`):
  - `YouTube URL` — text input for a single video URL. The app uses `yt_dlp.YoutubeDL.extract_info(url, download=True)` to fetch and download.
  - `Choose format` — radio with options `Audio (MP3)` and `Video (MP4)`.
  - `Save Directory` — text input where files will be written (default: `./downloads`). The app ensures the directory exists.
  - `⬇️ Download` — button that triggers the download.

Behavior and outputs:
- If `Audio (MP3)` is selected, `yt-dlp` is configured to download best audio and run the FFmpeg postprocessor `FFmpegExtractAudio` to create an MP3. Output template: `%(title)s.%(ext)s`, so final file is `{title}.mp3` in the `Save Directory`.
- If `Video (MP4)` is selected, `yt-dlp` attempts to download bestvideo+bestaudio and merge to MP4 (`merge_output_format: 'mp4'`). Final file is `{title}.mp4`.
- After download completes, the app uses Streamlit helpers to show a success message and provide playback:
  - `st.audio(file_path)` for MP3
  - `st.video(file_path)` for MP4
- The app also shows a `st.download_button` that returns the file contents to the browser for manual saving.

Error modes:
- Network / extraction failure: the exception from `yt-dlp` is caught and shown via `st.error`.
- Missing FFmpeg: audio conversion will fail. See [Troubleshooting](#troubleshooting).

Success criteria:
- The file appears in the `Save Directory` with the expected extension.
- The Streamlit UI shows playback and allows downloading.

Edge cases to be mindful of (implementation notes):
- Playlist URLs: `noplaylist` is set to `True` in `ydl_opts`, so playlists won't be downloaded.
- Filenames with characters not supported by the filesystem: `yt-dlp` applies some sanitization, but very unusual names may still fail.
- Duplicate titles: `%(title)s.%(ext)s` will overwrite existing files with the same title. Consider customizing `outtmpl` to include `%(id)s` or timestamps.

## File layout

- `main.py` — Streamlit app and the point of entry you run with `streamlit run main.py`.
- `vid.py` — auxiliary module (exists in the repo). If you extend or refactor, consult it for helper functions.
- `downloads/` — default place where downloaded files will be saved.
- `videos/` — (present in repo) may be used for organization or saved video files.

## Troubleshooting

- FFmpeg not found / conversion error:
  - Ensure `ffmpeg` is installed and on PATH: `ffmpeg -version`.
  - On Debian/Ubuntu: `sudo apt install ffmpeg`.
- Permission errors writing files:
  - Use a save directory you own (e.g., `~/Downloads/yt`), or run Streamlit as the appropriate user.
- Large downloads / timeouts:
  - `yt-dlp` may take time for big files; Streamlit's request/response model handles the blocking call but be patient. Consider moving to a background worker for production.
- Broken characters in filenames:
  - Modify `outtmpl` in `main.py` to add `%(id)s` or a sanitized title.
- Missing dependencies / import errors:
  - Ensure your virtual environment is activated and `streamlit` and `yt-dlp` are installed in it.

## Development notes

- To modify download behavior, edit `ydl_opts` in `main.py`.
- To avoid overwriting files, change `outtmpl` to include the video id: `'%(title)s - %(id)s.%(ext)s'`.
- Consider adding a `requirements.txt` with pinned versions for reproducibility.

Example `requirements.txt` suggestion:

```
streamlit>=1.0.0
yt-dlp>=2023.12.01
```

## Security & Legal

- Respect content owners and YouTube's terms of service. This tool is a downloader and may be used only where you have the right to download and convert content.

## License

This repository contains example code. Add a proper license (e.g., `MIT`) if you intend to publish or distribute.

---

If you'd like, I can also:

- Add a `requirements.txt` and a small `Makefile` or script to automate setup.
- Add a small `CONTRIBUTING.md` or tests for helper functions in `vid.py`.

Tell me which extras you want and I'll add them next.