#!/usr/bin/env python3
"""
Generate a smooth animated GIF banner morphing between 4 professional roles:
1. AI Researcher
2. Tech Teacher & Mentor
3. Software Engineer
4. LLM & AI Specialist
"""

import os
import sys

# Ensure UTF-8 output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont

TARGET_WIDTH = 960
TARGET_HEIGHT = 540

roles = [
    {
        "path": "./images/role_researcher.jpg",
        "tag": "ROLE: RESEARCHER",
        "title": "AI & DATA RESEARCHER",
        "subtitle": "Analyzing deep learning models, mathematical logic & data science",
        "badge_color": (16, 185, 129), # Emerald green
    },
    {
        "path": "./images/role_teacher.jpg",
        "tag": "ROLE: TEACHER",
        "title": "TECH EDUCATOR & MENTOR",
        "subtitle": "Inspiring developers, teaching AI architectures & guiding learners",
        "badge_color": (59, 130, 246), # Electric blue
    },
    {
        "path": "./images/role_software_engineer.jpg",
        "tag": "ROLE: SOFTWARE ENGINEER",
        "title": "FULL STACK & SOFTWARE ENGINEER",
        "subtitle": "Building robust backend systems, modern interfaces & scalable software",
        "badge_color": (168, 85, 247), # Purple
    },
    {
        "path": "./images/role_llm_ai.jpg",
        "tag": "ROLE: AI SPECIALIST",
        "title": "LLM & GENERATIVE AI SPECIALIST",
        "subtitle": "Designing neural network workflows, LLM agents & intelligent systems",
        "badge_color": (6, 182, 212), # Cyan
    }
]

def add_hud_badge(image, tag, title, subtitle, badge_color):
    """Adds a modern, sleek glassmorphic HUD badge at the bottom-left of the frame"""
    img = image.copy()
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Dimensions for badge
    box_x1 = 28
    box_y1 = TARGET_HEIGHT - 95
    box_x2 = 660
    box_y2 = TARGET_HEIGHT - 22
    radius = 12
    
    # Glassmorphism dark background with border
    draw.rounded_rectangle(
        [box_x1, box_y1, box_x2, box_y2],
        radius=radius,
        fill=(10, 14, 23, 215),
        outline=badge_color + (160,),
        width=2
    )
    
    # Left vertical accent bar
    draw.rounded_rectangle(
        [box_x1 + 6, box_y1 + 10, box_x1 + 12, box_y2 - 10],
        radius=3,
        fill=badge_color + (255,)
    )
    
    # Try loading Windows system fonts
    font_paths = [
        "C:\\Windows\\Fonts\\segoeuib.ttf",
        "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf",
        "C:\\Windows\\Fonts\\arial.ttf"
    ]
    tag_font = None
    title_font = None
    sub_font = None
    
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                tag_font = ImageFont.truetype(fp, 12)
                title_font = ImageFont.truetype(fp, 20)
                sub_font = ImageFont.truetype(fp, 13)
                break
            except Exception:
                continue
                
    if not title_font:
        tag_font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    # Draw tag pill
    tag_x = box_x1 + 24
    tag_y = box_y1 + 9
    tag_bbox = draw.textbbox((tag_x, tag_y), tag, font=tag_font)
    draw.rounded_rectangle(
        [tag_bbox[0] - 5, tag_bbox[1] - 2, tag_bbox[2] + 5, tag_bbox[3] + 2],
        radius=4,
        fill=badge_color + (80,),
        outline=badge_color + (180,)
    )
    draw.text((tag_x, tag_y), tag, font=tag_font, fill=badge_color + (255,))
    
    # Draw title
    draw.text((box_x1 + 24, box_y1 + 28), title, font=title_font, fill=(255, 255, 255, 255))
    
    # Draw subtitle
    draw.text((box_x1 + 24, box_y1 + 53), subtitle, font=sub_font, fill=(185, 200, 220, 230))
    
    # Composite overlay onto base image
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return img

def create_animation():
    print("[1/4] Preparing role banner images...")
    processed_base_images = []
    
    for r in roles:
        if not os.path.exists(r["path"]):
            raise FileNotFoundError(f"Image not found: {r['path']}")
            
        base_img = Image.open(r["path"]).convert("RGB")
        base_img = base_img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
        
        # Add sleek HUD badge
        badged_img = add_hud_badge(base_img, r["tag"], r["title"], r["subtitle"], r["badge_color"])
        processed_base_images.append(badged_img)
        print(f" -> Processed: {r['title']}")

    frames = []
    durations = []
    
    num_scenes = len(processed_base_images)
    hold_frames_count = 6      # Hold frames
    hold_duration_ms = 400     # 6 * 400ms = 2.4s hold per scene
    transition_steps = 6       # Crossfade frames
    transition_duration_ms = 80# 6 * 80ms = 480ms transition

    print("[2/4] Generating animation frames with smooth crossfades...")
    for i in range(num_scenes):
        current_img = processed_base_images[i]
        next_img = processed_base_images[(i + 1) % num_scenes]
        
        # 1. Add hold frames
        for _ in range(hold_frames_count):
            frames.append(current_img)
            durations.append(hold_duration_ms)
            
        # 2. Add transition (crossfade/dissolve) frames
        for step in range(1, transition_steps):
            alpha = step / float(transition_steps)
            blended = Image.blend(current_img, next_img, alpha)
            frames.append(blended)
            durations.append(transition_duration_ms)

    print(f" -> Total frames: {len(frames)}")
    print(f" -> Cycle duration: {sum(durations) / 1000.0:.2f} seconds")

    output_path = "./images/carousel.gif"
    print(f"[3/4] Quantizing frames for high visual quality...")
    
    # Generate an optimal global palette to prevent color flickering between frames
    # Sample multiple frames across all scenes
    sample_width, sample_height = TARGET_WIDTH // 2, TARGET_HEIGHT // 2
    contact_sheet = Image.new("RGB", (sample_width * 2, sample_height * 2))
    contact_sheet.paste(processed_base_images[0].resize((sample_width, sample_height)), (0, 0))
    contact_sheet.paste(processed_base_images[1].resize((sample_width, sample_height)), (sample_width, 0))
    contact_sheet.paste(processed_base_images[2].resize((sample_width, sample_height)), (0, sample_height))
    contact_sheet.paste(processed_base_images[3].resize((sample_width, sample_height)), (sample_width, sample_height))
    
    global_palette_img = contact_sheet.quantize(colors=256, method=Image.Quantize.MAXCOVERAGE)
    
    quantized_frames = []
    for f in frames:
        q = f.quantize(palette=global_palette_img, dither=Image.Dither.FLOYDSTEINBERG)
        quantized_frames.append(q)

    print(f"[4/4] Writing animated GIF to {output_path}...")
    quantized_frames[0].save(
        output_path,
        save_all=True,
        append_images=quantized_frames[1:],
        duration=durations,
        loop=0,
        optimize=True
    )
    
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"SUCCESS! Banner animation created: {output_path} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    create_animation()
