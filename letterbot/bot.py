"""Fluxo da conversa: menu principal e cada uma das opções."""

from . import interface as ui
from . import recomendacao as rec
from .catalogo import Filme, carregar_catalogo, listar_generos
from .favoritos import Favoritos

MENU = [
    ("1", "Recomendar por gênero"),
    ("2", "Me surpreenda"),
    ("3", "Filtrar por nota e duração"),
    ("4", "Buscar por título ou direção"),
    ("5", "Top 5 do catálogo"),
    ("6", "Meus favoritos"),
    ("0", "Sair"),
]


class LetterBot:
    def __init__(self, catalogo: list[Filme] | None = None, favoritos: Favoritos | None = None):
        self.catalogo = catalogo if catalogo is not None else carregar_catalogo()
        self.generos = listar_generos(self.catalogo)
        self.favoritos = favoritos if favoritos is not None else Favoritos()
        self.sugeridos: set[str] = set()

    # ---------- conversa ----------

    def iniciar(self) -> None:
        ui.cabecalho()
        ui.bot("Oi! Eu sou o LetterBot e vou te ajudar a escolher um filme.")
        ui.bot(f"Conheço {len(self.catalogo)} filmes de {len(self.generos)} gêneros. Por onde começamos?")
        acoes = {
            "1": self.por_genero,
            "2": self.surpresa,
            "3": self.filtrar,
            "4": self.buscar,
            "5": self.top5,
            "6": self.ver_favoritos,
        }
        while True:
            self._mostrar_menu()
            opcao = ui.perguntar("Escolha uma opção:")
            if opcao == "0" or rec.normalizar(opcao) == "sair":
                ui.bot("Até a próxima! Bom filme 🍿")
                return
            acao = acoes.get(opcao)
            if acao:
                acao()
            else:
                ui.aviso("Não entendi. Digite o número de uma das opções.")

    def _mostrar_menu(self) -> None:
        print()
        ui.linha()
        for chave, texto in MENU:
            if chave == "6" and len(self.favoritos):
                texto += ui.cor(f"  ({len(self.favoritos)})", "cinza")
            print(f"  {ui.cor(chave, 'laranja', 'negrito')}  {texto}")
        ui.linha()

    # ---------- opções do menu ----------

    def por_genero(self) -> None:
        genero = self._escolher_genero()
        if genero is None:
            return
        filmes = rec.por_genero(self.catalogo, genero)
        ui.bot(f"Boa escolha! Estes são os filmes de {genero.lower()} que eu mais recomendo:")
        self._escolher_da_lista(filmes)

    def surpresa(self) -> None:
        while True:
            filme = rec.surpresa(self.catalogo, self.sugeridos)
            self.sugeridos.add(filme.titulo)
            ui.bot("Que tal este?")
            self._detalhar(filme)
            if not ui.perguntar_sim_nao("Quer outra sugestão?"):
                return

    def filtrar(self) -> None:
        ui.bot("Vamos montar um filtro. Deixe em branco o que não importar.")
        nota = ui.perguntar_numero("Nota mínima (0 a 10):", 0, 10)
        duracao = ui.perguntar_numero("Duração máxima em minutos (ex.: 120):", 60, 300)
        genero = None
        if ui.perguntar_sim_nao("Quer limitar a um gênero?"):
            genero = self._escolher_genero()
        filmes = rec.filtrar(
            self.catalogo,
            nota_minima=nota or 0,
            duracao_maxima=int(duracao) if duracao else None,
            genero=genero,
        )
        if not filmes:
            ui.bot("Nenhum filme passou nesse filtro. Tente afrouxar um pouco os critérios.")
            return
        ui.bot(f"Encontrei {len(filmes)} filme(s) com esse perfil:")
        self._escolher_da_lista(filmes)

    def buscar(self) -> None:
        termo = ui.perguntar("Digite parte do título ou o nome de quem dirigiu:")
        filmes = rec.buscar(self.catalogo, termo)
        if not filmes:
            ui.bot(f"Não achei nada com “{termo}”. Tente outra palavra.")
            return
        ui.bot(f"Achei {len(filmes)} resultado(s):")
        self._escolher_da_lista(filmes)

    def top5(self) -> None:
        ui.bot("Os 5 filmes mais bem avaliados que eu conheço:")
        self._escolher_da_lista(rec.ranking(self.catalogo))

    def ver_favoritos(self) -> None:
        filmes = [f for f in self.catalogo if self.favoritos.contem(f.titulo)]
        if not filmes:
            ui.bot("Sua lista de favoritos ainda está vazia. Quando gostar de um filme, é só salvar.")
            return
        ui.bot("Seus favoritos:")
        self._escolher_da_lista(filmes)

    # ---------- partes reaproveitadas ----------

    def _escolher_genero(self) -> str | None:
        print()
        for numero, genero in enumerate(self.generos, 1):
            print(f"  {ui.cor(str(numero), 'laranja')}. {genero}")
        while True:
            resposta = ui.perguntar("Qual gênero? (número ou nome, Enter para voltar)")
            if resposta == "":
                return None
            genero = rec.encontrar_genero(resposta, self.generos)
            if genero:
                return genero
            ui.aviso("Não conheço esse gênero. Tente o número ou o nome da lista.")

    def _escolher_da_lista(self, filmes: list[Filme]) -> None:
        ui.mostrar_lista(filmes, self.favoritos)
        while True:
            resposta = ui.perguntar("Digite o número para ver detalhes (Enter para voltar):")
            if resposta == "":
                return
            if resposta.isdigit() and 1 <= int(resposta) <= len(filmes):
                self._detalhar(filmes[int(resposta) - 1])
                ui.mostrar_lista(filmes, self.favoritos)
            else:
                ui.aviso(f"Escolha um número de 1 a {len(filmes)}.")

    def _detalhar(self, filme: Filme) -> None:
        favorito = self.favoritos.contem(filme.titulo)
        ui.cartao(filme, favorito)
        if favorito:
            if ui.perguntar_sim_nao("Tirar dos favoritos?"):
                self.favoritos.remover(filme.titulo)
                ui.sucesso("Removido dos favoritos.")
        elif ui.perguntar_sim_nao("Salvar nos favoritos?"):
            self.favoritos.adicionar(filme.titulo)
            ui.sucesso("Salvo! Veja seus favoritos na opção 6 do menu.")
