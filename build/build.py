"""
Build script for the Nacho reading app.

Generates one MP3 per spoken phrase with edge-tts (Dominican Spanish voice,
free, no API key) and renders two self-contained builds:

  index.html         -> loads audio/*.mp3 next to it (small, for GitHub Pages)
  app-una-sola.html  -> every clip inlined as a data: URI (single file, offline)

Run:  python build/build.py
"""

import asyncio
import base64
import json
import os
import re
import sys

import edge_tts

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(RAIZ, "build")
AUDIO = os.path.join(RAIZ, "audio")


def cargar_contenido():
    with open(os.path.join(BUILD, "contenido.json"), encoding="utf-8") as f:
        return json.load(f)


def silabas_habladas(s):
    """'ma-má' -> 'ma, má'"""
    return ", ".join(s.split("-"))


def recolectar(contenido):
    """clave -> texto que se va a pronunciar (orden estable)."""
    clips = {}

    for frag in contenido["fragmentos"]:
        clips["f:" + frag] = frag

    for L in contenido["lecciones"]:
        if L.get("vocales"):
            for v in L["vocales"]:
                clips["v:" + v["l"]] = "%s... %s, de %s." % (v["l"], v["l"], v["w"])
                clips["s:" + v["l"]] = v["l"]
        if L.get("silabas"):
            clips["L:" + L["letra"]] = "%s... %s." % (
                L["letra"],
                ", ".join(L["silabas"]),
            )
            for s in L["silabas"]:
                clips["s:" + s] = s
        for p in L["palabras"]:
            clips["p:" + p["w"]] = "%s... %s." % (silabas_habladas(p["s"]), p["w"])
        for o in L.get("frases", []):
            clips["o:" + o] = o
        for a in L.get("adivinanzas", []):
            clips["a:" + a["texto"]] = a["texto"]

    return clips


def nombre_archivo(clave, i):
    limpio = re.sub(r"[^a-z0-9]+", "-", clave.lower())[:34].strip("-")
    return "%03d-%s.mp3" % (i, limpio or "clip")


async def sintetizar(texto, destino, voz, velocidad):
    com = edge_tts.Communicate(texto, voz, rate=velocidad)
    await com.save(destino)


async def generar(clips, voz, velocidad, forzar=False):
    manifiesto = {}
    total = len(clips)
    for i, (clave, texto) in enumerate(sorted(clips.items()), 1):
        archivo = nombre_archivo(clave, i)
        destino = os.path.join(AUDIO, archivo)
        manifiesto[clave] = archivo
        if os.path.exists(destino) and not forzar and os.path.getsize(destino) > 0:
            continue
        for intento in range(3):
            try:
                await sintetizar(texto, destino, voz, velocidad)
                break
            except Exception as err:  # red intermitente
                if intento == 2:
                    raise
                await asyncio.sleep(1.5)
        print("  [%3d/%3d] %s" % (i, total, archivo))
    return manifiesto


def render(contenido, manifiesto, inline):
    with open(os.path.join(BUILD, "plantilla.html"), encoding="utf-8") as f:
        plantilla = f.read()

    if inline:
        mapa = {}
        for clave, archivo in manifiesto.items():
            with open(os.path.join(AUDIO, archivo), "rb") as f:
                mapa[clave] = "data:audio/mpeg;base64," + base64.b64encode(
                    f.read()
                ).decode("ascii")
    else:
        mapa = {c: "audio/" + a for c, a in manifiesto.items()}

    salida = plantilla.replace(
        "/*__CONTENIDO__*/null", json.dumps(contenido, ensure_ascii=False)
    ).replace("/*__AUDIO__*/null", json.dumps(mapa, ensure_ascii=False))
    return salida


def main():
    contenido = cargar_contenido()
    clips = recolectar(contenido)
    os.makedirs(AUDIO, exist_ok=True)

    print("Generando %d clips con %s ..." % (len(clips), contenido["voz"]))
    manifiesto = asyncio.run(
        generar(clips, contenido["voz"], contenido["velocidad"], "--forzar" in sys.argv)
    )

    with open(os.path.join(AUDIO, "manifiesto.json"), "w", encoding="utf-8") as f:
        json.dump(manifiesto, f, ensure_ascii=False, indent=1)

    for nombre, inline in (("index.html", False), ("app-una-sola.html", True)):
        html = render(contenido, manifiesto, inline)
        with open(os.path.join(RAIZ, nombre), "w", encoding="utf-8") as f:
            f.write(html)
        print("%s -> %.2f MB" % (nombre, len(html.encode("utf-8")) / 1048576))


if __name__ == "__main__":
    main()
