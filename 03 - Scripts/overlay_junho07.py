# -*- coding: utf-8 -*-
"""
Gera overlay PNG transparente (1080x1920) com o mesmo design polaroid v2
pra ser sobreposto em video de story. Sem foto base, fundo totalmente
transparente exceto pelo painel cremoso translucido + texto + rodape.

Uso: gera overlay_t1.png que vai por cima do video da encomenda saindo.
"""
import os
from PIL import Image, ImageDraw, ImageFilter
from stories_maio30 import load_font, W, H, OURO, OURO_P, TXT, TXT_M
from stories_junho02 import (
    wrap_lines, block_h, draw_lines, fit_headline, PANEL_FILL,
)
from stories_junho05_v2 import (
    darken_gradient, panel_box, diamond, progress_minimal, rodape_branco,
    PANEL_PAD,
)

BASE = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
        r"\Ok - Delicias com Amor")


def overlay(cfg, total=3, out_name=None):
    # Comeca com PNG totalmente transparente
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # Top dim: escurecimento sutil no topo (igual nas telas estaticas)
    top_dim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(top_dim)
    for y in range(0, 240):
        a = int(70 * (1 - y / 240))
        td.line([(0, y), (W, y)], fill=(10, 6, 2, a))
    base = Image.alpha_composite(base, top_dim)

    # Gradiente escurecedor na base, igual nas telas estaticas
    base = darken_gradient(base, start_y=0.45, max_alpha=210)

    # Calcular dimensoes do painel
    md = ImageDraw.Draw(base)
    acc_font = load_font("CormorantGaramond-SemiBoldItalic.ttf", 56)
    t_font = fit_headline(md, cfg["titulo"], start=92, floor=58, step=4)
    body_font = load_font("Lora-Italic.ttf", 40)

    txt_maxw = W - PANEL_PAD * 2 - 100
    acc_lines = wrap_lines(md, cfg["acento"], acc_font, max_w=txt_maxw)
    t_lines = wrap_lines(md, cfg["titulo"], t_font, max_w=txt_maxw)
    b_lines = wrap_lines(md, cfg["corpo"], body_font, max_w=txt_maxw)

    acc_h = block_h(md, acc_lines, acc_font, 6)
    t_h = block_h(md, t_lines, t_font, 12)
    b_h = block_h(md, b_lines, body_font, 12)
    g1, g2 = 16, 64
    block = acc_h + g1 + t_h + g2 + b_h

    pad_v = 56
    panel_h = block + pad_v * 2
    bottom_y = H - 200
    panel_bot = bottom_y - 40
    panel_top = panel_bot - panel_h

    rect = [PANEL_PAD, panel_top, W - PANEL_PAD, panel_bot]
    base = panel_box(base, rect, radius=28, fill=PANEL_FILL)
    d = ImageDraw.Draw(base)

    y = panel_top + pad_v
    d.line([(W // 2 - 60, y - 26), (W // 2 + 60, y - 26)], fill=cfg["acc"], width=2)
    diamond(d, W // 2, y - 26, 5, cfg["acc"])

    draw_lines(d, acc_lines, acc_font, W // 2, y, cfg["acc"], 6)
    y += acc_h + g1
    draw_lines(d, t_lines, t_font, W // 2, y, TXT, 12)
    y += t_h
    d.line([(W // 2 - 110, y + g2 // 2), (W // 2 - 24, y + g2 // 2)], fill=cfg["acc"], width=2)
    d.line([(W // 2 + 24, y + g2 // 2), (W // 2 + 110, y + g2 // 2)], fill=cfg["acc"], width=2)
    diamond(d, W // 2, y + g2 // 2, 6, cfg["acc"])
    y += g2
    draw_lines(d, b_lines, body_font, W // 2, y, cfg.get("corpo_col", TXT_M), 12)

    progress_minimal(d, cfg["n"], total, OURO_P, panel_bot + 50)
    rodape_branco(d, H - 92)

    out = os.path.join(BASE, "02 - Criativos", "junho07",
                       out_name or f"overlay_t{cfg['n']}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    base.save(out, "PNG")
    print("Overlay salvo:", out)
    return out


# T1 ABERTURA - mesmo copy do PNG estatico
CFG_T1 = dict(
    n=1,
    acc=OURO,
    acento="domingo de saída,",
    titulo="hoje é dia de festa pra alguém.",
    corpo="saindo agora uma encomenda inteira. cada peça feita à mão, pra uma mesa que reúne.",
    corpo_col=TXT_M,
)


if __name__ == "__main__":
    overlay(CFG_T1, total=3, out_name="overlay_t1.png")
    print("Pronto.")
