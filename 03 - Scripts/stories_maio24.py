# -*- coding: utf-8 -*-
"""
Story Domingo à Noite — Ok Delícias com Amor — 24/05/2026
Conceito: fim de domingo sagrado, descanso merecido, passagem bíblica
Tom: íntimo, quente, espiritual, humanizado
Foto: nenhuma — gradiente escuro entardecer
"""

from PIL import Image, ImageDraw, ImageFont
import math, os

BASE_DIR  = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR = (r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions"
             r"\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316"
             r"\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts")

# Paleta entardecer / fim de domingo
NOITE_F   = ( 22,  10,   3)   # preto quente
NOITE_A   = ( 62,  30,   8)   # marrom âmbar profundo
CREME     = (255, 248, 234)
OURO      = (179, 138,  52)
OURO_S    = (210, 175, 100)
OURO_P    = (235, 210, 155)
ROSA      = (220, 185, 165)
VERDE     = (120, 150, 100)
VERDE_E   = ( 80, 110,  68)

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


def border(draw):
    draw.rounded_rectangle([16, 16, W - 16, H - 16], radius=32,
                            outline=OURO_S, width=2)
    draw.rounded_rectangle([26, 26, W - 26, H - 26], radius=24,
                            outline=(95, 68, 28), width=1)


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
    if col_out is None: col_out = ROSA
    if col_mid is None: col_mid = OURO_P
    for i in range(petals):
        draw_petal(draw, cx, cy, 360 / petals * i, plen, pw, col_out)
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=col_mid)


def draw_leaf(draw, cx, cy, angle_deg, length=12, width=5):
    draw_petal(draw, cx, cy, angle_deg,       length,      width,      VERDE)
    draw_petal(draw, cx, cy, angle_deg + 180, length * .4, width * .5, VERDE_E)


def diamond(draw, cx, cy, size, color):
    draw.polygon(
        [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)],
        fill=color
    )


def wrap_centered(draw, text, font, max_w, cx, y, fill,
                  line_spacing=10, shadow=False, shd_col=(8, 3, 1)):
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
                          fill=None, ol_col=(5, 2, 0), ol=2, line_sp=8):
    if fill is None: fill = OURO_P
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


def story_domingo():
    img  = bg_grad(NOITE_F, NOITE_A)
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc  = load_font("NothingYouCouldDo-Regular.ttf", 74)
    fnt_tit = load_font("Lora-Bold.ttf",            90)
    fnt_hum = load_font("Lora-BoldItalic.ttf",       42)
    fnt_ver = load_font("Lora-BoldItalic.ttf",       46)
    fnt_ref = load_font("InstrumentSans-Bold.ttf",   32)
    fnt_det = load_font("InstrumentSans-Bold.ttf",   40)
    fnt_br  = load_font("InstrumentSans-Bold.ttf",   34)

    # Flores topo — tons dourados sobre fundo escuro
    for fx, col_o in [(66, (195, 158, 92)), (W - 66, (172, 132, 68))]:
        draw_flower(draw, fx, 96, petals=6, plen=14, pw=7,
                    col_out=col_o, col_mid=OURO_P, cr=5)
        draw_leaf(draw, fx - 12, 110, 225, 12, 5)
        draw_leaf(draw, fx + 12, 110, 315, 12, 5)

    # Conteúdo centrado verticalmente (cy calculado para equilibrar topo/base)
    cy = 460

    # Script — âncora emocional
    cy = script_outlined_wrap(
        draw, "fim de domingo.",
        fnt_sc, W - 160, cx, cy,
        fill=OURO_S, ol_col=(14, 6, 1), ol=2, line_sp=4
    ) + 30

    # Ornamento
    draw.line([(cx - 90, cy), (cx - 16, cy)], fill=OURO_S, width=2)
    draw.line([(cx + 16, cy), (cx + 90, cy)], fill=OURO_S, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 40

    # Titulo — o descanso da Oliete
    cy = wrap_centered(
        draw, "hoje a Oliete descansou.",
        fnt_tit, W - 80, cx, cy,
        fill=CREME, shadow=True, line_spacing=10
    ) + 36

    # Divisor
    draw.line([(cx - 110, cy), (cx + 110, cy)], fill=(105, 75, 32), width=1)
    cy += 28

    # Humanização — não é cansaço, é descanso sagrado
    cy = wrap_centered(
        draw,
        "não que ela esteja cansada de trabalhar,"
        " porque Deus sabe que ela não cansa,"
        " ela ama o que faz.",
        fnt_hum, W - 120, cx, cy,
        fill=(195, 172, 128), line_spacing=10
    ) + 28

    # Divisor
    draw.line([(cx - 75, cy), (cx + 75, cy)], fill=(95, 68, 25), width=1)
    cy += 28

    # Versículo — Mateus 11.28 (uma chamada, quebra natural)
    cy = wrap_centered(
        draw,
        "\"Vinde a mim, todos os que estais cansados "
        "e sobrecarregados, e eu vos darei descanso.\"",
        fnt_ver, W - 110, cx, cy,
        fill=OURO_P, line_spacing=14
    ) + 18

    # Referência bíblica
    bb = draw.textbbox((0, 0), "Mateus 11.28", font=fnt_ref)
    draw.text((cx - (bb[2] - bb[0]) // 2, cy),
              "Mateus 11.28", font=fnt_ref, fill=OURO_S)
    cy += (bb[3] - bb[1]) + 50

    # Divisor
    draw.line([(cx - 75, cy), (cx + 75, cy)], fill=(105, 75, 32), width=1)
    cy += 32

    # Mensagem de encerramento
    cy = wrap_centered(
        draw, "amanhã voltamos com toda energia, amor e carinho.",
        fnt_det, W - 120, cx, cy,
        fill=(205, 188, 158), line_spacing=8
    )

    # Flores cantos inferiores — tom dourado sobre escuro
    for fx in [66, W - 66]:
        draw_flower(draw, fx, H - 130, petals=6, plen=12, pw=6,
                    col_out=(178, 138, 68), col_mid=OURO_P, cr=5)

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 72),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO_S)

    border(draw)
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio24", "story_maio24_domingo.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


if __name__ == "__main__":
    story_domingo()
    print("Story domingo à noite pronto.")
