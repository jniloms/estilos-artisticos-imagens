#!/bin/bash
# uso: importar.sh <id> <ext>  -> move o download mais recente do Downloads para originais/
cd "$(dirname "$0")"
for t in $(seq 1 30); do f=$(find "$HOME/Downloads" -maxdepth 1 -type f \( -name "Gemini_Generated_Image_*" -o -name "ChatGPT*" -o -name "*.png" \) -mmin -3 -printf "%T@ %p\n" | sort -n | tail -1 | cut -d" " -f2-); [ -n "$f" ] && break; sleep 2; done
[ -z "$f" ] && { echo "sem arquivo"; exit 1; }
mv "$f" "originais/$1.$2" && python3 fila-geracao.py marcar "$1" feito
