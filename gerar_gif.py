"""Gera assets/besouros.gif: besouros em ASCII, coloridos pelo algoritmo
genetico, andando pela tela em loop.

Uso: pip install pillow && python gerar_gif.py           (cores da evolucao)
     pip install pillow && python gerar_gif.py --acai    (tema acai)
"""
import os
import random
import sys

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

ACAI = "--acai" in sys.argv
if ACAI:
    FUNDO = (27, 10, 31)
    BORDA = (58, 29, 66)
    CORES_ACAI = [
        (201, 160, 220), (166, 108, 193), (142, 68, 173), (183, 132, 201),
        (155, 89, 182), (216, 180, 226), (124, 58, 150), (190, 120, 210),
        (148, 85, 170), (175, 140, 200),
    ]
else:
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


def clarear(rgb, f=0.45):
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


# no tema acai, cada besouro nasce com uma cor viva e evolui ate um tom de acai
CORES_INICIAIS = [
    (230, 57, 70), (42, 157, 143), (244, 162, 97), (69, 123, 157), (233, 196, 106),
    (168, 218, 220), (114, 183, 76), (231, 111, 81), (0, 150, 199), (255, 183, 3),
]
INICIO_EVOLUCAO = 8     # quadro em que as cores comecam a mudar
DURACAO_EVOLUCAO = 40   # quadros que cada besouro leva para virar acai
ATRASO_ENTRE = 3        # cada besouro comeca um pouco depois do anterior
DEGRAUS = 16            # tons intermediarios da transicao


def mistura(a, b, f):
    return tuple(int(round(x + (y - x) * f)) for x, y in zip(a, b))


def progresso(t, k):
    f = (t - INICIO_EVOLUCAO - k * ATRASO_ENTRE) / DURACAO_EVOLUCAO
    f = max(0.0, min(1.0, f))
    f = f * f * (3 - 2 * f)  # suaviza o inicio e o fim
    return round(f * DEGRAUS) / DEGRAUS


def main():
    cores = CORES_ACAI if ACAI else cores_da_evolucao()
    cache = {}

    def sprite(rgb, pose):
        if (rgb, pose) not in cache:
            cache[(rgb, pose)] = desenhar_besouro(rgb, pose)
        return cache[(rgb, pose)]

    def cor_no_quadro(k, t):
        if not ACAI:
            return tuple(cores[k])
        return mistura(CORES_INICIAIS[k], cores[k], progresso(t, k))

    # cada coluna tem dois besouros, a meio periodo de distancia
    besouros = []
    for k in range(len(cores)):
        col = k % COLUNAS
        x = 24 + col * (LARG_BESOURO + 16) - 10
        y0 = (k // COLUNAS) * (PERIODO / 2) + col * 57
        fase = (col * 3 + k // COLUNAS) % 2  # patas fora de sincronia
        besouros.append((k, x, y0, fase))

    quadros = []
    for t in range(QUADROS):
        q = Image.new("RGB", (LARGURA, ALTURA), FUNDO)
        usadas = [FUNDO, BORDA]
        for k, x, y0, fase in besouros:
            pose = ((t // TROCA_PATA) + fase) % 2
            rgb = cor_no_quadro(k, t)
            usadas += [rgb, clarear(rgb)]
            spr = sprite(rgb, pose)
            y = (y0 - t * PASSO) % PERIODO - (ALT_BESOURO + 70) + 20
            for yy in (y, y + PERIODO):
                if -ALT_BESOURO - 8 < yy < ALTURA:
                    q.paste(spr, (int(x), int(yy)), spr)
        ImageDraw.Draw(q).rounded_rectangle(
            (0, 0, LARGURA - 1, ALTURA - 1), radius=10, outline=BORDA
        )
        # paleta com as cores exatas deste quadro (sem pontilhado)
        tons = list(dict.fromkeys(usadas))
        pal = Image.new("P", (1, 1))
        flat = [v for c in tons for v in c]
        pal.putpalette(flat + flat[:3] * (256 - len(tons)))
        quadros.append(q.quantize(palette=pal, dither=Image.Dither.NONE))

    os.makedirs("assets", exist_ok=True)
    saida = "assets/besouros-acai.gif" if ACAI else "assets/besouros.gif"
    quadros[0].save(
        saida, save_all=True, append_images=quadros[1:],
        duration=DURACAO_MS, loop=0, optimize=True, disposal=1,
    )
    print(saida, "gerado")


if __name__ == "__main__":
    main()
