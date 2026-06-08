# -*- coding: utf-8 -*-
"""
Elementos de marca p/ o REEL de domingo (pan monstro IMG_8442):
  reel_intro.png   - cartela de abertura (opaca)
  reel_overlay.png - overlay persistente sobre o pan (transparente)
  reel_outro.png   - cartela de CTA no final (opaca)
Gera em Material 31.05/_work/. Sem travessao. Sem a palavra "caixa".
"""
import os
from PIL import Image, ImageDraw
from stories_maio30 import (
    load_font, bg_grad, border, topo_flores, base_flores, wrap_centered,
    W, H, CREME, PESSEGO, AMBAR, OURO, OURO_S, OURO_P, TXT, TXT_M, BRANCO,
)

OUT = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
       r"\Ok - Delicias com Amor\Material 31.05\_work")


def pill(d, text, font, cx, y, bg, txt_col, pad_x=30, pad_y=14, outline=None):
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    w, h = tw + pad_x * 2, th + pad_y * 2
    x = cx - w // 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg,
                        outline=outline, width=2 if outline else 0)
    d.text((x + pad_x - bb[0], y + pad_y - bb[1]), text, font=font, fill=txt_col)
    return y + h


def intro_card():
    img = bg_grad(CREME, PESSEGO)
    d = ImageDraw.Draw(img)
    topo_flores(d)
    base_flores(d)
    cx = W // 2
    cy = 700
    cy = wrap_centered(d, "feito num domingo,",
                       load_font("CormorantGaramond-SemiBoldItalic.ttf", 76),
                       W - 160, cx, cy, fill=OURO, line_spacing=6) + 16
    cy = wrap_centered(d, "direto da cozinha da Oli.",
                       load_font("Lora-Bold.ttf", 92), W - 120, cx, cy,
                       fill=TXT, shadow=True, shd_col=(232, 214, 178),
                       line_spacing=10) + 40
    d.line([(cx - 180, cy), (cx + 180, cy)], fill=OURO, width=2)
    cy += 36
    wrap_centered(d, "vem ver tudo que saiu hoje.",
                  load_font("Lora-Italic.ttf", 44), W - 160, cx, cy,
                  fill=TXT_M, line_spacing=10)
    fnt_br = load_font("InstrumentSans-Bold.ttf", 36)
    bb = d.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    d.text((cx - (bb[2] - bb[0]) // 2, H - 150), "Ok Delícias com Amor",
           font=fnt_br, fill=TXT_M)
    border(d, OURO_S)
    img.convert("RGB").save(os.path.join(OUT, "reel_intro.png"), "PNG")


def outro_card():
    img = bg_grad(PESSEGO, CREME)
    d = ImageDraw.Draw(img)
    topo_flores(d)
    base_flores(d)
    cx = W // 2
    cy = 640
    cy = wrap_centered(d, "tua mesa,",
                       load_font("CormorantGaramond-SemiBoldItalic.ttf", 74),
                       W - 160, cx, cy, fill=OURO, line_spacing=6) + 14
    cy = wrap_centered(d, "também merece.",
                       load_font("Lora-Bold.ttf", 96), W - 120, cx, cy,
                       fill=TXT, shadow=True, shd_col=(225, 190, 140),
                       line_spacing=10) + 44
    # CTA pill
    cta = "chama no direct e encomende"
    fnt = load_font("InstrumentSans-Bold.ttf", 40)
    bb = d.textbbox((0, 0), cta, font=fnt)
    pw, ph, r = bb[2] - bb[0] + 80, 104, 24
    px = cx - pw // 2
    d.rounded_rectangle([px, cy, px + pw, cy + ph], radius=r, fill=OURO,
                        outline=OURO_P, width=2)
    d.text((cx - (bb[2] - bb[0]) // 2, cy + (ph - (bb[3] - bb[1])) // 2 - bb[1]),
           cta, font=fnt, fill=BRANCO)
    cy += ph + 34
    fnt_h = load_font("InstrumentSans-Bold.ttf", 40)
    bb2 = d.textbbox((0, 0), "@ok_deliciascomamor", font=fnt_h)
    d.text((cx - (bb2[2] - bb2[0]) // 2, cy), "@ok_deliciascomamor",
           font=fnt_h, fill=TXT_M)
    cy += 96
    wrap_centered(d, "feito à mão, com amor.",
                  load_font("Lora-Italic.ttf", 42), W - 160, cx, cy,
                  fill=(150, 110, 55), line_spacing=8)
    border(d, OURO_S)
    img.convert("RGB").save(os.path.join(OUT, "reel_outro.png"), "PNG")


def persistent_overlay():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    topo_flores(d)
    border(d, OURO_S)
    cx = W // 2
    # wordmark pill (topo)
    pill(d, "Ok Delícias com Amor", load_font("InstrumentSans-Bold.ttf", 34),
         cx, 150, (255, 248, 234, 235), TXT, outline=OURO_S)
    # handle pill (base)
    pill(d, "@ok_deliciascomamor", load_font("InstrumentSans-Bold.ttf", 34),
         cx, H - 230, (255, 248, 234, 235), OURO, outline=OURO_S)
    img.save(os.path.join(OUT, "reel_overlay.png"), "PNG")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    intro_card()
    outro_card()
    persistent_overlay()
    print("Elementos do reel prontos.")
