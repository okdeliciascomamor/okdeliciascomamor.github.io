# -*- coding: utf-8 -*-
"""
4 Stories Sexta — Ok Delícias com Amor — 29/05/2026

Conceito A: "Sextou" — conversão de fim de semana + escassez de junho.
Story 1: HOOK — "sextou." (dourado/âmbar, golden hour, sol estilizado)
Story 2: OCASIÕES — "tem sempre aquela hora" (lavanda, lista editorial)
Story 3: SOLUÇÃO — "tá resolvido." (sálvia/verde fresco, empanados emoldurados)
Story 4: CTA — "garante o teu pedido" (terracota rosado, agenda de junho)

Cada story com paleta cromática própria (amarelo, roxo, verde, coral),
coesas pela mesma moldura, flores de canto, rodapé e indicador de progresso.
Sem travessão. Sem a palavra "caixa". Foto nova (16.52.16, empanados, nunca usada).
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter
import math, os

BASE_DIR  = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR = (r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions"
             r"\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316"
             r"\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts")

CREME      = (255, 248, 234)
CREME_F    = (252, 240, 218)
PESSEGO    = (255, 232, 192)
PESSEGO_Q  = (250, 215, 170)
AMBAR      = (248, 198, 142)  # pêssego/âmbar quente (golden hour)
BEGE       = (242, 220, 188)
BEGE_E     = (220, 192, 150)
SAGE       = (224, 232, 215)
LAVANDA    = (232, 222, 244)
LAVANDA_E  = (210, 196, 230)
OURO       = (179, 138,  52)
OURO_S     = (210, 175, 100)
OURO_P     = (235, 210, 155)
TERRA      = (138,  82,  48)
PAPRIKA    = (188,  72,  44)
LILAS_E    = (118,  92, 158)  # accent lavanda escuro (story 2)
# Card 3 — sálvia/verde fresco
VERDE_BG1  = (236, 242, 230)
VERDE_BG2  = (198, 218, 192)
MUSGO      = ( 92, 120,  72)  # accent verde escuro
VERDE_S    = (140, 168, 110)  # verde claro p/ script
VERDE_BORD = (170, 195, 150)
# Card 4 — terracota rosado
ROSA_BG1   = (252, 230, 220)
ROSA_BG2   = (245, 200, 186)
TERRACOTA  = (170,  90,  60)  # botão CTA
TERRA_S    = (200, 120,  90)  # terracota claro p/ script
ROSA_BORD  = (225, 180, 165)
TXT        = ( 38,  22,   8)
TXT_M      = ( 72,  50,  28)
BRANCO     = (255, 255, 255)

W, H = 1080, 1920


def load_font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONTS_DIR, name), size)
    except Exception:
        return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def bg_grad(top, bot):
    img = Image.new("RGB", (W, H), top)
    d   = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W - 1, y)], fill=lerp(top, bot, y / (H - 1)))
    return img


def border(draw, col=None):
    if col is None: col = OURO_S
    draw.rounded_rectangle([16, 16, W - 16, H - 16], radius=32, outline=col, width=2)
    draw.rounded_rectangle([26, 26, W - 26, H - 26], radius=24,
                            outline=(col[0]//2, col[1]//2, col[2]//2), width=1)


def draw_petal(draw, cx, cy, angle_deg, length, width, color):
    a  = math.radians(angle_deg)
    px = cx + length * math.cos(a)
    py = cy + length * math.sin(a)
    p  = math.radians(angle_deg + 90)
    ox = (width / 2) * math.cos(p)
    oy = (width / 2) * math.sin(p)
    draw.polygon(
        [(cx + ox, cy + oy), (px + ox * .3, py + oy * .3),
         (px, py), (px - ox * .3, py - oy * .3), (cx - ox, cy - oy)],
        fill=color
    )


def draw_flower(draw, cx, cy, petals=6, plen=12, pw=6, col_out=None, col_mid=None, cr=4):
    if col_out is None: col_out = OURO_P
    if col_mid is None: col_mid = CREME
    for i in range(petals):
        draw_petal(draw, cx, cy, 360 / petals * i, plen, pw, col_out)
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=col_mid)


def draw_leaf(draw, cx, cy, angle_deg, length=12, width=5, col_a=None, col_b=None):
    if col_a is None: col_a = (170, 195, 145)
    if col_b is None: col_b = (120, 150, 100)
    draw_petal(draw, cx, cy, angle_deg,       length,      width,      col_a)
    draw_petal(draw, cx, cy, angle_deg + 180, length * .4, width * .5, col_b)


def diamond(draw, cx, cy, size, color):
    draw.polygon(
        [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)],
        fill=color
    )


def four_pt_star(draw, cx, cy, size, color):
    draw.polygon(
        [(cx, cy - size), (cx + size * 0.35, cy - size * 0.35),
         (cx + size, cy), (cx + size * 0.35, cy + size * 0.35),
         (cx, cy + size), (cx - size * 0.35, cy + size * 0.35),
         (cx - size, cy), (cx - size * 0.35, cy - size * 0.35)],
        fill=color
    )


def sun_rays(draw, cx, cy, r_in, r_out, n, color, width=3):
    """Sol estilizado — golden hour da sexta. Discreto e elegante."""
    for i in range(n):
        a = math.radians(360 / n * i)
        x1 = cx + r_in * math.cos(a)
        y1 = cy + r_in * math.sin(a)
        x2 = cx + r_out * math.cos(a)
        y2 = cy + r_out * math.sin(a)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    draw.ellipse([cx - r_in + 4, cy - r_in + 4, cx + r_in - 4, cy + r_in - 4],
                 outline=color, width=3)


def arrow_right(draw, x, y, length, color, width=2, head=8):
    draw.line([(x, y), (x + length - head, y)], fill=color, width=width)
    draw.polygon([(x + length - head, y - head // 1.5),
                  (x + length - head, y + head // 1.5),
                  (x + length, y)], fill=color)


def crop_cover(path, tw, th, focus_x=0.5, focus_y=0.5):
    """Cover-crop pra preencher tw x th sem distorcer. focus_* desloca o recorte
    (0 = topo/esquerda, 0.5 = centro, 1 = base/direita)."""
    img = Image.open(path).convert("RGB")
    ratio = max(tw / img.width, th / img.height)
    nw, nh = int(img.width * ratio) + 1, int(img.height * ratio) + 1
    img = img.resize((nw, nh), Image.LANCZOS)
    left = int(max(0, min(nw - tw, (nw - tw) * focus_x)))
    top  = int(max(0, min(nh - th, (nh - th) * focus_y)))
    return img.crop((left, top, left + tw, top + th))


def wrap_centered(draw, text, font, max_w, cx, y, fill,
                  line_spacing=12, shadow=False, shd_col=(0, 0, 0)):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        bb   = draw.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    for line in lines:
        bb = draw.textbbox((0, 0), line, font=font)
        lw = bb[2] - bb[0]
        x  = cx - lw // 2
        if shadow:
            draw.text((x + 3, y + 3), line, font=font, fill=shd_col)
        draw.text((x, y), line, font=font, fill=fill)
        y += (bb[3] - bb[1]) + line_spacing
    return y


def script_outlined_wrap(draw, text, font, max_w, cx, y,
                          fill=OURO_P, ol_col=(180, 130, 40), ol=2, line_sp=8):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        bb   = draw.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    for line in lines:
        bb = draw.textbbox((0, 0), line, font=font)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        x  = cx - tw // 2
        for dx in [-ol, 0, ol]:
            for dy in [-ol, 0, ol]:
                if dx or dy:
                    draw.text((x + dx, y + dy), line, font=font, fill=ol_col)
        draw.text((x, y), line, font=font, fill=fill)
        y += th + line_sp
    return y


def topo_flores(draw, col_a=None, col_b=None):
    if col_a is None: col_a = (220, 185, 120)
    if col_b is None: col_b = (205, 168, 100)
    for fx, col_o in [(66, col_a), (W - 66, col_b)]:
        draw_flower(draw, fx, 96, petals=6, plen=14, pw=7,
                    col_out=col_o, col_mid=OURO_P, cr=5)
        draw_leaf(draw, fx - 12, 110, 225, 13, 5)
        draw_leaf(draw, fx + 12, 110, 315, 13, 5)


def base_flores(draw, col_out=None):
    if col_out is None: col_out = (210, 175, 100)
    for fx in [66, W - 66]:
        draw_flower(draw, fx, H - 130, petals=6, plen=13, pw=6,
                    col_out=col_out, col_mid=OURO_P, cr=5)


def marca_rodape(draw, fill=None):
    if fill is None: fill = TXT_M
    fnt_br = load_font("InstrumentSans-Bold.ttf", 36)
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    cx = W // 2
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 68),
              "Ok Delícias com Amor", font=fnt_br, fill=fill)


def progress_indicator(draw, idx, accent=None):
    if accent is None: accent = OURO
    fnt = load_font("InstrumentSans-Bold.ttf", 36)
    prog = f"{idx:02d} / 04"
    bb = draw.textbbox((0, 0), prog, font=fnt)
    pw = bb[2] - bb[0]
    ph = bb[3] - bb[1]
    cx = W // 2
    px = cx - pw // 2
    py = H - 240
    draw.line([(cx - pw // 2 - 80, py + ph // 2),
               (cx - pw // 2 - 16, py + ph // 2)], fill=accent, width=1)
    draw.line([(cx + pw // 2 + 16, py + ph // 2),
               (cx + pw // 2 + 80, py + ph // 2)], fill=accent, width=1)
    draw.text((px, py), prog, font=fnt, fill=accent)


# ─────────────────────────────────────────────────────────────────────────────
# STORY 1 — HOOK: "sextou." — golden hour, sol estilizado, pêssego quente
# ─────────────────────────────────────────────────────────────────────────────
def story_1_hook():
    img  = bg_grad(PESSEGO, AMBAR)
    draw = ImageDraw.Draw(img)
    cx   = W // 2
    ACC  = OURO

    topo_flores(draw)

    # Sol estilizado no topo (golden hour) — com respiro
    sun_rays(draw, cx, 340, 30, 56, 16, OURO_S, width=3)

    cy = 470

    # Script lead
    cy = script_outlined_wrap(
        draw, "chegou a melhor hora.",
        load_font("NothingYouCouldDo-Regular.ttf", 78),
        W - 120, cx, cy,
        fill=OURO_S, ol_col=(180, 130, 40), ol=2, line_sp=4
    ) + 30

    # Ornamento diamante
    draw.line([(cx - 100, cy), (cx - 16, cy)], fill=ACC, width=2)
    draw.line([(cx + 16, cy), (cx + 100, cy)], fill=ACC, width=2)
    diamond(draw, cx, cy, 6, ACC)
    cy += 60

    # HERO — "sextou." gigante, uma palavra
    fnt_hero = load_font("Lora-Bold.ttf", 210)
    bb_h = draw.textbbox((0, 0), "sextou.", font=fnt_hero)
    hw   = bb_h[2] - bb_h[0]
    hh   = bb_h[3] - bb_h[1]
    # garante que cabe
    if hw > W - 90:
        fnt_hero = load_font("Lora-Bold.ttf", 180)
        bb_h = draw.textbbox((0, 0), "sextou.", font=fnt_hero)
        hw   = bb_h[2] - bb_h[0]
        hh   = bb_h[3] - bb_h[1]
    hx = cx - hw // 2
    draw.text((hx + 6, cy + 6), "sextou.", font=fnt_hero, fill=(225, 180, 120))
    draw.text((hx,     cy),     "sextou.", font=fnt_hero, fill=TXT)
    cy += hh + 120

    # Subtítulo
    cy = wrap_centered(
        draw, "e o fim de semana já pede salgado.",
        load_font("Lora-BoldItalic.ttf", 52),
        W - 140, cx, cy,
        fill=TXT_M, line_spacing=14
    ) + 30

    # Hint deslize
    fnt_hint = load_font("Lora-Italic.ttf", 38)
    hint_txt = "arrasta, que hoje tem novidade"
    bb_hn = draw.textbbox((0, 0), hint_txt, font=fnt_hint)
    hnw   = bb_hn[2] - bb_hn[0]
    hnh   = bb_hn[3] - bb_hn[1]
    hy    = H - 360
    htx   = cx - (hnw + 56) // 2
    draw.text((htx, hy), hint_txt, font=fnt_hint, fill=(140, 100, 55))
    arrow_right(draw, htx + hnw + 16, hy + hnh // 2 + 2, 42, (140, 100, 55), 2, 12)

    progress_indicator(draw, 1, ACC)
    base_flores(draw)
    marca_rodape(draw)
    border(draw, col=OURO_S)

    out = os.path.join(BASE_DIR, "02 - Criativos", "maio29", "story_maio29_1.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 2 — OCASIÕES: "tem sempre aquela hora" — lavanda, lista editorial
# ─────────────────────────────────────────────────────────────────────────────
def story_2_ocasioes():
    img  = bg_grad(CREME, LAVANDA)
    draw = ImageDraw.Draw(img)
    cx   = W // 2
    ACC  = LILAS_E

    topo_flores(draw, col_a=(200, 180, 220), col_b=(190, 168, 215))

    cy = 280

    # Script lead
    cy = script_outlined_wrap(
        draw, "no fim de semana,",
        load_font("NothingYouCouldDo-Regular.ttf", 74),
        W - 120, cx, cy,
        fill=(150, 120, 185), ol_col=(110, 85, 150), ol=2, line_sp=4
    ) + 26

    # Ornamento
    draw.line([(cx - 100, cy), (cx - 16, cy)], fill=ACC, width=2)
    draw.line([(cx + 16, cy), (cx + 100, cy)], fill=ACC, width=2)
    diamond(draw, cx, cy, 6, ACC)
    cy += 48

    # Título herói
    cy = wrap_centered(
        draw, "tem sempre aquela hora.",
        load_font("Lora-Bold.ttf", 86),
        W - 110, cx, cy,
        fill=TXT, shadow=True, shd_col=(205, 192, 226), line_spacing=12
    ) + 56

    # Lista de 3 ocasiões — cada uma centralizada, separadas por diamante
    fnt_oc = load_font("Lora-Italic.ttf", 48)
    ocasioes = [
        "a visita que chega sem avisar",
        "o café da tarde que pede companhia",
        "a fome que bate às cinco",
    ]
    for i, oc in enumerate(ocasioes):
        cy = wrap_centered(
            draw, oc, fnt_oc, W - 150, cx, cy,
            fill=TXT_M, line_spacing=10
        ) + 26
        if i < len(ocasioes) - 1:
            # separador diamante entre itens
            diamond(draw, cx, cy, 6, ACC)
            cy += 36

    cy += 30

    # Fecho italic
    cy = wrap_centered(
        draw, "e nada disso espera.",
        load_font("Lora-BoldItalic.ttf", 50),
        W - 120, cx, cy,
        fill=ACC, line_spacing=12
    ) + 30

    # Hint deslize
    fnt_hint = load_font("Lora-Italic.ttf", 38)
    hint_txt = "tem solução pra todas elas"
    bb_hn = draw.textbbox((0, 0), hint_txt, font=fnt_hint)
    hnw   = bb_hn[2] - bb_hn[0]
    hnh   = bb_hn[3] - bb_hn[1]
    hy    = H - 360
    htx   = cx - (hnw + 56) // 2
    draw.text((htx, hy), hint_txt, font=fnt_hint, fill=(120, 95, 160))
    arrow_right(draw, htx + hnw + 16, hy + hnh // 2 + 2, 42, (120, 95, 160), 2, 12)

    progress_indicator(draw, 2, ACC)
    base_flores(draw, col_out=(190, 168, 215))
    marca_rodape(draw)
    border(draw, col=LAVANDA_E)

    out = os.path.join(BASE_DIR, "02 - Criativos", "maio29", "story_maio29_2.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 3 — SOLUÇÃO: "tá resolvido." — sálvia/verde fresco, empanados emoldurados
# ─────────────────────────────────────────────────────────────────────────────
def story_3_solucao():
    img  = bg_grad(VERDE_BG1, VERDE_BG2)
    cx   = W // 2
    ACC  = MUSGO

    # Geometria da foto (banda horizontal emoldurada no topo-meio)
    pw, ph = 860, 470
    px = (W - pw) // 2
    py = 350
    rad = 28

    # Sombra suave atrás da foto
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([px, py + 14, px + pw, py + ph + 14],
                         radius=rad, fill=(90, 60, 25, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")

    # Foto cover-crop com cantos arredondados
    photo = crop_cover(os.path.join(BASE_DIR, "fotos",
                       "WhatsApp_Image_2026-05-05_at_16.52.16.jpeg"),
                       pw, ph, focus_y=0.55)
    mask = Image.new("L", (pw, ph), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, pw, ph], radius=rad, fill=255)
    img.paste(photo, (px, py), mask)

    draw = ImageDraw.Draw(img)

    # Molduras (dourado + linha interna escura)
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=rad,
                           outline=OURO_S, width=3)
    draw.rounded_rectangle([px + 7, py + 7, px + pw - 7, py + ph - 7], radius=rad - 6,
                           outline=(150, 110, 35), width=1)

    topo_flores(draw, col_a=(178, 202, 150), col_b=(165, 190, 135))

    # Selo "feito à mão" sobre o canto inferior da foto
    selo_txt = "feito à mão"
    fnt_selo = load_font("InstrumentSans-Bold.ttf", 32)
    bbs = draw.textbbox((0, 0), selo_txt, font=fnt_selo)
    sw = bbs[2] - bbs[0] + 52
    sh = bbs[3] - bbs[1] + 22
    sx = px + 26
    sy = py + ph - sh - 26
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=sh // 2,
                           fill=MUSGO, outline=(150, 180, 120), width=2)
    draw.text((sx + (sw - (bbs[2] - bbs[0])) // 2,
               sy + (sh - (bbs[3] - bbs[1])) // 2 - 2),
              selo_txt, font=fnt_selo, fill=BRANCO)

    cy = py + ph + 56

    # Script lead
    cy = script_outlined_wrap(
        draw, "relaxa,",
        load_font("NothingYouCouldDo-Regular.ttf", 74),
        W - 120, cx, cy,
        fill=VERDE_S, ol_col=MUSGO, ol=2, line_sp=4
    ) + 24

    # Hero
    cy = wrap_centered(
        draw, "tá resolvido.",
        load_font("Lora-Bold.ttf", 104),
        W - 90, cx, cy,
        fill=TXT, shadow=True, shd_col=(202, 218, 190), line_spacing=8
    ) + 72

    # Divisor
    draw.line([(cx - 200, cy), (cx + 200, cy)], fill=ACC, width=2)
    cy += 34

    # Suporte
    cy = wrap_centered(
        draw, "salgado artesanal, feito na hora, do jeito que o fim de semana pede.",
        load_font("Lora-Italic.ttf", 44),
        W - 150, cx, cy,
        fill=(70, 92, 54), line_spacing=12
    ) + 30

    # Hint
    fnt_hint = load_font("Lora-Italic.ttf", 38)
    hint_txt = "garante o teu antes de junho"
    bb_hn = draw.textbbox((0, 0), hint_txt, font=fnt_hint)
    hnw   = bb_hn[2] - bb_hn[0]
    hnh   = bb_hn[3] - bb_hn[1]
    hy    = H - 360
    htx   = cx - (hnw + 56) // 2
    draw.text((htx, hy), hint_txt, font=fnt_hint, fill=(88, 116, 68))
    arrow_right(draw, htx + hnw + 16, hy + hnh // 2 + 2, 42, (88, 116, 68), 2, 12)

    progress_indicator(draw, 3, ACC)
    base_flores(draw, col_out=(165, 190, 135))
    marca_rodape(draw)
    border(draw, col=VERDE_BORD)

    out = os.path.join(BASE_DIR, "02 - Criativos", "maio29", "story_maio29_3.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 4 — CTA: "garante o teu pedido" — terracota rosado, agenda de junho
# ─────────────────────────────────────────────────────────────────────────────
def story_4_cta():
    img  = bg_grad(ROSA_BG1, ROSA_BG2)
    draw = ImageDraw.Draw(img)
    cx   = W // 2
    ACC  = TERRA

    topo_flores(draw, col_a=(232, 180, 165), col_b=(225, 168, 150))

    cy = 470

    # Script
    cy = script_outlined_wrap(
        draw, "já é sexta.",
        load_font("NothingYouCouldDo-Regular.ttf", 76),
        W - 120, cx, cy,
        fill=TERRA_S, ol_col=TERRA, ol=2, line_sp=4
    ) + 28

    # Ornamento
    draw.line([(cx - 95, cy), (cx - 16, cy)], fill=ACC, width=2)
    draw.line([(cx + 16, cy), (cx + 95, cy)], fill=ACC, width=2)
    diamond(draw, cx, cy, 6, ACC)
    cy += 50

    # Hero
    cy = wrap_centered(
        draw, "garante o teu pedido.",
        load_font("Lora-Bold.ttf", 92),
        W - 90, cx, cy,
        fill=TXT, shadow=True, shd_col=(236, 200, 188), line_spacing=12
    ) + 72

    # Divisor
    draw.line([(cx - 110, cy), (cx + 110, cy)], fill=(205, 150, 120), width=1)
    cy += 34

    # Suporte escassez
    cy = wrap_centered(
        draw, "a agenda de junho enche rápido. não deixa pra última hora.",
        load_font("Lora-Italic.ttf", 44),
        W - 140, cx, cy,
        fill=(135, 80, 55), line_spacing=12
    ) + 50

    # CTA box
    cta_text = "veja o cardápio completo"
    fnt_cta = load_font("InstrumentSans-Bold.ttf", 42)
    cta_w, cta_h, r = 740, 102, 20
    cta_x = cx - cta_w // 2
    draw.rounded_rectangle([cta_x, cy, cta_x + cta_w, cy + cta_h],
                            radius=r, fill=TERRACOTA, outline=(210, 160, 135), width=2)
    bb = draw.textbbox((0, 0), cta_text, font=fnt_cta)
    draw.text((cx - (bb[2] - bb[0]) // 2,
               cy + (cta_h - (bb[3] - bb[1])) // 2 - 2),
              cta_text, font=fnt_cta, fill=BRANCO)
    arr_x = cta_x + cta_w - 44
    arr_y = cy + cta_h // 2
    draw.polygon([(arr_x, arr_y - 10), (arr_x + 18, arr_y), (arr_x, arr_y + 10)],
                 fill=(236, 200, 188))
    cy += cta_h + 14

    lbl = "link disponível no story"
    fnt_lbl = load_font("InstrumentSans-Bold.ttf", 34)
    bb_l = draw.textbbox((0, 0), lbl, font=fnt_lbl)
    draw.text((cx - (bb_l[2] - bb_l[0]) // 2, cy + 6),
              lbl, font=fnt_lbl, fill=(165, 95, 65))

    progress_indicator(draw, 4, ACC)
    base_flores(draw, col_out=(225, 168, 150))
    marca_rodape(draw)
    border(draw, col=ROSA_BORD)

    out = os.path.join(BASE_DIR, "02 - Criativos", "maio29", "story_maio29_4.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


if __name__ == "__main__":
    story_1_hook()
    story_2_ocasioes()
    story_3_solucao()
    story_4_cta()
    print("4 Stories 29/05 prontos.")
