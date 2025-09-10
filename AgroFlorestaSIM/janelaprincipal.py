# Novo layout baseado na arquitetura sugerida
import tkinter as tk
from tkinter import ttk, messagebox
import os, json
from culturas import Cultura
from espaco import Espaco
from ControladorCulturas import ControladorCulturas
from InterfaceMalha import InterfaceMalha

ESCALA_METRO = 30
TAMANHO_INICIAL_MALHA = 10

class JanelaPrincipal:
    def __init__(self, caminho_json):
        self.controlador = ControladorCulturas(caminho_json)
        self.espaco = Espaco(tamanho=TAMANHO_INICIAL_MALHA)
        self.root = tk.Tk()
        self.root.title("AgroflorestaSIM")
        self.root.geometry("1000x800")

        self.frame_esq = tk.Frame(self.root)
        self.frame_esq.pack(side="left", fill="y", padx=10, pady=10)
        self.frame_dir = tk.Frame(self.root)
        self.frame_dir.pack(side="right", padx=10, pady=10)

        self.canvas = tk.Canvas(
            self.frame_dir,
            width=TAMANHO_INICIAL_MALHA * ESCALA_METRO,
            height=TAMANHO_INICIAL_MALHA * ESCALA_METRO,
            bg="white"
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.plantar_em_clique)  # Clique para plantar
        self.canvas.bind("<Button-1>", self.iniciar_arrasto)
        self.canvas.bind("<ButtonRelease-1>", self.finalizar_arrasto)


        self.malha_ui = InterfaceMalha(self.canvas, self.espaco)

        self.criar_interface_lateral()
        self.atualizar_combobox_culturas(self.controlador.culturas_dict)
        self.atualizar_selecionadas()
        self.malha_ui.redesenhar()
        self.root.mainloop()

        self.ultima_cultura_selecionada = None  # Armazena a cultura ativa
        self.posicao_inicio_arrasto = None
        
        

    def criar_interface_lateral(self):
        tk.Label(self.frame_esq, text="Culturas", font=("Arial", 14, "bold")).pack()
        self.frame_b = tk.Frame(self.frame_esq)
        self.frame_b.pack(fill="x")

        search_frame = tk.Frame(self.frame_b)
        search_frame.pack(pady=5, fill="x")
        tk.Label(search_frame, text="🔍").pack(side="left")
        self.entry_busca = tk.Entry(search_frame)
        self.entry_busca.pack(side="left", fill="x", expand=True)
        self.entry_busca.bind("<KeyRelease>", self.filtrar_culturas)
        self.entry_busca.bind("<Return>", self.plantar_primeiro_filtrado)

        self.combo_culturas = ttk.Combobox(self.frame_b, state="readonly")
        self.combo_culturas.pack(pady=5)
        self.combo_culturas.bind("<<ComboboxSelected>>", self.ao_selecionar_cultura)

        self.scale_malha = tk.Scale(
            self.frame_esq, from_=5, to=30, orient='horizontal',
            label='Escala da Malha', command=self.alterar_escala_malha
        )
        self.scale_malha.set(TAMANHO_INICIAL_MALHA)
        self.scale_malha.pack(pady=10)

        tk.Label(self.frame_esq, text="Remover Culturas", font=("Arial", 14, "bold")).pack(pady=10)
        self.frame_s = tk.Frame(self.frame_esq)
        self.frame_s.pack(fill="x")

    def atualizar_combobox_culturas(self, culturas_lista):
        nomes = [c['nome'] for c in culturas_lista]
        self.combo_culturas['values'] = nomes
        if nomes:
            self.combo_culturas.current(0)
        else:
            self.combo_culturas.set("")

    def filtrar_culturas(self, event=None):
        termo = self.entry_busca.get().lower()
        filtradas = self.controlador.buscar_por_nome(termo)
        self.atualizar_combobox_culturas(filtradas)

    def plantar_primeiro_filtrado(self, event=None):
        valores = self.combo_culturas['values']
        if valores:
            self.combo_culturas.set(valores[0])
            self.ao_selecionar_cultura(None)

    def ao_selecionar_cultura(self, event):
        nome = self.combo_culturas.get()
        cultura_dict = self.controlador.obter_por_nome(nome)
        if cultura_dict:
            self.ultima_cultura_selecionada = cultura_dict  # Agora guarda a última cultura selecionada

    def plantar(self, cd):
        nova = Cultura(**cd)
        try:
            x, y = self.espaco.adicionar_cultura(nova)
        except ValueError as e:
            messagebox.showinfo("Atenção", str(e))
            return
        self.controlador.registrar_selecao(nova, (x, y))
        self.atualizar_selecionadas()
        self.malha_ui.redesenhar()

    def atualizar_selecionadas(self):
        for w in self.frame_s.winfo_children(): w.destroy()

        valores = [f"{c.nome} em ({x},{y})" for c, (x, y) in self.controlador.selecionadas]
        if not valores:
            ttk.Label(self.frame_s, text="Nenhuma cultura selecionada.").pack()
            return

        self.combo_remover = ttk.Combobox(self.frame_s, values=valores)
        self.combo_remover.pack(pady=5)

        ttk.Button(self.frame_s, text="Remover Selecionada", command=self.remover_selecionada).pack(pady=5)

    def remover_selecionada(self):
        sel = self.combo_remover.get()
        if sel:
            nome, posicao = sel.split(" em ")
            x, y = eval(posicao)
            self.espaco.grade[x][y] = None
            self.controlador.remover_selecao(nome, x, y)
            self.atualizar_selecionadas()
            self.malha_ui.redesenhar()

    def alterar_escala_malha(self, valor):
        novo_tamanho = int(valor)
        self.espaco.redimensionar(novo_tamanho)
        self.canvas.config(width=novo_tamanho * ESCALA_METRO, height=novo_tamanho * ESCALA_METRO)
        self.controlador.selecionadas.clear()
        self.atualizar_selecionadas()
        self.malha_ui.redesenhar()
    def plantar_em_clique(self, event):
        if not self.ultima_cultura_selecionada:
            messagebox.showinfo("Seleção necessária", "Selecione uma cultura primeiro.")
            return

        x = event.y // ESCALA_METRO
        y = event.x // ESCALA_METRO
        nova = Cultura(**self.ultima_cultura_selecionada)

        if not self.espaco.linha_permitida_para(nova.categoria, x):
            messagebox.showinfo(
                "Linha inválida",
                f"{nova.categoria} não pode ser plantada na linha {x}.\n"
                f"Linhas permitidas: "
                f"{'Frutíferas → x % 3 == 0' if nova.categoria == 'Frutífera' else ''}"
                f"{'Hortaliças → x % 3 == 1' if nova.categoria == 'Hortaliça' else ''}"
                f"{'Roça → x % 3 == 0 ou 2' if nova.categoria == 'Roça' else ''}"
            )
            return

        if not self.espaco.is_disponivel(x, y):
            messagebox.showinfo("Espaço ocupado", "Essa posição já está ocupada.")
            return

        if not self.espaco.pode_plantar(nova, x, y):
            messagebox.showinfo("Restrição de plantio", f"Não é possível plantar {nova.nome} nessa posição.")
            return

        self.espaco.grade[x][y] = nova
        self.controlador.registrar_selecao(nova, (x, y))
        self.atualizar_selecionadas()
        self.malha_ui.redesenhar()
    def iniciar_arrasto(self, event):
        x = event.y // ESCALA_METRO
        y = event.x // ESCALA_METRO
        self.posicao_inicio_arrasto = (x, y)
    def finalizar_arrasto(self, event):
        if not self.ultima_cultura_selecionada:
            return

        x0, y0 = self.posicao_inicio_arrasto or (0, 0)
        x1 = event.y // ESCALA_METRO
        y1 = event.x // ESCALA_METRO

        # Ordenar coordenadas para percorrer corretamente
        linha_inicio, linha_fim = sorted((x0, x1))
        coluna_inicio, coluna_fim = sorted((y0, y1))

        cultura_base = Cultura(**self.ultima_cultura_selecionada)

        for x in range(linha_inicio, linha_fim + 1):
            for y in range(coluna_inicio, coluna_fim + 1):
                if not self.espaco.linha_permitida_para(cultura_base.categoria, x):
                    continue
                if not self.espaco.is_disponivel(x, y):
                    continue
                if not self.espaco.pode_plantar(cultura_base, x, y):
                    continue

                nova = Cultura(**self.ultima_cultura_selecionada)
                self.espaco.grade[x][y] = nova
                self.controlador.registrar_selecao(nova, (x, y))

        self.atualizar_selecionadas()
        self.malha_ui.redesenhar()
if __name__ == "__main__":
    JanelaPrincipal(os.path.join(os.path.dirname(__file__), "culturas.json"))
