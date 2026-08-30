# Nacho Lee — Aprendo a leer por sílabas

Web app to teach early reading in Spanish, following the letter sequence of the
*Cartilla Nacho*. Designed for a 4–5 year old: the syllable is the largest thing on
screen, huge tap targets, no reading required to navigate, recorded Dominican Spanish
voice, and a reward on every correct answer.

**Live:** https://dmaia-ai.github.io/libro-nacho/

## Lesson sequence

26 lessons, in the order the book teaches them:

| # | Lesson | Syllables |
|---|---|---|
| 1 | vocales | a e i o u |
| 2 | m de mamá | ma me mi mo mu |
| 3 | p de papá | pa pe pi po pu |
| 4 | s de sapo | sa si su se so |
| 5 | l de loma | la le li lo lu |
| 6 | n de nene | na ne ni no nu |
| 7 | t de tomate | ta te ti to tu |
| 8 | d de dedo | da de di do du |
| 9 | r de rosa | ra re ri ro ru |
| 10 | rr de perro | rra rre rri rro rru |
| 11 | c de casa | ca co cu |
| 12 | ñ de niña | ña ñi ñu ñe ño |
| 13 | v de vaca | va vu ve vo vi |
| 14 | b de burro | bu bo be bi ba |
| 15 | g de gato | ga go gu |
| 16 | y de yate | ya yi yo yu ye |
| 17 | f de foca | fa fi fe fu fo |
| 18 | h de hilo | hi ha hu ho he |
| 19 | j de joya | ja ju ji jo je |
| 20 | z de zorra | za zo zu |
| 21 | ll de llave | lla llu lli lle llo |
| 22 | g de guitarra | gue gui |
| 23 | c de cepillo | ce ci |
| 24 | ch de choza | cha che chi cho chu |
| 25 | q de queso | que qui |
| 26 | g de gema | ge gi |

The book's second half — inverse syllables (`al`, `es`, `an`), diphthongs (`ai`, `ue`)
and blends (`pla`, `bra`, `cri`) — is **not** covered yet. Those pages drop the
"one letter, one syllable family" shape this app is built around, so they need a
different lesson type.

The letter `c` and the letter `g` each appear in two lessons (hard and soft sound), so
audio keys for the letter clip are namespaced by lesson number, not by the letter.

## What's inside

Each lesson has four sections, reachable from the left sidebar:

| Section | What the child does |
|---|---|
| 🔊 Sonidos | Taps a syllable and watches the letter and the vowel join: `m + a = ma` |
| 🔤 Sílabas | Taps 🔊 and follows the syllables lighting up one by one, then merging into the word |
| 🧩 Adivinanzas | Listens to three riddles and picks the right picture |
| 🎮 Juego | One of four mini-games: listen-and-tap, which-one-starts-with, pop-the-syllable, build-the-word |

Rewards: a star counter, an on-screen celebration card with confetti and a chime on
every correct answer, a per-lesson trophy, and a trophy case in the sidebar.
Progress is stored in `localStorage`. Mistakes never lose progress.

## Why the syllable is the biggest thing on screen

The first version showed a huge picture, the word underneath, and the syllable
breakdown in small grey text. A child could solve every screen by naming the drawing,
without ever looking at the letters. The hierarchy is now inverted on purpose:

```
syllable  >  word  >  picture
```

The picture stays greyed out until the child has decoded the word, so it confirms the
reading instead of giving it away. Syllables light up in step with the real audio (the
highlight follows the player's `ended` event, not a timer), and at the end they slide
together and their inner borders collapse, so the word is seen being built from its
parts.

## Audio

The voice is **not** the browser's speech synthesis — most Windows machines have no
Spanish voice installed, which is why the app used to speak English or stay silent.
Instead the MP3 clips are pre-generated with [`edge-tts`](https://github.com/rany2/edge-tts)
(free, no API key) using the `es-DO-RamonaNeural` voice, and the app plays them from a
queue. If a clip is ever missing, it falls back to `speechSynthesis`.

Clip filenames are derived from a hash of the clip key, so adding a lesson does not
rename existing files and only the new clips get recorded.

## Builds

| File | Use |
|---|---|
| `index.html` | Loads `audio/*.mp3` next to it. ~90 KB. This is what GitHub Pages serves. |
| `app-una-sola.html` | Every clip inlined as a `data:` URI — one file, works offline from a USB stick. Opt-in, because with 26 lessons it is over 15 MB. |

## Rebuilding

```bash
pip install edge-tts
python build/build.py             # only records clips that don't exist yet
python build/build.py --una-sola  # also writes the big offline single file
python build/build.py --forzar    # re-records everything
```

Content lives in `build/contenido.json` — lessons, words, sentences and riddles.
Add a word there and the build script records its audio and rewrites the HTML.
`build/plantilla.html` is the app itself; the build injects the content and the audio
map into the two `/*__CONTENIDO__*/` and `/*__AUDIO__*/` placeholders.

## Notes

The *Cartilla Nacho* book itself is not included in this repository — only the letter
sequence and a handful of the short practice sentences, reimplemented as an app.
