import random
import tempfile
import unittest
from pathlib import Path

from letterbot import recomendacao as rec
from letterbot.catalogo import Filme, carregar_catalogo, listar_generos
from letterbot.favoritos import Favoritos


def filme(titulo, genero="Drama", nota=7.0, duracao=100, direcao="Fulana"):
    return Filme(titulo, genero, 2000, duracao, nota, direcao, "Sinopse.")


class TestCatalogo(unittest.TestCase):
    def test_catalogo_carrega_e_tem_campos_validos(self):
        catalogo = carregar_catalogo()
        self.assertGreaterEqual(len(catalogo), 30)
        for f in catalogo:
            self.assertTrue(0 <= f.nota <= 10, f.titulo)
            self.assertGreater(f.duracao, 0, f.titulo)
            self.assertTrue(f.sinopse, f.titulo)

    def test_titulos_nao_se_repetem(self):
        titulos = [f.titulo for f in carregar_catalogo()]
        self.assertEqual(len(titulos), len(set(titulos)))

    def test_generos_sem_repeticao_e_na_ordem(self):
        catalogo = [filme("A", "Ação"), filme("B", "Drama"), filme("C", "Ação")]
        self.assertEqual(listar_generos(catalogo), ["Ação", "Drama"])

    def test_duracao_formatada(self):
        self.assertEqual(filme("A", duracao=125).duracao_formatada, "2h05")
        self.assertEqual(filme("B", duracao=45).duracao_formatada, "45 min")


class TestRecomendacao(unittest.TestCase):
    def setUp(self):
        self.catalogo = [
            filme("Ação Boa", "Ação", 8.5, 140),
            filme("Ação Média", "Ação", 7.0, 95),
            filme("Drama Curto", "Drama", 8.0, 90, "Christopher Nolan"),
            filme("Ficção Longa", "Ficção científica", 9.0, 170),
        ]
        self.generos = listar_generos(self.catalogo)

    def test_normalizar_tira_acento_espaco_e_maiuscula(self):
        self.assertEqual(rec.normalizar("  AÇÃO "), "acao")

    def test_encontrar_genero_por_nome_sem_acento(self):
        self.assertEqual(rec.encontrar_genero("acao", self.generos), "Ação")

    def test_encontrar_genero_por_inicio_do_nome(self):
        self.assertEqual(rec.encontrar_genero("ficcao", self.generos), "Ficção científica")

    def test_encontrar_genero_por_numero(self):
        self.assertEqual(rec.encontrar_genero("2", self.generos), "Drama")

    def test_encontrar_genero_invalido(self):
        self.assertIsNone(rec.encontrar_genero("99", self.generos))
        self.assertIsNone(rec.encontrar_genero("faroeste", self.generos))
        self.assertIsNone(rec.encontrar_genero("a", self.generos))

    def test_por_genero_ordena_pela_nota(self):
        titulos = [f.titulo for f in rec.por_genero(self.catalogo, "Ação")]
        self.assertEqual(titulos, ["Ação Boa", "Ação Média"])

    def test_filtrar_por_nota_e_duracao(self):
        resultado = rec.filtrar(self.catalogo, nota_minima=8, duracao_maxima=150)
        self.assertEqual([f.titulo for f in resultado], ["Ação Boa", "Drama Curto"])

    def test_filtro_vazio_devolve_tudo(self):
        self.assertEqual(len(rec.filtrar(self.catalogo)), len(self.catalogo))

    def test_buscar_por_titulo_e_direcao(self):
        self.assertEqual([f.titulo for f in rec.buscar(self.catalogo, "longa")], ["Ficção Longa"])
        self.assertEqual([f.titulo for f in rec.buscar(self.catalogo, "nolan")], ["Drama Curto"])
        self.assertEqual(rec.buscar(self.catalogo, "   "), [])

    def test_ranking(self):
        self.assertEqual([f.titulo for f in rec.ranking(self.catalogo, 2)], ["Ficção Longa", "Ação Boa"])

    def test_surpresa_evita_filmes_ja_sugeridos(self):
        vistos = {"Ação Boa", "Ação Média", "Drama Curto"}
        sorteado = rec.surpresa(self.catalogo, vistos, random.Random(1))
        self.assertEqual(sorteado.titulo, "Ficção Longa")

    def test_surpresa_recomeca_quando_todos_ja_sairam(self):
        vistos = {f.titulo for f in self.catalogo}
        self.assertIn(rec.surpresa(self.catalogo, vistos), self.catalogo)


class TestFavoritos(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.caminho = Path(self.pasta.name) / "favoritos.json"

    def tearDown(self):
        self.pasta.cleanup()

    def test_adicionar_salva_e_persiste(self):
        Favoritos(self.caminho).adicionar("Matrix")
        self.assertTrue(Favoritos(self.caminho).contem("Matrix"))

    def test_nao_duplica(self):
        favoritos = Favoritos(self.caminho)
        self.assertTrue(favoritos.adicionar("Matrix"))
        self.assertFalse(favoritos.adicionar("Matrix"))
        self.assertEqual(len(favoritos), 1)

    def test_remover(self):
        favoritos = Favoritos(self.caminho)
        favoritos.adicionar("Matrix")
        self.assertTrue(favoritos.remover("Matrix"))
        self.assertFalse(favoritos.remover("Matrix"))
        self.assertEqual(len(Favoritos(self.caminho)), 0)

    def test_arquivo_corrompido_vira_lista_vazia(self):
        self.caminho.write_text("isso não é json", encoding="utf-8")
        self.assertEqual(len(Favoritos(self.caminho)), 0)


if __name__ == "__main__":
    unittest.main()
