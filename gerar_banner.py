"""Gera assets/besouros.svg: uma vitrine de besouros em ASCII, coloridos,
mostrando a populacao escurecendo ao longo das geracoes.

Uso: python gerar_banner.py
"""
import os
import random

SEED = 7
TAM_POP = 50
GERACOES_MOSTRADAS = [0, 1, 2, 3, 4, 5, 6, 8, 10, 14]

BESOURO = [
    r"       ,_    /) (\    _,",
    r"        >>  <<,_,>>  <<",
    r"       //   _0.-.0_   \\",
    r"        '._/░░░░░░░\_.'/",
    r"        '-.\.--.--./.-'",
    r"        __/ ░░░Y░░░ \ _",
    r"';,  .-(_| ░░░░|░░░░ |_)-.  ,:'",
    r"   \\/.'  |░░░░░|░░░░░|  `.\//",
    r"   (/    |░░░░░|░░░░░|    \)",
    r"         |░░░░░|░░░░░;",
    r"        /░░░░░░|░░░░░░\.",
    r"       (_/'.░ ░░░ ░.'\_)",
    r'        \\  `""`""`     //',
    r"         \\          //",
    r"           ':.     .:'",
]


# ---------- algoritmo genetico (mesma ideia do G.py) ----------

def fitness(rgb):
    return 1 - sum(rgb) / 765


def novo_besouro():
    return [random.randint(0, 255) for _ in range(3)]


def cruzar(pai, mae):
    return [random.choice((p, m)) for p, m in zip(pai, mae)]


def mutar(b):
    if random.random() < 0.1:
        i = random.randrange(3)
        b[i] = max(0, min(255, b[i] + random.randint(-255, 255)))
    return b


def proxima_geracao(pop):
    pesos = [fitness(b) + 1e-6 for b in pop]
    melhor = max(pop, key=fitness)
    nova = [melhor[:]]  # elitismo
    while len(nova) < len(pop):
        pai, mae = random.choices(pop, weights=pesos, k=2)
        nova.append(mutar(cruzar(pai, mae)))
    return nova


# ---------- SVG ----------

def esc(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return s.replace(" ", "\u00a0")  # espaco fixo: o SVG nao colapsa os espacos


def hexcor(rgb):
    return "#%02x%02x%02x" % tuple(rgb)


def clarear(rgb, f=0.55):
    return [int(c + (255 - c) * f) for c in rgb]


def besouro_svg(x, y, rgb, legenda):
    cor = hexcor(rgb)
    partes = []
    for i, linha in enumerate(BESOURO):
        c = hexcor(clarear(rgb)) if i == 3 else cor
        partes.append(
            f'<text x="{x}" y="{y + i * LH}" fill="{c}">{esc(linha)}</text>'
        )
    partes.append(
        f'<text x="{x + 16 * CW}" text-anchor="middle" y="{y + len(BESOURO) * LH + 12}" '
        f'class="leg">{esc(legenda)}</text>'
    )
    return "\n".join(partes)


FS = 10          # tamanho da fonte
CW = FS * 0.6    # largura de um caractere monoespacado
LH = FS * 1.2    # altura da linha
COL_W = 34 * CW
ROW_H = len(BESOURO) * LH + 34
POR_LINHA = 5
MARGEM = 24


def main():
    random.seed(SEED)
    pop = [novo_besouro() for _ in range(TAM_POP)]
    amostras = []
    for g in range(max(GERACOES_MOSTRADAS) + 1):
        if g in GERACOES_MOSTRADAS:
            # besouro mediano da geracao: representa bem a populacao
            mediano = sorted(pop, key=fitness)[len(pop) // 2]
            amostras.append((g, mediano[:]))
        pop = proxima_geracao(pop)

    linhas = (len(amostras) + POR_LINHA - 1) // POR_LINHA
    w = int(MARGEM * 2 + POR_LINHA * COL_W)
    h = int(MARGEM * 2 + 28 + linhas * ROW_H)

    corpo = []
    for k, (g, rgb) in enumerate(amostras):
        x = MARGEM + (k % POR_LINHA) * COL_W
        y = MARGEM + 40 + (k // POR_LINHA) * ROW_H
        corpo.append(besouro_svg(x, y, rgb, f"geração {g}"))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>
  text {{ font-family: 'DejaVu Sans Mono', Menlo, Consolas, monospace; font-size: {FS}px; white-space: pre; }}
  .leg {{ fill: #6e7781; font-size: 11px; }}
  .tit {{ fill: #57606a; font-size: 12px; letter-spacing: 1px; }}
</style>
<rect width="{w}" height="{h}" rx="10" fill="#f6f8fa" stroke="#d0d7de"/>
<text x="{MARGEM}" y="{MARGEM + 6}" class="tit">SELEÇÃO NATURAL · {TAM_POP} BESOUROS · FITNESS = ESCURIDÃO DA CARAPAÇA</text>
{chr(10).join(corpo)}
</svg>
"""
    os.makedirs("assets", exist_ok=True)
    with open("assets/besouros.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("assets/besouros.svg gerado")


if __name__ == "__main__":
    main()
