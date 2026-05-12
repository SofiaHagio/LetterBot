"""Leitura do catálogo de filmes."""

import json
from dataclasses import dataclass
from pathlib import Path

CAMINHO_CATALOGO = Path(__file__).parent / "dados" / "filmes.json"


@dataclass(frozen=True)
class Filme:
    titulo: str
    genero: str
    ano: int
    duracao: int  # em minutos
    nota: float  # de 0 a 10
    direcao: str
    sinopse: str

    @property
    def duracao_formatada(self) -> str:
        horas, minutos = divmod(self.duracao, 60)
        return f"{horas}h{minutos:02d}" if horas else f"{minutos} min"


def carregar_catalogo(caminho: Path = CAMINHO_CATALOGO) -> list[Filme]:
    """Lê o arquivo JSON e devolve a lista de filmes."""
    with open(caminho, encoding="utf-8") as arquivo:
        return [Filme(**dados) for dados in json.load(arquivo)]


def listar_generos(catalogo: list[Filme]) -> list[str]:
    """Devolve os gêneros na ordem em que aparecem no catálogo, sem repetir."""
    generos: list[str] = []
    for filme in catalogo:
        if filme.genero not in generos:
            generos.append(filme.genero)
    return generos
