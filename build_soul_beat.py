#!/usr/bin/env python3
"""
Builds the "Soul Beat" melotation: sheet music (SVG) and an MP3 rendered from it.

The pattern below was transcribed from source/productions-melotations/soul-beat/soul-beat.m4a
(about 116 BPM, 4/4, a repeating one-bar groove).
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
# (slot, instrument, duration in sixteenths, loudness 0-1; loudness applies to ghost notes)
# Kick on 1 and the "&" of 3, snare on the "&" of 2, medium ghost notes on the "a" of 1
# and the "e" of 3, and light ghost notes in between. Durations fill the bar exactly.
PATTERN = [
    (0, "kick", 2, 1.00),
    (2, "ghost", 1, 0.16),
    (3, "ghost", 1, 0.40),
    (4, "ghost", 2, 0.20),
    (6, "snare", 2, 0.85),
    (8, "ghost", 1, 0.16),
    (9, "ghost", 1, 0.40),
    (10, "ghost", 2, 0.20),
    (12, "kick", 2, 0.85),
    (14, "ghost", 2, 0.16),
]


# ---------------------------------------------------------------- notation
def build_svg():
    W, H = 1000, 330
    staff_top, gap = 120, 14           # five lines: y = top + i*gap
    lines = [staff_top + i * gap for i in range(5)]
    bar_x0, bar_x1 = 190, 940
    slot_w = (bar_x1 - bar_x0 - 70) / 16.0
    first_x = bar_x0 + 45

    def sx(slot):
        return first_x + slot * slot_w

    # kick in the bottom space, snare in the third space from the bottom
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

    # notes (stems up, beamed per beat)
    stem_len = 40
    beam_y = y_snare - stem_len
    notes = {slot: (inst, dur) for slot, inst, dur, _v in PATTERN}
    for slot, (inst, dur) in notes.items():
        x, y = sx(slot), ypos[inst]
        if inst == "ghost":
            a(f'<text x="{x-14.5}" y="{y+6}" font-size="17" fill="#222">(</text>')
            a(f'<text x="{x+8}" y="{y+6}" font-size="17" fill="#222">)</text>')
        a(f'<ellipse cx="{x}" cy="{y}" rx="6.2" ry="4.6" transform="rotate(-20 {x} {y})" fill="#222"/>')
        stem_x = x + 5.8
        a(f'<line x1="{stem_x}" y1="{y-1}" x2="{stem_x}" y2="{beam_y}" stroke="#222" stroke-width="1.4"/>')
    for beat in range(4):
        slots = sorted(sl for sl in notes if beat * 4 <= sl < beat * 4 + 4)
        xs = [sx(sl) + 5.8 for sl in slots]
        a(f'<line x1="{xs[0]-0.7}" y1="{beam_y+2}" x2="{xs[-1]+0.7}" y2="{beam_y+2}" stroke="#222" stroke-width="4.5"/>')
        # second beam joins neighbouring sixteenth notes
        for sl, nxt in zip(slots, slots[1:]):
            if notes[sl][1] == 1 and notes[nxt][1] == 1 and nxt == sl + 1:
                a(f'<line x1="{sx(sl)+5.8}" y1="{beam_y+9}" x2="{sx(nxt)+5.8}" y2="{beam_y+9}" '
                  f'stroke="#222" stroke-width="3.5"/>')
    # accent on the downbeat
    x0 = sx(0)
    a(f'<path d="M{x0-6} {beam_y-14} L{x0+6} {beam_y-10} L{x0-6} {beam_y-6}" fill="none" stroke="#222" stroke-width="1.4"/>')

    # counting row under the staff
    count_y = lines[4] + 32
    labels = ["1", "e", "&amp;", "a", "2", "e", "&amp;", "a", "3", "e", "&amp;", "a", "4", "e", "&amp;", "a"]
    for i, lab in enumerate(labels):
        weight = "bold" if lab.isdigit() else "normal"
        a(f'<text x="{sx(i)}" y="{count_y}" text-anchor="middle" font-size="12" '
          f'font-weight="{weight}" fill="#777">{lab}</text>')

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
    a(f'<text x="640" y="{ly+4}" font-size="12" fill="#333">Repeat the bar throughout</text>')
    a(f'<text x="40" y="{H-18}" font-size="12" font-style="italic" fill="#666">'
      f'Kick and snare land every dotted eighth, with soft ghost notes (two levels) filling the gaps.</text>')
    a('</svg>')
    return "\n".join(o)


# ------------------------------------------------------------------- audio
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
    # ghost: short snare, scaled by the note's loudness
    t = np.arange(int(0.16 * SR)) / SR
    noise = _bp(rng.standard_normal(len(t)), 1200, 7000) * np.exp(-t * 32)
    tone = np.sin(2 * np.pi * 200 * t) * np.exp(-t * 40)
    return 0.7 * noise + 0.55 * tone


def build_mp3(mp3_path):
    rng = np.random.default_rng(7)
    sixteenth = 60.0 / BPM / 4
    total = int((BARS_IN_MP3 * 16 * sixteenth + 0.6) * SR)
    mix = np.zeros(total)
    for bar in range(BARS_IN_MP3):
        for slot, inst, _dur, vel in PATTERN:
            start = int((bar * 16 + slot) * sixteenth * SR)
            s = synth(inst, rng)
            if inst == "ghost":
                s = s * vel
            elif inst == "snare":
                s = s * vel
            else:
                s = s * vel
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
