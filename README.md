# Estilos Artísticos para Geração de Imagens

Guia com 50 estilos artísticos populares em prompts de IA generativa (Midjourney, Stable Diffusion, DALL-E, Gemini, GPT). Para cada estilo há:

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
| `img/` | Imagens geradas pelos modelos (Gemini e GPT) para cada estilo. |

## Categorias de estilos

- Pintura clássica e movimentos históricos
- Sci-fi, fantasia e subculturas (Cyberpunk, Steampunk, Solarpunk etc.)
- Arte digital, jogos e ilustração moderna

## Atualizando as imagens

Coloque as novas imagens em `img/` seguindo o padrão de nomes (extensões `jpeg`, `jpg`, `png` ou `webp`; maiúsculas e minúsculas são ignoradas):

```
geral-<Estilo>-gpt.png               geral-<Estilo>-gemini.jpeg
mulhercomflores-<Estilo>-gpt.png     mulhercomflores-<Estilo>-gemini.jpeg
```

Em seguida, execute:

```bash
python3 atualizar-imagens.py
```

O script atualiza o HTML com as imagens encontradas.

## Autor

Nilo Martins
