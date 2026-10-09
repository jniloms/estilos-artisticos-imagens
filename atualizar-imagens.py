#!/usr/bin/env python3
"""Atualiza os links de imagem de estilos-artisticos-geracao-imagens.html
com base nos arquivos encontrados na subpasta img/.

Os dados da página ficam na variável ESTILOS (lista de objetos), entre os
marcadores /*ESTILOS:inicio*/ e /*ESTILOS:fim*/. Este script lê essa lista,
preenche os campos gpt/gemini de cada estilo e grava a lista de volta.

Nomes esperados (extensões: jpeg, jpg, png, webp; maiúsculas/minúsculas ignoradas):
  geral-<Estilo>-gpt.png            geral-<Estilo>-gemini.jpeg
  mulhercomflores-<Estilo>-gpt.png  mulhercomflores-<Estilo>-gemini.jpeg

<Estilo> é um dos nomes listados em "stems" no objeto do estilo (ex.: "Anime").
"""
import json, os, re, sys

PASTA = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(PASTA, "img")
ARQ = os.path.join(PASTA, "estilos-artisticos-geracao-imagens.html")
PREFIXO = {"geral": "geral", "mulher": "mulhercomflores"}
MODELOS = ("gpt", "gemini")
EXTS = ("jpeg", "jpg", "png", "webp")
MARCADORES = re.compile(r"(/\*ESTILOS:inicio\*/)(.*?)(/\*ESTILOS:fim\*/)", re.S)

os.makedirs(IMG, exist_ok=True)
arquivos = {f.lower(): f for f in os.listdir(IMG)}
usados = set()


def achar(stems, grupo, modelo):
    for s in stems:
        for e in EXTS:
            f = arquivos.get(f"{PREFIXO[grupo]}-{s}-{modelo}.{e}".lower())
            if f:
                usados.add(f)
                return "img/" + f
    return None


pagina = open(ARQ, encoding="utf-8").read()
m = MARCADORES.search(pagina)
if not m:
    sys.exit("Marcadores /*ESTILOS:inicio*/ e /*ESTILOS:fim*/ não encontrados no HTML.")
estilos = json.loads(m.group(2))

achadas = total = 0
for est in estilos:
    for grupo in PREFIXO:
        for modelo in MODELOS:
            caminho = achar(est["stems"], grupo, modelo)
            est[grupo][modelo] = caminho
            total += 1
            achadas += bool(caminho)

# "</" é escapado para que o JSON nunca encerre o bloco <script>.
dados = json.dumps(estilos, ensure_ascii=False, indent=1).replace("</", "<\\/")
nova = pagina[:m.start(2)] + dados + pagina[m.end(2):]
open(ARQ, "w", encoding="utf-8").write(nova)

print(f"{achadas} de {total} imagens ligadas ({len(estilos)} estilos).")
sobras = sorted(f for f in arquivos.values() if f not in usados)
if sobras:
    print(f"{len(sobras)} arquivo(s) em img/ sem estilo correspondente (confira o nome):")
    for f in sobras:
        print("  -", f)
