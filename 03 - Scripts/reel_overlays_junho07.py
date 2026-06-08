# -*- coding: utf-8 -*-
"""
Gera 7 overlays de texto (1080x1920 transparentes) pro Reel de Risoles 07/06.
Estilo de marca: scrim escuro suave na base, Lora Bold + Cormorant italico,
marca dagua Italiana no rodape. Texto legivel sobre video.

Sem em-dash. Voz da Oli. CTA pelo link.
"""
import os
from PIL import Image, ImageDraw
from stories_maio30 import load_font, W, H

OUT = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
       r"\Ok - Delicias com Amor\02 - Criativos\junho07_reel\overlays")
os.makedirs(OUT, exist_ok=True)

CREME = (255, 248, 234)
OURO_C = (220, 185, 110)
SHADOW = (8, 5, 1)


def bottom_scrim(base, top_y=1180, max_a=180):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for y in range(top_y, H):
        a = int(max_a * ((y - top_y) / (H - top_y)) ** 1.4)
        d.line([(0, y), (W, y)], fill=(18, 12, 4, a))
    return Image.alpha_composite(base, layer)


def top_scrim(base, bot_y=420, max_a=120):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for y in range(0, bot_y):
        a = int(max_a * (1 - y / bot_y) ** 1.4)
        d.line([(0, y), (W, y)], fill=(18, 12, 4, a))
    return Image.alpha_composite(base, layer)


def draw_centered(d, text, font, cy, fill, shadow=True, sh_off=4, sh_col=SHADOW):
    bb = d.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    x = W // 2 - tw // 2 - bb[0]
    y = cy - th // 2 - bb[1]
    if shadow:
        for ox, oy in [(sh_off, sh_off), (-sh_off, sh_off), (sh_off, -sh_off), (-sh_off, -sh_off)]:
            d.text((x + ox, y + oy), text, font=font, fill=sh_col)
    d.text((x, y), text, font=font, fill=fill)
    return th


def diamond(d, cx, cy, s, col):
    d.polygon([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)], fill=col)


def regua(d, cx, cy, col, half=90):
    d.line([(cx - half, cy), (cx - 22, cy)], fill=col, width=3)
    d.line([(cx + 22, cy), (cx + half, cy)], fill=col, width=3)
    diamond(d, cx, cy, 6, col)


def watermark(d):
    f = load_font("Italiana-Regular.ttf", 40)
    s = "Ok Delícias com Amor"
    bb = d.textbbox((0, 0), s, font=f)
    d.text((W // 2 - (bb[2] - bb[0]) // 2 - bb[0], 1838),
           s, font=f, fill=(255, 248, 234, 210))


def seg_normal(kicker, main, n, cta=None):
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base = bottom_scrim(base)
    d = ImageDraw.Draw(base)

    # bloco de texto ancorado embaixo
    main_font = load_font("Lora-Bold.ttf", 96)
    # auto-reduz se nao couber
    while d.textbbox((0, 0), main, font=main_font)[2] > W - 130 and main_font.size > 60:
        main_font = load_font("Lora-Bold.ttf", main_font.size - 4)
    kick_font = load_font("CormorantGaramond-SemiBoldItalic.ttf", 58)

    base_y = 1560
    _ = kick_font  # mantido por compat
    kick_font = load_font("CrimsonPro-Italic.ttf", 66)
    draw_centered(d, kicker, kick_font, base_y - 90, OURO_C)
    regua(d, W // 2, base_y - 42, OURO_C)
    draw_centered(d, main, main_font, base_y + 30, CREME)

    if cta:
        cta_font = load_font("InstrumentSans-Bold.ttf", 38)
        draw_centered(d, cta, cta_font, base_y + 130, OURO_C, sh_off=3)

    watermark(d)
    out = os.path.join(OUT, f"ov_{n}.png")
    base.save(out, "PNG")
    print("Salvo:", out)


def seg_hook(line1, line2, n):
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base = top_scrim(base, bot_y=1920, max_a=70)   # leve escurecimento geral pro hook
    base = bottom_scrim(base, top_y=1180, max_a=150)
    d = ImageDraw.Draw(base)

    f1 = load_font("CrimsonPro-Italic.ttf", 80)
    f2 = load_font("Lora-Bold.ttf", 118)
    while d.textbbox((0, 0), line2, font=f2)[2] > W - 120 and f2.size > 70:
        f2 = load_font("Lora-Bold.ttf", f2.size - 4)

    cy = H // 2 - 40
    draw_centered(d, line1, f1, cy - 110, OURO_C)
    draw_centered(d, line2, f2, cy + 10, CREME)
    regua(d, W // 2, cy + 110, OURO_C, half=120)

    watermark(d)
    out = os.path.join(OUT, f"ov_{n}.png")
    base.save(out, "PNG")
    print("Salvo:", out)


if __name__ == "__main__":
    # 1 HOOK (paga o teaser dos stories "como nasce um risole")
    seg_hook("vem ver,", "como nasce um risole.", 1)
    # 2 MASSA CRUA (a bola, antes de abrir)
    seg_normal("tudo começa,", "na massa.", 2)
    # 3 MASSA ABERTA (espichada fina)
    seg_normal("aberta na hora,", "bem fininha.", 3)
    # 4 RECHEIO
    seg_normal("por dentro,", "recheio de legumes.", 4)
    # 5 EMPANADOS
    seg_normal("um por um,", "empanado à mão.", 5)
    # 6 OLEO
    seg_normal("e então,", "vai pro óleo quente.", 6)
    # 7 FRITAR
    seg_normal("até ficar", "dourado e crocante.", 7)
    # 8 PRONTO + CTA
    seg_normal("feito à mão,", "do início ao fim.", 8, cta="cardápio no link da bio")
    print("8 overlays prontos.")
