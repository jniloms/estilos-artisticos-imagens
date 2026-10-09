# Estilos artísticos – geração de imagens

Página HTML (`estilos-artisticos-geracao-imagens.html`) com 100 estilos artísticos, cada um com 4 imagens: `geral` e `mulhercomflores` × `gpt` e `gemini`. Os dados ficam na variável `ESTILOS` entre `/*ESTILOS:inicio*/` e `/*ESTILOS:fim*/` (não altere os marcadores).

## Pastas e scripts
- `originais/`: imagens no formato/tamanho originais (Gemini = `.jpeg`, GPT = `.png`). Nome: `<geral|mulhercomflores>-<Estilo>-<gpt|gemini>.<ext>`, onde `<Estilo>` é o primeiro item de `stems` do estilo (sem acento, ex.: `Geometria Islamica`).
- `img/`: WebP (qualidade 95, máx. 1080 px por lado) gerado a partir de `originais/`. É o que a página mostra; o botão "baixar original" aponta para `originais/`.
- `atualizar-imagens.py`: converte novidades de `originais/` para `img/` e atualiza os links no HTML. Só reconverte o que é novo/alterado (apague o `.webp` para forçar). Aceita variações do nome do estilo (partes separadas por " – ", " / " ou texto entre parênteses). Requer Pillow com WebP.
- `fila-geracao.py` + `fila-geracao.json`: fila do que falta gerar (status `pendente|feito|erro|limite`). Comandos:
  - `python3 fila-geracao.py` (sincroniza e mostra o resumo)
  - `python3 fila-geracao.py proximas <gemini|gpt> <N>` (lista as próximas N com o prompt)
  - `python3 fila-geracao.py marcar <id> <status>` (`feito` só se o arquivo existir em `originais/`)
- `importar-download.sh <id> <ext>`: move o download mais recente (últimos 3 min, em `~/Downloads`, `Gemini_Generated_Image_*` ou `ChatGPT*`) para `originais/<id>.<ext>` e marca `feito`.

## Regras do conteúdo
- Prompts "mulher com flores": fenótipo coerente com o estilo (japonesa no Ukiyo-e, egípcia, maia, aborígene, chinesa etc.). Estilos europeus/genéricos antigos mantêm a loira. Se um prompt mudar, apague o `.webp` e mova o original para uma pasta `old/` (fora do script) até regerar a imagem.

## Geração automática no navegador (em andamento)
Fluxo usado com a extensão Claude in Chrome (precisa de `claude --chrome`; Chrome logado no Gemini/ChatGPT; "Perguntar onde salvar" desligado em `chrome://settings/downloads`):
1. Pegar prompts com `fila-geracao.py proximas gemini 4`.
2. No Gemini (`gemini.google.com/app`), via `javascript_tool`: clicar em `button[aria-label="Envio e ferramentas"]`, no item "Criar imagem", focar o `[role=textbox]`, `document.execCommand('insertText', …)`, clicar no botão `aria-label*="Enviar"` e aguardar o botão "Baixar imagem no tamanho original".
3. O download precisa de clique real (`find` + `left_click` no botão); clique via JS não baixa. Os refs mudam entre cargas, então rode `find` antes de clicar.
4. `./importar-download.sh "<id>" jpeg` (o ChatGPT salva `png`).
5. Esperar ~1 min entre gerações; rodar `python3 atualizar-imagens.py` a cada 4 imagens baixadas.
6. Se aparecer alerta de limite ou erro no Gemini: marcar o item como `limite`/`erro`, pausar e passar para o ChatGPT (ainda não testado).

## Estado em 2026-10-09
- Fila: Gemini 141 feitas / 59 pendentes; GPT 122 feitas / 78 pendentes (HTML liga 263 de 400 imagens).
- Nenhum alerta de limite do Gemini apareceu até aqui.
- Próxima pendente do Gemini: `mulhercomflores-Gravura em Metal-gemini` (gerar com `proximas gemini 4`). O ChatGPT ainda não foi testado.
- Os 5 estilos com fenótipo alterado (Ukiyo-e, Arte Egípcia, Arte Maia, Arte Aborígene, Pintura Chinesa) precisam ter a imagem `mulhercomflores` regerada (gpt e gemini).
