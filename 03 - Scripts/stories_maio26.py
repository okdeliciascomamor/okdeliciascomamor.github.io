# -*- coding: utf-8 -*-
"""
3 Stories Terça — Ok Delícias com Amor — 26/05/2026

Arc: enquete de cardápio — o seguidor decide
Story 1: Hook "hoje você decide." — gradiente, sem foto
Story 2: Batalha split screen Risoles vs Mini Hambúrguer — espaço pro poll sticker
Story 3: CTA "resultado amanhã. hoje, garante o seu."
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


def crop_half(path, target_w, target_h, enhance=True):
    """Carrega foto e faz cover-crop para target_w x target_h."""
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if enhance:
        img = ImageEnhance.Brightness(img).enhance(1.08)
        img = ImageEnhance.Color(img).enhance(1.14)
    ratio = max(target_w / img.width, target_h / img.height)
    nw    = int(img.width  * ratio)
    nh    = int(img.height * ratio)
    img   = img.resize((nw, nh), Image.LANCZOS)
    x_off = max(0, (nw - target_w) // 2)
    y_off = max(0, (nh - target_h) // 2)
    return img.crop((x_off, y_off, x_off + target_w, y_off + target_h))


# ─────────────────────────────────────────────────────────────────────────────
# STORY 1 — Hook: "hoje você decide."
# ─────────────────────────────────────────────────────────────────────────────
def story_1():
    img  = bg_grad(CREME, PESSEGO)
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc  = load_font("NothingYouCouldDo-Regular.ttf",  88)
    fnt_tit = load_font("Lora-Bold.ttf",                 100)
    fnt_sub = load_font("Lora-BoldItalic.ttf",            50)
    fnt_det = load_font("Lora-Italic.ttf",                42)
    fnt_br  = load_font("InstrumentSans-Bold.ttf",        36)

    # Flores topo
    for fx, col_o in [(66, (220, 185, 120)), (W - 66, (205, 168, 100))]:
        draw_flower(draw, fx, 96, petals=6, plen=14, pw=7,
                    col_out=col_o, col_mid=OURO_P, cr=5)
        draw_leaf(draw, fx - 12, 110, 225, 13, 5)
        draw_leaf(draw, fx + 12, 110, 315, 13, 5)

    cy = 560

    # Script
    cy = script_outlined_wrap(
        draw, "hoje você decide.",
        fnt_sc, W - 120, cx, cy,
        fill=OURO_S, ol_col=(180, 130, 40), ol=2, line_sp=4
    ) + 32

    # Ornamento
    draw.line([(cx - 90, cy), (cx - 16, cy)], fill=OURO, width=2)
    draw.line([(cx + 16, cy), (cx + 90, cy)], fill=OURO, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 44

    # Título
    cy = wrap_centered(
        draw, "qual sai no próximo pedido?",
        fnt_tit, W - 80, cx, cy,
        fill=TXT, shadow=True, shd_col=(210, 188, 148), line_spacing=12
    ) + 20

    # Divisor
    draw.line([(cx - 100, cy), (cx + 100, cy)], fill=(195, 168, 105), width=1)
    cy += 30

    # Subtítulo
    cy = wrap_centered(
        draw, "dois favoritos. um voto. você escolhe.",
        fnt_sub, W - 100, cx, cy,
        fill=TXT_M, line_spacing=12
    ) + 20

    # Detalhe
    wrap_centered(
        draw, "veja o próximo story e vote.",
        fnt_det, W - 140, cx, cy,
        fill=(140, 100, 55), line_spacing=10
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
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio26", "story_maio26_1.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 2 — Batalha split screen: Risoles vs Mini Hambúrguer
# Espaço inferior reservado para poll sticker do Instagram
# ─────────────────────────────────────────────────────────────────────────────
def story_2():
    HALF     = W // 2          # 540
    FOTO_H   = 1340            # altura da zona de foto (deixa 580px p/ poll+marca)
    OVL_DARK = (12, 5, 1)

    path_a = os.path.join(BASE_DIR, "fotos", "IMG_1049.JPEG")
    path_b = os.path.join(BASE_DIR, "fotos",
                          "WhatsApp_Image_2026-05-05_at_16.52.18_(1).jpeg")

    # Canvas base escuro
    img  = Image.new("RGB", (W, H), (18, 8, 2))
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    # --- Foto esquerda: Risoles (IMG_1049) ---
    foto_a = crop_half(path_a, HALF, FOTO_H)
    ov_a   = Image.new("RGBA", (HALF, FOTO_H), OVL_DARK + (155,))
    fa     = foto_a.convert("RGBA")
    fa.alpha_composite(ov_a)
    img.paste(fa.convert("RGB"), (0, 0))

    # --- Foto direita: Mini Hambúrguer ---
    foto_b = crop_half(path_b, HALF, FOTO_H)
    ov_b   = Image.new("RGBA", (HALF, FOTO_H), OVL_DARK + (140,))
    fb     = foto_b.convert("RGBA")
    fb.alpha_composite(ov_b)
    img.paste(fb.convert("RGB"), (HALF, 0))

    # Linha divisória dourada
    draw.line([(HALF, 0), (HALF, FOTO_H)], fill=OURO, width=3)

    # Badge VS central
    vs_y = FOTO_H // 2
    draw.ellipse([cx - 52, vs_y - 52, cx + 52, vs_y + 52], fill=(18, 8, 2))
    draw.ellipse([cx - 48, vs_y - 48, cx + 48, vs_y + 48], fill=OURO)
    fnt_vs = load_font("Lora-Bold.ttf", 44)
    bb = draw.textbbox((0, 0), "VS", font=fnt_vs)
    draw.text((cx - (bb[2] - bb[0]) // 2, vs_y - (bb[3] - bb[1]) // 2),
              "VS", font=fnt_vs, fill=BRANCO)

    fnt_sc   = load_font("NothingYouCouldDo-Regular.ttf", 62)
    fnt_nome = load_font("Lora-Bold.ttf",                 56)
    fnt_sub  = load_font("Lora-BoldItalic.ttf",           40)
    fnt_poll = load_font("InstrumentSans-Bold.ttf",        34)
    fnt_br   = load_font("InstrumentSans-Bold.ttf",        34)

    # Pergunta no topo (sobre as fotos)
    cy_top = 80
    cy_top = script_outlined_wrap(
        draw, "qual você pediria agora?",
        fnt_sc, W - 80, cx, cy_top,
        fill=OURO_P, ol_col=(10, 4, 1), ol=2, line_sp=4
    )

    # Nomes dos produtos em cada metade
    nome_y = FOTO_H - 200
    # Lado A — Risoles
    bb_a = draw.textbbox((0, 0), "risoles", font=fnt_nome)
    draw.text((HALF // 2 - (bb_a[2] - bb_a[0]) // 2, nome_y),
              "risoles", font=fnt_nome, fill=BRANCO)
    bb_a2 = draw.textbbox((0, 0), "o mais pedido", font=fnt_sub)
    draw.text((HALF // 2 - (bb_a2[2] - bb_a2[0]) // 2, nome_y + 68),
              "o mais pedido", font=fnt_sub, fill=OURO_P)

    # Lado B — Mini Hambúrguer
    bb_b = draw.textbbox((0, 0), "mini hambúrguer", font=fnt_nome)
    draw.text((HALF + HALF // 2 - (bb_b[2] - bb_b[0]) // 2, nome_y),
              "mini hambúrguer", font=fnt_nome, fill=BRANCO)
    bb_b2 = draw.textbbox((0, 0), "o novo destaque", font=fnt_sub)
    draw.text((HALF + HALF // 2 - (bb_b2[2] - bb_b2[0]) // 2, nome_y + 68),
              "o novo destaque", font=fnt_sub, fill=OURO_P)

    # Zona inferior — preenche fundo creme e faz gradiente suave
    poll_y = FOTO_H
    draw.rectangle([0, poll_y, W - 1, H - 1], fill=CREME)
    for gy in range(100):
        t = gy / 100
        draw.line([(0, poll_y + gy), (W, poll_y + gy)],
                  fill=lerp((18, 8, 2), CREME, t))

    # Instrução — legível no fundo claro, gramaticalmente correta
    fnt_poll_lg = load_font("InstrumentSans-Bold.ttf", 40)
    inst_y = poll_y + 130
    inst = "use a enquete abaixo para votar"
    bb_i = draw.textbbox((0, 0), inst, font=fnt_poll_lg)
    iw = bb_i[2] - bb_i[0]
    ih = bb_i[3] - bb_i[1]
    draw.text((cx - iw // 2, inst_y), inst, font=fnt_poll_lg, fill=TXT)

    # Seta apontando pra baixo (sticker vai abaixo)
    arr_cx = cx
    arr_y_top = inst_y + ih + 22
    draw.polygon(
        [(arr_cx - 20, arr_y_top),
         (arr_cx + 20, arr_y_top),
         (arr_cx,      arr_y_top + 32)],
        fill=OURO
    )

    # Ornamento separador antes da marca
    orn_y = H - 108
    draw.line([(cx - 80, orn_y), (cx - 12, orn_y)], fill=OURO_S, width=1)
    draw.line([(cx + 12, orn_y), (cx + 80, orn_y)], fill=OURO_S, width=1)
    diamond(draw, cx, orn_y, 5, OURO_S)

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 72),
              "Ok Delícias com Amor", font=fnt_br, fill=TXT_M)

    border(draw, col=OURO_S)
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio26", "story_maio26_2.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 3 — CTA: "resultado amanhã. hoje, garante o seu."
# ─────────────────────────────────────────────────────────────────────────────
def story_3():
    img  = bg_grad(PESSEGO, CREME)
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

    cy = 540

    # Script
    cy = script_outlined_wrap(
        draw, "resultado amanhã.",
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
        draw, "hoje, garante o seu.",
        fnt_tit, W - 80, cx, cy,
        fill=TXT, shadow=True, shd_col=(210, 188, 148), line_spacing=12
    ) + 20

    # Divisor
    draw.line([(cx - 100, cy), (cx + 100, cy)], fill=(195, 168, 105), width=1)
    cy += 30

    # Suporte
    cy = wrap_centered(
        draw, "enquanto o resultado não sai, a agenda da Oliete segue enchendo.",
        fnt_det, W - 120, cx, cy,
        fill=(110, 78, 38), line_spacing=12
    ) + 44

    # CTA box — link sticker vai em cima
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
              lbl, font=load_font("InstrumentSans-Bold.ttf", 28), fill=(150, 110, 55))

    # Flores base
    for fx in [66, W - 66]:
        draw_flower(draw, fx, H - 130, petals=6, plen=13, pw=6,
                    col_out=(210, 175, 100), col_mid=OURO_P, cr=5)

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 68),
              "Ok Delícias com Amor", font=fnt_br, fill=TXT_M)

    border(draw, col=OURO_S)
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio26", "story_maio26_3.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


if __name__ == "__main__":
    story_1()
    story_2()
    story_3()
    print("3 Stories 26/05 prontos.")
