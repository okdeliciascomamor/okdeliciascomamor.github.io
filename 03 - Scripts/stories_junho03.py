# -*- coding: utf-8 -*-
"""
5 Stories MAROTOS — Ok Delícias com Amor — 03/06/2026
Pegada do post de hoje ("Junho e de juntar"), lado divertido.

Conceito (copy: John Carlton, squad de copy): "as desculpas que a gente inventa
pra chamar todo mundo pra mesa no frio", confissao escalonada, e o truque que
nunca falha (deixa a gente cozinhar). Design: sistema vencedor (cartao de texto
limpo + emblema com foto real de salgado + paleta distinta por tela).
Sem travessao. Sem a palavra "caixa". "tu/teu" consistente.
"""
import os
from PIL import Image, ImageDraw
from stories_maio30 import (
    load_font, bg_grad, progress_indicator, W, H, CREME, CREME_F, BEGE_E,
    PESSEGO, PESSEGO_Q, AMBAR, OURO, OURO_S, OURO_P, TERRA, LAVANDA, LAVANDA_E,
    LILAS_E, VERDE_BG1, VERDE_BG2, MUSGO, VERDE_BORD, TXT, TXT_M,
)
from stories_junho02 import (
    photo_emblem, cantos, regua, ornamento_fecho, rodape, border,
    wrap_lines, block_h, draw_lines, fit_headline, panel_shadow, PANEL_FILL,
)

BASE = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
        r"\Ok - Delicias com Amor")
M31 = os.path.join(BASE, "Material 31.05", "_work")
M30 = os.path.join(BASE, "Material 30.05")


def tela(cfg):
    base = bg_grad(cfg["bg"][0], cfg["bg"][1]).convert("RGBA")
    md = ImageDraw.Draw(base)
    cx = W // 2

    acc_font = load_font("CormorantGaramond-SemiBoldItalic.ttf", 58)
    acc_lines = wrap_lines(md, cfg["acento"], acc_font)
    t_font = fit_headline(md, cfg["titulo"])
    t_lines = wrap_lines(md, cfg["titulo"], t_font)
    body_font = load_font("Lora-Italic.ttf", 42)
    b_lines = wrap_lines(md, cfg["corpo"], body_font)

    acc_h = block_h(md, acc_lines, acc_font, 6)
    t_h = block_h(md, t_lines, t_font, 12)
    b_h = block_h(md, b_lines, body_font, 12)
    g1, g2 = 18, 78
    block = acc_h + g1 + t_h + g2 + b_h

    pad = 70
    panel_cy = 905
    panel_h = block + pad * 2
    p_top = panel_cy - panel_h // 2
    p_bot = panel_cy + panel_h // 2
    rect = [64, p_top, W - 64, p_bot]

    base = Image.alpha_composite(base, panel_shadow(rect))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(rect, radius=30, fill=PANEL_FILL)
    d.rounded_rectangle(rect, radius=30, outline=cfg["acc"], width=2)
    d.rounded_rectangle([rect[0] + 9, rect[1] + 9, rect[2] - 9, rect[3] - 9],
                        radius=24, outline=OURO_P, width=1)

    cantos(d, cfg["flw_a"], cfg["flw_b"])
    photo_emblem(base, d, cx, 300, cfg["photo"], cfg["acc"],
                 cfg.get("fx", 0.5), cfg.get("fy", 0.5))

    y = p_top + pad
    draw_lines(d, acc_lines, acc_font, cx, y, cfg["acc"], 6); y += acc_h + g1
    draw_lines(d, t_lines, t_font, cx, y, TXT, 12); y += t_h
    regua(d, cx, y + g2 // 2, cfg["acc"]); y += g2
    draw_lines(d, b_lines, body_font, cx, y, cfg["corpo_col"], 12)

    ornamento_fecho(d, cx, p_bot + 90, cfg["acc"])
    progress_indicator(d, cfg["n"], 5, cfg["acc"])
    rodape(d)
    border(d, cfg["border"])

    out = os.path.join(BASE, "02 - Criativos", "junho03", f"story_junho03_{cfg['n']}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    base.convert("RGB").save(out, "PNG", quality=98)
    print("Salvo:", out)


CFGS = [
    dict(n=1, photo=os.path.join(BASE, "MIni Hamburgueres.jpeg"), fy=0.5,
         bg=(PESSEGO, AMBAR), acc=OURO, border=OURO_S,
         flw_a=(220, 185, 120), flw_b=(205, 168, 100),
         acento="junho chegou,",
         titulo="tá frio. junta todo mundo.",
         corpo="a gente separou uns truques pra encher a tua mesa. o último nunca falha.",
         corpo_col=(110, 78, 38)),
    dict(n=2, photo=os.path.join(M31, "IMG_8436.jpg"), fy=0.5,
         bg=(CREME, CREME_F), acc=TERRA, border=BEGE_E,
         flw_a=(222, 188, 130), flw_b=(210, 178, 120),
         acento="truque 1,",
         titulo="ninguém resiste a um cheirinho.",
         corpo="pastel fritando em casa, e a família aparece sozinha.",
         corpo_col=TXT_M),
    dict(n=3, photo=os.path.join(M30, "Canoinha de legumes 1.jpeg"), fy=0.5,
         bg=(CREME, LAVANDA), acc=LILAS_E, border=LAVANDA_E,
         flw_a=(200, 180, 220), flw_b=(190, 168, 215),
         acento="truque 2,",
         titulo="diz que é só um cafezinho.",
         corpo="aí tu bota a empadinha de legumes na mesa, e olha a conversa esticar.",
         corpo_col=(92, 70, 120)),
    dict(n=4, photo=os.path.join(M31, "IMG_8435.jpg"), fy=0.45,
         bg=(VERDE_BG1, VERDE_BG2), acc=MUSGO, border=VERDE_BORD,
         flw_a=(178, 202, 150), flw_b=(165, 190, 135),
         acento="o truque que nunca falha,",
         titulo="tu nem cozinha.",
         corpo="tu chama o pessoal, a gente entrega fresquinho, e tu leva a fama.",
         corpo_col=(70, 92, 54)),
    dict(n=5, photo=os.path.join(M31, "IMG_8439.jpg"), fy=0.5,
         bg=(PESSEGO, PESSEGO_Q), acc=TERRA, border=OURO_S,
         flw_a=(232, 180, 140), flw_b=(225, 168, 120),
         acento="junho é de juntar,",
         titulo="bora encher a tua mesa?",
         corpo="a agenda de junho enche rápido. chama no direct e marca a tua data.",
         corpo_col=(120, 75, 45)),
]


if __name__ == "__main__":
    for cfg in CFGS:
        tela(cfg)
    print("5 Stories marotos 03/06 prontos.")
