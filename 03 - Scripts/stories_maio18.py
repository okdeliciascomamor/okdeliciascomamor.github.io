"""
3 Stories Ok Delicias com Amor - 18/05/2026
Conceito: temporada de festas, feito a mao, abundancia artesanal
Complementa post_maio17.png (canoinhas overhead, full-bleed)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, os

BASE_DIR  = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR = r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts"

CREME      = (255, 248, 234)
LAVANDA    = (230, 222, 248)
LAVANDA_M  = (196, 181, 224)
OURO       = (179, 138, 52)
OURO_S     = (210, 175, 100)
OURO_P     = (235, 210, 155)
ROSA       = (240, 208, 220)
PESSEGO    = (255, 232, 192)
LILAS      = (208, 182, 228)
VERDE      = (148, 172, 124)
VERDE_E    = (100, 130,  80)
TXT        = ( 32,  18,   6)
TXT_M      = ( 72,  50,  22)

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

def draw_corner_ornament(draw, cx, cy, flip_x=False, flip_y=False, scale=1.0):
    sx = -1 if flip_x else 1
    sy = -1 if flip_y else 1
    s  = scale
    draw_flower(draw, cx, cy, petals=8,
                plen=int(34*s), pw=int(15*s),
                col_out=LILAS, col_mid=OURO_P, cr=int(10*s))
    for ang, dist, col in [(45, int(55*s), ROSA), (80, int(58*s), LILAS), (10, int(58*s), ROSA)]:
        fx = cx + sx * dist * math.cos(math.radians(ang))
        fy = cy + sy * dist * math.sin(math.radians(ang))
        draw_flower(draw, int(fx), int(fy), petals=6,
                    plen=int(17*s), pw=int(8*s),
                    col_out=col, col_mid=OURO_P, cr=int(6*s))
    for ang, dist in [(20, int(72*s)), (68, int(72*s))]:
        lx = cx + sx * dist * math.cos(math.radians(ang))
        ly = cy + sy * dist * math.sin(math.radians(ang))
        draw_leaf(draw, int(lx), int(ly), ang*sx, length=int(20*s), width=int(8*s))

def border_double(draw):
    draw.rounded_rectangle([16, 16, W-16, H-16], radius=32, outline=OURO_S, width=2)
    draw.rounded_rectangle([26, 26, W-26, H-26], radius=24, outline=OURO_P,  width=1)

def diamond(draw, cx, cy, size, color):
    draw.polygon([(cx, cy-size), (cx+size, cy), (cx, cy+size), (cx-size, cy)], fill=color)

def divider(draw, cx, y, half=100):
    draw.line([(cx-half, y), (cx-14, y)], fill=OURO_S, width=1)
    draw.line([(cx+14, y),   (cx+half, y)], fill=OURO_S, width=1)
    diamond(draw, cx, y, 5, OURO)

def bg_gradient(top, bot):
    img = Image.new("RGB", (W, H), top)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        draw.line([(0,y),(W-1,y)], fill=lerp(top, bot, y/(H-1)))
    return img

def paste_circle(base_img, foto_path, cx, cy, radius):
    foto = Image.open(foto_path).convert("RGB")
    foto = ImageEnhance.Brightness(foto).enhance(1.08)
    foto = ImageEnhance.Color(foto).enhance(1.18)
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
    halo = Image.new("RGBA", (W, H), (0,0,0,0))
    for r_off in range(28, 0, -1):
        a = int(18 * (1 - r_off/28))
        col = lerp(LAVANDA_M, LAVANDA, r_off/28)
        ImageDraw.Draw(halo).ellipse(
            [cx-(radius+r_off), cy-(radius+r_off),
             cx+(radius+r_off), cy+(radius+r_off)],
            fill=(*col, a))
    base_img = Image.alpha_composite(base_img.convert("RGBA"), halo).convert("RGB")
    base_img.paste(circle.convert("RGB"), (cx-radius, cy-radius), mask=circle.split()[3])
    return base_img


# ── STORY 1: Foto full-bleed com gradiente e copy de temporada ───────────────
def story_1():
    # Foto full-bleed (igual ao post_maio17, mas recortada para 9:16)
    foto = Image.open(os.path.join(BASE_DIR, "fotos", "IMG_1130.JPEG")).convert("RGB")
    foto = ImageEnhance.Brightness(foto).enhance(1.08)
    foto = ImageEnhance.Color(foto).enhance(1.18)
    foto = ImageEnhance.Contrast(foto).enhance(1.04)

    fw, fh = foto.size
    target = W / H
    if fw / fh > target:
        new_fw = int(fh * target)
        foto = foto.crop(((fw-new_fw)//2, 0, (fw+new_fw)//2, fh))
    else:
        new_fh = int(fw / target)
        foto = foto.crop((0, (fh-new_fh)//2, fw, (fh+new_fh)//2))
    img = foto.resize((W, H), Image.LANCZOS)

    # Gradiente no terco inferior
    grad_h = 620
    grad_y0 = H - grad_h
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    dov = ImageDraw.Draw(ov)
    cr2, cg2, cb2 = CREME
    for dy in range(grad_h):
        t = dy / (grad_h - 1)
        alpha = int((t ** 0.55) * 252)
        dov.line([(0, grad_y0+dy),(W-1, grad_y0+dy)], fill=(cr2,cg2,cb2,alpha))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")

    # Painel semi-opaco
    pov = Image.new("RGBA", (W, H), (0,0,0,0))
    pd = ImageDraw.Draw(pov)
    pd.rounded_rectangle([50, H-530, W-50, H-36], radius=28,
                         fill=(*CREME, 205), outline=(*OURO_P, 180), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), pov).convert("RGB")
    draw = ImageDraw.Draw(img)

    cx = W // 2

    # Ornamentos nos 4 cantos (sobre a foto)
    draw_corner_ornament(draw, 72,   80,   flip_x=False, flip_y=False, scale=0.95)
    draw_corner_ornament(draw, W-72, 80,   flip_x=True,  flip_y=False, scale=0.95)
    draw_corner_ornament(draw, 72,   H-80, flip_x=False, flip_y=True,  scale=0.82)
    draw_corner_ornament(draw, W-72, H-80, flip_x=True,  flip_y=True,  scale=0.82)

    # Bordas
    draw.rounded_rectangle([14,14,W-14,H-14], radius=30, outline=OURO_S, width=2)
    draw.rounded_rectangle([22,22,W-22,H-22], radius=24, outline=OURO_P, width=1)

    fnt_script = load_font("NothingYouCouldDo-Regular.ttf", 58)
    fnt_title  = load_font("Italiana-Regular.ttf", 134)
    fnt_sub    = load_font("Lora-Italic.ttf", 42)
    fnt_detail = load_font("InstrumentSans-Regular.ttf", 32)
    fnt_brand  = load_font("Italiana-Regular.ttf", 38)

    base_y = H - 490

    sc = "sua festa merece"
    sb = draw.textbbox((0,0), sc, font=fnt_script)
    draw.text((cx-(sb[2]-sb[0])//2, base_y), sc, font=fnt_script, fill=TXT_M)

    tt = "Feito a mao"
    tb = draw.textbbox((0,0), tt, font=fnt_title)
    ty = base_y + (sb[3]-sb[1]) + 8
    draw.text((cx-(tb[2]-tb[0])//2, ty), tt, font=fnt_title, fill=TXT)

    dv_y = ty + (tb[3]-tb[1]) + 12
    divider(draw, cx, dv_y, half=90)

    sub = "Salgados artesanais por encomenda"
    sub_b = draw.textbbox((0,0), sub, font=fnt_sub)
    draw.text((cx-(sub_b[2]-sub_b[0])//2, dv_y+14), sub, font=fnt_sub, fill=TXT_M)

    det = "Temporada de festas  ·  Garante sua data"
    det_b = draw.textbbox((0,0), det, font=fnt_detail)
    dw, dh = det_b[2]-det_b[0], det_b[3]-det_b[1]
    det_y = dv_y + 14 + (sub_b[3]-sub_b[1]) + 20
    px, py2 = 22, 10
    draw.rounded_rectangle([cx-dw//2-px, det_y-py2, cx+dw//2+px, det_y+dh+py2],
                            radius=20, fill=PESSEGO, outline=OURO_P, width=1)
    draw.text((cx-dw//2, det_y), det, font=fnt_detail, fill=TXT_M)

    br = "Ok Delicias com Amor"
    br_b = draw.textbbox((0,0), br, font=fnt_brand)
    draw.text((cx-(br_b[2]-br_b[0])//2, H-74), br, font=fnt_brand, fill=OURO)

    out = os.path.join(BASE_DIR, "story_maio18_1.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ── STORY 2: Processo artesanal — 3 fotos em tira ───────────────────────────
def story_2():
    img = bg_gradient(CREME, lerp(CREME, LAVANDA, 0.5))
    draw = ImageDraw.Draw(img)
    cx = W // 2

    fotos = [
        ("IMG_1040.JPEG", "A massa"),
        ("IMG_1130.JPEG", "O produto"),
        ("IMG_1049.JPEG", "O detalhe"),
    ]
    r = 220
    ys = [390, 960, 1530]

    for i, (fname, label) in enumerate(fotos):
        fpath = os.path.join(BASE_DIR, "fotos", fname)
        if not os.path.exists(fpath):
            continue
        img = paste_circle(img, fpath, cx, ys[i], r)
        draw = ImageDraw.Draw(img)
        draw.ellipse([cx-r-8, ys[i]-r-8, cx+r+8, ys[i]+r+8], outline=OURO_S, width=1)
        for ang in [0,90,180,270]:
            rad = math.radians(ang)
            lx = int(cx + (r+8)*math.cos(rad))
            ly = int(ys[i] + (r+8)*math.sin(rad))
            diamond(draw, lx, ly, 4, OURO)

        fnt_lbl = load_font("NothingYouCouldDo-Regular.ttf", 46)
        lb = draw.textbbox((0,0), label, font=fnt_lbl)
        draw.text((cx-(lb[2]-lb[0])//2, ys[i]+r+16), label, font=fnt_lbl, fill=TXT_M)

        # Flores laterais por faixa
        draw_flower(draw, 60,     ys[i], petals=6, plen=16, pw=8, col_out=ROSA,      col_mid=OURO_P, cr=6)
        draw_flower(draw, W-60,   ys[i], petals=6, plen=16, pw=8, col_out=LAVANDA_M, col_mid=OURO_P, cr=6)

    fnt_tit  = load_font("Italiana-Regular.ttf", 78)
    fnt_brand = load_font("Italiana-Regular.ttf", 36)

    tt = "do inicio ao fim"
    tb = draw.textbbox((0,0), tt, font=fnt_tit)
    draw.text((cx-(tb[2]-tb[0])//2, 100), tt, font=fnt_tit, fill=TXT)
    divider(draw, cx, 100+(tb[3]-tb[1])+10, half=72)

    br = "Ok Delicias com Amor"
    br_b = draw.textbbox((0,0), br, font=fnt_brand)
    draw.text((cx-(br_b[2]-br_b[0])//2, H-68), br, font=fnt_brand, fill=OURO)

    border_double(draw)

    out = os.path.join(BASE_DIR, "story_maio18_2.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


# ── STORY 3: CTA direto para encomenda ───────────────────────────────────────
def story_3():
    img = bg_gradient(lerp(CREME, LAVANDA, 0.08), lerp(LAVANDA, CREME, 0.12))
    draw = ImageDraw.Draw(img)
    cx = W // 2

    # Foto grande central
    foto_r = 360
    cy_foto = H // 2 - 60
    img = paste_circle(img, os.path.join(BASE_DIR, "fotos", "IMG_1130.JPEG"), cx, cy_foto, foto_r)
    draw = ImageDraw.Draw(img)

    # Guirlanda simples
    n = 52
    for i in range(n):
        ang = 360/n*i
        rad = math.radians(ang)
        wx = int(cx + int(foto_r*0.83)*math.cos(rad))
        wy = int(cy_foto + int(foto_r*0.83)*math.sin(rad))
        if i % 3 == 0:
            draw_flower(draw, wx, wy, petals=6, plen=12, pw=6, col_out=ROSA, col_mid=OURO_P, cr=4)
        elif i % 3 == 1:
            draw_leaf(draw, wx, wy, ang+90, length=14, width=6)
        else:
            draw_flower(draw, wx, wy, petals=5, plen=9, pw=5, col_out=LAVANDA_M, col_mid=OURO_P, cr=3)

    draw.ellipse([cx-foto_r-12, cy_foto-foto_r-12, cx+foto_r+12, cy_foto+foto_r+12],
                 outline=OURO_S, width=2)
    draw.ellipse([cx-foto_r-5,  cy_foto-foto_r-5,  cx+foto_r+5,  cy_foto+foto_r+5],
                 outline=OURO_P, width=1)
    for ang in [0,90,180,270]:
        rad = math.radians(ang)
        lx = int(cx+(foto_r+12)*math.cos(rad))
        ly = int(cy_foto+(foto_r+12)*math.sin(rad))
        diamond(draw, lx, ly, 5, OURO)

    fnt_script = load_font("NothingYouCouldDo-Regular.ttf", 56)
    fnt_title  = load_font("Italiana-Regular.ttf", 120)
    fnt_sub    = load_font("Lora-Italic.ttf", 40)
    fnt_detail = load_font("InstrumentSans-Regular.ttf", 34)
    fnt_brand  = load_font("Italiana-Regular.ttf", 38)

    # Topo
    sc_top = "encomendas abertas"
    sb_top = draw.textbbox((0,0), sc_top, font=fnt_script)
    sc_y = cy_foto - foto_r - 110
    divider(draw, cx, sc_y - 20, half=88)
    draw.text((cx-(sb_top[2]-sb_top[0])//2+1, sc_y+1), sc_top, font=fnt_script, fill=(160,130,90))
    draw.text((cx-(sb_top[2]-sb_top[0])//2,   sc_y),   sc_top, font=fnt_script, fill=TXT_M)

    fnt_mes = load_font("Italiana-Regular.ttf", 100)
    me = "junho"
    mb = draw.textbbox((0,0), me, font=fnt_mes)
    draw.text((cx-(mb[2]-mb[0])//2, sc_y-(mb[3]-mb[1])-30), me, font=fnt_mes, fill=TXT)

    # Base
    base_y = cy_foto + foto_r + 48

    tt = "chama no DM"
    tb = draw.textbbox((0,0), tt, font=fnt_title)
    draw.text((cx-(tb[2]-tb[0])//2, base_y), tt, font=fnt_title, fill=TXT)

    dv_y = base_y + (tb[3]-tb[1]) + 10
    divider(draw, cx, dv_y)

    sub = "ou link na bio"
    sub_b = draw.textbbox((0,0), sub, font=fnt_sub)
    draw.text((cx-(sub_b[2]-sub_b[0])//2, dv_y+14), sub, font=fnt_sub, fill=TXT_M)

    det = "Salgados artesanais por encomenda"
    det_b = draw.textbbox((0,0), det, font=fnt_detail)
    dw, dh = det_b[2]-det_b[0], det_b[3]-det_b[1]
    det_y = dv_y + 14 + (sub_b[3]-sub_b[1]) + 22
    px2, py2 = 28, 12
    draw.rounded_rectangle([cx-dw//2-px2, det_y-py2, cx+dw//2+px2, det_y+dh+py2],
                            radius=22, fill=PESSEGO, outline=OURO_P, width=1)
    draw.text((cx-dw//2, det_y), det, font=fnt_detail, fill=TXT_M)

    br = "Ok Delicias com Amor"
    br_b = draw.textbbox((0,0), br, font=fnt_brand)
    draw.text((cx-(br_b[2]-br_b[0])//2, H-72), br, font=fnt_brand, fill=OURO)

    draw_corner_ornament(draw, 64,   90,   flip_x=False, flip_y=False, scale=0.88)
    draw_corner_ornament(draw, W-64, 90,   flip_x=True,  flip_y=False, scale=0.88)
    draw_corner_ornament(draw, 64,   H-90, flip_x=False, flip_y=True,  scale=0.76)
    draw_corner_ornament(draw, W-64, H-90, flip_x=True,  flip_y=True,  scale=0.76)

    border_double(draw)

    out = os.path.join(BASE_DIR, "story_maio18_3.png")
    img.convert("RGB").save(out, "PNG", quality=98)
    print(f"Salvo: {out}")


if __name__ == "__main__":
    story_1()
    story_2()
    story_3()
    print("Stories 18/05 prontos.")
