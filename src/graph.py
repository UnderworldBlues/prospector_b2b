# src/graph.py
from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.agents import prospector_node, auditor_node

# Inicializa o grafo de estado
workflow = StateGraph(AgentState)
# Adiciona os nodes do grafo
workflow.add_node("prospector", prospector_node)
workflow.add_node("auditor", auditor_node)
# Define as arestas
workflow.add_edge(START, "prospector")
# O Prospector termina e envia o estado diretamente para o auditor
workflow.add_edge("prospector", "auditor")
# O auditor termina a análise e finaliza o processo
workflow.add_edge("auditor", END)
# Compila o grafo
app = workflow.compile()