from typing import TypedDict, List

class AgentState(TypedDict):
    termo_busca: str
    localizacao: str    
    lista_negocios: List[dict]      #agente 1
    resultado_auditoria: List[dict]  #agente 2 