# Novo layout baseado na arquitetura sugerida
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os, json
from culturas import Cultura
from espaco import Espaco
from ControladorCulturas import ControladorCulturas
from InterfaceMalha import InterfaceMalha
import deepseek  # 🔹 ADICIONADO

ESCALA_METRO = 30
TAMANHO_INICIAL_MALHA = 10

class JanelaPrincipal:
    def __init__(self, caminho_json):

        self.celulas_selecionadas = set()  # Conjunto de (x, y)
        self.modo_remocao = False
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
        self.canvas.bind("<B1-Motion>", self.atualizar_area_arrasto) #Mostrar seleção em tempo real
        self.canvas.bind("<ButtonRelease-1>", self.finalizar_arrasto)
        

        self.malha_ui = InterfaceMalha(self.canvas, self.espaco, pai=self)

        #GARANTE atributos usados em outros métodos
        self.ultima_cultura_selecionada = None
        self.posicao_inicio_arrasto = None

        self.criar_interface_lateral()
        self.atualizar_combobox_culturas(self.controlador.culturas_dict)
        self.atualizar_selecionadas()
        self.malha_ui.redesenhar()
        self.root.mainloop()

        style = ttk.Style()
        style.configure("BotaoVerde.TButton", background="green", foreground="white")
        style.map("BotaoVerde.TButton", background=[('active', 'darkgreen')])

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

        #Botão novo: Criar imagem do plantio
        ttk.Button(
            self.frame_esq, text="Criar imagem do plantio",
            command=self.criar_imagem_do_plantio
        ).pack(pady=6, fill="x")

        tk.Label(self.frame_esq, text="Remover Culturas", font=("Arial", 14, "bold")).pack(pady=10)
        self.frame_s = tk.Frame(self.frame_esq)
        self.frame_s.pack(fill="x")

    def atualizar_area_arrasto(self, event):
        if not self.posicao_inicio_arrasto:
            return

        x0, y0 = self.posicao_inicio_arrasto
        x1 = event.y // ESCALA_METRO
        y1 = event.x // ESCALA_METRO

        linha_inicio, linha_fim = sorted((x0, x1))
        coluna_inicio, coluna_fim = sorted((y0, y1))

        # Atualiza seleção visual em tempo real
        self.celulas_selecionadas = set(
            (x, y)
            for x in range(linha_inicio, linha_fim + 1)
            for y in range(coluna_inicio, coluna_fim + 1)
        )
        self.malha_ui.redesenhar()

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

        self.botao_remover_arrasto = ttk.Button(
            self.frame_s,
            text="Remover por arrasto (OFF)",
            command=self.toggle_remocao_arrasto
        )
        self.botao_remover_arrasto.pack(pady=3)
        ttk.Button(self.frame_s,text="Remover todas selecionadas",command=self.remover_todas_selecionadas).pack(pady=3)
        
    def toggle_remocao_arrasto(self):
        self.modo_remocao = not getattr(self, "modo_remocao", False)

        if self.modo_remocao:
            self.botao_remover_arrasto.config(
                text="Remover por arrasto (ON)",
                style="BotaoVerde.TButton"
            )
            messagebox.showinfo("Modo Remoção Ativado", "Agora você pode arrastar sobre a malha para remover culturas.")
        else:
            self.botao_remover_arrasto.config(
                text="Remover por arrasto (OFF)",
                style="TButton"
            )
            self.celulas_selecionadas.clear()
            self.malha_ui.redesenhar()

    
    
    def remover_todas_selecionadas(self):
        if not self.controlador.selecionadas:
            messagebox.showinfo("Nada para remover", "Nenhuma cultura está selecionada.")
            return

        if messagebox.askyesno("Confirmar", "Deseja remover todas as culturas selecionadas?"):
            for cultura, (x, y) in self.controlador.selecionadas:
                self.espaco.grade[x][y] = None
            self.controlador.selecionadas.clear()

            self.celulas_selecionadas.clear()
            self.ultima_cultura_selecionada = None  # força não desenhar marcação azul/vermelha

            self.malha_ui.redesenhar()
            self.atualizar_selecionadas()


    def ativar_remocao_arrasto(self):
        messagebox.showinfo("Modo Remoção", "Agora arraste sobre a malha para remover culturas.")
        self.modo_remocao = True
            
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
        # OBS: seu Espaco atual não tem redimensionar; mantenho sua chamada como está.
        self.espaco.redimensionar(novo_tamanho)
        self.canvas.config(width=novo_tamanho * ESCALA_METRO, height=novo_tamanho * ESCALA_METRO)
        self.controlador.selecionadas.clear()
        self.atualizar_selecionadas()
        self.malha_ui.redesenhar()

    def plantar_em_clique(self, event):
        if not getattr(self, "ultima_cultura_selecionada", None):
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
        x0, y0 = self.posicao_inicio_arrasto or (0, 0)
        x1 = event.y // ESCALA_METRO
        y1 = event.x // ESCALA_METRO

        linha_inicio, linha_fim = sorted((x0, x1))
        coluna_inicio, coluna_fim = sorted((y0, y1))

        # Atualiza seleção visual
        self.celulas_selecionadas = set(
            (x, y)
            for x in range(linha_inicio, linha_fim + 1)
            for y in range(coluna_inicio, coluna_fim + 1)
        )

        # REMOÇÃO (tem prioridade)
        if self.modo_remocao:
            for x, y in self.celulas_selecionadas:
                cultura = self.espaco.grade[x][y]
                if cultura:
                    self.espaco.grade[x][y] = None
                    self.controlador.remover_selecao(cultura.nome, x, y)

            self.modo_remocao = False  # desativa o modo automaticamente (ou mantenha ativo se preferir)
            self.atualizar_selecionadas()
            self.malha_ui.redesenhar()
            self.celulas_selecionadas.clear()
            return  # impede o plantio

        # PLANTIO (somente se não estiver no modo de remoção)
        if not getattr(self, "ultima_cultura_selecionada", None):
            return

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
        self.celulas_selecionadas.clear()


    # ------------------------------
    # NOVO: Gera prompt de imagem
    # ------------------------------
    def criar_imagem_do_plantio(self):
        # Verifica se a InterfaceMalha tem o método (adicionamos no arquivo dela)
        if not hasattr(self.malha_ui, "get_layout_para_imagem"):
            messagebox.showwarning(
                "Função indisponível",
                "Atualize o arquivo InterfaceMalha.py para incluir get_layout_para_imagem()."
            )
            return

        layout = self.malha_ui.get_layout_para_imagem()
        if not layout.get("itens"):
            messagebox.showinfo("Layout vazio", "Nenhuma cultura posicionada na malha.")
            return

        try:
            resp = deepseek.gerar_prompt_imagem(layout, idioma="pt-BR", estilo="realista fotográfico")
        except Exception as e:
            messagebox.showerror("Erro ao gerar prompt", f"{e}")
            return

        prompt = resp.get("prompt", "").strip()
        neg = resp.get("negative_prompt", "").strip()
        conteudo = "PROMPT:\n" + (prompt or "") + ("\n\nNEGATIVE PROMPT:\n" + neg if neg else "")

        # Janela com campo de texto + copiar/salvar
        dlg = tk.Toplevel(self.root)
        dlg.title("Prompt de imagem do plantio")
        dlg.geometry("820x560")

        txt = tk.Text(dlg, wrap="word")
        txt.insert("1.0", conteudo)
        txt.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(dlg)
        btn_frame.pack(fill="x", padx=10, pady=6)

        def copiar():
            self.root.clipboard_clear()
            self.root.clipboard_append(txt.get("1.0", "end-1c"))
            messagebox.showinfo("Copiado", "Prompt copiado para a área de transferência.")

        def salvar():
            arq = filedialog.asksaveasfilename(
                parent=dlg,
                title="Salvar prompt",
                defaultextension=".txt",
                filetypes=[("Arquivo de texto", "*.txt")]
            )
            if arq:
                with open(arq, "w", encoding="utf-8") as f:
                    f.write(txt.get("1.0", "end-1c"))
                messagebox.showinfo("Salvo", f"Arquivo salvo em:\n{arq}")

        ttk.Button(btn_frame, text="Copiar", command=copiar).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Salvar .txt", command=salvar).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Fechar", command=dlg.destroy).pack(side="right", padx=4)


if __name__ == "__main__":
    JanelaPrincipal(os.path.join(os.path.dirname(__file__), "culturas.json"))
