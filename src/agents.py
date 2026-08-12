import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import AgentState
from src.tools.google_places import buscar_negocios_locais
from src.tools.web_search import buscar_informacoes_web
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=os.getenv("AI_API_KEY")
)

llm_com_maps = llm.bind_tools([buscar_negocios_locais])
llm_com_web = llm.bind_tools([buscar_informacoes_web])

# agente 1
def prospector_node(state: AgentState):
    """Nó do Agente 1: Busca negócios locais no Google Maps."""
    print("[Prospector] Iniciando busca no mapa...")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um especialista em prospecção de vendas B2B. Use a ferramenta do Google Maps para encontrar negócios com base no termo e localização informados."),
        ("user", "Encontre negócios usando o termo '{termo}' em '{localizacao}' e retorne a lista de resultados chamando a ferramenta apropriada.")
    ])

    chain = prompt | llm_com_maps
    resposta = chain.invoke({
        "termo": state["termo_busca"],
        "localizacao": state["localizacao"]
    })
    lista_encontrada = []
    if resposta.tool_calls:
        args = resposta.tool_calls[0]["args"]
        lista_encontrada = buscar_negocios_locais.invoke(args)
    
    print(f"[Prospector] {len(lista_encontrada)} negócios encontrados.")

    return {"lista_negocios": lista_encontrada}


# agente 2
def auditor_node(state: AgentState):
    """Nó do Agente 2: Analisa a presença digital dos negócios."""
    print("[Auditor] Iniciando auditoria digital...")
    negocios = state["lista_negocios"]
    resultados = []
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Você é um especialista em Marketing Digital. 
        Vou te dar o nome de um negócio e a cidade dele. 
        Use a ferramenta de busca web para descobrir se ele tem site, Instagram, etc.
        Com base no que encontrar, escreva um resumo crítico de 2 a 3 frases sobre a presença digital do negócio. 
        Diga se a presença parece forte, fraca, ou inexistente."""),
        ("user", "Avalie a presença digital de: {nome_negocio} em {cidade}. O site cadastrado no maps é: {site}")
    ])
    
    chain = prompt | llm_com_web
    
    for negocio in negocios:
        nome = negocio.get("nome", "Desconhecido")
        site = negocio.get("website", "Não possui site no Maps")
        cidade = state["localizacao"]
        
        print(f"[Auditor] Pesquisando: {nome}...")

        resposta_pesquisa = chain.invoke({
            "nome_negocio": nome,
            "cidade": cidade,
            "site": site
        })
        dados_web = ""
        if resposta_pesquisa.tool_calls:
            args = resposta_pesquisa.tool_calls[0]["args"]
            dados_web = buscar_informacoes_web.invoke(args)

        prompt_final = ChatPromptTemplate.from_messages([
            ("system", "Você é um especialista em marketing. Baseado nos dados abaixo, resuma a presença digital do negócio em 2 frases."),
            ("user", "Negócio: {nome}\nDados encontrados na web:\n{dados}\n\nSua Análise:")
        ])
        
        chain_final = prompt_final | llm
        analise = chain_final.invoke({"nome": nome, "dados": dados_web})
        resultados.append({
            "nome_negocio": nome,
            "endereco": negocio.get("endereco"),
            "website_maps": site,
            "analise_presenca": analise.content
        })
    print("[Auditor] Auditoria concluída.")
    
    return {"resultado_auditoria": resultados}