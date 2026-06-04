# -*- coding: utf-8 -*-
"""
Capa do Facebook — Ok Delícias com Amor — 1640x624 (2x de 820x312).
Logo centralizada (zona segura desktop + mobile) sobre fundo quente da marca,
com halo suave pra logo encaixar sem retangulo branco, e flores delicadas
nas laterais. Sem travessao. Sem a palavra "caixa".
"""
import os
from PIL import Image, ImageDraw, ImageFilter
from stories_maio30 import (
    load_font, draw_flower, draw_leaf, diamond,
    CREME, LAVANDA, PESSEGO, OURO, OURO_S, OURO_P, TXT_M, VERDE_S,
)

W, H = 1640, 624
BASE = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
        r"\Ok - Delicias com Amor")
LOGO = os.path.join(BASE, "Logo.jpeg")
ROSA = (240, 208, 220)
LILAS = (208, 182, 228)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def bg_grad():
    img = Image.new("RGB", (W, H), CREME)
    d = ImageDraw.Draw(img)
    half = W / 2
    for x in range(W):
        if x < half:
            c = lerp(LAVANDA, CREME, x / half)
        else:
            c = lerp(CREME, PESSEGO, (x - half) / half)
        d.line([(x, 0), (x, H)], fill=c)
    return img


def halo(img, cx, cy, rw, rh):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse([cx - rw, cy - rh, cx + rw, cy + rh],
                                  fill=(255, 252, 246, 235))
    layer = layer.filter(ImageFilter.GaussianBlur(85))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def spray(d, cx, cy, col_a, col_b):
    # pequena guirlanda vertical de flores e folhas
    draw_flower(d, cx, cy - 70, petals=6, plen=26, pw=12, col_out=col_a, col_mid=OURO_P, cr=8)
    draw_leaf(d, cx - 18, cy - 50, 215, 22, 8); draw_leaf(d, cx + 18, cy - 50, 325, 22, 8)
    draw_flower(d, cx - 30, cy + 6, petals=6, plen=20, pw=9, col_out=col_b, col_mid=OURO_P, cr=6)
    draw_flower(d, cx + 34, cy + 30, petals=6, plen=18, pw=8, col_out=col_a, col_mid=OURO_P, cr=6)
    draw_leaf(d, cx, cy + 70, 270, 20, 7)
    draw_flower(d, cx + 4, cy + 96, petals=6, plen=16, pw=7, col_out=col_b, col_mid=OURO_P, cr=5)


def cantos(d):
    for (fx, fy) in [(54, 54), (W - 54, 54), (54, H - 54), (W - 54, H - 54)]:
        draw_flower(d, fx, fy, petals=6, plen=18, pw=8, col_out=(218, 192, 226), col_mid=OURO_P, cr=6)


def keyed_logo(path, target_h):
    logo = Image.open(path).convert("RGBA")
    px = list(logo.getdata())
    out = [(255, 255, 255, 0) if (p[0] > 247 and p[1] > 247 and p[2] > 247) else p for p in px]
    logo.putdata(out)
    w, h = logo.size
    nw = int(w * target_h / h)
    return logo.resize((nw, target_h), Image.LANCZOS)


def build():
    img = bg_grad()
    cx, cy = W // 2, H // 2 - 8

    img = halo(img, cx, cy, 430, 330)
    d = ImageDraw.Draw(img)

    cantos(d)
    spray(d, 250, cy, ROSA, LILAS)
    spray(d, W - 250, cy, LILAS, ROSA)

    logo = keyed_logo(LOGO, 470)
    img.paste(logo, (cx - logo.width // 2, cy - logo.height // 2), logo)

    out = os.path.join(BASE, "02 - Criativos", "junho04", "capa_facebook.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, "PNG", quality=97)
    print("Salvo:", out, img.size)


if __name__ == "__main__":
    build()
