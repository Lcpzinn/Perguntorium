from pathlib import Path
import textwrap

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


CARD_WIDTH_MM = 63
CARD_HEIGHT_MM = 88


def _card_dimensions():
    return CARD_WIDTH_MM * mm, CARD_HEIGHT_MM * mm


def _draw_card(canv, x, y, width, height, title, lines):
    canv.setStrokeColorRGB(0.2, 0.2, 0.2)
    canv.setFillColorRGB(1, 1, 1)
    canv.rect(x, y, width, height, stroke=1, fill=1)

    canv.setFillColorRGB(0, 0, 0)
    canv.setFont("Helvetica-Bold", 9)
    canv.drawString(x + 4 * mm, y + height - 7 * mm, title)

    canv.setFont("Helvetica", 9)
    current_y = y + height - 15 * mm
    for line in lines:
        wrapped = textwrap.wrap(line, width=32)
        for item in wrapped:
            if current_y < y + 5 * mm:
                break
            canv.drawString(x + 4 * mm, current_y, item)
            current_y -= 6 * mm


def _draw_student_cards(canv, distribuicao):
    alunos = distribuicao.get("alunos", [])
    if not alunos:
        return

    page_x, page_y = A4
    card_w, card_h = _card_dimensions()
    left_margin = 15 * mm
    top_margin = page_y - 20 * mm
    x_positions = [left_margin, left_margin + card_w + 10 * mm]

    current_page = 1
    index = 0
    for aluno in alunos:
        for card in aluno["cards"]:
            col = index % 2
            row = index // 2
            x = x_positions[col]
            y = top_margin - (row * (card_h + 10 * mm)) - card_h

            if y < 15 * mm:
                canv.showPage()
                current_page += 1
                index = 0
                col = 0
                row = 0
                x = x_positions[0]
                y = top_margin - (row * (card_h + 10 * mm)) - card_h

            _draw_card(
                canv,
                x,
                y,
                card_w,
                card_h,
                f"Aluno {aluno['aluno']}",
                [card.get("resposta", "")],
            )
            index += 1

    if index == 0:
        canv.drawString(20 * mm, page_y - 20 * mm, "Nenhum card para imprimir.")


def _draw_teacher_cards(canv, banco, distribuicao):
    cards_professor = []
    for aluno in distribuicao.get("alunos", []):
        for card in aluno["cards"]:
            pergunta = next(
                (item["pergunta"] for bloco in banco["blocos"] for item in bloco["cards"] if item["id"] == card["id"]),
                "Pergunta não localizada",
            )
            cards_professor.append({"pergunta": pergunta, "resposta": card["resposta"]})

    if not cards_professor:
        canv.setFont("Helvetica-Bold", 16)
        canv.drawString(20 * mm, A4[1] - 20 * mm, "Gabarito do professor")
        canv.drawString(20 * mm, A4[1] - 35 * mm, "Nenhum card disponível.")
        return

    page_x, page_y = A4
    card_w, card_h = _card_dimensions()
    left_margin = 15 * mm
    top_margin = page_y - 40 * mm
    x_positions = [left_margin, left_margin + card_w + 10 * mm]

    canv.setFont("Helvetica-Bold", 16)
    canv.drawString(20 * mm, page_y - 20 * mm, "Gabarito do professor")

    index = 0
    for card in cards_professor:
        col = index % 2
        row = index // 2
        x = x_positions[col]
        y = top_margin - (row * (card_h + 10 * mm)) - card_h

        if y < 15 * mm:
            canv.showPage()
            canv.setFont("Helvetica-Bold", 16)
            canv.drawString(20 * mm, page_y - 20 * mm, "Gabarito do professor")
            index = 0
            col = 0
            row = 0
            x = x_positions[0]
            y = top_margin - (row * (card_h + 10 * mm)) - card_h

        _draw_card(
            canv,
            x,
            y,
            card_w,
            card_h,
            "Professor",
            [card["pergunta"], "Resposta: " + card["resposta"]],
        )
        index += 1


def gerar_pdf(banco, distribuicao, caminho_arquivo):
    """Cria um PDF com os cards dos alunos e o gabarito do professor."""
    destino = Path(caminho_arquivo)
    destino.parent.mkdir(parents=True, exist_ok=True)

    pdf = canvas.Canvas(str(destino), pagesize=A4)

    _draw_student_cards(pdf, distribuicao)
    pdf.showPage()
    _draw_teacher_cards(pdf, banco, distribuicao)
    pdf.save()

    return destino
