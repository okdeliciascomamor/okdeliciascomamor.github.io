# -*- coding: utf-8 -*-
"""
3 Stories "Encomenda Saindo" — Ok Delícias com Amor — 07/06/2026 (domingo)

Prova social pura. Encomenda real saindo da cozinha da Oli num domingo,
com canapés decorados peça a peça (coração de pimentão, fios de ovos,
salada russa com maionese caseira).

Arco (Marshall Ganz):
  T1 SELF/ABERTURA - "olha o tamanho da saída" (panorama da encomenda)
  T2 US/DETALHE    - "olha o cuidado" (coração de pimentão um por um)
  T3 NOW/CTA       - "garante a tua próxima" (fios de ovos premium + link)

Design: POLAROID FULL-BLEED v2 (mesmo do junho05_v2).
Voz: a Oli em "a gente". Sem em-dash. CTA pelo link, nao direct.
Nao promete entrega "pra hoje" (essa encomenda ja tem dono, e a proxima).
"""
import os
from stories_junho05_v2 import tela_polaroid
from stories_maio30 import OURO, TERRA, LILAS_E, TXT_M

BASE = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
        r"\Ok - Delicias com Amor")
M07 = os.path.join(BASE, "Material 07.06", "_work")


def tela_polaroid_dom(cfg):
    """Override pra mudar o destino de gravacao (junho07/ em vez de junho05_v2/)."""
    # monkey-patch leve: a funcao tela_polaroid salva em junho05_v2 hard-coded.
    # vamos chamar e mover/renomear pra ca seria feio. melhor copiar a logica
    # mas como ja temos a funcao, vamos so re-implementar o save final.
    pass


# Estrategia mais limpa: usa a tela_polaroid e renomeia/move o arquivo gerado
# para junho07/. Mas o tela_polaroid hard-codea o caminho. Solucao mais limpa:
# criar uma versao local que aceita pasta de saida.

from stories_junho05_v2 import (
    Image, ImageDraw, ImageFilter, load_font, crop_cover, W, H,
    CREME, OURO_P, TXT,
    darken_gradient, panel_box, diamond, progress_minimal, rodape_branco,
    wrap_lines, block_h, draw_lines, fit_headline, PANEL_FILL, PANEL_PAD,
)


def tela(cfg, total=3):
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    photo = crop_cover(cfg["photo"], W, H, focus_x=cfg.get("fx", 0.5),
                       focus_y=cfg.get("fy", 0.5))
    base.paste(photo, (0, 0))

    top_dim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(top_dim)
    for y in range(0, 240):
        a = int(70 * (1 - y / 240))
        td.line([(0, y), (W, y)], fill=(10, 6, 2, a))
    base = Image.alpha_composite(base, top_dim)

    base = darken_gradient(base, start_y=0.45, max_alpha=210)

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

    out = os.path.join(BASE, "02 - Criativos", "junho07", f"story_junho07_{cfg['n']}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    base.convert("RGB").save(out, "PNG", quality=95)
    print("Salvo:", out)


CFGS = [
    # T1 ABERTURA - panorama da encomenda (frame_44s, vertical 2160x3840, mesma proporcao 9:16)
    dict(n=1,
         photo=os.path.join(M07, "frame_44s.jpg"),
         fy=0.5, fx=0.5,
         acc=OURO,
         acento="domingo de saída,",
         titulo="hoje é dia de festa pra alguém.",
         corpo="saindo agora uma encomenda inteira. cada peça feita à mão, pra uma mesa que reúne.",
         corpo_col=TXT_M),

    # T2 DETALHE - coracao de pimentao (canoinha com salada russa, decoracao manual)
    dict(n=2,
         photo=os.path.join(M07, "t2_coracao.jpg"),
         fy=0.5, fx=0.5,
         acc=(178, 50, 70),   # vermelho-coracao terroso, alinhado com o pimentao
         acento="olha o cuidado,",
         titulo="cada coração é feito à mão.",
         corpo="vão um a um, em cima da maionese caseira. não tem máquina que faz isso.",
         corpo_col=(120, 50, 60)),

    # T3 CTA - fios de ovos premium + link
    dict(n=3,
         photo=os.path.join(M07, "t3_fios.jpg"),
         fy=0.5, fx=0.5,
         acc=OURO,
         acento="pra tua próxima reunião,",
         titulo="a agenda enche cedo.",
         corpo="essas peças já tem dono. a próxima pode ser pra ti. cardápio inteiro no link aqui do story.",
         corpo_col=(110, 78, 38)),
]


if __name__ == "__main__":
    for cfg in CFGS:
        tela(cfg)
    print("3 Stories Encomenda Saindo 07/06 prontos.")
