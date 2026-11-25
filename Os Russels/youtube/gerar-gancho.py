#!/usr/bin/env python3
"""Fala de gancho do fim do vídeo, na voz da narradora (Gemini, Vindemiatrix + filtro grave).
  python3 gerar-gancho.py 8 9 10   -> ganchos/capNN.wav (chama para o capítulo NN+1)"""
import base64, json, os, re, subprocess, sys, time
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
LIVRO = os.path.join(AQUI, "..", "livro-01-o-afilhado")
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
NARR_AF = "asetrate=24000*0.88,aresample=24000,atempo=1.1364"

def titulo(n):
    for f in sorted(os.listdir(LIVRO)):
        if f.startswith(f"capitulo-{n:02d}-"):
            for l in open(os.path.join(LIVRO, f), encoding="utf-8"):
                m = re.match(r"#+\s*Cap[ií]tulo\s+\d+\s*[—–-]\s*(.+)", l)
                if m: return m.group(1).strip()

def tts(texto, saida):
    body = {"contents": [{"parts": [{"text": texto}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
              "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Vindemiatrix"}}}}}
    for t in range(4):
        r = subprocess.run(["curl", "-sS", "-X", "POST", URL, "-H", "Content-Type: application/json",
                            "-H", "x-goog-api-key: dummy", "-d", json.dumps(body)], capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            raw = saida + ".raw"
            open(raw, "wb").write(pcm)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", raw,
                            "-af", NARR_AF, saida], check=True)
            os.remove(raw); return True
        except Exception:
            print("tentativa", t, r.stdout[:200]); time.sleep(15)
    return False

for a in sys.argv[1:]:
    n = int(a); prox = titulo(n + 1)
    texto = (f"Diga em português do Brasil, num tom caloroso e convidativo, sem pressa: "
             f"No próximo capítulo de O Afilhado... {prox}. Ouça agora, na playlist do canal Romance no Bolso.")
    if os.environ.get("EM_BREVE"):
        texto = ("Diga em português do Brasil, num tom caloroso e convidativo, sem pressa: "
                 f"O capítulo {n + 1} de O Afilhado chega em breve. Ative o sininho do canal Romance no Bolso, "
                 "para ouvir assim que sair.")
    out = os.path.join(AQUI, "ganchos", f"cap{n:02d}.wav")
    print(n, prox, tts(texto, out))
