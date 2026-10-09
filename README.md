# Estilos Artísticos para Geração de Imagens

Guia com 100 estilos artísticos populares em prompts de IA generativa (Midjourney, Stable Diffusion, DALL-E, Gemini, GPT). Para cada estilo há:

- uma descrição das características visuais;
- um exemplo de prompt genérico;
- um prompt adaptado para gerar o retrato elegante de uma mulher jovem loira segurando um jarro com flores lilás, vermelhas e amarelas;
- imagens de comparação geradas pelo Gemini e pelo GPT.

## Conteúdo

| Arquivo / pasta | Descrição |
| :--- | :--- |
| `estilos-artisticos-geracao-imagens.md` | Guia em Markdown, com as tabelas de estilos e prompts. |
| `estilos-artisticos-geracao-imagens.html` | Versão em HTML com as imagens de exemplo incorporadas às tabelas. |
| `atualizar-imagens.py` | Script que atualiza as colunas de imagem do HTML a partir da pasta `img/`. |
| `originais/` | Imagens no tamanho e formato originais fornecidos pelos modelos (Gemini e GPT). |
| `img/` | Versões WebP (qualidade 95) geradas pelo script a partir de `originais/`; são as usadas na página. |

## Categorias de estilos (100 estilos)

- Pintura clássica e movimentos históricos
- Arte antiga e tradições do mundo
- Técnicas de desenho e pintura
- Animação, 3D e cultura pop
- Sci-fi, fantasia e subculturas (Cyberpunk, Steampunk, Solarpunk etc.)
- Arte digital, jogos e design gráfico
- Fotografia e efeitos de câmera
- Texturas de materiais, escultura e design físico

## Como a página é montada

Todo o conteúdo textual e os links das imagens ficam na variável `ESTILOS` (lista de objetos), dentro do próprio HTML, entre os marcadores `/*ESTILOS:inicio*/` e `/*ESTILOS:fim*/`. A tabela, o filtro, o painel de detalhes e o seletor "Mostrar prompts" são montados por JavaScript puro, sem bibliotecas externas.

Cada objeto tem: `nome`, `secao`, `stems` (nomes usados nos arquivos de imagem), `periodo`, `mestres`, `caracteristicas`, `historia`, `tecnica`, `geral` e `mulher` (cada um com `prompt`, `gpt` e `gemini`).

## Atualizando as imagens

Coloque as novas imagens em `originais/` seguindo o padrão de nomes (extensões `jpeg`, `jpg`, `png` ou `webp`; maiúsculas e minúsculas são ignoradas):

```
geral-<Estilo>-gpt.png               geral-<Estilo>-gemini.jpeg
mulhercomflores-<Estilo>-gpt.png     mulhercomflores-<Estilo>-gemini.jpeg
```

Em seguida, execute:

```bash
python3 atualizar-imagens.py
```

O script lê a variável `ESTILOS`, preenche os links `gpt` e `gemini` de cada estilo com as imagens encontradas e grava a lista de volta no HTML. Ele também avisa sobre arquivos de `img/` que não correspondem a nenhum estilo. O `<Estilo>` do nome do arquivo deve ser um dos valores de `stems` do estilo.

## Autor

Nilo Martins
