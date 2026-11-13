from pathlib import Path

import pytest

from perguntorium.pdf import CARD_WIDTH_MM, CARD_HEIGHT_MM, gerar_pdf


@pytest.fixture
def banco_exemplo():
    return {
        "materia": "Química",
        "topico": "Misturas",
        "quantidade_cards": 6,
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
                ],
            }
        ],
    }


def test_card_dimensions_are_defined():
    assert CARD_WIDTH_MM == 63
    assert CARD_HEIGHT_MM == 88


def test_gerar_pdf_cria_arquivo(tmp_path, banco_exemplo):
    distribuicao = {
        "alunos": [
            {"aluno": 1, "cards": [{"id": 1, "resposta": "Resposta 1"}, {"id": 2, "resposta": "Resposta 2"}]},
            {"aluno": 2, "cards": [{"id": 3, "resposta": "Resposta 3"}, {"id": 4, "resposta": "Resposta 4"}]},
        ]
    }

    arquivo = tmp_path / "atividade.pdf"
    gerar_pdf(banco_exemplo, distribuicao, arquivo)

    assert arquivo.exists()
    assert arquivo.stat().st_size > 0
