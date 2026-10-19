# Synthesized soundtrack synced to window.EVENTS exported by top10.html
import json, wave, numpy as np
sr = 44100
events = json.load(open('events.json'))
dur = 7 + 10 * 6.5 + 6.5
n = int(sr * dur); t = np.arange(n) / sr
rng = np.random.default_rng(7)
out = np.zeros(n)

def add(start, sig, amp=1.0):
    i = int(start * sr)
    if i >= n: return
    m = min(len(sig), n - i); out[i:i + m] += amp * sig[:m]

def env(L, a, d):
    x = np.arange(int(L * sr)) / sr
    return np.where(x < a, x / a, np.exp(-(x - a) / d))

# pad: Am - F - C - G, 4 bars of 2s each, looped
chords = [[110, 130.81, 164.81, 220], [87.31, 110, 130.81, 174.61], [65.41, 130.81, 164.81, 196], [98, 123.47, 146.83, 196]]
pad = np.zeros(n)
for b in range(int(dur / 2) + 1):
    seg = (t >= b * 2) & (t < b * 2 + 2)
    for f in chords[b % 4]:
        pad[seg] += np.sin(2 * np.pi * f * t[seg]) + .3 * np.sin(2 * np.pi * 2 * f * t[seg] + .5)
lfo = .6 + .4 * np.sin(2 * np.pi * .25 * t)
out += .022 * pad * lfo * np.clip(t / 2.5, 0, 1)

# beat (120 bpm) from the title hit to the end
kick_L = .35; x = np.arange(int(kick_L * sr)) / sr
kick = np.sin(2 * np.pi * (48 + 110 * np.exp(-x * 28)) * x) * np.exp(-x * 9)
hat = rng.standard_normal(int(.04 * sr)) * np.exp(-np.arange(int(.04 * sr)) / sr * 120)
snare = rng.standard_normal(int(.2 * sr)) * np.exp(-np.arange(int(.2 * sr)) / sr * 22)
bass_notes = [55, 43.65, 65.41, 49]
for k, bt in enumerate(np.arange(2.85, dur - .6, .5)):
    add(bt, kick, .55)
    add(bt + .25, hat, .10)
    if k % 2: add(bt, snare, .16)
    f = bass_notes[int(bt // 2) % 4]; xb = np.arange(int(.45 * sr)) / sr
    add(bt, np.sign(np.sin(2 * np.pi * f * xb)) * np.exp(-xb * 6) * .5 + np.sin(2 * np.pi * f * xb) * np.exp(-xb * 4), .09)

noise = rng.standard_normal(int(1.2 * sr))
whoosh = np.convolve(noise, np.ones(60) / 60, 'same') * np.sin(np.linspace(0, np.pi, len(noise))) ** 2
for e in events:
    s, ty = e['t'], e['type']
    if ty == 'type':
        L = int(.012 * sr); add(s, rng.standard_normal(L) * np.exp(-np.arange(L) / sr * 400), .18 * (.7 + .6 * rng.random()))
    elif ty == 'enter':
        L = int(.03 * sr); add(s, rng.standard_normal(L) * np.exp(-np.arange(L) / sr * 200), .3)
    elif ty == 'out':
        xb = np.arange(int(.1 * sr)) / sr; add(s, np.sin(2 * np.pi * 1320 * xb) * np.exp(-xb * 40), .07)
    elif ty in ('whoosh', 'whoosh_out'):
        add(s - .6 if ty == 'whoosh' else s - .3, whoosh, 1.1 if ty == 'whoosh' else .6)
    elif ty in ('impact', 'impact_small'):
        xb = np.arange(int(1.2 * sr)) / sr
        add(s, np.sin(2 * np.pi * (40 + 70 * np.exp(-xb * 18)) * xb) * np.exp(-xb * 2.5), .9 if ty == 'impact' else .35)
    elif ty == 'sparkle':
        for i, f in enumerate([1318.5, 1568, 1975.5, 2637]):
            xb = np.arange(int(.6 * sr)) / sr; add(s + i * .08, np.sin(2 * np.pi * f * xb) * np.exp(-xb * 6), .09)

out *= np.clip((dur - t) / .8, 0, 1)
out = np.tanh(out / np.max(np.abs(out)) * 1.4) * .89
st = np.stack([out, np.roll(out, 220)], 1)
with wave.open('music_top10.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st * 32767).astype(np.int16).tobytes())
print('ok', dur)
