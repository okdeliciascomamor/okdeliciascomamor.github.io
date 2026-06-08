# -*- coding: utf-8 -*-
"""
5 Stories Bastidor de Risoles — Ok Delícias com Amor — 05/06/2026
DESIGN v2: POLAROID FULL-BLEED.

Quebra com o "cartão de leitura" das semanas anteriores. Foto ocupa a
tela inteira, painel translúcido cremoso na base com o texto. Vibe
cinematográfica, mais editorial, foto manda.

Mesmo arco (Marshall Ganz Self -> Us -> Now) e mesma copy aprovada.
"""
import os
from PIL import Image, ImageDraw, ImageFilter
from stories_maio30 import (
    load_font, crop_cover, W, H,
    CREME, OURO, OURO_P, TERRA, LILAS_E, TXT, TXT_M,
)
from stories_junho02 import wrap_lines, block_h, draw_lines, fit_headline

BASE = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
        r"\Ok - Delicias com Amor")
M05 = os.path.join(BASE, "Material 05.06", "_work")
DRIVE = os.path.join(BASE, "fotos", "drive_zip")

PANEL_FILL = (255, 248, 234, 235)   # creme translucido alto
PANEL_PAD = 64


def darken_gradient(base, start_y=0.45, max_alpha=200):
    """Aplica gradiente preto suave da metade pra baixo, pra legibilidade do painel."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    y0 = int(H * start_y)
    for y in range(y0, H):
        a = int(max_alpha * ((y - y0) / (H - y0)) ** 1.3)
        od.line([(0, y), (W, y)], fill=(18, 12, 4, a))
    return Image.alpha_composite(base, overlay)


def round_mask(size, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0], size[1]], radius=radius, fill=255)
    return m


def panel_box(base, rect, radius=28, fill=PANEL_FILL):
    """Painel translucido cremoso com sombra suave."""
    # sombra
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([rect[0], rect[1] + 16, rect[2], rect[3] + 16],
                          radius=radius, fill=(10, 6, 2, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    base = Image.alpha_composite(base, shadow)
    # painel
    pn = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pn)
    pd.rounded_rectangle(rect, radius=radius, fill=fill)
    # fio dourado fino
    pd.rounded_rectangle(rect, radius=radius, outline=(195, 152, 58, 180), width=2)
    return Image.alpha_composite(base, pn)


def diamond(d, cx, cy, size, color):
    d.polygon([(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)], fill=color)


def progress_minimal(d, idx, total, acc, y):
    """Indicador de progresso discreto: bolinhas alinhadas."""
    cx = W // 2
    r = 5
    gap = 22
    total_w = total * (2 * r) + (total - 1) * gap
    x = cx - total_w // 2
    for i in range(1, total + 1):
        if i == idx:
            d.ellipse([x, y - r, x + 2 * r, y + r], fill=acc)
        else:
            d.ellipse([x, y - r, x + 2 * r, y + r], outline=(255, 248, 234, 200), width=2)
        x += 2 * r + gap


def rodape_branco(d, y):
    f = load_font("Italiana-Regular.ttf", 38)
    s = "Ok Delícias com Amor"
    bb = d.textbbox((0, 0), s, font=f)
    d.text((W // 2 - (bb[2] - bb[0]) // 2 - bb[0], y - bb[1]),
           s, font=f, fill=(255, 248, 234, 220))


def tela_polaroid(cfg):
    # 1. Foto full-bleed
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    photo = crop_cover(cfg["photo"], W, H, focus_x=cfg.get("fx", 0.5),
                       focus_y=cfg.get("fy", 0.5))
    base.paste(photo, (0, 0))

    # 2. Pequeno escurecimento geral (top) pra integrar texto branco do acento se necessario
    top_dim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(top_dim)
    for y in range(0, 240):
        a = int(70 * (1 - y / 240))
        td.line([(0, y), (W, y)], fill=(10, 6, 2, a))
    base = Image.alpha_composite(base, top_dim)

    # 3. Gradiente escurecedor inferior pra base do painel sobressair
    base = darken_gradient(base, start_y=0.45, max_alpha=210)

    # 4. Medir bloco de texto pra dimensionar painel
    md = ImageDraw.Draw(base)
    acc_font = load_font("CormorantGaramond-SemiBoldItalic.ttf", 56)
    t_font = fit_headline(md, cfg["titulo"], start=92, floor=58, step=4)
    body_font = load_font("Lora-Italic.ttf", 40)

    txt_maxw = W - PANEL_PAD * 2 - 100   # margem interna do painel
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
    # painel ancora no rodape
    bottom_y = H - 200
    panel_bot = bottom_y - 40
    panel_top = panel_bot - panel_h

    rect = [PANEL_PAD, panel_top, W - PANEL_PAD, panel_bot]
    base = panel_box(base, rect, radius=28, fill=PANEL_FILL)
    d = ImageDraw.Draw(base)

    # 5. Texto no painel
    y = panel_top + pad_v
    # regua dourada pequena acima do acento
    d.line([(W // 2 - 60, y - 26), (W // 2 + 60, y - 26)], fill=cfg["acc"], width=2)
    diamond(d, W // 2, y - 26, 5, cfg["acc"])

    draw_lines(d, acc_lines, acc_font, W // 2, y, cfg["acc"], 6)
    y += acc_h + g1
    draw_lines(d, t_lines, t_font, W // 2, y, TXT, 12)
    y += t_h
    # regua sob titulo
    d.line([(W // 2 - 110, y + g2 // 2), (W // 2 - 24, y + g2 // 2)], fill=cfg["acc"], width=2)
    d.line([(W // 2 + 24, y + g2 // 2), (W // 2 + 110, y + g2 // 2)], fill=cfg["acc"], width=2)
    diamond(d, W // 2, y + g2 // 2, 6, cfg["acc"])
    y += g2
    draw_lines(d, b_lines, body_font, W // 2, y, cfg.get("corpo_col", TXT_M), 12)

    # 6. Progress indicator + rodape em branco sobre a foto, fora do painel
    progress_minimal(d, cfg["n"], 5, OURO_P, panel_bot + 50)
    rodape_branco(d, H - 92)

    out = os.path.join(BASE, "02 - Criativos", "junho05_v2", f"story_junho05_v2_{cfg['n']}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    base.convert("RGB").save(out, "PNG", quality=95)
    print("Salvo:", out)


CFGS = [
    # T1 ABERTURA - massa aberta no balcao
    dict(n=1,
         photo=os.path.join(M05, "IMG_8520_close.jpg"),
         fy=0.5, fx=0.5,
         acc=OURO,
         acento="vem ver,",
         titulo="como nasce um risole.",
         corpo="hoje a gente abre a cozinha pra ti. é dia de risole, e tu vai ver de onde vem.",
         corpo_col=TXT_M),

    # T2 HERANCA - massa cortada em discos
    dict(n=2,
         photo=os.path.join(M05, "IMG_8523_close.jpg"),
         fy=0.5, fx=0.5,
         acc=LILAS_E,
         acento="vindo de longe,",
         titulo="essa massa tem nome.",
         corpo="é a mesma da Dona Wilma, mãe da Oli. 40 anos de cozinha, passados de mão em mão.",
         corpo_col=(92, 70, 120)),

    # T3 GESTO - risoles crus em meia-lua
    dict(n=3,
         photo=os.path.join(M05, "IMG_8524_close.jpg"),
         fy=0.5, fx=0.5,
         acc=TERRA,
         acento="olha o gesto,",
         titulo="risole é mão.",
         corpo="não tem máquina que fecha igual. é a mão da Oli, antes da empanada e do dourado.",
         corpo_col=(120, 75, 45)),

    # T4 TEASER - risoles dourados em blur (mistério)
    dict(n=4,
         photo=os.path.join(DRIVE, "3_close_blur.png"),
         fy=0.5, fx=0.5,
         acc=OURO,
         acento="spoiler,",
         titulo="tem reel chegando.",
         corpo="a massa, o recheio, o fechar, o fritar. tudo em meia-lua dourada. logo logo no feed.",
         corpo_col=TXT_M),

    # T5 CTA - risoles dourados nitidos
    dict(n=5,
         photo=os.path.join(DRIVE, "3_close.png"),
         fy=0.5, fx=0.5,
         acc=OURO,
         acento="pra tua próxima mesa,",
         titulo="espia o cardápio.",
         corpo="tá no link aqui do story. R$ 170 o cento, quatro sabores. junho enche rápido, garante a tua data.",
         corpo_col=(110, 78, 38)),
]


if __name__ == "__main__":
    for cfg in CFGS:
        tela_polaroid(cfg)
    print("5 Stories v2 (polaroid full-bleed) 05/06 prontos.")
