#!/usr/bin/env python3
"""Converte as imagens de originais/ para WebP (qualidade 95, no máximo 1080 px por lado, mantendo a proporção) em img/ e atualiza
os links de imagem de estilos-artisticos-geracao-imagens.html para as versões WebP.

Só reconverte arquivos novos ou alterados (compara datas de modificação).
Requer Pillow com suporte a WebP (pip install pillow).

Os dados da página ficam na variável ESTILOS (lista de objetos), entre os
marcadores /*ESTILOS:inicio*/ e /*ESTILOS:fim*/. Este script lê essa lista,
preenche os campos gpt/gemini de cada estilo e grava a lista de volta.

Nomes esperados (extensões: jpeg, jpg, png, webp; maiúsculas/minúsculas ignoradas):
  geral-<Estilo>-gpt.png            geral-<Estilo>-gemini.jpeg
  mulhercomflores-<Estilo>-gpt.png  mulhercomflores-<Estilo>-gemini.jpeg

Os nomes valem para a pasta originais/; em img/ o arquivo gerado tem a extensão .webp.
<Estilo> pode ser qualquer um dos "stems" do estilo, o nome completo ou, se o nome tiver
partes separadas por travessão (–) ou barra (/), ou algo entre parênteses, qualquer uma
dessas partes (ex.: "Aquarela (Watercolor)" aceita "Aquarela" e "Watercolor").
"""
import json, os, re, sys
from PIL import Image

PASTA = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(PASTA, "originais")
IMG = os.path.join(PASTA, "img")
QUALIDADE = 95
LADO_MAX = 1080
ARQ = os.path.join(PASTA, "estilos-artisticos-geracao-imagens.html")
PREFIXO = {"geral": "geral", "mulher": "mulhercomflores"}
MODELOS = ("gpt", "gemini")
EXTS = ("jpeg", "jpg", "png", "webp")
MARCADORES = re.compile(r"(/\*ESTILOS:inicio\*/)(.*?)(/\*ESTILOS:fim\*/)", re.S)

os.makedirs(IMG, exist_ok=True)
arquivos = {f.lower(): f for f in os.listdir(ORIG)}
usados = set()
convertidas = 0


def converter(f):
    """Gera img/<nome>.webp a partir de originais/<f>, se estiver ausente ou desatualizado."""
    global convertidas
    destino = os.path.splitext(f)[0] + ".webp"
    origem_p, destino_p = os.path.join(ORIG, f), os.path.join(IMG, destino)
    if not os.path.exists(destino_p) or os.path.getmtime(destino_p) < os.path.getmtime(origem_p):
        with Image.open(origem_p) as im:
            im.thumbnail((LADO_MAX, LADO_MAX), Image.LANCZOS)  # só reduz, mantém a proporção
            im.save(destino_p, "WEBP", quality=QUALIDADE, method=6)
        convertidas += 1
    return destino


def original(f):
    return "originais/" + f


def variantes(est):
    """Nomes aceitos nos arquivos: os "stems" e o nome do estilo, e cada parte deles.

    Divide em " – " / " — " / " / " (travessão ou barra com espaços; hífens dentro
    de palavras, como em Ukiyo-e, não dividem) e, para "Texto (Outro)", aceita
    "Texto" e "Outro" separadamente.
    """
    saida = []

    def add(c):
        c = " ".join(c.split())
        if c and c not in saida:
            saida.append(c)

    for base in [*est["stems"], est["nome"]]:
        add(base)
        dentro = re.findall(r"\(([^)]*)\)", base)
        fora = re.sub(r"\([^)]*\)", " ", base)
        for trecho in (fora, *dentro):
            add(trecho)
            for parte in re.split(r"\s+[–—/]\s+", trecho.strip()):
                add(parte)
    return saida


def achar(stems, grupo, modelo):
    """Devolve (caminho do WebP em img/, caminho do arquivo em originais/) ou (None, None)."""
    for s in stems:
        for e in EXTS:
            f = arquivos.get(f"{PREFIXO[grupo]}-{s}-{modelo}.{e}".lower())
            if f:
                usados.add(f)
                return "img/" + converter(f), original(f)
    return None, None


pagina = open(ARQ, encoding="utf-8").read()
m = MARCADORES.search(pagina)
if not m:
    sys.exit("Marcadores /*ESTILOS:inicio*/ e /*ESTILOS:fim*/ não encontrados no HTML.")
estilos = json.loads(m.group(2))

achadas = total = 0
for est in estilos:
    for grupo in PREFIXO:
        for modelo in MODELOS:
            caminho, orig = achar(variantes(est), grupo, modelo)
            est[grupo][modelo] = caminho
            est[grupo][modelo + "_original"] = orig
            total += 1
            achadas += bool(caminho)

# "</" é escapado para que o JSON nunca encerre o bloco <script>.
dados = json.dumps(estilos, ensure_ascii=False, indent=1).replace("</", "<\\/")
nova = pagina[:m.start(2)] + dados + pagina[m.end(2):]
open(ARQ, "w", encoding="utf-8").write(nova)

print(f"{convertidas} imagem(ns) convertida(s) para WebP.")
print(f"{achadas} de {total} imagens ligadas ({len(estilos)} estilos).")
sobras = sorted(f for f in arquivos.values() if f not in usados)
if sobras:
    print(f"{len(sobras)} arquivo(s) em originais/ sem estilo correspondente (confira o nome):")
    for f in sobras:
        print("  -", f)
