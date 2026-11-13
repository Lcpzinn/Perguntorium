from pathlib import Path
import base64
import re
import zlib

import pytest
from reportlab.lib.units import mm

from perguntorium.pdf import CARD_WIDTH_MM, CARD_HEIGHT_MM, _find_layout, gerar_pdf


def _conteudo_descomprimido(pdf_bytes):
    streams = re.findall(rb"stream\r?\n(.*?)endstream", pdf_bytes, re.DOTALL)
    streams = [stream.rstrip(b"\r\n") for stream in streams]
    return b"\n".join(
        zlib.decompress(base64.a85decode(b"<~" + stream, adobe=True))
        for stream in streams
    )


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


def test_layout_preserva_tamanho_poker_quando_ele_cabe():
    layout = _find_layout([{"title": "Aluno 1", "text": "Resposta breve"}])

    assert layout["card_width"] == pytest.approx(CARD_WIDTH_MM * mm)
    assert layout["card_height"] == pytest.approx(CARD_HEIGHT_MM * mm)


def test_gerar_pdf_cria_arquivo(tmp_path, banco_exemplo):
    distribuicao = {
        "alunos": [
            {"aluno": 1, "cards": [
                {"id": 1, "pergunta": "Pergunta 1", "resposta": "Resposta 1"},
                {"id": 2, "pergunta": "Pergunta 2", "resposta": "Resposta 2"},
            ]},
            {"aluno": 2, "cards": [
                {"id": 3, "pergunta": "Pergunta 3", "resposta": "Resposta 3"},
                {"id": 4, "pergunta": "Pergunta 4", "resposta": "Resposta 4"},
            ]},
        ]
    }

    arquivo = tmp_path / "atividade.pdf"
    gerar_pdf(banco_exemplo, distribuicao, arquivo)

    assert arquivo.exists()
    assert arquivo.stat().st_size > 0

    conteudo = arquivo.read_bytes()
    assert len(re.findall(rb"/Type\s*/Page\b", conteudo)) == 3
    assert b"/MediaBox [ 0 0 595.2756 841.8898 ]" in conteudo
    texto = _conteudo_descomprimido(conteudo)
    assert b"Cards do aluno 1" in texto
    assert b"Cards do aluno 2" in texto
    indice_gabarito = texto.index(b"Gabarito do professor")
    assert b"Pergunta 1" not in texto[:indice_gabarito]
    assert b"Pergunta 1" in texto[indice_gabarito:]
    for numero in range(1, 7):
        assert f"Pergunta {numero}".encode() in texto[indice_gabarito:]
        assert f"Resposta {numero}".encode() in texto[indice_gabarito:]

    assert texto.count(b"Pergunta 1") == 1


def test_gerar_pdf_preserva_texto_longo(tmp_path, banco_exemplo):
    distribuicao = {
        "alunos": [
            {
                "aluno": 1,
                "cards": [
                    {
                        "id": 1,
                        "pergunta": "Question",
                        "resposta": "Beginning " + "long readable answer " * 120 + "END_MARKER",
                    }
                ],
            }
        ]
    }

    arquivo = tmp_path / "texto_longo.pdf"
    gerar_pdf(banco_exemplo, distribuicao, arquivo)

    assert b"END_MARKER" in _conteudo_descomprimido(arquivo.read_bytes())


def test_gerar_pdf_separa_folhas_de_continuacao_por_aluno(tmp_path, banco_exemplo):
    cards = [
        {
            "id": numero,
            "pergunta": f"Pergunta {numero}",
            "resposta": f"Inicio {numero} " + "texto longo para leitura " * 60 + f" FIM_{numero}",
        }
        for numero in range(1, 7)
    ]
    distribuicao = {"alunos": [{"aluno": 1, "cards": cards}]}
    arquivo = tmp_path / "continuacao.pdf"

    gerar_pdf(banco_exemplo, distribuicao, arquivo)

    conteudo = arquivo.read_bytes()
    texto = _conteudo_descomprimido(conteudo)
    assert len(re.findall(rb"/Type\s*/Page\b", conteudo)) > 2
    assert texto.count(b"Cards do aluno 1") > 1
    for numero in range(1, 7):
        assert f"FIM_{numero}".encode() in texto
