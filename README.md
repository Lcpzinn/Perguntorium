# Perguntorium

Programa em Python para gerar cartas de respostas para sala de aula sem uso de computador ou celular, com material impresso para professores e alunos.

## Objetivo

O software lê um ou mais bancos de questões em JSON, distribui respostas aleatoriamente aos alunos, valida regras do jogo e gera um PDF com:

- cards para os alunos
- gabarito para o professor

## Requisitos

- Python 3.10+
- ReportLab
- pytest

## Instalação

No diretório do projeto, instale as dependências:

```powershell
"C:/Users/Projeto ciências/AppData/Local/Python/pythoncore-3.14-64/python.exe" -m pip install -r requirements.txt
```

## Como usar

### Executar a CLI

```powershell
"C:/Users/Projeto ciências/AppData/Local/Python/pythoncore-3.14-64/python.exe" main.py cards_quimica_misturas.json --alunos 6 --cards-por-aluno 5 --saida exemplo.pdf
```

### Também pode ser usado interativamente

```powershell
"C:/Users/Projeto ciências/AppData/Local/Python/pythoncore-3.14-64/python.exe" main.py
```

## Regras do MVP

- mínimo de 5 cards por aluno
- cada aluno não recebe a mesma resposta mais de uma vez
- a mesma resposta pode aparecer em alunos diferentes
- se o total de cards não cobrir todas as respostas, o programa pede aumento na quantidade
- o sorteio considera todos os blocos do banco selecionado

## Testes

```powershell
"C:/Users/Projeto ciências/AppData/Local/Python/pythoncore-3.14-64/python.exe" -m pytest -q
```

## Estrutura do projeto

- `cards_quimica_misturas.json`: banco exemplo
- `src/perguntorium/loader.py`: leitura e validação do JSON
- `src/perguntorium/distribuicao.py`: regras de distribuição
- `src/perguntorium/pdf.py`: geração do PDF
- `src/perguntorium/cli.py`: interface de linha de comando
- `tests/`: testes automatizados
