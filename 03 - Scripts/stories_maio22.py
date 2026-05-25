"""
3 Stories Urgência Junho — Ok Delícias com Amor — 22/05/2026
Conceito: datas de junho fechando, urgência com a calma e carinho da Oliete.
Arc: gancho suave > processo artesanal como razão > CTA direto
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, os

BASE_DIR  = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR = r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts"

CREME     = (255, 248, 234)
LAVANDA   = (230, 222, 248)
LAVANDA_M = (196, 181, 224)
LAVANDA_E = (158, 138, 200)
OURO      = (179, 138, 52)
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
    except:
        return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def bg_grad(top, bot):
    img = Image.new("RGB", (W, H), top)
    d   = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W-1, y)], fill=lerp(top, bot, y/(H-1)))
    return img


def border(draw, col=None):
    if col is None:
        col = OURO_S
    draw.rounded_rectangle([16, 16, W-16, H-16], radius=32, outline=col, width=2)
    draw.rounded_rectangle([26, 26, W-26, H-26], radius=24, outline=OURO_P, width=1)


def draw_petal(draw, cx, cy, angle_deg, length, width, color):
    a  = math.radians(angle_deg)
    px, py = cx + length*math.cos(a), cy + length*math.sin(a)
    p  = math.radians(angle_deg + 90)
    ox, oy = (width/2)*math.cos(p), (width/2)*math.sin(p)
    draw.polygon([(cx+ox, cy+oy), (px+ox*.3, py+oy*.3), (px, py),
                   (px-ox*.3, py-oy*.3), (cx-ox, cy-oy)], fill=color)


def draw_flower(draw, cx, cy, petals=6, plen=12, pw=6, col_out=None, col_mid=None, cr=4):
    if col_out is None: col_out = ROSA
    if col_mid is None: col_mid = OURO_P
    for i in range(petals):
        draw_petal(draw, cx, cy, 360/petals*i, plen, pw, col_out)
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=col_mid)


def draw_leaf(draw, cx, cy, angle_deg, length=12, width=5):
    draw_petal(draw, cx, cy, angle_deg,       length,     width,    VERDE)
    draw_petal(draw, cx, cy, angle_deg + 180, length*.4,  width*.5, VERDE_E)


def diamond(draw, cx, cy, size, color):
    draw.polygon([(cx, cy-size), (cx+size, cy), (cx, cy+size), (cx-size, cy)], fill=color)


def foto_fundo(foto_path, overlay_alpha=200, overlay_color=None):
    if overlay_color is None:
        overlay_color = ESCURO
    foto = Image.open(foto_path).convert("RGB")
    foto = ImageEnhance.Brightness(foto).enhance(0.85)
    fw, fh = foto.size
    ratio  = W / H
    if fw / fh > ratio:
        nfw = int(fh * ratio)
        foto = foto.crop(((fw-nfw)//2, 0, (fw+nfw)//2, fh))
    else:
        nfh = int(fw / ratio)
        foto = foto.crop((0, (fh-nfh)//2, fw, (fh+nfh)//2))
    foto = foto.resize((W, H), Image.LANCZOS)
    ov   = Image.new("RGBA", (W, H), (*overlay_color, overlay_alpha))
    base = Image.alpha_composite(foto.convert("RGBA"), ov)
    return base.convert("RGB")


def wrap_centered(draw, text, font, max_w, cx, y, fill,
                  line_spacing=10, shadow=False, shd_col=(4, 2, 0)):
    words = text.split()
    lines = []
    cur   = ""
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
            draw.text((x+3, y+3), line, font=font, fill=shd_col)
        draw.text((x, y), line, font=font, fill=fill)
        y += (bb[3] - bb[1]) + line_spacing
    return y


def script_outlined_wrap(draw, text, font, max_w, cx, y,
                          fill=None, ol_col=(5, 2, 0), ol=2, line_sp=8):
    if fill is None:
        fill = OURO_P
    words = text.split()
    lines = []
    cur   = ""
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
                    draw.text((x+dx, y+dy), line, font=font, fill=ol_col)
        draw.text((x, y), line, font=font, fill=fill)
        y += th + line_sp
    return y


def c_text_shadow(draw, text, font, cx, y, fill, shd=4, shd_col=(4, 2, 0)):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    x  = cx - tw // 2
    draw.text((x+shd, y+shd), text, font=font, fill=shd_col)
    draw.text((x, y), text, font=font, fill=fill)
    return y + th


# ── STORY 1: GANCHO — junho chegando ────────────────────────────────────────
# Foto escura, texto impactante, tom suave
def story_1():
    img  = foto_fundo(os.path.join(BASE_DIR, "fotos", "IMG_1049.JPEG"),
                      overlay_alpha=205, overlay_color=(10, 5, 1))
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc   = load_font("NothingYouCouldDo-Regular.ttf", 72)
    fnt_tit  = load_font("Lora-Bold.ttf",          96)
    fnt_body = load_font("Lora-BoldItalic.ttf",     52)
    fnt_det  = load_font("InstrumentSans-Bold.ttf", 40)
    fnt_br   = load_font("InstrumentSans-Bold.ttf", 34)

    draw_flower(draw, 66,   90, petals=6, plen=14, pw=7,
                col_out=(200, 180, 160), col_mid=OURO_P, cr=5)
    draw_flower(draw, W-66, 90, petals=6, plen=14, pw=7,
                col_out=(200, 180, 160), col_mid=OURO_P, cr=5)

    # Bloco central
    cy = H // 2 - 310

    # Script gancho
    cy = script_outlined_wrap(draw, "junho ta chegando",
                               fnt_sc, W-130, cx, cy,
                               fill=OURO_P, line_sp=6) + 18

    draw.line([(cx-80, cy), (cx+80, cy)], fill=OURO_S, width=2)
    cy += 28

    # Título com wrap
    cy = wrap_centered(draw, "você já sabe o que vai servir?",
                        fnt_tit, W-100, cx, cy,
                        fill=CREME, shadow=True, line_spacing=10)
    cy += 32

    # Divisor
    draw.line([(cx-60, cy), (cx+60, cy)], fill=OURO_S, width=1)
    cy += 26

    # Body
    cy = wrap_centered(draw, "a agenda da Oliete ta quase cheia.",
                        fnt_body, W-120, cx, cy,
                        fill=(220, 202, 178), shadow=True, line_spacing=8)
    cy += 32

    # Detalhe em ouro
    det = "mas ainda tem data disponível."
    det_b = draw.textbbox((0, 0), det, font=fnt_det)
    draw.text((cx-(det_b[2]-det_b[0])//2+3, cy+3), det, font=fnt_det, fill=(4, 2, 0))
    draw.text((cx-(det_b[2]-det_b[0])//2,   cy),   det, font=fnt_det, fill=OURO_P)

    # Seta para próxima story
    arr_y = H - 220
    draw.line([(cx, arr_y), (cx, arr_y+54)], fill=OURO_S, width=2)
    diamond(draw, cx, arr_y+58, 8, OURO_S)

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx-(br_b[2]-br_b[0])//2, H-72),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO_S)

    border(draw, col=(100, 80, 50))
    out = os.path.join(BASE_DIR, "story_maio22_1.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ── STORY 2: PROCESSO — a razão artesanal da urgência ───────────────────────
# Fundo claro, foto em arco, explica por que datas fecham cedo
def story_2():
    img  = bg_grad(CREME, lerp(CREME, LAVANDA, 0.48))
    cx   = W // 2

    arch_w = 860; arch_h = 860; top_y = 272

    foto = Image.open(os.path.join(BASE_DIR, "fotos", "foto_drive_B.jpg")).convert("RGB")
    foto = ImageEnhance.Brightness(foto).enhance(1.06)
    foto = ImageEnhance.Color(foto).enhance(1.18)
    fw, fh = foto.size
    # Crop quadrado centralizado
    side = min(fw, fh)
    foto = foto.crop(((fw-side)//2, (fh-side)//2, (fw+side)//2, (fh+side)//2))
    foto = foto.resize((arch_w, arch_h), Image.LANCZOS)

    mask = Image.new("L", (arch_w, arch_h), 0)
    md   = ImageDraw.Draw(mask)
    r    = arch_w // 2
    md.rectangle([0, r, arch_w, arch_h], fill=255)
    md.ellipse([0, 0, arch_w, arch_w], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(3))

    foto_rgba = Image.new("RGBA", (arch_w, arch_h), (0, 0, 0, 0))
    foto_rgba.paste(foto, (0, 0))
    foto_rgba.putalpha(mask)
    lx = cx - arch_w // 2
    img.paste(foto_rgba.convert("RGB"), (lx, top_y), mask=foto_rgba.split()[3])

    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([lx-2, top_y-2, lx+arch_w+2, top_y+arch_h+2],
                            radius=r+2, outline=OURO_S, width=2)

    fnt_sc   = load_font("NothingYouCouldDo-Regular.ttf", 76)
    fnt_tit  = load_font("Lora-Bold.ttf",          88)
    fnt_body = load_font("Lora-BoldItalic.ttf",     50)
    fnt_det  = load_font("InstrumentSans-Bold.ttf", 38)
    fnt_br   = load_font("InstrumentSans-Bold.ttf", 34)

    # Flores nos cantos
    for fx, col_o in [(66, ROSA), (W-66, LAVANDA_M)]:
        draw_flower(draw, fx, 96, petals=6, plen=16, pw=8,
                    col_out=col_o, col_mid=OURO_P, cr=6)
        draw_leaf(draw, fx-14, 112, 225, 14, 6)
        draw_leaf(draw, fx+14, 112, 315, 14, 6)

    # Script topo — usa wrap pra não sair do canvas
    sc_y = 138
    script_outlined_wrap(draw, "feita com atenção",
                          fnt_sc, W - 160, cx, sc_y,
                          fill=TXT_M, ol_col=(180, 150, 90), ol=2, line_sp=4)

    base_y = top_y + arch_h + 46

    # Ornamento
    draw.line([(cx-88, base_y-8), (cx-14, base_y-8)], fill=OURO_S, width=2)
    draw.line([(cx+14, base_y-8), (cx+88, base_y-8)], fill=OURO_S, width=2)
    diamond(draw, cx, base_y-8, 6, OURO)

    # Título linha 1 — escuro
    base_y = wrap_centered(draw, "cada salgado",
                            fnt_tit, W-100, cx, base_y,
                            fill=TXT, shadow=True, line_spacing=8)
    base_y += 4

    # Título linha 2 — dourado
    base_y = wrap_centered(draw, "feito com atenção de verdade.",
                            fnt_tit, W-100, cx, base_y,
                            fill=OURO, shadow=False, line_spacing=8)
    base_y += 28

    draw.line([(cx-60, base_y), (cx+60, base_y)], fill=OURO_P, width=2)
    base_y += 24

    # Body
    base_y = wrap_centered(draw, "por isso a Oliete não abre datas sem fim.",
                            fnt_body, W-120, cx, base_y,
                            fill=TXT_M, shadow=False, line_spacing=8)
    base_y += 16

    # Detalhe
    det_b = draw.textbbox((0, 0), "por isso as encomendas fecham cedo.", font=fnt_det)
    draw.text((cx-(det_b[2]-det_b[0])//2, base_y),
              "por isso as encomendas fecham cedo.", font=fnt_det, fill=TXT_M)

    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx-(br_b[2]-br_b[0])//2, H-70),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO)

    border(draw)
    out = os.path.join(BASE_DIR, "story_maio22_2.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ── STORY 3: CTA — chama agora ──────────────────────────────────────────────
# Foto escura, chamada direta, botão dourado
def story_3():
    img  = foto_fundo(os.path.join(BASE_DIR, "fotos", "IMG_1108.JPEG"),
                      overlay_alpha=210, overlay_color=(12, 5, 1))
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc   = load_font("NothingYouCouldDo-Regular.ttf", 70)
    fnt_tit  = load_font("Lora-Bold.ttf",          112)
    fnt_body = load_font("Lora-BoldItalic.ttf",     54)
    fnt_det  = load_font("InstrumentSans-Bold.ttf", 46)
    fnt_br   = load_font("InstrumentSans-Bold.ttf", 34)

    draw_flower(draw, 66,   92, petals=6, plen=14, pw=7,
                col_out=(190, 170, 145), col_mid=OURO_P, cr=5)
    draw_flower(draw, W-66, 92, petals=6, plen=14, pw=7,
                col_out=(190, 170, 145), col_mid=OURO_P, cr=5)

    cy = H // 2 - 290

    # Script gancho
    cy = script_outlined_wrap(draw, "ainda dá tempo",
                               fnt_sc, W-130, cx, cy,
                               fill=(232, 212, 178), line_sp=6) + 20

    draw.line([(cx-88, cy), (cx-14, cy)], fill=OURO_S, width=2)
    draw.line([(cx+14, cy), (cx+88, cy)], fill=OURO_S, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 26

    # "ainda tem data" — Lora-Bold 112px
    cy = c_text_shadow(draw, "ainda tem data", fnt_tit, cx, cy, fill=CREME, shd=5) + 6

    # "pra junho." — dourado
    cy = c_text_shadow(draw, "pra junho.", fnt_tit, cx, cy, fill=OURO_P, shd=5) + 34

    draw.line([(cx-72, cy), (cx+72, cy)], fill=(100, 78, 40), width=2)
    cy += 26

    # Body
    cy = wrap_centered(draw, "mas as encomendas fecham cedo.",
                        fnt_body, W-140, cx, cy,
                        fill=(205, 185, 155), line_spacing=10, shadow=True)
    cy += 38

    # Botão CTA dourado
    det   = "chama agora no WhatsApp"
    det_b = draw.textbbox((0, 0), det, font=fnt_det)
    dw    = det_b[2] - det_b[0]
    dh    = det_b[3] - det_b[1]
    px2, py2 = 40, 22
    draw.rounded_rectangle([cx-dw//2-px2+5, cy-py2+5,
                              cx+dw//2+px2+5, cy+dh+py2+5],
                             radius=30, fill=(12, 5, 1))
    draw.rounded_rectangle([cx-dw//2-px2, cy-py2,
                              cx+dw//2+px2, cy+dh+py2],
                             radius=30, fill=OURO, outline=OURO_P, width=2)
    draw.text((cx-dw//2, cy), det, font=fnt_det, fill=CREME)
    cy += dh + py2*2 + 26

    # Sub
    script_outlined_wrap(draw, "link na bio | DM aberto",
                          fnt_body, W-130, cx, cy,
                          fill=(185, 165, 130), ol_col=(5, 2, 0))

    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx-(br_b[2]-br_b[0])//2, H-70),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO_S)

    border(draw, col=(90, 65, 30))
    out = os.path.join(BASE_DIR, "story_maio22_3.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


if __name__ == "__main__":
    story_1()
    story_2()
    story_3()
    print("\n3 Stories 22/05 prontos.")
