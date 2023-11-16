import random


class AlocadorDePaginas:
    """Simula a alocação e liberação de páginas na memória de acordo com diferentes algoritmos, apresentando dados de desempenho de cada algoritmo. Todas as simulações presumem que todos os quadros estejam livres no início do teste."""

    def __init__(self,
                 num_quadros: int,  # Quadros disponíveis na memória física
                 max_pag_novas: int,  # Máximo de páginas enderecáveis por processo
                 qtd_acessos: int = 100000,  # Quantidade de acessos aleatórios para teste
                 tam_quadro: int = 128,  # Tamanho de cada quadro (bytes)
                 tempo_memoria: int = 100,  # Tempo de acesso a memória (ns)
                 tempo_tratamento: int = 8e6,  # Tempo de tratamento de falhas (ns)
                 ) -> None:

        self.__num_quadros = num_quadros
        self.__max_pag_novas = max_pag_novas
        self.__qtd_acessos = qtd_acessos
        self.__tam_quadro = tam_quadro
        self.__tempo_memoria = tempo_memoria
        self.__tempo_tratamento = tempo_tratamento

    # GETTERS/SETTERS
    @property
    def qtd_acessos(self) -> int:
        return self.__qtd_acessos

    # ALGORITMOS DE SUBSTITUIÇÃO
    def fifo(self) -> dict:
        """Algoritmo de fila simples, onde a página referenciada mais antiga é removida para entrar uma nova."""
        fila = []
        contador_falhas = 0

        # Percorre a sequência de acessos
        for pag_nova in self.__gerar_sequencia_acessos():
            if pag_nova not in fila:
                contador_falhas += 1
                # Se ainda há espaço, adicionar nova ao final
                if len(fila) < self.__num_quadros:
                    fila.append(pag_nova)
                # Se não houver espaço, remover primeiro e adicionar nova ao final
                else:
                    fila.pop(0)
                    fila.append(pag_nova)

        return self.__calcular_metricas_falhas(contador_falhas)

    def segunda_chance(self):
        """Algoritmo de fila com segunda chance, caso a página tenha sido referenciada no último ciclo ela volta ao final da fila ao invés de ser excluída. Utiliza 1 bit para Referenciado (R)."""
        fila = []  # Cada elemento é uma lista [página, bit_R]
        contador_falhas = 0

        # Percorre a sequência de acessos
        for pag_nova in self.__gerar_sequencia_acessos():
            # Verifica se a página já está na fila
            pag_encontrada = False
            for i, [pag_atual, _] in enumerate(fila):
                if pag_atual == pag_nova:
                    # Atualiza página atual com o bit_R = 1
                    fila[i][1] = 1
                    pag_encontrada = True
                    break

            if not pag_encontrada:
                contador_falhas += 1
                # Se ainda há espaço, adiciona a página com o bit_R = 1
                if len(fila) < self.__num_quadros:
                    fila.append([pag_nova, 1])
                else:
                    # Percorre fila até substituir alguma página
                    while True:
                        # Verifica o bit_R do primeiro elemento
                        pag_atual, bit_R = fila.pop(0)
                        if bit_R:
                            # Se o bit_R == 1, modifica o bit para 0 e coloca no final
                            fila.append([pag_atual, 0])
                        else:
                            # Se o bit_R == 0, coloca página nova no final e encerra
                            fila.append([pag_nova, 1])
                            break

        return self.__calcular_metricas_falhas(contador_falhas)

    def relogio(self):
        """Algoritmo de segunda chance com relógio, uma variante com estrutura de dados circular ao invés de fila simples."""
        relogio = []  # Cada elemento é uma lista [página, bit_R]
        ponteiro = 0  # Ponteiro que se move circularmente pela relogio
        contador_falhas = 0

        # Percorre a sequência de acessos
        for pag_nova in self.__gerar_sequencia_acessos():
            # Verifica se a página já está na relogio
            pag_encontrada = False
            for i, [pag_atual, _] in enumerate(relogio):
                if pag_atual == pag_nova:
                    # Atualiza página atual com o bit_R = 1
                    relogio[i][1] = 1
                    pag_encontrada = True
                    break

            # Se a página não está no relogio, é uma falha de página
            if not pag_encontrada:
                contador_falhas += 1
                # Se ainda há espaço, adiciona a página com o bit_R = 1
                if len(relogio) < self.__num_quadros:
                    relogio.append([pag_nova, 1])
                else:
                    # Percorre relógio circularmente até substituir alguma página
                    while True:
                        pag_atual, bit_R = relogio[ponteiro]
                        if bit_R:
                            # Atualiza página apontada com bit_R = 0 e avança o ponteiro
                            relogio[ponteiro][1] = 0
                            ponteiro = (ponteiro + 1) % self.__num_quadros
                        else:
                            # Substitui por nova página com bit_R = 1 e avança ponteiro
                            relogio[ponteiro] = [pag_nova, 1]
                            ponteiro = (ponteiro + 1) % self.__num_quadros
                            break

        return self.__calcular_metricas_falhas(contador_falhas)

    def nru(self):
        """Algoritmo 'não usado recentemente', que prioriza remover páginas não referenciadas, mesmo que modificadas. Define 4 classes com base em 2 bits: Referenciado (R) e Modificado (M), e remove aqueles de menor classe. Bit Presente/Ausente é usado para verificar se está na memória."""
        tabela_paginas = []  # Cada elemento é uma lista [página, bit_PA, bit_R, bit_M]
        contador_falhas = 0

        # Percorre a sequência de acessos
        for pag_nova in self.__gerar_sequencia_acessos():
            # Verifica se a página já está na relogio
            pag_encontrada = False
            for i, [pag_atual, bit_PA, _, _] in enumerate(tabela_paginas):
                if pag_atual == pag_nova:
                    # Atualiza página atual com o bit_PA = 1
                    tabela_paginas[i][1] = 1
                    pag_encontrada = True
                    break

            # Verifica se a página já está na lista
            if not pag_encontrada:
                contador_falhas += 1
                # Se ainda há espaço, adiciona a página com bit_PA, bit_R e bit_M = 1
                if len(tabela_paginas) < self.__num_quadros:
                    # Simula leitura e escrita
                    tabela_paginas.append([pag_nova, 1, 1, 1])
                else:
                    # Categoriza as páginas
                    classes = {0: [], 1: [], 2: [], 3: []}
                    for p, r, m in tabela_paginas:
                        classe = r * 2 + m  # Calcula a classe com base nos bits R e M
                        classes[classe].append(p)

                    # Encontra a classe mais baixa não vazia
                    for classe in range(4):
                        if classes[classe]:
                            pagina_substituir = random.choice(classes[classe])
                            break

                    # Substitui a página
                    tabela_paginas = [
                        (p, r, m) for p, r, m in tabela_paginas if p != pagina_substituir]
                    # Assume leitura e escrita para simplificar
                    tabela_paginas.append((pag_nova, 1, 1))

            # Aqui você pode adicionar lógica para atualizar os R e M bits, dependendo do uso

        return contador_falhas

    def nru2(self):
        """Algoritmo 'não usado recentemente', que prioriza remover páginas não referenciadas, mesmo que modificadas. Define 4 classes com base em 2 bits: Referenciado (R) e Modificado (M), e remove aqueles de menor classe. Bit Presente/Ausente é usado para verificar se está na memória."""
        # Inicializa a tabela de páginas do processo
        # Página do processo é o índice de cada linha, e cada linha é uma lista [bit_PA, bit_R, bit_M]
        tabela_paginas = [[0, 0, 0] for _ in range(self.__max_pag_novas)]
        contador_falhas = 0
        quadros_disponiveis = self.__num_quadros
        contador_reset = 250  # Número de acessos até que todos bits R sejam zerados

        # Percorre a sequência de acessos
        for pag_nova in self.__gerar_sequencia_acessos():
            
            # Verifica bit_PA da página referenciada
            if tabela_paginas[pag_nova][0]:
                # Atualiza página acessada com bit_R = 1
                tabela_paginas[pag_nova][1] = 1

            # Verifica se a página já está na lista
            else:
                contador_falhas += 1
                # Se ainda há espaço, adiciona a página com bit_PA, bit_R e bit_M = 1
                if quadros_disponiveis > 0:
                    quadros_disponiveis -= 1
                    tabela_paginas[pag_nova] = [1, 1, 1]
                else:
                    # Categoriza as páginas
                    classes = {0: [], 1: [], 2: [], 3: []}
                    for p, r, m in tabela_paginas:
                        classe = r * 2 + m  # Calcula a classe com base nos bits R e M
                        classes[classe].append(p)

                    # Encontra a classe mais baixa não vazia
                    for classe in range(4):
                        if classes[classe]:
                            pagina_substituir = random.choice(classes[classe])
                            break

                    # Substitui a página
                    tabela_paginas = [
                        (p, r, m) for p, r, m in tabela_paginas if p != pagina_substituir]
                    # Assume leitura e escrita para simplificar
                    tabela_paginas.append((pag_nova, 1, 1))

            # Aqui você pode adicionar lógica para atualizar os R e M bits, dependendo do uso
            contador_reset -= 1
            if contador_reset == 0:
                for linha in tabela_paginas:
                    linha[1] = 0
                contador_reset = 250

        return contador_falhas

    def lru(self, page_sequence):
        # LRU implementation
        pass

    # MÉTODOS AUXILIARES
    def __gerar_sequencia_acessos(self) -> int:
        """Gera uma sequência pseudoaleatória de páginas referenciadas. A sequência gerada é sempre a mesma para comparação de algoritmos."""
        random.seed(12345)  # Garante que a sequência de acessos seja sempre a mesma
        for _ in range(self.__qtd_acessos):
            # Gera sequência um a um ao invés de guardar tudo em memória
            yield random.randint(0, self.__max_pag_novas-1)

    def __calcular_metricas_falhas(self, falhas: int) -> dict:
        """Calcula as métricas relevantes para os algoritmos de substituição de páginas."""

        taxa_falhas = falhas/self.__qtd_acessos
        tempo_medio_acesso = (1 - taxa_falhas) * self.__tempo_memoria + \
            (taxa_falhas * self.__tempo_tratamento)

        metricas_falhas = {
            'total': falhas,
            'taxa': taxa_falhas,
            'porcentagem': round(taxa_falhas*100, 4),
            'tempo_medio': tempo_medio_acesso,
        }
        return metricas_falhas
