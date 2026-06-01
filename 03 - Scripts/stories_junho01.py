# -*- coding: utf-8 -*-
"""
3 Stories Segunda de Produção — Ok Delícias com Amor — 01/06/2026

Pilar Bastidores. Tema do mês: "Junho é de juntar".
Story 1: massa sendo moldada (creme/bege) - "dia de produção"
Story 2: dourado saindo do forno (pêssego/âmbar) - "saiu do forno"
Story 3: card de convite (lavanda) - "garante a tua" + CTA

Reusa os helpers de stories_maio30. Sem travessao. Sem a palavra "caixa".
Cada foto usada uma unica vez. Acento de abertura em Cormorant Garamond.
"""
import os
from PIL import ImageDraw
from stories_maio30 import (
    load_font, bg_grad, border, framed_photo, photo_badge, topo_flores,
    base_flores, wrap_centered, diamond, arrow_right, progress_indicator,
    marca_rodape, W, H, CREME, BEGE, BEGE_E, PESSEGO, AMBAR, OURO, OURO_S,
    OURO_P, TERRA, LAVANDA, LAVANDA_E, LILAS_E, TXT, TXT_M, BRANCO,
)

MAT = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
       r"\Ok - Delicias com Amor\Material 01.06")
RAW  = os.path.join(MAT, "photo_2026-06-01_16-52-55 (2).jpg")  # massa crua
BUNS = os.path.join(MAT, "photo_2026-06-01_16-52-55.jpg")       # dourado forno


def salvar(img, nome):
    out = os.path.join(os.path.dirname(MAT), "02 - Criativos", "junho01", nome)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, "PNG", quality=98)
    print("Salvo:", out)


def hint(draw, cx, txt, col):
    fnt = load_font("Lora-Italic.ttf", 38)
    bb = draw.textbbox((0, 0), txt, font=fnt)
    hnw, hnh = bb[2] - bb[0], bb[3] - bb[1]
    hy = H - 360
    htx = cx - (hnw + 56) // 2
    draw.text((htx, hy), txt, font=fnt, fill=col)
    arrow_right(draw, htx + hnw + 16, hy + hnh // 2 + 2, 42, col, 2, 12)


def foto_story(bg_top, bg_bot, acc, photo, badge, kicker, kicker_col, headline,
               support, support_col, hint_txt, hint_col, idx, border_col,
               flores_a=None, flores_b=None, frame_col=OURO_S, frame_in=(150, 110, 35),
               shadow_a=(90, 60, 25, 90), focus_y=0.5, badge_bg=None, badge_ol=None):
    img = bg_grad(bg_top, bg_bot)
    img = framed_photo(img, photo, 860, 760, 110, 250, focus_y=focus_y,
                       frame_col=frame_col, frame_in=frame_in, shadow_a=shadow_a)
    d = ImageDraw.Draw(img)
    topo_flores(d, col_a=flores_a, col_b=flores_b)
    if badge:
        photo_badge(d, badge, 110, 250, 760, badge_bg or OURO, badge_ol or OURO_P)
    cx = W // 2
    cy = 250 + 760 + 54
    cy = wrap_centered(d, kicker,
                       load_font("CormorantGaramond-SemiBoldItalic.ttf", 72),
                       W - 130, cx, cy, fill=kicker_col, line_spacing=6) + 16
    cy = wrap_centered(d, headline, load_font("Lora-Bold.ttf", 104),
                       W - 100, cx, cy, fill=TXT, shadow=True,
                       shd_col=(232, 214, 178), line_spacing=8) + 40
    d.line([(cx - 200, cy), (cx + 200, cy)], fill=acc, width=2)
    cy += 34
    wrap_centered(d, support, load_font("Lora-Italic.ttf", 42), W - 150, cx, cy,
                  fill=support_col, line_spacing=12)
    hint(d, cx, hint_txt, hint_col)
    progress_indicator(d, idx, 3, acc)
    base_flores(d, col_out=flores_b)
    marca_rodape(d)
    border(d, col=border_col)
    return img


def story_1():
    img = foto_story(
        CREME, BEGE, TERRA, RAW, "segunda",
        "segunda na Ok,", OURO, "dia de produção.",
        "a semana começa com a mão na massa.", (120, 84, 50),
        "vem ver", (150, 110, 55), 1, BEGE_E,
        flores_a=(222, 188, 130), flores_b=(210, 178, 120),
        badge_bg=TERRA, badge_ol=OURO_S, focus_y=0.5)
    salvar(img, "story_junho01_1.png")


def story_2():
    img = foto_story(
        PESSEGO, AMBAR, OURO, BUNS, "do forno",
        "e olha o resultado,", OURO, "saiu do forno.",
        "douradinho, fresquinho, feito com calma.", TXT_M,
        "tem mais", (150, 110, 55), 2, OURO_S,
        badge_bg=OURO, badge_ol=OURO_P, focus_y=0.45)
    salvar(img, "story_junho01_2.png")


def story_3():
    # Card de convite (sem foto)
    img = bg_grad(CREME, LAVANDA)
    d = ImageDraw.Draw(img)
    topo_flores(d, col_a=(200, 180, 220), col_b=(190, 168, 215))
    cx = W // 2
    cy = 470

    cy = wrap_centered(d, "a cozinha não para,",
                       load_font("CormorantGaramond-SemiBoldItalic.ttf", 74),
                       W - 130, cx, cy, fill=LILAS_E, line_spacing=6) + 18
    # ornamento
    d.line([(cx - 100, cy), (cx - 16, cy)], fill=LILAS_E, width=2)
    d.line([(cx + 16, cy), (cx + 100, cy)], fill=LILAS_E, width=2)
    diamond(d, cx, cy, 6, LILAS_E)
    cy += 56

    cy = wrap_centered(d, "garante a tua.", load_font("Lora-Bold.ttf", 100),
                       W - 100, cx, cy, fill=TXT, shadow=True,
                       shd_col=(205, 192, 226), line_spacing=8) + 44

    cy = wrap_centered(d, "junho enche rápido, e cada pedido é feito na hora.",
                       load_font("Lora-Italic.ttf", 44), W - 150, cx, cy,
                       fill=(92, 70, 120), line_spacing=12) + 50

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
    cy += ph + 16

    lbl = "@ok_deliciascomamor"
    fl = load_font("InstrumentSans-Bold.ttf", 34)
    bl = d.textbbox((0, 0), lbl, font=fl)
    d.text((cx - (bl[2] - bl[0]) // 2, cy + 6), lbl, font=fl, fill=(120, 95, 160))

    progress_indicator(d, 3, 3, LILAS_E)
    base_flores(d, col_out=(190, 168, 215))
    marca_rodape(d)
    border(d, col=LAVANDA_E)
    salvar(img, "story_junho01_3.png")


if __name__ == "__main__":
    story_1()
    story_2()
    story_3()
    print("3 Stories 01/06 prontos.")
