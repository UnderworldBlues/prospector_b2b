# Prospector B2B multi-agente

Este projeto é um sistema autônomo baseado em inteligência artificial para prospecção de vendas B2B e geração de leads. Ele utiliza o ecossistema LangChain/LangGraph para orquestrar agentes que buscam negócios locais e avaliam a presença digital de cada um.

## Arquitetura dos Agentes

O fluxo de projeto foi construído usando uma arquitetura de stateGraph, operando com dois agentes principais:

1. **Agente Prospector (Node 1):** 
   - Recebe um nicho e uma localização (ex: "Agência de Marketing em Uberlândia").
   - Utiliza a API do **Google Maps** para encontrar os negócios na região, retornando nome, endereço físico e URL.
2. **Agente Auditor Digital (Node 2):**
   - Recebe a lista mapeada pelo Prospector.
   - Utiliza a API do **Tavily** para pesquisar na web informações complementares sobre a empresa (Instagram, LinkedIn, site oficial, etc).
   - O modelo processa o conteúdo das páginas e gera uma análise qualitativa de 2 a 3 frases sobre o quão forte é a presença digital daquele negócio.

## Tecnologias Utilizadas

- **Python 3.14**
- [LangGraph](https://langchain-ai.github.io/langgraph/) & [LangChain](https://python.langchain.com/)
- Google Gemini (via `langchain-google-genai`)
- Tavily Search API
- Google Maps API (`googlemaps`)

## Configurar e Rodar o Projeto

### 1. Clonar e preparar o ambiente
```bash
# Clone o repositório
git clone [https://github.com/seu-usuario/prospector-b2b.git](https://github.com/seu-usuario/prospector-b2b.git)
cd prospector-b2b
# Crie e ative um ambiente virtual
python -m venv venv
venv\Scripts\activate
# Instale as dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto e preencha-o com suas chaves de API:

```env
AI_API_KEY="sua_chave_aqui"
GOOGLE_MAPS_API_KEY="sua_chave_aqui"
TAVILY_API_KEY="sua_chave_aqui"

```

### 3. Executar o fluxo

Edite o arquivo `main.py` para definir o termo de busca e a localização que deseja analisar. Em seguida, execute:

```bash

python main.py

```