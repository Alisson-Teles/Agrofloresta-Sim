# Novo layout baseado na arquitetura sugerida
import tkinter as tk
from tkinter import ttk, messagebox
import os, json
from culturas import Cultura
from espaco import Espaco

ESCALA_METRO = 30
TAMANHO_INICIAL_MALHA = 10

class ControladorCulturas:
    def __init__(self, caminho_json):
        self.culturas_dict = self.carregar_culturas(caminho_json)
        self.selecionadas = []

    def carregar_culturas(self, caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)

    def buscar_por_nome(self, termo):
        return [c for c in self.culturas_dict if termo.lower() in c['nome'].lower()]

    def obter_por_nome(self, nome):
        return next((c for c in self.culturas_dict if c['nome'] == nome), None)

    def registrar_selecao(self, cultura, posicao):
        self.selecionadas.append((cultura, posicao))

    def remover_selecao(self, nome, x, y):
        for i, (c, (cx, cy)) in enumerate(self.selecionadas):
            if c.nome == nome and (cx, cy) == (x, y):
                del self.selecionadas[i]
                break
