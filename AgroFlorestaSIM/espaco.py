# espaco.py
from typing import List, Tuple

class Espaco:
    def __init__(self, tamanho: int = 10):
        self.tamanho = tamanho
        self.grade = [[None for _ in range(tamanho)] for _ in range(tamanho)]
        self.ultimas_posicoes = {'Frutífera': (0, 0), 'Hortaliça': (0, 0), 'Roça': (0, 0)}

    def is_disponivel(self, x: int, y: int) -> bool:
        return 0 <= x < self.tamanho and 0 <= y < self.tamanho and self.grade[x][y] is None

    def pode_plantar(self, cultura, x: int, y: int) -> bool:
        raio = cultura.diametro_copa // 2
        for i in range(max(0, x - raio), min(self.tamanho, x + raio + 1)):
            for j in range(max(0, y - raio), min(self.tamanho, y + raio + 1)):
                ocupante = self.grade[i][j]
                if ocupante is not None and ocupante.categoria == cultura.categoria:
                    return False
        return True

    def adicionar_cultura(self, cultura) -> Tuple[int, int]:
        def linha_preferida(x):
            if cultura.categoria == 'Frutífera':
                return x % 3 == 0
            elif cultura.categoria == 'Hortaliça':
                return x % 3 == 1
            elif cultura.categoria == 'Roça':
                return x % 3 in (0, 2)
            return True

        x_ini, y_ini = self.ultimas_posicoes.get(cultura.categoria, (0, 0))

        # Primeiro: busca a partir da última posição usada
        for x in range(x_ini, self.tamanho):
            if linha_preferida(x):
                for y in range(y_ini if x == x_ini else 0, self.tamanho):
                    if self.is_disponivel(x, y) and self.pode_plantar(cultura, x, y):
                        self.grade[x][y] = cultura
                        self.ultimas_posicoes[cultura.categoria] = (x, y + 1 if y + 1 < self.tamanho else 0)
                        return x, y

        # Se falhar, faz varredura total
        for x in range(self.tamanho):
            if linha_preferida(x):
                for y in range(self.tamanho):
                    if self.is_disponivel(x, y) and self.pode_plantar(cultura, x, y):
                        self.grade[x][y] = cultura
                        self.ultimas_posicoes[cultura.categoria] = (x, y + 1 if y + 1 < self.tamanho else 0)
                        return x, y

        raise ValueError(f"Não há espaço suficiente para plantar {cultura.nome} com copa de {cultura.diametro_copa}m.")
    def limpar(self):
        self.grade = [[None for _ in range(self.tamanho)] for _ in range(self.tamanho)]
    def linha_permitida_para(self, categoria, x):
        if categoria == 'Frutífera':
            return x % 3 == 0
        elif categoria == 'Hortaliça':
            return x % 3 == 1
        elif categoria == 'Roça':
            return x % 3 in (0, 2)
        return True
