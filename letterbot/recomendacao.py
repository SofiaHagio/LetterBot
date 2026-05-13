"""Regras de busca, filtro e recomendação.

Tudo aqui é função pura: recebe o catálogo e devolve uma nova lista,
o que facilita os testes.
"""

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
