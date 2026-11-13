# Progresso do projeto Perguntorium

Este arquivo registra o que foi implementado até o momento no projeto e serve como ponto de referência para continuar o desenvolvimento.

## Visão geral

O objetivo do projeto é gerar uma atividade impressa para professores do Ensino Fundamental, com cards de respostas para alunos e um gabarito do professor em um único PDF. O programa lê bancos de questões em JSON, valida a estrutura, distribui as respostas entre os alunos e produz o material de impressão.

## Estrutura atual do projeto

- `main.py`: ponto de entrada do programa.
- `README.md`: documentação geral de uso e regras do MVP.
- `cards_quimica_misturas.json`: banco de exemplo real com 30 cards.
- `src/perguntorium/loader.py`: leitura e validação do JSON.
- `src/perguntorium/distribuicao.py`: lógica de distribuição dos cards.
- `src/perguntorium/pdf.py`: geração do PDF para impressão.
- `src/perguntorium/cli.py`: interface da linha de comando.
- `tests/`: testes automatizados para validação das regras.

## Funcionalidades implementadas

### 1. Leitura e validação do banco JSON

A função `carregar_banco()` foi implementada para:
- verificar se o arquivo existe;
- ler o conteúdo em JSON;
- validar a estrutura mínima do banco;
- rejeitar JSON inválido;
- garantir que cada card tenha pergunta e resposta válidas;
- validar campos obrigatórios (`materia`, `topico`, `quantidade_cards`, `blocos`);
- checar se a quantidade declarada no banco bate com o total de cards reais.

Também existe a função `validar_banco()`, responsável pela validação do esquema mínimo.

### 2. Combinação de bancos

A CLI implementa a função `combinar_bancos()`, que permite juntar mais de um JSON em uma única atividade.

Regras relevantes:
- os cards são combinados em um único conjunto;
- IDs existentes são preservados com prefixo para evitar conflitos;
- o banco combinado mantém o formato compatível com o restante do fluxo.

### 3. Distribuição das respostas entre os alunos

A lógica foi implementada em `distribuicao.py` com a função `distribuir_cartas()`.

Regras atendidas:
- número de alunos maior que zero;
- mínimo de 5 cards por aluno;
- cada aluno recebe respostas sem repetição;
- a mesma resposta pode aparecer em alunos diferentes;
- considera todos os blocos do banco selecionado;
- usa `random.Random(semente)` para permitir distribuição determinística em testes;
- se não houver cobertura suficiente para todas as respostas, dispara `CoberturaInsuficienteError`;
- quando o banco tem menos respostas do que o necessário, solicita aumento na quantidade de cards por aluno.

### 4. Interface de linha de comando

A CLI em `cli.py` executa as etapas principais:
- leitura dos arquivos JSON;
- entrada do número de alunos;
- entrada da quantidade de cards por aluno;
- geração do PDF final.

Também há suporte para:
- execução em modo interativo;
- execução com parâmetros de linha de comando;
- opção `--semente` para tornar o sorteio reproduzível em testes;
- múltiplos arquivos JSON via `--arquivo` ou forma tradicional.

### 5. Geração do PDF

O módulo `pdf.py` gera um PDF com:
- cards dos alunos em folhas A4;
- marcações de corte para impressão;
- material separado por aluno;
- gabarito do professor no mesmo arquivo;
- paginação automática em caso de muitos cards;
- páginas de continuação para o mesmo aluno quando necessário;
- separação visual entre o material dos alunos e o gabarito.

Também há lógica para ajustar a página ao tamanho do conteúdo e manter a legibilidade do texto.

## Regras do MVP confirmadas no código

O projeto já contempla as decisões principais do contexto do MVP:

- mínimo de 5 cards por aluno;
- não repetir a mesma resposta no conjunto do mesmo aluno;
- resposta pode ser compartilhada entre alunos diferentes;
- o professor pode combinar múltiplos arquivos JSON;
- se não houver cobertura suficiente, o programa avisa e pede aumento na quantidade;
- o material dos alunos permanece separado do gabarito;
- a geração do PDF é realizada em um único arquivo.

## Testes automatizados existentes

Os testes cobrem os principais pontos do comportamento esperado:

### `tests/test_loader.py`
- banco JSON válido;
- arquivo inexistente;
- JSON inválido;
- card sem pergunta;
- card sem resposta;
- campo obrigatório ausente.

### `tests/test_distribuicao.py`
- limite de cards por aluno;
- cobertura total de respostas quando possível;
- repetição entre alunos sem duplicar dentro do mesmo aluno;
- distribuição determinística com semente;
- atualização de quantidade quando faltam cards;
- validação de entradas inválidas.

### `tests/test_pdf.py`
- dimensões dos cards;
- layout preservando o tamanho de cartão poker;
- criação do PDF;
- presença de páginas e textos esperados;
- continuação por aluno quando o texto for longo;
- separação visual do gabarito.

### `tests/test_cli.py`
- leitura de arquivos via CLI;
- validação de entrada numérica;
- recuperação de erro quando a cobertura é insuficiente.

## Estado atual do projeto

O projeto está em um estágio funcional de MVP, com a base principal implementada:
- leitura e validação do JSON;
- distribuição de cards respeitando as regras do jogo;
- geração de PDF com material do aluno e gabarito do professor;
- testes automatizados cobrindo as regras centrais;
- interface CLI funcional.

## Ajuste recente: gabarito do professor

Foi identificado e corrigido um problema na geração do PDF: o gabarito do professor estava sendo montado a partir dos cards já distribuídos para os alunos, o que gerava repetição, ordem aleatória e excesso de itens impressos para o professor.

A correção foi aplicada para garantir que o gabarito seja produzido a partir do banco completo do exercício, em ordem estável e sem duplicatas por aluno. Essa mudança reduz o material de impressão do professor ao que realmente é necessário: cada pergunta com a sua resposta correta, uma única vez.

## Validação prática do PDF

Foi executado um teste real de geração do arquivo PDF com o comando `python main.py --arquivo cards_quimica_misturas.json --alunos 6 --cards-por-aluno 5 --saida atividade_teste.pdf`.

O arquivo foi gerado com sucesso e a mensagem final foi confirmada pela CLI, indicando que a atividade foi criada corretamente. Nesta etapa, o foco foi verificar a geração do documento e a estrutura do material impresso.

## Observações finais

Este relatório foi gravado para registrar o estado atual do projeto e facilitar a continuidade do trabalho sem perder o contexto já implementado. O próximo passo recomendado, caso o desenvolvimento continue, é revisar a paginação e a impressão final para garantir melhor usabilidade em sala e validação visual do PDF gerado.
