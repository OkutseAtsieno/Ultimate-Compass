Put your demo clips here, e.g. football_tracking.mp4 (MP4 / H.264, under ~20 MB).
Compress with:  ffmpeg -i input.mp4 -vf scale=1280:-2 -c:v libx264 -crf 28 -preset slow -an football_tracking.mp4
