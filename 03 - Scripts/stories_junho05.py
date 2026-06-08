# -*- coding: utf-8 -*-
"""
5 Stories Bastidor de Risoles — Ok Delícias com Amor — 05/06/2026
Sustentação do Reel de bastidores do dia (pilar: Bastidores e Feito à Mão).

Squad sintetizado:
- Marshall Ganz Public Narrative (Self -> Us -> Now) como arco macro.
- Kindra Hall (Founder Story na T2, Value Story na T3) como conteúdo das telas.
- Park Howell ABT como estrutura interna de cada copy (sem cair em AAA).
Cliente é o herói. Marca é a guia. Voz da Oli em "a gente".

T1 ABERTURA  - convite pra dentro da cozinha (Self)
T2 HERANÇA   - Founder compactado: receita da Dona Wilma, mãe da Oli
T3 GESTO     - Value: "risole é mão", máquina não fecha igual
T4 GANCHO    - Us: tem reel novo no feed, vem ver
T5 CTA       - Now: cardápio no link, agenda enchendo

Design: sistema "cartão de leitura" aprovado (igual junho04).
Paletas escolhidas pra não cansar com junho04 e reforçar o dourado do risole.
Sem travessao. "mãe da Oli" pra Dona Wilma. CTA pelo link, nunca direct.
Não promete entrega pra hoje. Acentos completos.
"""
import os
from PIL import Image, ImageDraw
from stories_maio30 import (
    load_font, bg_grad, progress_indicator, draw_flower, diamond, W, H,
    CREME, CREME_F, PESSEGO, PESSEGO_Q, AMBAR, OURO, OURO_S, OURO_P, TERRA,
    LAVANDA, LAVANDA_E, LILAS_E,
    TXT, TXT_M,
)
from stories_junho02 import (
    photo_emblem, cantos, regua, ornamento_fecho, rodape, border,
    wrap_lines, block_h, draw_lines, fit_headline, panel_shadow, PANEL_FILL,
)

BASE = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
        r"\Ok - Delicias com Amor")
M30 = os.path.join(BASE, "Material 30.05")
M31 = os.path.join(BASE, "Material 31.05", "_work")
M05 = os.path.join(BASE, "Material 05.06", "_work")
FOTOS = os.path.join(BASE, "fotos")
DRIVE = os.path.join(BASE, "fotos", "drive_zip")


def ornament_emblem(d, cx, cy, ring_col):
    """Emblema floral dourado (sem foto). Usado quando o tema é abstrato
    (herança na T2) ou quando o foco vai pro sticker (gancho do reel na T4)."""
    r = 100
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ring_col, width=4)
    d.ellipse([cx - r - 9, cy - r - 9, cx + r + 9, cy + r + 9], outline=OURO_P, width=2)
    draw_flower(d, cx, cy, petals=8, plen=40, pw=15, col_out=ring_col, col_mid=OURO_P, cr=10)
    draw_flower(d, cx, cy, petals=8, plen=22, pw=9, col_out=OURO_P, col_mid=ring_col, cr=6)
    for a in (cx - r - 28, cx + r + 28):
        diamond(d, a, cy, 6, ring_col)


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
    if cfg.get("ornament"):
        ornament_emblem(d, cx, 300, cfg["acc"])
    else:
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

    out = os.path.join(BASE, "02 - Criativos", "junho05", f"story_junho05_{cfg['n']}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    base.convert("RGB").save(out, "PNG", quality=98)
    print("Salvo:", out)


CFGS = [
    # T1 ABERTURA - "vem ver, como nasce um risole." (Self)
    # Foto da Oli hoje: massa aberta no balcao (Material 05.06)
    dict(n=1,
         photo=os.path.join(M05, "IMG_8520_close.jpg"),
         fy=0.5,
         bg=(CREME, CREME_F), acc=OURO, border=OURO_S,
         flw_a=(222, 188, 130), flw_b=(210, 178, 120),
         acento="vem ver,",
         titulo="como nasce um risole.",
         corpo="hoje a gente abre a cozinha pra ti. é dia de risole, e tu vai ver de onde vem.",
         corpo_col=TXT_M),

    # T2 HERANÇA - "vindo de longe, essa massa tem nome." (Founder Story)
    dict(n=2, ornament=True,
         bg=(CREME, LAVANDA), acc=LILAS_E, border=LAVANDA_E,
         flw_a=(200, 180, 220), flw_b=(190, 168, 215),
         acento="vindo de longe,",
         titulo="essa massa tem nome.",
         corpo="é a mesma da Dona Wilma, mãe da Oli. 40 anos de cozinha, passados de mão em mão.",
         corpo_col=(92, 70, 120)),

    # T3 GESTO - "olha o gesto, risole é mão." (Value Story)
    # Foto da Oli hoje: risoles crus em meia-lua com farinha (antes da empanada)
    dict(n=3,
         photo=os.path.join(M05, "IMG_8524.jpg"),
         fy=0.5,
         bg=(PESSEGO, AMBAR), acc=TERRA, border=OURO_S,
         flw_a=(232, 180, 130), flw_b=(225, 168, 120),
         acento="olha o gesto,",
         titulo="risole é mão.",
         corpo="não tem máquina que fecha igual. é a mão da Oli, antes da empanada e do dourado.",
         corpo_col=(120, 75, 45)),

    # T4 TEASER - "spoiler, tem reel chegando." (Us, reel ainda nao publicado)
    dict(n=4, ornament=True,
         bg=(CREME, CREME_F), acc=OURO, border=OURO_S,
         flw_a=(222, 188, 130), flw_b=(210, 178, 120),
         acento="spoiler,",
         titulo="tem reel chegando.",
         corpo="a massa, o recheio, o fechar, o fritar. tudo em meia-lua dourada. logo logo no feed.",
         corpo_col=TXT_M),

    # T5 CTA - "pra tua próxima mesa, espia o cardápio." (Now)
    dict(n=5,
         photo=os.path.join(DRIVE, "3_close.png"),
         fy=0.5,
         bg=(PESSEGO, PESSEGO_Q), acc=OURO, border=OURO_S,
         flw_a=(220, 185, 120), flw_b=(205, 168, 100),
         acento="pra tua próxima mesa,",
         titulo="espia o cardápio.",
         corpo="tá no link aqui do story. R$ 170 o cento, quatro sabores. junho enche rápido, garante a tua data.",
         corpo_col=(110, 78, 38)),
]


if __name__ == "__main__":
    for cfg in CFGS:
        tela(cfg)
    print("5 Stories Bastidor de Risoles 05/06 prontos.")
