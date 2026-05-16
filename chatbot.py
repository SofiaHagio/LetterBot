"""Ponto de entrada do LetterBot.

Execute com:  python chatbot.py
"""

import sys

if sys.version_info < (3, 10):
    sys.exit("O LetterBot precisa do Python 3.10 ou superior.")

from letterbot.bot import LetterBot  # noqa: E402

if __name__ == "__main__":
    LetterBot().iniciar()
