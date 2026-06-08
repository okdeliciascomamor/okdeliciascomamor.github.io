# -*- coding: utf-8 -*-
"""
Monta o Reel de Risoles 07/06 a partir dos clipes da Oli.
Corta cada clipe no ponto certo, normaliza pra 1080x1920@30fps,
queima o overlay de texto da marca, junta tudo com audio original
(ASMR de cozinha: rolo, recheio, chiado da fritura).

Sequencia: hook dourado -> massa -> recheio -> empanado -> oleo -> fritar -> pronto.
"""
import os
import subprocess

BASE = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
        r"\Ok - Delicias com Amor")
SRC = os.path.join(BASE, "Material 07.06 - Reels Risoles")
OUTDIR = os.path.join(BASE, "02 - Criativos", "junho07_reel")
OV = os.path.join(OUTDIR, "overlays")
WORK = os.path.join(OUTDIR, "_segments")
os.makedirs(WORK, exist_ok=True)

# (clipe, in, dur, overlay)
SEGS = [
    ("IMG_8557.MOV", 1.0, 1.4, "ov_1.png"),   # HOOK dourado
    ("IMG_8514.MOV", 6.0, 4.5, "ov_2.png"),   # MASSA aberta
    ("IMG_8515.MOV", 29.5, 5.0, "ov_3.png"),  # RECHEIO de legumes (colher na massa)
    ("IMG_8548.MOV", 2.0, 3.5, "ov_4.png"),   # EMPANADOS crus
    ("IMG_8549.MOV", 3.6, 3.4, "ov_5.png"),   # vai pro OLEO
    ("IMG_8555.MOV", 6.0, 4.5, "ov_6.png"),   # FRITAR dourando
    ("IMG_8557.MOV", 0.8, 5.5, "ov_7.png"),   # PRONTO + CTA
]


def build_segment(i, clip, t_in, dur, overlay):
    src = os.path.join(SRC, clip)
    ovp = os.path.join(OV, overlay)
    out = os.path.join(WORK, f"seg_{i}.mp4")
    fade_out_st = max(0.0, dur - 0.12)
    vf = ("[0:v]scale=1080:1920:flags=lanczos,setsar=1,fps=30[v];"
          "[v][1:v]overlay=0:0:format=auto[vo]")
    af = (f"afade=t=in:d=0.08,afade=t=out:st={fade_out_st:.2f}:d=0.12,"
          "aresample=48000")
    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{t_in}", "-i", src,
        "-loop", "1", "-i", ovp,
        "-t", f"{dur}",
        "-filter_complex", vf,
        "-map", "[vo]", "-map", "0:a",
        "-af", af,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2",
        "-r", "30",
        "-movflags", "+faststart",
        out,
    ]
    print(f"[seg {i}] {clip} in={t_in}s dur={dur}s + {overlay}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:])
        raise SystemExit(f"Falhou seg {i}")
    return out


def main():
    seg_files = []
    for i, (clip, t_in, dur, ov) in enumerate(SEGS, 1):
        seg_files.append(build_segment(i, clip, t_in, dur, ov))

    # concat list
    listpath = os.path.join(WORK, "concat.txt")
    with open(listpath, "w", encoding="utf-8") as f:
        for s in seg_files:
            f.write(f"file '{s}'\n")

    final = os.path.join(OUTDIR, "reel_risoles_junho07.mp4")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listpath,
           "-c", "copy", "-movflags", "+faststart", final]
    print("Concatenando...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:])
        raise SystemExit("Falhou concat")
    print("REEL PRONTO:", final)


if __name__ == "__main__":
    main()
