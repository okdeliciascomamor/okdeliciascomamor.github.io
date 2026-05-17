"""
Post Ok Delicias com Amor - 17/05/2026
Angulo 2: Desejo
Tema: "A mesa que as pessoas param para fotografar"
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math
import os

# -------------------------------------------------------------------
# CAMINHOS
# -------------------------------------------------------------------
BASE_DIR = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FONTS_DIR = r"C:\Users\nasci\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\ffaf7eb1-e899-4b15-8564-46cec1055316\c0cd45e2-3d2e-40a4-a7fe-06fecc44a961\skills\canvas-design\canvas-fonts"
FOTO_PATH = os.path.join(BASE_DIR, "fotos", "WhatsApp_Image_2026-05-05_at_16.52.18.jpeg")
OUTPUT_PATH = os.path.join(BASE_DIR, "post_maio17.png")

# -------------------------------------------------------------------
# PALETA
# -------------------------------------------------------------------
LAVANDA     = (230, 222, 245)
CREME       = (255, 248, 234)
OURO        = (195, 152, 58)
OURO_CLARO  = (220, 185, 95)
OURO_SUAVE  = (240, 210, 130)
ROSA        = (240, 208, 220)
LILAS       = (208, 182, 228)
PESSEGO     = (255, 232, 192)
VERDE       = (148, 172, 124)
VERDE_ESC   = (100, 130, 80)
TXT         = (58, 40, 18)
TXT_M       = (98, 70, 36)
BRANCO      = (255, 255, 255)

# -------------------------------------------------------------------
# FONTES
# -------------------------------------------------------------------
def load_font(name, size):
    path = os.path.join(FONTS_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except Exception as e:
        print(f"AVISO: fonte {name} nao carregou ({e}), usando default.")
        return ImageFont.load_default()

fnt_script   = load_font("NothingYouCouldDo-Regular.ttf", 52)
fnt_title    = load_font("Italiana-Regular.ttf", 88)
fnt_sub      = load_font("Lora-Italic.ttf", 36)
fnt_detail   = load_font("InstrumentSans-Regular.ttf", 26)
fnt_brand    = load_font("Italiana-Regular.ttf", 34)

# -------------------------------------------------------------------
# HELPERS GEOMETRICOS
# -------------------------------------------------------------------

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def gradient_rect(img, x0, y0, x1, y1, color_top, color_bot):
    draw = ImageDraw.Draw(img)
    h = y1 - y0
    for dy in range(h):
        t = dy / max(h - 1, 1)
        c = lerp_color(color_top, color_bot, t)
        draw.line([(x0, y0 + dy), (x1, y0 + dy)], fill=c)

# -------------------------------------------------------------------
# FLORES DECORATIVAS
# -------------------------------------------------------------------

def draw_petal(draw, cx, cy, angle_deg, length, width, color):
    angle = math.radians(angle_deg)
    px = cx + length * math.cos(angle)
    py = cy + length * math.sin(angle)
    perp = math.radians(angle_deg + 90)
    ox = (width / 2) * math.cos(perp)
    oy = (width / 2) * math.sin(perp)
    poly = [
        (cx + ox, cy + oy),
        (px + ox * 0.3, py + oy * 0.3),
        (px, py),
        (px - ox * 0.3, py - oy * 0.3),
        (cx - ox, cy - oy),
    ]
    draw.polygon(poly, fill=color)

def draw_flower(draw, cx, cy, petals=8, petal_len=22, petal_w=10,
                color_outer=None, color_center=None, center_r=7):
    if color_outer is None:
        color_outer = ROSA
    if color_center is None:
        color_center = OURO_SUAVE
    for i in range(petals):
        angle = 360 / petals * i
        draw_petal(draw, cx, cy, angle, petal_len, petal_w, color_outer)
    draw.ellipse([cx - center_r, cy - center_r, cx + center_r, cy + center_r],
                 fill=color_center)

def draw_leaf(draw, cx, cy, angle_deg, length=18, width=8, color=None):
    if color is None:
        color = VERDE
    draw_petal(draw, cx, cy, angle_deg, length, width, color)
    draw_petal(draw, cx, cy, angle_deg + 180, length * 0.5, width * 0.6, color)

def draw_corner_ornament(draw, cx, cy, flip_x=False, flip_y=False):
    sx = -1 if flip_x else 1
    sy = -1 if flip_y else 1

    # Flor central do canto
    draw_flower(draw, cx, cy, petals=8, petal_len=24, petal_w=11,
                color_outer=LILAS, color_center=OURO_SUAVE)

    # Flores pequenas ao redor
    for ang, dist, col in [
        (45, 38, ROSA), (90, 44, LILAS), (0, 44, ROSA),
    ]:
        fx = cx + sx * dist * math.cos(math.radians(ang))
        fy = cy + sy * dist * math.sin(math.radians(ang))
        draw_flower(draw, int(fx), int(fy), petals=6, petal_len=14, petal_w=7,
                    color_outer=col, color_center=OURO_SUAVE, center_r=4)

    # Folhas
    for ang, dist in [(20, 52), (70, 52)]:
        lx = cx + sx * dist * math.cos(math.radians(ang))
        ly = cy + sy * dist * math.sin(math.radians(ang))
        draw_leaf(draw, int(lx), int(ly), 45 * sx, length=18, width=7, color=VERDE)
        draw_leaf(draw, int(lx), int(ly), 135 * sx, length=14, width=6, color=VERDE_ESC)

# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------

def build_post():
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H), CREME)

    # --- FUNDO GRADIENTE LAVANDA -> CREME ---
    gradient_rect(img, 0, 0, W, H, LAVANDA, CREME)

    draw = ImageDraw.Draw(img)

    # --- BORDA DOURADA FINA EXTERNA ---
    margin = 18
    draw_rounded_rect(draw, [margin, margin, W - margin, H - margin],
                      radius=28, fill=None, outline=OURO_CLARO, width=2)

    # --- ORNAMENTOS NOS 4 CANTOS ---
    off = 56
    draw_corner_ornament(draw, off, off, flip_x=False, flip_y=False)
    draw_corner_ornament(draw, W - off, off, flip_x=True, flip_y=False)
    draw_corner_ornament(draw, off, H - off, flip_x=False, flip_y=True)
    draw_corner_ornament(draw, W - off, H - off, flip_x=True, flip_y=True)

    # --- FOTO DO PRODUTO ---
    foto_raw = Image.open(FOTO_PATH).convert("RGB")

    # Ajuste de brilho e cor
    foto_raw = ImageEnhance.Brightness(foto_raw).enhance(1.10)
    foto_raw = ImageEnhance.Color(foto_raw).enhance(1.12)

    # Crop quadrado centralizado
    fw, fh = foto_raw.size
    side = min(fw, fh)
    left = (fw - side) // 2
    top = (fh - side) // 2
    foto_sq = foto_raw.crop((left, top, left + side, top + side))

    # Tamanho da moldura da foto
    foto_w = 580
    foto_h = 520
    foto_resized = foto_sq.resize((foto_w, foto_h), Image.LANCZOS)

    foto_x = (W - foto_w) // 2
    foto_y = 80

    # Sombra suave
    shadow = Image.new("RGBA", (foto_w + 16, foto_h + 16), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([8, 8, foto_w + 8, foto_h + 8], radius=28,
                             fill=(40, 20, 10, 80))
    shadow_blur = shadow.filter(ImageFilter.GaussianBlur(12))
    img.paste(shadow_blur.convert("RGB"), (foto_x - 8, foto_y - 8),
              mask=shadow_blur.split()[3])

    # Moldura creme arredondada
    frame_pad = 8
    frame_layer = Image.new("RGBA", (foto_w + frame_pad * 2, foto_h + frame_pad * 2),
                            (255, 255, 255, 0))
    fdraw = ImageDraw.Draw(frame_layer)
    fdraw.rounded_rectangle([0, 0, foto_w + frame_pad * 2 - 1,
                              foto_h + frame_pad * 2 - 1],
                             radius=32, fill=(255, 248, 234, 255))
    img.paste(frame_layer.convert("RGB"),
              (foto_x - frame_pad, foto_y - frame_pad),
              mask=frame_layer.split()[3])

    # Foto com máscara arredondada
    mask = Image.new("L", (foto_w, foto_h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, foto_w - 1, foto_h - 1], radius=26, fill=255)
    img.paste(foto_resized, (foto_x, foto_y), mask=mask)

    # Borda dourada na foto
    fdraw2 = ImageDraw.Draw(img)
    fdraw2.rounded_rectangle([foto_x - 1, foto_y - 1, foto_x + foto_w, foto_y + foto_h],
                              radius=27, fill=None, outline=OURO_CLARO, width=2)

    # --- PAINEL CREME INFERIOR ---
    panel_y = foto_y + foto_h + 22
    panel_h = H - panel_y - 28
    panel_x0, panel_x1 = 48, W - 48

    draw_rounded_rect(draw, [panel_x0, panel_y, panel_x1, panel_y + panel_h],
                      radius=22, fill=(255, 252, 242, 255) if False else CREME)
    # Redesenhar com PIL direto (rounded_rectangle nao aceita alpha aqui)
    draw.rounded_rectangle([panel_x0, panel_y, panel_x1, panel_y + panel_h],
                            radius=22, fill=CREME, outline=OURO_SUAVE, width=1)

    # --- COPY ---
    cx = W // 2

    # Script: "sua festa merece"
    script_text = "sua festa merece"
    bbox = draw.textbbox((0, 0), script_text, font=fnt_script)
    sw = bbox[2] - bbox[0]
    sy_pos = panel_y + 22
    draw.text((cx - sw // 2, sy_pos), script_text, font=fnt_script, fill=TXT_M)

    # Titulo grande: "Feito a mao"
    title_text = "Feito a mao"
    # Usar à (a com crase) via Unicode
    title_text = "Feito à mão"
    bbox = draw.textbbox((0, 0), title_text, font=fnt_title)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    ty_pos = sy_pos + 52
    draw.text((cx - tw // 2, ty_pos), title_text, font=fnt_title, fill=TXT)

    # Linha dourada + ornamento divisor
    div_y = ty_pos + th + 18
    line_half = 90
    draw.line([(cx - line_half, div_y), (cx - 14, div_y)],
              fill=OURO_CLARO, width=2)
    draw.line([(cx + 14, div_y), (cx + line_half, div_y)],
              fill=OURO_CLARO, width=2)
    # Losango central
    d = 5
    draw.polygon([(cx, div_y - d), (cx + d, div_y), (cx, div_y + d), (cx - d, div_y)],
                 fill=OURO)

    # Sub: "Salgados artesanais por encomenda"
    sub_text = "Salgados artesanais por encomenda"
    bbox = draw.textbbox((0, 0), sub_text, font=fnt_sub)
    subw = bbox[2] - bbox[0]
    sub_y = div_y + 20
    draw.text((cx - subw // 2, sub_y), sub_text, font=fnt_sub, fill=TXT_M)

    # Detalhe menor: "Festa Junina · Garanta sua data"
    detail_text = "Festa Junina  ·  Garanta sua data"
    bbox = draw.textbbox((0, 0), detail_text, font=fnt_detail)
    dw = bbox[2] - bbox[0]
    dh = bbox[3] - bbox[1]
    detail_y = sub_y + 52
    # Pill de fundo dourado
    pill_pad_x, pill_pad_y = 20, 8
    draw.rounded_rectangle(
        [cx - dw // 2 - pill_pad_x, detail_y - pill_pad_y,
         cx + dw // 2 + pill_pad_x, detail_y + dh + pill_pad_y],
        radius=16, fill=PESSEGO, outline=OURO_SUAVE, width=1
    )
    draw.text((cx - dw // 2, detail_y), detail_text, font=fnt_detail, fill=TXT_M)

    # Marca: "Ok Delicias com Amor"
    brand_text = "Ok Delícias com Amor"
    bbox = draw.textbbox((0, 0), brand_text, font=fnt_brand)
    bw = bbox[2] - bbox[0]
    brand_y = panel_y + panel_h - 52
    draw.text((cx - bw // 2, brand_y), brand_text, font=fnt_brand, fill=OURO)

    # Linha fina acima da marca
    draw.line([(cx - 80, brand_y - 10), (cx + 80, brand_y - 10)],
              fill=OURO_SUAVE, width=1)

    # --- SALVAR ---
    img = img.convert("RGB")
    img.save(OUTPUT_PATH, "PNG", quality=98)
    print(f"Post salvo em: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    result = build_post()
    print("Concluido:", result)
