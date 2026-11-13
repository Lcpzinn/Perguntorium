import pytest

from perguntorium.distribuicao import distribuir_cartas


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


def test_distribuicao_avisar_quando_nao_houver_cards_suficientes(banco_exemplo):
    with pytest.raises(ValueError, match="insuficiente"):
        distribuir_cartas(banco_exemplo, numero_alunos=3, cards_por_aluno=5, semente=7)


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

    with pytest.raises(ValueError, match="cobrir todas as respostas"):
        distribuir_cartas(banco, numero_alunos=2, cards_por_aluno=5, semente=7)
