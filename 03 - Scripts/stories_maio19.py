"""
3 Stories Ok Delicias com Amor - 19/05/2026
Conceito: artesanal, feminino, aconchegante
Paleta: creme, lavanda, dourado
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, os

BASE_DIR  = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR = r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts"

CREME      = (255, 248, 234)
LAVANDA    = (230, 222, 248)
LAVANDA_M  = (196, 181, 224)
LAVANDA_E  = (160, 140, 200)
OURO       = (179, 138, 52)
OURO_S     = (210, 175, 100)
OURO_P     = (235, 210, 155)
ROSA       = (240, 208, 220)
PESSEGO    = (255, 232, 192)
VERDE      = (148, 172, 124)
VERDE_E    = (100, 130,  80)
TXT        = ( 32,  18,   6)
TXT_M      = ( 72,  50,  22)
BRANCO     = (255, 255, 255)

W, H = 1080, 1920

def load_font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONTS_DIR, name), size)
    except:
        return ImageFont.load_default()

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))

def draw_petal(draw, cx, cy, angle_deg, length, width, color):
    a  = math.radians(angle_deg)
    px = cx + length * math.cos(a)
    py = cy + length * math.sin(a)
    p  = math.radians(angle_deg + 90)
    ox = (width / 2) * math.cos(p)
    oy = (width / 2) * math.sin(p)
    draw.polygon([
        (cx+ox, cy+oy), (px+ox*.3, py+oy*.3),
        (px, py),        (px-ox*.3, py-oy*.3),
        (cx-ox, cy-oy)], fill=color)

def draw_flower(draw, cx, cy, petals=6, plen=14, pw=7,
                col_out=None, col_mid=None, cr=5):
    if col_out is None: col_out = ROSA
    if col_mid is None: col_mid = OURO_P
    for i in range(petals):
        draw_petal(draw, cx, cy, 360/petals*i, plen, pw, col_out)
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=col_mid)

def draw_leaf(draw, cx, cy, angle_deg, length=14, width=6):
    draw_petal(draw, cx, cy, angle_deg,     length,     width,    VERDE)
    draw_petal(draw, cx, cy, angle_deg+180, length*.4,  width*.5, VERDE_E)

def base_bg(gradient_top, gradient_bot):
    img = Image.new("RGB", (W, H), gradient_top)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        draw.line([(0, y), (W-1, y)], fill=lerp(gradient_top, gradient_bot, t))
    return img

def border_double(draw):
    draw.rounded_rectangle([16, 16, W-16, H-16], radius=32, outline=OURO_S, width=2)
    draw.rounded_rectangle([26, 26, W-26, H-26], radius=24, outline=OURO_P,  width=1)

def wreath_ring(draw, cx, cy, radius, n=56):
    for i in range(n):
        ang = 360 / n * i
        rad = math.radians(ang)
        wx = int(cx + radius * math.cos(rad))
        wy = int(cy + radius * math.sin(rad))
        if i % 3 == 0:
            draw_flower(draw, wx, wy, petals=6, plen=13, pw=6,
                        col_out=ROSA, col_mid=OURO_P, cr=5)
        elif i % 3 == 1:
            draw_leaf(draw, wx, wy, ang + 90, length=15, width=7)
        else:
            draw_flower(draw, wx, wy, petals=5, plen=10, pw=5,
                        col_out=LAVANDA_M, col_mid=OURO_P, cr=4)

def paste_circle(base_img, foto_path, cx, cy, radius):
    foto = Image.open(foto_path).convert("RGB")
    foto = ImageEnhance.Brightness(foto).enhance(1.08)
    foto = ImageEnhance.Color(foto).enhance(1.15)
    foto = ImageEnhance.Sharpness(foto).enhance(1.2)
    fw, fh = foto.size
    side = min(fw, fh)
    foto = foto.crop(((fw-side)//2, (fh-side)//2, (fw+side)//2, (fh+side)//2))
    foto = foto.resize((radius*2, radius*2), Image.LANCZOS)

    mask_big = Image.new("L", (radius*4, radius*4), 0)
    ImageDraw.Draw(mask_big).ellipse([6, 6, radius*4-6, radius*4-6], fill=255)
    mask_big = mask_big.filter(ImageFilter.GaussianBlur(4))
    mask = mask_big.resize((radius*2, radius*2), Image.LANCZOS)

    circle = Image.new("RGBA", (radius*2, radius*2), (0,0,0,0))
    circle.paste(foto, (0,0))
    circle.putalpha(mask)

    # halo
    halo = Image.new("RGBA", (W, H), (0,0,0,0))
    for r_off in range(30, 0, -1):
        a = int(20 * (1 - r_off/30))
        col = lerp(LAVANDA_M, LAVANDA, r_off/30)
        ImageDraw.Draw(halo).ellipse(
            [cx-(radius+r_off), cy-(radius+r_off),
             cx+(radius+r_off), cy+(radius+r_off)],
            fill=(*col, a))
    base_img = Image.alpha_composite(base_img.convert("RGBA"), halo).convert("RGB")

    base_img.paste(circle.convert("RGB"), (cx-radius, cy-radius), mask=circle.split()[3])
    return base_img

def diamond(draw, cx, cy, size, color):
    draw.polygon([(cx, cy-size), (cx+size, cy), (cx, cy+size), (cx-size, cy)], fill=color)

def divider(draw, cx, y, half=100):
    draw.line([(cx-half, y), (cx-14, y)], fill=OURO_S, width=1)
    draw.line([(cx+14, y),   (cx+half, y)], fill=OURO_S, width=1)
    diamond(draw, cx, y, 5, OURO)


# ── STORY 1: Produto em destaque + CTA suave ─────────────────────────────────
def story_1():
    img = base_bg(CREME, lerp(CREME, LAVANDA, 0.45))
    draw = ImageDraw.Draw(img)

    cx = W // 2
    foto_r = 380
    cy_foto = 740

    img = paste_circle(img, os.path.join(BASE_DIR, "fotos", "IMG_1153.JPEG"), cx, cy_foto, foto_r)
    draw = ImageDraw.Draw(img)

    # guirlanda
    wreath_ring(draw, cx, cy_foto, int(foto_r * 0.83))

    # anel duplo dourado
    draw.ellipse([cx-foto_r-14, cy_foto-foto_r-14, cx+foto_r+14, cy_foto+foto_r+14],
                 outline=OURO_S, width=2)
    draw.ellipse([cx-foto_r-6,  cy_foto-foto_r-6,  cx+foto_r+6,  cy_foto+foto_r+6],
                 outline=OURO_P, width=1)
    for ang in [0, 90, 180, 270]:
        rad = math.radians(ang)
        lx = int(cx + (foto_r+14) * math.cos(rad))
        ly = int(cy_foto + (foto_r+14) * math.sin(rad))
        diamond(draw, lx, ly, 5, OURO)

    # === TEXTO ===
    fnt_script = load_font("NothingYouCouldDo-Regular.ttf", 58)
    fnt_title  = load_font("Italiana-Regular.ttf", 130)
    fnt_sub    = load_font("Lora-Italic.ttf", 42)
    fnt_detail = load_font("InstrumentSans-Regular.ttf", 32)
    fnt_brand  = load_font("Italiana-Regular.ttf", 38)

    base_y = cy_foto + foto_r + 44

    # script
    sc = "feita com atenção"
    sb = draw.textbbox((0,0), sc, font=fnt_script)
    draw.text((cx-(sb[2]-sb[0])//2+1, base_y+1), sc, font=fnt_script, fill=(160,130,90))
    draw.text((cx-(sb[2]-sb[0])//2,   base_y),   sc, font=fnt_script, fill=TXT_M)

    # titulo
    tt = "à mão"
    tb = draw.textbbox((0,0), tt, font=fnt_title)
    ty = base_y + (sb[3]-sb[1]) + 6
    draw.text((cx-(tb[2]-tb[0])//2, ty), tt, font=fnt_title, fill=TXT)

    dv_y = ty + (tb[3]-tb[1]) + 14
    divider(draw, cx, dv_y)

    sub = "Salgados artesanais por encomenda"
    sub_b = draw.textbbox((0,0), sub, font=fnt_sub)
    draw.text((cx-(sub_b[2]-sub_b[0])//2, dv_y+16), sub, font=fnt_sub, fill=TXT_M)

    # pill
    det = "encomendas abertas para junho"
    det_b = draw.textbbox((0,0), det, font=fnt_detail)
    dw, dh = det_b[2]-det_b[0], det_b[3]-det_b[1]
    det_y = dv_y + 16 + (sub_b[3]-sub_b[1]) + 22
    px, py2 = 24, 12
    draw.rounded_rectangle([cx-dw//2-px, det_y-py2, cx+dw//2+px, det_y+dh+py2],
                            radius=24, fill=PESSEGO, outline=OURO_P, width=1)
    draw.text((cx-dw//2, det_y), det, font=fnt_detail, fill=TXT_M)

    # marca
    br = "Ok Delicias com Amor"
    br_b = draw.textbbox((0,0), br, font=fnt_brand)
    br_y = H - 72
    draw.line([(cx-70, br_y-12), (cx+70, br_y-12)], fill=OURO_P, width=1)
    draw.text((cx-(br_b[2]-br_b[0])//2, br_y), br, font=fnt_brand, fill=OURO)

    # ornamentos de canto (topo)
    for ang in [45, 135]:
        rad = math.radians(ang)
        fx = int(cx + 460 * math.cos(rad))
        fy = int(90  + 460 * math.sin(rad))  # ficam fora, apenas florzinhas nos cantos
    draw_flower(draw, 60,     80,     petals=6, plen=18, pw=9,  col_out=LAVANDA_M, col_mid=OURO_P, cr=6)
    draw_flower(draw, W-60,   80,     petals=6, plen=18, pw=9,  col_out=ROSA,      col_mid=OURO_P, cr=6)
    draw_flower(draw, 60,     H-80,   petals=5, plen=14, pw=7,  col_out=ROSA,      col_mid=OURO_P, cr=5)
    draw_flower(draw, W-60,   H-80,   petals=5, plen=14, pw=7,  col_out=LAVANDA_M, col_mid=OURO_P, cr=5)

    border_double(draw)

    out = os.path.join(BASE_DIR, "story_maio19_1.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ── STORY 2: Cardapio visual — salgados em destaque ──────────────────────────
def story_2():
    img = base_bg(lerp(CREME, LAVANDA, 0.1), lerp(CREME, LAVANDA, 0.55))
    draw = ImageDraw.Draw(img)
    cx = W // 2

    # Tres fotos pequenas em coluna
    fotos_paths = [
        ("IMG_1130.JPEG", "Pasteis e canoinhas"),
        ("IMG_1153.JPEG", "Empadinhas artesanais"),
        ("IMG_1134.JPEG", "Empadinha especial"),
    ]
    r = 230
    positions_y = [400, 960, 1520]

    for i, (fname, label) in enumerate(fotos_paths):
        fpath = os.path.join(BASE_DIR, "fotos", fname)
        if not os.path.exists(fpath):
            continue
        cy = positions_y[i]
        img = paste_circle(img, fpath, cx, cy, r)
        draw = ImageDraw.Draw(img)

        # mini guirlanda
        wreath_ring(draw, cx, cy, int(r * 0.84), n=36)
        draw.ellipse([cx-r-9, cy-r-9, cx+r+9, cy+r+9], outline=OURO_S, width=1)

        # label da foto
        fnt_lbl = load_font("Lora-Italic.ttf", 34)
        lb = draw.textbbox((0,0), label, font=fnt_lbl)
        lx = cx - (lb[2]-lb[0])//2
        ly = cy + r + 18
        draw.text((lx, ly), label, font=fnt_lbl, fill=TXT_M)

    # titulo no topo
    fnt_tit = load_font("Italiana-Regular.ttf", 88)
    fnt_sub = load_font("InstrumentSans-Regular.ttf", 32)
    fnt_brand = load_font("Italiana-Regular.ttf", 36)

    tt = "nosso cardapio"
    tb = draw.textbbox((0,0), tt, font=fnt_tit)
    ty_top = 80
    draw.text((cx-(tb[2]-tb[0])//2, ty_top), tt, font=fnt_tit, fill=TXT)
    divider(draw, cx, ty_top + (tb[3]-tb[1]) + 10, half=80)

    # subtitulo
    sub = "salgados por encomenda"
    sb = draw.textbbox((0,0), sub, font=fnt_sub)
    draw.text((cx-(sb[2]-sb[0])//2, ty_top + (tb[3]-tb[1]) + 28),
              sub, font=fnt_sub, fill=TXT_M)

    # marca
    br = "Ok Delicias com Amor"
    br_b = draw.textbbox((0,0), br, font=fnt_brand)
    draw.text((cx-(br_b[2]-br_b[0])//2, H-68), br, font=fnt_brand, fill=OURO)

    draw_flower(draw, 60,   H//2, petals=6, plen=16, pw=8, col_out=ROSA,      col_mid=OURO_P, cr=5)
    draw_flower(draw, W-60, H//2, petals=6, plen=16, pw=8, col_out=LAVANDA_M, col_mid=OURO_P, cr=5)

    border_double(draw)

    out = os.path.join(BASE_DIR, "story_maio19_2.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ── STORY 3: CTA de encomenda — urgencia elegante ────────────────────────────
def story_3():
    img = base_bg(lerp(CREME, LAVANDA, 0.05), lerp(LAVANDA, CREME, 0.15))
    draw = ImageDraw.Draw(img)
    cx = W // 2

    # Foto grande centralizada
    foto_r = 350
    cy_foto = H // 2 - 80
    img = paste_circle(img, os.path.join(BASE_DIR, "fotos", "IMG_1134.JPEG"), cx, cy_foto, foto_r)
    draw = ImageDraw.Draw(img)

    wreath_ring(draw, cx, cy_foto, int(foto_r * 0.83))
    draw.ellipse([cx-foto_r-14, cy_foto-foto_r-14, cx+foto_r+14, cy_foto+foto_r+14],
                 outline=OURO_S, width=2)
    draw.ellipse([cx-foto_r-6,  cy_foto-foto_r-6,  cx+foto_r+6,  cy_foto+foto_r+6],
                 outline=OURO_P, width=1)
    for ang in [0, 90, 180, 270]:
        rad = math.radians(ang)
        lx = int(cx + (foto_r+14) * math.cos(rad))
        ly = int(cy_foto + (foto_r+14) * math.sin(rad))
        diamond(draw, lx, ly, 5, OURO)

    fnt_script = load_font("NothingYouCouldDo-Regular.ttf", 60)
    fnt_title  = load_font("Italiana-Regular.ttf", 118)
    fnt_sub    = load_font("Lora-Italic.ttf", 40)
    fnt_detail = load_font("InstrumentSans-Regular.ttf", 34)
    fnt_brand  = load_font("Italiana-Regular.ttf", 38)

    # Topo: script
    sc = "vagas limitadas"
    sb = draw.textbbox((0,0), sc, font=fnt_script)
    sc_y = cy_foto - foto_r - 120
    draw.text((cx-(sb[2]-sb[0])//2+1, sc_y+1), sc, font=fnt_script, fill=(160,130,90))
    draw.text((cx-(sb[2]-sb[0])//2,   sc_y),   sc, font=fnt_script, fill=TXT_M)
    divider(draw, cx, sc_y - 18, half=90)

    # Linha acima do script: "junho"
    fnt_mes = load_font("Italiana-Regular.ttf", 96)
    me = "junho"
    mb = draw.textbbox((0,0), me, font=fnt_mes)
    draw.text((cx-(mb[2]-mb[0])//2, sc_y - (mb[3]-mb[1]) - 36), me, font=fnt_mes, fill=TXT)

    # Baixo: CTA
    base_y = cy_foto + foto_r + 44

    tt = "garante a sua"
    tb = draw.textbbox((0,0), tt, font=fnt_title)
    draw.text((cx-(tb[2]-tb[0])//2, base_y), tt, font=fnt_title, fill=TXT)

    dv_y = base_y + (tb[3]-tb[1]) + 10
    divider(draw, cx, dv_y)

    sub = "encomendas pelo WhatsApp ou DM"
    sub_b = draw.textbbox((0,0), sub, font=fnt_sub)
    draw.text((cx-(sub_b[2]-sub_b[0])//2, dv_y+16), sub, font=fnt_sub, fill=TXT_M)

    # pill
    det = "link na bio"
    det_b = draw.textbbox((0,0), det, font=fnt_detail)
    dw, dh = det_b[2]-det_b[0], det_b[3]-det_b[1]
    det_y = dv_y + 16 + (sub_b[3]-sub_b[1]) + 24
    px2, py2 = 32, 14
    draw.rounded_rectangle([cx-dw//2-px2, det_y-py2, cx+dw//2+px2, det_y+dh+py2],
                            radius=24, fill=PESSEGO, outline=OURO_P, width=1)
    draw.text((cx-dw//2, det_y), det, font=fnt_detail, fill=TXT_M)

    # marca
    br = "Ok Delicias com Amor"
    br_b = draw.textbbox((0,0), br, font=fnt_brand)
    draw.text((cx-(br_b[2]-br_b[0])//2, H-72), br, font=fnt_brand, fill=OURO)

    draw_flower(draw, 60,   100,  petals=6, plen=18, pw=9,  col_out=ROSA,      col_mid=OURO_P, cr=6)
    draw_flower(draw, W-60, 100,  petals=6, plen=18, pw=9,  col_out=LAVANDA_M, col_mid=OURO_P, cr=6)
    draw_flower(draw, 60,   H-100, petals=5, plen=14, pw=7, col_out=LAVANDA_M, col_mid=OURO_P, cr=5)
    draw_flower(draw, W-60, H-100, petals=5, plen=14, pw=7, col_out=ROSA,      col_mid=OURO_P, cr=5)

    border_double(draw)

    out = os.path.join(BASE_DIR, "story_maio19_3.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


if __name__ == "__main__":
    story_1()
    story_2()
    story_3()
    print("Todos os stories salvos.")
