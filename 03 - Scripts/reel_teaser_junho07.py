# -*- coding: utf-8 -*-
"""
TEASER DE MARCA - Risoles - Ok Delicias com Amor - 07/06/2026

Reedicao cinematografica do reel de risoles:
- enquadramentos SEM MAO (a Oli trabalha sem luva, nao fica legal aparecer)
- macros fechados, slow-motion nos beats de textura
- crossfade (dissolve) entre cenas, ritmo de filme de produto
- overlays de texto da marca com fade in/out
- MUDO (trilha entra no app; teaser de marca e music-driven)

Beats: hook dourado -> massa -> recheio -> empanado -> oleo -> fritura -> reveal
"""
import os
import subprocess

BASE = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
        r"\Ok - Delicias com Amor")
SRC = os.path.join(BASE, "Material 07.06 - Reels Risoles")
OUTDIR = os.path.join(BASE, "02 - Criativos", "junho07_reel")
OV = os.path.join(OUTDIR, "overlays")
WORK = os.path.join(OUTDIR, "_teaser_seg")
os.makedirs(WORK, exist_ok=True)

T = 0.35  # duracao do crossfade

# nome, clipe, in, dur_fonte, fator_slow, crop("W:H:X:Y" ou None), overlay
BEATS = [
    ("hook",      "IMG_8557.MOV", 1.0, 1.6, 1.45, "1200:2133:480:850", "ov_1.png"),
    ("massacrua", "massa crua.mp4", 34.6, 1.1, 1.5, None, "ov_2.png"),
    ("massa",     "IMG_8515.MOV", 17.0, 2.2, 1.55, "1100:1956:540:1350", "ov_3.png"),
    ("recheio",   "IMG_8515.MOV", 37.6, 2.2, 1.55, "1035:1840:1080:1700", "ov_4.png"),
    ("empanado",  "IMG_8548.MOV", 2.0, 2.2, 1.45, "1500:2667:330:560", "ov_5.png"),
    ("oleo",      "IMG_8553.MOV", 4.0, 2.6, 1.30, "1515:2690:322:1150", "ov_6.png"),
    ("fritura",   "IMG_8554.MOV", 9.0, 3.2, 1.18, "1620:2880:270:600", "ov_7.png"),
    ("reveal",    "IMG_8557.MOV", 0.8, 3.2, 1.50, None, "ov_8.png"),
]


def build_beat(i, name, clip, t_in, src_dur, factor, crop, overlay):
    src = os.path.join(SRC, clip)
    ovp = os.path.join(OV, overlay)
    out = os.path.join(WORK, f"b{i}_{name}.mp4")
    D = src_dur * factor  # duracao final do beat
    fade_out_st = max(0.4, D - 0.55)

    vchain = []
    if crop:
        vchain.append(f"crop={crop}")
    vchain.append("scale=1080:1920:flags=lanczos")
    vchain.append("setsar=1")
    vchain.append(f"setpts=PTS*{factor}")
    vchain.append("fps=30")
    vfilter = "[0:v]" + ",".join(vchain) + "[v]"

    ovfilter = (f"[1:v]format=rgba,"
                f"fade=t=in:st=0.25:d=0.4:alpha=1,"
                f"fade=t=out:st={fade_out_st:.2f}:d=0.35:alpha=1[ov]")
    comp = "[v][ov]overlay=0:0:shortest=1,format=yuv420p[vo]"
    fc = ";".join([vfilter, ovfilter, comp])

    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{t_in}", "-t", f"{src_dur}", "-i", src,
        "-loop", "1", "-i", ovp,
        "-filter_complex", fc,
        "-map", "[vo]",
        "-t", f"{D:.2f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-pix_fmt", "yuv420p", "-r", "30",
        out,
    ]
    print(f"[{i}] {name:9s} {clip} in={t_in}s src={src_dur}s x{factor} -> {D:.2f}s")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1800:])
        raise SystemExit(f"falhou beat {name}")
    return out, D


def main():
    segs = []
    durs = []
    for i, b in enumerate(BEATS):
        out, D = build_beat(i, *b)
        segs.append(out)
        durs.append(D)

    # xfade chain
    inputs = []
    for s in segs:
        inputs += ["-i", s]

    # calcula offsets cumulativos
    filt = []
    last = "[0:v]"
    acc = durs[0]
    for i in range(1, len(segs)):
        offset = acc - T
        lbl = f"[x{i}]"
        filt.append(f"{last}[{i}:v]xfade=transition=fade:duration={T}:offset={offset:.3f}{lbl}")
        last = lbl
        acc = acc + durs[i] - T
    final_v = last

    # audio silencioso bem formado
    fc = ";".join(filt)
    final = os.path.join(OUTDIR, "teaser_risoles_junho07.mp4")
    cmd = ["ffmpeg", "-y"] + inputs + [
        "-f", "lavfi", "-t", f"{acc:.2f}", "-i", "anullsrc=r=48000:cl=stereo",
        "-filter_complex", fc,
        "-map", final_v, "-map", f"{len(segs)}:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "19",
        "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "128k", "-shortest",
        "-movflags", "+faststart",
        final,
    ]
    print(f"Crossfade chain -> total {acc:.2f}s")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        raise SystemExit("falhou xfade")
    print("TEASER PRONTO:", final)


if __name__ == "__main__":
    main()
