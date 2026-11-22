#!/usr/bin/env python3.10
"""
Builds the "Shareholder Son" vocal melotation: sheet music with lyrics (SVG, via Verovio)
and an MP3 sung from that sheet music.

The melody was reverse-engineered from a voice recording (pitch tracking plus syllable timing).
The MP3 is made from the notes below, not from the recording: each syllable is spoken by the
macOS speech voice, then re-pitched and stretched to the written note with PSOLA
(pitch-synchronous overlap-add), which keeps the vowel colour while changing pitch and length.

Pitches here are sounding pitches. The score uses a treble clef with an 8 beneath it, the
usual way to write a low voice.

Outputs go to docs/assets/melotations/shareholder-son/
Requires: verovio, numpy, ffmpeg (with libmp3lame), and the macOS `say` command.
"""
import subprocess
import tempfile
import wave
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np

from build_guitar_melotations import OUT_ROOT, midi, parse_pitch
import build_guitar_melotations as g

SLUG = "shareholder-son"
TITLE = "Shareholder Son"
BPM = 120
SIXTEENTH = 60.0 / BPM / 4
VOICE = "Alex"

# (pitch, length in sixteenths, syllable text, syllabic) ; pitch None = rest ; tie flag last
# Sixteenth-note grid measured from the recording (one sixteenth = 0.125 s at 120 BPM).
BARS = [
    [("B2", 4, "my", "single", False),
     ("G3", 3, "share", "begin", False),
     ("F3", 2, "hold", "middle", False),
     ("D#3", 3, "er", "end", False),
     ("A2", 4, "son", "single", True)],
    [("A2", 4, None, None, False),
     (None, 1, None, None, False),
     ("C#3", 1, "I", "single", False),
     ("D3", 3, "give", "single", False),
     ("D3", 3, "my", "single", False),
     ("F3", 3, "chair", "single", False),
     (None, 1, None, None, False)],
    [("A2", 2, "to", "single", False),
     ("A2", 6, "you", "single", False),
     (None, 8, None, None, False)],
]

TYPE = {1: ("16th", 0), 2: ("eighth", 0), 3: ("eighth", 1), 4: ("quarter", 0),
        6: ("quarter", 1), 8: ("half", 0), 12: ("half", 1), 16: ("whole", 0)}


def musicxml():
    x = ['<?xml version="1.0" encoding="UTF-8"?>', '<score-partwise version="3.1">',
         f'<work><work-title>{escape(TITLE)}</work-title></work>',
         '<part-list><score-part id="P1"><part-name>Voice</part-name>'
         '<part-abbreviation>Vo.</part-abbreviation></score-part></part-list>', '<part id="P1">']
    prev_tied = False
    for i, bar in enumerate(BARS):
        x.append(f'<measure number="{i + 1}">')
        if i == 0:
            x.append('<attributes><divisions>4</divisions><key><fifths>0</fifths></key>'
                     '<time><beats>4</beats><beat-type>4</beat-type></time>'
                     '<clef><sign>G</sign><line>2</line><clef-octave-change>-1</clef-octave-change></clef>'
                     '</attributes>')
            x.append(f'<direction placement="above"><direction-type><words font-style="italic">'
                     f'approx. {BPM} beats per minute, chanted</words></direction-type></direction>')
        state = {}
        for pitch, dur, text, syl, tie in bar:
            typ, dots = TYPE[dur]
            dot = '<dot/>' * dots
            if pitch is None:
                x.append(f'<note><rest/><duration>{dur}</duration><type>{typ}</type>{dot}</note>')
                prev_tied = False
                continue
            step, alt, octv = parse_pitch(pitch)
            cur = state.get((step, octv), 0)
            show = None
            if not prev_tied and alt != cur:
                show = {1: "sharp", -1: "flat", 0: "natural"}[alt]
            state[(step, octv)] = alt
            s = '<note><pitch>' + f'<step>{step}</step>' + (f'<alter>{alt}</alter>' if alt else '')
            s += f'<octave>{octv}</octave></pitch><duration>{dur}</duration>'
            if prev_tied:
                s += '<tie type="stop"/>'
            if tie:
                s += '<tie type="start"/>'
            s += f'<type>{typ}</type>{dot}'
            if show:
                s += f'<accidental>{show}</accidental>'
            if prev_tied or tie:
                s += '<notations>' + ('<tied type="stop"/>' if prev_tied else '') + \
                     ('<tied type="start"/>' if tie else '') + '</notations>'
            if text:
                s += f'<lyric number="1"><syllabic>{syl}</syllabic><text>{escape(text)}</text></lyric>'
            s += '</note>'
            x.append(s)
            prev_tied = tie
        x.append('</measure>')
    x.append('</part></score-partwise>')
    return "\n".join(x)


def render_svg(path):
    import verovio
    tk = verovio.toolkit()
    tk.setOptions({"pageWidth": 1800, "pageHeight": 60000, "scale": 60,
                   "adjustPageHeight": True, "breaks": "auto",
                   "pageMarginLeft": 60, "pageMarginRight": 60,
                   "pageMarginTop": 60, "pageMarginBottom": 60,
                   "footer": "none", "header": "auto"})
    tk.loadData(musicxml())
    if tk.getPageCount() != 1:
        raise RuntimeError("expected one page")
    import re
    svg = tk.renderToSVG(1)
    svg = re.sub(r"(<svg[^>]*>)", r'\1<rect width="100%" height="100%" fill="#fffdf8"/>', svg, count=1)
    Path(path).write_text(svg, encoding="utf-8")


# ------------------------------------------------------------------ voice
VSR = 22050


def read_wav(path):
    with wave.open(str(path)) as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    return data


def speak(text, tmp):
    aiff = Path(tmp) / f"{text}.aiff"
    wav = Path(tmp) / f"{text}.wav"
    # [[pmod 0]] flattens the speech melody; [[pbas]] sets a low base pitch; slow rate gives longer vowels
    subprocess.run(["say", "-v", VOICE, "-r", "110", "-o", str(aiff),
                    f"[[pbas 38]][[pmod 0]] {text}"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(aiff), "-ac", "1",
                    "-ar", str(VSR), "-sample_fmt", "s16", str(wav)], check=True)
    x = read_wav(wav)
    keep = np.where(np.abs(x) > 0.01 * np.max(np.abs(x)))[0]
    return x[keep[0]: keep[-1] + 1]


def analyse(x):
    """Return period P0 (samples), voiced span (v0, v1) and pitch marks inside it."""
    hop = int(0.01 * VSR)
    win = int(0.03 * VSR)
    lo, hi = int(VSR / 400), int(VSR / 60)
    peak_rms = np.sqrt((x ** 2).mean())
    frames = []
    for i in range(0, len(x) - win - hi, hop):
        seg = x[i:i + win]
        rms = np.sqrt((seg ** 2).mean())
        if rms < 0.25 * peak_rms:
            frames.append((i, 0.0, 0))
            continue
        ref = x[i:i + win + hi]
        ac = np.array([np.dot(seg, ref[t:t + win]) for t in range(lo, hi)])
        norm = np.sqrt(np.dot(seg, seg) * np.dot(ref[:win], ref[:win])) + 1e-9
        k = int(np.argmax(ac))
        frames.append((i, ac[k] / norm, lo + k))
    voiced = [f for f in frames if f[1] > 0.6]
    if not voiced:
        raise RuntimeError("no voiced region found")
    periods = sorted(f[2] for f in voiced)
    p0 = periods[len(periods) // 2]
    v0 = voiced[0][0]
    v1 = voiced[-1][0] + win
    # pitch marks: positive peaks one period apart, starting at the strongest peak
    seed_lo = v0 + (v1 - v0) // 3
    seed = seed_lo + int(np.argmax(x[seed_lo: seed_lo + 2 * p0]))
    marks = [seed]
    while marks[-1] + p0 * 1.2 < v1:
        c = marks[-1] + p0
        a, b = int(c - 0.2 * p0), int(c + 0.2 * p0)
        marks.append(a + int(np.argmax(x[a:b])))
    while marks[0] - p0 * 1.2 > v0:
        c = marks[0] - p0
        a, b = int(c - 0.2 * p0), int(c + 0.2 * p0)
        marks.insert(0, a + int(np.argmax(x[a:b])))
    return p0, v0, v1, np.array(marks)


def sing_syllable(x, f0_hz, dur_s, rng):
    p0, v0, v1, marks = analyse(x)
    pre = x[:v0]
    post = x[v1:]
    voiced_dur = max(dur_s - (len(pre) + len(post)) / VSR, 0.12)
    n_voiced = int(voiced_dur * VSR)
    out = np.zeros(n_voiced + 2 * p0 * 4)
    t = 0.0
    k = 0
    vib_phase = rng.uniform(0, 6.28)
    span = max(v1 - v0, 1)
    while t < n_voiced:
        frac = t / n_voiced
        a = v0 + frac * span                         # stretch the voiced part evenly
        idx = int(np.argmin(np.abs(marks - a)))
        m = marks[idx]
        lo, hi = max(m - p0, 0), min(m + p0, len(x))
        seg = x[lo:hi] * np.hanning(hi - lo)
        start = int(t) + p0 - (m - lo)
        if start >= 0 and start + len(seg) <= len(out):
            out[start:start + len(seg)] += seg
        sec = t / VSR
        vib = 1 + 0.010 * np.sin(2 * np.pi * 5.3 * sec + vib_phase) * min(sec / 0.25, 1.0)
        t += VSR / (f0_hz * vib)
        k += 1
    voiced_out = out[p0: p0 + n_voiced]
    # short fades at the joins
    f = min(int(0.01 * VSR), len(voiced_out) // 4)
    voiced_out[:f] *= np.linspace(0, 1, f)
    voiced_out[-f:] *= np.linspace(1, 0, f)
    return np.concatenate([pre, voiced_out, post])


def reverb(x):
    n = int(0.9 * VSR)
    rng = np.random.default_rng(5)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / (VSR * 0.22))
    ir[0] = 0
    wet = np.fft.irfft(np.fft.rfft(x, len(x) + n) * np.fft.rfft(ir, len(x) + n), len(x) + n)
    dry = np.concatenate([x, np.zeros(n)])
    return dry + 0.035 * wet


def build_mp3(mp3_path):
    rng = np.random.default_rng(11)
    events = []
    slot = 0
    for bar in BARS:
        for pitch, dur, text, syl, tie in bar:
            if pitch is not None and text:
                # merge the tied continuation
                total = dur
                events.append([slot, total, pitch, text])
            elif pitch is not None and events:
                events[-1][1] += dur           # tied tail of the previous syllable
            slot += dur
    cache = {}
    with tempfile.TemporaryDirectory() as tmp:
        for _s, _d, _p, text in events:
            if text not in cache:
                cache[text] = speak(text, tmp)
        end_slot = max(e[0] + e[1] for e in events)
        total_n = int((end_slot * SIXTEENTH + 2.0) * VSR)
        mix = np.zeros(total_n)
        for start, dur, pitch, text in events:
            f0 = 440.0 * 2 ** ((midi(pitch) - 69) / 12.0)
            seg = sing_syllable(cache[text], f0, dur * SIXTEENTH, rng)
            seg = seg / (np.max(np.abs(seg)) + 1e-9) * 0.8
            # nudge notes with long vowels to ring a little
            off = int(start * SIXTEENTH * VSR)
            mix[off:off + len(seg)] += seg[: total_n - off]
        mix = reverb(mix)
        mix = mix / np.max(np.abs(mix)) * 0.9
        wav = Path(tmp) / "voice.wav"
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(VSR)
            w.writeframes((mix * 32767).astype(np.int16).tobytes())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ar", "44100",
                        "-codec:a", "libmp3lame", "-b:a", "128k",
                        "-metadata", f"title={TITLE}", "-metadata", "artist=Perry Dime",
                        str(mp3_path)], check=True)


def main():
    for bar in BARS:
        if sum(n[1] for n in bar) != 16:
            raise ValueError("bar does not add up to 16 sixteenths")
    out = OUT_ROOT / SLUG
    out.mkdir(parents=True, exist_ok=True)
    render_svg(out / f"{SLUG}.svg")
    build_mp3(out / f"{SLUG}.mp3")
    print(f"{SLUG}: written to {out}")


if __name__ == "__main__":
    main()
