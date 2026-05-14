#!/usr/bin/env python3
"""
Create animated GIF carousel with video frames + images
"""
import cv2
import os
from PIL import Image
import numpy as np

# Paths
video_path = "./images/mp_.mp4"
image_paths = [
    "./images/ChatGPT Image May 14, 2026, 03_57_36 PM.png",
    "./images/Gemini_Generated_Image_quag5nquag5nquag.png",
    "./images/banner.png"
]
output_path = "./images/carousel.gif"

frames = []

print("🎬 Creating carousel GIF with video + images...")

# Extract frames from video
if os.path.exists(video_path):
    print(f"\n📹 Extracting frames from video...")
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"   FPS: {fps}, Total frames: {total_frames}")
        
        # Extract every Nth frame to keep it manageable
        frame_interval = max(1, total_frames // 15)  # Get ~15 frames from video
        frame_count = 0
        extracted = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_interval == 0:
                try:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # Convert to PIL Image
                    pil_frame = Image.fromarray(frame_rgb)
                    # Resize
                    pil_frame.thumbnail((1000, 800), Image.Resampling.LANCZOS)
                    frames.append(pil_frame)
                    extracted += 1
                except Exception as e:
                    print(f"   ⚠️  Error processing frame: {e}")
            
            frame_count += 1
        
        cap.release()
        print(f"   ✓ Extracted {extracted} video frames")
        
    except Exception as e:
        print(f"   ❌ Error reading video: {e}")
else:
    print(f"   ❌ Video not found: {video_path}")

# Add images
print(f"\n🖼️  Adding images...")
for img_path in image_paths:
    if not os.path.exists(img_path):
        print(f"   ❌ Not found: {img_path}")
        continue
    
    try:
        img = Image.open(img_path)
        print(f"   ✓ Loaded: {os.path.basename(img_path)}")
        
        # Convert to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize
        img.thumbnail((1000, 800), Image.Resampling.LANCZOS)
        
        # Add image 5 times to show longer
        frames.extend([img] * 5)
        print(f"      → Added (5x)")
        
    except Exception as e:
        print(f"   ⚠️  Error: {e}")

# Create animated GIF
if frames:
    print(f"\n📝 Creating GIF...")
    print(f"   Total frames: {len(frames)}")
    print(f"   Frame size: {frames[0].size}")
    
    try:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=200,  # 200ms per frame
            loop=0  # Loop forever
        )
        
        # Get file size
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Size in MB
        
        print(f"\n✅ SUCCESS!")
        print(f"   Output: {output_path}")
        print(f"   Size: {file_size:.2f} MB")
        print(f"   Animation: Video → Image 1 → Image 2 → Image 3 (loops)")
        
    except Exception as e:
        print(f"   ❌ Error creating GIF: {e}")
else:
    print("\n❌ No frames to create GIF!")
