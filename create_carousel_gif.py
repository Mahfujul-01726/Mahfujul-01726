#!/usr/bin/env python3
"""
Create an animated GIF carousel from images
"""
import os
from PIL import Image

# Paths
image_paths = [
    "./images/mp_.mp4",  # Video thumbnail/placeholder
    "./images/ChatGPT Image May 14, 2026, 03_57_36 PM.png",
    "./images/Gemini_Generated_Image_quag5nquag5nquag.png",
    "./images/banner.png"
]
output_path = "./images/carousel.gif"

frames = []

print("Creating carousel GIF...")

for img_path in image_paths:
    if not os.path.exists(img_path):
        print(f"❌ Not found: {img_path}")
        continue
    
    try:
        # Handle video file
        if img_path.endswith('.mp4'):
            print(f"⏭️  Skipping video: {img_path}")
            continue
        
        # Open image
        img = Image.open(img_path)
        print(f"✓ Loaded: {img_path}")
        
        # Convert RGBA to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = rgb_img
        
        # Resize to max 1000px width
        img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        
        # Add image 3 times to show it for longer
        frames.extend([img, img, img])
        print(f"  → Added to carousel (3x)")
        
    except Exception as e:
        print(f"⚠️  Error with {img_path}: {e}")
        continue

if frames:
    # Create animated GIF
    print(f"\n📝 Creating GIF with {len(frames)} frames...")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=500,  # 500ms per frame
        loop=0  # Loop forever
    )
    print(f"✅ GIF created: {output_path}")
    print(f"   Frames: {len(frames)}")
    print(f"   Size: {frames[0].size}")
else:
    print("❌ No images to create GIF")
