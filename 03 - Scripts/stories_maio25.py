# -*- coding: utf-8 -*-
"""
3 Stories Segunda Chuvosa — Ok Delícias com Amor — 25/05/2026

Arc: bastidores do dia → produto + enquete → urgência Festa Junina

Story 1: "a cozinha não parou." — foto herói, bastidores da segunda
Story 2: "é o pastel da Oliete." — produto de perto + poll visual
Story 3: "junho está chegando." — urgência Festa Junina, CTA WhatsApp
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
import math, os

BASE_DIR  = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR = (r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions"
             r"\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316"
             r"\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts")

CREME     = (255, 248, 234)
PESSEGO   = (255, 232, 192)
OURO      = (179, 138,  52)
OURO_S    = (210, 175, 100)
OURO_P    = (235, 210, 155)
LAVANDA_M = (196, 181, 224)
TXT       = ( 38,  22,   8)
TXT_M     = ( 72,  50,  28)
BRANCO    = (255, 255, 255)
VERDE     = (128, 155, 105)
VERDE_E   = ( 88, 116,  75)

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


def foto_fundo(path, overlay_alpha=160, overlay_color=(18, 8, 2)):
    """Foto full-bleed com overlay escuro para legibilidade do texto."""
    img  = Image.open(path)
    img  = ImageOps.exif_transpose(img).convert("RGB")
    img  = ImageEnhance.Brightness(img).enhance(1.08)
    img  = ImageEnhance.Color(img).enhance(1.14)
    # Redimensionar cobrindo todo o canvas (crop centralizado)
    ratio_w = W / img.width
    ratio_h = H / img.height
    ratio   = max(ratio_w, ratio_h)
    nw      = int(img.width  * ratio)
    nh      = int(img.height * ratio)
    img     = img.resize((nw, nh), Image.LANCZOS)
    x_off   = max(0, (nw - W) // 2)
    y_off   = max(0, (nh - H) // 2)
    img     = img.crop((x_off, y_off, x_off + W, y_off + H))
    # Overlay escuro quente
    overlay = Image.new("RGBA", (W, H), overlay_color + (overlay_alpha,))
    base    = img.convert("RGBA")
    base.alpha_composite(overlay)
    return base.convert("RGB")


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
    if col_out is None: col_out = (210, 195, 235)
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


def poll_buttons(draw, cx, y, opt_a, opt_b,
                 fnt, col_a=OURO_S, col_b=BRANCO):
    """Dois botões de enquete visual (sem funcionalidade, estético)."""
    bw, bh, gap, r = 420, 88, 24, 18
    # Botão A
    ax = cx - bw - gap // 2
    draw.rounded_rectangle([ax, y, ax + bw, y + bh],
                            radius=r, fill=OURO, outline=OURO_S, width=2)
    bb = draw.textbbox((0, 0), opt_a, font=fnt)
    draw.text((ax + (bw - (bb[2] - bb[0])) // 2,
               y  + (bh - (bb[3] - bb[1])) // 2),
              opt_a, font=fnt, fill=BRANCO)
    # Botão B — fundo semi-escuro para texto branco legível
    bx = cx + gap // 2
    draw.rounded_rectangle([bx, y, bx + bw, y + bh],
                            radius=r, fill=(60, 38, 14), outline=OURO_S, width=2)
    bb2 = draw.textbbox((0, 0), opt_b, font=fnt)
    draw.text((bx + (bw - (bb2[2] - bb2[0])) // 2,
               y  + (bh - (bb2[3] - bb2[1])) // 2),
              opt_b, font=fnt, fill=BRANCO)
    return y + bh + 16


# ─────────────────────────────────────────────────────────────────────────────
# STORY 1 — Bastidores: "a cozinha não parou"
# Foto herói full-bleed, texto mínimo, tom documental
# ─────────────────────────────────────────────────────────────────────────────
def story_1():
    foto_path = os.path.join(BASE_DIR, "fotos", "IMG_1049.JPEG")
    img  = foto_fundo(foto_path, overlay_alpha=158, overlay_color=(18, 8, 2))
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc  = load_font("NothingYouCouldDo-Regular.ttf", 72)
    fnt_tit = load_font("Lora-Bold.ttf",                100)
    fnt_sub = load_font("Lora-BoldItalic.ttf",           48)
    fnt_br  = load_font("InstrumentSans-Bold.ttf",       36)

    cy = 480

    # Script âncora
    cy = script_outlined_wrap(
        draw, "segunda de manhã.",
        fnt_sc, W - 160, cx, cy,
        fill=OURO_P, ol_col=(10, 4, 1), ol=2, line_sp=4
    ) + 24

    # Ornamento
    draw.line([(cx - 90, cy), (cx - 16, cy)], fill=OURO_S, width=2)
    draw.line([(cx + 16, cy), (cx + 90, cy)], fill=OURO_S, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 44

    # Título
    cy = wrap_centered(
        draw, "a cozinha não parou.",
        fnt_tit, W - 80, cx, cy,
        fill=BRANCO, shadow=True, shd_col=(8, 3, 1), line_spacing=12
    ) + 24

    # Subtítulo
    cy = wrap_centered(
        draw, "enquanto o céu fechava, ela produzia.",
        fnt_sub, W - 120, cx, cy,
        fill=OURO_P, line_spacing=10
    )

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 72),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO_S)

    border(draw, col=OURO_S)
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio25", "story_maio25_1.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 2 — Produto + Poll: "é o pastel da Oliete"
# Foto de perto, texto de desejo, enquete visual
# ─────────────────────────────────────────────────────────────────────────────
def story_2():
    foto_path = os.path.join(BASE_DIR, "fotos", "IMG_1153.JPEG")
    img  = foto_fundo(foto_path, overlay_alpha=145, overlay_color=(20, 9, 2))
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc   = load_font("NothingYouCouldDo-Regular.ttf", 68)
    fnt_tit  = load_font("Lora-Bold.ttf",                 96)
    fnt_sub  = load_font("Lora-BoldItalic.ttf",           46)
    fnt_det  = load_font("Lora-Italic.ttf",               40)
    fnt_poll = load_font("InstrumentSans-Bold.ttf",        38)
    fnt_br   = load_font("InstrumentSans-Bold.ttf",        36)

    cy = 430

    # Script
    cy = script_outlined_wrap(
        draw, "foi isso que saiu da cozinha.",
        fnt_sc, W - 140, cx, cy,
        fill=OURO_P, ol_col=(10, 4, 1), ol=2, line_sp=4
    ) + 20

    # Ornamento
    draw.line([(cx - 90, cy), (cx - 16, cy)], fill=OURO_S, width=2)
    draw.line([(cx + 16, cy), (cx + 90, cy)], fill=OURO_S, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 44

    # Título
    cy = wrap_centered(
        draw, "o pedido completo.",
        fnt_tit, W - 80, cx, cy,
        fill=BRANCO, shadow=True, shd_col=(8, 3, 1), line_spacing=10
    ) + 22

    # Detalhe de produto
    cy = wrap_centered(
        draw, "coxinha, pastel, rolinho. do jeito que você gosta.",
        fnt_det, W - 120, cx, cy,
        fill=OURO_P, line_spacing=10
    ) + 52

    # Divisor
    draw.line([(cx - 100, cy), (cx + 100, cy)], fill=(180, 150, 80), width=1)
    cy += 36

    # Pergunta
    cy = wrap_centered(
        draw, "qual é o seu favorito?",
        fnt_sub, W - 120, cx, cy,
        fill=BRANCO, line_spacing=10
    ) + 32

    # Poll visual
    poll_buttons(draw, cx, cy, "quero encomendar", "já sou cliente", fnt_poll)

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 72),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO_S)

    border(draw, col=OURO_S)
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio25", "story_maio25_2.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 3 — Urgência: "junho está chegando"
# Sem foto — gradiente creme/dourado, Festa Junina, CTA direto
# ─────────────────────────────────────────────────────────────────────────────
def story_3():
    img  = bg_grad(CREME, PESSEGO)
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc  = load_font("NothingYouCouldDo-Regular.ttf",  76)
    fnt_tit = load_font("Lora-Bold.ttf",                  98)
    fnt_sub = load_font("Lora-BoldItalic.ttf",             52)
    fnt_det = load_font("Lora-Italic.ttf",                 44)
    fnt_cta = load_font("InstrumentSans-Bold.ttf",         42)
    fnt_br  = load_font("InstrumentSans-Bold.ttf",         36)

    # Flores topo — tons quentes e festivos
    for fx, col_o in [(66, (220, 185, 120)), (W - 66, (205, 168, 100))]:
        draw_flower(draw, fx, 96, petals=6, plen=14, pw=7,
                    col_out=col_o, col_mid=OURO_P, cr=5)
        draw_leaf(draw, fx - 12, 110, 225, 13, 5)
        draw_leaf(draw, fx + 12, 110, 315, 13, 5)

    cy = 600

    # Script âncora — contagem
    cy = script_outlined_wrap(
        draw, "em 6 dias.",
        fnt_sc, W - 160, cx, cy,
        fill=OURO_S, ol_col=(180, 130, 40), ol=2, line_sp=4
    ) + 24

    # Ornamento
    draw.line([(cx - 90, cy), (cx - 16, cy)], fill=OURO, width=2)
    draw.line([(cx + 16, cy), (cx + 90, cy)], fill=OURO, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 40

    # Título
    cy = wrap_centered(
        draw, "junho chega.",
        fnt_tit, W - 80, cx, cy,
        fill=TXT, shadow=True, shd_col=(210, 188, 148), line_spacing=10
    ) + 16

    # Divisor
    draw.line([(cx - 100, cy), (cx + 100, cy)], fill=(195, 168, 105), width=1)
    cy += 30

    # Gancho Festa Junina
    cy = wrap_centered(
        draw, "sua Festa Junina já tem salgado?",
        fnt_sub, W - 100, cx, cy,
        fill=TXT_M, line_spacing=12
    ) + 20

    # Suporte
    cy = wrap_centered(
        draw, "a agenda da Oliete está abrindo agora. quem reserva primeiro, garante.",
        fnt_det, W - 120, cx, cy,
        fill=(110, 78, 38), line_spacing=12
    ) + 44

    # CTA box
    cta_text = "(55) 99928-5883"
    cta_w, cta_h, r = 680, 100, 20
    cta_x = cx - cta_w // 2
    draw.rounded_rectangle([cta_x, cy, cta_x + cta_w, cy + cta_h],
                            radius=r, fill=OURO, outline=OURO_P, width=2)
    bb = draw.textbbox((0, 0), cta_text, font=fnt_cta)
    draw.text((cx - (bb[2] - bb[0]) // 2,
               cy + (cta_h - (bb[3] - bb[1])) // 2),
              cta_text, font=fnt_cta, fill=BRANCO)
    cy += cta_h + 12

    # Label abaixo do botão
    lbl = "WhatsApp para encomendas"
    bb_l = draw.textbbox((0, 0), lbl, font=fnt_br)
    draw.text((cx - (bb_l[2] - bb_l[0]) // 2, cy),
              lbl, font=load_font("InstrumentSans-Bold.ttf", 28), fill=(150, 110, 55))

    # Flores cantos inferiores
    for fx in [66, W - 66]:
        draw_flower(draw, fx, H - 130, petals=6, plen=13, pw=6,
                    col_out=(210, 175, 100), col_mid=OURO_P, cr=5)

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 68),
              "Ok Delícias com Amor", font=fnt_br, fill=TXT_M)

    border(draw, col=OURO_S)
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio25", "story_maio25_3.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


if __name__ == "__main__":
    story_1()
    story_2()
    story_3()
    print("3 Stories 25/05 prontos.")
