from crewai import Agent, Task, Crew, Process

# 1. Definição do Agente de Inteligência de Mercado
pesquisador_leads = Agent(
    role='Especialista em Prospecção Digital',
    goal='Identificar tendências de consumo e perfis de clientes interessados em {nicho} para a loja {nome_loja}',
    backstory='Você é um expert em análise de dados sociais. Sua função é mapear o que o público local de {nome_loja} está buscando e quais são as dores e desejos atuais relacionados a {contexto_novidade}.',
    verbose=True,
    allow_delegation=False
)

# 2. Definição do Agente de Engajamento (Copywriter)
copywriter_wa = Agent(
    role='Estrategista de WhatsApp Marketing',
    goal='Criar fluxos de conversas e mensagens persuasivas para grupos de WhatsApp da {nome_loja}',
    backstory='Você domina técnicas de Copywriting e Gatilhos Mentais (Escassez, Prova Social e Exclusividade). Seu objetivo é transformar a {contexto_novidade} em um evento imperdível, sem parecer spam.',
    verbose=True
)

# 3. Definição das Tarefas
tarefa_pesquisa = Task(
    description=(
        'Analise o nicho de {nicho} e identifique 3 comportamentos de compra atuais. '
        'Foque em como a {contexto_novidade} se encaixa nesses comportamentos para atrair novos clientes.'
    ),
    agent=pesquisador_leads,
    expected_output='Um relatório estratégico detalhando o público-alvo e os argumentos de venda baseados em tendências.'
)

tarefa_disparo = Task(
    description=(
        'Com base no relatório de pesquisa, crie 3 mensagens prontas para WhatsApp: '
        '1. Um Lembrete de "Vem aí" (Antecipação). '
        '2. Um Lançamento oficial com foco na {contexto_novidade}. '
        '3. Uma Promoção relâmpago para os membros do grupo. '
        'Use emojis e quebras de linha para facilitar a leitura no celular.'
    ),
    agent=copywriter_wa,
    expected_output='Os 3 modelos de mensagens estruturados e prontos para envio.'
)

# 4. Configuração da Equipe (Crew)
equipe_tracao = Crew(
    agents=[pesquisador_leads, copywriter_wa],
    tasks=[tarefa_pesquisa, tarefa_disparo],
    process=Process.sequential, # Executa a pesquisa primeiro, depois o copy
    verbose=True
)

# 5. Execução com Cenário Realista
if __name__ == "__main__":
    # Dados da simulação de "Novidades na Loja"
    inputs_da_campanha = {
        'nome_loja': 'Conecta TI & Crafts', 
        'nicho': 'Artesanato sustentável e acessórios premium',
        'contexto_novidade': 'Nova coleção de peças em Miriti e Acendedores Ecológicos "Buriti Brasa"'
    }

    print("\n" + "="*50)
    print(f"🚀 INICIANDO AGENTE DE TRAÇÃO PARA: {inputs_da_campanha['nome_loja']}")
    print("="*50 + "\n")

    resultado = equipe_tracao.kickoff(inputs=inputs_da_campanha)

    print("\n" + "="*50)
    print("✅ ESTRATÉGIA E MENSAGENS GERADAS COM SUCESSO:")
    print("="*50)
    print(resultado)