#!/usr/bin/env python3
"""Atualiza as colunas de imagem de estilos-artisticos-geracao-imagens.html
com base nos arquivos encontrados na subpasta img/.

Nomes esperados (extensões: jpeg, jpg, png, webp; maiúsculas/minúsculas ignoradas):
  geral-<Estilo>-gpt.png            geral-<Estilo>-gemini.jpeg
  mulhercomflores-<Estilo>-gpt.png  mulhercomflores-<Estilo>-gemini.jpeg
"""
import html, os, re, sys, urllib.parse

PASTA = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(PASTA, "img")
ARQ = os.path.join(PASTA, "estilos-artisticos-geracao-imagens.html")
PREFIXO = {"geral": "geral", "mulher": "mulhercomflores"}
EXTS = ("jpeg", "jpg", "png", "webp")

os.makedirs(IMG, exist_ok=True)
arquivos = {f.lower(): f for f in os.listdir(IMG)}

def achar(stems, slot):
    tipo, tag = slot.split("-")
    for s in stems:
        for e in EXTS:
            f = arquivos.get(f"{PREFIXO[tipo]}-{s}-{tag}.{e}".lower())
            if f:
                return f
    return None

def celula(f, alt, slot):
    if not f:
        return f'<td class="img empty" data-slot="{slot}"></td>'
    u = "img/" + urllib.parse.quote(f)
    a = html.escape(alt)
    return (f'<td class="img" data-slot="{slot}"><button class="thumb" data-full="{u}" '
            f'data-cap="{a}"><img loading="lazy" src="{u}" alt="{a}"></button></td>')

pagina = open(ARQ, encoding="utf-8").read()
achadas = total = 0

def linha(m):
    global achadas, total
    stems = html.unescape(m.group(1)).split("|")
    nome = html.unescape(m.group(2))
    def td(mt):
        global achadas, total
        slot = mt.group(1)
        f = achar(stems, slot)
        total += 1
        achadas += bool(f)
        tipo, tag = slot.split("-")
        return celula(f, f"{nome} – {tipo} – {tag}", slot)
    return re.sub(r'<td class="img(?: empty)?" data-slot="([^"]+)"(?:></td>|>.*?</button></td>)', td, m.group(0), flags=re.S)

novo = re.sub(r'<tr data-stems="([^"]*)" data-name="([^"]*)".*?</tr>', linha, pagina, flags=re.S)
open(ARQ, "w", encoding="utf-8").write(novo)
print(f"{achadas} de {total} células de imagem preenchidas.")
