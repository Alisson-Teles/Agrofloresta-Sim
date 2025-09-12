# Novo layout baseado na arquitetura sugerida
import tkinter as tk
from tkinter import ttk, messagebox
import os, json
from culturas import Cultura
from espaco import Espaco

ESCALA_METRO = 30
TAMANHO_INICIAL_MALHA = 10

class InterfaceMalha:
    def __init__(self, canvas, espaco,pai=None):
        self.canvas = canvas
        self.espaco = espaco
        self.pai = pai  # agora guardamos a referência à JanelaPrincipal


    def redesenhar(self):
        self.canvas.delete("all")
        for i in range(self.espaco.tamanho):
            for j in range(self.espaco.tamanho):
                x0, y0 = j * ESCALA_METRO, i * ESCALA_METRO
                x1, y1 = x0 + ESCALA_METRO, y0 + ESCALA_METRO
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="gray")
                c = self.espaco.grade[i][j]
                if c:
                    self.canvas.create_text(
                        x0 + ESCALA_METRO / 2, y0 + ESCALA_METRO / 2,
                        text=c.icone or "?", font=("Arial", 20), anchor="center")
                # Marca visual para células selecionadas Checa se a célula está na seleção atual
                if self.pai and self.pai.celulas_selecionadas and (i, j) in self.pai.celulas_selecionadas:
                    cultura_dict = getattr(self.pai, "ultima_cultura_selecionada", None)
                    modo_remocao = getattr(self.pai, "modo_remocao", False)

                    if modo_remocao:
                        # Em modo de remoção: destaca apenas onde há cultura
                        if self.espaco.grade[i][j] is not None:
                            self.canvas.create_rectangle(
                                x0 + 2, y0 + 2, x1 - 2, y1 - 2,
                                outline="red", width=2, dash=(4, 2)
                            )
                    elif cultura_dict:
                        cultura_temp = Cultura(**cultura_dict)

                        linha_valida = self.espaco.linha_permitida_para(cultura_temp.categoria, i)
                        disponivel = self.espaco.is_disponivel(i, j)
                        pode_plantar = self.espaco.pode_plantar(cultura_temp, i, j)

                        cor = "blue" if linha_valida and disponivel and pode_plantar else "red"

                        self.canvas.create_rectangle(
                            x0 + 2, y0 + 2, x1 - 2, y1 - 2,
                            outline=cor, width=2, dash=(4, 2)
                        )

                    
    def get_layout_para_imagem(self):
        """
        Retorna o layout atual da malha em um dicionário pronto para
        deepseek.gerar_prompt_imagem(layout).

        Estrutura:
        {
          "grid": {
            "linhas": int,
            "colunas": int,
            "tamanho_celula": float|int,
            "unidade": "m"  # interpretando ESCALA_METRO como pixels por metro
          },
          "itens": [
            {"nome": str, "linha": int, "coluna": int, "rotacao": float, "escala": float},
            ...
          ]
        }
        """
        linhas = int(self.espaco.tamanho)
        colunas = int(self.espaco.tamanho)

        # Se ESCALA_METRO = pixels por metro, então cada célula de grade equivale a 1 metro.
        # Ajuste aqui se você quiser outro mapeamento.
        tamanho_celula_metros = 1

        itens = []
        # A grade é indexada como [linha][coluna] (i=janelas/linhas, j=colunas)
        for li in range(self.espaco.tamanho):
            for co in range(self.espaco.tamanho):
                c = self.espaco.grade[li][co]
                if c is not None:
                    itens.append({
                        "nome": getattr(c, "nome", str(c)),
                        "linha": li,
                        "coluna": co,
                        "rotacao": 0.0,   # não há rotação na UI atual
                        "escala": 1.0     # escala padrão 1:1
                    })

        layout = {
            "grid": {
                "linhas": linhas,
                "colunas": colunas,
                "tamanho_celula": tamanho_celula_metros,
                "unidade": "m"
            },
            "itens": itens
        }

        return layout