"""Tudo o que aparece na tela: cores, cartões de filme e leitura de respostas."""

import os
import sys

from .catalogo import Filme

# Ativa as cores ANSI no terminal do Windows
if os.name == "nt":
    os.system("")

_USA_COR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None

_CORES = {
    "reset": "\033[0m",
    "negrito": "\033[1m",
    "fraco": "\033[2m",
    "laranja": "\033[38;5;208m",
    "verde": "\033[38;5;71m",
    "amarelo": "\033[38;5;220m",
    "cinza": "\033[38;5;245m",
    "vermelho": "\033[38;5;167m",
}

LARGURA = 62


def cor(texto: str, *estilos: str) -> str:
    if not _USA_COR:
        return texto
    return "".join(_CORES[e] for e in estilos) + texto + _CORES["reset"]


def bot(mensagem: str) -> None:
    """Fala do LetterBot."""
    print(f"\n{cor('🎬 LetterBot', 'laranja', 'negrito')}  {mensagem}")


def aviso(mensagem: str) -> None:
    print(f"\n{cor('⚠ ' + mensagem, 'vermelho')}")


def sucesso(mensagem: str) -> None:
    print(f"\n{cor('✔ ' + mensagem, 'verde')}")


def linha() -> None:
    print(cor("─" * LARGURA, "cinza"))


def cabecalho() -> None:
    print()
    print(cor("═" * LARGURA, "laranja"))
    print(cor("  🎬  LETTERBOT".ljust(LARGURA - 1), "laranja", "negrito"))
    print(cor("  Seu assistente para escolher o filme de hoje", "cinza"))
    print(cor("═" * LARGURA, "laranja"))


def perguntar(texto: str) -> str:
    """Lê uma resposta. Ctrl+C ou Ctrl+D encerram a conversa com educação."""
    try:
        return input(f"\n{cor('›', 'laranja', 'negrito')} {texto} ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        raise SystemExit(0)


def perguntar_sim_nao(texto: str) -> bool:
    resposta = perguntar(f"{texto} {cor('(s/n)', 'cinza')}").lower()
    return resposta in {"s", "sim", "y", "yes"}


def perguntar_numero(texto: str, minimo: float, maximo: float, permitir_vazio: bool = True) -> float | None:
    """Pede um número dentro do intervalo. Enter vazio devolve None."""
    while True:
        resposta = perguntar(texto).replace(",", ".")
        if resposta == "" and permitir_vazio:
            return None
        try:
            valor = float(resposta)
        except ValueError:
            aviso("Digite só o número, por favor.")
            continue
        if minimo <= valor <= maximo:
            return valor
        aviso(f"Escolha um valor entre {minimo:g} e {maximo:g}.")
