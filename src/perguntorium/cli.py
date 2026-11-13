import argparse
from pathlib import Path

from .distribuicao import distribuir_cartas
from .loader import carregar_banco
from .pdf import gerar_pdf


def combinar_bancos(bancos):
    """Combina vários bancos em um único banco de uso na atividade."""
    cards = []
    for indice, banco in enumerate(bancos, start=1):
        for bloco in banco["blocos"]:
            for card in bloco["cards"]:
                card_copia = dict(card)
                if "id" in card_copia:
                    card_copia["id"] = f"{indice}-{card_copia['id']}"
                cards.append(card_copia)

    return {
        "materia": "Bancos combinados",
        "topico": "Atividade combinada",
        "quantidade_cards": len(cards),
        "blocos": [{
            "bloco": 1,
            "titulo": "Todos os blocos",
            "cards": cards,
        }],
    }


def pedir_inteiro(prompt, minimo=None):
    while True:
        valor = input(prompt).strip()
        try:
            numero = int(valor)
        except ValueError:
            print("Digite um número inteiro válido.")
            continue

        if minimo is not None and numero < minimo:
            print(f"O valor mínimo é {minimo}.")
            continue

        return numero


def interpretar_arquivos(raw_arquivos):
    if not raw_arquivos:
        raise ValueError("Informe pelo menos um arquivo JSON.")

    caminhos = []
    for item in raw_arquivos.split(","):
        caminho = item.strip()
        if caminho:
            caminhos.append(Path(caminho))

    if not caminhos:
        raise ValueError("Nenhum arquivo JSON foi informado.")

    return caminhos


def executar_atividade(arquivos, numero_alunos, cards_por_aluno, caminho_saida, semente=None):
    bancos = [carregar_banco(caminho) for caminho in arquivos]
    banco = combinar_bancos(bancos) if len(bancos) > 1 else bancos[0]
    distribuicao = distribuir_cartas(banco, numero_alunos, cards_por_aluno, semente=semente)
    destino = gerar_pdf(banco, distribuicao, caminho_saida)
    return destino


def main():
    parser = argparse.ArgumentParser(
        description="Perguntorium: geração de cards e gabarito em PDF.",
        epilog="Exemplo: python main.py cards_quimica_misturas.json --alunos 6 --cards-por-aluno 5 --saida atividade.pdf",
    )
    parser.add_argument("arquivos", nargs="*", help="Arquivos JSON com os cards.")
    parser.add_argument("--alunos", type=int, help="Quantidade de alunos.")
    parser.add_argument("--cards-por-aluno", type=int, help="Quantidade de cards por aluno.")
    parser.add_argument("--saida", default="atividade.pdf", help="Caminho do PDF final.")
    parser.add_argument("--semente", type=int, default=None, help="Semente opcional para distribuição determinística.")
    args = parser.parse_args()

    print("Perguntorium")
    print("-" * 40)

    if args.arquivos:
        caminhos = [Path(item) for item in args.arquivos]
    else:
        entrada = input("Informe os arquivos JSON separados por vírgula: ").strip()
        caminhos = interpretar_arquivos(entrada)

    if args.alunos is None:
        numero_alunos = pedir_inteiro("Quantidade de alunos: ", minimo=1)
    else:
        numero_alunos = args.alunos

    if args.cards_por_aluno is None:
        cards_por_aluno = pedir_inteiro("Cards por aluno (mínimo 5): ", minimo=5)
    else:
        cards_por_aluno = args.cards_por_aluno

    try:
        destino = executar_atividade(caminhos, numero_alunos, cards_por_aluno, args.saida, semente=args.semente)
    except FileNotFoundError as erro:
        print(f"Erro: arquivo não encontrado. Verifique o caminho informado: {erro}")
        return 1
    except ValueError as erro:
        print(f"Erro: {erro}")
        return 1

    print(f"Atividade criada com sucesso: {destino}")
    print("Imprima o arquivo PDF, recorte os cards e separe o gabarito do professor.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
