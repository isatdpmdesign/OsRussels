#!/usr/bin/env python3
"""Miniatura chamativa (1280x720) de um capítulo para o YouTube.

Imagem em tela cheia, gancho grande em serifa itálica (uma palavra em magenta),
selo "CAPÍTULO N", selo "AUDIOLIVRO" e logo Romance no Bolso.

  python3 gerar-thumb.py --cap 3 --imagem imagens/cap03.jpg \
      --frase "Ela não sabia|que ele *estava ali*" --lado esquerda --foco 0.5 --saida thumb.png

--frase: linhas separadas por "|"; trecho entre *asteriscos* sai em magenta.
--lado: onde fica o texto (esquerda/direita), para não cobrir rosto.
--foco: 0..1, ponto horizontal da imagem que deve ficar em quadro no zoom.
"""
import argparse, os, re
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
A = lambda n: os.path.join(AQUI, "assets", n)
W, H = 1280, 720
MAGENTA = (255, 8, 100)
BRANCO = (255, 255, 255)


def enquadrar(img, zoom, foco_x, foco_y):
    s = max(W / img.width, H / img.height) * zoom
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = int(np.clip(foco_x * img.width - W / 2, 0, img.width - W))
    y = int(np.clip(foco_y * img.height - H / 2, 0, img.height - H))
    return img.crop((x, y, x + W, y + H))


def degrade(lado):
    xs = np.linspace(0, 1, W)
    if lado == "direita":
        xs = xs[::-1]
    ys = np.linspace(0, 1, H)
    a = np.clip(1.1 - xs * 1.6, 0, 1) ** 1.3                  # lado do texto
    v = np.clip((ys - 0.45) / 0.35, 0, 1)                     # só na metade de baixo
    b = np.clip((ys - 0.62) / 0.38, 0, 1) ** 1.6 * 150        # base escura
    alfa = np.maximum(a[None, :] * v[:, None] * 225, b[:, None]).astype(np.uint8)
    cam = np.zeros((H, W, 4), np.uint8)
    cam[..., :3] = (12, 6, 10)
    cam[..., 3] = alfa
    return Image.fromarray(cam, "RGBA")


def texto_com_sombra(base, xy, txt, fonte, cor, anchor="la"):
    sombra = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).text((xy[0] + 3, xy[1] + 5), txt, font=fonte, fill=(0, 0, 0, 220), anchor=anchor)
    base.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(base).text(xy, txt, font=fonte, fill=cor, anchor=anchor)


def selo(base, x, y, txt, fonte, fundo, cor):
    d = ImageDraw.Draw(base)
    l, t, r, b = d.textbbox((0, 0), txt, font=fonte)
    pw, ph = r - l + 36, b - t + 20
    d.rounded_rectangle((x, y, x + pw, y + ph), ph // 2, fill=fundo)
    d.text((x + 18 - l, y + 10 - t), txt, font=fonte, fill=cor)
    return pw, ph


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", type=int, required=True)
    ap.add_argument("--imagem", required=True)
    ap.add_argument("--frase", required=True)
    ap.add_argument("--lado", choices=["esquerda", "direita"], default="esquerda")
    ap.add_argument("--foco", type=float, default=0.5)
    ap.add_argument("--foco-y", type=float, default=0.42)
    ap.add_argument("--zoom", type=float, default=1.12)
    ap.add_argument("--saida", required=True)
    a = ap.parse_args()

    img = Image.open(a.imagem).convert("RGB")
    img = enquadrar(img, a.zoom, a.foco, a.foco_y)
    img = ImageEnhance.Contrast(img).enhance(1.12)
    img = ImageEnhance.Color(img).enhance(1.12)
    base = img.convert("RGBA")
    base.alpha_composite(degrade(a.lado))

    m = 56  # margem
    # selos no topo, do lado do texto
    fsel = ImageFont.truetype(A("Montserrat-ExtraBold.ttf"), 26)
    xsel = m if a.lado == "esquerda" else None
    w1, h1 = ImageDraw.Draw(base).textbbox((0, 0), f"CAPÍTULO {a.cap}", font=fsel)[2:]
    if xsel is None:
        xsel = W - m - (w1 + 36) - 14 - 180
    pw, ph = selo(base, xsel, m, f"CAPÍTULO {a.cap}", fsel, MAGENTA, BRANCO)
    selo(base, xsel + pw + 14, m, "🎧 AUDIOLIVRO".replace("🎧 ", ""), fsel, (255, 255, 255), (20, 14, 18))

    # logo no canto oposto ao texto
    logo = Image.open(A("logo-romance-no-bolso.png")).convert("RGBA")
    lw = 210
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    lx = W - m - lw + 10 if a.lado == "esquerda" else m - 10
    base.alpha_composite(logo, (lx, m - 14))

    # gancho
    linhas = a.frase.split("|")
    tam = 92 if max(len(re.sub(r"\*", "", l)) for l in linhas) <= 16 else 78
    f = ImageFont.truetype(A("PlayfairDisplay-BlackItalic.ttf"), tam)
    alt = int(tam * 1.08)
    y0 = H - m - alt * len(linhas) + 6
    for i, linha in enumerate(linhas):
        partes = re.split(r"(\*[^*]+\*)", linha)
        larg = sum(ImageDraw.Draw(base).textlength(p.strip("*"), font=f) for p in partes)
        x = m if a.lado == "esquerda" else W - m - larg
        for p in partes:
            if not p:
                continue
            cor = MAGENTA if p.startswith("*") else BRANCO
            t = p.strip("*")
            texto_com_sombra(base, (x, y0 + i * alt), t, f, cor)
            x += ImageDraw.Draw(base).textlength(t, font=f)

    # filete magenta acima do gancho
    xf = m if a.lado == "esquerda" else W - m - 90
    ImageDraw.Draw(base).rectangle((xf, y0 - 22, xf + 90, y0 - 16), fill=MAGENTA)
    base.convert("RGB").save(a.saida, quality=95)
    print(a.saida)


if __name__ == "__main__":
    main()
