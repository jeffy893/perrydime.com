#!/usr/bin/env python3
"""
Builds the "Soul Beat" melotation: sheet music (SVG) and an MP3 rendered from it.

The pattern below was transcribed from source/productions-melotations/soul-beat/soul-beat.m4a
(about 116 BPM, 4/4, repeating one-bar groove built from dotted eighth notes).
Both the notation and the audio are generated from the same PATTERN list, so they always agree.

Outputs (in docs/assets/melotations/soul-beat/):
    soul-beat.svg   sheet music
    soul-beat.mp3   the beat, synthesized from the sheet music

Requires: numpy, scipy, ffmpeg (with libmp3lame) on PATH.
"""
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

OUT_DIR = Path(__file__).parent.resolve() / "docs/assets/melotations/soul-beat"

BPM = 116
BARS_IN_MP3 = 8
SR = 44100

# One bar of 4/4 = 16 sixteenth-note slots.
# (slot, instrument, duration in sixteenths)
# Five dotted eighths (3 sixteenths each) plus a sixteenth rest = 16.
PATTERN = [
    (0, "kick", 3),
    (3, "ghost", 3),
    (6, "snare", 3),
    (9, "ghost", 3),
    (12, "kick", 3),
]
REST_SLOT = 15  # sixteenth rest


# ---------------------------------------------------------------- notation
def build_svg():
    W, H = 900, 330
    staff_top, gap = 120, 14           # five lines: y = top + i*gap
    lines = [staff_top + i * gap for i in range(5)]
    bar_x0, bar_x1 = 190, 840
    slot_w = (bar_x1 - bar_x0 - 70) / 16.0
    first_x = bar_x0 + 45

    def sx(slot):
        return first_x + slot * slot_w

    # vertical positions: kick in bottom space, snare in third space from bottom
    y_kick = lines[4] - gap / 2
    y_snare = lines[2] + gap / 2
    ypos = {"kick": y_kick, "snare": y_snare, "ghost": y_snare}

    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
      f'font-family="Georgia, \'Times New Roman\', serif">')
    a('<title>Soul Beat - drum notation</title>')
    a(f'<rect width="{W}" height="{H}" fill="#fffdf8"/>')
    a(f'<text x="{W/2}" y="42" text-anchor="middle" font-size="30" font-weight="bold" fill="#222">Soul Beat</text>')
    a(f'<text x="{W/2}" y="64" text-anchor="middle" font-size="14" font-style="italic" fill="#555">for drum set</text>')
    a(f'<text x="40" y="98" font-size="14" fill="#222">'
      f'<tspan font-weight="bold">Soul</tspan> \u2022 \u2669 = {BPM}</text>')
    a(f'<text x="{W-40}" y="98" text-anchor="end" font-size="13" font-style="italic" fill="#555">Perry Dime</text>')

    # staff
    for y in lines:
        a(f'<line x1="40" y1="{y}" x2="{bar_x1}" y2="{y}" stroke="#222" stroke-width="1.2"/>')
    # opening barline
    a(f'<line x1="40" y1="{lines[0]}" x2="40" y2="{lines[4]}" stroke="#222" stroke-width="1.5"/>')
    # percussion clef: two thick vertical bars
    for cx in (80, 92):
        a(f'<rect x="{cx}" y="{lines[1]}" width="5" height="{lines[3]-lines[1]}" fill="#222"/>')
    # time signature
    for txt, y in (("4", lines[1] + 2), ("4", lines[3] + 2)):
        a(f'<text x="140" y="{y+7}" text-anchor="middle" font-size="30" font-weight="bold" fill="#222">{txt}</text>')

    # start repeat
    a(f'<line x1="{bar_x0-12}" y1="{lines[0]}" x2="{bar_x0-12}" y2="{lines[4]}" stroke="#222" stroke-width="4"/>')
    a(f'<line x1="{bar_x0-6}" y1="{lines[0]}" x2="{bar_x0-6}" y2="{lines[4]}" stroke="#222" stroke-width="1.2"/>')
    for yy in (lines[1] + gap / 2, lines[3] - gap / 2):
        a(f'<circle cx="{bar_x0}" cy="{yy}" r="2.3" fill="#222"/>')
    # end repeat
    a(f'<line x1="{bar_x1-9}" y1="{lines[0]}" x2="{bar_x1-9}" y2="{lines[4]}" stroke="#222" stroke-width="1.2"/>')
    a(f'<line x1="{bar_x1-3}" y1="{lines[0]}" x2="{bar_x1-3}" y2="{lines[4]}" stroke="#222" stroke-width="4"/>')
    for yy in (lines[1] + gap / 2, lines[3] - gap / 2):
        a(f'<circle cx="{bar_x1-15}" cy="{yy}" r="2.3" fill="#222"/>')

    # notes
    stem_len = 40
    for slot, inst, dur in PATTERN:
        x, y = sx(slot), ypos[inst]
        ghost = inst == "ghost"
        if ghost:
            # parentheses around the notehead
            a(f'<text x="{x-14}" y="{y+6}" font-size="18" fill="#222">(</text>')
            a(f'<text x="{x+7.5}" y="{y+6}" font-size="18" fill="#222">)</text>')
        a(f'<ellipse cx="{x}" cy="{y}" rx="6.2" ry="4.6" transform="rotate(-20 {x} {y})" fill="#222"/>')
        sx_stem = x + 5.8
        a(f'<line x1="{sx_stem}" y1="{y-1}" x2="{sx_stem}" y2="{y-stem_len}" stroke="#222" stroke-width="1.4"/>')
        # eighth flag
        top = y - stem_len
        a(f'<path d="M{sx_stem} {top} c 2 10 16 14 12 30 c 2 -10 -6 -14 -12 -16 z" fill="#222"/>')
        # augmentation dot
        a(f'<circle cx="{x+14}" cy="{y-gap/4}" r="2" fill="#222"/>')
        if inst == "kick" and slot == 0:
            # accent on the downbeat
            a(f'<path d="M{x-6} {top-12} L{x+6} {top-8} L{x-6} {top-4}" fill="none" stroke="#222" stroke-width="1.4"/>')

    # sixteenth rest
    rx, ry = sx(REST_SLOT) + 4, lines[2]
    a(f'<circle cx="{rx-2}" cy="{ry-7}" r="2.6" fill="#222"/>')
    a(f'<circle cx="{rx-5}" cy="{ry+2}" r="2.6" fill="#222"/>')
    a(f'<path d="M{rx+3} {ry-12} L{rx-6} {ry+14}" stroke="#222" stroke-width="1.8" fill="none"/>')

    # counting row under the staff
    count_y = lines[4] + 32
    labels = ["1", "e", "&", "a", "2", "e", "&", "a", "3", "e", "&", "a", "4", "e", "&", "a"]
    for i, lab in enumerate(labels):
        weight = "bold" if lab.isdigit() else "normal"
        a(f'<text x="{sx(i)}" y="{count_y}" text-anchor="middle" font-size="12" '
          f'font-weight="{weight}" fill="#777">{"&amp;" if lab == "&" else lab}</text>')

    # legend
    ly = H - 52
    a(f'<ellipse cx="60" cy="{ly}" rx="5.5" ry="4" transform="rotate(-20 60 {ly})" fill="#222"/>')
    a(f'<text x="74" y="{ly+4}" font-size="12" fill="#333">Kick (bottom space)</text>')
    a(f'<ellipse cx="230" cy="{ly}" rx="5.5" ry="4" transform="rotate(-20 230 {ly})" fill="#222"/>')
    a(f'<text x="244" y="{ly+4}" font-size="12" fill="#333">Snare (third space)</text>')
    a(f'<text x="395" y="{ly+5}" font-size="15" fill="#222">(</text>'
      f'<ellipse cx="410" cy="{ly}" rx="5.5" ry="4" transform="rotate(-20 410 {ly})" fill="#222"/>'
      f'<text x="418" y="{ly+5}" font-size="15" fill="#222">)</text>')
    a(f'<text x="432" y="{ly+4}" font-size="12" fill="#333">Ghost note (soft snare)</text>')
    a(f'<text x="620" y="{ly+4}" font-size="12" fill="#333">Repeat the bar throughout</text>')
    a(f'<text x="40" y="{H-18}" font-size="12" font-style="italic" fill="#666">'
      f'Five dotted eighths and a sixteenth rest: a 3+3+3+3+3+1 groove that cycles against the 4/4 pulse.</text>')
    a('</svg>')
    return "\n".join(o)


# ------------------------------------------------------------------- audio
def _lp(x, hz, order=2):
    b, a = butter(order, hz / (SR / 2), btype="low")
    return lfilter(b, a, x)


def _bp(x, lo, hi):
    b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], btype="band")
    return lfilter(b, a, x)


def synth(inst, rng):
    if inst == "kick":
        t = np.arange(int(0.45 * SR)) / SR
        freq = 45 + 85 * np.exp(-t * 28)
        phase = 2 * np.pi * np.cumsum(freq) / SR
        body = np.sin(phase) * np.exp(-t * 9)
        click = _bp(rng.standard_normal(len(t)), 1500, 5000) * np.exp(-t * 180) * 0.25
        return 0.95 * (body + click)
    if inst == "snare":
        t = np.arange(int(0.32 * SR)) / SR
        noise = _bp(rng.standard_normal(len(t)), 1200, 8000) * np.exp(-t * 17)
        tone = (np.sin(2 * np.pi * 190 * t) + 0.5 * np.sin(2 * np.pi * 330 * t)) * np.exp(-t * 26)
        return 0.7 * noise + 0.55 * tone
    # ghost: quiet, short snare
    t = np.arange(int(0.16 * SR)) / SR
    noise = _bp(rng.standard_normal(len(t)), 1200, 7000) * np.exp(-t * 32)
    tone = np.sin(2 * np.pi * 200 * t) * np.exp(-t * 40)
    return 0.22 * (0.7 * noise + 0.55 * tone)


def build_mp3(mp3_path):
    rng = np.random.default_rng(7)
    sixteenth = 60.0 / BPM / 4
    total = int((BARS_IN_MP3 * 16 * sixteenth + 0.6) * SR)
    mix = np.zeros(total)
    for bar in range(BARS_IN_MP3):
        for slot, inst, _dur in PATTERN:
            start = int((bar * 16 + slot) * sixteenth * SR)
            s = synth(inst, rng)
            mix[start:start + len(s)] += s[: total - start]
    mix = np.tanh(1.4 * mix) / np.tanh(1.4)
    mix = 0.9 * mix / np.max(np.abs(mix))
    with tempfile.TemporaryDirectory() as d:
        wav = Path(d) / "beat.wav"
        wavfile.write(wav, SR, (mix * 32767).astype(np.int16))
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
             "-codec:a", "libmp3lame", "-b:a", "192k",
             "-metadata", "title=Soul Beat", "-metadata", "artist=Perry Dime",
             str(mp3_path)],
            check=True,
        )


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "soul-beat.svg").write_text(build_svg(), encoding="utf-8")
    build_mp3(OUT_DIR / "soul-beat.mp3")
    print(f"Wrote {OUT_DIR}/soul-beat.svg and soul-beat.mp3")


if __name__ == "__main__":
    main()
