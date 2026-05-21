from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, os

W, H = 1080, 1920
FONTS = 'C:/Users/nasci/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/ffaf7eb1-e899-4b15-8564-46cec1055316/c0cd45e2-3d2e-40a4-a7fe-06fecc44a961/skills/canvas-design/canvas-fonts'
PHOTO = 'C:/Users/nasci/Documents/Kaempf Business/Jobs 2026/Ok - Delicias com Amor/fotos/WhatsApp_Image_2026-05-05_at_16.52.18.jpeg'
OUT_DIR = 'C:/Users/nasci/Documents/Kaempf Business/Jobs 2026/Ok - Delicias com Amor'

F = lambda name, sz: ImageFont.truetype(f'{FONTS}/{name}', sz)

# ─── PALETTE ────────────────────────────────────────────────────────────────
BG_LILA   = (230, 222, 245)
BG_MED    = (196, 181, 224)
BG_CREAM  = (255, 248, 234)
GOLD      = (195, 152,  58)
LGOLD     = (220, 185,  95)
MGOLD     = (240, 210, 130)
WHITE     = (255, 255, 255)
PETAL_1   = (240, 208, 220)
PETAL_2   = (208, 182, 228)
PETAL_3   = (255, 232, 192)
STEM      = (148, 172, 124)
DARK_TXT  = ( 58,  40,  18)
MID_TXT   = ( 98,  70,  36)
ROSA      = (240, 208, 220)

# ─── FLOWER / LEAF HELPERS (identical to create_post.py) ────────────────────
def draw_petal(img, cx, cy, size, angle_deg, color_rgb, alpha=190):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
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
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    r = size * 0.20
    ImageDraw.Draw(layer).ellipse([cx-r, cy-r, cx+r, cy+r], fill=center_col + (230,))
    img.alpha_composite(layer)

def draw_leaf(img, cx, cy, size, angle_deg):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
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

def draw_heart(img, cx, cy, size, color, alpha=200):
    """Draw a simple heart shape using bezier approximation."""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pts = []
    for i in range(360):
        t = math.radians(i)
        # Heart parametric equation
        x = size * (16 * math.sin(t)**3)
        y = -size * (13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t))
        pts.append((cx + x/17, cy + y/17))
    d.polygon(pts, fill=color + (alpha,))
    img.alpha_composite(layer)

# ─── BACKGROUND GRADIENT (lavanda → cream, vertical) ────────────────────────
def make_gradient_bg(top_col=BG_LILA, bot_col=BG_CREAM):
    bg = Image.new('RGB', (W, H))
    for y in range(H):
        t = y / H
        r = int(top_col[0] + (bot_col[0] - top_col[0]) * t)
        g = int(top_col[1] + (bot_col[1] - top_col[1]) * t)
        b = int(top_col[2] + (bot_col[2] - top_col[2]) * t)
        ImageDraw.Draw(bg).line([(0, y), (W, y)], fill=(r, g, b))
    return bg.convert('RGBA')

def gold_border(canvas):
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([18, 18, W-18, H-18], radius=28, outline=GOLD + (148,), width=2)

def corner_flowers(canvas, scale=1.0):
    """Four-corner flower clusters matching the feed post aesthetic."""
    s = scale
    # top-left
    draw_flower(canvas, int(80*s), int(82*s), int(58*s), PETAL_1, (255,218,172), 5, 180)
    draw_flower(canvas, int(132*s), int(48*s), int(42*s), PETAL_2, MGOLD, 5, 165)
    draw_flower(canvas, int(44*s), int(148*s), int(34*s), PETAL_3, (255,200,158), 5, 148)
    draw_leaf(canvas, int(100*s), int(104*s), int(44*s), 48)
    draw_leaf(canvas, int(64*s), int(118*s), int(32*s), 122)
    draw_leaf(canvas, int(122*s), int(74*s), int(30*s), -18)
    # top-right
    draw_flower(canvas, W-int(80*s), int(82*s), int(58*s), PETAL_2, MGOLD, 5, 180)
    draw_flower(canvas, W-int(132*s), int(48*s), int(42*s), PETAL_1, (255,218,172), 5, 165)
    draw_flower(canvas, W-int(44*s), int(148*s), int(34*s), PETAL_3, (255,200,158), 5, 148)
    draw_leaf(canvas, W-int(100*s), int(104*s), int(44*s), 132)
    draw_leaf(canvas, W-int(64*s), int(118*s), int(32*s), 58)
    draw_leaf(canvas, W-int(122*s), int(74*s), int(30*s), 198)
    # bottom-left
    draw_flower(canvas, int(72*s), H-int(72*s), int(50*s), PETAL_3, MGOLD, 5, 162)
    draw_flower(canvas, int(118*s), H-int(44*s), int(34*s), PETAL_1, (255,218,172), 5, 142)
    draw_leaf(canvas, int(94*s), H-int(96*s), int(40*s), -42)
    draw_leaf(canvas, int(52*s), H-int(108*s), int(30*s), -98)
    # bottom-right
    draw_flower(canvas, W-int(72*s), H-int(72*s), int(50*s), PETAL_1, MGOLD, 5, 162)
    draw_flower(canvas, W-int(118*s), H-int(44*s), int(34*s), PETAL_2, (255,218,172), 5, 142)
    draw_leaf(canvas, W-int(94*s), H-int(96*s), int(40*s), 222)
    draw_leaf(canvas, W-int(52*s), H-int(108*s), int(30*s), 278)

def side_flowers(canvas):
    mid = H // 2
    draw_tiny(canvas, 42, mid - 80, 26, PETAL_2)
    draw_tiny(canvas, 42, mid + 80, 22, PETAL_1)
    draw_tiny(canvas, W-42, mid - 80, 26, PETAL_3)
    draw_tiny(canvas, W-42, mid + 80, 22, PETAL_2)

def centered_text(draw, text, font, y, fill, shadow=True):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    tx = (W - tw) // 2
    if shadow:
        draw.text((tx+2, y+2), text, font=font, fill=(58, 40, 18, 40))
    draw.text((tx, y), text, font=font, fill=fill)
    return tx, tw

def wrap_text(draw, text, font, max_width, fill, y_start, line_spacing=8, shadow=False):
    """Wrap text to fit max_width, return final y."""
    words = text.split()
    lines = []
    current = ''
    for word in words:
        test = (current + ' ' + word).strip()
        bb = draw.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    y = y_start
    for line in lines:
        centered_text(draw, line, font, y, fill, shadow=shadow)
        bb = draw.textbbox((0, 0), line, font=font)
        y += (bb[3] - bb[1]) + line_spacing
    return y

def gold_divider(draw, y, width=320):
    cx = W // 2
    draw.line([(cx - width//2, y), (cx - 18, y)], fill=GOLD + (100,), width=1)
    draw.line([(cx + 18, y), (cx + width//2, y)], fill=GOLD + (100,), width=1)
    draw.polygon([(cx, y-6), (cx+6, y), (cx, y+6), (cx-6, y)], fill=GOLD + (185,))

# ═══════════════════════════════════════════════════════════════════════════
# STORY 1 — D-4: Urgência de Encomendas
# ═══════════════════════════════════════════════════════════════════════════
def make_story_1():
    canvas = make_gradient_bg(BG_LILA, BG_CREAM)

    # Corner + side flowers
    corner_flowers(canvas, scale=1.0)
    side_flowers(canvas)

    # Gold border
    gold_border(canvas)

    draw = ImageDraw.Draw(canvas)

    # ── FONTS ──
    f_script  = F('NothingYouCouldDo-Regular.ttf', 68)
    f_counter = F('Gloock-Regular.ttf', 220)
    f_dias    = F('Italiana-Regular.ttf', 88)
    f_body    = F('Lora-Italic.ttf', 46)
    f_cta     = F('InstrumentSans-Regular.ttf', 38)
    f_brand   = F('InstrumentSans-Regular.ttf', 28)
    f_sub_sm  = F('Lora-Regular.ttf', 36)

    # ── Script top tag ──
    tag = 'Dia das Maes'
    centered_text(draw, tag, f_script, 220, GOLD + (210,), shadow=False)

    # ── Golden rule ──
    gold_divider(draw, 312, 400)

    # ── Big counter "4" ──
    num_font = F('Gloock-Regular.ttf', 360)
    bb = draw.textbbox((0, 0), '4', font=num_font)
    nx = (W - (bb[2]-bb[0])) // 2
    # Soft shadow for depth
    draw.text((nx+4, 356), '4', font=num_font, fill=(195, 152, 58, 40))
    draw.text((nx, 352), '4', font=num_font, fill=GOLD + (255,))

    # ── "dias" label ──
    centered_text(draw, 'dias', f_dias, 732, MID_TXT + (220,), shadow=False)

    # ── Gold divider ──
    gold_divider(draw, 848, 380)

    # ── Body copy ──
    body_y = 878
    body_y = wrap_text(draw, 'As encomendas do Dia das Maes', F('Lora-Italic.ttf', 46), 820, DARK_TXT + (235,), body_y, line_spacing=6)
    body_y = wrap_text(draw, 'estao quase todas fechadas.', F('Lora-Italic.ttf', 46), 820, DARK_TXT + (235,), body_y + 2, line_spacing=6)

    # ── Emphasis line ──
    body_y += 28
    centered_text(draw, 'Ainda tem lugar para voce', f_sub_sm, body_y, MID_TXT + (200,), shadow=False)
    body_y += 46
    centered_text(draw, 'por enquanto.', F('Lora-Italic.ttf', 40), body_y, GOLD + (230,), shadow=False)

    # ── Cream CTA panel ──
    panel_y = H - 280
    pl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(pl).rounded_rectangle(
        [70, panel_y, W-70, panel_y + 200],
        radius=20, fill=BG_CREAM + (235,))
    canvas = Image.alpha_composite(canvas, pl)
    draw = ImageDraw.Draw(canvas)

    # CTA border
    draw.rounded_rectangle([70, panel_y, W-70, panel_y+200], radius=20, outline=GOLD+(160,), width=2)

    centered_text(draw, 'Manda mensagem agora', F('Lora-Italic.ttf', 36), panel_y + 30, MID_TXT + (210,), shadow=False)
    centered_text(draw, '(55) 99928-5883', F('Gloock-Regular.ttf', 54), panel_y + 88, GOLD + (255,), shadow=True)
    centered_text(draw, 'Ok Delícias com Amor', F('InstrumentSans-Regular.ttf', 26), panel_y + 158, MID_TXT + (180,), shadow=False)

    out = f'{OUT_DIR}/story_1_urgencia.png'
    canvas.convert('RGB').save(out, quality=97, dpi=(300, 300))
    print('Saved:', out)


# ═══════════════════════════════════════════════════════════════════════════
# STORY 2 — Identidade da Marca (com foto do produto)
# ═══════════════════════════════════════════════════════════════════════════
def make_story_2():
    canvas = make_gradient_bg(BG_LILA, BG_CREAM)

    # Corner flowers only at top (photo will dominate center)
    # Top flowers
    draw_flower(canvas, 80, 82, 58, PETAL_1, (255,218,172), 5, 180)
    draw_flower(canvas, 132, 48, 42, PETAL_2, MGOLD, 5, 165)
    draw_flower(canvas, 44, 148, 34, PETAL_3, (255,200,158), 5, 148)
    draw_leaf(canvas, 100, 104, 44, 48)
    draw_leaf(canvas, 64, 118, 32, 122)
    draw_flower(canvas, W-80, 82, 58, PETAL_2, MGOLD, 5, 180)
    draw_flower(canvas, W-132, 48, 42, PETAL_1, (255,218,172), 5, 165)
    draw_flower(canvas, W-44, 148, 34, PETAL_3, (255,200,158), 5, 148)
    draw_leaf(canvas, W-100, 104, 44, 132)
    draw_leaf(canvas, W-64, 118, 32, 58)

    # Bottom corner accents (smaller — photo is star)
    draw_flower(canvas, 60, H-60, 38, PETAL_3, MGOLD, 5, 145)
    draw_flower(canvas, W-60, H-60, 38, PETAL_1, MGOLD, 5, 145)
    draw_leaf(canvas, 80, H-88, 30, -42)
    draw_leaf(canvas, W-80, H-88, 30, 222)

    gold_border(canvas)
    draw = ImageDraw.Draw(canvas)

    # ── Script tag top ──
    f_script = F('NothingYouCouldDo-Regular.ttf', 62)
    centered_text(draw, 'feito com amor, do inicio ao fim', f_script, 218, GOLD + (200,), shadow=False)
    gold_divider(draw, 306, 380)

    # ── PHOTO BLOCK ──
    photo_w = 860
    photo_h = 680
    photo_x = (W - photo_w) // 2
    photo_y = 328

    raw = Image.open(PHOTO).convert('RGB')
    rw, rh = raw.size
    # Crop to target aspect ratio
    target_ratio = photo_w / photo_h
    src_ratio = rw / rh
    if src_ratio > target_ratio:
        new_w = int(rh * target_ratio)
        raw = raw.crop(((rw - new_w)//2, 0, (rw + new_w)//2, rh))
    else:
        new_h = int(rw / target_ratio)
        raw = raw.crop((0, (rh - new_h)//2, rw, (rh + new_h)//2))
    raw = raw.resize((photo_w, photo_h), Image.LANCZOS)
    raw = ImageEnhance.Brightness(raw).enhance(1.08)
    raw = ImageEnhance.Color(raw).enhance(1.12)

    mask = Image.new('L', (photo_w, photo_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, photo_w, photo_h], radius=32, fill=255)

    photo_rgba = raw.convert('RGBA')
    photo_rgba.putalpha(mask)

    # Drop shadow
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for sp in range(14, 0, -1):
        a = int(16 * (15-sp)/14)
        ImageDraw.Draw(shadow).rounded_rectangle(
            [photo_x + sp//2 + 8, photo_y + sp//2 + 8,
             photo_x + photo_w + sp//2 + 8, photo_y + photo_h + sp//2 + 8],
            radius=36, fill=(40, 20, 8, a))
    canvas = Image.alpha_composite(canvas, shadow)
    canvas.paste(photo_rgba, (photo_x, photo_y), mask=photo_rgba.split()[3])

    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([photo_x-3, photo_y-3, photo_x+photo_w+3, photo_y+photo_h+3],
                            radius=34, outline=GOLD + (200,), width=2)

    # ── Quote area ──
    quote_top = photo_y + photo_h + 42

    # Opening quote mark in gold
    f_quote_mark = F('Italiana-Regular.ttf', 120)
    bb = draw.textbbox((0,0), '“', font=f_quote_mark)
    draw.text((W//2 - (bb[2]-bb[0])//2 - 20, quote_top - 30), '“', font=f_quote_mark, fill=GOLD + (210,))

    f_quote = F('Italiana-Regular.ttf', 62)
    centered_text(draw, 'A gente nao faz salgado em escala.', f_quote, quote_top + 50, DARK_TXT + (240,), shadow=True)

    # Closing quote mark
    bb2 = draw.textbbox((0,0), '”', font=f_quote_mark)
    draw.text((W//2 - (bb2[2]-bb2[0])//2 + 20, quote_top + 114), '”', font=f_quote_mark, fill=GOLD + (210,))

    gold_divider(draw, quote_top + 192, 360)

    f_body = F('Lora-Italic.ttf', 40)
    body_y = quote_top + 218
    wrap_text(draw, 'Cada peca passa pela mesma mao,', f_body, 820, MID_TXT + (215,), body_y, line_spacing=4)
    wrap_text(draw, 'do inicio ao fim.', f_body, 820, MID_TXT + (215,), body_y + 56, line_spacing=4)

    # Brand signature
    f_brand = F('InstrumentSans-Regular.ttf', 26)
    centered_text(draw, 'Ok Delícias com Amor  |  Santo Cristo, RS', f_brand, H - 96, GOLD + (190,), shadow=False)

    out = f'{OUT_DIR}/story_2_identidade.png'
    canvas.convert('RGB').save(out, quality=97, dpi=(300, 300))
    print('Saved:', out)


# ═══════════════════════════════════════════════════════════════════════════
# STORY 3 — D-1: Último Aviso
# ═══════════════════════════════════════════════════════════════════════════
def make_story_3():
    canvas = make_gradient_bg(BG_LILA, BG_CREAM)

    # All four corners — denser than story 1 for more emotion
    corner_flowers(canvas, scale=1.0)

    # Extra accent flowers mid-side
    draw_tiny(canvas, 40, H//2 - 120, 30, PETAL_2)
    draw_tiny(canvas, 40, H//2,       24, PETAL_1)
    draw_tiny(canvas, 40, H//2 + 120, 28, PETAL_3)
    draw_tiny(canvas, W-40, H//2 - 120, 30, PETAL_3)
    draw_tiny(canvas, W-40, H//2,       24, PETAL_2)
    draw_tiny(canvas, W-40, H//2 + 120, 28, PETAL_1)

    gold_border(canvas)
    draw = ImageDraw.Draw(canvas)

    # ── Script tag ──
    f_script = F('NothingYouCouldDo-Regular.ttf', 62)
    centered_text(draw, 'Dia das Maes, 10/05', f_script, 210, GOLD + (210,), shadow=False)
    gold_divider(draw, 302, 400)

    # ── Big headline ──
    f_head = F('Italiana-Regular.ttf', 118)
    centered_text(draw, 'Amanha e', f_head, 340, DARK_TXT + (255,), shadow=True)
    centered_text(draw, 'o dia dela.', f_head, 468, DARK_TXT + (255,), shadow=True)

    # ── Gold divider ──
    gold_divider(draw, 618, 360)

    # ── LARGE HEART (emotional centerpiece) ──
    draw_heart(canvas, W//2, 790, 22, GOLD, alpha=220)
    # Inner heart slightly lighter
    draw_heart(canvas, W//2, 790, 16, LGOLD, alpha=175)

    draw = ImageDraw.Draw(canvas)

    # ── Date badge next to heart ──
    badge_cx = W//2 + 185
    badge_cy = 790
    br = 60
    badge_layer = Image.new('RGBA', (W, H), (0,0,0,0))
    bd = ImageDraw.Draw(badge_layer)
    bd.ellipse([badge_cx-br, badge_cy-br, badge_cx+br, badge_cy+br], fill=(242, 202, 72, 245))
    bd.ellipse([badge_cx-br+4, badge_cy-br+4, badge_cx+br-4, badge_cy+br-4],
               outline=(195,152,58,180), width=2)
    canvas = Image.alpha_composite(canvas, badge_layer)
    draw = ImageDraw.Draw(canvas)

    f_badgeLg = F('Gloock-Regular.ttf', 42)
    f_badgeSm = F('Gloock-Regular.ttf', 30)
    b_top = '10'
    b_bot = '05'
    bt = draw.textbbox((0,0), b_top, font=f_badgeLg)
    draw.text((badge_cx-(bt[2]-bt[0])//2, badge_cy-46), b_top, font=f_badgeLg, fill=(50,28,4))
    draw.line([(badge_cx-26, badge_cy-2), (badge_cx+26, badge_cy-2)], fill=(120,90,20), width=1)
    bb = draw.textbbox((0,0), b_bot, font=f_badgeSm)
    draw.text((badge_cx-(bb[2]-bb[0])//2, badge_cy+6), b_bot, font=f_badgeSm, fill=(50,28,4))

    # Badge dots
    for i in range(8):
        a = math.radians(i * 45 + 22)
        dx = badge_cx + (br+9)*math.cos(a)
        dy = badge_cy + (br+9)*math.sin(a)
        draw.ellipse([dx-2, dy-2, dx+2, dy+2], fill=GOLD + (145,))

    # ── Body copy ──
    gold_divider(draw, 958, 380)

    f_body  = F('Lora-Italic.ttf', 48)
    f_body2 = F('Lora-Regular.ttf', 38)
    centered_text(draw, 'Se voce ainda nao pediu,', f_body, 988, DARK_TXT + (235,), shadow=False)
    centered_text(draw, 'essa e a ultima chance.', f_body, 1048, DARK_TXT + (235,), shadow=False)

    centered_text(draw, 'Manda mensagem agora.', f_body2, 1132, MID_TXT + (210,), shadow=False)

    # ── CTA Panel ──
    panel_y = H - 330
    pl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(pl).rounded_rectangle(
        [64, panel_y, W-64, panel_y + 240],
        radius=22, fill=BG_CREAM + (240,))
    canvas = Image.alpha_composite(canvas, pl)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([64, panel_y, W-64, panel_y+240], radius=22, outline=GOLD+(170,), width=2)

    f_cta_label = F('Lora-Italic.ttf', 36)
    f_cta_num   = F('Gloock-Regular.ttf', 62)
    f_brand     = F('InstrumentSans-Regular.ttf', 26)

    centered_text(draw, 'WhatsApp', f_cta_label, panel_y + 28, MID_TXT + (200,), shadow=False)
    centered_text(draw, '(55) 99928-5883', f_cta_num, panel_y + 84, GOLD + (255,), shadow=True)
    centered_text(draw, '@ok_deliciascomamor', f_brand, panel_y + 162, MID_TXT + (190,), shadow=False)
    centered_text(draw, 'Ok Delícias com Amor', F('InstrumentSans-Regular.ttf', 22), panel_y + 200, GOLD + (160,), shadow=False)

    out = f'{OUT_DIR}/story_3_ultimo_aviso.png'
    canvas.convert('RGB').save(out, quality=97, dpi=(300, 300))
    print('Saved:', out)


# ─── RUN ALL ─────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('Generating Story 1 — Urgencia...')
    make_story_1()

    print('Generating Story 2 — Identidade...')
    make_story_2()

    print('Generating Story 3 — Ultimo Aviso...')
    make_story_3()

    print('\nAll 3 stories saved.')
