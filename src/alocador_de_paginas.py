import random


class AlocadorDePaginas:
    """Simula a alocação e liberação de páginas na memória de acordo com diferentes algoritmos, apresentando dados de desempenho de cada algoritmo."""

    def __init__(self, num_quadros: int, tam_quadro: int, max_paginas: int) -> None:
        self.__num_quadros = num_quadros  # Quadros disponíveis na memória física
        self.__tam_quadro = tam_quadro  # Tamanho em Bytes de cada quadro
        self.__max_paginas = max_paginas  # Máximo de páginas enderecáveis por processo

    def gerar_sequencia_paginas(tam_sequencia: int, max_paginas: int, seed: int = 42) -> int:
        """Gera uma sequência pseudoaleatória de páginas referenciadas. A sequência gerada é sempre a mesma a não ser que o parâmetro seed seja alterado."""
        random.seed(seed)
        for _ in range(tam_sequencia-1):
            yield random.randint(0, max_paginas-1)

    def fifo(self, page_sequence_gen):
        page_faults = 0
        queue = []  # Queue to implement FIFO

        for page in page_sequence_gen:
            # If the page is not in memory
            if page not in self.frames:
                page_faults += 1

                # If there is still space in memory, add the page
                if len(self.frames) < self.num_frames:
                    self.frames.append(page)
                    queue.append(page)
                else:
                    # Replace the oldest page
                    oldest_page = queue.pop(0)
                    self.frames.remove(oldest_page)
                    self.frames.append(page)
                    queue.append(page)

        return page_faults

    def second_chance(self, page_sequence):
        # Second-Chance implementation
        pass

    def clock(self, page_sequence):
        # Clock implementation
        pass

    def nru(self, page_sequence):
        # NRU implementation
        pass

    def lru(self, page_sequence):
        # LRU implementation
        pass
