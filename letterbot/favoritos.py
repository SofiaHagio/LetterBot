"""Lista de favoritos, salva em um arquivo JSON para não se perder ao fechar o bot."""

import json
from pathlib import Path

CAMINHO_PADRAO = Path.home() / ".letterbot" / "favoritos.json"


class Favoritos:
    def __init__(self, caminho: Path = CAMINHO_PADRAO):
        self.caminho = Path(caminho)
        self.titulos: list[str] = self._ler()

    def _ler(self) -> list[str]:
        try:
            with open(self.caminho, encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            return [t for t in dados if isinstance(t, str)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _salvar(self) -> None:
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with open(self.caminho, "w", encoding="utf-8") as arquivo:
            json.dump(self.titulos, arquivo, ensure_ascii=False, indent=2)

    def contem(self, titulo: str) -> bool:
        return titulo in self.titulos

    def adicionar(self, titulo: str) -> bool:
        """Adiciona o filme. Devolve False se ele já estava na lista."""
        if self.contem(titulo):
            return False
        self.titulos.append(titulo)
        self._salvar()
        return True

    def remover(self, titulo: str) -> bool:
        """Remove o filme. Devolve False se ele não estava na lista."""
        if not self.contem(titulo):
            return False
        self.titulos.remove(titulo)
        self._salvar()
        return True

    def __len__(self) -> int:
        return len(self.titulos)
