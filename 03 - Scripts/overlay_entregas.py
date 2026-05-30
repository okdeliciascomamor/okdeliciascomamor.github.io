# -*- coding: utf-8 -*-
"""
Overlays de marca (PNG 1080x1920 transparente) para os VIDEO STORIES das
entregas de 30/05. Full-bleed: o video preenche a tela, o overlay traz flores
de canto, moldura dourada, scrim creme inferior (legibilidade), kicker em
Cormorant Garamond italic, headline em Lora Bold e assinatura da marca.

Gera entrega_ov_1.png ... entrega_ov_4.png em Material 30.05/Entregas/_work/.
Sem travessao. Sem a palavra "caixa".
"""

import os
from PIL import Image, ImageDraw
from stories_maio30 import (
    load_font, topo_flores, border, diamond, wrap_centered,
    W, H, OURO, OURO_S, OURO_P, TXT, TXT_M, CREME, BRANCO,
)

OUT_DIR = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
           r"\Ok - Delicias com Amor\Material 30.05\Entregas\_work")


def cream_scrim(draw, y0=1030, full_at=1300, max_a=240):
    """Gradiente creme transparente->opaco no terco inferior, p/ leitura."""
    for y in range(y0, H):
        t = (y - y0) / max(1, (full_at - y0))
        a = int(max_a * min(1.0, t))
        draw.line([(0, y), (W, y)], fill=(255, 248, 234, a))


def make_overlay(kicker, headline, support, out, cta_pill=False):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = W // 2

    cream_scrim(d)
    topo_flores(d)
    border(d, OURO_S)

    cy = 1255
    cy = wrap_centered(d, kicker,
                       load_font("CormorantGaramond-SemiBoldItalic.ttf", 62),
                       W - 150, cx, cy, fill=(150, 110, 40), line_spacing=4) + 12
    cy = wrap_centered(d, headline,
                       load_font("Lora-Bold.ttf", 86),
                       W - 110, cx, cy, fill=TXT, shadow=True,
                       shd_col=(232, 214, 178), line_spacing=6) + 34
    d.line([(cx - 190, cy), (cx + 190, cy)], fill=OURO, width=2)
    cy += 34

    if cta_pill:
        fnt = load_font("InstrumentSans-Bold.ttf", 38)
        bb = d.textbbox((0, 0), support, font=fnt)
        pw, ph, r = 760, 100, 22
        pxx = cx - pw // 2
        d.rounded_rectangle([pxx, cy, pxx + pw, cy + ph], radius=r,
                            fill=OURO, outline=OURO_P, width=2)
        d.text((cx - (bb[2] - bb[0]) // 2, cy + (ph - (bb[3] - bb[1])) // 2 - 2),
               support, font=fnt, fill=BRANCO)
    else:
        wrap_centered(d, support, load_font("Lora-Italic.ttf", 42),
                      W - 150, cx, cy, fill=TXT_M, line_spacing=10)

    # assinatura
    fnt_br = load_font("InstrumentSans-Bold.ttf", 36)
    bbb = d.textbbox((0, 0), "Ok Delícias com Amor", font=fnt_br)
    d.text((cx - (bbb[2] - bbb[0]) // 2, H - 96), "Ok Delícias com Amor",
           font=fnt_br, fill=TXT_M)

    os.makedirs(OUT_DIR, exist_ok=True)
    p = os.path.join(OUT_DIR, out)
    img.save(p, "PNG")
    print("Salvo:", p)


if __name__ == "__main__":
    make_overlay("a canoinha de legumes,", "tá saindo.",
                 "fresquinha, no ponto certo pra ti provar.", "entrega_ov_1.png")
    make_overlay("e tem mais,", "bandeja atrás de bandeja.",
                 "cada uma montada à mão.", "entrega_ov_2.png")
    make_overlay("tem canudo também,", "recheado na hora.",
                 "crocante por fora, cremoso por dentro.", "entrega_ov_3.png")
    make_overlay("tudo isso saiu hoje.", "a próxima é tua?",
                 "chama no direct e garante a tua", "entrega_ov_4.png",
                 cta_pill=True)
    print("Overlays prontos.")
