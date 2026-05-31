# -*- coding: utf-8 -*-
"""
Overlays de marca p/ os VIDEO STORIES de domingo (31/05) — angulo:
a Oli trabalha no domingo por amor, presente nas comemoracoes.
Reusa make_overlay de overlay_entregas, apontando p/ Material 31.05/_work.
"""
import overlay_entregas as oe

oe.OUT_DIR = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
              r"\Ok - Delicias com Amor\Material 31.05\_work")

if __name__ == "__main__":
    oe.make_overlay("acha que domingo a Oli para?", "que nada.",
                    "domingo é dia de festa, e a Oli faz questão de estar junto.",
                    "dom_ov_1.png")
    oe.make_overlay("pra ela,", "salgado é presença.",
                    "um jeito de estar na tua mesa, com carinho.",
                    "dom_ov_2.png")
    oe.make_overlay("e hoje,", "tem fartura.",
                    "tudo isso saiu da cozinha dela neste domingo.",
                    "dom_ov_3.png")
    oe.make_overlay("tua mesa de domingo,", "também merece.",
                    "chama no direct e garante a tua",
                    "dom_ov_4.png", cta_pill=True)
    print("Overlays domingo prontos.")
