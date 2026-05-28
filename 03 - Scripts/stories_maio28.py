# -*- coding: utf-8 -*-
"""
7 Stories Quinta — Ok Delícias com Amor — 28/05/2026

Arc: dive nos 4 sabores do risoles (campeão da enquete de maio26)
Story 1: HOOK — choice visual
Story 2: FRANGO — editorial clássico centrado, dourado puro
Story 3: CARNE — assimétrico magazine, terra/bordô tinge
Story 4: CALABRESA — vibrante com energia, faíscas
Story 5: LEGUMES — botânico minimalista, sage green
Story 6: ENQUETE — paleta lavanda, sticker space
Story 7: CTA — urgência dourada

Cada sabor com layout, paleta accent e ornamento próprios.
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
import math, os

BASE_DIR  = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR = (r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions"
             r"\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316"
             r"\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts")

CREME      = (255, 248, 234)
CREME_F    = (252, 240, 218)  # creme mais quente (frango)
PESSEGO    = (255, 232, 192)
PESSEGO_Q  = (250, 215, 170)  # pêssego mais quente (calabresa)
BEGE       = (242, 220, 188)  # bege terroso (carne)
BEGE_E     = (220, 192, 150)
SAGE       = (224, 232, 215)  # sage claro (legumes)
SAGE_M     = (200, 215, 188)
LAVANDA    = (232, 222, 244)
OURO       = (179, 138,  52)
OURO_S     = (210, 175, 100)
OURO_P     = (235, 210, 155)
TERRA      = (138,  82,  48)  # marrom terra (carne accent)
PAPRIKA    = (188,  72,  44)  # vermelho calabresa
VERDE      = (128, 155, 105)
VERDE_E    = ( 88, 116,  75)
VERDE_S    = (140, 168, 118)  # verde sage para legumes
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


def draw_leaf(draw, cx, cy, angle_deg, length=12, width=5,
              col_a=None, col_b=None):
    if col_a is None: col_a = VERDE
    if col_b is None: col_b = VERDE_E
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


def flame(draw, cx, cy, h, color):
    """Mini chama estilizada — pra calabresa"""
    draw.polygon(
        [(cx, cy - h),
         (cx + h * 0.5, cy - h * 0.2),
         (cx + h * 0.35, cy + h * 0.3),
         (cx, cy + h * 0.5),
         (cx - h * 0.35, cy + h * 0.3),
         (cx - h * 0.5, cy - h * 0.2)],
        fill=color
    )


def botanic_leaf(draw, cx, cy, h, angle_deg, color, dark):
    """Folha botânica orientada — pra legumes"""
    a = math.radians(angle_deg)
    tip_x = cx + h * math.cos(a)
    tip_y = cy + h * math.sin(a)
    p = math.radians(angle_deg + 90)
    w = h * 0.32
    side1_x = cx + h * 0.5 * math.cos(a) + w * math.cos(p)
    side1_y = cy + h * 0.5 * math.sin(a) + w * math.sin(p)
    side2_x = cx + h * 0.5 * math.cos(a) - w * math.cos(p)
    side2_y = cy + h * 0.5 * math.sin(a) - w * math.sin(p)
    draw.polygon([(cx, cy), (side1_x, side1_y), (tip_x, tip_y),
                  (side2_x, side2_y)], fill=color)
    draw.line([(cx, cy), (tip_x, tip_y)], fill=dark, width=2)


def arrow_right(draw, x, y, length, color, width=2, head=8):
    """Seta para direita desenhada com polígono"""
    draw.line([(x, y), (x + length - head, y)], fill=color, width=width)
    draw.polygon([(x + length - head, y - head // 1.5),
                  (x + length - head, y + head // 1.5),
                  (x + length, y)], fill=color)


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


def wrap_left(draw, text, font, max_w, x_left, y, fill, line_spacing=10):
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
        draw.text((x_left, y), line, font=font, fill=fill)
        y += (bb[3] - bb[1]) + line_spacing
    return y


def script_outlined_wrap(draw, text, font, max_w, cx, y,
                          fill=OURO_P, ol_col=(10, 4, 1), ol=2, line_sp=8):
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
# STORY 1 — HOOK: "4 sabores, uma escolha"
# ─────────────────────────────────────────────────────────────────────────────
def story_1():
    img  = bg_grad(CREME, PESSEGO)
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc  = load_font("NothingYouCouldDo-Regular.ttf",  82)
    fnt_tit = load_font("Lora-Bold.ttf",                 108)
    fnt_sub = load_font("Lora-BoldItalic.ttf",            52)
    fnt_det = load_font("Lora-Italic.ttf",                42)
    fnt_tag = load_font("InstrumentSans-Bold.ttf",        32)

    topo_flores(draw)

    cy = 380

    # Script
    cy = script_outlined_wrap(
        draw, "vocês já escolheram.",
        fnt_sc, W - 120, cx, cy,
        fill=OURO_S, ol_col=(180, 130, 40), ol=2, line_sp=4
    ) + 34

    # Ornamento
    draw.line([(cx - 100, cy), (cx - 16, cy)], fill=OURO, width=2)
    draw.line([(cx + 16, cy), (cx + 100, cy)], fill=OURO, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 50

    # Título — pergunta herói
    cy = wrap_centered(
        draw, "qual sabor é o seu?",
        fnt_tit, W - 80, cx, cy,
        fill=TXT, shadow=True, shd_col=(210, 188, 148), line_spacing=14
    ) + 36

    # 4 tags dos sabores em linha horizontal
    sabores_tags = ["FRANGO", "CARNE", "CALABRESA", "LEGUMES"]
    tag_pad_x = 24
    tag_pad_y = 14
    tag_h = 56
    tag_gap = 14
    # Mede e quebra em 2 linhas (2+2)
    tag_sizes = []
    for t in sabores_tags:
        bb = draw.textbbox((0, 0), t, font=fnt_tag)
        tag_sizes.append((bb[2] - bb[0] + tag_pad_x * 2, bb[3] - bb[1] + tag_pad_y * 2))

    # Linha 1: Frango + Carne
    row1_w = tag_sizes[0][0] + tag_sizes[1][0] + tag_gap
    row1_x = cx - row1_w // 2
    rx = row1_x
    for i in [0, 1]:
        tw, th = tag_sizes[i]
        draw.rounded_rectangle([rx, cy, rx + tw, cy + th],
                                radius=24, fill=OURO_P,
                                outline=OURO, width=2)
        bb = draw.textbbox((0, 0), sabores_tags[i], font=fnt_tag)
        draw.text((rx + (tw - (bb[2] - bb[0])) // 2,
                   cy + (th - (bb[3] - bb[1])) // 2 - 2),
                  sabores_tags[i], font=fnt_tag, fill=TXT)
        rx += tw + tag_gap
    cy += tag_sizes[0][1] + 16

    # Linha 2: Calabresa + Legumes
    row2_w = tag_sizes[2][0] + tag_sizes[3][0] + tag_gap
    row2_x = cx - row2_w // 2
    rx = row2_x
    for i in [2, 3]:
        tw, th = tag_sizes[i]
        draw.rounded_rectangle([rx, cy, rx + tw, cy + th],
                                radius=24, fill=OURO_P,
                                outline=OURO, width=2)
        bb = draw.textbbox((0, 0), sabores_tags[i], font=fnt_tag)
        draw.text((rx + (tw - (bb[2] - bb[0])) // 2,
                   cy + (th - (bb[3] - bb[1])) // 2 - 2),
                  sabores_tags[i], font=fnt_tag, fill=TXT)
        rx += tw + tag_gap
    cy += tag_sizes[2][1] + 36

    # Divisor
    draw.line([(cx - 110, cy), (cx + 110, cy)], fill=(195, 168, 105), width=1)
    cy += 30

    # Sub
    cy = wrap_centered(
        draw, "4 receitas. uma decisão.",
        fnt_sub, W - 100, cx, cy,
        fill=TXT_M, line_spacing=12
    ) + 18

    # Detalhe + seta
    fnt_det_hint = load_font("Lora-Italic.ttf", 38)
    txt_hint = "arrasta pra conhecer cada uma"
    bb_h = draw.textbbox((0, 0), txt_hint, font=fnt_det_hint)
    hw   = bb_h[2] - bb_h[0]
    hh   = bb_h[3] - bb_h[1]
    htx  = cx - (hw + 50) // 2
    draw.text((htx, cy), txt_hint, font=fnt_det_hint, fill=(140, 100, 55))
    arrow_right(draw, htx + hw + 14, cy + hh // 2 + 2, 40, (140, 100, 55), width=2, head=12)

    base_flores(draw)
    marca_rodape(draw)
    border(draw, col=OURO_S)

    out = os.path.join(BASE_DIR, "02 - Criativos", "maio28", "story_maio28_1.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 2 — FRANGO: editorial clássico centralizado, dourado puro
# Layout: "01" gigante em script no fundo (watermark), nome SUPERPOSTO em cima
# ─────────────────────────────────────────────────────────────────────────────
def story_2_frango():
    img  = bg_grad(CREME, CREME_F)
    draw = ImageDraw.Draw(img)
    cx   = W // 2
    ACC  = OURO  # accent dourado clássico

    topo_flores(draw)

    # "01" GIGANTE em script no canto superior direito (corner watermark)
    fnt_corner = load_font("Lora-Bold.ttf", 320)
    corner_txt = "01"
    bb_c = draw.textbbox((0, 0), corner_txt, font=fnt_corner)
    cw   = bb_c[2] - bb_c[0]
    # cor um pouco mais visível que watermark, mas leve
    draw.text((W - cw - 100, 180), corner_txt, font=fnt_corner, fill=(228, 200, 150))

    # Linha vertical decorativa à esquerda — CURTA, só na área do header
    draw.line([(70, 240), (70, 540)], fill=ACC, width=2)
    for py_dot in [240, 390, 540]:
        diamond(draw, 70, py_dot, 7, ACC)
    # Linha vertical decorativa à direita — espelhada (simetria)
    draw.line([(W - 70, 240), (W - 70, 540)], fill=ACC, width=2)
    for py_dot in [240, 390, 540]:
        diamond(draw, W - 70, py_dot, 7, ACC)

    # Label "SABOR 01" em sans bold acima do nome (legível)
    fnt_lbl = load_font("InstrumentSans-Bold.ttf", 38)
    cy = 500
    lbl_txt = "SABOR  ·  Nº 01"
    bbl = draw.textbbox((0, 0), lbl_txt, font=fnt_lbl)
    draw.text((cx - (bbl[2] - bbl[0]) // 2, cy), lbl_txt, font=fnt_lbl, fill=ACC)
    cy += (bbl[3] - bbl[1]) + 30

    # Ornamento — diamante + 2 linhas
    draw.line([(cx - 90, cy), (cx - 14, cy)], fill=ACC, width=2)
    draw.line([(cx + 14, cy), (cx + 90, cy)], fill=ACC, width=2)
    diamond(draw, cx, cy, 7, ACC)
    cy += 60

    # NOME HERO
    fnt_nome = load_font("Lora-Bold.ttf", 200)
    bb_n = draw.textbbox((0, 0), "Frango", font=fnt_nome)
    nw   = bb_n[2] - bb_n[0]
    nh   = bb_n[3] - bb_n[1]
    nx   = cx - nw // 2
    # sombra profunda
    draw.text((nx + 6, cy + 6), "Frango", font=fnt_nome, fill=(200, 170, 110))
    draw.text((nx,     cy),     "Frango", font=fnt_nome, fill=TXT)
    cy += nh + 70  # espaço generoso pra descender do 'g' não tocar tagline

    # Tagline em italic dourado
    fnt_tag = load_font("Lora-BoldItalic.ttf", 54)
    cy = wrap_centered(
        draw, "o clássico.",
        fnt_tag, W - 100, cx, cy,
        fill=ACC, line_spacing=10
    ) + 30

    # Divisor longo dourado
    draw.line([(cx - 200, cy), (cx + 200, cy)], fill=ACC, width=2)
    cy += 36

    # Descrição
    fnt_desc = load_font("Lora-Italic.ttf", 44)
    cy = wrap_centered(
        draw, "peito desfiado e temperado na hora, cremoso no ponto certo.",
        fnt_desc, W - 160, cx, cy,
        fill=TXT_M, line_spacing=12
    ) + 38

    # Badge "o que todo mundo pede primeiro" — pillbox dourado
    badge_txt = "o que todo mundo pede primeiro"
    fnt_b = load_font("InstrumentSans-Bold.ttf", 32)
    bbb = draw.textbbox((0, 0), badge_txt, font=fnt_b)
    bw = bbb[2] - bbb[0] + 60
    bh = bbb[3] - bbb[1] + 24
    bx = cx - bw // 2
    draw.rounded_rectangle([bx, cy, bx + bw, cy + bh], radius=bh // 2,
                            fill=ACC, outline=(150, 110, 35), width=2)
    draw.text((bx + (bw - (bbb[2] - bbb[0])) // 2,
               cy + (bh - (bbb[3] - bbb[1])) // 2 - 2),
              badge_txt, font=fnt_b, fill=BRANCO)

    # Hint deslize
    fnt_hint = load_font("Lora-Italic.ttf", 36)
    hint_txt = "deslize pro próximo sabor"
    bb_h = draw.textbbox((0, 0), hint_txt, font=fnt_hint)
    hw   = bb_h[2] - bb_h[0]
    hh   = bb_h[3] - bb_h[1]
    hy   = H - 340
    htx  = cx - (hw + 60) // 2
    draw.text((htx, hy), hint_txt, font=fnt_hint, fill=(140, 100, 55))
    arrow_right(draw, htx + hw + 14, hy + hh // 2 + 2, 44, (140, 100, 55), 2, 12)

    progress_indicator(draw, 1, ACC)
    base_flores(draw)
    marca_rodape(draw)
    border(draw, col=OURO_S)

    out = os.path.join(BASE_DIR, "02 - Criativos", "maio28", "story_maio28_2.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 3 — CARNE: assimétrico magazine, terra/bordô
# Layout: número "02" lateral esquerda, nome empilhado, descrição embaixo
# ─────────────────────────────────────────────────────────────────────────────
def story_3_carne():
    img  = bg_grad(BEGE, BEGE_E)
    draw = ImageDraw.Draw(img)
    cx   = W // 2
    ACC  = TERRA  # accent terra/marrom

    topo_flores(draw, col_a=(190, 145, 90), col_b=(170, 120, 70))

    # Linha vertical decorativa à esquerda — só na área do header (não invade descrição)
    draw.line([(80, 260), (80, 720)], fill=ACC, width=2)
    for py_dot in [260, 410, 560, 720]:
        diamond(draw, 80, py_dot, 7, ACC)
    # Linha vertical à direita também (simetria)
    draw.line([(W - 80, 260), (W - 80, 720)], fill=ACC, width=2)
    for py_dot in [260, 410, 560, 720]:
        diamond(draw, W - 80, py_dot, 7, ACC)

    # Mini label "SABOR" em sans bold legível
    fnt_mini = load_font("InstrumentSans-Bold.ttf", 34)
    label_y  = 250
    draw.text((140, label_y), "SABOR", font=fnt_mini, fill=ACC)

    # Número "02" enorme em script à esquerda
    fnt_num = load_font("NothingYouCouldDo-Regular.ttf", 220)
    bb_num = draw.textbbox((0, 0), "02", font=fnt_num)
    num_x = 170
    num_y = 320
    # outline 2px pra peso
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            if dx or dy:
                draw.text((num_x + dx, num_y + dy), "02", font=fnt_num, fill=(110, 65, 35))
    draw.text((num_x, num_y), "02", font=fnt_num, fill=ACC)

    # NOME — uma linha só, gigante, alinhado à direita do número
    fnt_nome = load_font("Lora-Bold.ttf", 180)
    nome_txt = "Carne"
    bb_nm = draw.textbbox((0, 0), nome_txt, font=fnt_nome)
    nmw   = bb_nm[2] - bb_nm[0]
    nmh   = bb_nm[3] - bb_nm[1]
    # Alinha à direita do espaço disponível (depois do "02")
    nome_x_right = W - 90
    nx = nome_x_right - nmw
    nome_y = 420
    # sombra
    draw.text((nx + 5, nome_y + 5), nome_txt, font=fnt_nome, fill=(195, 160, 110))
    draw.text((nx,     nome_y),     nome_txt, font=fnt_nome, fill=TXT)

    # Tagline italic centralizado abaixo do bloco
    cy = 770
    fnt_tag = load_font("Lora-BoldItalic.ttf", 56)
    cy = wrap_centered(
        draw, '"sabor de casa."',
        fnt_tag, W - 160, cx, cy,
        fill=ACC, line_spacing=10
    ) + 30

    # Ornamento horizontal mais espesso (linha dupla)
    draw.line([(cx - 180, cy),     (cx + 180, cy)],     fill=ACC, width=2)
    draw.line([(cx - 180, cy + 6), (cx + 180, cy + 6)], fill=ACC, width=1)
    cy += 40

    # Descrição em parágrafo amplo
    fnt_desc = load_font("Lora-Italic.ttf", 44)
    cy = wrap_centered(
        draw, "carne moída temperada com a receita que vem de família.",
        fnt_desc, W - 200, cx, cy,
        fill=TXT_M, line_spacing=14
    ) + 50

    # Selo "receita da Oliete" — pillbox com estrelas polígono
    seal_txt = "receita da Oliete"
    fnt_seal = load_font("InstrumentSans-Bold.ttf", 34)
    bbs = draw.textbbox((0, 0), seal_txt, font=fnt_seal)
    stw = bbs[2] - bbs[0]
    sth = bbs[3] - bbs[1]
    # bordas com estrelas: reserva espaço pra elas
    star_gap = 30
    sw = stw + 100 + star_gap * 2  # texto + padding + estrelas
    sh = sth + 22
    sx = cx - sw // 2
    draw.rounded_rectangle([sx, cy, sx + sw, cy + sh], radius=sh // 2,
                            fill=None, outline=ACC, width=2)
    # Estrelas nos lados internos
    star_y_mid = cy + sh // 2
    four_pt_star(draw, sx + 28, star_y_mid, 9, ACC)
    four_pt_star(draw, sx + sw - 28, star_y_mid, 9, ACC)
    # Texto centralizado entre as estrelas
    draw.text((cx - stw // 2, cy + (sh - sth) // 2 - 2),
              seal_txt, font=fnt_seal, fill=ACC)

    # Hint deslize
    fnt_hint = load_font("Lora-Italic.ttf", 36)
    hint_txt = "deslize pro próximo sabor"
    bb_h = draw.textbbox((0, 0), hint_txt, font=fnt_hint)
    hw   = bb_h[2] - bb_h[0]
    hh   = bb_h[3] - bb_h[1]
    hy   = H - 340
    htx  = cx - (hw + 60) // 2
    draw.text((htx, hy), hint_txt, font=fnt_hint, fill=ACC)
    arrow_right(draw, htx + hw + 14, hy + hh // 2 + 2, 44, ACC, 2, 12)

    progress_indicator(draw, 2, ACC)
    base_flores(draw, col_out=(190, 145, 90))
    marca_rodape(draw)
    border(draw, col=(150, 110, 70))

    out = os.path.join(BASE_DIR, "02 - Criativos", "maio28", "story_maio28_3.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 4 — CALABRESA: vibrante com energia, faíscas/chamas
# Layout: badge circular gigante com "03", nome com tracking espaçado, faíscas
# ─────────────────────────────────────────────────────────────────────────────
def story_4_calabresa():
    img  = bg_grad(PESSEGO, PESSEGO_Q)
    draw = ImageDraw.Draw(img)
    cx   = W // 2
    ACC  = PAPRIKA  # accent vermelho calabresa

    topo_flores(draw, col_a=(220, 150, 100), col_b=(210, 140, 90))

    # 5 chamas decorativas espalhadas no topo
    for fx, fy, fs in [(180, 230, 22), (320, 200, 18), (cx, 220, 26),
                        (760, 200, 18), (900, 230, 22)]:
        flame(draw, fx, fy, fs, ACC)

    # Badge circular gigante com "03" dentro
    circle_cx = cx
    circle_cy = 530
    circle_r  = 160
    # Anel externo
    draw.ellipse([circle_cx - circle_r - 8, circle_cy - circle_r - 8,
                  circle_cx + circle_r + 8, circle_cy + circle_r + 8],
                 outline=ACC, width=3)
    # Anel interno
    draw.ellipse([circle_cx - circle_r, circle_cy - circle_r,
                  circle_cx + circle_r, circle_cy + circle_r],
                 fill=BRANCO, outline=ACC, width=2)
    # "03" dentro
    fnt_num = load_font("Lora-Bold.ttf", 200)
    bb_n = draw.textbbox((0, 0), "03", font=fnt_num)
    nw_n = bb_n[2] - bb_n[0]
    nh_n = bb_n[3] - bb_n[1]
    draw.text((circle_cx - nw_n // 2, circle_cy - nh_n // 2 - 12),
              "03", font=fnt_num, fill=ACC)
    # Mini "sabor" acima do número dentro do círculo
    fnt_mini = load_font("InstrumentSans-Bold.ttf", 30)
    bbm = draw.textbbox((0, 0), "SABOR", font=fnt_mini)
    draw.text((circle_cx - (bbm[2] - bbm[0]) // 2, circle_cy - circle_r // 2 - 22),
              "SABOR", font=fnt_mini, fill=ACC)

    # NOME com tracking espaçado (simulado com espaços entre letras)
    cy = 770
    fnt_nome = load_font("Lora-Bold.ttf", 150)
    # Renderiza letra por letra com tracking
    nome_str = "CALABRESA"
    tracking = 8
    # Calcula largura total
    total_w = 0
    letter_widths = []
    for ch in nome_str:
        b = draw.textbbox((0, 0), ch, font=fnt_nome)
        lw = b[2] - b[0]
        letter_widths.append(lw)
        total_w += lw
    total_w += tracking * (len(nome_str) - 1)
    # Cabe?
    if total_w > W - 80:
        # reduz fonte se não cabe
        fnt_nome = load_font("Lora-Bold.ttf", 120)
        letter_widths = []
        total_w = 0
        for ch in nome_str:
            b = draw.textbbox((0, 0), ch, font=fnt_nome)
            lw = b[2] - b[0]
            letter_widths.append(lw)
            total_w += lw
        total_w += tracking * (len(nome_str) - 1)
    x_start = cx - total_w // 2
    bb_h = draw.textbbox((0, 0), nome_str[0], font=fnt_nome)
    nome_h = bb_h[3] - bb_h[1]
    for i, ch in enumerate(nome_str):
        # sombra
        draw.text((x_start + 4, cy + 4), ch, font=fnt_nome, fill=(195, 160, 130))
        draw.text((x_start,     cy),     ch, font=fnt_nome, fill=TXT)
        x_start += letter_widths[i] + tracking
    cy += nome_h + 30

    # Tagline italic — sem chamas ao lado (eviita conflito visual com descenders)
    fnt_tag = load_font("Lora-BoldItalic.ttf", 54)
    tag_txt = "o marcante."
    bb_t = draw.textbbox((0, 0), tag_txt, font=fnt_tag)
    tw_t = bb_t[2] - bb_t[0]
    th_t = bb_t[3] - bb_t[1]
    tx = cx - tw_t // 2
    draw.text((tx, cy), tag_txt, font=fnt_tag, fill=ACC)
    cy += th_t + 50

    # Divisor com chamas no centro
    draw.line([(cx - 220, cy), (cx - 40, cy)], fill=ACC, width=2)
    draw.line([(cx + 40, cy), (cx + 220, cy)], fill=ACC, width=2)
    flame(draw, cx, cy, 16, ACC)
    cy += 40

    # Descrição
    fnt_desc = load_font("Lora-Italic.ttf", 44)
    cy = wrap_centered(
        draw, "calabresa com cebola refogada na medida, sabor que assina.",
        fnt_desc, W - 160, cx, cy,
        fill=TXT_M, line_spacing=14
    ) + 40

    # Selo "pra quem gosta de sabor forte" em pill vermelha
    badge_txt = "pra quem gosta de sabor forte"
    fnt_b = load_font("InstrumentSans-Bold.ttf", 32)
    bbb = draw.textbbox((0, 0), badge_txt, font=fnt_b)
    bw = bbb[2] - bbb[0] + 60
    bh = bbb[3] - bbb[1] + 24
    bx = cx - bw // 2
    draw.rounded_rectangle([bx, cy, bx + bw, cy + bh], radius=bh // 2,
                            fill=ACC, outline=(140, 50, 30), width=2)
    draw.text((bx + (bw - (bbb[2] - bbb[0])) // 2,
               cy + (bh - (bbb[3] - bbb[1])) // 2 - 2),
              badge_txt, font=fnt_b, fill=BRANCO)

    # Hint deslize
    fnt_hint = load_font("Lora-Italic.ttf", 36)
    hint_txt = "deslize pro próximo sabor"
    bb_h2 = draw.textbbox((0, 0), hint_txt, font=fnt_hint)
    hw   = bb_h2[2] - bb_h2[0]
    hh   = bb_h2[3] - bb_h2[1]
    hy   = H - 340
    htx  = cx - (hw + 60) // 2
    draw.text((htx, hy), hint_txt, font=fnt_hint, fill=ACC)
    arrow_right(draw, htx + hw + 14, hy + hh // 2 + 2, 44, ACC, 2, 12)

    progress_indicator(draw, 3, ACC)
    base_flores(draw, col_out=(210, 140, 90))
    marca_rodape(draw)
    border(draw, col=(160, 90, 60))

    out = os.path.join(BASE_DIR, "02 - Criativos", "maio28", "story_maio28_4.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 5 — LEGUMES: botânico minimalista, sage green
# Layout: aberto/respirado, folhas botânicas, tipografia refinada
# ─────────────────────────────────────────────────────────────────────────────
def story_5_legumes():
    img  = bg_grad(CREME, SAGE)
    draw = ImageDraw.Draw(img)
    cx   = W // 2
    ACC  = VERDE_E  # accent verde sage escuro
    ACC_L = VERDE_S

    # Flores topo com verde
    for fx in [66, W - 66]:
        draw_flower(draw, fx, 96, petals=6, plen=14, pw=7,
                    col_out=(170, 195, 145), col_mid=CREME, cr=5)
    # Folhas botânicas decorativas espalhadas no topo
    botanic_leaf(draw, 180, 240, 50, 215, ACC_L, ACC)
    botanic_leaf(draw, 230, 280, 38, 195, ACC_L, ACC)
    botanic_leaf(draw, W - 180, 240, 50, 325, ACC_L, ACC)
    botanic_leaf(draw, W - 230, 280, 38, 345, ACC_L, ACC)

    # Mini script "sabor" no topo centralizado
    fnt_sub_lbl = load_font("Lora-Italic.ttf", 44)
    lbl_txt = "sabor"
    bbl = draw.textbbox((0, 0), lbl_txt, font=fnt_sub_lbl)
    cy = 360
    draw.text((cx - (bbl[2] - bbl[0]) // 2, cy), lbl_txt, font=fnt_sub_lbl, fill=ACC)
    cy += (bbl[3] - bbl[1]) + 14

    # Número delicado em italic Lora (não bold, não script)
    fnt_num = load_font("Lora-Italic.ttf", 130)
    num_txt = "04"
    bb_n = draw.textbbox((0, 0), num_txt, font=fnt_num)
    nw = bb_n[2] - bb_n[0]
    nh = bb_n[3] - bb_n[1]
    draw.text((cx - nw // 2, cy), num_txt, font=fnt_num, fill=ACC)
    cy += nh + 36  # espaço maior pra não cortar descender

    # Linha sutil + folha pequena
    draw.line([(cx - 60, cy), (cx - 16, cy)], fill=ACC_L, width=1)
    draw.line([(cx + 16, cy), (cx + 60, cy)], fill=ACC_L, width=1)
    botanic_leaf(draw, cx, cy, 10, 90, ACC_L, ACC)
    cy += 50

    # NOME — Lora Bold mas mais leve que outros
    fnt_nome = load_font("Lora-Bold.ttf", 160)
    bb_nm = draw.textbbox((0, 0), "Legumes", font=fnt_nome)
    nmw = bb_nm[2] - bb_nm[0]
    nmh = bb_nm[3] - bb_nm[1]
    nmx = cx - nmw // 2
    # sombra verde claro
    draw.text((nmx + 4, cy + 4), "Legumes", font=fnt_nome, fill=(180, 205, 160))
    draw.text((nmx,     cy),     "Legumes", font=fnt_nome, fill=TXT)
    cy += nmh + 40

    # Tagline em italic verde
    fnt_tag = load_font("Lora-BoldItalic.ttf", 52)
    cy = wrap_centered(
        draw, "o equilibrado.",
        fnt_tag, W - 100, cx, cy,
        fill=ACC, line_spacing=10
    ) + 36

    # Divisor com 3 folhas
    botanic_leaf(draw, cx - 100, cy, 14, 180, ACC_L, ACC)
    botanic_leaf(draw, cx,        cy, 18, 270, ACC_L, ACC)
    botanic_leaf(draw, cx + 100, cy, 14, 0,   ACC_L, ACC)
    cy += 50

    # Descrição
    fnt_desc = load_font("Lora-Italic.ttf", 44)
    cy = wrap_centered(
        draw, "legumes selecionados, opção vegetariana fresca e leve.",
        fnt_desc, W - 160, cx, cy,
        fill=TXT_M, line_spacing=14
    ) + 40

    # Badge "100% vegetariano" — pill verde com folhinhas botânicas nas laterais
    badge_txt = "100% vegetariano"
    fnt_b = load_font("InstrumentSans-Bold.ttf", 32)
    bbb = draw.textbbox((0, 0), badge_txt, font=fnt_b)
    btw = bbb[2] - bbb[0]
    bth = bbb[3] - bbb[1]
    leaf_gap = 36
    bw = btw + 80 + leaf_gap * 2
    bh = bth + 24
    bx = cx - bw // 2
    draw.rounded_rectangle([bx, cy, bx + bw, cy + bh], radius=bh // 2,
                            fill=ACC, outline=(70, 100, 60), width=2)
    # Folhas nas laterais (cor clara pra contrastar com verde escuro)
    leaf_y_mid = cy + bh // 2
    botanic_leaf(draw, bx + 32, leaf_y_mid, 14, 90,  (220, 235, 200), BRANCO)
    botanic_leaf(draw, bx + bw - 32, leaf_y_mid, 14, 270, (220, 235, 200), BRANCO)
    # Texto branco centralizado
    draw.text((cx - btw // 2, cy + (bh - bth) // 2 - 2),
              badge_txt, font=fnt_b, fill=BRANCO)

    # Hint "última parada" + seta
    fnt_hint = load_font("Lora-Italic.ttf", 36)
    hint_txt = "última parada. desliza pra fechar."
    bb_h = draw.textbbox((0, 0), hint_txt, font=fnt_hint)
    hw   = bb_h[2] - bb_h[0]
    hh   = bb_h[3] - bb_h[1]
    hy   = H - 340
    htx  = cx - (hw + 60) // 2
    draw.text((htx, hy), hint_txt, font=fnt_hint, fill=ACC)
    arrow_right(draw, htx + hw + 14, hy + hh // 2 + 2, 44, ACC, 2, 12)

    progress_indicator(draw, 4, ACC)
    base_flores(draw, col_out=(170, 195, 145))
    marca_rodape(draw)
    border(draw, col=ACC_L)

    out = os.path.join(BASE_DIR, "02 - Criativos", "maio28", "story_maio28_5.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 6 — ENQUETE: paleta lavanda (mudança visual), 4 opções listadas
# ─────────────────────────────────────────────────────────────────────────────
def story_6_enquete():
    img  = bg_grad(CREME, LAVANDA)
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc   = load_font("NothingYouCouldDo-Regular.ttf",  76)
    fnt_tit  = load_font("Lora-Bold.ttf",                  92)
    fnt_op   = load_font("InstrumentSans-Bold.ttf",        38)
    fnt_inst = load_font("InstrumentSans-Bold.ttf",        40)

    topo_flores(draw)

    cy = 280

    # Script tag
    cy = script_outlined_wrap(
        draw, "agora é sua vez.",
        fnt_sc, W - 120, cx, cy,
        fill=OURO_S, ol_col=(180, 130, 40), ol=2, line_sp=4
    ) + 30

    # Ornamento
    draw.line([(cx - 100, cy), (cx - 16, cy)], fill=OURO, width=2)
    draw.line([(cx + 16, cy), (cx + 100, cy)], fill=OURO, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 50

    # Pergunta herói
    cy = wrap_centered(
        draw, "qual vai no teu próximo pedido?",
        fnt_tit, W - 100, cx, cy,
        fill=TXT, shadow=True, shd_col=(195, 178, 215), line_spacing=14
    ) + 40

    # 4 opções listadas como tags (2x2 grid)
    opts = ["FRANGO", "CARNE", "CALABRESA", "LEGUMES"]
    opt_colors = [OURO_P, BEGE_E, (240, 180, 150), VERDE_S]
    opt_borders = [OURO, TERRA, PAPRIKA, VERDE_E]
    tag_pad_x = 24
    tag_pad_y = 14
    tag_gap = 14
    tag_sizes = []
    for t in opts:
        bb = draw.textbbox((0, 0), t, font=fnt_op)
        tag_sizes.append((bb[2] - bb[0] + tag_pad_x * 2, bb[3] - bb[1] + tag_pad_y * 2))

    # Linha 1
    row1_w = tag_sizes[0][0] + tag_sizes[1][0] + tag_gap
    rx = cx - row1_w // 2
    for i in [0, 1]:
        tw, th = tag_sizes[i]
        draw.rounded_rectangle([rx, cy, rx + tw, cy + th],
                                radius=22, fill=opt_colors[i],
                                outline=opt_borders[i], width=2)
        bb = draw.textbbox((0, 0), opts[i], font=fnt_op)
        draw.text((rx + (tw - (bb[2] - bb[0])) // 2,
                   cy + (th - (bb[3] - bb[1])) // 2 - 2),
                  opts[i], font=fnt_op, fill=TXT)
        rx += tw + tag_gap
    cy += tag_sizes[0][1] + 14

    # Linha 2
    row2_w = tag_sizes[2][0] + tag_sizes[3][0] + tag_gap
    rx = cx - row2_w // 2
    for i in [2, 3]:
        tw, th = tag_sizes[i]
        draw.rounded_rectangle([rx, cy, rx + tw, cy + th],
                                radius=22, fill=opt_colors[i],
                                outline=opt_borders[i], width=2)
        bb = draw.textbbox((0, 0), opts[i], font=fnt_op)
        draw.text((rx + (tw - (bb[2] - bb[0])) // 2,
                   cy + (th - (bb[3] - bb[1])) // 2 - 2),
                  opts[i], font=fnt_op, fill=TXT)
        rx += tw + tag_gap
    cy += tag_sizes[2][1] + 60

    # Instrução + seta pra baixo
    inst = "use a enquete abaixo pra votar"
    bb_i = draw.textbbox((0, 0), inst, font=fnt_inst)
    iw   = bb_i[2] - bb_i[0]
    ih   = bb_i[3] - bb_i[1]
    draw.text((cx - iw // 2, cy), inst, font=fnt_inst, fill=TXT)
    cy += ih + 24

    draw.polygon(
        [(cx - 22, cy), (cx + 22, cy), (cx, cy + 34)],
        fill=OURO
    )

    base_flores(draw)
    marca_rodape(draw)
    border(draw, col=OURO_S)

    out = os.path.join(BASE_DIR, "02 - Criativos", "maio28", "story_maio28_6.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 7 — CTA: "garante a tua caixa" + cardápio
# ─────────────────────────────────────────────────────────────────────────────
def story_7_cta():
    img  = bg_grad(PESSEGO, CREME)
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc  = load_font("NothingYouCouldDo-Regular.ttf",  76)
    fnt_tit = load_font("Lora-Bold.ttf",                  96)
    fnt_det = load_font("Lora-Italic.ttf",                 42)
    fnt_cta = load_font("InstrumentSans-Bold.ttf",         42)
    fnt_br  = load_font("InstrumentSans-Bold.ttf",         36)

    topo_flores(draw)

    cy = 540

    # Script
    cy = script_outlined_wrap(
        draw, "já sabe qual.",
        fnt_sc, W - 120, cx, cy,
        fill=OURO_S, ol_col=(180, 130, 40), ol=2, line_sp=4
    ) + 28

    # Ornamento
    draw.line([(cx - 90, cy), (cx - 16, cy)], fill=OURO, width=2)
    draw.line([(cx + 16, cy), (cx + 90, cy)], fill=OURO, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 44

    # Título
    cy = wrap_centered(
        draw, "garante a tua caixa.",
        fnt_tit, W - 80, cx, cy,
        fill=TXT, shadow=True, shd_col=(210, 188, 148), line_spacing=12
    ) + 20

    # Divisor
    draw.line([(cx - 100, cy), (cx + 100, cy)], fill=(195, 168, 105), width=1)
    cy += 30

    # Suporte
    cy = wrap_centered(
        draw, "a agenda da Oliete segue enchendo. junho tá batendo na porta.",
        fnt_det, W - 120, cx, cy,
        fill=(110, 78, 38), line_spacing=12
    ) + 44

    # CTA box
    cta_text = "veja o cardápio completo"
    cta_w, cta_h, r = 720, 100, 20
    cta_x = cx - cta_w // 2
    draw.rounded_rectangle([cta_x, cy, cta_x + cta_w, cy + cta_h],
                            radius=r, fill=OURO, outline=OURO_P, width=2)
    bb = draw.textbbox((0, 0), cta_text, font=fnt_cta)
    draw.text((cx - (bb[2] - bb[0]) // 2,
               cy + (cta_h - (bb[3] - bb[1])) // 2),
              cta_text, font=fnt_cta, fill=BRANCO)
    arr_x = cta_x + cta_w - 42
    arr_y = cy + cta_h // 2
    draw.polygon([(arr_x, arr_y - 10), (arr_x + 18, arr_y), (arr_x, arr_y + 10)],
                 fill=OURO_P)
    cy += cta_h + 12

    lbl = "link disponível no story"
    fnt_lbl_cta = load_font("InstrumentSans-Bold.ttf", 34)
    bb_l = draw.textbbox((0, 0), lbl, font=fnt_lbl_cta)
    draw.text((cx - (bb_l[2] - bb_l[0]) // 2, cy + 6),
              lbl, font=fnt_lbl_cta, fill=(150, 110, 55))

    base_flores(draw)
    marca_rodape(draw)
    border(draw, col=OURO_S)

    out = os.path.join(BASE_DIR, "02 - Criativos", "maio28", "story_maio28_7.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


if __name__ == "__main__":
    story_1()
    story_2_frango()
    story_3_carne()
    story_4_calabresa()
    story_5_legumes()
    story_6_enquete()
    story_7_cta()
    print("7 Stories 28/05 prontos.")
