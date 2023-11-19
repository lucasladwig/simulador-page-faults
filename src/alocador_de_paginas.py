import random
import time
import math


class AlocadorDePaginas:
    """Simula a alocação e liberação de páginas na memória de acordo com diferentes algoritmos, apresentando dados de desempenho de cada algoritmo. Todas as simulações presumem que todos os quadros estejam livres no início do teste."""

    def __init__(self,
                 num_quadros: int,
                 max_pag_novas: int,
                 num_acessos: int = 100_000,
                 tempo_memoria: int = 100,
                 tempo_tratamento: int = 8e6,
                 ) -> None:
        # Quadros disponíveis na memória física
        self.__num_quadros = num_quadros

        # Máximo de páginas enderecáveis por processo
        self.__max_pag_novas = max_pag_novas

        # Número de acessos aleatórios para teste
        self.__num_acessos = num_acessos

        # Tempo de acesso a memória (ns)
        self.__tempo_memoria = tempo_memoria

        # Tempo de tratamento de falhas (ns)
        self.__tempo_tratamento = tempo_tratamento


    # GETTERS/SETTERS
    @property
    def num_quadros(self) -> int:
        return self.__num_quadros

    @num_quadros.setter
    def num_quadros(self, num_quadros: int) -> None:
        self.__num_quadros = num_quadros

    @property
    def max_pag_novas(self) -> int:
        return self.__max_pag_novas

    @max_pag_novas.setter
    def max_pag_novas(self, max_pag_novas: int) -> None:
        self.__max_pag_novas = max_pag_novas

    @property
    def num_acessos(self) -> int:
        return self.__num_acessos

    @num_acessos.setter
    def num_acessos(self, num_acessos: int) -> None:
        self.__num_acessos = num_acessos

    @property
    def tempo_memoria(self) -> int:
        return self.__tempo_memoria

    @tempo_memoria.setter
    def tempo_memoria(self, tempo_memoria: int) -> None:
        self.__tempo_memoria = tempo_memoria

    @property
    def tempo_tratamento(self) -> int:
        return self.__tempo_tratamento

    @tempo_tratamento.setter
    def tempo_tratamento(self, tempo_tratamento: int) -> None:
        self.__tempo_tratamento = tempo_tratamento


    # DECORADORES
    def medir_tempo(algoritmo):
        """Mede o tempo de execução da função passada como argumento, além do próprio resultado da função executada.
        Utilizada como decorador @medir_tempo, devendo ser utilizado na definição de cada função desejada."""
        def wrapper(*args, **kwargs):
            # Tempos em segundos
            inicio = time.time()
            metricas = algoritmo(*args, **kwargs)  # Função a ser executada
            final = time.time()

            # Converte para ms com 3 casas decimais
            tempo_execucao_ms = round(((final - inicio) * 1000), 3)
            return metricas, tempo_execucao_ms
        return wrapper


    # ALGORITMOS DE SUBSTITUIÇÃO
    @medir_tempo
    def fifo(self, sequencia) -> dict:
        """Algoritmo de fila simples, onde a página referenciada mais antiga é removida para entrar uma nova."""
        fila = []
        contador_falhas = 0

        # Percorre a sequência de páginas referenciadas
        for pag_nova in sequencia():
            # Se página não está na fila
            if pag_nova not in fila:
                contador_falhas += 1
                # Se ainda há espaço, adicionar nova ao final
                if len(fila) < self.__num_quadros:
                    fila.append(pag_nova)
                # Se não houver espaço, remover primeiro e adicionar nova ao final
                else:
                    fila.pop(0)
                    fila.append(pag_nova)

        return self.__calcular_metricas(contador_falhas)

    @medir_tempo
    def segunda_chance(self, sequencia) -> dict:
        """Algoritmo de fila com segunda chance. 
        Utiliza um bit de referência para controlar se a página foi acessada no último ciclo.
        Caso a página tenha sido acessada no último ciclo, ela volta ao final da fila ao invés de ser excluída."""
        fila = []  # Cada elemento é uma lista [página, bit_R]
        contador_falhas = 0

        # Percorre a sequência de páginas referenciadas
        for pag_nova in sequencia():
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

        return self.__calcular_metricas(contador_falhas)

    @medir_tempo
    def relogio(self, sequencia) -> dict:
        """Algoritmo de segunda chance, implementado com uma fila circular (ou 'relógio') para melhorar desempenho. 
        Utiliza um bit de referência para controlar se a página foi acessada no último ciclo.
        Caso a página tenha sido acessada no último ciclo, ela volta ao final da fila ao invés de ser excluída."""
        relogio = []  # Cada elemento é uma lista [página, bit_R]
        ponteiro = 0  # Ponteiro que se move circularmente pela relogio
        contador_falhas = 0

        # Percorre a sequência de páginas referenciadas
        for pag_nova in sequencia():
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

        return self.__calcular_metricas(contador_falhas)

    @medir_tempo
    def nru(self, sequencia) -> dict:
        """Algoritmo 'não usado recentemente', que prioriza remover páginas não referenciadas, mesmo que modificadas. 
        Define 4 classes com base em 2 bits: referenciado (R) e modificado (M), e remove aqueles de menor classe. 
        Bit Presente/Ausente é usado para verificar se está na memória."""
        # Inicializa a tabela com uma linha para cada página do processo
        # O índice da linha equivale ao número da página
        # Cada linha contém uma lista de bits [bit_PA, bit_R, bit_M]
        tabela = [[0, 0, 0] for _ in range(self.__max_pag_novas)]
        quadros_disponiveis = self.__num_quadros
        contador_falhas = 0

        # Simula interrupção de clock com base no numero de quadros (número de acessos para atualizar contadores)
        faixa_aleatoria = [5, 25]  # ou [25, 250]
        contador_reset = random.randint(*faixa_aleatoria)

        # Percorre a sequência de páginas referenciadas
        for pag_nova in sequencia():

            # Se página referenciada está carregada na memória (bit_PA = 1)
            if tabela[pag_nova][0]:
                # Atualiza página com bit_R = 1 e bit_M = 0 ou 1 (aleatório)
                tabela[pag_nova][1] = 1
                tabela[pag_nova][2] = random.randint(0, 1)

            # Caso página não esteja carregada na memória
            else:
                contador_falhas += 1

                # Se ainda há espaço, adiciona a página com bit_PA, bit_R e bit_M = 0 ou 1 (aleatório)
                if quadros_disponiveis > 0:
                    quadros_disponiveis -= 1
                    tabela[pag_nova] = [1, 1, 0]
                else:
                    # Categoriza as páginas em classes
                    classes = {0: [], 1: [], 2: [], 3: []}

                    # Percorre tabela de páginas pelo índice
                    for pag in range(len(tabela)):
                        # Verifica se a página está carregada na memória
                        if tabela[pag][0]:
                            # Determina classe com base nos bits R e M e adiciona na classe adequada
                            classe_pag = tabela[pag][1] * 2 + tabela[pag][2]
                            classes[classe_pag].append(pag)

                    # Encontra a classe mais baixa não vazia
                    for classe in range(4):
                        if classes[classe]:
                            pag_a_remover = random.choice(classes[classe])
                            break

                    # Zera todos os bits da página removida e incrementa quadros disponíves
                    tabela[pag_a_remover] = [0, 0, 0]
                    quadros_disponiveis += 1

                    # Carrega nova página na memória com bit_PA e bit_R = 1, e bit_M = 0 ou 1, e decrementa quadros disponíveis
                    tabela[pag_nova] = [1, 1, random.randint(0, 1)]
                    quadros_disponiveis -= 1

            # Simula "reset" a cada n ciclos (aleatório)
            contador_reset -= 1
            if contador_reset == 0:
                # Atualiza todos bit_R para 0
                for linha in tabela:
                    linha[1] = 0
                # Reinicia contador de reset com outro valor aleatório
                contador_reset = random.randint(*faixa_aleatoria)

        return self.__calcular_metricas(contador_falhas)

    @medir_tempo
    def lru_lista(self, sequencia) -> dict:
        """Algoritmo 'menos usado recentemente' com lista ordenada das páginas carregadas em memória. 
        Páginas utilizadas mais recentemente ficam no final da lista ('invertida' para melhorar desempenho).
        Quando ocorre um page fault, remove sempre a última página da lista."""
        # Lista de páginas carregadas: índices iniciais são os usados menos recentemente
        paginas_carregadas = []
        contador_falhas = 0

        # Percorre a sequência de páginas referenciadas
        for pagina in sequencia():
            # Se a página não estiver na lista
            if pagina not in paginas_carregadas:
                contador_falhas += 1
                # Se a lista de páginas estiver cheia, remove primeira pagina
                if len(paginas_carregadas) >= self.__num_quadros:
                    paginas_carregadas.pop(0)
                # Insere página no final da lista
                paginas_carregadas.append(pagina)
            # Se página for encontrada, move-a para o final da lista
            else:
                paginas_carregadas.remove(pagina)
                paginas_carregadas.append(pagina)

        return self.__calcular_metricas(contador_falhas)

    @medir_tempo
    def nfu_contador(self, sequencia) -> dict:
        """Algoritmo 'não usado frequentemente', que prioriza remover páginas menos referenciadas. 
        Mantém um contador de acessos para cada página, incrementando-o com o valor do bit de referência a cada interrupção de clock.
        A interrupção de clock é simulada como um pequeno número aleatório de referências de página (sequência de acessos). 
        Em caso de falha de página, remove aleatoriamente uma página entre as de menor contador."""
        # Inicializa a tabela com uma linha para cada página do processo
        # O índice da linha equivale ao número da página
        # Cada linha contém uma lista de bits [bit_PA, bit_R, contador]
        tabela = [[0, 0, 0] for _ in range(self.__max_pag_novas)]
        quadros_disponiveis = self.__num_quadros
        contador_falhas = 0

        # Simula interrupção de clock com base no numero de quadros (número de acessos para atualizar contadores)
        faixa_aleatoria = [5, 25]
        contador_clock = random.randint(*faixa_aleatoria)

        # Percorre a sequência de páginas referenciadas
        for pag_nova in sequencia():

            # Se página referenciada está carregada na memória (bit_PA = 1)
            if tabela[pag_nova][0]:
                tabela[pag_nova][1] = 1  # bit_R = 1

            # Caso página não esteja carregada na memória
            else:
                contador_falhas += 1

                # Se ainda há espaço, adiciona a página com bit_PA = 1 e bit_R = 0 (mantém contador)
                if quadros_disponiveis > 0:
                    quadros_disponiveis -= 1
                    tabela[pag_nova][0] = 1
                    tabela[pag_nova][1] = 0
                else:
                    # Encontra menor valor de contador para as paginas carregadas em memória
                    min_contador = math.inf
                    for linha in tabela:
                        if linha[0] == 1 and linha[2] < min_contador:
                            min_contador = linha[2]

                    # Percorre a tabela pelos índices (páginas) e separa aqueles de menor contador
                    menores_contadores = [pag for pag in range(len(tabela))
                                          if tabela[pag][0] == 1 and tabela[pag][2] == min_contador]

                    # Exclui aleatoriamente uma página entre os de menor contador (mantém contador)
                    pag_a_remover = random.choice(menores_contadores)
                    tabela[pag_a_remover][0] = 0
                    tabela[pag_a_remover][1] = 0
                    quadros_disponiveis += 1

                    # Carrega nova página na memória com bit_PA = 1 e bit_R = 0 (mantém contador)
                    quadros_disponiveis -= 1
                    tabela[pag_nova][0] = 1
                    tabela[pag_nova][1] = 0

            # Simula interrupção de clock a cada n ciclos (aleatório)
            contador_clock -= 1
            if contador_clock == 0:
                # Incrementa contador com bit_R e atualiza bit_R para 0
                for linha in tabela:
                    linha[2] += linha[1]
                    linha[1] = 0
                # Reinicia contador de clock com outro valor aleatório
                contador_clock = random.randint(*faixa_aleatoria)

        return self.__calcular_metricas(contador_falhas)

    @medir_tempo
    def envelhecimento(self, sequencia):
        """Algoritmo 'não usado frequentemente' com envelhecimento, priorizando remover páginas menos referenciadas.
        Mantém um contador de acessos para cada página, incrementando-o a cada interrupção de clock (com o valor do bit_R).
        Diminui contadores ao longo do tempo para dar chanca de "renovar" as páginas a serem substituidas. 
        A interrupção de clock e simulada como um pequeno número aleatório de referências de página (sequência de acessos). 
        Em caso de falha de página, remove aleatoriamente uma página entre as de menor contador."""
        # Inicializa a tabela com uma linha para cada página do processo
        # O índice da linha equivale ao número da página
        # Cada linha contém uma lista de bits [bit_PA, bit_R, contador(binario)]
        tabela = [[0, 0, 0] for _ in range(self.__max_pag_novas)]
        quadros_disponiveis = self.__num_quadros
        contador_falhas = 0

        # Simula interrupção de clock com base no numero de quadros (número de acessos para atualizar contadores)
        faixa_aleatoria = [5, 25]
        contador_clock = random.randint(*faixa_aleatoria)

        # Percorre a sequência de páginas referenciadas
        for pag_nova in sequencia():

            # Se página referenciada está carregada na memória (bit_PA = 1)
            if tabela[pag_nova][0]:
                tabela[pag_nova][1] = 1  # bit_R = 1

            # Caso página não esteja carregada na memória
            else:
                contador_falhas += 1

                # Se ainda há espaço, adiciona a página com bit_PA = 1 e bit_R = 0 (mantém contador)
                if quadros_disponiveis > 0:
                    quadros_disponiveis -= 1
                    tabela[pag_nova][0] = 1
                    tabela[pag_nova][1] = 0
                else:
                    # Encontra menor valor de contador para as paginas carregadas em memória
                    min_contador = math.inf
                    for linha in tabela:
                        if linha[0] == 1 and linha[2] < min_contador:
                            min_contador = linha[2]

                    # Percorre a tabela pelos índices (páginas) e separa aqueles de menor contador
                    menores_contadores = [pag for pag in range(len(tabela))
                                          if tabela[pag][0] == 1 and tabela[pag][2] == min_contador]

                    # Exclui aleatoriamente uma página entre os de menor contador (mantém contador)
                    pag_a_remover = random.choice(menores_contadores)
                    tabela[pag_a_remover][0] = 0
                    tabela[pag_a_remover][1] = 0
                    quadros_disponiveis += 1

                    # Carrega nova página na memória com bit_PA = 1 e bit_R = 0 (mantém contador)
                    quadros_disponiveis -= 1
                    tabela[pag_nova][0] = 1
                    tabela[pag_nova][1] = 0

            # Simula interrupção de clock a cada n ciclos (aleatório)
            contador_clock -= 1
            if contador_clock == 0:
                # Atualiza contador deslocando bits para direita e adicionando bit_R ao mais significativo
                for linha in tabela:
                    linha[2] = (linha[2] >> 1) | (linha[1] << 3)
                    linha[1] = 0
                # Reinicia contador de clock com outro valor aleatório
                contador_clock = random.randint(*faixa_aleatoria)

        return self.__calcular_metricas(contador_falhas)


    # SEQUÊNCIAS DE ACESSOS
    def sequencia_aleatoria(self) -> int:
        """Gera uma sequência pseudoaleatória dentro da faixa possível de páginas referenciadas. 
        A sequência aleatória é fixada para garantir condições iguais de comparação de algoritmos."""
        random.seed(112233)  # "Fixa" a sequência aleatória
        
        # Gera sequência um a um ao invés de guardar tudo em memória
        for _ in range(self.__num_acessos):
            yield random.randint(0, self.__max_pag_novas - 1)

    def sequencia_localizada(self) -> int:
        """Gera uma sequência aleatória com maior localidade espacial. 
        A sequência avança aleatoriamente a partir de uma página inicial.
        A localidade é definida em 1/4 do total de páginas. Outros valores podem ser testados.
        A sequência aleatória é fixada para garantir condições iguais de comparação de algoritmos."""
        random.seed(445566)  # "Fixa" a sequência aleatória
        
        pagina = random.randint(0, self.__max_pag_novas - 1)  # Inicia em uma página qualquer
        localidade = self.__max_pag_novas // 8  # Define a região de localidade

        # Gera sequência um a um ao invés de guardar tudo em memória
        for _ in range(0, self.__num_acessos):
            passo = random.randint(-localidade, localidade)  # Escolhe próxima página a partir de uma faixa
            pagina += passo
            yield pagina % self.__max_pag_novas

    def sequencia_linear(self) -> int:
        """Gera uma sequência linear dentro da faixa possível de páginas referenciadas. 
        Inicia a sequencia a partir de uma pagina aleatória.
        A sequência aleatória é fixada para garantir condições iguais de comparação de algoritmos."""
        random.seed(778899)  # "Fixa" a sequência aleatória
        
        pag_inicial = random.randint(0, self.__max_pag_novas - 1)  # Inicia em uma página qualquer

        # Gera sequência um a um ao invés de guardar tudo em memória
        for i in range(self.__num_acessos):
            yield (pag_inicial + i) % self.__max_pag_novas


    # MÉTODOS AUXILIARES
    def __calcular_metricas(self, falhas: int) -> dict:
        """Calcula as métricas relevantes para os algoritmos de substituição de páginas."""
        taxa_falhas = falhas/self.__num_acessos

        # Calcula tempo médio de acesso à memória e converte em ms
        tempo_medio_acesso = ((1 - taxa_falhas) * self.__tempo_memoria +
                              (taxa_falhas * self.__tempo_tratamento)) / 1e6

        metricas = {
            "total": falhas,
            "porcentagem": round(taxa_falhas*100, 4),
            "acesso": round(tempo_medio_acesso, 3),
        }
        return metricas
