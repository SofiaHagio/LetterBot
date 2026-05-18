<div align="center">

# 🎬 LetterBot

**Um chatbot de terminal que ajuda você a escolher o filme de hoje**

Recomendações por gênero, sugestão surpresa, filtros por nota e duração, busca e uma lista de favoritos que fica salva entre uma conversa e outra. Tudo em Python puro, sem instalar nada.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Sem dependências](https://img.shields.io/badge/depend%C3%AAncias-nenhuma-2E7D32?style=flat-square)
![Testes](https://img.shields.io/badge/testes-unittest-F7A41D?style=flat-square)

<sub>Computational Thinking with Python · FIAP · Engenharia de Software</sub>

</div>

---

## Sobre o projeto

Escolher um filme costuma levar mais tempo do que assistir a ele. O LetterBot resolve isso numa conversa curta pelo terminal: você diz o que está com vontade de ver e ele sugere, explica e guarda os que você gostou.

O catálogo tem **35 filmes em 7 gêneros** (ação, comédia, terror, drama, ficção científica, animação e romance), cada um com ano, duração, direção, nota e sinopse.

---

## Funcionalidades

| Opção | O que faz |
|---|---|
| **Recomendar por gênero** | Lista os filmes do gênero, do mais bem avaliado para o menos |
| **Me surpreenda** | Sorteia um filme, sem repetir os que já saíram na conversa |
| **Filtrar** | Combina nota mínima, duração máxima e gênero |
| **Buscar** | Procura por parte do título ou pelo nome de quem dirigiu |
| **Top 5** | Os filmes mais bem avaliados do catálogo |
| **Favoritos** | Salva e remove filmes de uma lista que continua lá quando você abre o bot de novo |

Detalhes que deixam a conversa mais natural:

- **Entende o que você digita:** aceita o número ou o nome do gênero, com ou sem acento (`acao`, `Ação` e `1` funcionam igual) e até só o começo da palavra (`ficcao`).
- **Ficha de cada filme** com ano, duração, direção, estrelas e sinopse.
- **Interface colorida** no terminal, que também funciona no Windows.
- **Não quebra:** entradas inválidas geram uma mensagem amigável, e `Ctrl + C` encerra sem erro.

---

## Demonstração

```
══════════════════════════════════════════════════════════════
  🎬  LETTERBOT
  Seu assistente para escolher o filme de hoje
══════════════════════════════════════════════════════════════

🎬 LetterBot  Oi! Eu sou o LetterBot e vou te ajudar a escolher um filme.
🎬 LetterBot  Conheço 35 filmes de 7 gêneros. Por onde começamos?

  1  Recomendar por gênero
  2  Me surpreenda
  3  Filtrar por nota e duração
  4  Buscar por título ou direção
  5  Top 5 do catálogo
  6  Meus favoritos
  0  Sair

› Escolha uma opção: 4
› Digite parte do título ou o nome de quem dirigiu: nolan

🎬 LetterBot  Achei 2 resultado(s):

   1. A Origem
      8.8  2010 · 2h28 · Ficção científica
   2. Interestelar
      8.7  2014 · 2h49 · Ficção científica

› Digite o número para ver detalhes (Enter para voltar): 2
──────────────────────────────────────────────────────────────
  Interestelar
  Ficção científica · 2014 · 2h49 · direção de Christopher Nolan
  ★★★★☆  8.7/10

  Com a Terra morrendo, um grupo de astronautas atravessa um
  buraco de minhoca em busca de um novo lar.
──────────────────────────────────────────────────────────────

› Salvar nos favoritos? (s/n) s
✔ Salvo! Veja seus favoritos na opção 6 do menu.
```

---

## Como executar

Requer **Python 3.10 ou superior**. Não há dependências externas.

```bash
git clone https://github.com/SofiaHagio/LetterBot.git
cd LetterBot
python chatbot.py
```

Para rodar os testes:

```bash
python -m unittest -v
```

> Os favoritos ficam salvos em `~/.letterbot/favoritos.json`, na pasta do seu usuário.

---

## Como o código está organizado

```
LetterBot/
├── chatbot.py              # Ponto de entrada
├── letterbot/
│   ├── bot.py              # Fluxo da conversa e opções do menu
│   ├── interface.py        # Cores, ficha do filme e leitura das respostas
│   ├── recomendacao.py     # Busca, filtros, ranking e sorteio
│   ├── favoritos.py        # Lista de favoritos salva em JSON
│   ├── catalogo.py         # Leitura do catálogo
│   └── dados/
│       └── filmes.json     # Os 35 filmes
└── tests/
    └── test_letterbot.py   # 20 testes automatizados
```

- **Separação de responsabilidades:** o que aparece na tela (`interface.py`), as regras (`recomendacao.py`) e os dados (`filmes.json`) ficam em arquivos diferentes.
- **Regras testáveis:** as funções de recomendação não leem nem escrevem nada, só recebem uma lista e devolvem outra. Por isso são fáceis de testar.
- **Catálogo fácil de ampliar:** para adicionar um filme, basta incluir mais um item no `filmes.json`.

---

## Equipe

| Nome | RM |
|---|---|
| Guilherme Tomé Nogueira | 570144 |
| Lucas de Andrade Astorini | 569119 |
| Sabrina Lopes da Silva | 571870 |
| Sofia Satomi Hagio | 569120 |
