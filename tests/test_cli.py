from pathlib import Path

from perguntorium.cli import main, pedir_inteiro, resolver_arquivos
from perguntorium.distribuicao import CoberturaInsuficienteError


def test_resolver_arquivos_aceita_argumento_unico():
    caminhos = resolver_arquivos(["cards_quimica_misturas.json"])

    assert caminhos == [Path("cards_quimica_misturas.json")]


def test_resolver_arquivos_aceita_lista_legacy():
    caminhos = resolver_arquivos(["arquivo1.json", "arquivo2.json"])

    assert caminhos == [Path("arquivo1.json"), Path("arquivo2.json")]


def test_pedir_inteiro_repete_entrada_fora_dos_limites(monkeypatch, capsys):
    respostas = iter(["2", "11", "7"])
    monkeypatch.setattr("builtins.input", lambda _: next(respostas))

    valor = pedir_inteiro("Quantidade: ", minimo=5, maximo=10)

    assert valor == 7
    saida = capsys.readouterr().out
    assert "mínimo é 5" in saida
    assert "máximo é 10" in saida


def test_main_pede_aumento_de_cards_quando_falta_cobertura(monkeypatch, tmp_path):
    import sys

    argumentos = [
        "main.py",
        "--arquivo", "banco.json",
        "--alunos", "2",
        "--cards-por-aluno", "5",
        "--saida", str(tmp_path / "atividade.pdf"),
    ]
    monkeypatch.setattr(sys, "argv", argumentos)
    monkeypatch.setattr("builtins.input", lambda _: "15")

    chamadas = []

    def executar(arquivos, alunos, cards_por_aluno, saida, semente=None):
        chamadas.append(cards_por_aluno)
        if len(chamadas) == 1:
            raise CoberturaInsuficienteError(15, 30)
        return Path(saida)

    monkeypatch.setattr("perguntorium.cli.executar_atividade", executar)

    assert main() == 0
    assert chamadas == [5, 15]
