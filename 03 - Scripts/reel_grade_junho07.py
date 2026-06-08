# -*- coding: utf-8 -*-
"""
Grade cinematografico do teaser de risoles (look filme de comida premium) +
trilha (chiado da fritura tratado) + versao muda pra trilha da plataforma.

Saidas:
  teaser_risoles_junho07_cine.mp4       (grade + trilha de chiado, ~24MB)
  teaser_risoles_junho07_cine_mudo.mp4  (grade, mudo, pra som da plataforma)

Le a duracao do teaser de origem (qualquer numero de beats) e ajusta tudo.
"""
import os
import subprocess

BASE = (r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026"
        r"\Ok - Delicias com Amor")
OUTDIR = os.path.join(BASE, "02 - Criativos", "junho07_reel")
SRC_TEASER = os.path.join(OUTDIR, "teaser_risoles_junho07.mp4")
GRADED = os.path.join(OUTDIR, "_teaser_graded.mp4")
FINAL = os.path.join(OUTDIR, "teaser_risoles_junho07_cine.mp4")
MUDO = os.path.join(OUTDIR, "teaser_risoles_junho07_cine_mudo.mp4")
SIZZLE = os.path.join(BASE, "Material 07.06 - Reels Risoles", "IMG_8555.MOV")

GRADE = (
    "colortemperature=temperature=5000:mix=0.6:pl=0.0,"
    "eq=contrast=1.11:brightness=-0.010:saturation=1.20:gamma=0.98:gamma_r=1.03:gamma_b=0.95,"
    "colorbalance=rs=-0.05:gs=-0.02:bs=0.06:rm=0.05:gm=0.01:bm=-0.04:rh=0.11:gh=0.04:bh=-0.09,"
    "curves=master='0/0.03 0.25/0.21 0.5/0.52 0.75/0.79 1/0.98':blue='0/0.04 0.5/0.48 1/0.95'"
)


def run(cmd, label):
    print(">>", label)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2200:])
        raise SystemExit(f"falhou: {label}")


def probe_dur(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
    return float(out)


def main():
    D = probe_dur(SRC_TEASER)
    print(f"Duracao do teaser: {D:.2f}s")
    fade_out = max(0.5, D - 1.3)

    # PASSO 1: grade + bloom + vinheta + grao + sharpen (mudo, crf alto p/ master)
    fc = (
        f"[0:v]{GRADE}[graded];"
        "[graded]split=2[base][glow];"
        "[glow]gblur=sigma=14,curves=master='0/0 0.6/0 0.75/0.35 1/1'[glowk];"
        "[base][glowk]blend=all_mode=screen:all_opacity=0.26[bloom];"
        "[bloom]vignette=angle=PI/5.5,"
        "noise=alls=7:allf=t+u,"
        "unsharp=luma_msize_x=5:luma_msize_y=5:luma_amount=0.5:chroma_amount=0.0,"
        "format=yuv420p[vo]"
    )
    run([
        "ffmpeg", "-y", "-i", SRC_TEASER,
        "-filter_complex", fc, "-map", "[vo]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "30", "-an",
        "-movflags", "+faststart", GRADED,
    ], "grade cinematografico")

    # PASSO 2: trilha (chiado em loop, cortado na duracao) + reencode controlado
    run([
        "ffmpeg", "-y", "-i", GRADED,
        "-stream_loop", "2", "-i", SIZZLE,
        "-filter_complex",
        f"[1:a]aformat=channel_layouts=stereo,atrim=0:{D:.2f},"
        "highpass=f=130,lowpass=f=6000,volume=1.7,alimiter=limit=0.89,"
        f"afade=t=in:d=0.7,afade=t=out:st={fade_out:.2f}:d=1.3,aresample=48000[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "22",
        "-maxrate", "11M", "-bufsize", "22M", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-shortest",
        "-movflags", "+faststart", FINAL,
    ], "trilha + reencode")

    # PASSO 3: versao muda (mesmo video, sem audio) pra trilha da plataforma
    run([
        "ffmpeg", "-y", "-i", FINAL, "-an", "-c:v", "copy",
        "-movflags", "+faststart", MUDO,
    ], "versao muda")

    # limpa intermediario pesado
    if os.path.exists(GRADED):
        os.remove(GRADED)

    print("\nCINE (com trilha):", FINAL)
    print("CINE MUDO (p/ som da plataforma):", MUDO)


if __name__ == "__main__":
    main()
