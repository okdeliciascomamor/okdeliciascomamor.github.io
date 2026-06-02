# -*- coding: utf-8 -*-
"""
5 Stories de Storytelling — Ok Delícias com Amor — 02/06/2026
REDESIGN v2 (leitura em primeiro lugar).

Texto num painel claro (cartao) com sombra suave e fio dourado, pra leitura
descolar do fundo. Titulo em Lora Bold (legivel), corpo em Lora Italico,
acento em Cormorant. Numeral de capitulo suave so no topo (decorativo, longe
do texto). Moldura, flores de canto, regua, ornamento de fecho e carimbo
"agora sim" mantidos. Italiana so no numeral e na assinatura.

Sem travessao. Sem a palavra "caixa". Tudo PIL puro.
"""
import os, math
from PIL import Image, ImageDraw, ImageFilter
from stories_maio30 import (
    load_font, bg_grad, draw_flower, draw_leaf, diamond, progress_indicator,
    crop_cover, W, H, CREME, CREME_F, BEGE, BEGE_E, PESSEGO, AMBAR, OURO,
    OURO_S, OURO_P, TERRA, LAVANDA, LAVANDA_E, LILAS_E, VERDE_BG1, VERDE_BG2,
    MUSGO, VERDE_S, VERDE_BORD, TXT, TXT_M,
)

BASE = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
        r"\Ok - Delicias com Amor")
M31 = os.path.join(BASE, "Material 31.05", "_work")
M30 = os.path.join(BASE, "Material 30.05")
PANEL_X0, PANEL_X1 = 64, W - 64
TXT_MAXW = (PANEL_X1 - PANEL_X0) - 120   # margem interna do cartao
PANEL_FILL = (255, 253, 248)


def A(rgb, a):
    return (rgb[0], rgb[1], rgb[2], a)


def wrap_lines(d, text, font, max_w=TXT_MAXW):
    words = text.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        bb = d.textbbox((0, 0), t, font=font)
        if bb[2] - bb[0] <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def block_h(d, lines, font, line_sp):
    h = 0
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=font)
        h += (bb[3] - bb[1]) + line_sp
    return h - line_sp if lines else 0


def draw_lines(d, lines, font, cx, top, fill, line_sp):
    y = top
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=font)
        lw = bb[2] - bb[0]; lh = bb[3] - bb[1]
        d.text((cx - lw // 2 - bb[0], y - bb[1]), ln, font=font, fill=fill)
        y += lh + line_sp
    return y


def fit_headline(d, text, start=92, floor=58, step=4, max_lines=2):
    s = start
    while s >= floor:
        f = load_font("Lora-Bold.ttf", s)
        if len(wrap_lines(d, text, f)) <= max_lines:
            return f
        s -= step
    return load_font("Lora-Bold.ttf", floor)


ICON_COL = (150, 110, 45)   # ouro-marrom de comida


def _poly(d, cx, cy, th, col, raw, width=3):
    xs = [p[0] for p in raw]; ys = [p[1] for p in raw]
    sc = th / (max(ys) - min(ys))
    ox = (min(xs) + max(xs)) / 2; oy = (min(ys) + max(ys)) / 2
    pts = [(cx + (x - ox) * sc, cy + (y - oy) * sc) for x, y in raw]
    pts.append(pts[0])
    d.line(pts, fill=col, width=width, joint="curve")


def icon_coxinha(d, cx, cy, th, col):
    # gota: bulbo redondo embaixo, ponta em cima
    R = 0.36; cyc = 0.16
    raw = [(0.0, -0.66)]   # apice (ponta)
    N = 44
    for i in range(N + 1):
        a = math.radians(-58 + (296) * i / N)   # arco inferior do bulbo
        raw.append((R * math.cos(a), cyc + R * math.sin(a)))
    _poly(d, cx, cy, th, col, raw)


def icon_empada(d, cx, cy, th, col):
    R = th / 2; pts = []
    for i in range(121):
        t = 2 * math.pi * i / 120
        rr = R * (1 + 0.16 * math.cos(8 * t))
        pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    pts.append(pts[0])
    d.line(pts, fill=col, width=3, joint="curve")
    for dx, dy, c in [(-R * 0.32, 0, (150, 175, 110)), (R * 0.26, -R * 0.16, (222, 150, 80)),
                      (0, R * 0.32, (228, 192, 92)), (R * 0.05, 0, (150, 175, 110))]:
        d.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5], fill=c)


def icon_pastel(d, cx, cy, th, col):
    R = th / 2
    d.arc([cx - R, cy - R, cx + R, cy + R], 0, 180, fill=col, width=3)
    d.line([(cx - R, cy), (cx + R, cy)], fill=col, width=3)
    for k in range(-3, 4):
        x = cx + k * (R / 3.4)
        d.line([(x, cy), (x, cy - 8)], fill=col, width=2)


def icon_canudo(d, cx, cy, th, col):
    R = th / 2
    ang = math.radians(-32); dx, dy = math.cos(ang), math.sin(ang)
    px, py = -dy, dx; w = R * 0.44; L = th * 0.96
    x0, y0 = cx - dx * L / 2, cy - dy * L / 2
    x1, y1 = cx + dx * L / 2, cy + dy * L / 2
    d.line([(x0 + px * w, y0 + py * w), (x1 + px * w, y1 + py * w)], fill=col, width=3)
    d.line([(x0 - px * w, y0 - py * w), (x1 - px * w, y1 - py * w)], fill=col, width=3)
    d.line([(x0 + px * w, y0 + py * w), (x0 - px * w, y0 - py * w)], fill=col, width=3)
    d.ellipse([x1 - w, y1 - w, x1 + w, y1 + w], outline=col, width=3)
    d.ellipse([x1 - w * 0.4, y1 - w * 0.4, x1 + w * 0.4, y1 + w * 0.4], fill=col)


def icon_trio(d, cx, cy, th, col):
    R = th / 2
    d.ellipse([cx - R, cy + R * 0.18, cx + R, cy + R * 0.78], outline=col, width=3)
    for off in (-R * 0.52, 0, R * 0.52):
        icon_coxinha(d, cx + off, cy - R * 0.04, th * 0.42, col)


ICONS = {"coxinha": icon_coxinha, "empada": icon_empada, "pastel": icon_pastel,
         "canudo": icon_canudo, "trio": icon_trio}


def emblem(d, cx, cy, kind, ring_col):
    r = 96
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ring_col, width=3)
    d.ellipse([cx - r + 9, cy - r + 9, cx + r - 9, cy + r - 9], outline=ring_col, width=1)
    diamond(d, cx - r - 24, cy, 6, ring_col)
    diamond(d, cx + r + 24, cy, 6, ring_col)
    ICONS[kind](d, cx, cy, 104, ICON_COL)


def photo_emblem(base, d, cx, cy, path, ring_col, fx=0.5, fy=0.5):
    r = 100
    # sombra suave
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([cx - r, cy - r + 8, cx + r, cy + r + 8],
                               fill=(70, 50, 22, 70))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    # mat creme
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PANEL_FILL)
    rp = r - 8
    photo = crop_cover(path, 2 * rp, 2 * rp, fx, fy)
    mask = Image.new("L", (2 * rp, 2 * rp), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 2 * rp - 1, 2 * rp - 1], fill=255)
    base.paste(photo, (cx - rp, cy - rp), mask)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ring_col, width=4)
    d.ellipse([cx - r - 9, cy - r - 9, cx + r + 9, cy + r + 9], outline=OURO_P, width=2)
    diamond(d, cx - r - 28, cy, 6, ring_col)
    diamond(d, cx + r + 28, cy, 6, ring_col)


def panel_shadow(rect):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([rect[0], rect[1] + 14, rect[2], rect[3] + 14],
                         radius=30, fill=(70, 50, 22, 70))
    return layer.filter(ImageFilter.GaussianBlur(22))


def regua(d, cx, cy, acc):
    d.line([(cx - 130, cy), (cx - 28, cy)], fill=acc, width=2)
    d.line([(cx + 28, cy), (cx + 130, cy)], fill=acc, width=2)
    diamond(d, cx, cy, 8, acc)


def ornamento_fecho(d, cx, cy, acc):
    d.line([(cx - 96, cy), (cx - 26, cy)], fill=acc, width=2)
    d.line([(cx + 26, cy), (cx + 96, cy)], fill=acc, width=2)
    diamond(d, cx, cy, 8, acc)
    draw_leaf(d, cx - 116, cy, 200, 15, 6)
    draw_leaf(d, cx + 116, cy, 340, 15, 6)


def cantos(d, col_a, col_b):
    draw_flower(d, 70, 100, petals=6, plen=20, pw=9, col_out=col_a, col_mid=OURO_P, cr=6)
    draw_leaf(d, 52, 122, 235, 18, 7); draw_leaf(d, 88, 122, 305, 14, 6)
    draw_flower(d, W - 70, 100, petals=6, plen=20, pw=9, col_out=col_b, col_mid=OURO_P, cr=6)
    draw_leaf(d, W - 88, 122, 235, 14, 6); draw_leaf(d, W - 52, 122, 305, 18, 7)
    draw_flower(d, 70, H - 120, petals=6, plen=13, pw=6, col_out=col_b, col_mid=OURO_P, cr=5)
    draw_flower(d, W - 70, H - 120, petals=6, plen=13, pw=6, col_out=col_b, col_mid=OURO_P, cr=5)


def border(d, col):
    d.rounded_rectangle([16, 16, W - 16, H - 16], radius=32, outline=col, width=2)
    d.rounded_rectangle([26, 26, W - 26, H - 26], radius=24,
                        outline=(col[0] // 2, col[1] // 2, col[2] // 2), width=1)


def rodape(d):
    f = load_font("Italiana-Regular.ttf", 46)
    s = "Ok Delícias com Amor"
    bb = d.textbbox((0, 0), s, font=f)
    d.text((W // 2 - (bb[2] - bb[0]) // 2 - bb[0], H - 108 - bb[1]), s, font=f, fill=TXT_M)


def selo_agora_sim(base, cx, cy, acc):
    sl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sl)
    ew, eh = 460, 200
    sd.ellipse([cx - ew // 2, cy - eh // 2, cx + ew // 2, cy + eh // 2],
               outline=A(acc, 255), width=4)
    sd.ellipse([cx - ew // 2 + 13, cy - eh // 2 + 13, cx + ew // 2 - 13, cy + eh // 2 - 13],
               outline=A(acc, 165), width=2)
    f = load_font("Italiana-Regular.ttf", 78)
    s = "agora sim."
    bb = sd.textbbox((0, 0), s, font=f)
    tw = bb[2] - bb[0]; th = bb[3] - bb[1]
    sd.text((cx - tw // 2 - bb[0], cy - th // 2 - bb[1]), s, font=f, fill=A(acc, 255))
    diamond(sd, cx - tw // 2 - 44, cy, 7, A(acc, 255))
    diamond(sd, cx + tw // 2 + 44, cy, 7, A(acc, 255))
    sl = sl.rotate(-4, resample=Image.BICUBIC, center=(cx, cy))
    return Image.alpha_composite(base, sl)


def tela(cfg):
    base = bg_grad(cfg["bg"][0], cfg["bg"][1]).convert("RGBA")
    md = ImageDraw.Draw(base)
    cx = W // 2

    # medir bloco de texto
    acc_font = load_font("CormorantGaramond-SemiBoldItalic.ttf", 58)
    acc_lines = wrap_lines(md, cfg["acento"], acc_font) if cfg.get("acento") else []
    t_font = fit_headline(md, cfg["titulo"])
    t_lines = wrap_lines(md, cfg["titulo"], t_font)
    body_font = load_font("Lora-Italic.ttf", 42)
    b_lines = wrap_lines(md, cfg["corpo"], body_font)

    acc_h = block_h(md, acc_lines, acc_font, 6) if acc_lines else 0
    t_h = block_h(md, t_lines, t_font, 12)
    b_h = block_h(md, b_lines, body_font, 12)
    g1 = 18 if acc_lines else 0
    g2 = 78
    block = acc_h + g1 + t_h + g2 + b_h

    pad = 70
    panel_cy = 905
    panel_h = block + pad * 2
    p_top = panel_cy - panel_h // 2
    p_bot = panel_cy + panel_h // 2
    rect = [PANEL_X0, p_top, PANEL_X1, p_bot]

    # sombra + painel
    base = Image.alpha_composite(base, panel_shadow(rect))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(rect, radius=30, fill=PANEL_FILL)
    d.rounded_rectangle(rect, radius=30, outline=cfg["acc"], width=2)
    d.rounded_rectangle([rect[0] + 9, rect[1] + 9, rect[2] - 9, rect[3] - 9],
                        radius=24, outline=A(cfg["acc"], 90), width=1)

    cantos(d, cfg["flw_a"], cfg["flw_b"])
    photo_emblem(base, d, cx, 300, cfg["photo"], cfg["acc"],
                 cfg.get("fx", 0.5), cfg.get("fy", 0.5))

    # texto no painel
    y = p_top + pad
    if acc_lines:
        draw_lines(d, acc_lines, acc_font, cx, y, cfg["acc"], 6)
        y += acc_h + g1
    draw_lines(d, t_lines, t_font, cx, y, TXT, 12)
    y += t_h
    regua(d, cx, y + g2 // 2, cfg["acc"])
    y += g2
    draw_lines(d, b_lines, body_font, cx, y, cfg["corpo_col"], 12)

    # fecho abaixo do painel
    if cfg.get("selo"):
        base = selo_agora_sim(base, cx, p_bot + 110, cfg["acc"])
        d = ImageDraw.Draw(base)
    else:
        ornamento_fecho(d, cx, p_bot + 90, cfg["acc"])

    progress_indicator(d, cfg["n"], 5, cfg["acc"])
    rodape(d)
    border(d, cfg["border"])

    out = os.path.join(BASE, "02 - Criativos", "junho02", f"story_junho02_{cfg['n']}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    base.convert("RGB").save(out, "PNG", quality=98)
    print("Salvo:", out)


CFGS = [
    dict(n=1, icon="coxinha", photo=os.path.join(M31, "IMG_8435.jpg"), fy=0.45,
         bg=(CREME, CREME_F), acc=OURO, border=OURO_S,
         flw_a=(222, 188, 130), flw_b=(210, 178, 120),
         acento="senta que tem história,",
         titulo="a mãe da Oli nunca mediu o sal.",
         corpo="a Dona Wilma molhava o dedo na massa, provava, fechava os olhos um instante, e dizia: agora sim.",
         corpo_col=TXT_M),
    dict(n=2, icon="empada", photo=os.path.join(M30, "Canoinha de legumes 1.jpeg"), fy=0.5,
         bg=(CREME, LAVANDA), acc=LILAS_E, border=LAVANDA_E,
         flw_a=(200, 180, 220), flw_b=(190, 168, 215),
         acento=None,
         titulo="um dia, a Oli se pegou fazendo igual.",
         corpo="o mesmo dedo, os mesmos olhos fechando sozinhos. ela não aprendeu isso. ela recebeu da mãe.",
         corpo_col=(86, 64, 116)),
    dict(n=3, icon="pastel", photo=os.path.join(M31, "IMG_8436.jpg"), fy=0.5,
         bg=(PESSEGO, AMBAR), acc=TERRA, border=OURO_S,
         flw_a=(232, 180, 130), flw_b=(225, 168, 120),
         acento=None,
         titulo="o dom veio dela.",
         corpo="a receita, o ponto, o jeito de fazer com amor. mais de 40 anos que hoje vivem na mão da Oli.",
         corpo_col=(110, 68, 40)),
    dict(n=4, icon="canudo", photo=os.path.join(M31, "IMG_8437.jpg"), fy=0.5,
         bg=(VERDE_BG1, VERDE_BG2), acc=MUSGO, border=VERDE_BORD,
         flw_a=(178, 202, 150), flw_b=(165, 190, 135),
         acento=None,
         titulo="por isso a gente faz à mão.",
         corpo="não pra ser mais rápido, pra ser mais nosso. e todo dia a gente agradece a Deus pelo dom que veio da Dona Wilma.",
         corpo_col=(64, 86, 48)),
    dict(n=5, icon="trio", photo=os.path.join(M31, "IMG_8438.jpg"), fy=0.5,
         bg=(PESSEGO, AMBAR), acc=OURO, border=OURO_S,
         flw_a=(220, 185, 120), flw_b=(205, 168, 100),
         acento=None,
         titulo="junho é de juntar.",
         corpo="essa semana, chama alguém pra dentro de casa. a gente cuida dos salgados, tu cuidas do reencontro.",
         corpo_col=(104, 74, 36), selo=True),
]


if __name__ == "__main__":
    for cfg in CFGS:
        tela(cfg)
    print("5 Stories storytelling 02/06 (redesign v2, leitura) prontos.")
