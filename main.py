from src.graph import app

def formatar_relatorio_final(resultado_final: dict):
    print("\n" + "="*50)
    print("Relatorio Final da Auditoria Digital")
    print("="*50 + "\n")
    auditoria = resultado_final.get("resultado_auditoria", [])
    if not auditoria:
        print("Nenhum dado retornado da auditoria.")
        return
    for index, negocio in enumerate(auditoria, start=1):
        print(f"[{index}] {negocio.get('nome_negocio')}")
        print(f"    Endereço: {negocio.get('endereco')}")
        print(f"    Site no Maps: {negocio.get('website_maps')}")
        print(f"    Análise Digital: {negocio.get('analise_presenca')}")
        print("-" * 50)

def main():
    print("Iniciando busca...\n")
    inputs_iniciais = {
        "termo_busca": "restaurante",
        "localizacao": "xique xique, bahia"
    }
    print(f"Buscando por: {inputs_iniciais['termo_busca']} em {inputs_iniciais['localizacao']}\n")
    
    try:
        resultado = app.invoke(inputs_iniciais)
        formatar_relatorio_final(resultado)
    except Exception as e:
         print(f"\nerro durante a execução do grafo: {e}")

if __name__ == "__main__":
    main()