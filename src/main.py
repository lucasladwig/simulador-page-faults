from alocador_de_paginas import AlocadorDePaginas


def main():
    """Inicia o simulador com base em cenários predefinidos, e no final permite ao usuário inserir outros parâmetros."""
    print("\n-----SIMULADOR DE ALOCAÇÃO DE PÁGINAS-----")
    print("\nOBS: Todos os cenários são calculados com 100.000 acessos aleatórios")
    input("\nAperte enter para calcular próximo cenário: ")

    # CENÁRIO 01
    # Descrição
    print("\nCENÁRIO 01: Poucas páginas, poucos quadros")
    print("- Número de quadros na memória física: 64")
    print("- Máximo de páginas endereçáveis: 128")
    print("- Quantidade de acessos aleatórios: 100.000")

    # Cálculos
    alocador_01 = AlocadorDePaginas(64, 128)
    fifo_01 = alocador_01.fifo()
    seg_chance_01 = alocador_01.segunda_chance()
    relogio_01 = alocador_01.relogio()

    # Resultados
    print("\nRESULTADOS DOS ALGORITMOS: ")
    print("\nFIFO:")
    print(f"-Falhas totais: {fifo_01['total']}")
    print(f"-Percentual de falhas: {fifo_01['porcentagem']}%")
    print(f"-Tempo médio de acesso à memória: {fifo_01['tempo_medio']}ns")
    
    print("\nSegunda Chance:")
    print(f"-Falhas totais: {seg_chance_01['total']}")
    print(f"-Percentual de falhas: {seg_chance_01['porcentagem']}%")
    print(f"-Tempo médio de acesso à memória: {seg_chance_01['tempo_medio']}ns")

    print("\nRelógio:")
    print(f"-Falhas totais: {relogio_01['total']}")
    print(f"-Percentual de falhas: {relogio_01['porcentagem']}%")
    print(f"-Tempo médio de acesso à memória: {relogio_01['tempo_medio']}ns")


    # CENÁRIO PERSONALIZADO
    # Entradas do usuário
    # print("\nCENÁRIO PERSONALIZADO: Insira os valores: ")
    # num_quadros = int(input("- Número de quadros na memória física: "))
    # max_paginas = int(input("- Máximo de páginas endereçáveis: "))
    # tam_quadro = int(input("- Tamanho do quadro (Bytes): "))
    # qtd_acessos = int(input("- Número de acessos aleatórios: "))


if __name__ == "__main__":
    main()
