# -*- coding: utf-8 -*-
"""
Post Segunda Chuvosa v2 — Ok Delícias com Amor — 25/05/2026
Conceito: céu cinza vs caixa dourada de salgados
Foto: IMG_1049 — caixa de pastéis dourados (herói visual)
Referência: Lamentações 3:22-23
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
import math, os

BASE_DIR  = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR = (r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions"
             r"\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316"
             r"\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts")

CINZA_T   = (182, 188, 205)
CREME     = (255, 248, 234)
OURO      = (179, 138,  52)
OURO_S    = (210, 175, 100)
OURO_P    = (235, 210, 155)
LAVANDA_F = (196, 181, 224)
TXT       = ( 38,  22,   8)
TXT_M     = ( 80,  58,  28)
CHUMBO    = ( 88,  95, 115)

W, H = 1080, 1080


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
    draw.rounded_rectangle([16, 16, W - 16, H - 16], radius=28,
                            outline=OURO_S, width=2)
    draw.rounded_rectangle([26, 26, W - 26, H - 26], radius=20,
                            outline=(195, 175, 118), width=1)


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
    if col_out is None: col_out = LAVANDA_F
    if col_mid is None: col_mid = OURO_P
    for i in range(petals):
        draw_petal(draw, cx, cy, 360 / petals * i, plen, pw, col_out)
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=col_mid)


def draw_leaf(draw, cx, cy, angle_deg, length=12, width=5):
    VERDE   = (128, 155, 105)
    VERDE_E = ( 88, 116,  75)
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
            draw.text((x + 2, y + 2), line, font=font, fill=shd_col)
        draw.text((x, y), line, font=font, fill=fill)
        y += (bb[3] - bb[1]) + line_spacing
    return y


def script_outlined_wrap(draw, text, font, max_w, cx, y,
                          fill=None, ol_col=(210, 205, 222), ol=2, line_sp=8):
    if fill is None: fill = OURO_S
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


def paste_rounded(canvas, foto, x, y, radius=18):
    """Cola foto com cantos arredondados no canvas RGB."""
    ph_w, ph_h = foto.size
    mask = Image.new("L", (ph_w, ph_h), 0)
    md   = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, ph_w, ph_h], radius=radius, fill=255)
    canvas.paste(foto, (x, y), mask)


def post_segunda_chuvosa():
    img  = bg_grad(CINZA_T, CREME)
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc  = load_font("NothingYouCouldDo-Regular.ttf", 52)
    fnt_tit = load_font("Lora-Bold.ttf",                 82)
    fnt_sub = load_font("Lora-BoldItalic.ttf",           46)
    fnt_ver = load_font("Lora-Italic.ttf",               37)
    fnt_ref = load_font("InstrumentSans-Bold.ttf",       26)
    fnt_br  = load_font("InstrumentSans-Bold.ttf",       30)

    # Flores topo (tons lavanda — céu cinza)
    for fx, col_o in [(60, (200, 192, 222)), (W - 60, (186, 178, 212))]:
        draw_flower(draw, fx, 76, petals=6, plen=13, pw=6,
                    col_out=col_o, col_mid=OURO_P, cr=5)
        draw_leaf(draw, fx - 10, 89, 225, 11, 4)
        draw_leaf(draw, fx + 10, 89, 315, 11, 4)

    cy = 162

    # Script âncora — leitura garantida (escuro sobre cinza)
    cy = script_outlined_wrap(
        draw, "segunda de manhã.",
        fnt_sc, W - 160, cx, cy,
        fill=TXT, ol_col=(235, 230, 240), ol=2, line_sp=4
    ) + 16

    # Ornamento
    draw.line([(cx - 78, cy), (cx - 14, cy)], fill=OURO_S, width=1)
    draw.line([(cx + 14, cy), (cx + 78, cy)], fill=OURO_S, width=1)
    diamond(draw, cx, cy, 5, OURO)
    cy += 28

    # Título — o setup
    cy = wrap_centered(
        draw, "o céu está cinza.",
        fnt_tit, W - 80, cx, cy,
        fill=TXT, line_spacing=8
    ) + 12

    # Divisor fino antes da foto
    draw.line([(24, cy), (W - 24, cy)], fill=(185, 168, 140), width=1)
    cy += 14

    # ─── FOTO HERÓI ─── caixa de pastéis dourados
    foto_path = os.path.join(BASE_DIR, "fotos", "IMG_1049.JPEG")
    ph_w  = W - 48      # 1032 — borda 24px cada lado
    ph_h  = 345
    x_ph  = 24
    y_ph  = cy

    try:
        foto = ImageOps.exif_transpose(Image.open(foto_path)).convert("RGB")
        # Redimensionar para largura-alvo mantendo proporção
        ratio  = ph_w / foto.width
        new_h  = int(foto.height * ratio)
        foto   = foto.resize((ph_w, new_h), Image.LANCZOS)
        # Cortar: pular borda da caixa (~30%) e tomar ph_h
        skip   = int(new_h * 0.30)
        foto   = foto.crop((0, skip, ph_w, skip + ph_h))

        # Realçar brilho e cor dos salgados dourados
        foto = ImageEnhance.Brightness(foto).enhance(1.12)
        foto = ImageEnhance.Color(foto).enhance(1.18)
        foto = ImageEnhance.Contrast(foto).enhance(1.08)

        # Borda dourada antes de colar
        draw.rounded_rectangle(
            [x_ph - 2, y_ph - 2, x_ph + ph_w + 2, y_ph + ph_h + 2],
            radius=21, outline=OURO_S, width=2
        )
        paste_rounded(img, foto, x_ph, y_ph, radius=18)

        # Overlay dourado suave no rodapé da foto (transição para texto)
        grad_h = 60
        for gy in range(grad_h):
            alpha = int(80 * gy / grad_h)
            overlay_col = lerp(CREME, CREME, 1.0)  # creme puro
            rl = draw.getdraw() if hasattr(draw, 'getdraw') else draw
            # linha com opacidade simulada: blend manual não é trivial em RGB puro,
            # mas a divisória dourada abaixo já cria a separação visual necessária

        cy = y_ph + ph_h + 2

    except Exception as e:
        print(f"Aviso foto: {e}")
        cy += ph_h

    # Divisor fino após foto
    draw.line([(24, cy + 12), (W - 24, cy + 12)], fill=(185, 168, 140), width=1)
    cy += 28

    # Subtítulo — a virada
    cy = wrap_centered(
        draw, "mas a Oliete já está na cozinha.",
        fnt_sub, W - 80, cx, cy,
        fill=TXT_M, line_spacing=8
    ) + 12

    # Versículo distilado
    cy = wrap_centered(
        draw, "\"Grande é a tua fidelidade.\"",
        fnt_ver, W - 120, cx, cy,
        fill=CHUMBO, line_spacing=10
    ) + 8

    # Referência bíblica
    ref  = "Lamentações 3:22-23"
    bb   = draw.textbbox((0, 0), ref, font=fnt_ref)
    draw.text((cx - (bb[2] - bb[0]) // 2, cy), ref, font=fnt_ref, fill=OURO)
    cy += (bb[3] - bb[1])

    # Flores base (dourado quente — calor da cozinha)
    for fx in [60, W - 60]:
        draw_flower(draw, fx, H - 80, petals=6, plen=12, pw=6,
                    col_out=(215, 178, 105), col_mid=OURO_P, cr=5)

    # Assinatura da marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 54),
              "Ok Delícias com Amor", font=fnt_br, fill=TXT_M)

    border(draw)

    out = os.path.join(BASE_DIR, "02 - Criativos", "post_maio25.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


if __name__ == "__main__":
    post_segunda_chuvosa()
    print("Post v2 pronto.")
