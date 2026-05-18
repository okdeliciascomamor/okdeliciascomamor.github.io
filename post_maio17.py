"""
Post Ok Delicias com Amor - 17/05/2026
Redesign: foto full-bleed + gradiente + tipografia grande
Foto: IMG_1130.JPEG (canoizinhas overhead com toppings coloridos)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math
import os

# -------------------------------------------------------------------
# CAMINHOS
# -------------------------------------------------------------------
BASE_DIR   = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR  = r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts"
FOTO_PATH  = os.path.join(BASE_DIR, "fotos", "IMG_1130.JPEG")
OUTPUT     = os.path.join(BASE_DIR, "post_maio17.png")

# -------------------------------------------------------------------
# PALETA
# -------------------------------------------------------------------
LAVANDA    = (230, 222, 245)
CREME      = (255, 248, 234)
OURO       = (195, 152, 58)
OURO_CLARO = (220, 185, 95)
OURO_SUAVE = (240, 210, 130)
ROSA       = (240, 208, 220)
LILAS      = (208, 182, 228)
PESSEGO    = (255, 232, 192)
VERDE      = (148, 172, 124)
VERDE_ESC  = (100, 130, 80)
TXT        = (58, 40, 18)
TXT_M      = (98, 70, 36)

# -------------------------------------------------------------------
# FONTES
# -------------------------------------------------------------------
def load_font(name, size):
    path = os.path.join(FONTS_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except Exception as e:
        print(f"AVISO: {name} ({e})")
        return ImageFont.load_default()

fnt_script = load_font("NothingYouCouldDo-Regular.ttf", 52)
fnt_title  = load_font("Italiana-Regular.ttf", 108)
fnt_sub    = load_font("Lora-Italic.ttf", 32)
fnt_detail = load_font("InstrumentSans-Regular.ttf", 26)
fnt_brand  = load_font("Italiana-Regular.ttf", 32)

# -------------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------------
def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def draw_petal(draw, cx, cy, angle_deg, length, width, color):
    angle = math.radians(angle_deg)
    px    = cx + length * math.cos(angle)
    py    = cy + length * math.sin(angle)
    perp  = math.radians(angle_deg + 90)
    ox    = (width / 2) * math.cos(perp)
    oy    = (width / 2) * math.sin(perp)
    poly  = [
        (cx + ox,        cy + oy),
        (px + ox * 0.3,  py + oy * 0.3),
        (px,             py),
        (px - ox * 0.3,  py - oy * 0.3),
        (cx - ox,        cy - oy),
    ]
    draw.polygon(poly, fill=color)

def draw_flower(draw, cx, cy, petals=8, petal_len=22, petal_w=10,
                color_outer=None, color_center=None, center_r=7):
    if color_outer  is None: color_outer  = ROSA
    if color_center is None: color_center = OURO_SUAVE
    for i in range(petals):
        draw_petal(draw, cx, cy, 360 / petals * i, petal_len, petal_w, color_outer)
    draw.ellipse([cx - center_r, cy - center_r, cx + center_r, cy + center_r],
                 fill=color_center)

def draw_leaf(draw, cx, cy, angle_deg, length=20, width=9, color=None):
    if color is None: color = VERDE
    draw_petal(draw, cx, cy, angle_deg,        length,          width,        color)
    draw_petal(draw, cx, cy, angle_deg + 180,  length * 0.45,   width * 0.6,  VERDE_ESC)

def draw_corner_ornament(draw, cx, cy, flip_x=False, flip_y=False, scale=1.0):
    sx = -1 if flip_x else 1
    sy = -1 if flip_y else 1
    s  = scale

    # Flor central grande
    draw_flower(draw, cx, cy, petals=8,
                petal_len=int(38*s), petal_w=int(17*s),
                color_outer=LILAS, color_center=OURO_SUAVE, center_r=int(11*s))

    # 3 flores medias
    for ang, dist, col in [(45, int(60*s), ROSA), (85, int(65*s), LILAS), (5, int(65*s), ROSA)]:
        fx = cx + sx * dist * math.cos(math.radians(ang))
        fy = cy + sy * dist * math.sin(math.radians(ang))
        draw_flower(draw, int(fx), int(fy), petals=6,
                    petal_len=int(19*s), petal_w=int(9*s),
                    color_outer=col, color_center=OURO_SUAVE, center_r=int(6*s))

    # Flores minusculas
    for ang, dist, col in [(22, int(82*s), PESSEGO), (66, int(82*s), PESSEGO)]:
        fx = cx + sx * dist * math.cos(math.radians(ang))
        fy = cy + sy * dist * math.sin(math.radians(ang))
        draw_flower(draw, int(fx), int(fy), petals=5,
                    petal_len=int(10*s), petal_w=int(5*s),
                    color_outer=col, color_center=OURO_SUAVE, center_r=int(3*s))

    # Folhas
    for ang, dist in [(14, int(70*s)), (76, int(70*s)), (38, int(92*s)), (54, int(92*s))]:
        lx = cx + sx * dist * math.cos(math.radians(ang))
        ly = cy + sy * dist * math.sin(math.radians(ang))
        draw_leaf(draw, int(lx), int(ly), ang * sx,
                  length=int(22*s), width=int(9*s), color=VERDE)

# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------
def build_post():
    W, H = 1080, 1080

    # === FOTO FULL-BLEED ===
    foto_raw = Image.open(FOTO_PATH).convert("RGB")
    foto_raw = ImageEnhance.Brightness(foto_raw).enhance(1.10)
    foto_raw = ImageEnhance.Color(foto_raw).enhance(1.20)
    foto_raw = ImageEnhance.Contrast(foto_raw).enhance(1.05)

    fw, fh = foto_raw.size
    # Crop para quadrado, centralizado
    side = min(fw, fh)
    l = (fw - side) // 2
    t = (fh - side) // 2
    foto_sq = foto_raw.crop((l, t, l + side, t + side))
    img = foto_sq.resize((W, H), Image.LANCZOS)

    # === GRADIENT OVERLAY (terco inferior) ===
    # Creme emergindo do fundo para legibilidade do texto
    grad_h  = 460
    grad_y0 = H - grad_h
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    cr, cg, cb = CREME
    for dy in range(grad_h):
        t = dy / (grad_h - 1)
        # curva mais agressiva para boa base sob o painel de texto
        alpha = int((t ** 0.60) * 248)
        draw_ov.line([(0, grad_y0 + dy), (W - 1, grad_y0 + dy)],
                     fill=(cr, cg, cb, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    img      = img_rgba.convert("RGB")
    draw     = ImageDraw.Draw(img)

    # === PAINEL SEMI-OPACO PARA LEGIBILIDADE DO TEXTO ===
    _ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    _d  = ImageDraw.Draw(_ov)
    _d.rounded_rectangle(
        [55, H - 412, W - 55, H - 28],
        radius=24,
        fill=(*CREME, 210),
        outline=(*OURO_SUAVE, 185),
        width=1,
    )
    img  = Image.alpha_composite(img.convert("RGBA"), _ov).convert("RGB")
    draw = ImageDraw.Draw(img)

    # === BORDAS DOURADAS DUPLAS ===
    m1, m2 = 14, 22
    draw.rounded_rectangle([m1, m1, W-m1, H-m1], radius=28,
                            fill=None, outline=OURO_CLARO, width=2)
    draw.rounded_rectangle([m2, m2, W-m2, H-m2], radius=22,
                            fill=None, outline=OURO_SUAVE,  width=1)

    # === ORNAMENTOS NOS 4 CANTOS ===
    off = 68
    draw_corner_ornament(draw, off,     off,     flip_x=False, flip_y=False, scale=1.00)
    draw_corner_ornament(draw, W - off, off,     flip_x=True,  flip_y=False, scale=1.00)
    draw_corner_ornament(draw, off,     H - off, flip_x=False, flip_y=True,  scale=0.88)
    draw_corner_ornament(draw, W - off, H - off, flip_x=True,  flip_y=True,  scale=0.88)

    # === COPY (sobre o gradiente) ===
    cx = W // 2

    # -- Script: "sua festa merece" --
    script_text = "sua festa merece"
    s_bbox = draw.textbbox((0, 0), script_text, font=fnt_script)
    sw     = s_bbox[2] - s_bbox[0]
    sh     = s_bbox[3] - s_bbox[1]
    sy_pos = H - 370
    draw.text((cx - sw // 2, sy_pos), script_text, font=fnt_script, fill=TXT_M)

    # -- Titulo: "Feito a mao" --
    title_text = "Feito à mão"   # "Feito à mão"
    t_bbox = draw.textbbox((0, 0), title_text, font=fnt_title)
    tw     = t_bbox[2] - t_bbox[0]
    th     = t_bbox[3] - t_bbox[1]
    ty_pos = sy_pos + sh + 12
    draw.text((cx - tw // 2, ty_pos), title_text, font=fnt_title, fill=TXT)

    # -- Divisor dourado com losango --
    div_y     = ty_pos + th + 12
    line_half = 82
    draw.line([(cx - line_half, div_y), (cx - 13, div_y)], fill=OURO_CLARO, width=2)
    draw.line([(cx + 13,        div_y), (cx + line_half, div_y)], fill=OURO_CLARO, width=2)
    d = 5
    draw.polygon([(cx, div_y - d), (cx + d, div_y), (cx, div_y + d), (cx - d, div_y)],
                 fill=OURO)

    # -- Sub: "Salgados artesanais por encomenda" --
    sub_text = "Salgados artesanais por encomenda"
    sub_bbox = draw.textbbox((0, 0), sub_text, font=fnt_sub)
    subw     = sub_bbox[2] - sub_bbox[0]
    subh     = sub_bbox[3] - sub_bbox[1]
    sub_y    = div_y + 16
    draw.text((cx - subw // 2, sub_y), sub_text, font=fnt_sub, fill=TXT_M)

    # -- Pill CTA: "Festa Junina  Garanta sua data" --
    detail_text = "Temporada de festas  ·  Garante sua data"
    d_bbox  = draw.textbbox((0, 0), detail_text, font=fnt_detail)
    dw      = d_bbox[2] - d_bbox[0]
    dh      = d_bbox[3] - d_bbox[1]
    det_y   = sub_y + subh + 18
    pad_x, pad_y = 22, 10
    draw.rounded_rectangle(
        [cx - dw // 2 - pad_x, det_y - pad_y,
         cx + dw // 2 + pad_x, det_y + dh + pad_y],
        radius=20, fill=PESSEGO, outline=OURO_SUAVE, width=1
    )
    draw.text((cx - dw // 2, det_y), detail_text, font=fnt_detail, fill=TXT_M)

    # -- Marca --
    brand_text = "Ok Delícias com Amor"   # "Ok Delícias com Amor"
    b_bbox  = draw.textbbox((0, 0), brand_text, font=fnt_brand)
    bw      = b_bbox[2] - b_bbox[0]
    brand_y = H - 58
    draw.line([(cx - 72, brand_y - 10), (cx + 72, brand_y - 10)],
              fill=OURO_SUAVE, width=1)
    draw.text((cx - bw // 2, brand_y), brand_text, font=fnt_brand, fill=OURO)

    # === SALVAR ===
    img = img.convert("RGB")
    img.save(OUTPUT, "PNG", quality=98)
    print(f"Salvo: {OUTPUT}")
    return OUTPUT


if __name__ == "__main__":
    result = build_post()
    print("Concluido:", result)
