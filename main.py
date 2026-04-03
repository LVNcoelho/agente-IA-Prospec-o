import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# 1. Definição do Agente de Inteligência de Mercado
pesquisador_leads = Agent(
    role='Especialista em Prospecção Digital',
    goal='Identificar tendências de consumo e perfis de clientes interessados em {nicho} para a loja {nome_loja}',
    backstory='Você é um expert em análise de dados sociais e tendências locais de Castanhal e região.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 2. Definição do Agente de Engajamento (Copywriter)
copywriter_wa = Agent(
    role='Estrategista de WhatsApp Marketing',
    goal='Criar fluxos de conversas e mensagens persuasivas para os grupos da {nome_loja}',
    backstory='Você domina gatilhos mentais e sabe como engajar clientes de forma humana e autêntica.',
    verbose=True,
    llm=llm  # <--- Avisando que deve usar o Gemini
)

# 3. Definição das Tarefas
tarefa_pesquisa = Task(
    description='Analise o nicho de {nicho} e como a {contexto_novidade} se encaixa nos desejos dos clientes.',
    agent=pesquisador_leads,
    expected_output='Um relatório estratégico detalhando o público-alvo e argumentos de venda.'
)

tarefa_disparo = Task(
    description='Crie 3 modelos de mensagens para WhatsApp (Antecipação, Lançamento e Promoção) sobre a {contexto_novidade}.',
    agent=copywriter_wa,
    expected_output='Os 3 modelos de mensagens prontos para envio.'
)

# 4. Configuração da Equipe (Crew)
equipe_tracao = Crew(
    agents=[pesquisador_leads, copywriter_wa],
    tasks=[tarefa_pesquisa, tarefa_disparo],
    process=Process.sequential,
    verbose=True
)

# 5. Execução com Cenário Realista
if __name__ == "__main__":
    inputs_da_campanha = {
        'nome_loja': 'Conecta TI & Crafts', 
        'nicho': 'Artesanato em Miriti e Soluções Digitais',
        'contexto_novidade': 'Nova coleção de peças em Miriti e acendedores ecológicos Buriti Brasa'
    }

    print("\n🚀 INICIANDO AGENTE DE TRAÇÃO COM GEMINI...\n")
    resultado = equipe_tracao.kickoff(inputs=inputs_da_campanha)
    print("\n" + "="*50)
    print(resultado)