"""
5 Stories Storytelling — Ok Delícias com Amor — 20/05/2026
Conceito: a Oliete nao sabe falar nao. Junho enchendo. Urgencia real.
Narrativa em 5 atos: gancho, revelacao, humanizacao, virada, CTA
v2: Lora-Bold substitui Italiana, fontes maiores, outline em script, sombras
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
    px, py = cx + length * math.cos(a), cy + length * math.sin(a)
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
    draw_petal(draw, cx, cy, angle_deg,       length,      width,   VERDE)
    draw_petal(draw, cx, cy, angle_deg + 180, length*.4,   width*.5, VERDE_E)


def diamond(draw, cx, cy, size, color):
    draw.polygon([(cx, cy-size), (cx+size, cy), (cx, cy+size), (cx-size, cy)], fill=color)


def wrap_centered(draw, text, font, max_w, cx, y, fill, line_spacing=10, shadow=False):
    """Quebra texto, centraliza cada linha. Retorna y final."""
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
            draw.text((x+3, y+3), line, font=font, fill=(4, 2, 0))
        draw.text((x, y), line, font=font, fill=fill)
        y += (bb[3] - bb[1]) + line_spacing
    return y


def foto_fundo(foto_path, overlay_alpha=190, overlay_color=None):
    """Retorna imagem full-bleed com overlay escurecido."""
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


def script_outlined(draw, text, font, cx, y, fill=None, ol_col=(5, 2, 0), ol=2):
    """Texto script com outline escuro — legivel em QUALQUER fundo."""
    if fill is None:
        fill = OURO_P
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    x  = cx - tw // 2
    for dx in [-ol, 0, ol]:
        for dy in [-ol, 0, ol]:
            if dx or dy:
                draw.text((x+dx, y+dy), text, font=font, fill=ol_col)
    draw.text((x, y), text, font=font, fill=fill)
    return y + th


def script_outlined_wrap(draw, text, font, max_w, cx, y,
                          fill=None, ol_col=(5, 2, 0), ol=2, line_sp=8):
    """Script outlined com word-wrap automatico. Retorna y apos ultimo linha."""
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
    """Texto centralizado com sombra intensa. Retorna y + altura."""
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    x  = cx - tw // 2
    draw.text((x+shd, y+shd), text, font=font, fill=shd_col)
    draw.text((x, y), text, font=font, fill=fill)
    return y + th


# ── STORY 1: GANCHO ───────────────────────────────────────────────────────────
# "tem algo acontecendo na cozinha da Oliete..."
def story_1():
    img  = foto_fundo(os.path.join(BASE_DIR, "fotos", "IMG_1067.JPEG"),
                      overlay_alpha=205, overlay_color=(10, 5, 1))
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc   = load_font("NothingYouCouldDo-Regular.ttf", 70)
    fnt_tit  = load_font("Lora-Bold.ttf",          124)
    fnt_body = load_font("Lora-BoldItalic.ttf",    62)
    fnt_sub  = load_font("Lora-BoldItalic.ttf",    52)
    fnt_br   = load_font("InstrumentSans-Bold.ttf", 36)

    # Flores nos cantos superiores
    draw_flower(draw, 66,   92, petals=6, plen=15, pw=7,
                col_out=(200, 180, 160), col_mid=OURO_P, cr=5)
    draw_flower(draw, W-66, 92, petals=6, plen=15, pw=7,
                col_out=(200, 180, 160), col_mid=OURO_P, cr=5)

    # Script com outline e wrap — completamente dentro da borda
    sc   = "você já sabe quem faz o melhor?"
    sc_y = 210
    sc_end = script_outlined_wrap(draw, sc, fnt_sc, W-130, cx, sc_y,
                                   fill=OURO_P, line_sp=6)

    # Linha dourada
    draw.line([(cx-80, sc_end+16), (cx+80, sc_end+16)], fill=OURO_S, width=2)

    # Titulo em Lora-Bold — MUITO mais legivel que Italiana
    ty = sc_end + 46
    for tl, cor in [("tem algo", CREME), ("acontecendo", CREME)]:
        ty = c_text_shadow(draw, tl, fnt_tit, cx, ty, fill=cor)
        ty += 10

    # Body
    body_y = ty + 30
    body_y = c_text_shadow(draw, "na cozinha da Oliete.", fnt_body, cx, body_y, fill=OURO_P)

    # Suspense
    sub_y = body_y + 54
    script_outlined(draw, "e você precisa saber.", fnt_sub, cx, sub_y,
                    fill=(220, 200, 168), ol_col=(5, 2, 0))

    # Seta para o proximo story
    arr_y = H - 224
    draw.line([(cx, arr_y), (cx, arr_y+56)], fill=OURO_S, width=2)
    diamond(draw, cx, arr_y+60, 8, OURO_S)

    # Marca
    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx-(br_b[2]-br_b[0])//2, H-74),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO_S)

    border(draw, col=(100, 80, 50))
    out = os.path.join(BASE_DIR, "story_maio20_1.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ── STORY 2: REVELACAO ───────────────────────────────────────────────────────
# "Maio: lotado. Junho: enchendo. Julho: ja tem reservas."
def story_2():
    img  = bg_grad(CREME, lerp(CREME, LAVANDA, 0.55))
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc    = load_font("NothingYouCouldDo-Regular.ttf", 62)
    fnt_mes   = load_font("Lora-Bold.ttf",          148)
    fnt_stat  = load_font("InstrumentSans-Bold.ttf", 52)
    fnt_stat2 = load_font("InstrumentSans-Bold.ttf", 44)
    fnt_br    = load_font("InstrumentSans-Bold.ttf", 36)

    # Flores nos quatro cantos
    draw_flower(draw, 66,   94, petals=6, plen=16, pw=8,
                col_out=ROSA,      col_mid=OURO_P, cr=6)
    draw_flower(draw, W-66, 94, petals=6, plen=16, pw=8,
                col_out=LAVANDA_M, col_mid=OURO_P, cr=6)
    draw_flower(draw, 66,   H-94, petals=5, plen=12, pw=6,
                col_out=LAVANDA_M, col_mid=OURO_P, cr=5)
    draw_flower(draw, W-66, H-94, petals=5, plen=12, pw=6,
                col_out=ROSA,      col_mid=OURO_P, cr=5)

    # Header — texto escuro sobre fundo claro, sem outline, com wrap
    sc   = "a agenda da Oliete em 2026"
    sc_y = 136
    sc_end = wrap_centered(draw, sc, fnt_sc, W-130, cx, sc_y,
                            fill=TXT_M, line_spacing=6, shadow=False)

    sep_y = sc_end + 12
    draw.line([(cx-90, sep_y), (cx+90, sep_y)], fill=OURO_S, width=2)
    diamond(draw, cx, sep_y, 6, OURO)

    # 3 blocos de meses — ocupam toda a tela de forma proporcional
    meses = [
        ("maio",   "lotado.",           VERDE,     (255, 250, 242)),
        ("junho",  "enchendo rápido.",  OURO,      (255, 252, 237)),
        ("julho",  "já tem reservas.",  LAVANDA_E, (247, 242, 255)),
    ]

    block_start = sep_y + 32
    block_end   = H - 172
    total_gap   = block_end - block_start
    bh          = int(total_gap / 3) - 22
    gap         = 22

    block_y = block_start
    for mes, status, cor_mes, bg_block in meses:
        draw.rounded_rectangle([60, block_y, W-60, block_y+bh],
                                radius=20, fill=bg_block, outline=OURO_P, width=2)
        mb   = draw.textbbox((0, 0), mes,    font=fnt_mes)
        stb  = draw.textbbox((0, 0), status, font=fnt_stat)
        text_h     = (mb[3]-mb[1]) + 10 + (stb[3]-stb[1])
        text_top_y = block_y + (bh - text_h) // 2
        draw.text((cx-(mb[2]-mb[0])//2,   text_top_y),                     mes,    font=fnt_mes,  fill=cor_mes)
        draw.text((cx-(stb[2]-stb[0])//2, text_top_y+(mb[3]-mb[1])+10),   status, font=fnt_stat, fill=TXT_M)
        block_y += bh + gap

    # Mensagem final de urgencia
    msg   = "quem deixa pra última hora, fica sem."
    msg_b = draw.textbbox((0, 0), msg, font=fnt_stat2)
    msg_y = block_y + 14
    draw.text((cx-(msg_b[2]-msg_b[0])//2, msg_y), msg, font=fnt_stat2, fill=TXT_M)

    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx-(br_b[2]-br_b[0])//2, H-70),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO)

    border(draw)
    out = os.path.join(BASE_DIR, "story_maio20_2.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ── STORY 3: HUMANIZACAO ─────────────────────────────────────────────────────
# "ela ate pediu pra tirar o link. porque ela nao sabe falar nao."
def story_3():
    img  = foto_fundo(os.path.join(BASE_DIR, "fotos", "IMG_1077.JPEG"),
                      overlay_alpha=202, overlay_color=(10, 5, 1))
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc   = load_font("NothingYouCouldDo-Regular.ttf", 80)
    fnt_tit  = load_font("Lora-Bold.ttf",          100)
    fnt_body = load_font("Lora-BoldItalic.ttf",    60)
    fnt_det  = load_font("InstrumentSans-Bold.ttf", 42)
    fnt_br   = load_font("InstrumentSans-Bold.ttf", 36)

    draw_flower(draw, 66,   84, petals=5, plen=13, pw=6,
                col_out=(200, 180, 160), col_mid=OURO_P, cr=4)
    draw_flower(draw, W-66, 84, petals=5, plen=13, pw=6,
                col_out=(200, 180, 160), col_mid=OURO_P, cr=4)

    # Script com outline
    sc_y = 186
    sc_end = script_outlined(draw, "a verdade sobre a Oliete:",
                              fnt_sc, cx, sc_y, fill=OURO_P)
    draw.line([(cx-72, sc_end+16), (cx+72, sc_end+16)], fill=OURO_S, width=2)

    # "ela ate pediu" — script menor, com outline
    y = sc_end + 46
    sc2_b = draw.textbbox((0, 0), "ela ate pediu", font=fnt_sc)
    y_after = script_outlined(draw, "ela até pediu", fnt_sc, cx, y,
                               fill=(228, 212, 188), ol_col=(5, 2, 0))
    y = y_after + 8

    # "pra tirar o link." — Lora-Bold, PUNCH
    l2_b = draw.textbbox((0, 0), "pra tirar o link.", font=fnt_tit)
    y = c_text_shadow(draw, "pra tirar o link.", fnt_tit, cx, y, fill=CREME)
    y += 42

    draw.line([(cx-62, y), (cx+62, y)], fill=OURO_S, width=2)
    y += 36

    # "porque ela nao sabe" — corpo grande
    body_b = draw.textbbox((0, 0), "porque ela nao sabe", font=fnt_body)
    y = c_text_shadow(draw, "porque ela não sabe", fnt_body, cx, y,
                      fill=(218, 202, 182))
    y += 8

    # "falar nao." — Lora-Bold, dourado, PUNCH
    y = c_text_shadow(draw, "falar não.", fnt_tit, cx, y, fill=OURO_P)
    y += 50

    draw.line([(cx-50, y), (cx+50, y)], fill=(120, 90, 50), width=1)
    y += 32

    # Detalhe — cada pedido vira cuidado
    wrap_centered(draw, "cada pedido vira cuidado. cada salgado, carinho.",  # já correto
                  fnt_det, W-160, cx, y, fill=(198, 178, 148),
                  line_spacing=12, shadow=True)

    # Seta
    arr_y = H - 222
    draw.line([(cx, arr_y), (cx, arr_y+52)], fill=OURO_S, width=2)
    diamond(draw, cx, arr_y+56, 7, OURO_S)

    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx-(br_b[2]-br_b[0])//2, H-72),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO_S)

    border(draw, col=(90, 65, 30))
    out = os.path.join(BASE_DIR, "story_maio20_3.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ── STORY 4: VIRADA ───────────────────────────────────────────────────────────
# "quando ela diz sim, e porque vai fazer com tudo."
def story_4():
    img  = bg_grad(lerp(CREME, LAVANDA, 0.05), lerp(CREME, LAVANDA, 0.50))
    cx   = W // 2

    # Foto em arco — ocupa topo da tela
    arch_w = 860; arch_h = 860; top_y = 268

    foto = Image.open(os.path.join(BASE_DIR, "fotos", "IMG_1140.JPEG")).convert("RGB")
    foto = ImageEnhance.Brightness(foto).enhance(1.08)
    foto = ImageEnhance.Color(foto).enhance(1.2)
    fw, fh = foto.size
    ratio  = arch_w / arch_h
    if fw / fh > ratio:
        nfw = int(fh * ratio)
        foto = foto.crop(((fw-nfw)//2, 0, (fw+nfw)//2, fh))
    else:
        nfh = int(fw / ratio)
        foto = foto.crop((0, (fh-nfh)//2, fw, (fh+nfh)//2))
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

    fnt_sc   = load_font("NothingYouCouldDo-Regular.ttf", 78)
    fnt_tit  = load_font("Lora-Bold.ttf",          110)
    fnt_body = load_font("Lora-BoldItalic.ttf",    56)
    fnt_det  = load_font("InstrumentSans-Bold.ttf", 42)
    fnt_br   = load_font("InstrumentSans-Bold.ttf", 36)

    # Flores nos cantos
    for fx, col_o in [(66, ROSA), (W-66, LAVANDA_M)]:
        draw_flower(draw, fx, 92, petals=6, plen=16, pw=8,
                    col_out=col_o, col_mid=OURO_P, cr=6)
        draw_leaf(draw, fx-14, 108, 225, 14, 6)
        draw_leaf(draw, fx+14, 108, 315, 14, 6)

    # Script topo — texto escuro sobre fundo claro
    sc   = "mas quando ela diz sim..."
    sb   = draw.textbbox((0, 0), sc, font=fnt_sc)
    sc_y = 140
    draw.text((cx-(sb[2]-sb[0])//2+2, sc_y+2), sc, font=fnt_sc, fill=(180, 150, 90))
    draw.text((cx-(sb[2]-sb[0])//2,   sc_y),   sc, font=fnt_sc, fill=TXT_M)

    base_y = top_y + arch_h + 50

    # Ornamento
    draw.line([(cx-88, base_y-8), (cx-14, base_y-8)], fill=OURO_S, width=2)
    draw.line([(cx+14, base_y-8), (cx+88, base_y-8)], fill=OURO_S, width=2)
    diamond(draw, cx, base_y-8, 6, OURO)

    # Titulo — Lora-Bold, fundo claro, sem sombra necessaria
    base_y = wrap_centered(draw, "é porque vai fazer", fnt_tit, W-100, cx, base_y,
                            fill=TXT, shadow=False, line_spacing=8)
    base_y += 4
    base_y = wrap_centered(draw, "com tudo.", fnt_tit, W-100, cx, base_y,
                            fill=OURO, shadow=False, line_spacing=8)
    base_y += 34

    draw.line([(cx-62, base_y), (cx+62, base_y)], fill=OURO_P, width=2)
    base_y += 30

    # Body
    for line in ["cada salgado feito com o cuidado", "de quem faz isso por amor."]:
        lb = draw.textbbox((0, 0), line, font=fnt_body)
        draw.text((cx-(lb[2]-lb[0])//2, base_y), line, font=fnt_body, fill=TXT_M)
        base_y += (lb[3]-lb[1]) + 8

    base_y += 20
    # Detalhe
    det_b = draw.textbbox((0, 0), "reserve sua data com antecedencia", font=fnt_det)
    draw.text((cx-(det_b[2]-det_b[0])//2, base_y),
              "reserve sua data com antecedência", font=fnt_det, fill=TXT_M)

    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx-(br_b[2]-br_b[0])//2, H-70),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO)

    border(draw)
    out = os.path.join(BASE_DIR, "story_maio20_4.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ── STORY 5: CTA ─────────────────────────────────────────────────────────────
# "a hora é agora. manda mensagem."
def story_5():
    img  = foto_fundo(os.path.join(BASE_DIR, "fotos", "IMG_1142.JPEG"),
                      overlay_alpha=208, overlay_color=(12, 5, 1))
    draw = ImageDraw.Draw(img)
    cx   = W // 2

    fnt_sc   = load_font("NothingYouCouldDo-Regular.ttf", 70)
    fnt_tit  = load_font("Lora-Bold.ttf",          150)
    fnt_body = load_font("Lora-BoldItalic.ttf",    56)
    fnt_det  = load_font("InstrumentSans-Bold.ttf", 48)
    fnt_br   = load_font("InstrumentSans-Bold.ttf", 36)

    draw_flower(draw, 66,   94, petals=6, plen=15, pw=7,
                col_out=(190, 170, 145), col_mid=OURO_P, cr=5)
    draw_flower(draw, W-66, 94, petals=6, plen=15, pw=7,
                col_out=(190, 170, 145), col_mid=OURO_P, cr=5)

    # Bloco central — verticalizado
    cy = H // 2 - 290

    # Script com outline e wrap
    cy = script_outlined_wrap(draw, "se a sua festa merece o melhor",
                               fnt_sc, W-130, cx, cy,
                               fill=(232, 212, 178), line_sp=6) + 20

    draw.line([(cx-90, cy), (cx-14, cy)], fill=OURO_S, width=2)
    draw.line([(cx+14, cy), (cx+90, cy)], fill=OURO_S, width=2)
    diamond(draw, cx, cy, 6, OURO)
    cy += 26

    # "a hora" — Lora-Bold 150px, impacto maximo
    cy = c_text_shadow(draw, "a hora", fnt_tit, cx, cy, fill=CREME, shd=5) + 6

    # "e agora." — Lora-Bold 150px, dourado
    cy = c_text_shadow(draw, "é agora.", fnt_tit, cx, cy, fill=OURO_P, shd=5) + 34

    draw.line([(cx-72, cy), (cx+72, cy)], fill=(100, 78, 40), width=2)
    cy += 28

    # Body — pode quebrar linha, texto importante
    cy = wrap_centered(draw, "vagas de julho já estão sendo reservadas.",
                        fnt_body, W-140, cx, cy,
                        fill=(205, 185, 155), line_spacing=10, shadow=True)
    cy += 40

    # Botao CTA
    det   = "manda mensagem agora"
    det_b = draw.textbbox((0, 0), det, font=fnt_det)
    dw    = det_b[2] - det_b[0]
    dh    = det_b[3] - det_b[1]
    px2, py2 = 44, 22
    # Sombra do botao
    draw.rounded_rectangle([cx-dw//2-px2+5, cy-py2+5,
                              cx+dw//2+px2+5, cy+dh+py2+5],
                             radius=30, fill=(12, 5, 1))
    # Botao dourado
    draw.rounded_rectangle([cx-dw//2-px2, cy-py2,
                              cx+dw//2+px2, cy+dh+py2],
                             radius=30, fill=OURO, outline=OURO_P, width=2)
    draw.text((cx-dw//2, cy), det, font=fnt_det, fill=CREME)
    cy += dh + py2*2 + 28

    # Sub
    script_outlined(draw, "link na bio | DM aberto", fnt_body, cx, cy,
                    fill=(185, 165, 130), ol_col=(5, 2, 0))

    br_b = draw.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    draw.text((cx-(br_b[2]-br_b[0])//2, H-70),
              "Ok Delícias com Amor", font=fnt_br, fill=OURO_S)

    border(draw, col=(90, 65, 30))
    out = os.path.join(BASE_DIR, "story_maio20_5.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


if __name__ == "__main__":
    story_1()
    story_2()
    story_3()
    story_4()
    story_5()
    print("\nStorytelling 20/05 v2 completo.")
