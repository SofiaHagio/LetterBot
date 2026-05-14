"""Regras de busca, filtro e recomendação.

Tudo aqui é função pura: recebe o catálogo e devolve uma nova lista,
o que facilita os testes.
"""

import random
import unicodedata

from .catalogo import Filme


def normalizar(texto: str) -> str:
    """Deixa o texto em minúsculas e sem acentos, para comparar entradas.

    Exemplo: "  Ação " vira "acao".
    """
    sem_acento = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return sem_acento.lower().strip()


def encontrar_genero(entrada: str, generos: list[str]) -> str | None:
    """Aceita o número do gênero na lista ou o nome, com ou sem acento."""
    entrada = normalizar(entrada)
    if entrada.isdigit():
        indice = int(entrada) - 1
        return generos[indice] if 0 <= indice < len(generos) else None
    for genero in generos:
        nome = normalizar(genero)
        if entrada == nome or (len(entrada) >= 3 and nome.startswith(entrada)):
            return genero
    return None


def por_genero(catalogo: list[Filme], genero: str) -> list[Filme]:
    """Filmes de um gênero, do mais bem avaliado para o menos."""
    return ordenar_por_nota([f for f in catalogo if f.genero == genero])


def ordenar_por_nota(filmes: list[Filme]) -> list[Filme]:
    return sorted(filmes, key=lambda f: (-f.nota, f.titulo))


def filtrar(
    catalogo: list[Filme],
    nota_minima: float = 0,
    duracao_maxima: int | None = None,
    genero: str | None = None,
) -> list[Filme]:
    """Aplica os filtros informados. Filtro vazio não restringe nada."""
    resultado = [
        f
        for f in catalogo
        if f.nota >= nota_minima
        and (duracao_maxima is None or f.duracao <= duracao_maxima)
        and (genero is None or f.genero == genero)
    ]
    return ordenar_por_nota(resultado)


def buscar(catalogo: list[Filme], termo: str) -> list[Filme]:
    """Busca por parte do título ou da direção, ignorando acentos."""
    termo = normalizar(termo)
    if not termo:
        return []
    return ordenar_por_nota(
        [f for f in catalogo if termo in normalizar(f.titulo) or termo in normalizar(f.direcao)]
    )


def ranking(catalogo: list[Filme], quantidade: int = 5) -> list[Filme]:
    """Os filmes mais bem avaliados do catálogo."""
    return ordenar_por_nota(catalogo)[:quantidade]


def surpresa(catalogo: list[Filme], ja_vistos: set[str] | None = None, sorteio=random) -> Filme:
    """Sorteia um filme, evitando os que já foram sugeridos na sessão.

    Quando todos já saíram, volta a sortear entre o catálogo inteiro.
    """
    ja_vistos = ja_vistos or set()
    opcoes = [f for f in catalogo if f.titulo not in ja_vistos] or catalogo
    return sorteio.choice(opcoes)
