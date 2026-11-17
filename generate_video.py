import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH = 720
HEIGHT = 1280
FPS = 30

# Colors
BG_DARK = (14, 5, 8)       # #0e0508
BG_WINE = (28, 10, 18)     # #1c0a12
GOLD = (212, 175, 55)      # #d4af37
GOLD_LIGHT = (246, 230, 180) # #f6e6b4
GOLD_DARK = (140, 107, 29) # #8c6b1d
TEXT_CREAM = (234, 222, 205) # #eadecd
TEXT_MUTED = (184, 166, 152) # #b8a698
WHITE = (255, 255, 255)
HEART_RED = (226, 75, 96)

# Fonts
def get_font(size, bold=False, script=False):
    try:
        if script:
            # Try French Script or Segoe Script
            for name in ['C:/Windows/Fonts/FRSCRIPT.TTF', 'C:/Windows/Fonts/segoesc.ttf', 'C:/Windows/Fonts/georgiai.ttf']:
                if os.path.exists(name):
                    return ImageFont.truetype(name, size)
        elif bold:
            for name in ['C:/Windows/Fonts/cambriab.ttf', 'C:/Windows/Fonts/georgiab.ttf']:
                if os.path.exists(name):
                    return ImageFont.truetype(name, size)
        else:
            for name in ['C:/Windows/Fonts/cambria.ttc', 'C:/Windows/Fonts/georgia.ttf']:
                if os.path.exists(name):
                    return ImageFont.truetype(name, size)
    except Exception:
        pass
    return ImageFont.load_default()

font_title = get_font(72, script=True)
font_h1 = get_font(38, bold=True)
font_h2 = get_font(28, bold=True)
font_h3 = get_font(22, bold=True)
font_sub = get_font(18, bold=False)
font_tag = get_font(14, bold=True)
font_body = get_font(18, bold=False)
font_italic = get_font(20, script=True)
font_time = get_font(16, bold=True)
font_time_title = get_font(22, bold=True)
font_time_desc = get_font(15, bold=False)
font_seal = get_font(32, bold=True)

# Helper: Draw centered text
def draw_centered_text(draw, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (WIDTH - w) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return y + (bbox[3] - bbox[1])

# Load Assets
couple_img = None
if os.path.exists('couple_transparent.webp'):
    couple_img = Image.open('couple_transparent.webp').convert('RGBA')
elif os.path.exists('couple_transparent.png'):
    couple_img = Image.open('couple_transparent.png').convert('RGBA')

venue_img = None
if os.path.exists('venue.webp'):
    venue_img = Image.open('venue.webp').convert('RGB')
elif os.path.exists('venue.jpg'):
    venue_img = Image.open('venue.jpg').convert('RGB')

# Build the Master Web Canvas
# We will create 7 screen sections, each 1200px tall
SCREEN_H = 1200
TOTAL_SCREENS = 7
CANVAS_H = SCREEN_H * TOTAL_SCREENS
print(f'Rendering master canvas ({WIDTH}x{CANVAS_H})...')

canvas = Image.new('RGB', (WIDTH, CANVAS_H), BG_DARK)
draw = ImageDraw.Draw(canvas)

# Create rich background gradients and sparkles
for y in range(0, CANVAS_H, 4):
    factor = 0.5 + 0.5 * np.sin(y / 400.0)
    r = int(14 + 18 * factor)
    g = int(5 + 6 * factor)
    b = int(8 + 12 * factor)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Add random gold ambient sparkles
np.random.seed(42)
for _ in range(350):
    sx = np.random.randint(20, WIDTH - 20)
    sy = np.random.randint(50, CANVAS_H - 50)
    sr = np.random.randint(1, 3)
    opacity = np.random.randint(120, 240)
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(GOLD_LIGHT[0], GOLD_LIGHT[1], GOLD_LIGHT[2], opacity))

# Helper: Draw Card Background
def draw_card_bg(top_y, height):
    margin = 36
    x1, y1 = margin, top_y
    x2, y2 = WIDTH - margin, top_y + height
    # Card outline
    draw.rounded_rectangle([x1, y1, x2, y2], radius=24, fill=BG_WINE, outline=GOLD, width=1)
    # Golden top border accent
    cw = (x2 - x1) * 0.6
    cx = (WIDTH - cw) // 2
    draw.line([(cx, y1), (cx + cw, y1)], fill=GOLD_LIGHT, width=2)

def draw_ornament_divider(y):
    cx = WIDTH // 2
    draw.line([(cx - 90, y), (cx - 15, y)], fill=GOLD, width=1)
    draw.line([(cx + 15, y), (cx + 90, y)], fill=GOLD, width=1)
    # Diamond
    d = 4
    draw.polygon([(cx, y - d), (cx + d, y), (cx, y + d), (cx - d, y)], fill=GOLD_LIGHT)

# ==================== SECTION 1: HERO ====================
y_base = 0
card_top = y_base + 80
draw_card_bg(card_top, 1020)

cy = card_top + 60
# Arabic Bismillah
draw_centered_text(draw, cy, "Bismillah Ar-Rahman Ar-Rahim", font_sub, GOLD_LIGHT)
cy += 45

# Badge
badge_w = 260
badge_h = 32
bx = (WIDTH - badge_w) // 2
draw.rounded_rectangle([bx, cy, bx + badge_w, cy + badge_h], radius=16, fill=(45, 18, 25), outline=GOLD, width=1)
draw_centered_text(draw, cy + 6, "*  BAAT PAKKI CEREMONY  *", font_tag, GOLD_LIGHT)
cy += 65

# Couple Names
draw_centered_text(draw, cy, "Sahil", font_title, (255, 245, 225))
cy += 95
draw_centered_text(draw, cy, "&", font_title, GOLD)
cy += 95
draw_centered_text(draw, cy, "Misba", font_title, (255, 245, 225))
cy += 110

draw_ornament_divider(cy)
cy += 35

draw_centered_text(draw, cy, "SUNDAY - 22 NOVEMBER 2026", font_h3, GOLD_LIGHT)
cy += 45
draw_centered_text(draw, cy, "Hotel Hari Priya - Bagalkote", font_body, TEXT_MUTED)

# ==================== SECTION 2: THE COUPLE ====================
y_base = SCREEN_H
card_top = y_base + 80
draw_card_bg(card_top, 1040)

cy = card_top + 45
draw_centered_text(draw, cy, "THE BEGINNING OF FOREVER", font_tag, GOLD)
cy += 30
draw_centered_text(draw, cy, "Meet The Happy Couple", font_h1, (255, 246, 230))
cy += 50

# Couple Image
if couple_img:
    cw, ch = couple_img.size
    target_h = 360
    target_w = int(cw * (target_h / ch))
    resized_couple = couple_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Arch background behind couple
    arch_w = target_w + 50
    arch_h = target_h + 30
    ax = (WIDTH - arch_w) // 2
    draw.rounded_rectangle([ax, cy, ax + arch_w, cy + arch_h], radius=70, fill=(38, 14, 22), outline=GOLD, width=1)
    
    couple_x = (WIDTH - target_w) // 2
    canvas.paste(resized_couple, (couple_x, cy + 15), resized_couple)
    
    # Floating hearts
    draw.text((couple_x + 20, cy + 40), "<3", font=font_tag, fill=HEART_RED)
    draw.text((couple_x + target_w - 30, cy + 25), "<3", font=font_tag, fill=HEART_RED)
    draw.text((WIDTH // 2 - 10, cy - 10), "<3", font=font_tag, fill=HEART_RED)
    
    cy += arch_h + 30

draw_centered_text(draw, cy, "Sahil & Misba", font_h1, GOLD_LIGHT)
cy += 50

# Quran Quote Box
qb_w = 580
qb_h = 130
qbx = (WIDTH - qb_w) // 2
draw.rounded_rectangle([qbx, cy, qbx + qb_w, cy + qb_h], radius=16, fill=(20, 8, 14), outline=GOLD_DARK, width=1)
draw_centered_text(draw, cy + 22, '"And among His signs is that He created for you mates', font_body, TEXT_CREAM)
draw_centered_text(draw, cy + 50, 'from among yourselves, that you may find tranquility in them..."', font_body, TEXT_CREAM)
draw_centered_text(draw, cy + 85, "- SURAH AR-RUM 30:21 -", font_tag, GOLD)

# ==================== SECTION 3: INVITATION ====================
y_base = SCREEN_H * 2
card_top = y_base + 80
draw_card_bg(card_top, 1040)

cy = card_top + 45
draw_centered_text(draw, cy, "WARMEST WELCOME", font_tag, GOLD)
cy += 35
draw_centered_text(draw, cy, "With the grace of Almighty Allah", font_body, TEXT_MUTED)
draw_centered_text(draw, cy + 28, "and the joyful blessings of our families,", font_body, TEXT_MUTED)
cy += 65
draw_centered_text(draw, cy, "WE CORDIALLY INVITE YOU TO THE", font_tag, GOLD_LIGHT)
cy += 30
draw_centered_text(draw, cy, "BAAT PAKKI", font_h1, GOLD_LIGHT)
cy += 45
draw_centered_text(draw, cy, "of our beloved", font_body, TEXT_MUTED)
cy += 35
draw_centered_text(draw, cy, "Sahil & Misba", font_title, (255, 245, 225))
cy += 90

draw_ornament_divider(cy)
cy += 35

# Date Spotlight
box_w = 540
box_h = 120
bx = (WIDTH - box_w) // 2
draw.rounded_rectangle([bx, cy, bx + box_w, cy + box_h], radius=18, fill=(40, 12, 22), outline=GOLD, width=1)

# Left: Sunday
draw.text((bx + 40, cy + 45), "SUNDAY", font=font_h3, fill=GOLD_LIGHT)
# Center: 22
draw.line([(bx + 200, cy + 15), (bx + 200, cy + box_h - 15)], fill=GOLD, width=1)
draw.text((bx + 235, cy + 25), "22", font=font_title, fill=WHITE)
draw.line([(bx + 340, cy + 15), (bx + 340, cy + box_h - 15)], fill=GOLD, width=1)
# Right: November
draw.text((bx + 365, cy + 45), "NOVEMBER", font=font_h3, fill=GOLD_LIGHT)

cy += box_h + 15
draw_centered_text(draw, cy, "2 0 2 6", font_h3, GOLD)
cy += 45

draw_centered_text(draw, cy, "Time: 12:00 PM to 6:00 PM", font_body, TEXT_CREAM)
cy += 32
draw_centered_text(draw, cy, "Venue: Hotel Hari Priya, Bagalkote", font_body, TEXT_CREAM)

# ==================== SECTION 4: COUNTDOWN ====================
y_base = SCREEN_H * 3
card_top = y_base + 120
draw_card_bg(card_top, 800)

cy = card_top + 60
draw_centered_text(draw, cy, "COUNTING DOWN THE MOMENTS", font_tag, GOLD)
cy += 35
draw_centered_text(draw, cy, "Until The Celebration", font_h1, (255, 246, 230))
cy += 70

# 4 Countdown Boxes
units = [("DAYS", "280"), ("HOURS", "12"), ("MINS", "45"), ("SECS", "30")]
box_size = 130
gap = 16
total_w = 4 * box_size + 3 * gap
start_x = (WIDTH - total_w) // 2

for i, (label, val) in enumerate(units):
    bx = start_x + i * (box_size + gap)
    draw.rounded_rectangle([bx, cy, bx + box_size, cy + box_size], radius=16, fill=(35, 10, 18), outline=GOLD, width=1)
    # Value
    draw.text((bx + 35, cy + 25), val, font=font_h1, fill=WHITE)
    # Label
    draw.text((bx + 40, cy + 85), label, font=font_tag, fill=GOLD)

cy += box_size + 50
draw_centered_text(draw, cy, "Sunday - 22 November 2026 - 12:00 PM IST", font_body, TEXT_MUTED)

# ==================== SECTION 5: ITINERARY ====================
y_base = SCREEN_H * 4
card_top = y_base + 80
draw_card_bg(card_top, 1040)

cy = card_top + 45
draw_centered_text(draw, cy, "PROGRAM OF THE DAY", font_tag, GOLD)
cy += 30
draw_centered_text(draw, cy, "Ceremony Itinerary", font_h1, (255, 246, 230))
cy += 60

timeline_items = [
    ("12:00 PM", "Welcome", "Ahlan Wa Sahlan - Welcoming beloved family & friends"),
    ("01:30 PM", "Royal Dastarkhwan (Lunch)", "A lavish celebratory feast in honor of the couple"),
    ("03:30 PM", "Ring Exchange Ceremony", "The auspicious Baat Pakki ring exchange and blessings"),
    ("05:30 PM", "Warm Farewell", "Concluding with heartfelt prayers, duas, and love")
]

line_x = 90
draw.line([(line_x, cy + 15), (line_x, cy + len(timeline_items) * 155 - 40)], fill=GOLD, width=2)

for time_str, title, desc in timeline_items:
    # Node
    draw.ellipse([line_x - 9, cy + 4, line_x + 9, cy + 22], fill=BG_DARK, outline=GOLD, width=2)
    draw.ellipse([line_x - 3, cy + 10, line_x + 3, cy + 16], fill=GOLD_LIGHT)
    
    # Text
    draw.text((line_x + 30, cy), time_str, font=font_time, fill=GOLD_LIGHT)
    draw.text((line_x + 30, cy + 25), title, font=font_time_title, fill=WHITE)
    draw.text((line_x + 30, cy + 60), desc, font=font_time_desc, fill=TEXT_MUTED)
    cy += 155

# ==================== SECTION 6: VENUE ====================
y_base = SCREEN_H * 5
card_top = y_base + 80
draw_card_bg(card_top, 1040)

cy = card_top + 45
draw_centered_text(draw, cy, "VENUE & DESTINATION", font_tag, GOLD)
cy += 30
draw_centered_text(draw, cy, "Hotel Hari Priya", font_h1, (255, 246, 230))
cy += 50

# Venue Photograph
if venue_img:
    vw, vh = venue_img.size
    target_vw = 580
    target_vh = int(vh * (target_vw / vw))
    resized_venue = venue_img.resize((target_vw, target_vh), Image.Resampling.LANCZOS)
    
    vx = (WIDTH - target_vw) // 2
    canvas.paste(resized_venue, (vx, cy))
    draw.rounded_rectangle([vx, cy, vx + target_vw, cy + target_vh], radius=16, outline=GOLD, width=2)
    cy += target_vh + 30

# Address Box
ab_w = 580
ab_h = 150
abx = (WIDTH - ab_w) // 2
draw.rounded_rectangle([abx, cy, abx + ab_w, cy + ab_h], radius=16, fill=(25, 8, 15), outline=GOLD_DARK, width=1)
draw_centered_text(draw, cy + 22, "HOTEL HARI PRIYA", font_h3, GOLD_LIGHT)
draw_centered_text(draw, cy + 55, "APMC Circle, Near DC Office,", font_body, TEXT_CREAM)
draw_centered_text(draw, cy + 85, "Bagalkote, Karnataka - 587103, India.", font_body, TEXT_CREAM)
draw_centered_text(draw, cy + 115, "Sunday, 22 November 2026 - 12:00 PM to 6:00 PM", font_tag, GOLD)

cy += ab_h + 35
# Button
btn_w = 420
btn_h = 56
btn_x = (WIDTH - btn_w) // 2
draw.rounded_rectangle([btn_x, cy, btn_x + btn_w, cy + btn_h], radius=28, fill=GOLD, outline=GOLD_LIGHT, width=1)
draw.text((btn_x + 95, cy + 16), "OPEN IN GOOGLE MAPS", font=font_h3, fill=(25, 8, 12))

# ==================== SECTION 7: CLOSING BLESSINGS ====================
y_base = SCREEN_H * 6
card_top = y_base + 100
draw_card_bg(card_top, 960)

cy = card_top + 60
draw_centered_text(draw, cy, "WITH SINCERE PRAYERS", font_tag, GOLD)
cy += 35
draw_centered_text(draw, cy, "Hope to See You There", font_h1, (255, 246, 230))
cy += 55

draw_centered_text(draw, cy, '"Your presence and blessings will make this joyful occasion', font_body, TEXT_CREAM)
draw_centered_text(draw, cy + 30, 'truly memorable. We eagerly look forward to welcoming you."', font_body, TEXT_CREAM)
cy += 95

# Mini Couple Vignette
if couple_img:
    cw, ch = couple_img.size
    target_h = 240
    target_w = int(cw * (target_h / ch))
    resized_mini = couple_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    cx = (WIDTH - target_w) // 2
    canvas.paste(resized_mini, (cx, cy), resized_mini)
    cy += target_h + 35

draw_centered_text(draw, cy, "WITH LOVE & BEST COMPLIMENTS", font_tag, GOLD)
cy += 35
draw_centered_text(draw, cy, "Sahil & Misba", font_title, (255, 245, 225))

print('Master canvas completed!')

# ==================== RENDER VIDEO FRAMES ====================
print('Generating video frames with wax seal opening and slow smooth scrolling...')

output_video_path = 'Sahil_Misba_Invitation_Video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, float(FPS), (WIDTH, HEIGHT))

# Scene 1: Wax Seal Envelope Opening (0 to 3.5 seconds = 105 frames)
# Closed envelope
env_img = Image.new('RGB', (WIDTH, HEIGHT), BG_DARK)
edraw = ImageDraw.Draw(env_img)

# Envelope box
eb_w = 580
eb_h = 760
eb_x = (WIDTH - eb_w) // 2
eb_y = (HEIGHT - eb_h) // 2
edraw.rounded_rectangle([eb_x, eb_y, eb_x + eb_w, eb_y + eb_h], radius=20, fill=(35, 12, 22), outline=GOLD, width=2)
# Fold creases
edraw.line([(eb_x, eb_y), (WIDTH // 2, HEIGHT // 2)], fill=GOLD_DARK, width=1)
edraw.line([(eb_x + eb_w, eb_y), (WIDTH // 2, HEIGHT // 2)], fill=GOLD_DARK, width=1)
edraw.line([(eb_x, eb_y + eb_h), (WIDTH // 2, HEIGHT // 2)], fill=GOLD_DARK, width=1)
edraw.line([(eb_x + eb_w, eb_y + eb_h), (WIDTH // 2, HEIGHT // 2)], fill=GOLD_DARK, width=1)

# Wax seal in center
seal_r = 75
seal_cx, seal_cy = WIDTH // 2, HEIGHT // 2
edraw.ellipse([seal_cx - seal_r, seal_cy - seal_r, seal_cx + seal_r, seal_cy + seal_r], fill=GOLD, outline=GOLD_LIGHT, width=2)
edraw.ellipse([seal_cx - seal_r + 15, seal_cy - seal_r + 15, seal_cx + seal_r - 15, seal_cy + seal_r - 15], outline=GOLD_DARK, width=1)
# S & M
draw_centered_text(edraw, seal_cy - 16, "S & M", font_seal, (55, 30, 8))
draw_centered_text(edraw, eb_y + eb_h + 40, "* TAP TO OPEN INVITATION *", font_tag, GOLD_LIGHT)

env_cv = cv2.cvtColor(np.array(env_img), cv2.COLOR_RGB2BGR)

# Hold closed envelope for 45 frames (1.5s)
for _ in range(45):
    out.write(env_cv)

# Seal break and burst (30 frames)
for f in range(30):
    frame = env_cv.copy()
    burst_r = int((f / 30.0) * 800)
    alpha = max(0.0, 1.0 - (f / 30.0))
    cv2.circle(frame, (seal_cx, seal_cy), burst_r, (200, 230, 255), -1)
    # Blend
    blended = cv2.addWeighted(frame, alpha, env_cv, 1.0 - alpha, 0)
    out.write(blended)

# Crossfade to Screen 1 (15 frames)
screen1_crop = canvas.crop((0, 0, WIDTH, HEIGHT))
screen1_cv = cv2.cvtColor(np.array(screen1_crop), cv2.COLOR_RGB2BGR)
for f in range(15):
    alpha = f / 15.0
    blended = cv2.addWeighted(screen1_cv, alpha, env_cv, 1.0 - alpha, 0)
    out.write(blended)

# Scene 2 to 7: Smooth Cinematic Scrolling through all screens
# For each screen: Dwell/Hold for ~3.5 seconds, then slowly scroll to next screen over ~2.0 seconds
scroll_positions = [
    0,                  # Screen 1: Hero
    SCREEN_H,          # Screen 2: Couple
    SCREEN_H * 2,      # Screen 3: Invitation
    SCREEN_H * 3,      # Screen 4: Countdown
    SCREEN_H * 4,      # Screen 5: Itinerary
    SCREEN_H * 5,      # Screen 6: Venue
    CANVAS_H - HEIGHT  # Screen 7: Closing
]

for idx, current_y in enumerate(scroll_positions):
    print(f'Rendering screen {idx + 1}/{len(scroll_positions)}...')
    
    # Render static dwell frames (90 frames = 3.0 seconds)
    crop = canvas.crop((0, current_y, WIDTH, current_y + HEIGHT))
    frame_cv = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2BGR)
    for _ in range(90):
        out.write(frame_cv)
    
    # If not the last screen, transition/scroll smoothly to the next
    if idx < len(scroll_positions) - 1:
        next_y = scroll_positions[idx + 1]
        transition_frames = 60 # 2.0 seconds of smooth scrolling
        for step in range(transition_frames):
            # Smooth ease-in-out cosine interpolation
            progress = 0.5 - 0.5 * np.cos((step / float(transition_frames)) * np.pi)
            y_pos = int(current_y + (next_y - current_y) * progress)
            y_pos = min(max(0, y_pos), CANVAS_H - HEIGHT)
            
            scrolled_crop = canvas.crop((0, y_pos, WIDTH, y_pos + HEIGHT))
            scrolled_cv = cv2.cvtColor(np.array(scrolled_crop), cv2.COLOR_RGB2BGR)
            out.write(scrolled_cv)

# Hold on closing screen for additional 60 frames (2.0s)
for _ in range(60):
    out.write(frame_cv)

# Fade out to black (30 frames)
for f in range(30):
    alpha = 1.0 - (f / 30.0)
    fade_cv = (frame_cv * alpha).astype(np.uint8)
    out.write(fade_cv)

out.release()
print(f'Video generated successfully: {output_video_path}')
print(f'File size: {os.path.getsize(output_video_path)} bytes')

