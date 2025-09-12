import requests
import json

# --- PT -> EN dictionary for crop names (extend as needed)
PT_EN = {
    "MAMÃO": "papaya",
    "MILHO": "corn",
    "MILHO VERDE": "sweet corn",
    "ALFACE": "lettuce",
    "ABACAXI": "pineapple",
    "ABOBRINHA-MENINA": "zucchini",
    "AGRIÃO": "watercress",
    "ALHO": "garlic",
    "AMENDOIM": "peanut",
    "BANANA": "banana",
    "BATATA": "potato",
    "BATATA-DOCE": "sweet potato",
    "BERINJELA": "eggplant",
    "BETERRABA": "beetroot",
    "BRÓCOLIS": "broccoli",
    "CEBOLA": "onion",
    "CENOURA": "carrot",
    "COUVE-FLOR": "cauliflower",
    "ERVILHA": "pea",
    "FEIJÃO-CARIOCA": "common bean (carioca)",
    "GRÃO-DE-BICO": "chickpea",
    "LENTILHA": "lentil",
    "MAÇÃ": "apple",
    "MANDIOCA": "cassava",
    "SOJA": "soybean",
    "TOMATE": "tomato",
    "TRIGO": "wheat",
    "UVA": "grape",
}

def crop_en(name_pt: str) -> str:
    if not name_pt:
        return "unknown crop"
    key = name_pt.strip().upper()
    return PT_EN.get(key, name_pt)  # fallback: keep original if not found


# Replace with your OpenRouter API key
API_KEY = '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'  # ⚠️ troque pela sua chave
API_URL = 'https://openrouter.ai/api/v1/chat/completions'

# Define the headers for the API request
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# -------------------------------
# Função extra: gerar prompt do plantio
# -------------------------------
def gerar_prompt_imagem(layout, idioma="en", estilo="realistic photographic"):
    """
    Generate an image prompt faithful to the planting layout,
    explicitly describing the positions (row, column) and
    the relative position (cx, cy normalized 0–1) of each crop's center.
    """
    grid = layout.get("grid", {}) or {}
    itens = layout.get("itens", []) or []

    linhas = int(grid.get("linhas", 0) or 0)
    colunas = int(grid.get("colunas", 0) or 0)
    tam = grid.get("tamanho_celula", 1)
    un = grid.get("unidade", "m")

    # Order by row/column for determinism
    try:
        itens_sorted = sorted(itens, key=lambda it: (int(it.get("linha", 0)), int(it.get("coluna", 0))))
    except Exception:
        itens_sorted = itens

    # Compact block with all positions
    linhas_mapa = []
    linhas_mapa.append(f"GRID {linhas}x{colunas} (cell={tam}{un})")
    linhas_mapa.append("STRICT MAP (one crop per line):")
    linhas_mapa.append("# format: row,column:name | cx=fraction_x cy=fraction_y | rot=degrees scale=factor")

    def norm(v, total):
        # cell center: (index + 0.5) / total; avoids div by zero
        return (float(v) + 0.5) / float(total if total else 1)

    for it in itens_sorted:
        li = int(it.get("linha", 0))
        co = int(it.get("coluna", 0))
        cx = round(norm(co, colunas), 4)
        cy = round(norm(li, linhas), 4)
        rot = float(it.get("rotacao", 0))
        esc = float(it.get("escala", 1.0))
        nome_pt = str(it.get("nome", "?"))
        nome = crop_en(nome_pt)  # translate to English if we have it
        linhas_mapa.append(f"{li},{co}:{nome} | cx={cx} cy={cy} | rot={rot} scale={esc}")

    mapa_estrito = "\n".join(linhas_mapa)

    regras = (
        "RULES (mandatory):\n"
        "- Reproduce exactly the positions and quantities described in the STRICT MAP; do not invent or omit crops.\n"
        "- Use the normalized coordinates (cx, cy) as composition anchors for the visual center of each crop.\n"
        "- Respect the grid: rows on the vertical axis (top=0), columns on the horizontal axis (left=0).\n"
        "- Maintain proportions between crops when possible; prioritize readability of the grid arrangement.\n"
        "- The scene should be a realistic agricultural environment (soil, natural light) unless the chosen style specifies otherwise."
    )

    briefing = (
        f"Output language: {idioma}\n"
        f"Desired style: {estilo}\n\n"
        "MANDATORY RESPONSE FORMAT:\n"
        "PROMPT:\n"
        "NEGATIVE PROMPT:\n\n"
        f"{mapa_estrito}\n\n"
        f"{regras}\n"
    )

    data = {
    "model": "deepseek/deepseek-chat-v3.1:free",
    "messages": [
        {
            "role": "system",
            "content": (
                "You are a strict image prompt engineer. "
                "RESPOND IN ENGLISH ONLY. Do not use any other language. "
                "If the input contains Portuguese or other languages, translate to English, "
                "but keep proper nouns (e.g., crop names) as-is. "
                "Follow the STRICT MAP and the RULES exactly."
            )
        },
        {
            "role": "user",
            "content": (
                f"Output language: {idioma}\n"
                f"Desired style: {estilo}\n\n"
                "MANDATORY RESPONSE FORMAT:\n"
                "PROMPT:\n"
                "NEGATIVE PROMPT:\n\n"
                f"{mapa_estrito}\n\n"
                f"{regras}\n"
            )
        }
    ],
    "temperature": 0.2
}

    resp = requests.post(API_URL, json=data, headers=headers, timeout=60)
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]

    # separate PROMPT and NEGATIVE PROMPT
    prompt, negative = content, ""
    upper = content.upper()
    if "NEGATIVE PROMPT:" in upper:
        idx = upper.index("NEGATIVE PROMPT:")
        prompt = content[:idx].replace("PROMPT:", "").strip()
        negative = content[idx + len("NEGATIVE PROMPT:"):].strip()

    return {"prompt": prompt, "negative_prompt": negative, "raw": content}


# -------------------------------
#  Teste antigo (mantido)
# -------------------------------
if __name__ == "__main__":
    # Teste simples original
    data = {
        "model": "deepseek/deepseek-chat-v3.1:free",
        "messages": [{"role": "user", "content": "Can you say hello word ?"}]
    }
    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200:
        print("API Response:", response.json())
    else:
        print("Failed to fetch data from API. Status Code:", response.status_code)

    # Teste novo: gerar prompt do plantio
    exemplo_layout = {
        "grid": {"linhas": 3, "colunas": 3, "tamanho_celula": 1, "unidade": "m"},
        "itens": [
            {"nome": "MILHO", "linha": 0, "coluna": 0, "rotacao": 0, "escala": 1},
            {"nome": "ALFACE", "linha": 1, "coluna": 1, "rotacao": 0, "escala": 1},
        ]
    }
    try:
        resp = gerar_prompt_imagem(exemplo_layout)
        print("\n=== PROMPT ===\n", resp["prompt"])
        print("\n=== NEGATIVE PROMPT ===\n", resp["negative_prompt"])
    except Exception as e:
        print("Erro no teste de gerar_prompt_imagem:", e)
