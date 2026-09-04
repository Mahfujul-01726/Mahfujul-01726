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
input_video = "my animation video.mp4"
output_gif = "./images/carousel.gif"

print(f"Converting '{input_video}' to '{output_gif}' with maximum quality...")

# FFmpeg filter:
# - fps=16 (super smooth motion, perfect timing)
# - scale=960:-1:flags=lanczos (crisp widescreen resolution)
# - palettegen: generates custom 256-color palette optimized for the video
# - paletteuse: applies bayer dither for smooth gradients without banding
filter_complex = (
    "fps=16,scale=960:-1:flags=lanczos,split[s0][s1];"
    "[s0]palettegen=max_colors=256:stats_mode=diff[p];"
    "[s1][p]paletteuse=dither=bayer:bayer_scale=4"
)

cmd = [
    ffmpeg_exe,
    "-y",
    "-i", input_video,
    "-vf", filter_complex,
    output_gif
]

result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if result.returncode == 0:
    size_mb = os.path.getsize(output_gif) / (1024 * 1024)
    print(f"SUCCESS! Output saved to: {output_gif}")
    print(f"Size: {size_mb:.2f} MB")
else:
    print("Error converting video:")
    print(result.stderr)
