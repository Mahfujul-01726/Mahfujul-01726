#!/usr/bin/env python3
"""
Create animated GIF carousel with video frames + images
All items have same size, increased time between changes
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

# Fixed size for all frames
FIXED_WIDTH = 1200
FIXED_HEIGHT = 600

def resize_and_pad(img, target_width, target_height):
    """Resize image and pad to exact dimensions"""
    img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Create new image with white background
    final_img = Image.new('RGB', (target_width, target_height), (255, 255, 255))
    
    # Calculate position to center the image
    x = (target_width - img.width) // 2
    y = (target_height - img.height) // 2
    
    final_img.paste(img, (x, y))
    return final_img

frames = []

print("🎬 Creating carousel GIF with video + images...")
print(f"   Size: {FIXED_WIDTH}x{FIXED_HEIGHT}")
print()

# Extract frames from video
if os.path.exists(video_path):
    print(f"📹 Extracting frames from video...")
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"   FPS: {fps}, Total frames: {total_frames}")
        
        # Extract every Nth frame to keep it manageable
        frame_interval = max(1, total_frames // 12)  # Get ~12 frames from video
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
                    # Resize and pad to fixed size
                    pil_frame = resize_and_pad(pil_frame, FIXED_WIDTH, FIXED_HEIGHT)
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
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize and pad to fixed size
        img = resize_and_pad(img, FIXED_WIDTH, FIXED_HEIGHT)
        
        # Add image 8 times to show longer (increased display time)
        frames.extend([img] * 8)
        print(f"      → Added (8x for longer display)")
        
    except Exception as e:
        print(f"   ⚠️  Error: {e}")

# Create animated GIF
if frames:
    print(f"\n📝 Creating GIF...")
    print(f"   Total frames: {len(frames)}")
    print(f"   Frame size: {frames[0].size}")
    print(f"   Duration per frame: 500ms (increased wait time)")
    
    try:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=500,  # 500ms per frame (doubled from 200ms)
            loop=0  # Loop forever
        )
        
        # Get file size
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Size in MB
        
        print(f"\n✅ SUCCESS!")
        print(f"   Output: {output_path}")
        print(f"   Size: {file_size:.2f} MB")
        print(f"   All frames: {FIXED_WIDTH}x{FIXED_HEIGHT} (SAME SIZE)")
        print(f"   Animation: Video → Image 1 → Image 2 → Image 3 (loops)")
        print(f"   Total duration: ~{len(frames) * 0.5:.1f} seconds per cycle")
        
    except Exception as e:
        print(f"   ❌ Error creating GIF: {e}")
else:
    print("\n❌ No frames to create GIF!")
