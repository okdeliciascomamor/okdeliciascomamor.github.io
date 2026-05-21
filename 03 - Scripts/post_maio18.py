"""
Post Ok Delicias com Amor - 18/05/2026
Conceito: produto como obra de arte, uma empadinha so.
Layout: foto no terco superior, texto generoso no terco inferior.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, os

BASE_DIR  = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR = r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts"
FOTO_PATH = os.path.join(BASE_DIR, "fotos", "IMG_1153.JPEG")
OUTPUT    = os.path.join(BASE_DIR, "post_maio18.png")

CREME      = (255, 248, 234)
LAVANDA    = (230, 222, 248)
LAVANDA_M  = (196, 181, 224)
OURO       = (179, 138, 52)
OURO_SUAVE = (210, 175, 100)
OURO_PAL   = (235, 210, 155)
ROSA       = (240, 208, 220)
PESSEGO    = (255, 232, 192)
VERDE      = (148, 172, 124)
VERDE_ESC  = (100, 130, 80)
TXT        = (32, 18, 6)
TXT_M      = (72, 50, 22)

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
    if col_mid is None: col_mid = OURO_PAL
    for i in range(petals):
        draw_petal(draw, cx, cy, 360/petals*i, plen, pw, col_out)
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=col_mid)

def draw_leaf(draw, cx, cy, angle_deg, length=14, width=6):
    draw_petal(draw, cx, cy, angle_deg,     length,      width,      VERDE)
    draw_petal(draw, cx, cy, angle_deg+180, length*.4,   width*.5,   VERDE_ESC)

def build_post():
    W, H = 1080, 1350

    # === FUNDO: creme no topo -> lavanda suave ===
    img = Image.new("RGB", (W, H), CREME)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H-1)
        col = lerp(CREME, LAVANDA, t * 0.38)
        draw.line([(0, y), (W-1, y)], fill=col)

    # === DIVISOR HORIZONTAL creme -> lavanda na metade ===
    # Fundo inferior ligeiramente mais creme para contraste do texto
    split_y = 550
    for y in range(split_y, H):
        t = (y - split_y) / (H - split_y)
        col = lerp(lerp(CREME, LAVANDA, 0.38 * split_y / H), CREME, t * 0.7)
        draw.line([(0, y), (W-1, y)], fill=col)

    draw = ImageDraw.Draw(img)

    # === FOTO CIRCULAR no terco superior ===
    cx, cy_foto = W // 2, 430
    foto_r = 310

    foto_raw = Image.open(FOTO_PATH).convert("RGB")
    foto_raw = ImageEnhance.Brightness(foto_raw).enhance(1.10)
    foto_raw = ImageEnhance.Color(foto_raw).enhance(1.18)
    foto_raw = ImageEnhance.Sharpness(foto_raw).enhance(1.25)

    fw, fh = foto_raw.size
    side   = min(fw, fh)
    foto_sq = foto_raw.crop(((fw-side)//2, (fh-side)//2,
                              (fw+side)//2, (fh+side)//2))
    foto_sq = foto_sq.resize((foto_r*2, foto_r*2), Image.LANCZOS)

    # Mascara circular antialiased
    mask_big = Image.new("L", (foto_r*4, foto_r*4), 0)
    ImageDraw.Draw(mask_big).ellipse([6, 6, foto_r*4-6, foto_r*4-6], fill=255)
    mask_big = mask_big.filter(ImageFilter.GaussianBlur(4))
    mask = mask_big.resize((foto_r*2, foto_r*2), Image.LANCZOS)

    foto_circle = Image.new("RGBA", (foto_r*2, foto_r*2), (0,0,0,0))
    foto_circle.paste(foto_sq, (0, 0))
    foto_circle.putalpha(mask)

    # Halo suave atras da foto
    halo = Image.new("RGBA", (W, H), (0,0,0,0))
    for r_off in range(28, 0, -1):
        a = int(22 * (1 - r_off/28))
        col = lerp(LAVANDA_M, LAVANDA, r_off/28)
        ImageDraw.Draw(halo).ellipse(
            [cx-(foto_r+r_off), cy_foto-(foto_r+r_off),
             cx+(foto_r+r_off), cy_foto+(foto_r+r_off)],
            fill=(*col, a))
    img = Image.alpha_composite(img.convert("RGBA"), halo).convert("RGB")

    # Sombra suave
    shadow = Image.new("RGBA", (W, H), (0,0,0,0))
    for s in range(16, 0, -1):
        ImageDraw.Draw(shadow).ellipse(
            [cx-foto_r+s, cy_foto-foto_r+s+s, cx+foto_r+s+2, cy_foto+foto_r+s+s+2],
            fill=(50, 30, 10, int(10*(1-s/16))))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")

    img.paste(foto_circle.convert("RGB"),
              (cx-foto_r, cy_foto-foto_r),
              mask=foto_circle.split()[3])

    draw = ImageDraw.Draw(img)

    # === GUIRLANDA FLORAL cobrindo o aro da panelinha ===
    # O aro metalico/enferrujado fica a ~82% do raio da foto
    wreath_r = int(foto_r * 0.82)
    n = 48  # densidade suficiente para cobertura total
    for i in range(n):
        ang = 360 / n * i
        rad = math.radians(ang)
        wx = int(cx + wreath_r * math.cos(rad))
        wy = int(cy_foto + wreath_r * math.sin(rad))
        if i % 3 == 0:
            draw_flower(draw, wx, wy, petals=6,
                        plen=13, pw=7,
                        col_out=ROSA, col_mid=OURO_PAL, cr=5)
        elif i % 3 == 1:
            draw_leaf(draw, wx, wy, ang + 90, length=15, width=7)
        else:
            draw_flower(draw, wx, wy, petals=5,
                        plen=10, pw=5,
                        col_out=LAVANDA_M, col_mid=OURO_PAL, cr=4)

    # Anel duplo dourado
    draw.ellipse([cx-foto_r-13, cy_foto-foto_r-13,
                  cx+foto_r+13, cy_foto+foto_r+13],
                 outline=OURO_SUAVE, width=2)
    draw.ellipse([cx-foto_r-6,  cy_foto-foto_r-6,
                  cx+foto_r+6,  cy_foto+foto_r+6],
                 outline=OURO_PAL,   width=1)

    # Losangos nos cardeais do anel
    for ang in [0, 90, 180, 270]:
        rad = math.radians(ang)
        lx = int(cx + (foto_r+13) * math.cos(rad))
        ly = int(cy_foto + (foto_r+13) * math.sin(rad))
        d = 5
        draw.polygon([(lx,ly-d),(lx+d,ly),(lx,ly+d),(lx-d,ly)], fill=OURO)

    # Ornamentos florais nas diagonais
    fl_dist = foto_r + 50
    for ang, sc in [(45,1.0),(135,1.0),(225,0.92),(315,0.92)]:
        rad = math.radians(ang)
        fx = int(cx + fl_dist * math.cos(rad))
        fy = int(cy_foto + fl_dist * math.sin(rad))
        draw_flower(draw, fx, fy, petals=6,
                    plen=int(sc*17), pw=int(sc*8),
                    col_out=ROSA, col_mid=OURO_PAL, cr=int(sc*5))
        for la in [ang+40, ang-40]:
            lr = math.radians(la)
            lx2 = int(fx + sc*22*math.cos(lr))
            ly2 = int(fy + sc*22*math.sin(lr))
            draw_leaf(draw, lx2, ly2, la, length=int(sc*11), width=int(sc*5))

    # === DIVISOR ORNAMENTAL entre foto e texto ===
    div1_y = cy_foto + foto_r + 34
    lhalf  = 140
    draw.line([(cx-lhalf, div1_y),(cx-16, div1_y)], fill=OURO_SUAVE, width=1)
    draw.line([(cx+16, div1_y),   (cx+lhalf, div1_y)], fill=OURO_SUAVE, width=1)
    d = 5
    draw.polygon([(cx,div1_y-d),(cx+d,div1_y),(cx,div1_y+d),(cx-d,div1_y)], fill=OURO)
    draw_flower(draw, cx-lhalf-10, div1_y, petals=5,
                plen=9, pw=4, col_out=LAVANDA_M, col_mid=OURO_PAL, cr=3)
    draw_flower(draw, cx+lhalf+10, div1_y, petals=5,
                plen=9, pw=4, col_out=LAVANDA_M, col_mid=OURO_PAL, cr=3)

    # === TIPOGRAFIA ===
    fnt_script = load_font("NothingYouCouldDo-Regular.ttf", 52)
    fnt_title  = load_font("Italiana-Regular.ttf", 116)
    fnt_sub    = load_font("Lora-Italic.ttf", 36)
    fnt_detail = load_font("InstrumentSans-Regular.ttf", 27)
    fnt_brand  = load_font("Italiana-Regular.ttf", 34)

    base_y = div1_y + 32

    # Script: "pastel, empadinha, enroladinho..."
    sc_text = "pastel, empadinha, enroladinho..."
    sb = draw.textbbox((0,0), sc_text, font=fnt_script)
    sx = cx - (sb[2]-sb[0])//2
    # sombra sutil
    draw.text((sx+1, base_y+1), sc_text, font=fnt_script,
              fill=(160, 130, 90))
    draw.text((sx, base_y),     sc_text, font=fnt_script, fill=TXT_M)

    # Titulo: "feita com atencao"
    tt = "todos feitos à mão"
    tb = draw.textbbox((0,0), tt, font=fnt_title)
    tw, th = tb[2]-tb[0], tb[3]-tb[1]
    ty = base_y + (sb[3]-sb[1]) + 8
    draw.text((cx-tw//2, ty), tt, font=fnt_title, fill=TXT)

    # Divisor dourado fino
    dv_y = ty + th + 14
    draw.line([(cx-72, dv_y),(cx-12, dv_y)], fill=OURO_SUAVE, width=1)
    draw.line([(cx+12, dv_y),(cx+72, dv_y)], fill=OURO_SUAVE, width=1)
    draw.polygon([(cx,dv_y-4),(cx+4,dv_y),(cx,dv_y+4),(cx-4,dv_y)], fill=OURO)

    # Sub
    sub_t = "Salgados artesanais por encomenda"
    sub_b = draw.textbbox((0,0), sub_t, font=fnt_sub)
    sub_y = dv_y + 14
    draw.text((cx-(sub_b[2]-sub_b[0])//2, sub_y), sub_t, font=fnt_sub, fill=TXT_M)

    # Pill CTA
    det_t = "encomendas abertas para junho"
    det_b = draw.textbbox((0,0), det_t, font=fnt_detail)
    dw, dh = det_b[2]-det_b[0], det_b[3]-det_b[1]
    det_y = sub_y + (sub_b[3]-sub_b[1]) + 18
    px, py = 22, 10
    draw.rounded_rectangle(
        [cx-dw//2-px, det_y-py, cx+dw//2+px, det_y+dh+py],
        radius=20, fill=PESSEGO, outline=OURO_PAL, width=1)
    draw.text((cx-dw//2, det_y), det_t, font=fnt_detail, fill=TXT_M)

    # Marca
    br_t = "Ok Delicias com Amor"
    br_b = draw.textbbox((0,0), br_t, font=fnt_brand)
    br_y = H - 56
    draw.line([(cx-62, br_y-10),(cx+62, br_y-10)], fill=OURO_PAL, width=1)
    draw.text((cx-(br_b[2]-br_b[0])//2, br_y), br_t, font=fnt_brand, fill=OURO)

    # === BORDA DUPLA ===
    draw.rounded_rectangle([14,14,W-14,H-14], radius=28,
                            outline=OURO_SUAVE, width=2)
    draw.rounded_rectangle([22,22,W-22,H-22], radius=22,
                            outline=OURO_PAL,   width=1)

    img.convert("RGB").save(OUTPUT, "PNG", quality=98)
    print(f"Salvo: {OUTPUT}")

if __name__ == "__main__":
    build_post()
