# main.py
import os
from janelaprincipal import JanelaPrincipal  # certifique-se que gui.py contém a classe JanelaPrincipal

if __name__ == "__main__":
    caminho = os.path.join(os.path.dirname(__file__), "culturas.json")
    JanelaPrincipal(caminho)