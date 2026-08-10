# Nacho Lee — Mis primeras 7 lecciones

Web app to teach early reading in Spanish, based on the first seven lessons of the
*Cartilla Nacho* sequence: **vowels → m → p → l → n → t → d**.
Designed for a 4–5 year old: huge tap targets, no reading required to navigate,
recorded Dominican Spanish voice, and a reward on every correct answer.

**Live:** https://dmaia-ai.github.io/libro-nacho/

## What's inside

Each lesson has four sections, reachable from the left sidebar:

| Section | What the child does |
|---|---|
| 🔊 Sonidos | Taps the giant letter and each syllable to hear it |
| 🖼️ Dibujos | Taps big pictures to hear the word split into syllables, plus the sentences from the book |
| 🧩 Adivinanzas | Listens to three riddles and picks the right picture |
| 🎮 Juego | One of four mini-games: listen-and-tap, which-one-starts-with, pop-the-syllable, build-the-word |

Rewards: a star counter, an on-screen celebration card with confetti and a chime on
every correct answer, a per-lesson trophy, and a trophy case in the sidebar.
Progress is stored in `localStorage`. Mistakes never lose progress.

## Audio

The voice is **not** the browser's speech synthesis — most Windows machines have no
Spanish voice installed, which is why the app used to speak English or stay silent.
Instead, 137 MP3 clips are pre-generated with [`edge-tts`](https://github.com/rany2/edge-tts)
(free, no API key) using the `es-DO-RamonaNeural` voice, and the app plays them from
a queue, chaining short fragments (`"Toca la"` + `"ma"`) to keep the clip count low.
If a clip is ever missing, it falls back to `speechSynthesis`.

## Builds

| File | Use |
|---|---|
| `index.html` | Loads `audio/*.mp3` next to it. 60 KB. This is what GitHub Pages serves. |
| `app-una-sola.html` | Every clip inlined as a `data:` URI. 3.9 MB, one file, works offline from a USB stick or as a Claude artifact. |

## Rebuilding

```bash
pip install edge-tts
python build/build.py          # only generates clips that don't exist yet
python build/build.py --forzar # re-records everything
```

Content lives in `build/contenido.json` — lessons, words, sentences and riddles.
Add a word there and the build script records its audio and rewrites both HTML files.
`build/plantilla.html` is the app itself; the build injects the content and the audio
map into the two `/*__CONTENIDO__*/` and `/*__AUDIO__*/` placeholders.

## Notes

The *Cartilla Nacho* book itself is not included in this repository — only the letter
sequence and a handful of the short practice sentences, reimplemented as an app.
