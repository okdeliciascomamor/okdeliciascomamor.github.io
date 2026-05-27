# -*- coding: utf-8 -*-
"""
3 Stories Quarta — Ok Delícias com Amor — 27/05/2026

Arc: revelação do resultado da enquete (Risoles 62% vs Mini Hambúrguer 38%)
Story 1: REVEAL — "62%" + "vocês decidiram"
Story 2: HERO — foto_drive_C (risoles em produção) + escassez
Story 3: CTA — "garante o teu lugar" + cardápio

Fotos NOVAS (não repetidas):
- Story 1: sem foto (typography)
- Story 2: foto_drive_C.jpg (risoles em produção — nunca usada)
- Story 3: sem foto (typography + botão)
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
import math, os

BASE_DIR  = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR = (r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions"
             r"\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316"
             r"\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts")

CREME     = (255, 248, 234)
LAVANDA   = (232, 222, 244)
LAVANDA_E = (196, 181, 224)
PESSEGO   = (255, 232, 192)
OURO      = (179, 138,  52)
OURO_S    = (210, 175, 100)
OURO_P    = (235, 210, 155)
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


def draw_leaf(draw, cx, cy, angle_deg, length=12, width=5):
    draw_petal(draw, cx, cy, angle_deg,       length,      width,      VERDE)
    draw_petal(draw, cx, cy, angle_deg + 180, length * .4, width * .5, VERDE_E)


def diamond(draw, cx, cy, size, color):
    draw.polygon(
        [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)],
        fill=color
    )


def small_star(draw, cx, cy, size, color):
    """Estrela 4-pontas pequena"""
    draw.polygon(
        [(cx, cy - size), (cx + size * 0.35, cy - size * 0.35),
         (cx + size, cy), (cx + size * 0.35, cy + size * 0.35),
         (cx, cy + size), (cx - size * 0.35, cy + size * 0.35),
         (cx - size, cy), (cx - size * 0.35, cy - size * 0.35)],
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


def foto_fundo(path, W_, H_, enhance=True):
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if enhance:
        img = ImageEnhance.Brightness(img).enhance(1.06)
        img = ImageEnhance.Color(img).enhance(1.12)
    ratio = max(W_ / img.width, H_ / img.height)
    nw    = int(img.width  * ratio)
    nh    = int(img.height * ratio)
    img   = img.resize((nw, nh), Image.LANCZOS)
    x_off = max(0, (nw - W_) // 2)
    y_off = max(0, (nh - H_) // 2)
    return img.crop((x_off, y_off, x_off + W_, y_off + H_))


# ─────────────────────────────────────────────────────────────────────────────
# STORY 1 — REVEAL: "62%" vocês decidiram
# ─────────────────────────────────────────────────────────────────────────────
def story_1():
    img  = bg_grad(CREME, LAVANDA)
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc   = load_font("NothingYouCouldDo-Regular.ttf",  78)
    fnt_tit  = load_font("Lora-Bold.ttf",                  86)
    fnt_sub  = load_font("Lora-BoldItalic.ttf",            48)
    fnt_det  = load_font("Lora-Italic.ttf",                40)
    fnt_br   = load_font("InstrumentSans-Bold.ttf",        36)

    # Flores topo
    for fx, col_o in [(66, (220, 185, 120)), (W - 66, (205, 168, 100))]:
        draw_flower(draw, fx, 96, petals=6, plen=14, pw=7,
                    col_out=col_o, col_mid=OURO_P, cr=5)
        draw_leaf(draw, fx - 12, 110, 225, 13, 5)
        draw_leaf(draw, fx + 12, 110, 315, 13, 5)

    cy = 300

    # Script tag
    cy = script_outlined_wrap(
        draw, "vocês decidiram.",
        fnt_sc, W - 120, cx, cy,
        fill=OURO_S, ol_col=(180, 130, 40), ol=2, line_sp=4
    ) + 36

    # Linha ornamental
    draw.line([(cx - 100, cy), (cx - 16, cy)], fill=OURO, width=2)
    draw.line([(cx + 16, cy), (cx + 100, cy)], fill=OURO, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 70

    # Print da enquete do Instagram — herói visual (prova social real)
    poll_path = os.path.join(BASE_DIR, "02 - Criativos", "maio27", "poll_print.png")
    poll = Image.open(poll_path).convert("RGBA")

    # Escala para 880px de largura
    target_w = 880
    scale    = target_w / poll.width
    target_h = int(poll.height * scale)
    poll     = poll.resize((target_w, target_h), Image.LANCZOS)

    poll_x = cx - target_w // 2
    poll_y = cy

    # Sombra suave embaixo (sem wrapper card — print direto na composição)
    img_rgba = img.convert("RGBA")
    shadow = Image.new("RGBA", (target_w + 60, target_h + 60), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for k in range(10):
        a = max(0, int(22 - k * 2))
        sd.rounded_rectangle(
            [k, k, target_w + 60 - k, target_h + 60 - k],
            radius=22, fill=(120, 100, 140, a)
        )
    img_rgba.alpha_composite(shadow, (poll_x - 30, poll_y - 16))

    # Print colado direto
    img_rgba.alpha_composite(poll, (poll_x, poll_y))

    img  = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    cy = poll_y + target_h + 70

    # Estrelinhas decorativas ao redor do print
    small_star(draw, poll_x - 36,             poll_y + 16,              11, OURO_S)
    small_star(draw, poll_x + target_w + 36,  poll_y + target_h - 20,   13, OURO_S)
    small_star(draw, poll_x + target_w + 28,  poll_y + 30,               9, OURO_S)
    small_star(draw, poll_x - 28,             poll_y + target_h - 40,    8, OURO_S)

    # Sublinha dourada
    draw.line([(cx - 220, cy), (cx + 220, cy)], fill=OURO, width=2)
    cy += 40

    # Título
    cy = wrap_centered(
        draw, "risoles é o favorito.",
        fnt_tit, W - 80, cx, cy,
        fill=TXT, shadow=True, shd_col=(195, 178, 215), line_spacing=12
    ) + 24

    # Sub
    cy = wrap_centered(
        draw, "6 em cada 10 escolheram.",
        fnt_sub, W - 100, cx, cy,
        fill=TXT_M, line_spacing=10
    ) + 20

    # Detalhe
    wrap_centered(
        draw, "veja o próximo story.",
        fnt_det, W - 140, cx, cy,
        fill=(108, 86, 118), line_spacing=10
    )

    # Flores base
    for fx in [66, W - 66]:
        draw_flower(draw, fx, H - 130, petals=6, plen=13, pw=6,
                    col_out=(210, 175, 100), col_mid=OURO_P, cr=5)

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 68),
              "Ok Delícias com Amor", font=fnt_br, fill=TXT_M)

    border(draw, col=OURO_S)
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio27", "story_maio27_1.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 2 — HERO: foto_drive_C (risoles em produção)
# ─────────────────────────────────────────────────────────────────────────────
def story_2():
    # Foto de fundo full bleed
    img = foto_fundo(os.path.join(BASE_DIR, "fotos", "foto_drive_C.jpg"), W, H)

    # Overlay gradiente pra legibilidade do texto (topo + base bem escuros)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(H):
        if y < 520:
            # topo bem escuro pra script tag ser legível
            a = int(235 * (1 - y / 520))
            od.line([(0, y), (W, y)], fill=(18, 10, 2, min(a, 240)))
        elif y > 1100:
            # base escura pra copy principal
            a = int(230 * ((y - 1100) / (H - 1100)))
            od.line([(0, y), (W, y)], fill=(18, 10, 2, min(a, 235)))

    img = img.convert("RGBA")
    img.alpha_composite(overlay)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc  = load_font("NothingYouCouldDo-Regular.ttf",  76)
    fnt_tit = load_font("Lora-Bold.ttf",                  88)
    fnt_sub = load_font("Lora-BoldItalic.ttf",            46)
    fnt_det = load_font("Lora-Italic.ttf",                40)
    fnt_br  = load_font("InstrumentSans-Bold.ttf",        34)

    # Topo: script tag — branco com contorno escuro grosso pra contraste máximo
    cy = 150
    cy = script_outlined_wrap(
        draw, "feito à mão, agora.",
        fnt_sc, W - 80, cx, cy,
        fill=BRANCO, ol_col=(0, 0, 0), ol=3, line_sp=4
    )

    # Ornamento dourado abaixo do script
    cy += 18
    draw.line([(cx - 90, cy), (cx - 14, cy)], fill=OURO_P, width=2)
    draw.line([(cx + 14, cy), (cx + 90, cy)], fill=OURO_P, width=2)
    diamond(draw, cx, cy, 6, OURO_P)

    # Inferior: copy principal
    cy = H - 600
    cy = wrap_centered(
        draw, "a Oli não para hoje.",
        fnt_tit, W - 100, cx, cy,
        fill=BRANCO, shadow=True, shd_col=(0, 0, 0), line_spacing=14
    ) + 26

    # Divisor
    draw.line([(cx - 110, cy), (cx + 110, cy)], fill=OURO, width=2)
    cy += 32

    # Sub: escassez
    cy = wrap_centered(
        draw, "as vagas de junho seguem enchendo.",
        fnt_sub, W - 100, cx, cy,
        fill=OURO_P, line_spacing=12
    ) + 18

    # Detail
    wrap_centered(
        draw, "veja o próximo story pra garantir o seu.",
        fnt_det, W - 120, cx, cy,
        fill=(220, 200, 160), line_spacing=10
    )

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 72),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO_P)

    border(draw, col=OURO_S)
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio27", "story_maio27_2.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 3 — CTA: "garante o teu lugar"
# ─────────────────────────────────────────────────────────────────────────────
def story_3():
    img  = bg_grad(LAVANDA, CREME)
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc  = load_font("NothingYouCouldDo-Regular.ttf",  76)
    fnt_tit = load_font("Lora-Bold.ttf",                  96)
    fnt_sub = load_font("Lora-BoldItalic.ttf",             50)
    fnt_det = load_font("Lora-Italic.ttf",                 42)
    fnt_cta = load_font("InstrumentSans-Bold.ttf",         42)
    fnt_br  = load_font("InstrumentSans-Bold.ttf",         36)

    # Flores topo
    for fx, col_o in [(66, (220, 185, 120)), (W - 66, (205, 168, 100))]:
        draw_flower(draw, fx, 96, petals=6, plen=14, pw=7,
                    col_out=col_o, col_mid=OURO_P, cr=5)
        draw_leaf(draw, fx - 12, 110, 225, 13, 5)
        draw_leaf(draw, fx + 12, 110, 315, 13, 5)

    cy = 520

    # Script
    cy = script_outlined_wrap(
        draw, "antes que junho feche.",
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
        draw, "garante o teu lugar.",
        fnt_tit, W - 80, cx, cy,
        fill=TXT, shadow=True, shd_col=(195, 178, 215), line_spacing=12
    ) + 20

    # Divisor
    draw.line([(cx - 100, cy), (cx + 100, cy)], fill=(160, 138, 175), width=1)
    cy += 30

    # Suporte
    cy = wrap_centered(
        draw, "a agenda da Oliete não para. e junho ainda nem começou.",
        fnt_det, W - 120, cx, cy,
        fill=(98, 78, 110), line_spacing=12
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

    lbl = "link disponivel no story"
    bb_l = draw.textbbox((0, 0), lbl, font=fnt_br)
    draw.text((cx - (bb_l[2] - bb_l[0]) // 2, cy),
              lbl, font=load_font("InstrumentSans-Bold.ttf", 28),
              fill=(140, 105, 70))

    # Flores base
    for fx in [66, W - 66]:
        draw_flower(draw, fx, H - 130, petals=6, plen=13, pw=6,
                    col_out=(210, 175, 100), col_mid=OURO_P, cr=5)

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 68),
              "Ok Delícias com Amor", font=fnt_br, fill=TXT_M)

    border(draw, col=OURO_S)
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio27", "story_maio27_3.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


if __name__ == "__main__":
    story_1()
    story_2()
    story_3()
    print("3 Stories 27/05 prontos.")
