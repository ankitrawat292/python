# TechWith Linux – 3D Intro

`TechWithLinux_Intro_3D.mp4` – 12s, 1920x1080, 30fps, with soundtrack.

## Re-render
```bash
npm install                # three + playwright-core
python3 music.py           # -> music.wav
node render.mjs            # -> video_noaudio.mp4 (headless Chromium + ffmpeg)
ffmpeg -i video_noaudio.mp4 -i music.wav -c:v copy -c:a aac -shortest TechWithLinux_Intro_3D.mp4
```
Preview stills: `node render.mjs 2,5,11`. Edit text/colors/timing in `index.html` (`renderFrame`).
