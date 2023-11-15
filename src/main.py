from alocador_de_paginas import AlocadorDePaginas

def main():
    """Inicia o simulador com base nos inputs do usuário (ou valores padrão)."""
    
    # Início
    print("=== SIMULADOR DE ALOCAÇÃO DE PÁGINAS ===")
    
    # Cenário 01
    print("\nCENÁRIO 01: Popoucas páginas ")
    print("Insira os parâmetros conforme forem pedidos, ou deixe em branco para valores padrão.")
    
    num_quadros = int(input("- Número de quadros na memória física: "))
    tam_quadro = int(input("- Tamanho do quadro em Bytes: "))
    max_paginas = int(input("- Máximo de páginas endereçáveis: "))

    page_sequence = list(map(int, input("Enter page sequence: ").split()))

    allocator = AlocadorDePaginas(num_quadros, tam_quadro, max_paginas)
    for algo in ['FIFO', 'Second-Chance', 'NRU', 'LRU', 'Clock']:
        print(f"Simulating {algo}:")
        allocator.simulate(page_sequence, algo)
        # Display statistics


if __name__ == "__main__":
    main()
