import os
from langchain_core.tools import tool
from tavily import TavilyClient

@tool
def buscar_informacoes_web(query: str) -> str:
    """
    Pesquisa na web por informações de um negócio para avaliar sua presença digital.
    O input deve ser uma string de busca bem formulada (ex: 'Nome do Negócio cidade site oficial Instagram').
    Retorna os links encontrados (como site, LinkedIn, Instagram) e um resumo do conteúdo das páginas.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "api key não encontrada no .env"
    
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(
            query=query, 
            search_depth="basic", 
            max_results=3
        )
        
        resultados = []
        for result in response.get("results", []):
            resultados.append(
                f"Título: {result['title']}\n"
                f"URL: {result['url']}\n"
                f"Conteúdo Extraído: {result['content']}\n"
            )
        if not resultados:
            return "Nenhuma informação relevante ou presença digital encontrada na web para esta busca."
                    
        return "\n---\n".join(resultados)
        
    except Exception as e:
        return [{"erro": f"Erro na busca web: {str(e)}"}]