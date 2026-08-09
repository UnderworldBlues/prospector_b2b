import os
import googlemaps
from langchain_core.tools import tool

@tool
def buscar_negocios_locais(termo: str, localizacao: str) -> list:
    """
    Busca negócios locais no Google Maps com base em um termo (ex: 'clínica odontológica') 
    e uma localização (ex: 'Uberlândia, MG').
    Retorna uma lista de dicionários contendo nome, endereço e website.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return "api key não encontrada no .env"
    
    gmaps = googlemaps.Client(key=api_key)
    query = f"{termo} em {localizacao}"
    
    try:
        places_result = gmaps.places(query=query)
        negocios = []
        for place in places_result.get('results', [])[:5]: 
            place_id = place['place_id']
            details = gmaps.place(place_id, fields=['name', 'formatted_address', 'website'])
            result = details.get('result', {})
            negocios.append({
                "nome": result.get("name"),
                "endereco": result.get("formatted_address"),
                "website": result.get("website", "Sem website no Maps")
            })
            
        return negocios
    
    except Exception as e:
        return [{"erro": f"Erro ao acessar API do Google: {str(e)}"}]