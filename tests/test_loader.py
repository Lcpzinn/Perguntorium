from pathlib import Path

import pytest

from perguntorium.loader import carregar_banco, validar_banco


def test_carregar_banco_json_valido():
    caminho = Path(__file__).resolve().parents[1] / "cards_quimica_misturas.json"

    dados = carregar_banco(caminho)

    assert dados["materia"] == "Química - Ensino Fundamental II"
    assert dados["quantidade_cards"] == 30
    total_cards = sum(len(bloco["cards"]) for bloco in dados["blocos"])
    assert total_cards == 30


def test_carregar_banco_arquivo_inexistente():
    caminho = Path(__file__).resolve().parents[1] / "arquivo_inexistente.json"

    with pytest.raises(FileNotFoundError):
        carregar_banco(caminho)


def test_carregar_banco_json_invalido(tmp_path):
    caminho = tmp_path / "arquivo_invalido.json"
    caminho.write_text("{json invalido", encoding="utf-8")

    with pytest.raises(ValueError, match="JSON"):
        carregar_banco(caminho)


def test_validar_banco_rejeita_card_sem_pergunta():
    banco = {
        "materia": "Química",
        "topico": "Misturas",
        "quantidade_cards": 1,
        "blocos": [
            {
                "bloco": 1,
                "titulo": "Bloco de teste",
                "cards": [{"id": 1, "resposta": "Resposta correta"}],
            }
        ],
    }

    with pytest.raises(ValueError, match="pergunta"):
        validar_banco(banco)


def test_validar_banco_rejeita_card_sem_resposta():
    banco = {
        "materia": "Química",
        "topico": "Misturas",
        "quantidade_cards": 1,
        "blocos": [
            {
                "bloco": 1,
                "titulo": "Bloco de teste",
                "cards": [{"id": 1, "pergunta": "Qual é a resposta?"}],
            }
        ],
    }

    with pytest.raises(ValueError, match="resposta"):
        validar_banco(banco)
