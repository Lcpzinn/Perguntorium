import random


class CoberturaInsuficienteError(ValueError):
    """Indica quantos cards cada aluno precisa para cobrir todas as respostas."""

    def __init__(self, cards_minimos_por_aluno, cards_maximos_por_aluno):
        self.cards_minimos_por_aluno = cards_minimos_por_aluno
        self.cards_maximos_por_aluno = cards_maximos_por_aluno
        super().__init__(
            "A quantidade total de cards dos alunos não cobre todas as respostas. "
            f"Aumente para {cards_minimos_por_aluno} a {cards_maximos_por_aluno} cards por aluno."
        )


def distribuir_cartas(banco, numero_alunos, cards_por_aluno, semente=None):
    """Distribui cards aleatoriamente respeitando as regras do jogo."""
    if numero_alunos <= 0:
        raise ValueError("O número de alunos deve ser maior que zero.")

    if cards_por_aluno < 5:
        raise ValueError("O mínimo de cards por aluno é 5.")

    todos_cards = []
    for bloco in banco["blocos"]:
        for card in bloco["cards"]:
            todos_cards.append(dict(card))

    cards_por_resposta = {}
    for card in todos_cards:
        cards_por_resposta.setdefault(card["resposta"], []).append(card)

    respostas_unicas = list(cards_por_resposta)
    if len(respostas_unicas) < 5:
        raise ValueError(
            "O banco precisa ter pelo menos 5 respostas distintas para cada aluno "
            "receber o mínimo de cards sem repetição."
        )
    if cards_por_aluno > len(respostas_unicas):
        raise ValueError(
            f"O banco tem apenas {len(respostas_unicas)} respostas distintas; "
            "um aluno não pode receber mais cards do que isso sem repetir respostas."
        )

    total_necessario = numero_alunos * cards_por_aluno
    if total_necessario < len(respostas_unicas):
        cards_minimos = (len(respostas_unicas) + numero_alunos - 1) // numero_alunos
        raise CoberturaInsuficienteError(max(5, cards_minimos), len(respostas_unicas))

    rng = random.Random(semente)
    rng.shuffle(respostas_unicas)
    alunos = [[] for _ in range(numero_alunos)]

    for resposta in respostas_unicas:
        elegiveis = [
            indice for indice, cards in enumerate(alunos)
            if len(cards) < cards_por_aluno
        ]
        menor_quantidade = min(len(alunos[indice]) for indice in elegiveis)
        menos_cards = [
            indice for indice in elegiveis
            if len(alunos[indice]) == menor_quantidade
        ]
        aluno = rng.choice(menos_cards)
        alunos[aluno].append(rng.choice(cards_por_resposta[resposta]).copy())

    for indice, cards in enumerate(alunos):
        respostas_do_aluno = {card["resposta"] for card in cards}
        while len(cards) < cards_por_aluno:
            elegiveis = [
                resposta for resposta in respostas_unicas
                if resposta not in respostas_do_aluno
            ]
            resposta = rng.choice(elegiveis)
            cards.append(rng.choice(cards_por_resposta[resposta]).copy())
            respostas_do_aluno.add(resposta)

    resultado = {
        "alunos": [
            {"aluno": indice + 1, "cards": cards}
            for indice, cards in enumerate(alunos)
        ]
    }
    return resultado
