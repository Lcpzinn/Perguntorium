import pytest

from perguntorium.distribuicao import CoberturaInsuficienteError, distribuir_cartas


@pytest.fixture
def banco_exemplo():
    return {
        "materia": "Química",
        "topico": "Misturas",
        "quantidade_cards": 10,
        "blocos": [
            {
                "bloco": 1,
                "titulo": "Bloco de teste",
                "cards": [
                    {"id": 1, "pergunta": "Pergunta 1", "resposta": "Resposta 1"},
                    {"id": 2, "pergunta": "Pergunta 2", "resposta": "Resposta 2"},
                    {"id": 3, "pergunta": "Pergunta 3", "resposta": "Resposta 3"},
                    {"id": 4, "pergunta": "Pergunta 4", "resposta": "Resposta 4"},
                    {"id": 5, "pergunta": "Pergunta 5", "resposta": "Resposta 5"},
                    {"id": 6, "pergunta": "Pergunta 6", "resposta": "Resposta 6"},
                    {"id": 7, "pergunta": "Pergunta 7", "resposta": "Resposta 7"},
                    {"id": 8, "pergunta": "Pergunta 8", "resposta": "Resposta 8"},
                    {"id": 9, "pergunta": "Pergunta 9", "resposta": "Resposta 9"},
                    {"id": 10, "pergunta": "Pergunta 10", "resposta": "Resposta 10"},
                ],
            }
        ],
    }


def test_distribuicao_respeita_limite_por_aluno(banco_exemplo):
    resultado = distribuir_cartas(banco_exemplo, numero_alunos=2, cards_por_aluno=5, semente=7)

    assert len(resultado["alunos"]) == 2
    for aluno in resultado["alunos"]:
        assert len(aluno["cards"]) == 5
        respostas = [card["resposta"] for card in aluno["cards"]]
        assert len(respostas) == len(set(respostas))


def test_distribuicao_cobre_todas_as_respostas_quando_possivel(banco_exemplo):
    resultado = distribuir_cartas(banco_exemplo, numero_alunos=2, cards_por_aluno=5, semente=7)

    respostas_distribuidas = {
        card["resposta"]
        for aluno in resultado["alunos"]
        for card in aluno["cards"]
    }

    assert len(respostas_distribuidas) == banco_exemplo["quantidade_cards"]


def test_distribuicao_repete_respostas_entre_alunos_sem_repetir_no_mesmo_aluno(banco_exemplo):
    resultado = distribuir_cartas(banco_exemplo, numero_alunos=3, cards_por_aluno=5, semente=7)

    respostas_por_aluno = [
        [card["resposta"] for card in aluno["cards"]]
        for aluno in resultado["alunos"]
    ]
    assert all(len(respostas) == len(set(respostas)) for respostas in respostas_por_aluno)
    assert sum(map(len, respostas_por_aluno)) == 15
    assert len(set.union(*(set(respostas) for respostas in respostas_por_aluno))) == 10


def test_distribuicao_e_deterministica_com_a_mesma_semente(banco_exemplo):
    primeira = distribuir_cartas(banco_exemplo, numero_alunos=3, cards_por_aluno=5, semente=7)
    segunda = distribuir_cartas(banco_exemplo, numero_alunos=3, cards_por_aluno=5, semente=7)

    assert primeira == segunda


def test_distribuicao_ativa_pedido_de_aumento_quando_falta_cobertura(banco_exemplo):
    with pytest.raises(CoberturaInsuficienteError) as erro:
        distribuir_cartas(banco_exemplo, numero_alunos=1, cards_por_aluno=5, semente=7)

    assert erro.value.cards_minimos_por_aluno == 10
    assert erro.value.cards_maximos_por_aluno == 10


def test_distribuicao_avisar_quando_nao_cobrir_todas_as_respostas():
    banco = {
        "materia": "Química",
        "topico": "Misturas",
        "quantidade_cards": 30,
        "blocos": [
            {
                "bloco": 1,
                "titulo": "Bloco",
                "cards": [
                    {"id": i, "pergunta": f"Pergunta {i}", "resposta": f"Resposta {i}"}
                    for i in range(1, 31)
                ],
            }
        ],
    }

    with pytest.raises(CoberturaInsuficienteError) as erro:
        distribuir_cartas(banco, numero_alunos=2, cards_por_aluno=5, semente=7)

    assert erro.value.cards_minimos_por_aluno == 15


@pytest.mark.parametrize(
    ("numero_alunos", "cards_por_aluno"),
    [(0, 5), (2, 0), (2, -1), (2, 4), (2, 11)],
)
def test_distribuicao_rejeita_quantidades_invalidas(banco_exemplo, numero_alunos, cards_por_aluno):
    with pytest.raises(ValueError):
        distribuir_cartas(banco_exemplo, numero_alunos, cards_por_aluno, semente=7)
