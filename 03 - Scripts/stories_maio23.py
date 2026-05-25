# -*- coding: utf-8 -*-
"""
3 Stories Sabado Engajamento - Ok Delicias com Amor - 23/05/2026
Conceito: enquete leve de fim de semana + resposta com produto + bastidores entrega grande
Arc: pergunta > resposta produto > bastidores do dia
Fotos: story_1 sem foto (gradiente puro) | story_2 IMG_1139 (nova) | story_3 foto_drive_A (nova)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, os

BASE_DIR  = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR = (r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions"
             r"\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316"
             r"\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts")

CREME     = (255, 248, 234)
LAVANDA   = (230, 222, 248)
LAVANDA_M = (196, 181, 224)
LAVANDA_E = (158, 138, 200)
OURO      = (179, 138,  52)
OURO_S    = (210, 175, 100)
OURO_P    = (235, 210, 155)
ROSA      = (240, 208, 220)
VERDE     = (148, 172, 124)
VERDE_E   = (100, 130,  80)
TXT       = ( 32,  18,   6)
TXT_M     = ( 72,  50,  22)
ESCURO    = ( 20,  10,   2)

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
    if col is None:
        col = OURO_S
    draw.rounded_rectangle([16, 16, W - 16, H - 16], radius=32, outline=col, width=2)
    draw.rounded_rectangle([26, 26, W - 26, H - 26], radius=24, outline=OURO_P, width=1)


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


def foto_fundo(foto_path, overlay_alpha=200, overlay_color=None):
    if overlay_color is None:
        overlay_color = ESCURO
    foto = Image.open(foto_path).convert("RGB")
    foto = ImageEnhance.Brightness(foto).enhance(0.87)
    fw, fh = foto.size
    ratio  = W / H
    if fw / fh > ratio:
        nfw = int(fh * ratio)
        foto = foto.crop(((fw - nfw) // 2, 0, (fw + nfw) // 2, fh))
    else:
        nfh = int(fw / ratio)
        foto = foto.crop((0, (fh - nfh) // 2, fw, (fh + nfh) // 2))
    foto = foto.resize((W, H), Image.LANCZOS)
    ov   = Image.new("RGBA", (W, H), (*overlay_color, overlay_alpha))
    base = Image.alpha_composite(foto.convert("RGBA"), ov)
    return base.convert("RGB")


def wrap_centered(draw, text, font, max_w, cx, y, fill,
                  line_spacing=10, shadow=False, shd_col=(4, 2, 0)):
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
    if fill is None:
        fill = OURO_P
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


def c_text_shadow(draw, text, font, cx, y, fill, shd=4, shd_col=(4, 2, 0)):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    x  = cx - tw // 2
    draw.text((x + shd, y + shd), text, font=font, fill=shd_col)
    draw.text((x, y),             text, font=font, fill=fill)
    return y + th


# ── STORY 1: ENQUETE ─────────────────────────────────────────────────────────
# Fundo creme/lavanda, sem foto. Tom: leve, sábado, engajamento.
# O sticker de enquete real do Instagram vai sobre esta arte.
def story_1():
    img  = bg_grad(CREME, lerp(CREME, LAVANDA, 0.52))
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc  = load_font("NothingYouCouldDo-Regular.ttf", 68)
    fnt_tit = load_font("Lora-Bold.ttf",           78)
    fnt_btn = load_font("Lora-Bold.ttf",            68)
    fnt_det = load_font("InstrumentSans-Bold.ttf",  38)
    fnt_br  = load_font("InstrumentSans-Bold.ttf",  34)

    # Flores topo
    for fx, col_o in [(66, ROSA), (W - 66, LAVANDA_M)]:
        draw_flower(draw, fx, 96, petals=6, plen=16, pw=8,
                    col_out=col_o, col_mid=OURO_P, cr=6)
        draw_leaf(draw, fx - 14, 112, 225, 14, 6)
        draw_leaf(draw, fx + 14, 112, 315, 14, 6)

    cy = 450

    # Script topo — usa wrap para garantir que fica dentro do canvas
    cy = script_outlined_wrap(
        draw, "sábado de manhã...",
        fnt_sc, W - 160, cx, cy,
        fill=TXT_M, ol_col=(180, 150, 90), ol=2, line_sp=4
    ) + 24

    # Ornamento
    draw.line([(cx - 80, cy), (cx - 14, cy)], fill=OURO_S, width=2)
    draw.line([(cx + 14, cy), (cx + 80, cy)], fill=OURO_S, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 30

    # Pergunta principal
    cy = wrap_centered(draw, "você prefere",
                       fnt_tit, W - 100, cx, cy,
                       fill=TXT, shadow=True, line_spacing=8)
    cy = wrap_centered(draw, "festa com...",
                       fnt_tit, W - 100, cx, cy,
                       fill=TXT, shadow=True, line_spacing=8) + 42

    # --- Botão 1: SALGADO ---
    btn_w = W - 130
    btn_h = 138
    bx    = cx - btn_w // 2
    draw.rounded_rectangle(
        [bx + 4, cy + 4, bx + btn_w + 4, cy + btn_h + 4],
        radius=28, fill=(28, 14, 3)
    )
    draw.rounded_rectangle(
        [bx, cy, bx + btn_w, cy + btn_h],
        radius=28, fill=OURO, outline=OURO_P, width=2
    )
    bb1 = draw.textbbox((0, 0), "salgado", font=fnt_btn)
    bw1, bh1 = bb1[2] - bb1[0], bb1[3] - bb1[1]
    draw.text((cx - bw1 // 2, cy + (btn_h - bh1) // 2),
              "salgado", font=fnt_btn, fill=CREME)
    cy += btn_h + 20

    # --- Botão 2: DOCE ---
    draw.rounded_rectangle(
        [bx + 4, cy + 4, bx + btn_w + 4, cy + btn_h + 4],
        radius=28, fill=(28, 14, 3)
    )
    draw.rounded_rectangle(
        [bx, cy, bx + btn_w, cy + btn_h],
        radius=28, fill=LAVANDA_E, outline=LAVANDA_M, width=2
    )
    bb2 = draw.textbbox((0, 0), "doce", font=fnt_btn)
    bw2, bh2 = bb2[2] - bb2[0], bb2[3] - bb2[1]
    draw.text((cx - bw2 // 2, cy + (btn_h - bh2) // 2),
              "doce", font=fnt_btn, fill=CREME)
    cy += btn_h + 44

    # Teaser
    draw.line([(cx - 60, cy), (cx + 60, cy)], fill=OURO_P, width=1)
    cy += 24
    cy = wrap_centered(
        draw, "a Oli já tem a resposta.",
        fnt_det, W - 120, cx, cy,
        fill=TXT_M, line_spacing=8
    ) + 30

    # --- Ornamento floral central (sem foto — story e enquete, visual limpo) ---
    cy_fl = cy + 120
    # Flor grande no centro
    draw_flower(draw, cx, cy_fl, petals=8, plen=22, pw=9,
                col_out=ROSA, col_mid=OURO_P, cr=8)
    # Flores menores aos lados
    draw_flower(draw, cx - 84, cy_fl + 24, petals=6, plen=13, pw=6,
                col_out=LAVANDA_M, col_mid=OURO_P, cr=5)
    draw_flower(draw, cx + 84, cy_fl + 24, petals=6, plen=13, pw=6,
                col_out=LAVANDA_M, col_mid=OURO_P, cr=5)
    # Folhas
    draw_leaf(draw, cx - 32, cy_fl + 16, 220, 18, 7)
    draw_leaf(draw, cx + 32, cy_fl + 16, 320, 18, 7)
    draw_leaf(draw, cx - 68, cy_fl - 4, 175, 13, 5)
    draw_leaf(draw, cx + 68, cy_fl - 4, 5, 13, 5)
    # Diamantes decorativos
    diamond(draw, cx - 148, cy_fl, 5, OURO_P)
    diamond(draw, cx + 148, cy_fl, 5, OURO_P)
    # Linha ornamental sutil
    draw.line([(cx - 130, cy_fl + 54), (cx + 130, cy_fl + 54)],
              fill=OURO_P, width=1)

    # Seta apontando para o próximo story
    arr_y = cy_fl + 150
    draw.line([(cx, arr_y), (cx, arr_y + 42)], fill=OURO_S, width=2)
    diamond(draw, cx, arr_y + 46, 7, OURO_S)

    # Flores cantos inferiores — maiores e mais visíveis
    draw_flower(draw, 66,    H - 130, petals=6, plen=13, pw=6,
                col_out=ROSA, col_mid=OURO_P, cr=5)
    draw_flower(draw, W - 66, H - 130, petals=6, plen=13, pw=6,
                col_out=LAVANDA_M, col_mid=OURO_P, cr=5)

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 72),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO)

    border(draw)
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio23", "story_maio23_1.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ── STORY 2: RESPOSTA — produto em destaque ───────────────────────────────────
# Foto: IMG_1139 (3 empadinhas + panelinha esmaltada do gatinho — nova, nunca usada)
def story_2():
    img  = foto_fundo(os.path.join(BASE_DIR, "fotos", "IMG_8261.jpg"),
                      overlay_alpha=148, overlay_color=(12, 6, 1))
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc   = load_font("NothingYouCouldDo-Regular.ttf", 70)
    fnt_tit  = load_font("Lora-Bold.ttf",           108)
    fnt_body = load_font("Lora-BoldItalic.ttf",      50)
    fnt_det  = load_font("InstrumentSans-Bold.ttf",  40)
    fnt_br   = load_font("InstrumentSans-Bold.ttf",  34)

    # Flores topo
    for fx in [66, W - 66]:
        draw_flower(draw, fx, 92, petals=6, plen=14, pw=7,
                    col_out=(195, 175, 150), col_mid=OURO_P, cr=5)

    cy = H // 2 - 300

    # Script
    cy = script_outlined_wrap(
        draw, "a Oli respondeu.",
        fnt_sc, W - 130, cx, cy,
        fill=(232, 212, 180), line_sp=6
    ) + 20

    # Ornamento
    draw.line([(cx - 88, cy), (cx - 14, cy)], fill=OURO_S, width=2)
    draw.line([(cx + 14, cy), (cx + 88, cy)], fill=OURO_S, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 28

    # Titulo grande — resposta da enquete
    cy = c_text_shadow(draw, "salgado.", fnt_tit, cx, cy, fill=CREME, shd=5) + 22

    # Divisor
    draw.line([(cx - 70, cy), (cx + 70, cy)], fill=(100, 78, 40), width=2)
    cy += 26

    # Body — concordância: "feito" masculino (salgado)
    cy = wrap_centered(
        draw, "feito com amor, do início ao fim.",
        fnt_body, W - 120, cx, cy,
        fill=(215, 195, 160), shadow=True, line_spacing=8
    ) + 28

    # Detalhe
    cy = wrap_centered(
        draw, "cada pedido, com a atenção da Oliete.",
        fnt_det, W - 120, cx, cy,
        fill=OURO_S, line_spacing=8
    )

    # Seta
    arr_y = H - 220
    draw.line([(cx, arr_y), (cx, arr_y + 48)], fill=OURO_S, width=2)
    diamond(draw, cx, arr_y + 52, 7, OURO_S)

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 72),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO_S)

    border(draw, col=(100, 80, 50))
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio23", "story_maio23_2.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ── STORY 3: BASTIDORES — entrega grande do dia ───────────────────────────────
# Foto: foto_drive_A (salgados organizados na bandeja, producao — nova, nunca usada)
# PLACEHOLDER: atualizar com foto real da entrega quando o Fabricio trazer
def story_3():
    img  = foto_fundo(os.path.join(BASE_DIR, "fotos", "IMG_8263.jpg"),
                      overlay_alpha=165, overlay_color=(10, 5, 1))
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc   = load_font("NothingYouCouldDo-Regular.ttf", 70)
    fnt_tit  = load_font("Lora-Bold.ttf",           96)
    fnt_body = load_font("Lora-BoldItalic.ttf",     50)
    fnt_det  = load_font("InstrumentSans-Bold.ttf", 42)
    fnt_br   = load_font("InstrumentSans-Bold.ttf", 34)

    # Flores topo
    for fx in [66, W - 66]:
        draw_flower(draw, fx, 92, petals=6, plen=14, pw=7,
                    col_out=(190, 170, 145), col_mid=OURO_P, cr=5)

    cy = H // 2 - 290

    # Script
    cy = script_outlined_wrap(
        draw, "hoje cedo na cozinha.",
        fnt_sc, W - 130, cx, cy,
        fill=(232, 212, 178), line_sp=6
    ) + 20

    # Ornamento
    draw.line([(cx - 88, cy), (cx - 14, cy)], fill=OURO_S, width=2)
    draw.line([(cx + 14, cy), (cx + 88, cy)], fill=OURO_S, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 28

    # Titulo
    cy = c_text_shadow(draw, "tem entrega",  fnt_tit, cx, cy, fill=CREME,  shd=5) + 6
    cy = c_text_shadow(draw, "grande.",      fnt_tit, cx, cy, fill=OURO_P, shd=5) + 30

    # Divisor
    draw.line([(cx - 70, cy), (cx + 70, cy)], fill=(100, 78, 40), width=2)
    cy += 26

    # Body
    cy = wrap_centered(
        draw, "fica de olho nos próximos Stories.",
        fnt_body, W - 120, cx, cy,
        fill=(205, 185, 155), shadow=True, line_spacing=10
    ) + 28

    # Detalhe
    cy = wrap_centered(
        draw, "tudo preparado com carinho.",
        fnt_det, W - 120, cx, cy,
        fill=OURO_P, line_spacing=8
    )

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx - (br_b[2] - br_b[0]) // 2, H - 72),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO_S)

    border(draw, col=(90, 65, 30))
    out = os.path.join(BASE_DIR, "02 - Criativos", "maio23", "story_maio23_3.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


if __name__ == "__main__":
    story_1()
    story_2()
    story_3()
    print("\n3 Stories 23/05 prontos.")
