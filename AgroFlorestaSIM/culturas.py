import json
import os

# Variável global para gerenciar IDs únicos
global proximo_id
proximo_id = 1

class Cultura:
    def __init__(
        self,
        nome,
        tipo,
        classificacao_agronomica=None,
        classificacao_morfologica=None,
        sinergias=None,
        antagonismos=None,
        tempo_crescimento=0,
        rendimento=0,
        necessidades=None,
        necessidade_luz=None,
        necessidade_hidrica=None,
        temperatura_ideal=None,
        faixa_ph=None,
        porte=None,
        ciclo=None,
        epocas_plantio=None,
        exigencia_nutricional=None,
        sombreamento=0,
        pragas=None,
        doencas=None,
        controle_natural=None,
        cobertura_solo=1,
        diametro_copa=1,  # Novo atributo adicionado
        atrai_polinizadores=None,
        interacao_outros=None,
        resistencia=None,
        tempo_colheita=None,
        icone="?",
        **kwargs
    ):
        global proximo_id
        self.id_cultura = proximo_id
        proximo_id += 1

        self.nome = nome
        self.tipo = tipo
        # Categoria explícita: Frutífera, Hortaliça ou Roça
        lower_tipo = (tipo or "").lower()
        if 'frut' in lower_tipo:
            self.categoria = 'Frutífera'
        elif 'hort' in lower_tipo:
            self.categoria = 'Hortaliça'
        else:
            self.categoria = 'Roça'

        self.classificacao_agronomica = classificacao_agronomica or "Não especificado"
        self.classificacao_morfologica = classificacao_morfologica or "Não especificado"
        self.sinergias = sinergias or []
        self.antagonismos = antagonismos or []
        self.tempo_crescimento = tempo_crescimento
        self.rendimento = rendimento
        self.necessidades = necessidades or {"sol": "moderado", "agua": "moderado", "solo": "neutro"}
        self.necessidade_luz = necessidade_luz
        self.necessidade_hidrica = necessidade_hidrica
        self.temperatura_ideal = temperatura_ideal
        self.faixa_ph = faixa_ph
        self.porte = porte
        self.ciclo = ciclo
        self.epocas_plantio = epocas_plantio
        self.exigencia_nutricional = exigencia_nutricional
        self.sombreamento = int(sombreamento)
        self.pragas = pragas or []
        self.doencas = doencas or []
        self.controle_natural = controle_natural or []
        self.cobertura_solo = int(cobertura_solo)
        self.diametro_copa = int(diametro_copa)  # Atributo novo
        self.atrai_polinizadores = atrai_polinizadores
        self.interacao_outros = interacao_outros
        self.resistencia = resistencia
        self.tempo_colheita = tempo_colheita
        self.icone = icone
        self.atributos_extras = kwargs
        self.idade = 0
        self.saudavel = True

    def to_dict(self):
        return {
            "id_cultura": self.id_cultura,
            "nome": self.nome,
            "tipo": self.tipo,
            "categoria": self.categoria,
            "classificacao_agronomica": self.classificacao_agronomica,
            "classificacao_morfologica": self.classificacao_morfologica,
            "sinergias": self.sinergias,
            "antagonismos": self.antagonismos,
            "tempo_crescimento": self.tempo_crescimento,
            "rendimento": self.rendimento,
            "necessidades": self.necessidades,
            "necessidade_luz": self.necessidade_luz,
            "necessidade_hidrica": self.necessidade_hidrica,
            "temperatura_ideal": self.temperatura_ideal,
            "faixa_ph": self.faixa_ph,
            "porte": self.porte,
            "ciclo": self.ciclo,
            "epocas_plantio": self.epocas_plantio,
            "exigencia_nutricional": self.exigencia_nutricional,
            "sombreamento": self.sombreamento,
            "pragas": self.pragas,
            "doencas": self.doencas,
            "controle_natural": self.controle_natural,
            "cobertura_solo": self.cobertura_solo,
            "diametro_copa": self.diametro_copa,
            "atrai_polinizadores": self.atrai_polinizadores,
            "interacao_outros": self.interacao_outros,
            "resistencia": self.resistencia,
            "tempo_colheita": self.tempo_colheita,
            "icone": self.icone,
            "atributos_extras": self.atributos_extras,
        }

if __name__ == "__main__":
    caminho_json = os.path.join(os.path.dirname(__file__), "culturas.json")

    novas_culturas = [
        Cultura(
            nome="MAMÃO",
            tipo="Frutífera",
            classificacao_agronomica="Comercial",
            classificacao_morfologica="Árvore de porte médio",
            sinergias=["Bananeira", "Crotalária"],
            antagonismos=["Tomate"],
            tempo_crescimento=120,
            rendimento=30,
            necessidades={"sol": "pleno", "agua": "moderado", "solo": "fértil"},
            necessidade_luz="pleno",
            necessidade_hidrica="moderada",
            temperatura_ideal="25–30°C",
            faixa_ph="5.5–6.7",
            porte="Médio",
            ciclo="Anual",
            epocas_plantio=["Primavera"],
            exigencia_nutricional="Alta",
            sombreamento=1,
            pragas=["Mosca-das-frutas"],
            doencas=["Oídio"],
            controle_natural=["Neem", "Trichoderma"],
            cobertura_solo=3,
            diametro_copa = 2,
            atrai_polinizadores="Sim",
            interacao_outros="Melhora estrutura do solo",
            resistencia="Moderada à seca",
            tempo_colheita="6 meses",
            icone="🍈"
        ),
        Cultura(
            nome="MILHO",
            tipo="Cereal",
            classificacao_agronomica="Grão",
            classificacao_morfologica="Erva anual",
            sinergias=["Feijão", "Crotalária"],
            antagonismos=["Tomate"],
            tempo_crescimento=90,
            rendimento=80,
            necessidades={"sol": "pleno", "agua": "alta", "solo": "argiloso"},
            necessidade_luz="pleno",
            necessidade_hidrica="alta",
            temperatura_ideal="20–30°C",
            faixa_ph="5.5–6.5",
            porte="Alto",
            ciclo="Curto",
            epocas_plantio=["Primavera", "Verão"],
            exigencia_nutricional="Alta (N, P, K)",
            sombreamento=2,
            pragas=["Lagarta-do-cartucho"],
            doencas=["Ferrugem"],
            controle_natural=["Bacillus thuringiensis"],
            cobertura_solo=3,
            diametro_copa=1,
            atrai_polinizadores="Não",
            interacao_outros="Bom para consórcio",
            resistencia="Alta resistência a ventos",
            tempo_colheita="4 meses",
            icone="🌽"
        ),
        Cultura(
            nome="ALFACE",
            tipo="Hortaliça",
            classificacao_agronomica="Folhosa",
            classificacao_morfologica="Herbácea",
            sinergias=["Cenoura", "Rabanete"],
            antagonismos=["Salsinha"],
            tempo_crescimento=40,
            rendimento=5,
            necessidades={"sol": "meia sombra", "agua": "moderado", "solo": "rico em matéria orgânica"},
            necessidade_luz="meia sombra",
            necessidade_hidrica="média",
            temperatura_ideal="15–20°C",
            faixa_ph="6.0–7.0",
            porte="Baixo",
            ciclo="Curto",
            epocas_plantio=["Outono", "Primavera"],
            exigencia_nutricional="Média",
            sombreamento=0,
            pragas=["Pulgões"],
            doencas=["Míldio"],
            controle_natural=["Alho", "Calda bordalesa"],
            cobertura_solo=1,
            diametro_copa=1,
            atrai_polinizadores="Não",
            interacao_outros="Não interfere",
            resistencia="Fraca à seca",
            tempo_colheita="40 dias",
            icone="🥬"
        ),
    ]

    # Carrega o JSON existente (se houver)
    if os.path.exists(caminho_json):
        with open(caminho_json, "r", encoding="utf-8") as f:
            existentes = json.load(f)
    else:
        existentes = []

    for cultura in novas_culturas:
        existentes.append(cultura.to_dict())

    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(existentes, f, ensure_ascii=False, indent=2)

    print("✅ Culturas adicionadas ao culturas.json com sucesso.")
