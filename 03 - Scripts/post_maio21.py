"""
Post Ok Delicias com Amor - 21/05/2026
Conceito: Prova Social — convidados que lembram da festa pela comida
Layout: foto em arco (arch) no topo, painel de texto editorial abaixo
Foto: IMG_1142.JPEG (3 sabores de empada com forminhas de renda + panelinha vintage)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math, os

BASE_DIR  = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR = r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts"
FOTO_PATH = os.path.join(BASE_DIR, "fotos", "IMG_1142.JPEG")
OUTPUT    = os.path.join(BASE_DIR, "post_maio21.png")

CREME      = (255, 248, 234)
LAVANDA    = (230, 222, 248)
LAVANDA_M  = (196, 181, 224)
OURO       = (179, 138, 52)
OURO_S     = (210, 175, 100)
OURO_P     = (235, 210, 155)
ROSA       = (240, 208, 220)
PESSEGO    = (255, 232, 192)
VERDE      = (148, 172, 124)
VERDE_E    = (100, 130,  80)
TXT        = ( 32,  18,   6)
TXT_M      = ( 72,  50,  22)

W, H = 1080, 1350

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

def draw_flower(draw, cx, cy, petals=6, plen=12, pw=6,
                col_out=None, col_mid=None, cr=4):
    if col_out is None: col_out = ROSA
    if col_mid is None: col_mid = OURO_P
    for i in range(petals):
        draw_petal(draw, cx, cy, 360/petals*i, plen, pw, col_out)
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=col_mid)

def draw_leaf(draw, cx, cy, angle_deg, length=12, width=5):
    draw_petal(draw, cx, cy, angle_deg,     length,     width,    VERDE)
    draw_petal(draw, cx, cy, angle_deg+180, length*.4,  width*.5, VERDE_E)

def diamond(draw, cx, cy, size, color):
    draw.polygon([(cx,cy-size),(cx+size,cy),(cx,cy+size),(cx-size,cy)], fill=color)

def build_post():
    # === FUNDO: gradiente creme -> lavanda muito suave ===
    img = Image.new("RGB", (W, H), CREME)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        draw.line([(0,y),(W-1,y)], fill=lerp(CREME, LAVANDA, t * 0.32))

    # === FOTO EM ARCO (arch) ===
    # Arco: retangulo com topo arredondado em semicirculo
    arch_x      = 80          # margem lateral
    arch_top    = 60          # margem topo
    arch_w      = W - 2*arch_x
    arch_h      = 760          # altura total do arco
    arch_radius = arch_w // 2  # raio do semicirculo no topo

    # Recortar e redimensionar a foto para caber no arco
    foto = Image.open(FOTO_PATH).convert("RGB")
    foto = ImageEnhance.Brightness(foto).enhance(1.06)
    foto = ImageEnhance.Color(foto).enhance(1.15)
    foto = ImageEnhance.Sharpness(foto).enhance(1.2)

    fw, fh = foto.size
    # Zoom 30% + deslocamento para baixo — salgados em destaque, menos panelinha
    target_ratio = arch_w / arch_h
    if fw / fh > target_ratio:
        new_fw = int(fh * target_ratio)
        foto = foto.crop(((fw - new_fw)//2, 0, (fw + new_fw)//2, fh))
    else:
        new_fh = int(fw / target_ratio)
        foto = foto.crop((0, (fh - new_fh)//2, fw, (fh + new_fh)//2))
    foto = foto.resize((arch_w, arch_h), Image.LANCZOS)

    # Mascara em arco (retangulo + semicirculo no topo)
    mask = Image.new("L", (arch_w, arch_h), 0)
    md   = ImageDraw.Draw(mask)
    # Parte retangular (de arch_radius ate arch_h)
    md.rectangle([0, arch_radius, arch_w, arch_h], fill=255)
    # Semicirculo no topo
    md.ellipse([0, 0, arch_w, arch_w], fill=255)
    # Suaviza borda
    mask = mask.filter(ImageFilter.GaussianBlur(3))

    foto_rgba = Image.new("RGBA", (arch_w, arch_h), (0,0,0,0))
    foto_rgba.paste(foto, (0,0))
    foto_rgba.putalpha(mask)

    # Sombra suave embaixo do arco
    shadow = Image.new("RGBA", (W, H), (0,0,0,0))
    sd = ImageDraw.Draw(shadow)
    for s in range(18, 0, -1):
        a_val = int(8 * (1 - s/18))
        sd.rounded_rectangle(
            [arch_x+s, arch_top+s, arch_x+arch_w+s, arch_top+arch_h+s],
            radius=arch_radius, fill=(40,20,5,a_val))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")

    # Cola a foto
    img.paste(foto_rgba.convert("RGB"),
              (arch_x, arch_top), mask=foto_rgba.split()[3])

    draw = ImageDraw.Draw(img)

    # Borda do arco (linha dourada fina)
    # Usamos dois tracos: um retangulo arredondado tracado
    draw.rounded_rectangle(
        [arch_x-3, arch_top-3, arch_x+arch_w+3, arch_top+arch_h+3],
        radius=arch_radius+3, outline=OURO_S, width=2)
    draw.rounded_rectangle(
        [arch_x+4, arch_top+4, arch_x+arch_w-4, arch_top+arch_h-4],
        radius=arch_radius-4, outline=OURO_P, width=1)

    # Losangos nos 4 cantos do arco
    for px2, py2 in [
        (arch_x,          arch_top + arch_radius),  # esq meio
        (arch_x + arch_w, arch_top + arch_radius),  # dir meio
        (arch_x,          arch_top + arch_h),        # esq baixo
        (arch_x + arch_w, arch_top + arch_h),        # dir baixo
    ]:
        diamond(draw, px2, py2, 5, OURO)

    # Flores nos cantos inferiores do arco
    for fx, fy, col_o in [
        (arch_x - 18, arch_top + arch_h + 18, ROSA),
        (arch_x + arch_w + 18, arch_top + arch_h + 18, LAVANDA_M),
    ]:
        draw_flower(draw, fx, fy, petals=6, plen=14, pw=7, col_out=col_o, col_mid=OURO_P, cr=5)
        draw_leaf(draw, fx-16, fy+10, 225, length=13, width=6)
        draw_leaf(draw, fx+16, fy+10, 315, length=13, width=6)

    # Guirlanda floral discretissima ao longo do arco
    # Apenas nas laterais retas (nao no semicirculo)
    n_lat = 10
    for side, sign in [(-1, -1), (1, 1)]:
        for i in range(n_lat):
            t = (i + 0.5) / n_lat
            # Posicao ao longo da lateral reta
            fy2 = arch_top + arch_radius + t * (arch_h - arch_radius)
            fx2 = arch_x + (arch_w if side == 1 else 0) + sign * 22
            if i % 2 == 0:
                draw_flower(draw, int(fx2), int(fy2), petals=5, plen=9, pw=4,
                            col_out=ROSA if i % 4 == 0 else LAVANDA_M,
                            col_mid=OURO_P, cr=3)
            else:
                draw_leaf(draw, int(fx2), int(fy2), 90*side, length=10, width=4)

    # === DIVISOR ORNAMENTAL ===
    cx   = W // 2
    div_y = arch_top + arch_h + 36
    lhalf = 120
    draw.line([(cx-lhalf, div_y), (cx-14, div_y)], fill=OURO_S, width=1)
    draw.line([(cx+14, div_y),    (cx+lhalf, div_y)], fill=OURO_S, width=1)
    diamond(draw, cx, div_y, 5, OURO)
    draw_flower(draw, cx-lhalf-14, div_y, petals=5, plen=9, pw=4, col_out=LAVANDA_M, col_mid=OURO_P, cr=3)
    draw_flower(draw, cx+lhalf+14, div_y, petals=5, plen=9, pw=4, col_out=ROSA,      col_mid=OURO_P, cr=3)

    # === TIPOGRAFIA ===
    fnt_script = load_font("NothingYouCouldDo-Regular.ttf", 62)
    fnt_title  = load_font("Lora-Bold.ttf",           96)
    fnt_sub    = load_font("Lora-BoldItalic.ttf",     40)
    fnt_detail = load_font("InstrumentSans-Bold.ttf", 28)
    fnt_brand  = load_font("InstrumentSans-Bold.ttf", 30)

    base_y = div_y + 18

    # Script — 2 linhas, shadow mais visivel no fundo claro
    sc = "feito pra quem quer que os"
    sb = draw.textbbox((0,0), sc, font=fnt_script)
    draw.text((cx-(sb[2]-sb[0])//2+2, base_y+2), sc, font=fnt_script, fill=(180,155,110))
    draw.text((cx-(sb[2]-sb[0])//2,   base_y),   sc, font=fnt_script, fill=TXT_M)

    sc2 = "convidados lembrem da festa"
    sb2 = draw.textbbox((0,0), sc2, font=fnt_script)
    sc2_y = base_y + (sb[3]-sb[1]) + 6
    draw.text((cx-(sb2[2]-sb2[0])//2+2, sc2_y+2), sc2, font=fnt_script, fill=(180,155,110))
    draw.text((cx-(sb2[2]-sb2[0])//2,   sc2_y),   sc2, font=fnt_script, fill=TXT_M)

    # Titulo: "pela comida." — Lora-Bold com sombra sutil
    tt  = "pela comida."
    tb  = draw.textbbox((0,0), tt, font=fnt_title)
    ty  = sc2_y + (sb2[3]-sb2[1]) + 10
    tw  = tb[2] - tb[0]
    draw.text((cx - tw//2 + 3, ty + 3), tt, font=fnt_title, fill=(180, 155, 110))
    draw.text((cx - tw//2,     ty),     tt, font=fnt_title, fill=TXT)

    # Divisor ornamental
    dv2_y = ty + (tb[3]-tb[1]) + 14
    draw.line([(cx-80, dv2_y),(cx-14, dv2_y)], fill=OURO_S, width=2)
    draw.line([(cx+14, dv2_y),(cx+80, dv2_y)], fill=OURO_S, width=2)
    diamond(draw, cx, dv2_y, 5, OURO)

    # Sub — Lora-BoldItalic maior
    sub   = "Salgados artesanais por encomenda"
    sub_b = draw.textbbox((0,0), sub, font=fnt_sub)
    sub_y = dv2_y + 14
    draw.text((cx-(sub_b[2]-sub_b[0])//2, sub_y), sub, font=fnt_sub, fill=TXT_M)

    # Pill CTA — InstrumentSans-Bold maior
    det   = "Datas limitadas para junho"
    det_b = draw.textbbox((0,0), det, font=fnt_detail)
    dw, dh = det_b[2]-det_b[0], det_b[3]-det_b[1]
    det_y = sub_y + (sub_b[3]-sub_b[1]) + 16
    px3, py3 = 26, 10
    draw.rounded_rectangle(
        [cx-dw//2-px3, det_y-py3, cx+dw//2+px3, det_y+dh+py3],
        radius=22, fill=PESSEGO, outline=OURO_P, width=1)
    draw.text((cx-dw//2, det_y), det, font=fnt_detail, fill=TXT_M)

    # Marca
    br   = "Ok Delícias com Amor"
    br_b = draw.textbbox((0,0), br, font=fnt_brand)
    br_y = H - 52
    draw.line([(cx-70, br_y-10),(cx+70, br_y-10)], fill=OURO_P, width=1)
    draw.text((cx-(br_b[2]-br_b[0])//2, br_y), br, font=fnt_brand, fill=OURO)

    # === BORDA DUPLA ===
    draw.rounded_rectangle([14,14,W-14,H-14], radius=28, outline=OURO_S, width=2)
    draw.rounded_rectangle([22,22,W-22,H-22], radius=22, outline=OURO_P,  width=1)

    img.convert("RGB").save(OUTPUT, "PNG", quality=98)
    print(f"Salvo: {OUTPUT}")

if __name__ == "__main__":
    build_post()
