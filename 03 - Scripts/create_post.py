from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, os

S = 1080
FONTS = 'C:/Users/nasci/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/ffaf7eb1-e899-4b15-8564-46cec1055316/c0cd45e2-3d2e-40a4-a7fe-06fecc44a961/skills/canvas-design/canvas-fonts'
PHOTO = 'C:/Users/nasci/Documents/Kaempf Business/Jobs 2026/Ok - Delicias com Amor/fotos/WhatsApp_Image_2026-05-05_at_16.52.18.jpeg'
OUT   = 'C:/Users/nasci/Documents/Kaempf Business/Jobs 2026/Ok - Delicias com Amor/post_canvas_final.png'

F = lambda name, sz: ImageFont.truetype(f'{FONTS}/{name}', sz)

# PALETTE
BG_LILA  = (230, 222, 245)
BG_CREAM = (255, 248, 234)
GOLD     = (195, 152, 58)
LGOLD    = (220, 185, 95)
MGOLD    = (240, 210, 130)
WHITE    = (255, 255, 255)
PETAL_1  = (240, 208, 220)
PETAL_2  = (208, 182, 228)
PETAL_3  = (255, 232, 192)
STEM     = (148, 172, 124)
DARK_TXT = (58, 40, 18)
MID_TXT  = (98, 70, 36)

# CANVAS — lavender to cream gradient
bg = Image.new('RGB', (S, S))
for y in range(S):
    t = y / S
    r = int(BG_LILA[0] + (BG_CREAM[0] - BG_LILA[0]) * t)
    g = int(BG_LILA[1] + (BG_CREAM[1] - BG_LILA[1]) * t)
    b = int(BG_LILA[2] + (BG_CREAM[2] - BG_LILA[2]) * t)
    ImageDraw.Draw(bg).line([(0, y), (S, y)], fill=(r, g, b))

canvas = bg.copy().convert('RGBA')

# FLOWERS & LEAVES helpers
def draw_petal(img, cx, cy, size, angle_deg, color_rgb, alpha=190):
    layer = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pts = []
    for i in range(20):
        a = math.radians(i * 18)
        rx = size * 0.42 * math.cos(a)
        ry = size * math.sin(a)
        ra = math.radians(angle_deg)
        x = cx + rx * math.cos(ra) - ry * math.sin(ra)
        y = cy + rx * math.sin(ra) + ry * math.cos(ra)
        pts.append((x, y))
    d.polygon(pts, fill=color_rgb + (alpha,))
    img.alpha_composite(layer)

def draw_flower(img, cx, cy, size, petal_col, center_col, n=5, alpha=185):
    for i in range(n):
        angle = i * (360 / n)
        px = cx + size * 0.58 * math.cos(math.radians(angle))
        py = cy + size * 0.58 * math.sin(math.radians(angle))
        draw_petal(img, px, py, size * 0.52, angle, petal_col, alpha)
    layer = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    r = size * 0.20
    ImageDraw.Draw(layer).ellipse([cx-r, cy-r, cx+r, cy+r], fill=center_col + (230,))
    img.alpha_composite(layer)

def draw_leaf(img, cx, cy, size, angle_deg):
    layer = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pts = []
    for i in range(16):
        a = math.radians(i * 22.5)
        rx = size * 0.30 * math.cos(a)
        ry = size * math.sin(a)
        ra = math.radians(angle_deg)
        x = cx + rx * math.cos(ra) - ry * math.sin(ra)
        y = cy + rx * math.sin(ra) + ry * math.cos(ra)
        pts.append((x, y))
    d.polygon(pts, fill=STEM + (162,))
    img.alpha_composite(layer)

def draw_tiny(img, cx, cy, sz, col):
    draw_flower(img, cx, cy, sz, col, MGOLD, 5, 155)

# --- TOP-LEFT corner ---
draw_flower(canvas, 70, 72, 50, PETAL_1, (255,218,172), 5, 180)
draw_flower(canvas, 118, 42, 36, PETAL_2, MGOLD, 5, 165)
draw_flower(canvas, 38, 128, 30, PETAL_3, (255,200,158), 5, 148)
draw_leaf(canvas, 88, 92, 38, 48)
draw_leaf(canvas, 58, 102, 28, 122)
draw_leaf(canvas, 108, 68, 26, -18)

# --- TOP-RIGHT corner ---
draw_flower(canvas, S-70, 72, 50, PETAL_2, MGOLD, 5, 180)
draw_flower(canvas, S-118, 42, 36, PETAL_1, (255,218,172), 5, 165)
draw_flower(canvas, S-38, 128, 30, PETAL_3, (255,200,158), 5, 148)
draw_leaf(canvas, S-88, 92, 38, 132)
draw_leaf(canvas, S-58, 102, 28, 58)
draw_leaf(canvas, S-108, 68, 26, 198)

# --- BOTTOM-LEFT corner ---
draw_flower(canvas, 62, S-62, 42, PETAL_3, MGOLD, 5, 162)
draw_flower(canvas, 102, S-38, 28, PETAL_1, (255,218,172), 5, 142)
draw_leaf(canvas, 82, S-82, 34, -42)
draw_leaf(canvas, 45, S-92, 26, -98)

# --- BOTTOM-RIGHT corner ---
draw_flower(canvas, S-62, S-62, 42, PETAL_1, MGOLD, 5, 162)
draw_flower(canvas, S-102, S-38, 28, PETAL_2, (255,218,172), 5, 142)
draw_leaf(canvas, S-82, S-82, 34, 222)
draw_leaf(canvas, S-45, S-92, 26, 278)

# --- side accents ---
draw_tiny(canvas, 36, S//2 - 44, 24, PETAL_2)
draw_tiny(canvas, 36, S//2 + 44, 20, PETAL_1)
draw_tiny(canvas, S-36, S//2 - 44, 24, PETAL_3)
draw_tiny(canvas, S-36, S//2 + 44, 20, PETAL_2)

# Gold border
draw_base = ImageDraw.Draw(canvas)
draw_base.rounded_rectangle([18, 18, S-18, S-18], radius=22, outline=GOLD + (148,), width=1)

# PHOTO in rounded frame
photo_size = 598
sx = (S - photo_size) // 2
sy = 54

raw = Image.open(PHOTO).convert('RGB')
w, h = raw.size
cs = min(w, h)
raw = raw.crop(((w-cs)//2, (h-cs)//2, (w+cs)//2, (h+cs)//2))
raw = raw.resize((photo_size, photo_size), Image.LANCZOS)
raw = ImageEnhance.Brightness(raw).enhance(1.10)
raw = ImageEnhance.Color(raw).enhance(1.12)

# Rounded mask
mask = Image.new('L', (photo_size, photo_size), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, photo_size, photo_size], radius=38, fill=255)

photo_rgba = raw.convert('RGBA')
photo_rgba.putalpha(mask)

# Drop shadow
shadow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
for sp in range(12, 0, -1):
    a = int(14 * (13-sp)/12)
    ImageDraw.Draw(shadow).rounded_rectangle(
        [sx + sp//2 + 6, sy + sp//2 + 6,
         sx + photo_size + sp//2 + 6, sy + photo_size + sp//2 + 6],
        radius=42, fill=(40, 20, 8, a))
canvas = Image.alpha_composite(canvas, shadow)
canvas.paste(photo_rgba, (sx, sy), mask=photo_rgba.split()[3])

draw = ImageDraw.Draw(canvas)
draw.rounded_rectangle([sx-3, sy-3, sx+photo_size+3, sy+photo_size+3],
                        radius=41, outline=GOLD + (195,), width=2)

# CREAM PANEL
panel_y = sy + photo_size + 18
panel_h = S - panel_y - 28
panel_x = 58
pl = Image.new('RGBA', (S, S), (0, 0, 0, 0))
ImageDraw.Draw(pl).rounded_rectangle(
    [panel_x, panel_y, S-panel_x, panel_y + panel_h],
    radius=16, fill=BG_CREAM + (228,))
canvas = Image.alpha_composite(canvas, pl)
draw = ImageDraw.Draw(canvas)

# TYPOGRAPHY
f_script  = F('NothingYouCouldDo-Regular.ttf', 50)
f_title   = F('Italiana-Regular.ttf', 80)
f_sub     = F('Lora-Italic.ttf', 29)
f_brand   = F('InstrumentSans-Regular.ttf', 21)
f_badgeLg = F('Gloock-Regular.ttf', 32)
f_badgeSm = F('InstrumentSans-Regular.ttf', 16)

# Script
sc = 'Delícias com Amor'
scb = draw.textbbox((0,0), sc, font=f_script)
scx = (S - (scb[2]-scb[0])) // 2
scy = panel_y + 14
draw.text((scx, scy), sc, font=f_script, fill=GOLD + (238,))

# Rule with small heart ornament
rl_y = scy + 62
draw.line([(panel_x+38, rl_y), (S//2 - 20, rl_y)], fill=GOLD + (95,), width=1)
draw.line([(S//2 + 20, rl_y), (S-panel_x-38, rl_y)], fill=GOLD + (95,), width=1)
# Diamond ornament center
draw.polygon([(S//2, rl_y-6), (S//2+6, rl_y), (S//2, rl_y+6), (S//2-6, rl_y)], fill=GOLD + (180,))

# Title
title = 'Para quem merece'
tb = draw.textbbox((0,0), title, font=f_title)
tw = tb[2]-tb[0]
tx = (S - tw) // 2
ty = rl_y + 10
draw.text((tx+1, ty+1), title, font=f_title, fill=(58,40,18,45))
draw.text((tx, ty), title, font=f_title, fill=DARK_TXT + (255,))

# Sub
sub = 'Encomendas para o Dia das Mães'
sb2 = draw.textbbox((0,0), sub, font=f_sub)
sbx = (S - (sb2[2]-sb2[0])) // 2
sby = ty + 90
draw.text((sbx, sby), sub, font=f_sub, fill=MID_TXT + (205,))

# Brand
brand = 'Ok Delícias com Amor'
brb = draw.textbbox((0,0), brand, font=f_brand)
brx = (S - (brb[2]-brb[0])) // 2
bry = sby + 42
draw.text((brx, bry), brand, font=f_brand, fill=GOLD + (192,))

# DATE BADGE — corner of photo
bcx = sx + photo_size - 4
bcy = sy + 4
br2 = 44
bl = Image.new('RGBA', (S, S), (0,0,0,0))
bd = ImageDraw.Draw(bl)
bd.ellipse([bcx-br2, bcy-br2, bcx+br2, bcy+br2], fill=(242, 202, 72, 242))
bd.ellipse([bcx-br2+3, bcy-br2+3, bcx+br2-3, bcy+br2-3], outline=(195,152,58,175), width=1)
canvas = Image.alpha_composite(canvas, bl)
draw = ImageDraw.Draw(canvas)

# Badge text
b_top = '10'
b_bot = '05'
bt = draw.textbbox((0,0), b_top, font=f_badgeLg)
draw.text((bcx-(bt[2]-bt[0])//2, bcy-32), b_top, font=f_badgeLg, fill=(50,28,4))
draw.line([(bcx-20, bcy-2), (bcx+20, bcy-2)], fill=(120,90,20), width=1)
bb = draw.textbbox((0,0), b_bot, font=f_badgeLg)
draw.text((bcx-(bb[2]-bb[0])//2, bcy+4), b_bot, font=f_badgeLg, fill=(50,28,4))

# Badge dots
for i in range(8):
    a = math.radians(i * 45 + 22)
    dx = bcx + (br2+7)*math.cos(a)
    dy = bcy + (br2+7)*math.sin(a)
    draw.ellipse([dx-1.5, dy-1.5, dx+1.5, dy+1.5], fill=GOLD + (145,))

# Final save
canvas.convert('RGB').save(OUT, quality=97, dpi=(300, 300))
print('Saved:', OUT)
