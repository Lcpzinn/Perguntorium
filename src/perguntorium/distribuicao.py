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
            todos_cards.append(dict(card))

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

    if total_necessario < len(respostas_unicas):
        raise ValueError(
            "Quantidade insuficiente de cards para cobrir todas as respostas do banco. "
            f"Necessário: {len(respostas_unicas)} cards distribuídos no mínimo; atual: {total_necessario}."
        )

    rng = random.Random(semente)
    restantes = [card.copy() for card in todos_cards]
    rng.shuffle(restantes)

    alunos = {indice: [] for indice in range(numero_alunos)}

    for resposta in respostas_unicas:
        candidatos = [card for card in restantes if card["resposta"] == resposta]
        if not candidatos:
            continue

        aluno_alvo = None
        for indice in range(numero_alunos):
            if len(alunos[indice]) < cards_por_aluno and not any(card["resposta"] == resposta for card in alunos[indice]):
                aluno_alvo = indice
                break

        if aluno_alvo is None:
            raise ValueError("Não foi possível distribuir todos os cards sem repetir respostas dentro do mesmo aluno.")

        card_escolhido = candidatos[0]
        alunos[aluno_alvo].append(card_escolhido)
        restantes.remove(card_escolhido)

    for indice in range(numero_alunos):
        while len(alunos[indice]) < cards_por_aluno and restantes:
            candidatos = [
                card for card in restantes
                if not any(carta["resposta"] == card["resposta"] for carta in alunos[indice])
            ]
            if not candidatos:
                break
            escolha = rng.choice(candidatos)
            alunos[indice].append(escolha)
            restantes.remove(escolha)

    if any(len(alunos[indice]) < cards_por_aluno for indice in range(numero_alunos)):
        raise ValueError("Não foi possível completar a distribuição com os cards disponíveis.")

    resultado = {
        "alunos": [
            {"aluno": indice + 1, "cards": alunos[indice]}
            for indice in range(numero_alunos)
        ]
    }
    return resultado
