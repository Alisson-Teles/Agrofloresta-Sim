import numpy as np

# Função para calcular a área total do sistema
def calcular_area_total(N, A_p):
    return N * A_p

# Função para calcular a densidade de plantio
def calcular_densidade_plantio(P, A):
    return P / A

# Função para calcular a cobertura vegetal média
def calcular_cobertura_vegetal_media(A_c, N):
    return np.sum(A_c) / N

# Função para calcular o rendimento médio das culturas
def calcular_rendimento_medio(H, A):
    return np.sum(H) / A

# Função para calcular a taxa de regeneração do sistema
def calcular_taxa_regeneracao(A_n, A):
    return (A_n - A) / A

# Função para simular o sistema de agrofloresta
def simular_agrofloresta(N, A_p, P, S, A_c, H, A_n):
    # Área total
    A = calcular_area_total(N, A_p)
    
    # Densidade de plantio
    D = calcular_densidade_plantio(P, A)
    
    # Cobertura vegetal média
    C = calcular_cobertura_vegetal_media(A_c, N)
    
    # Rendimento médio das culturas
    Y = calcular_rendimento_medio(H, A)
    
    # Taxa de regeneração do sistema
    R = calcular_taxa_regeneracao(A_n, A)
    
    return {
        "Área Total (ha)": A,
        "Densidade de Plantio (plantas/ha)": D,
        "Cobertura Vegetal Média (%)": C,
        "Rendimento Médio (ton/ha)": Y,
        "Taxa de Regeneração (%)": R
    }

# Função para receber as entradas do usuário
def obter_dados_usuario():
    N = int(input("Número de parcelas: "))
    A_p = float(input("Área por parcela (em hectares): "))
    P = int(input("Número total de plantas: "))
    S = float(input("Espaçamento entre plantas (em metros): "))
    
    A_c = []
    for i in range(N):
        A_c.append(float(input(f"Cobertura vegetal da parcela {i+1} (em %): ")))
    A_c = np.array(A_c)
    
    H = []
    for i in range(N):
        H.append(float(input(f"Colheita da parcela {i+1} (em toneladas): ")))
    H = np.array(H)
    
    A_n = float(input("Área total regenerada após um tempo (em hectares): "))
    
    return N, A_p, P, S, A_c, H, A_n

# Execução do programa
def main():
    N, A_p, P, S, A_c, H, A_n = obter_dados_usuario()
    resultado = simular_agrofloresta(N, A_p, P, S, A_c, H, A_n)
    
    print("\nResultados da Simulação:")
    for chave, valor in resultado.items():
        print(f"{chave}: {valor:.2f}")

if __name__ == "__main__":
    main()