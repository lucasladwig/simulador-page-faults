from tabulate import tabulate
from alocador_de_paginas import AlocadorDePaginas


def main():
    """Inicia o simulador com base em cenários predefinidos. 
    No final permite ao usuário definir seu próprio cenário."""
    print("\nSIMULADOR DE ALOCAÇÃO DE PÁGINAS")
    print("================================================================")
    print("Todos os cenários são calculados com os seguintes parâmetros:")
    print("- Número de acessos aleatórios: 100.000")
    print("- Tempo de acesso a memória: 100ns")
    print("- Tempo de tratamento de falha de página: 8ms (8 x 10^6 ns)")

    # Instanciar alocador com valores quaisquer
    alocador = AlocadorDePaginas(16, 32)

    # CENÁRIOS PREDEFINIDOS
    cenarios = {
        # Poucos quadros, paginas em 1.5x ou 2x
        1: [64, 96, alocador.sequencia_aleatoria],
        2: [64, 96, alocador.sequencia_localizada],
        3: [64, 96, alocador.sequencia_linear],
        4: [64, 128, alocador.sequencia_aleatoria],
        5: [64, 128, alocador.sequencia_localizada],
        6: [64, 128, alocador.sequencia_linear],

        # Muitos quadros, paginas em 1.5x ou 2x
        7: [1024, 1536, alocador.sequencia_aleatoria],
        8: [1024, 1536, alocador.sequencia_localizada],
        9: [1024, 1536, alocador.sequencia_linear],
        10: [1024, 2048, alocador.sequencia_aleatoria],
        11: [1024, 2048, alocador.sequencia_localizada],
        12: [1024, 2048, alocador.sequencia_linear],
    }

    for cenario, [quadros, paginas, sequencia] in cenarios.items():
        # Pausa ausa entre cada cenário
        input("\nAperte ENTER para calcular próximo cenário: ")

        # Carregar parâmetros do cenário no alocador
        alocador.num_quadros = quadros
        alocador.max_pag_novas = paginas

        # Descrição
        print(f"\n\nCENÁRIO {cenario}")
        print(f"==================================")
        print(f"- Quadros na memória: {quadros}")
        print(f"- Páginas endereçáveis: {paginas}")
        print(f"- Tipo de sequência de acesso: {sequencia.__name__}\n")

        # Rodar algoritmos
        fifo, tempo_fifo = alocador.fifo(sequencia)
        seg_chance, tempo_seg_chance = alocador.segunda_chance(sequencia)
        relogio, tempo_relogio = alocador.relogio(sequencia)
        nru, tempo_nru = alocador.nru(sequencia)
        lru_lista, tempo_lru_lista = alocador.lru_lista(sequencia)
        nfu_contador, tempo_nfu_contador = alocador.nfu_contador(sequencia)
        envelhecimento, tempo_envelhecimento = alocador.envelhecimento(sequencia)

        # Organizar dados em linhas
        cabecalho = [
            "ALGORITMO",
            "Falhas (total)",
            "Falhas (%)",
            "Acesso médio (ms)",
            "Execução (ms)",
        ]
        resultados = [
            ["FIFO", fifo['total'], fifo['porcentagem'], fifo['acesso'], tempo_fifo],
            ["Segunda Chance", seg_chance['total'], seg_chance['porcentagem'], seg_chance['acesso'], tempo_seg_chance],
            ["Relógio", relogio['total'], relogio['porcentagem'],relogio['acesso'], tempo_relogio],
            ["NRU", nru['total'], nru['porcentagem'], nru['acesso'], tempo_nru],
            ["LRU com lista", lru_lista['total'], lru_lista['porcentagem'], lru_lista['acesso'], tempo_lru_lista],
            ["NFU com contador", nfu_contador['total'], nfu_contador['porcentagem'], nfu_contador['acesso'], tempo_nfu_contador],
            ["Envelhecimento", envelhecimento['total'], envelhecimento['porcentagem'], envelhecimento['acesso'], tempo_envelhecimento],
        ]

        # Imprimir resultados (em formato de tabela)
        print(tabulate(resultados, headers=cabecalho))


    # CENÁRIO PERSONALIZADO
    personalizar = input("\n\nDeseja personalizar um cenário? (S para SIM, qualquer outro para NÃO): ")

    if personalizar.lower() != "s":
        quit()
    
    # Descrição
    print(f"\n\nCENÁRIO PERSONALIZADO")
    print(f"=====================================")
    print(f"Insira TODOS os parâmetros abaixo:")
    pers_quadros = int(input("- Quadros na memória (16 a 1024): "))
    pers_paginas = int(input("- Páginas alocáveis (entre 1x e 4x núm. quadros): "))
    pers_acessos = int(input("- Acessos aleatórios (a partir de 1000): "))
    pers_memoria = int(input("- Tempo de acesso a memória em ns (50 a 200): "))
    pers_tratamento = int(input("- Tempo de tratamento de falha de página em ns (8 a 20 milhões): "))
    pers_sequencia = int(input("- Sequência de acesso (1 = aleatória, 2 = localizada, 3 = linear): "))

    # Instanciar alocador com valores personalizados
    pers_alocador = AlocadorDePaginas(pers_quadros, 
                                 pers_paginas,
                                 num_acessos=pers_acessos,
                                 tempo_memoria=pers_memoria,
                                 tempo_tratamento=pers_tratamento,
                                 )
    
    match pers_sequencia:
        case 1:
            seq = pers_alocador.sequencia_aleatoria
        case 2:
            seq = pers_alocador.sequencia_localizada
        case 3:
            seq = pers_alocador.sequencia_linear

    # Rodar algoritmos
    pers_fifo, tempo_pers_fifo = pers_alocador.fifo(seq)
    pers_seg_chance, tempo_pers_seg_chance = pers_alocador.segunda_chance(seq)
    pers_relogio, tempo_pers_relogio = pers_alocador.relogio(seq)
    pers_nru, tempo_pers_nru = pers_alocador.nru(seq)
    pers_lru_lista, tempo_pers_lru_lista = pers_alocador.lru_lista(seq)
    pers_nfu_contador, tempo_pers_nfu_contador = pers_alocador.nfu_contador(seq)
    pers_envelhecimento, tempo_pers_envelhecimento = pers_alocador.envelhecimento(seq)

    # Organizar dados em linhas
    cabecalho = [
        "ALGORITMO",
        "Falhas (total)",
        "Falhas (%)",
        "Acesso médio (ms)",
        "Execução (ms)",
    ]
    resultados = [
        ["FIFO", pers_fifo['total'], pers_fifo['porcentagem'], pers_fifo['acesso'], tempo_pers_fifo],
        ["Segunda Chance", pers_seg_chance['total'], pers_seg_chance['porcentagem'], pers_seg_chance['acesso'], tempo_pers_seg_chance],
        ["Relógio", pers_relogio['total'], pers_relogio['porcentagem'],pers_relogio['acesso'], tempo_pers_relogio],
        ["NRU", pers_nru['total'], pers_nru['porcentagem'], pers_nru['acesso'], tempo_pers_nru],
        ["LRU com lista", pers_lru_lista['total'], pers_lru_lista['porcentagem'], pers_lru_lista['acesso'], tempo_pers_lru_lista],
        ["NFU com contador", pers_nfu_contador['total'], pers_nfu_contador['porcentagem'], pers_nfu_contador['acesso'], tempo_pers_nfu_contador],
        ["Envelhecimento", pers_envelhecimento['total'], pers_envelhecimento['porcentagem'], pers_envelhecimento['acesso'], tempo_pers_envelhecimento],
    ]

    # Imprimir resultados (em formato de tabela)
    print("\n")
    print(tabulate(resultados, headers=cabecalho))

if __name__ == "__main__":
    main()
