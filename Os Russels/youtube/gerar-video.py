#!/usr/bin/env python3
"""Gera o vídeo de YouTube de um capítulo do audiolivro.

Layout (template da autora, Figma "Romance de bolso"): fundo escuro com brilho
magenta em cima e azul embaixo, card arredondado com a imagem do capítulo, logo
Romance no Bolso sobre o card, player de vidro com ondas sonoras que correm
conforme o áudio, e o título do capítulo embaixo.

Uso:
  python3 gerar-video.py --cap 1 --imagem cap01.png --audio cap01.mp3 --saida cap01.mp4
  python3 gerar-video.py --cap 1 --imagem cap01.png --audio cap01.mp3 --preview quadro.png
"""
import argparse, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(AQUI, "assets")
LIVRO = os.path.join(AQUI, "..", "livro-01-o-afilhado")

W, H, FPS = 1920, 1080, 25
FUNDO = (21, 20, 16)
CARD = (546, 187, 1375, 800)          # x0, y0, x1, y1 da imagem
CARD_R = 70
PLAYER = (560, 748, 1360, 898)
PLAYER_R = 75
PLAY_C, PLAY_R = (633, 823), 37
ONDA = (712, 1306)                    # faixa horizontal das barras
ONDA_CY, ONDA_MEIA = 823, 31          # centro vertical e meia-altura máxima
BARRA_W, BARRA_PASSO = 3, 6
BARRA_SEG = 0.08                      # cada barra = 80 ms de áudio
TITULO_Y = 948


def titulo_do_capitulo(n):
    for f in sorted(os.listdir(LIVRO)):
        if f.startswith(f"capitulo-{n:02d}-"):
            with open(os.path.join(LIVRO, f), encoding="utf-8") as fh:
                for linha in fh:
                    m = re.match(r"#+\s*Cap[ií]tulo\s+\d+\s*[—–-]\s*(.+)", linha)
                    if m:
                        return m.group(1).strip()
    sys.exit(f"título do capítulo {n} não encontrado")


def mascara_arredondada(w, h, r, escala=4):
    m = Image.new("L", (w * escala, h * escala), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * escala - 1, h * escala - 1), r * escala, fill=255)
    return m.resize((w, h), Image.LANCZOS)


def brilho(cx, cy, rx, ry, cor, alfa, blur):
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(camada).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=cor + (alfa,))
    return camada.filter(ImageFilter.GaussianBlur(blur))


def cobrir(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def montar_fundo(imagem, cap, titulo):
    base = Image.new("RGBA", (W, H), FUNDO + (255,))
    base.alpha_composite(brilho(960, 170, 470, 260, (200, 10, 90), 200, 120))
    base.alpha_composite(brilho(960, 900, 430, 120, (40, 80, 200), 150, 90))

    # sombra do card
    cx0, cy0, cx1, cy1 = CARD
    cw, ch = cx1 - cx0, cy1 - cy0
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle((cx0, cy0 + 20, cx1, cy1 + 20), CARD_R, fill=(0, 0, 0, 160))
    base.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(30)))

    foto = cobrir(Image.open(imagem).convert("RGB"), cw, ch)
    base.paste(foto, (cx0, cy0), mascara_arredondada(cw, ch, CARD_R))

    # player de vidro: o que está atrás, desfocado e escurecido, + brilho azul embaixo
    px0, py0, px1, py1 = PLAYER
    pw, ph = px1 - px0, py1 - py0
    atras = base.crop(PLAYER).filter(ImageFilter.GaussianBlur(22))
    vidro = Image.alpha_composite(atras, Image.new("RGBA", (pw, ph), (16, 14, 13, 200)))
    grad = np.zeros((ph, pw, 4), np.uint8)
    t = np.clip((np.arange(ph) - ph * 0.35) / (ph * 0.65), 0, 1) ** 1.3
    xs = np.abs(np.arange(pw) - pw / 2) / (pw / 2)
    a = (t[:, None] * np.clip(1.15 - xs[None, :] ** 2, 0, 1) * 200).astype(np.uint8)
    grad[..., 0], grad[..., 1], grad[..., 2], grad[..., 3] = 35, 70, 165, a
    vidro = Image.alpha_composite(vidro, Image.fromarray(grad, "RGBA"))
    m = mascara_arredondada(pw, ph, PLAYER_R)
    base.paste(vidro, (px0, py0), m)
    borda = Image.new("RGBA", (pw * 4, ph * 4), (0, 0, 0, 0))
    ImageDraw.Draw(borda).rounded_rectangle((2, 2, pw * 4 - 3, ph * 4 - 3), PLAYER_R * 4,
                                            outline=(255, 255, 255, 55), width=6)
    base.alpha_composite(borda.resize((pw, ph), Image.LANCZOS), (px0, py0))

    # botão play
    d = Image.new("RGBA", (W * 1, H * 1), (0, 0, 0, 0))
    x, y = PLAY_C
    dd = ImageDraw.Draw(d)
    dd.ellipse((x - PLAY_R, y - PLAY_R, x + PLAY_R, y + PLAY_R), fill=(95, 95, 95, 150))
    dd.polygon([(x - 10, y - 15), (x - 10, y + 15), (x + 15, y)], fill=(35, 32, 32, 230))
    base.alpha_composite(d)

    # logo
    logo = Image.open(os.path.join(ASSETS, "logo-romance-no-bolso.png")).convert("RGBA")
    logo = logo.resize((278, 124), Image.LANCZOS)
    base.alpha_composite(logo, (960 - 129, 106))

    # título
    fonte = ImageFont.truetype(os.path.join(ASSETS, "Urbanist-Light.ttf"), 44)
    texto = f"Capítulo {cap:02d} - {titulo}"
    dt = ImageDraw.Draw(base)
    bw = dt.textlength(texto, font=fonte)
    dt.text((960 - bw / 2, TITULO_Y), texto, font=fonte, fill=(245, 245, 248, 255), anchor="lm")
    return base.convert("RGB")


def envelope(audio):
    sr = 16000
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", audio, "-ac", "1", "-ar", str(sr),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    s = np.frombuffer(raw, np.float32)
    n = int(sr * BARRA_SEG)
    k = len(s) // n
    rms = np.sqrt(np.mean(s[: k * n].reshape(k, n) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    v = np.clip((db + 48) / 36, 0, 1) ** 1.4
    # um pouco de variação entre barras vizinhas, como no mockup
    rng = np.random.default_rng(7)
    v = v * (0.75 + 0.25 * rng.random(len(v)))
    return v, len(s) / sr


def quadro_onda(env, t, larg, alt):
    """RGBA da faixa de ondas no instante t: barras entram pela direita."""
    img = np.zeros((alt, larg, 4), np.uint8)
    nbar = larg // BARRA_PASSO + 2
    pos = t / BARRA_SEG
    k_ult = int(pos)
    frac = pos - k_ult
    cy = alt // 2
    for j in range(nbar):
        k = k_ult - j
        x = int(larg - BARRA_W - (j + frac) * BARRA_PASSO)
        if x < 0:
            break
        v = env[k] if 0 <= k < len(env) else 0.0
        if v < 0.06:  # silêncio = pontinho
            img[cy - 1:cy + 2, x:x + 2] = (255, 255, 255, 230)
            continue
        h = max(3, int(v * ONDA_MEIA))
        img[cy - h:cy + h + 1, x:x + BARRA_W] = (255, 255, 255, 245)
    # esmaecer as pontas
    borda = 40
    f = np.ones(larg)
    f[:borda] = np.linspace(0, 1, borda)
    img[..., 3] = (img[..., 3] * f[None, :]).astype(np.uint8)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", type=int, required=True)
    ap.add_argument("--imagem", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--saida")
    ap.add_argument("--preview", help="salva só um quadro PNG (t=60s) e sai")
    a = ap.parse_args()

    titulo = titulo_do_capitulo(a.cap)
    fundo = montar_fundo(a.imagem, a.cap, titulo)
    env, dur = envelope(a.audio)
    larg, alt = ONDA[1] - ONDA[0], ONDA_MEIA * 2 + 6
    ox, oy = ONDA[0], ONDA_CY - alt // 2

    if a.preview:
        q = fundo.convert("RGBA")
        q.alpha_composite(Image.fromarray(quadro_onda(env, min(60, dur / 2), larg, alt), "RGBA"), (ox, oy))
        q.convert("RGB").save(a.preview)
        print(a.preview)
        return

    fundo_png = a.saida + ".fundo.png"
    fundo.save(fundo_png)
    cmd = ["ffmpeg", "-y", "-v", "error", "-stats",
           "-loop", "1", "-framerate", str(FPS), "-i", fundo_png,
           "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{larg}x{alt}", "-r", str(FPS), "-i", "-",
           "-i", a.audio,
           "-filter_complex", f"[0:v][1:v]overlay={ox}:{oy}:shortest=1,format=yuv420p[v]",
           "-map", "[v]", "-map", "2:a",
           "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage", "-crf", "22",
           "-g", str(FPS * 4), "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
           "-movflags", "+faststart", "-shortest", a.saida]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(np.ceil(dur * FPS))
    for i in range(n):
        p.stdin.write(quadro_onda(env, i / FPS, larg, alt).tobytes())
    p.stdin.close()
    p.wait()
    os.remove(fundo_png)
    if p.returncode:
        sys.exit(p.returncode)
    print(a.saida)


if __name__ == "__main__":
    main()
