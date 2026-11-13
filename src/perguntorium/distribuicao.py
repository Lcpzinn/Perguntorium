import random


def distribuir_cartas(banco, numero_alunos, cards_por_aluno, semente=None):
    """Distribui cards aleatoriamente respeitando as regras do jogo."""
    if numero_alunos <= 0:
        raise ValueError("O número de alunos deve ser maior que zero.")

    if cards_por_aluno < 5:
        raise ValueError("O mínimo de cards por aluno é 5.")

    todos_cards = []
    for bloco in banco["blocos"]:
        for card in bloco["cards"]:
            todos_cards.append(card)

    total_disponivel = len(todos_cards)
    total_necessario = numero_alunos * cards_por_aluno

    if total_disponivel < total_necessario:
        raise ValueError(
            "Quantidade insuficiente de cards para atender o total solicitado "
            f"({total_necessario}) com {numero_alunos} alunos e {cards_por_aluno} cards por aluno."
        )

    respostas_unicas = []
    vistas = set()
    for card in todos_cards:
        resposta = card["resposta"]
        if resposta not in vistas:
            vistas.add(resposta)
            respostas_unicas.append(resposta)

    if total_disponivel < len(respostas_unicas):
        raise ValueError("Quantidade insuficiente de cards para cobrir todas as respostas.")

    rng = random.Random(semente)
    restantes = [card.copy() for card in todos_cards]
    rng.shuffle(restantes)

    alunos = {indice: [] for indice in range(numero_alunos)}

    for resposta in respostas_unicas:
        candidato = None
        for card in restantes:
            if card["resposta"] == resposta:
                candidato = card
                break

        if candidato is None:
            continue

        aluno_alvo = rng.choice(list(alunos.keys()))
        while len(alunos[aluno_alvo]) >= cards_por_aluno:
            aluno_alvo = rng.choice(list(alunos.keys()))

        if any(card["resposta"] == resposta for card in alunos[aluno_alvo]):
            for indice in rng.sample(list(alunos.keys()), k=len(alunos)):
                if len(alunos[indice]) < cards_por_aluno and not any(card["resposta"] == resposta for card in alunos[indice]):
                    aluno_alvo = indice
                    break

        alunos[aluno_alvo].append(candidato)
        restantes.remove(candidato)

    for indice in range(numero_alunos):
        while len(alunos[indice]) < cards_por_aluno:
            candidato = None
            for card in restantes:
                if not any(c["resposta"] == card["resposta"] for c in alunos[indice]):
                    candidato = card
                    break

            if candidato is None:
                candidato = restantes[0]

            alunos[indice].append(candidato)
            restantes.remove(candidato)

    resultado = {
        "alunos": [
            {"aluno": indice + 1, "cards": alunos[indice]}
            for indice in range(numero_alunos)
        ]
    }
    return resultado
