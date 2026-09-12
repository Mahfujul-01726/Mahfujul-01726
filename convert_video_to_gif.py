#!/usr/bin/env python3
"""
Convert 'my animation video.mp4' into a pristine, high-fidelity animated GIF for GitHub README banner
Uses FFmpeg palettegen + paletteuse for maximum quality & color accuracy.
"""

import subprocess
import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
input_video = "my animation video_gwr_video_mvp.mp4"
output_gif = "./images/carousel.gif"
output_webp = "./images/carousel.webp"

print(f"Processing '{input_video}'...")

# 1. Generate Animated WebP (1280x720 HD, 16 fps, high fidelity)
print(f"[1/2] Generating HD Animated WebP '{output_webp}'...")
cmd_webp = [
    ffmpeg_exe,
    "-y",
    "-i", input_video,
    "-vcodec", "libwebp",
    "-filter:v", "fps=16,scale=1280:-1:flags=lanczos",
    "-lossless", "0",
    "-q:v", "75",
    "-loop", "0",
    output_webp
]
res_webp = subprocess.run(cmd_webp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if res_webp.returncode == 0:
    size_webp_mb = os.path.getsize(output_webp) / (1024 * 1024)
    print(f"SUCCESS! WebP saved to: {output_webp} ({size_webp_mb:.2f} MB)")
else:
    print(f"Error generating WebP:\n{res_webp.stderr}")

# 2. Generate Optimized GIF (720px, 12 fps, max 128 colors, <10MB for GitHub)
print(f"[2/2] Generating Animated GIF '{output_gif}'...")
filter_complex = (
    "fps=12,scale=720:-1:flags=lanczos,split[s0][s1];"
    "[s0]palettegen=max_colors=128:stats_mode=diff[p];"
    "[s1][p]paletteuse=dither=bayer:bayer_scale=3"
)
cmd_gif = [
    ffmpeg_exe,
    "-y",
    "-i", input_video,
    "-vf", filter_complex,
    output_gif
]
res_gif = subprocess.run(cmd_gif, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if res_gif.returncode == 0:
    size_gif_mb = os.path.getsize(output_gif) / (1024 * 1024)
    print(f"SUCCESS! GIF saved to: {output_gif} ({size_gif_mb:.2f} MB)")
else:
    print(f"Error generating GIF:\n{res_gif.stderr}")

