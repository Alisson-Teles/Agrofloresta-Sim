# Novo layout baseado na arquitetura sugerida
import tkinter as tk
from tkinter import ttk, messagebox
import os, json
from culturas import Cultura
from espaco import Espaco

ESCALA_METRO = 30
TAMANHO_INICIAL_MALHA = 10

class InterfaceMalha:
    def __init__(self, canvas, espaco):
        self.canvas = canvas
        self.espaco = espaco

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