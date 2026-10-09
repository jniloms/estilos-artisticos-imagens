#!/usr/bin/env python3
"""Mantém fila-geracao.json: lista das imagens que faltam gerar e o status de cada uma.

Uso:
  python3 fila-geracao.py            # sincroniza a fila com o HTML/originais/ e mostra o resumo
  python3 fila-geracao.py proximas gemini 4   # imprime (JSON) as próximas N pendentes do modelo
  python3 fila-geracao.py marcar <id> <feito|erro|limite> [obs]

Status: pendente, feito, erro, limite. "feito" só é aceito se o arquivo existir em originais/.
O id é "<grupo>-<Estilo>-<modelo>" (mesmo padrão do nome do arquivo, sem extensão).
"""
import json, os, re, sys

PASTA = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(PASTA, "index.html")
ORIG = os.path.join(PASTA, "originais")
FILA = os.path.join(PASTA, "fila-geracao.json")
PREFIXO = {"geral": "geral", "mulher": "mulhercomflores"}
EXT = {"gpt": "png", "gemini": "jpeg"}


def estilos():
    t = open(HTML, encoding="utf-8").read()
    return json.loads(re.search(r"/\*ESTILOS:inicio\*/(.*?)/\*ESTILOS:fim\*/", t, re.S).group(1))


def existe(id_):
    pre = id_.lower() + "."
    return any(f.lower().startswith(pre) for f in os.listdir(ORIG)) if os.path.isdir(ORIG) else False


def carregar():
    return json.load(open(FILA, encoding="utf-8")) if os.path.exists(FILA) else {}


def salvar(fila):
    json.dump(fila, open(FILA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def sincronizar():
    fila = carregar()
    for e in estilos():
        for g in PREFIXO:
            for m in EXT:
                id_ = f"{PREFIXO[g]}-{e['stems'][0]}-{m}"
                it = fila.get(id_, {})
                if e[g].get(m) or existe(id_):          # já existe imagem
                    if it.get("status") != "feito":
                        it["status"] = "feito"
                else:
                    if it.get("status") == "feito":     # arquivo sumiu (ex.: prompt mudou)
                        it["status"] = "pendente"
                    it.setdefault("status", "pendente")
                it.update(estilo=e["nome"], modelo=m, arquivo=f"{id_}.{EXT[m]}", prompt=e[g]["prompt"])
                fila[id_] = it
    salvar(fila)
    return fila


def resumo(fila):
    c = {}
    for it in fila.values():
        k = (it["modelo"], it["status"]); c[k] = c.get(k, 0) + 1
    for k in sorted(c): print(f"{k[0]:7} {k[1]:9} {c[k]}")


if __name__ == "__main__":
    a = sys.argv[1:]
    fila = sincronizar()
    if not a:
        resumo(fila)
    elif a[0] == "proximas":
        n = int(a[2]) if len(a) > 2 else 4
        pend = [{"id": k, **v} for k, v in fila.items() if v["modelo"] == a[1] and v["status"] == "pendente"]
        print(json.dumps(pend[:n], ensure_ascii=False, indent=1))
    elif a[0] == "marcar":
        id_, st = a[1], a[2]
        if st == "feito" and not existe(id_):
            sys.exit(f"{id_}: arquivo não encontrado em originais/")
        fila[id_]["status"] = st
        if len(a) > 3: fila[id_]["obs"] = a[3]
        salvar(fila); print("ok")
