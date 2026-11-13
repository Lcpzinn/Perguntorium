import math
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


CARD_WIDTH_MM = 63
CARD_HEIGHT_MM = 88
PAGE_MARGIN = 12 * mm
PAGE_TITLE_HEIGHT = 18 * mm
CARD_GAP = 8 * mm
MIN_FONT_SIZE = 8
MAX_FONT_SIZE = 12


def _make_paragraph(text, font_size):
    estilo = ParagraphStyle(
        "CardText",
        fontName="Helvetica",
        fontSize=font_size,
        leading=font_size * 1.25,
        alignment=1,
        splitLongWords=1,
    )
    texto = escape(str(text)).replace("\n", "<br/>")
    return Paragraph(texto, estilo)


def _measure_layout(items, columns, font_size):
    rows = math.ceil(len(items) / columns)
    area_width = A4[0] - 2 * PAGE_MARGIN
    area_height = A4[1] - 2 * PAGE_MARGIN - PAGE_TITLE_HEIGHT
    cell_width = (area_width - (columns - 1) * CARD_GAP) / columns
    cell_height = (area_height - (rows - 1) * CARD_GAP) / rows
    card_width = cell_width
    card_height = cell_height

    poker_width = CARD_WIDTH_MM * mm
    poker_height = CARD_HEIGHT_MM * mm
    if cell_width >= poker_width and cell_height >= poker_height:
        cabem_no_tamanho_original = all(
            _make_paragraph(item["text"], font_size).wrap(
                poker_width - 8 * mm,
                poker_height - 18 * mm,
            )[1] <= poker_height - 18 * mm
            for item in items
        )
        if cabem_no_tamanho_original:
            card_width = poker_width
            card_height = poker_height

    text_width = card_width - 8 * mm
    text_height = card_height - 18 * mm

    if text_width <= 0 or text_height <= 0:
        return None

    for item in items:
        paragraph = _make_paragraph(item["text"], font_size)
        _, paragraph_height = paragraph.wrap(text_width, text_height)
        if paragraph_height > text_height:
            return None

    return {
        "columns": columns,
        "card_width": card_width,
        "card_height": card_height,
        "font_size": font_size,
    }


def _find_layout(items):
    if not items:
        return None

    aspect_ratio = CARD_WIDTH_MM / CARD_HEIGHT_MM
    layouts = []
    for columns in range(1, len(items) + 1):
        for half_points in range(MAX_FONT_SIZE * 2, MIN_FONT_SIZE * 2 - 1, -1):
            font_size = half_points / 2
            layout = _measure_layout(items, columns, font_size)
            if layout is not None:
                ratio = layout["card_width"] / layout["card_height"]
                shape_score = -abs(math.log(ratio / aspect_ratio))
                area_score = layout["card_width"] * layout["card_height"]
                layout["score"] = (font_size, shape_score, area_score)
                layouts.append(layout)
                break

    return max(layouts, key=lambda layout: layout["score"]) if layouts else None


def _paginate_cards(items):
    paginas = []
    inicio = 0

    while inicio < len(items):
        layout = None
        quantidade = len(items) - inicio
        while quantidade:
            candidatos = items[inicio:inicio + quantidade]
            layout = _find_layout(candidatos)
            if layout is not None:
                paginas.append({"items": candidatos, "layout": layout})
                inicio += quantidade
                break
            quantidade -= 1

        if layout is None:
            raise ValueError(
                "Um texto dos cards é longo demais para caber em uma folha A4 "
                f"mesmo com fonte de {MIN_FONT_SIZE} pontos. Revise o conteúdo."
            )

    return paginas


def _draw_cut_marks(canv, x, y, width, height):
    margin = 3 * mm
    canv.setStrokeColorRGB(0.5, 0.5, 0.5)
    canv.setLineWidth(0.5)
    canv.line(x - margin, y + height / 2, x - 2 * mm, y + height / 2)
    canv.line(x + width + 2 * mm, y + height / 2, x + width + margin, y + height / 2)
    canv.line(x + width / 2, y - margin, x + width / 2, y - 2 * mm)
    canv.line(x + width / 2, y + height + 2 * mm, x + width / 2, y + height + margin)


def _draw_card(canv, x, y, width, height, item, layout):
    canv.setStrokeColorRGB(0.2, 0.2, 0.2)
    canv.setFillColorRGB(1, 1, 1)
    canv.rect(x, y, width, height, stroke=1, fill=1)
    _draw_cut_marks(canv, x, y, width, height)

    canv.setFillColorRGB(0, 0, 0)
    canv.setFont("Helvetica-Bold", 8)
    canv.drawCentredString(x + width / 2, y + height - 5 * mm, item["title"])

    paragraph = _make_paragraph(item["text"], layout["font_size"])
    text_width = width - 8 * mm
    text_height = height - 18 * mm
    _, paragraph_height = paragraph.wrap(text_width, text_height)
    paragraph.drawOn(canv, x + 4 * mm, y + (height - paragraph_height) / 2 - 2 * mm)


def _draw_page(canv, page_title, pagina):
    canv.setFont("Helvetica-Bold", 14)
    canv.setFillColorRGB(0, 0, 0)
    canv.drawString(PAGE_MARGIN, A4[1] - PAGE_MARGIN, page_title)

    layout = pagina["layout"]
    columns = layout["columns"]
    card_width = layout["card_width"]
    card_height = layout["card_height"]
    rows = math.ceil(len(pagina["items"]) / columns)
    area_width = A4[0] - 2 * PAGE_MARGIN
    area_height = A4[1] - 2 * PAGE_MARGIN - PAGE_TITLE_HEIGHT
    used_width = columns * card_width + (columns - 1) * CARD_GAP
    used_height = rows * card_height + (rows - 1) * CARD_GAP
    left = PAGE_MARGIN + (area_width - used_width) / 2
    top = A4[1] - PAGE_MARGIN - PAGE_TITLE_HEIGHT - (area_height - used_height) / 2

    for index, item in enumerate(pagina["items"]):
        row, column = divmod(index, columns)
        x = left + column * (card_width + CARD_GAP)
        y = top - (row + 1) * card_height - row * CARD_GAP
        _draw_card(canv, x, y, card_width, card_height, item, layout)


def _student_pages(distribuicao):
    paginas = []
    for aluno in distribuicao.get("alunos", []):
        aluno_numero = aluno["aluno"]
        items = [
            {"title": f"Aluno {aluno_numero}", "text": card.get("resposta", "")}
            for card in aluno["cards"]
        ]
        if not items:
            paginas.append({
                "title": f"Cards do aluno {aluno_numero}",
                "items": [],
                "layout": None,
            })
            continue

        for indice, pagina in enumerate(_paginate_cards(items)):
            sufixo = " (continuação)" if indice else ""
            paginas.append({
                **pagina,
                "title": f"Cards do aluno {aluno_numero}{sufixo}",
            })

    if not paginas:
        paginas.append({
            "title": "Cards dos alunos",
            "items": [],
            "layout": None,
        })
    return paginas


def _teacher_pages(banco, distribuicao):
    itens_ordenados = []
    for bloco in banco.get("blocos", []):
        for card in bloco.get("cards", []):
            pergunta = card.get("pergunta")
            if pergunta is None:
                raise ValueError("Não foi possível localizar a pergunta de um card do gabarito.")
            itens_ordenados.append({
                "title": "Professor",
                "text": f"{pergunta}\nResposta: {card.get('resposta', '')}",
            })

    if not itens_ordenados:
        return [{
            "title": "Gabarito do professor",
            "items": [],
            "layout": None,
        }]

    paginas = []
    for indice, pagina in enumerate(_paginate_cards(itens_ordenados)):
        sufixo = " (continuação)" if indice else ""
        paginas.append({
            **pagina,
            "title": f"Gabarito do professor{sufixo}",
        })
    return paginas


def _draw_empty_page(canv, titulo, mensagem):
    canv.setFont("Helvetica-Bold", 14)
    canv.drawString(PAGE_MARGIN, A4[1] - PAGE_MARGIN, titulo)
    canv.setFont("Helvetica", 12)
    canv.drawString(PAGE_MARGIN, A4[1] - PAGE_MARGIN - 15 * mm, mensagem)


def gerar_pdf(banco, distribuicao, caminho_arquivo):
    """Cria um PDF A4 com cards separados por aluno e gabarito do professor."""
    paginas = _student_pages(distribuicao) + _teacher_pages(banco, distribuicao)
    destino = Path(caminho_arquivo)
    destino.parent.mkdir(parents=True, exist_ok=True)

    pdf = canvas.Canvas(str(destino), pagesize=A4)
    for indice, pagina in enumerate(paginas):
        if pagina["layout"] is None:
            mensagem = "Nenhum card para imprimir."
            if pagina["title"] == "Gabarito do professor":
                mensagem = "Nenhum card disponível."
            _draw_empty_page(pdf, pagina["title"], mensagem)
        else:
            _draw_page(pdf, pagina["title"], pagina)
        if indice < len(paginas) - 1:
            pdf.showPage()

    pdf.save()
    return destino
