#!/usr/bin/env python3.10
"""
Builds guitar melotations: sheet music (SVG, engraved with Verovio) and an MP3
synthesized from the same note data (plucked-string model).

The pieces were transcribed by hand from the scores printed in the Survitality book
(pub.perrydime.com/survitality/*_intercourse.jpg). Guitar music is written an octave
above where it sounds (treble clef 8vb), and the audio follows that.

Note format, one string per bar, bars joined by '|':
    E5:4        pitch and length in sixteenths (4 = quarter, 2 = eighth, 8 = half, 16 = whole)
    r:4         rest
    [A4 C#5]:16 chord
    suffix ~    tie into the next note or chord of the same pitches

Outputs go to docs/assets/melotations/<slug>/<slug>.svg and .mp3
Requires: verovio, numpy, scipy, ffmpeg with libmp3lame.
"""
import re
import subprocess
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
import wave

OUT_ROOT = Path(__file__).parent.resolve() / "docs/assets/melotations"
SR = 44100

# ----------------------------------------------------------------- scores
# Arpeggio bars of "Artificial_Intercourse"
A = "E5:4 C#6:4 A5:4 C#6:4"        # A major
G = "D5:4 B5:4 G5:4 B5:4"          # G major
D = "A4:4 F#5:4 D5:4 F#5:4"        # D major
E = "B4:4 G#5:4 E5:4 G#5:4"        # E major
CH_T = "[A4 C#5 E5 A5]:16~"        # A major chord, tied into the next bar
CH = "[A4 C#5 E5 A5]:16"
D_T = "A4:4 F#5:4 D5:4 F#5:4~"
D_FROM_TIE = "F#5:4 F#5:4 D5:4 F#5:4"

ARTIFICIAL = [
    # 1-7
    A, A, G, G, A, A, G,
    # 8-16
    G, A, G, D, E, CH_T, CH, CH_T, CH,
    # 17-25
    A, G, D, E, CH_T, CH, CH_T, CH, A,
    # 26-32
    G, D, "G3:4 G5:4 B3:4 G5:4", D_T, D_FROM_TIE, D_T, D_FROM_TIE,
    # 33-42
    "G3:4 G5:4 B3:4 G5:4", D, "F4:4 F5:4 A4:4 F5:4~", "F5:4 F5:4 C5:4 F5:4",
    "A4:4 G5:4 B4:4 G5:4~", "G5:4 G5:4 D5:4 G5:4", CH_T, CH, CH_T, CH,
    # 43-55
    "[B3 D5 G5]:8 [D4 A4 D5 F#5]:8", "[G4 B4 D5 F5]:8 [A4 D5 F#5 A5]:8",
    CH_T, CH, CH_T, CH,
    "[B3 D5 G5]:8 [D4 A4 D5 F#5]:8", "[G4 B4 D5 F5]:8 [A4 D5 F#5 A5]:8",
    CH_T, CH, CH_T, CH, A,
    # 56-62
    A, G, G, A, A, G, G,
    # 63-70
    A, G, D, E, "A4:4 C#5:4 E5:4 A5:4", "r:16", "r:16", "r:16",
]

NATURAL = [
    "E5:4",                              # pick-up bar
    "A5:4 G5:4 E5:4",
    "G#5:2 A5:8 r:2",
    "r:12",
    "r:4 r:4 A5:2 B5:2",
    "C6:4 B5:4 E5:4",
    "E5:2 F5:2 E5:4 D5:4",
    "r:12",
    "r:4 r:4 B4:2 C5:2",
    "D5:4 C5:4 B4:4",
    "B4:2 C5:4 B4:2 A4:4",
    "r:12",
    "B4:4 A4:4 G4:4",
    "D4:4 D#4:4 E4:4",
] + ["r:12"] * 18

PIECES = [
    {
        "slug": "artificial-intercourse",
        "title": "Artificial_Intercourse",
        "bars": ARTIFICIAL,
        "beats": 4, "beat_type": 4, "bpm": 112, "pickup": False,
    },
    {
        "slug": "natural-intercourse",
        "title": "Natural_Intercourse",
        "bars": NATURAL,
        "beats": 3, "beat_type": 4, "bpm": 84, "pickup": True,
    },
]

# ------------------------------------------------------------------ parse
TOKEN = re.compile(r"\[([^\]]+)\]:(\d+)(~?)|([A-Gr][#b]?\d?):(\d+)(~?)")
STEP_SEMI = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def parse_pitch(p):
    m = re.match(r"([A-G])([#b]?)(\d)", p)
    step, acc, octv = m.group(1), m.group(2), int(m.group(3))
    return step, {"#": 1, "b": -1, "": 0}[acc], octv


def midi(p):
    step, alt, octv = parse_pitch(p)
    return 12 * (octv + 1) + STEP_SEMI[step] + alt


def parse_bar(text):
    out = []
    for m in TOKEN.finditer(text):
        if m.group(1) is not None:
            pitches, dur, tie = m.group(1).split(), int(m.group(2)), bool(m.group(3))
        else:
            pitches = [] if m.group(4) == "r" else [m.group(4)]
            dur, tie = int(m.group(5)), bool(m.group(6))
        out.append({"pitches": pitches, "dur": dur, "tie_start": tie, "tie_stop": False})
    return out


def parse_piece(piece):
    bars = [parse_bar(b) for b in piece["bars"]]
    prev = None
    for bar in bars:
        for n in bar:
            if prev is not None and prev["tie_start"] and prev["pitches"] == n["pitches"]:
                n["tie_stop"] = True
            prev = n
    return bars


# -------------------------------------------------------------- MusicXML
TYPE = {1: "16th", 2: "eighth", 4: "quarter", 8: "half", 12: "half", 16: "whole"}


def musicxml(piece, bars):
    beats = piece["beats"]
    bar_len = beats * 4
    x = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<score-partwise version="3.1">',
         f'<work><work-title>{escape(piece["title"])}</work-title></work>',
         '<part-list><score-part id="P1"><part-name>Guitar</part-name>'
         '<part-abbreviation>Guit.</part-abbreviation></score-part></part-list>',
         '<part id="P1">']
    for i, bar in enumerate(bars):
        implicit = ""   # the printed score numbers the pick-up bar as measure 1
        num = i + 1
        x.append(f'<measure number="{num}"{implicit}>')
        if i == 0:
            x.append(f'<attributes><divisions>4</divisions><key><fifths>0</fifths></key>'
                     f'<time><beats>{beats}</beats><beat-type>{piece["beat_type"]}</beat-type></time>'
                     '<clef><sign>G</sign><line>2</line><clef-octave-change>-1</clef-octave-change></clef>'
                     '</attributes>')
            x.append(f'<direction placement="above"><direction-type>'
                     f'<words font-style="italic">approx. {piece["bpm"]} beats per minute</words>'
                     '</direction-type></direction>')
        state = {}
        total = sum(n["dur"] for n in bar)
        whole_rest = len(bar) == 1 and not bar[0]["pitches"] and total == bar_len
        # beams: pair consecutive eighth notes inside one beat
        pos = 0
        beam_of = {}
        for j, n in enumerate(bar):
            nxt = bar[j + 1] if j + 1 < len(bar) else None
            if (n["dur"] == 2 and n["pitches"] and nxt and nxt["dur"] == 2 and nxt["pitches"]
                    and pos % 4 == 0):
                beam_of[j] = "begin"
                beam_of[j + 1] = "end"
            pos += n["dur"]
        for j, n in enumerate(bar):
            if not n["pitches"]:
                if whole_rest:
                    x.append(f'<note><rest measure="yes"/><duration>{n["dur"]}</duration></note>')
                else:
                    x.append(f'<note><rest/><duration>{n["dur"]}</duration><type>{TYPE[n["dur"]]}</type></note>')
                continue
            for k, p in enumerate(n["pitches"]):
                step, alt, octv = parse_pitch(p)
                key = (step, octv)
                cur = state.get(key, 0)
                show = None
                if not n["tie_stop"] and alt != cur:
                    show = {1: "sharp", -1: "flat", 0: "natural"}[alt]
                state[key] = alt
                s = '<note>'
                if k:
                    s += '<chord/>'
                s += f'<pitch><step>{step}</step>'
                if alt:
                    s += f'<alter>{alt}</alter>'
                # MusicXML stores sounding pitch; the 8vb clef then displays it an octave higher
                s += f'<octave>{octv - 1}</octave></pitch><duration>{n["dur"]}</duration>'
                if n["tie_stop"]:
                    s += '<tie type="stop"/>'
                if n["tie_start"]:
                    s += '<tie type="start"/>'
                s += f'<type>{TYPE[n["dur"]]}</type>'
                if n["dur"] == 12:
                    s += '<dot/>'
                if show:
                    s += f'<accidental>{show}</accidental>'
                if n["dur"] < 8 and n["dur"] != 4 or (n["dur"] == 4 and False):
                    pass
                if j in beam_of and k == 0:
                    s += f'<beam number="1">{beam_of[j]}</beam>'
                elif j in beam_of:
                    s += f'<beam number="1">{beam_of[j]}</beam>'
                if n["tie_stop"] or n["tie_start"]:
                    s += '<notations>'
                    if n["tie_stop"]:
                        s += '<tied type="stop"/>'
                    if n["tie_start"]:
                        s += '<tied type="start"/>'
                    s += '</notations>'
                s += '</note>'
                x.append(s)
        x.append('</measure>')
    x.append('</part></score-partwise>')
    return "\n".join(x)


def render_svg(piece, bars, path):
    import verovio
    tk = verovio.toolkit()
    tk.setOptions({
        "pageWidth": 2100, "pageHeight": 60000, "scale": 55,
        "adjustPageHeight": True, "breaks": "auto",
        "pageMarginLeft": 60, "pageMarginRight": 60,
        "pageMarginTop": 60, "pageMarginBottom": 60,
        "footer": "none", "header": "auto",
    })
    tk.loadData(musicxml(piece, bars))
    if tk.getPageCount() != 1:
        raise RuntimeError(f"expected one page, got {tk.getPageCount()}")
    svg = tk.renderToSVG(1)
    # white background so the score reads on any page colour
    svg = re.sub(r"(<svg[^>]*>)", r'\1<rect width="100%" height="100%" fill="#fffdf8"/>', svg, count=1)
    Path(path).write_text(svg, encoding="utf-8")


# ------------------------------------------------------------------ audio
def pluck(freq, seconds, vel, rng):
    n_samp = int(seconds * SR)
    delay = SR / freq - 0.5
    n = int(np.floor(delay))
    frac = delay - n
    g = 0.996
    t0 = (1 - frac) * 0.5 * g
    t1 = 0.5 * g
    t2 = frac * 0.5 * g
    off = n + 3
    y = np.zeros(n_samp + off)
    burst = rng.uniform(-1, 1, n + 2)
    burst = np.convolve(burst, [0.5, 0.5], mode="same")      # soften the attack
    y[off: off + len(burst)] = burst
    # comb filter with a fractional delay, evaluated one block of n samples at a time
    for b in range(off, len(y), n):
        e = min(b + n, len(y))
        idx = np.arange(b, e)
        y[b:e] += t0 * y[idx - n] + t1 * y[idx - n - 1] + t2 * y[idx - n - 2]
    y = y[off:]
    env = np.exp(-np.arange(n_samp) / (SR * 3.5))
    return vel * y * env


def synth(piece, bars, mp3_path):
    rng = np.random.default_rng(3)
    sixteenth = 60.0 / piece["bpm"] / 4
    # flatten into events, merging ties
    events = []   # (start_slot, pitches, dur_slots)
    slot = 0
    open_tie = {}
    for bar in bars:
        for n in bar:
            if n["pitches"]:
                key = tuple(n["pitches"])
                if n["tie_stop"] and key in open_tie:
                    ev = open_tie[key]
                    ev[2] += n["dur"]
                    if not n["tie_start"]:
                        del open_tie[key]
                else:
                    ev = [slot, list(n["pitches"]), n["dur"]]
                    events.append(ev)
                    if n["tie_start"]:
                        open_tie[key] = ev
            slot += n["dur"]
    last = max(e[0] + e[2] for e in events)
    total = int((last * sixteenth + 5.0) * SR)
    mix = np.zeros(total)
    for start, pitches, dur in events:
        t0 = start * sixteenth
        ring = min(dur * sixteenth + 1.2, 6.0)
        for i, p in enumerate(sorted(pitches, key=midi)):
            freq = 440.0 * 2 ** ((midi(p) - 12 - 69) / 12.0)    # sounds an octave below written
            vel = 0.9 if len(pitches) == 1 else 0.7
            s = pluck(freq, ring, vel, rng)
            # short fade at the end of the note's written length
            fade_from = int(dur * sixteenth * SR)
            if fade_from < len(s):
                tail = len(s) - fade_from
                s[fade_from:] *= np.exp(-np.arange(tail) / (SR * 0.35))
            off = int((t0 + 0.012 * i) * SR)
            mix[off:off + len(s)] += s[: total - off]
    # gentle warmth + normalize
    mix = np.convolve(mix, [0.35, 0.35, 0.3])[: len(mix)]
    mix = np.tanh(1.2 * mix / np.max(np.abs(mix))) * 0.85
    with tempfile.TemporaryDirectory() as d:
        wav = Path(d) / "g.wav"
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((mix * 32767).astype(np.int16).tobytes())
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ac", "1",
             "-codec:a", "libmp3lame", "-b:a", "96k",
             "-metadata", f"title={piece['title']}", "-metadata", "artist=Perry Dime",
             str(mp3_path)],
            check=True)


def main():
    for piece in PIECES:
        bars = parse_piece(piece)
        total = sum(n["dur"] for n in bars[1]) if piece["pickup"] else None
        for i, bar in enumerate(bars):
            full = piece["beats"] * 4
            got = sum(n["dur"] for n in bar)
            if got != full and not (piece["pickup"] and i == 0):
                raise ValueError(f"{piece['slug']} bar {i + 1}: {got} sixteenths, expected {full}")
        out = OUT_ROOT / piece["slug"]
        out.mkdir(parents=True, exist_ok=True)
        render_svg(piece, bars, out / f"{piece['slug']}.svg")
        synth(piece, bars, out / f"{piece['slug']}.mp3")
        print(f"{piece['slug']}: {len(bars)} bars written to {out}")


if __name__ == "__main__":
    main()
