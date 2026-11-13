import json
from pathlib import Path


def carregar_banco(caminho):
    """Lê e valida um banco de questões em formato JSON."""
    caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except json.JSONDecodeError as erro:
        raise ValueError(f"JSON inválido em {caminho}: {erro.msg}") from erro

    validar_banco(dados)
    return dados


def validar_banco(banco):
    """Valida a estrutura mínima dos dados do banco."""
    if not isinstance(banco, dict):
        raise ValueError("O banco deve ser um dicionário JSON.")

    campos_obrigatorios = ["materia", "topico", "quantidade_cards", "blocos"]
    for campo in campos_obrigatorios:
        if campo not in banco:
            raise ValueError(f"Campo obrigatório ausente: {campo}")

    if not isinstance(banco["blocos"], list):
        raise ValueError("A lista de blocos deve existir e ser uma lista.")

    if not isinstance(banco["quantidade_cards"], int):
        raise ValueError("O campo 'quantidade_cards' deve ser um inteiro.")

    total_cards = 0

    for bloco in banco["blocos"]:
        if not isinstance(bloco, dict):
            raise ValueError("Cada bloco deve ser um objeto JSON.")

        if "cards" not in bloco or not isinstance(bloco["cards"], list):
            raise ValueError(f"O bloco '{bloco.get('titulo', 'sem nome')}' não possui uma lista de cards.")

        for card in bloco["cards"]:
            if not isinstance(card, dict):
                raise ValueError("Cada card deve ser um objeto JSON.")

            if "pergunta" not in card or not isinstance(card["pergunta"], str) or not card["pergunta"].strip():
                raise ValueError("Cada card deve possuir uma pergunta válida.")

            if "resposta" not in card or not isinstance(card["resposta"], str) or not card["resposta"].strip():
                raise ValueError("Cada card deve possuir uma resposta válida.")

            total_cards += 1

    if total_cards != banco["quantidade_cards"]:
        raise ValueError(
            "A quantidade de cards informada não bate com o total encontrado no banco. "
            f"Esperado: {banco['quantidade_cards']}; encontrado: {total_cards}."
        )

    return True
