# -*- coding: utf-8 -*-
"""
5 Stories Sábado — Ok Delícias com Amor — 30/05/2026

Conceito: BASTIDORES — produção da canoinha de legumes, do ingrediente fresco
ao produto pronto. Paga a promessa de ontem ("feito à mão, feito na hora")
mostrando o processo num sábado de entrega.

Story 1: HOOK       — "tudo fresco." (ingredientes juntos, abertura)
Story 2: LEGUMES     — "os legumes." (brócolis e cenoura fresquinhos)
Story 3: MOLHO       — "molho branco." (feito do zero)
Story 4: MONTAGEM     — "recheada na mão." (forminha de florzinha)
Story 5: PRONTO + CTA — "feito na hora." (canoinha dourada, entrega de hoje)

Cada story com paleta própria (creme, verde, lavanda, pêssego, dourado),
coesos pela mesma moldura, flores de canto, rodapé e indicador de progresso.
Sem travessão. Sem a palavra "caixa". Cada foto usada uma única vez.
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter
import math, os

BASE_DIR  = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
MAT_DIR   = os.path.join(BASE_DIR, "Material 30.05")
FONTS_DIR = (r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions"
             r"\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316"
             r"\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts")

CREME      = (255, 248, 234)
CREME_F    = (252, 240, 218)
PESSEGO    = (255, 232, 192)
PESSEGO_Q  = (250, 215, 170)
AMBAR      = (248, 198, 142)
BEGE       = (242, 220, 188)
BEGE_E     = (220, 192, 150)
LAVANDA    = (232, 222, 244)
LAVANDA_E  = (210, 196, 230)
OURO       = (179, 138,  52)
OURO_S     = (210, 175, 100)
OURO_P     = (235, 210, 155)
TERRA      = (138,  82,  48)
LILAS_E    = (118,  92, 158)
# Verde sálvia
VERDE_BG1  = (236, 242, 230)
VERDE_BG2  = (198, 218, 192)
MUSGO      = ( 92, 120,  72)
VERDE_S    = (140, 168, 110)
VERDE_BORD = (170, 195, 150)
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


def arrow_right(draw, x, y, length, color, width=2, head=8):
    draw.line([(x, y), (x + length - head, y)], fill=color, width=width)
    draw.polygon([(x + length - head, y - head // 1.5),
                  (x + length - head, y + head // 1.5),
                  (x + length, y)], fill=color)


def crop_cover(path, tw, th, focus_x=0.5, focus_y=0.5):
    """Cover-crop pra preencher tw x th sem distorcer. focus_* desloca o recorte."""
    img = Image.open(path).convert("RGB")
    ratio = max(tw / img.width, th / img.height)
    nw, nh = int(img.width * ratio) + 1, int(img.height * ratio) + 1
    img = img.resize((nw, nh), Image.LANCZOS)
    left = int(max(0, min(nw - tw, (nw - tw) * focus_x)))
    top  = int(max(0, min(nh - th, (nh - th) * focus_y)))
    return img.crop((left, top, left + tw, top + th))


def framed_photo(img, path, pw, ph, px, py, rad=28, focus_x=0.5, focus_y=0.5,
                 frame_col=OURO_S, frame_in=(150, 110, 35), shadow_a=(90, 60, 25, 90)):
    """Cola uma foto cover-crop com cantos arredondados, sombra suave e moldura dupla.
    Retorna o novo img (alpha_composite gera nova imagem)."""
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([px, py + 14, px + pw, py + ph + 14], radius=rad, fill=shadow_a)
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")

    photo = crop_cover(path, pw, ph, focus_x, focus_y)
    mask = Image.new("L", (pw, ph), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, pw, ph], radius=rad, fill=255)
    img.paste(photo, (px, py), mask)

    d = ImageDraw.Draw(img)
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=rad, outline=frame_col, width=3)
    d.rounded_rectangle([px + 7, py + 7, px + pw - 7, py + ph - 7], radius=rad - 6,
                        outline=frame_in, width=1)
    return img


def photo_badge(draw, txt, px, py, ph, fill, outline, text_col=BRANCO):
    """Selo pílula no canto inferior-esquerdo da foto."""
    fnt = load_font("InstrumentSans-Bold.ttf", 30)
    bb = draw.textbbox((0, 0), txt, font=fnt)
    sw = bb[2] - bb[0] + 48
    sh = bb[3] - bb[1] + 20
    sx = px + 24
    sy = py + ph - sh - 24
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=sh // 2,
                           fill=fill, outline=outline, width=2)
    draw.text((sx + (sw - (bb[2] - bb[0])) // 2, sy + (sh - (bb[3] - bb[1])) // 2 - 2),
              txt, font=fnt, fill=text_col)


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


def progress_indicator(draw, idx, total=5, accent=None):
    if accent is None: accent = OURO
    fnt = load_font("InstrumentSans-Bold.ttf", 36)
    prog = f"{idx:02d} / {total:02d}"
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


def kicker_ornamento(draw, cx, cy, acc):
    draw.line([(cx - 100, cy), (cx - 16, cy)], fill=acc, width=2)
    draw.line([(cx + 16, cy), (cx + 100, cy)], fill=acc, width=2)
    diamond(draw, cx, cy, 6, acc)


def hint_arrasta(draw, cx, txt, col):
    fnt = load_font("Lora-Italic.ttf", 38)
    bb = draw.textbbox((0, 0), txt, font=fnt)
    hnw = bb[2] - bb[0]
    hnh = bb[3] - bb[1]
    hy  = H - 360
    htx = cx - (hnw + 56) // 2
    draw.text((htx, hy), txt, font=fnt, fill=col)
    arrow_right(draw, htx + hnw + 16, hy + hnh // 2 + 2, 42, col, 2, 12)


def salvar(img, nome):
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio30", nome)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 1 — HOOK: "tudo fresco." — creme, ingredientes juntos
# ─────────────────────────────────────────────────────────────────────────────
def story_1_hook():
    cx  = W // 2
    ACC = OURO
    img = bg_grad(CREME, CREME_F)
    img = framed_photo(img, os.path.join(MAT_DIR, "Ingredientes Frescos Canoinha de legumes.jpeg"),
                       860, 760, 110, 250, focus_y=0.5)
    draw = ImageDraw.Draw(img)
    topo_flores(draw)
    photo_badge(draw, "fresquinho", 110, 250, 760, OURO, OURO_P)

    cy = 250 + 760 + 54
    cy = wrap_centered(draw, "sábado é dia de bastidor,",
                       load_font("CormorantGaramond-SemiBoldItalic.ttf", 72),
                       W - 130, cx, cy, fill=OURO, line_spacing=6) + 16
    cy = wrap_centered(draw, "tudo fresco.", load_font("Lora-Bold.ttf", 108),
                       W - 100, cx, cy, fill=TXT, shadow=True,
                       shd_col=(232, 214, 178), line_spacing=8) + 40
    draw.line([(cx - 200, cy), (cx + 200, cy)], fill=ACC, width=2)
    cy += 34
    wrap_centered(draw, "a canoinha de legumes nasce de ingrediente de verdade.",
                  load_font("Lora-Italic.ttf", 42), W - 150, cx, cy,
                  fill=TXT_M, line_spacing=12)

    hint_arrasta(draw, cx, "vem ver de perto", (150, 110, 55))
    progress_indicator(draw, 1, 5, ACC)
    base_flores(draw)
    marca_rodape(draw)
    border(draw, col=OURO_S)
    salvar(img, "story_maio30_1.png")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 2 — LEGUMES: "os legumes." — verde sálvia, brócolis e cenoura
# ─────────────────────────────────────────────────────────────────────────────
def story_2_legumes():
    cx  = W // 2
    ACC = MUSGO
    img = bg_grad(VERDE_BG1, VERDE_BG2)
    img = framed_photo(img, os.path.join(MAT_DIR, "Brócolis e Cenouta Fresquinhos.jpeg"),
                       860, 760, 110, 250, focus_y=0.5,
                       frame_col=(150, 180, 120), frame_in=(90, 118, 70),
                       shadow_a=(60, 80, 45, 90))
    draw = ImageDraw.Draw(img)
    topo_flores(draw, col_a=(178, 202, 150), col_b=(165, 190, 135))
    photo_badge(draw, "do dia", 110, 250, 760, MUSGO, (150, 180, 120))

    cy = 250 + 760 + 54
    cy = wrap_centered(draw, "primeiro,",
                       load_font("CormorantGaramond-SemiBoldItalic.ttf", 72),
                       W - 130, cx, cy, fill=MUSGO, line_spacing=6) + 16
    cy = wrap_centered(draw, "os legumes.", load_font("Lora-Bold.ttf", 108),
                       W - 100, cx, cy, fill=TXT, shadow=True,
                       shd_col=(202, 218, 190), line_spacing=8) + 40
    draw.line([(cx - 200, cy), (cx + 200, cy)], fill=ACC, width=2)
    cy += 34
    wrap_centered(draw, "brócolis e cenoura fresquinhos, escolhidos um a um.",
                  load_font("Lora-Italic.ttf", 42), W - 150, cx, cy,
                  fill=(70, 92, 54), line_spacing=12)

    hint_arrasta(draw, cx, "tem mais por vir", (88, 116, 68))
    progress_indicator(draw, 2, 5, ACC)
    base_flores(draw, col_out=(165, 190, 135))
    marca_rodape(draw)
    border(draw, col=VERDE_BORD)
    salvar(img, "story_maio30_2.png")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 3 — MOLHO: "molho branco." — lavanda, molho do zero
# ─────────────────────────────────────────────────────────────────────────────
def story_3_molho():
    cx  = W // 2
    ACC = LILAS_E
    img = bg_grad(CREME, LAVANDA)
    img = framed_photo(img, os.path.join(MAT_DIR, "Molho Branco.jpeg"),
                       860, 760, 110, 250, focus_y=0.55,
                       frame_col=(190, 172, 215), frame_in=(120, 95, 160),
                       shadow_a=(80, 65, 110, 85))
    draw = ImageDraw.Draw(img)
    topo_flores(draw, col_a=(200, 180, 220), col_b=(190, 168, 215))
    photo_badge(draw, "do zero", 110, 250, 760, LILAS_E, (190, 172, 215))

    cy = 250 + 760 + 54
    cy = wrap_centered(draw, "o que une tudo,",
                       load_font("CormorantGaramond-SemiBoldItalic.ttf", 72),
                       W - 130, cx, cy, fill=LILAS_E, line_spacing=6) + 16
    cy = wrap_centered(draw, "molho branco.", load_font("Lora-Bold.ttf", 100),
                       W - 100, cx, cy, fill=TXT, shadow=True,
                       shd_col=(205, 192, 226), line_spacing=8) + 40
    draw.line([(cx - 200, cy), (cx + 200, cy)], fill=ACC, width=2)
    cy += 34
    wrap_centered(draw, "feito do zero, na panela, bem cremoso.",
                  load_font("Lora-Italic.ttf", 42), W - 150, cx, cy,
                  fill=(92, 70, 120), line_spacing=12)

    hint_arrasta(draw, cx, "agora junta tudo", (120, 95, 160))
    progress_indicator(draw, 3, 5, ACC)
    base_flores(draw, col_out=(190, 168, 215))
    marca_rodape(draw)
    border(draw, col=LAVANDA_E)
    salvar(img, "story_maio30_3.png")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 4 — MONTAGEM: "recheada na mão." — pêssego, forminha de florzinha
# ─────────────────────────────────────────────────────────────────────────────
def story_4_montagem():
    cx  = W // 2
    ACC = TERRA
    img = bg_grad(PESSEGO, PESSEGO_Q)
    img = framed_photo(img, os.path.join(MAT_DIR, "Canoinha de legumes 4.jpeg"),
                       860, 760, 110, 250, focus_y=0.35,
                       frame_col=OURO_S, frame_in=TERRA,
                       shadow_a=(90, 55, 30, 90))
    draw = ImageDraw.Draw(img)
    topo_flores(draw, col_a=(232, 180, 140), col_b=(225, 168, 120))
    photo_badge(draw, "à mão", 110, 250, 760, TERRA, OURO_S)

    cy = 250 + 760 + 54
    cy = wrap_centered(draw, "depois,",
                       load_font("CormorantGaramond-SemiBoldItalic.ttf", 72),
                       W - 130, cx, cy, fill=TERRA, line_spacing=6) + 16
    cy = wrap_centered(draw, "recheada na mão.", load_font("Lora-Bold.ttf", 92),
                       W - 100, cx, cy, fill=TXT, shadow=True,
                       shd_col=(235, 205, 165), line_spacing=8) + 40
    draw.line([(cx - 200, cy), (cx + 200, cy)], fill=ACC, width=2)
    cy += 34
    wrap_centered(draw, "uma a uma, em forminha de florzinha, com calma.",
                  load_font("Lora-Italic.ttf", 42), W - 150, cx, cy,
                  fill=(120, 75, 45), line_spacing=12)

    hint_arrasta(draw, cx, "e o resultado é esse", (150, 100, 60))
    progress_indicator(draw, 4, 5, ACC)
    base_flores(draw, col_out=(225, 175, 120))
    marca_rodape(draw)
    border(draw, col=BEGE_E)
    salvar(img, "story_maio30_4.png")


# ─────────────────────────────────────────────────────────────────────────────
# STORY 5 — PRONTO + CTA: "feito na hora." — dourado, entrega de hoje
# ─────────────────────────────────────────────────────────────────────────────
def story_5_pronto():
    cx  = W // 2
    ACC = OURO
    img = bg_grad(PESSEGO, AMBAR)
    img = framed_photo(img, os.path.join(MAT_DIR, "Canoinha de legumes.jpeg"),
                       860, 680, 110, 230, focus_y=0.5,
                       frame_col=OURO_S, frame_in=(150, 110, 35),
                       shadow_a=(90, 60, 25, 95))
    draw = ImageDraw.Draw(img)
    topo_flores(draw)
    photo_badge(draw, "na hora", 110, 230, 680, OURO, OURO_P)

    cy = 230 + 680 + 48
    cy = wrap_centered(draw, "e tá pronta:",
                       load_font("CormorantGaramond-SemiBoldItalic.ttf", 72),
                       W - 130, cx, cy, fill=OURO, line_spacing=6) + 14
    cy = wrap_centered(draw, "feito na hora.", load_font("Lora-Bold.ttf", 100),
                       W - 100, cx, cy, fill=TXT, shadow=True,
                       shd_col=(225, 180, 120), line_spacing=8) + 36
    cy = wrap_centered(draw, "canoinha de legumes fresquinha, saindo hoje na entrega.",
                       load_font("Lora-Italic.ttf", 42), W - 150, cx, cy,
                       fill=(110, 78, 38), line_spacing=12) + 44

    # CTA
    cta_text = "chama no direct e garante a tua"
    fnt_cta = load_font("InstrumentSans-Bold.ttf", 38)
    cta_w, cta_h, r = 800, 100, 20
    cta_x = cx - cta_w // 2
    draw.rounded_rectangle([cta_x, cy, cta_x + cta_w, cy + cta_h],
                           radius=r, fill=OURO, outline=OURO_P, width=2)
    bb = draw.textbbox((0, 0), cta_text, font=fnt_cta)
    draw.text((cx - (bb[2] - bb[0]) // 2, cy + (cta_h - (bb[3] - bb[1])) // 2 - 2),
              cta_text, font=fnt_cta, fill=BRANCO)
    cy += cta_h + 14

    lbl = "entrega de sábado"
    fnt_lbl = load_font("InstrumentSans-Bold.ttf", 34)
    bb_l = draw.textbbox((0, 0), lbl, font=fnt_lbl)
    draw.text((cx - (bb_l[2] - bb_l[0]) // 2, cy + 6), lbl, font=fnt_lbl, fill=(150, 110, 55))

    progress_indicator(draw, 5, 5, ACC)
    base_flores(draw)
    marca_rodape(draw)
    border(draw, col=OURO_S)
    salvar(img, "story_maio30_5.png")


if __name__ == "__main__":
    story_1_hook()
    story_2_legumes()
    story_3_molho()
    story_4_montagem()
    story_5_pronto()
    print("5 Stories 30/05 prontos.")
