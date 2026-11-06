# Perguntorium: orientações do projeto

## Objetivo

Construir, em etapas pequenas, um programa de linha de comando em Python para professores do Ensino Fundamental no Brasil prepararem uma atividade impressa de perguntas e respostas. O programa deve ler um ou mais bancos de questões em JSON, distribuir cards de acordo com as opções escolhidas pelo professor e gerar um PDF imprimível com os materiais dos alunos e o gabarito do professor.

Este é um projeto de introdução à programação. Priorize código legível, nomes claros, funções pequenas e conceitos que o autor já possa aprender e explicar. Evite frameworks, arquitetura excessiva e funcionalidades não combinadas.

## Como colaborar

- Desenvolva somente a etapa que o usuário aprovou; não antecipe funcionalidades de etapas futuras.
- Antes de alterar o formato dos bancos, examine os arquivos existentes e preserve sua compatibilidade sempre que possível.
- Explique decisões importantes e questione requisitos que possam tornar a atividade ambígua, impossível de imprimir ou difícil de usar em sala.
- Prefira a biblioteca padrão do Python. Use ReportLab para produzir PDFs, conforme requisito da disciplina.
- Escreva testes automatizados para as regras da aplicação. Prefira `unittest` inicialmente, para manter o projeto acessível e sem dependência de teste adicional.
- Execute os testes relevantes após cada etapa e informe claramente o que foi verificado e o que ficou pendente.
- Não adicione dependências sem explicar sua finalidade e como instalá-las.
- Mantenha mensagens, documentação e interface em português do Brasil, salvo solicitação diferente.

## Escopo inicial proposto

O primeiro produto funcional deve ser pequeno e verificável:

1. Ler um banco JSON existente e validar sua estrutura e seus cards.
2. Perguntar ao professor quantos alunos participarão e quantos cards cada aluno receberá.
3. Selecionar e distribuir os cards aleatoriamente, validando entradas e avisando quando a quantidade pedida não puder ser atendida conforme a regra de repetição definida.
4. Gerar um PDF para impressão com os cards dos alunos e um gabarito do professor no mesmo arquivo.
5. Testar a leitura/validação do banco, os limites da distribuição, a aleatoriedade controlável nos testes e a criação básica do PDF.

O banco atual, `cards_quimica_misturas.json`, contém 30 pares de pergunta e resposta em cinco blocos. Trate-o como exemplo real e teste sua leitura antes de propor mudanças no esquema.

## Decisões a confirmar antes da lógica de distribuição

Não assuma o formato da dinâmica sem combinar com o usuário. Em particular, esclareça:

- **Confirmado:** o professor lê cada pergunta em voz alta, e os alunos procuram a resposta nos cards que receberam.
- **Confirmado:** o aluno que acredita ter a resposta fala em voz alta; se estiver incorreta, o professor informa a resposta esperada e explica o conteúdo.
- **Confirmado:** os cards dos alunos mostram somente as respostas; as perguntas ficam com o professor.
- **Confirmado:** uma resposta pode ser distribuída a mais de um aluno, mas cada aluno recebe somente parte do conjunto de respostas.
- **Confirmado:** cada resposta aparece no máximo uma vez nos cards de cada aluno.
- **Confirmado:** o professor escolhe quantos cards cada aluno recebe; o mínimo é cinco cards por aluno.
- **Confirmado:** o sorteio considera todos os blocos do banco escolhido.
- **Confirmado:** o professor pode selecionar vários arquivos JSON, combinando seus cards na mesma atividade.
- **Confirmado:** quando houver cards suficientes no total, cada resposta do banco deve ser entregue a pelo menos um aluno.
- **Confirmado:** se o total de cards não for suficiente para cobrir todas as respostas, o programa avisa e solicita que o professor aumente a quantidade de cards por aluno; não gera uma atividade parcial.
- **Confirmado:** cada card do professor mostra a pergunta e, logo abaixo, a resposta correta.

Regra de distribuição confirmada: não repetir uma resposta no conjunto de um mesmo aluno; a mesma resposta pode ser impressa para alunos diferentes. Cobrir todas as respostas ao menos uma vez e, se faltarem cards, solicitar ao professor que aumente a quantidade por aluno.

## Impressão e acessibilidade de uso

- **Confirmado:** tamanho dos cards tipo poker, 63 × 88 mm.
- Planeje várias cartas por página A4, com linhas de corte e margens adequadas para impressoras comuns.
- Não dependa de impressão frente e verso no MVP; esse recurso exige alinhamento e deve ser uma decisão posterior.
- Garanta que textos longos caibam sem cortes, com fonte legível e quebra de linha previsível.
- Mantenha os materiais dos alunos separados visualmente do gabarito, mesmo que estejam no mesmo PDF.
- Verifique que a distribuição aleatória não revele acidentalmente as respostas no material destinado aos alunos.

## Testes esperados

Cada etapa deve incluir testes proporcionais ao que foi implementado. No mínimo, cobrir:

- JSON válido, arquivo ausente ou inválido, campos obrigatórios e cards sem pergunta/resposta.
- Entradas de quantidade inválidas, zero/negativas e pedidos acima do limite escolhido.
- Distribuição contendo somente cards elegíveis, respeitando a política de repetição e quantidades por aluno.
- Sorteio determinístico por semente injetável nos testes, sem depender de uma ordem fixa em produção.
- Geração de PDF: arquivo criado, páginas/cards esperados e tamanho de carta definido.

Testes não devem depender de acesso à internet nem de dados pessoais de alunos. Use dados fictícios.

## Roteiro de trabalho

As etapas abaixo são uma proposta, não autorização para implementá-las todas de uma vez:

1. **Definir regras do jogo:** responder às perguntas em “Decisões a confirmar” e fechar o que entra no MVP.
2. **Especificar os dados:** validar o JSON atual e documentar o esquema mínimo, sem quebrar o banco existente.
3. **Preparar a base Python:** definir a estrutura mínima, ambiente/dependências e comandos de execução e teste.
4. **Ler e validar bancos:** implementar carregamento e mensagens de erro claras; cobrir com testes.
5. **Distribuir cards:** implementar entrada de dados, seleção aleatória e validação das quantidades; cobrir regras com testes.
6. **Gerar PDF:** montar cards no tamanho aprovado, marcas de corte e gabarito no mesmo documento; testar a saída.
7. **Validar o fluxo completo:** executar uma atividade de exemplo, revisar impressão e documentar o uso para professores.

## Critério de conclusão do MVP

Um professor consegue executar o programa, escolher um banco compatível, informar os dados da turma, receber avisos compreensíveis para entradas inviáveis e gerar um único PDF imprimível com os cards previstos e o gabarito correto. As regras principais têm testes automatizados executáveis localmente.

## Próximo passo

As regras essenciais da dinâmica e o tamanho dos cards foram confirmados com o usuário. Apresente o plano de trabalho atualizado e aguarde aprovação antes de iniciar a implementação. Confirme os detalhes de paginação e impressão antes de implementar o PDF.