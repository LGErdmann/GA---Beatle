"""Gera assets/besouros.gif: besouros em ASCII, coloridos pelo algoritmo
genetico, andando pela tela em loop.

Uso: pip install pillow && python gerar_gif.py
"""
import os
import random

from PIL import Image, ImageDraw, ImageFont

SEED = 7
TAM_POP = 50
GERACOES = [0, 1, 2, 3, 4, 5, 6, 8, 10, 14]   # uma cor por geracao

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
LINHAS_COM_PERNAS = {0, 6, 7, 8, 12, 13, 14}
LINHA_OLHOS = 3

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
    nova = [max(pop, key=fitness)[:]]  # elitismo
    while len(nova) < len(pop):
        pai, mae = random.choices(pop, weights=pesos, k=2)
        nova.append(mutar(cruzar(pai, mae)))
    return nova


def cores_da_evolucao():
    random.seed(SEED)
    pop = [novo_besouro() for _ in range(TAM_POP)]
    cores = []
    for g in range(max(GERACOES) + 1):
        if g in GERACOES:
            # besouro mediano: representa bem a populacao daquela geracao
            cores.append(tuple(sorted(pop, key=fitness)[len(pop) // 2]))
        pop = proxima_geracao(pop)
    return cores


# ---------- animacao ----------

FONTE = ImageFont.truetype("DejaVuSansMono.ttf", 12)
CW = FONTE.getlength("M")
LH = 14
LARG_BESOURO = int(32 * CW)
ALT_BESOURO = len(BESOURO) * LH

FUNDO = (246, 248, 250)
BORDA = (208, 215, 222)
COLUNAS = 5
LARGURA = COLUNAS * (LARG_BESOURO + 16) + 24
ALTURA = 380
PERIODO = 2 * (ALT_BESOURO + 70)  # dois besouros por coluna
QUADROS = 104
PASSO = PERIODO / QUADROS          # pixels por quadro (loop perfeito)
TROCA_PATA = 4                     # quadros por passo das patas
DURACAO_MS = 70


def clarear(rgb, f=0.55):
    return tuple(int(c + (255 - c) * f) for c in rgb)


def desenhar_besouro(rgb, pose):
    """Desenha um besouro; as patas da esquerda e da direita sobem e
    descem em oposicao conforme a pose (0 ou 1)."""
    img = Image.new("RGBA", (LARG_BESOURO, ALT_BESOURO + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.fontmode = "1"  # sem antialias: cores exatas no GIF
    dy = 4 if pose else -4
    for i, linha in enumerate(BESOURO):
        cor = clarear(rgb) if i == LINHA_OLHOS else rgb
        meio = len(linha.rstrip()) / 2 if i in (12, 13, 14) else 16
        for j, ch in enumerate(linha):
            if ch == " ":
                continue
            y = i * LH + 4
            eh_pata = i in LINHAS_COM_PERNAS and (
                (i == 0 and (j < 10 or j > 21))
                or (i in (6, 7, 8) and (j < 7 or j > 23))
                or (i >= 12 and ch not in '`"')
            )
            if eh_pata:
                y += dy if j < meio else -dy
            d.text((j * CW, y), ch, font=FONTE, fill=cor)
    return img


def main():
    cores = cores_da_evolucao()
    sprites = [[desenhar_besouro(c, p) for p in (0, 1)] for c in cores]

    # cada coluna tem dois besouros, a meio periodo de distancia
    besouros = []
    for k, _ in enumerate(cores):
        col = k % COLUNAS
        x = 24 + col * (LARG_BESOURO + 16) - 10
        y0 = (k // COLUNAS) * (PERIODO / 2) + col * 57
        fase = (col * 3 + k // COLUNAS) % 2  # patas fora de sincronia
        besouros.append((sprites[k], x, y0, fase))

    quadros = []
    for t in range(QUADROS):
        q = Image.new("RGB", (LARGURA, ALTURA), FUNDO)
        for spr, x, y0, fase in besouros:
            pose = ((t // TROCA_PATA) + fase) % 2
            y = (y0 - t * PASSO) % PERIODO - (ALT_BESOURO + 70) + 20
            for yy in (y, y + PERIODO):
                if -ALT_BESOURO - 8 < yy < ALTURA:
                    q.paste(spr[pose], (int(x), int(yy)), spr[pose])
        ImageDraw.Draw(q).rounded_rectangle(
            (0, 0, LARGURA - 1, ALTURA - 1), radius=10, outline=BORDA
        )
        quadros.append(q)

    # paleta unica para todos os quadros (sem tremido de cor)
    tons = [FUNDO, BORDA, (255, 255, 255)] + list(cores) + [clarear(c) for c in cores]
    pal = Image.new("P", (1, 1))
    flat = [v for c in tons for v in c]
    pal.putpalette(flat + flat[:3] * (256 - len(tons)))
    quadros = [q.quantize(palette=pal, dither=Image.Dither.NONE) for q in quadros]

    os.makedirs("assets", exist_ok=True)
    quadros[0].save(
        "assets/besouros.gif", save_all=True, append_images=quadros[1:],
        duration=DURACAO_MS, loop=0, optimize=True, disposal=1,
    )
    print("assets/besouros.gif gerado")


if __name__ == "__main__":
    main()
