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
2b. (Interface atual, 2026-10-09) O menu não tem mais "Criar imagem": use `gemini.google.com/images` (já em modo imagem; aguarde carregar) e o mesmo `[role=textbox]`/botão Enviar. Passe o mouse sobre a imagem para aparecer os ícones e clique no de download ("Baixar no tamanho original", canto superior direito da imagem) por coordenadas.
2b'. Depois de enviar, a conversa vira `gemini.google.com/app/<id>`. Ali o ícone de download sobre a imagem (hover, canto superior direito) baixa só com UM clique (aparece o toast "Fazendo o download no tamanho original…" e o arquivo demora a chegar; `importar-download.sh` espera até 60 s). Um segundo clique abre o editor da imagem; não repita. No editor, o download é o ícone no canto superior direito da tela (~(1352, 30) em 1568x708). Se `importar-download.sh` disser "sem arquivo", confira a data do arquivo em `~/Downloads` (não importe download antigo).
2c. Permissão do usuário nesta sessão: pode copiar as imagens baixadas pelo navegador (`~/Downloads`) e ler arquivos fora do projeto sem perguntar; o sandbox esconde `~/Downloads`, então rode `importar-download.sh` com o sandbox desativado.
3. O download precisa de clique real (`find` + `left_click` no botão); clique via JS não baixa. Os refs mudam entre cargas, então rode `find` antes de clicar.
4. `./importar-download.sh "<id>" jpeg` (o ChatGPT salva `png`).
5. Esperar ~1 min entre gerações; rodar `python3 atualizar-imagens.py` a cada 4 imagens baixadas.
5b. ChatGPT (testado em 2026-10-09, funciona): navegar para `chatgpt.com`, inserir via `execCommand('insertText')` em `div.ProseMirror[contenteditable=true]` (o id `#prompt-textarea` não existe mais; aguarde ~3 s após navegar) o texto `Generate an image: <prompt>` e clicar `button[data-testid="send-button"]` (fallback: botão com `aria-label` "Enviar"). Leva ~50-60 s (esperar com `wait`, não com JS longo: `javascript_tool` estoura em 45 s). Depois, via JS: clicar `img[alt*="gerada"]` (abre o visualizador), clicar o botão com `aria-label` "Baixar"; se aparecer menu (série de 2 imagens), clicar o item "Baixar imagem". O download JS funciona no ChatGPT. O arquivo chega como `<título da conversa>.png` (não `ChatGPT*`); o importador aceita qualquer `*.png` recente. Se o importador disser "sem arquivo", confira `~/Downloads` e o visualizador (um clique real em (770,300) e no ícone (1383,22) resolve). Se vier recusa de política ("semelhança com conteúdo de terceiros"), refaça acrescentando "original, generic ... (not based on any existing character)" (foi preciso em `geral-Quadrinhos Americanos-gpt`).
6. Se aparecer alerta de limite ou erro no Gemini: marcar o item como `limite`/`erro`, pausar e passar para o ChatGPT (ainda não testado).

## Interface da página (HTML)
- Tudo em um único arquivo: CSS, `ESTILOS` (dados + prompts originais em inglês), `I18N` (entre `/*I18N:inicio*/` e `/*I18N:fim*/`, não altere os marcadores) e o JS. `atualizar-imagens.py` e `fila-geracao.py` só leem/escrevem o bloco `ESTILOS`.
- `I18N.estilos[<stems[0]>]` = `{ en: {nome, periodo, caracteristicas, historia, tecnica, mestres?}, pt: {g, m} }`: `en` traduz os textos (campo ausente cai no pt-BR); `pt.g`/`pt.m` são os prompts em pt-BR (geral / mulher com flores). Na interface en-US os prompts são os originais de `ESTILOS`. `I18N.secoes` traduz os nomes das seções. Ao criar um estilo novo, adicione a entrada em `I18N` (senão aparece em pt-BR nos dois idiomas) e, se mudar um prompt, atualize também a versão pt-BR.
- Idioma: padrão pelo `navigator.languages` (pt* = pt-BR, senão en-US); escolha salva em `localStorage['idioma']`. Os textos da interface ficam no objeto `UI` do JS.
- Temas (`data-theme` no `<html>`, salvo em `localStorage['tema']`): classico, claro, escuro, brutalismo, vidro, synthwave, nordico, bauhaus. Cada tema é um bloco de variáveis CSS no início do `<style>`; para criar outro, adicione o bloco, um item em `TEMAS`, os nomes em `UI.pt.temas`/`UI.en.temas` e o id na regex do script do `<head>`.
- Layout: a página não rola; só `#wrap` rola. O topo (`#top`) tem o hero (título/subtítulo) que recolhe ao rolar, deixando uma barra de uma linha (busca, contagem, prompts, idioma, tema). Abaixo de 760 px os controles (prompts, idioma, tema) vão para um painel aberto pelo botão sanduíche `#burger`, e na tabela o nome do estilo fica na vertical, com o botão "ver detalhes" só como ícone (coluna do nome com 52 px). O visualizador de imagens (`#dlg`) navega pelas imagens visíveis da tabela (ou do painel de detalhes) com setas do teclado, botões e deslize.
- Para testar visualmente: `python3 -m http.server` na pasta (o Playwright bloqueia `file://`).

## Estado em 2026-10-09
- Fila concluída: Gemini 200/200 e GPT 200/200 feitas; HTML liga 400 de 400 imagens. Nenhum alerta de limite do Gemini nem do ChatGPT apareceu.
- Fluxo ChatGPT que funciona (item 5b): enviar o prompt, esperar ~60 s, recarregar a conversa (`location.reload()`, senão a imagem às vezes não renderiza), abrir a imagem via JS, tirar um screenshot pequeno, clicar o ícone de download em (1383,22), tirar outro screenshot e clicar em (1270,58) (item "Baixar imagem" do menu, quando a conversa gerou 2 imagens; inofensivo se não houver menu). Sem os screenshots entre os cliques o download às vezes não ocorre.
- `geral-Disney Classico-gpt`, `geral-Quadrinhos Americanos-gpt` e `mulhercomflores-Disney Classico-gpt` foram gerados com o prompt reescrito como "original/generic".
- `~/Downloads` tem um `Vigilante Sob a Chuva Neon.png` sobrando (download duplicado do Quadrinhos geral).
- Gemini: `mulhercomflores-Fotografia Aerea` saiu como díptico (retrato + vista aérea) e `mulhercomflores-Escultura em Marmore` como mulher ao lado de uma estátua (não busto); considere regerar com prompt mais claro.
- Os 5 estilos com fenótipo alterado (Ukiyo-e, Arte Egípcia, Arte Maia, Arte Aborígene, Pintura Chinesa) precisam ter a imagem `mulhercomflores` regerada (gpt e gemini).
