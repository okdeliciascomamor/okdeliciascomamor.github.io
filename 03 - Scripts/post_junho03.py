# -*- coding: utf-8 -*-
"""
POST de feed 1080x1080 — Ok Delícias com Amor — 03/06/2026
Abertura do mes: "Junho e de juntar".

Copy: Copy Chief (squad de copy). Direcao de arte: Design Chief (squad de design).
Sintese e implementacao aqui. Leitura primeiro (cartao claro), foto-heroi real
(mini hamburgueres fartos), moldura e flores da marca.
Sem travessao. Sem a palavra "caixa".
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from stories_maio30 import (
    load_font, draw_flower, draw_leaf, diamond, crop_cover,
    CREME, LAVANDA, LAVANDA_E, PESSEGO, AMBAR, OURO, OURO_S, OURO_P, TERRA,
    VERDE_S, MUSGO, TXT, TXT_M, BRANCO,
)

W = H = 1080
BASE = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
        r"\Ok - Delicias com Amor")
FOTO = os.path.join(BASE, "MIni Hamburgueres.jpeg")
PANEL_FILL = (255, 253, 248)


def A(rgb, a):
    return (rgb[0], rgb[1], rgb[2], a)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def bg_grad(top, bot):
    img = Image.new("RGB", (W, H), top)
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(top, bot, y / (H - 1)))
    return img


def border(d, col):
    d.rounded_rectangle([16, 16, W - 16, H - 16], radius=30, outline=col, width=2)
    d.rounded_rectangle([26, 26, W - 26, H - 26], radius=22,
                        outline=(col[0] // 2, col[1] // 2, col[2] // 2), width=1)


def cantos(d):
    draw_flower(d, 64, 84, petals=6, plen=18, pw=8, col_out=(222, 188, 130), col_mid=OURO_P, cr=6)
    draw_leaf(d, 47, 104, 235, 16, 6); draw_leaf(d, 81, 104, 305, 13, 5)
    draw_flower(d, W - 64, 84, petals=6, plen=18, pw=8, col_out=(210, 178, 120), col_mid=OURO_P, cr=6)
    draw_leaf(d, W - 81, 104, 235, 13, 5); draw_leaf(d, W - 47, 104, 305, 16, 6)
    draw_flower(d, 64, H - 84, petals=6, plen=13, pw=6, col_out=(210, 178, 120), col_mid=OURO_P, cr=5)
    draw_flower(d, W - 64, H - 84, petals=6, plen=13, pw=6, col_out=(210, 178, 120), col_mid=OURO_P, cr=5)


def wrap_lines(d, text, font, maxw):
    words = text.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        bb = d.textbbox((0, 0), t, font=font)
        if bb[2] - bb[0] <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def block_h(d, lines, font, sp):
    h = 0
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=font); h += (bb[3] - bb[1]) + sp
    return h - sp if lines else 0


def draw_lines(d, lines, font, cx, top, fill, sp):
    y = top
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=font); lw = bb[2] - bb[0]; lh = bb[3] - bb[1]
        d.text((cx - lw // 2 - bb[0], y - bb[1]), ln, font=font, fill=fill)
        y += lh + sp
    return y


def fit_headline(d, text, maxw, start=92, floor=60, step=4):
    s = start
    while s >= floor:
        f = load_font("Lora-Bold.ttf", s)
        if len(wrap_lines(d, text, f, maxw)) <= 2:
            return f
        s -= step
    return load_font("Lora-Bold.ttf", floor)


def regua(d, cx, cy, acc):
    d.line([(cx - 120, cy), (cx - 28, cy)], fill=acc, width=2)
    d.line([(cx + 28, cy), (cx + 120, cy)], fill=acc, width=2)
    diamond(d, cx, cy, 7, acc)


def hero_photo(img, path, pw, ph, px, py, rad=34):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([px, py + 12, px + pw, py + ph + 12],
                                         radius=rad, fill=(60, 38, 14, 85))
    img = Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(16)))
    photo = crop_cover(path, pw, ph, 0.5, 0.5)
    photo = ImageEnhance.Brightness(photo).enhance(1.07)
    photo = ImageEnhance.Color(photo).enhance(1.12)
    photo = ImageEnhance.Contrast(photo).enhance(1.04)
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw, ph], radius=rad, fill=255)
    img = img.convert("RGB")
    img.paste(photo, (px, py), mask)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=rad, outline=OURO_S, width=3)
    d.rounded_rectangle([px + 7, py + 7, px + pw - 7, py + ph - 7], radius=rad - 5,
                        outline=(150, 110, 35), width=1)
    # selo "feito à mão"
    fnt = load_font("InstrumentSans-Bold.ttf", 30)
    txt = "feito à mão"
    bb = d.textbbox((0, 0), txt, font=fnt)
    sw = bb[2] - bb[0] + 44; shh = bb[3] - bb[1] + 20
    sx = px + 22; sy = py + ph - shh - 22
    d.rounded_rectangle([sx, sy, sx + sw, sy + shh], radius=shh // 2, fill=OURO, outline=OURO_P, width=2)
    d.text((sx + 22 - bb[0], sy + 10 - bb[1]), txt, font=fnt, fill=BRANCO)
    return img


def build():
    img = bg_grad(LAVANDA, CREME)
    cx = W // 2

    pw, ph, py = 624, 430, 96
    px = (W - pw) // 2
    img = hero_photo(img, FOTO, pw, ph, px, py)
    d = ImageDraw.Draw(img)
    cantos(d)

    # medir bloco de texto
    px0, px1 = 78, W - 78
    pad = 46
    maxw = (px1 - px0) - 2 * 42
    kf = load_font("CormorantGaramond-SemiBoldItalic.ttf", 44)
    kl = wrap_lines(d, "mês frio, casa cheia,", kf, maxw)
    hf = fit_headline(d, "junho é de juntar.", maxw, start=96, floor=64)
    hl = wrap_lines(d, "junho é de juntar.", hf, maxw)
    sf = load_font("Lora-Italic.ttf", 35)
    sl = wrap_lines(d, "a gente faz o salgado. o resto, vocês juntam.", sf, maxw)

    kh = block_h(d, kl, kf, 6)
    hh = block_h(d, hl, hf, 10)
    shh = block_h(d, sl, sf, 10)
    g1, g2 = 16, 70
    block = kh + g1 + hh + g2 + shh

    ctop = py + ph + 30
    panel_h = block + pad * 2
    rect = [px0, ctop, px1, ctop + panel_h]

    # sombra + cartao
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([rect[0], rect[1] + 12, rect[2], rect[3] + 12],
                                         radius=28, fill=(60, 40, 18, 70))
    img = Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(20))).convert("RGB")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(rect, radius=28, fill=PANEL_FILL)
    d.rounded_rectangle(rect, radius=28, outline=OURO, width=2)
    d.rounded_rectangle([rect[0] + 8, rect[1] + 8, rect[2] - 8, rect[3] - 8], radius=22,
                        outline=OURO_P, width=1)

    y = ctop + pad
    draw_lines(d, kl, kf, cx, y, OURO, 6); y += kh + g1
    draw_lines(d, hl, hf, cx, y, TXT, 10); y += hh
    regua(d, cx, y + g2 // 2, OURO); y += g2
    draw_lines(d, sl, sf, cx, y, TXT_M, 10)

    # assinatura
    fnt = load_font("Italiana-Regular.ttf", 44)
    s = "Ok Delícias com Amor"
    bb = d.textbbox((0, 0), s, font=fnt)
    d.text((cx - (bb[2] - bb[0]) // 2 - bb[0], rect[3] + 28 - bb[1]), s, font=fnt, fill=TXT_M)
    fnt2 = load_font("InstrumentSans-Bold.ttf", 26)
    h2 = "@ok_deliciascomamor"
    b2 = d.textbbox((0, 0), h2, font=fnt2)
    d.text((cx - (b2[2] - b2[0]) // 2, rect[3] + 84), h2, font=fnt2, fill=OURO)

    border(d, OURO_S)

    out = os.path.join(BASE, "02 - Criativos", "junho03", "post_junho03.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, "PNG", quality=97)
    print("Salvo:", out)


if __name__ == "__main__":
    build()
