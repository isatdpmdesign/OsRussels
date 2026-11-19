"""Cap 19: gera os diálogos Josh/Aurora em blocos contínuos (multi-speaker) e recorta
cada fala de volta para o seu {slug}.seg.wav, que o gerar-cap19.py costura com a narração.

Uso:  python3 blocos19.py [BLOCO ...] [--recortar] [--takes N]
      --recortar  só recorta de novo um bloco já gerado (custo zero)
      --takes N   gera N takes de cada bloco (blocoN.t1.wav ...) para a autora escolher;
                  o take 1 é o que entra no capítulo até ela escolher outro.
"""
import json, base64, subprocess, os, sys, re, difflib, unicodedata, time
import numpy as np, soundfile as sf

import importlib.util
_spec = importlib.util.spec_from_file_location("cap19", os.path.join(os.path.dirname(os.path.abspath(__file__)), "gerar-cap19.py"))
G = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(G)

BASE = os.environ.get("GTTS_BASE", "/tmp/gtts") + "/gtts19"
OUT = BASE + "/blocos"; os.makedirs(OUT, exist_ok=True)
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
VOZ = {"Josh": "Zubenelgenubi", "Aurora": "Leda"}
NOME = {"JOSH": "Josh", "AU": "Aurora"}

GERAL = ("Leia em português do Brasil, com sotaque brasileiro, como uma cena de audiolivro de romance de época, "
         "interpretada por um ator e uma atriz, com naturalidade, como conversa de verdade, sem ler, em ritmo calmo, com pausas entre as falas. "
         "Madrugada, na sala de estar escura de um casarão, à luz de uma vela; os dois conversam em volume normal, médio, "
         "no mesmo nível um do outro: não sussurram, não cochicham, não falam alto. Josh tem vinte e um anos: voz de homem jovem, masculina, grave e aveludada, voz de peito, a mesma do começo ao fim, nunca fina, nunca fanha, nunca feminina; "
         "nunca animado, nunca simpático, nunca leve, nunca recitando frases; ele respira antes de falar e as "
         "reticências são hesitações de verdade. Aurora tem dezoito anos: voz suave, sem nenhuma infantilidade. ")

# bloco: (primeira fala, última fala, direção de cena daquele momento)
FAIXAS = {
 "A1a": ("m011", "m017", "Ele acabou de descer e a encontrou ali sem esperar; está sem jeito, contido, gentil. "
         "Ela, sentada no chão com o livro do irmão que morreu, está vulnerável e calma."),
 "A1b": ("m019", "m031", "Os dois lembram da noite em que ele a viu chorar, logo que chegou. Ele fala devagar, com "
         "ternura contida, escolhendo cada palavra; ela pergunta com dúvida verdadeira, querendo entender."),
 "A2":  ("m033", "m050", "A conversa fica mais íntima. Ele confessa que se importava com ela, com cuidado e um pouco "
         "de vergonha; ela provoca de leve, com meio sorriso, até rir de verdade. Na última pergunta dela a leveza some."),
 "A3":  ("m053", "m069", "A tensão sobe. Josh na mesma voz jovem das falas anteriores, nunca mais velho nem mais grosso. Ela cobra, com afronta e ciúme mal escondido; ele responde intenso, "
         "olhando para ela, sem levantar a voz. No fim ela explode, irritada."),
 "S1":  ("r071", "r090", "Briga contida. Ela está ferida, desafiadora, com angústia crescente. Ele está no limite: "
         "quer fugir dali porque a deseja e não pode ficar; cada resposta sai pesada, com o desejo segurado na voz."),
 "S2":  ("r093", "r111", "Ele diz, pela primeira vez em voz alta, as três razões pelas quais não pode ficar com ela. "
         "Volume normal, sem cochichar, na mesma voz grave das falas anteriores; vulnerável, falhando em algumas palavras, parando no meio da frase. Não é discurso: é um "
         "homem confessando o que o machuca. Ela escuta; quando fala, é insegura e suave, e no fim decidida."),
 "S3":  ("r115", "r129", "Agora ela responde de pé, firme, decidida, com uma afronta carinhosa; a voz dela não treme. "
         "Ele chega ao próprio limite: voz intensa, quase rachando, carregada de desejo, tentando resistir "
         "e já sem conseguir."),
 "S4":  ("r137", "r142", "Os dois estão a um palmo um do outro: o momento antes do primeiro beijo e logo depois dele. "
         "Falam quase encostados, com a respiração curta. Ele: grave, rouco de desejo, hesitante, cheio de necessidade. "
         "Ela: suave, decidida, ofegante."),
 "S5":  ("r151", "r160", "Logo depois do beijo, testa contra testa, os dois sem fôlego. Ele fala com ternura e medo do "
         "dia seguinte, a voz emocionada, quase embargada; ela, suave e firme, o acalma. Despedida terna."),
}

_PREF = re.compile(r"^Diga[^:]*:\s*")
def _limpa(t): return _PREF.sub("", t).strip()

def montar():
    ordem = [s[0] for s in G.SEG]
    por = {s[0]: s for s in G.SEG}
    blocos = {}
    for bid, (a, b, direc) in FAIXAS.items():
        # corta no take colado e em pedaços de no máximo 8 falas (autora, 19/11: bloco longo
        # faz o Josh derivar para voz de moça)
        pedacos = [[]]
        for sl in ordem[ordem.index(a):ordem.index(b) + 1]:
            _, vk, t, _ = por[sl]
            if t.startswith("CLIP:"):
                pedacos.append([])
            elif vk in NOME:
                pedacos[-1].append((sl, NOME[vk], _limpa(t)))
        finais = []
        for pc in pedacos:
            if not pc: continue
            n = -(-len(pc) // 7)
            tam = -(-len(pc) // n)
            finais += [pc[i:i + tam] for i in range(0, len(pc), tam)]
        for i, pc in enumerate(finais):
            blocos[bid if len(finais) == 1 else f"{bid}.{i + 1}"] = (direc, pc)
    return blocos

BLOCOS = montar()

def gera(bid, sufixo=""):
    direc, linhas = BLOCOS[bid]
    texto = GERAL + direc + "\n\n" + "\n".join(f"{f}: {t}" for _, f, t in linhas)
    body = {"contents": [{"parts": [{"text": texto}]}], "generationConfig": {"responseModalities": ["AUDIO"],
            "speechConfig": {"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": [
                {"speaker": f, "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOZ[f]}}} for f in VOZ]}}}}
    req = f"{OUT}/{bid}{sufixo}.req"; js = f"{OUT}/{bid}{sufixo}.json"; json.dump(body, open(req, "w"))
    k = os.environ.get("GKEY"); u = URL + ("?key=" + k if k else "")
    for t in range(3):
        subprocess.run(["curl", "-sS", "-X", "POST", u, "-H", "Content-Type: application/json", "-d", "@" + req, "-o", js], timeout=300)
        d = json.load(open(js))
        try:
            pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            a = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
            chars = sum(len(t) for _, _, t in linhas)
            if len(a) / SR > chars / 6 + 8:  # o modelo "embalou" (cap 19, S3.3 saiu com 8 min): refaz
                print("LONGO DEMAIS", bid, round(len(a) / SR), "s para", chars, "caracteres"); continue
            sf.write(f"{OUT}/{bid}{sufixo}.wav", a, SR); return a
        except Exception:
            dump = json.dumps(d)
            print("falhou", bid, dump[:200])
            if "RESOURCE_EXHAUSTED" in dump: print("COTA_ESGOTADA"); sys.exit(3)
            time.sleep(10)
    return None

LIMITE_JOSH_HZ = 120
PISO_JOSH_HZ = 85  # abaixo disso ele soa grosso, mais velho (cap 19, 'Não. Não consegui.')  # o Josh fica por volta de 100 Hz; acima de 130 já soa feminino

def f0(a, sr=SR):
    fr = []; n = 2048
    for i in range(0, len(a) - n, 1024):
        x = a[i:i + n]
        if np.sqrt((x ** 2).mean()) < 0.03: continue
        c = np.correlate(x, x, "full")[n - 1:]; lo, hi = sr // 350, sr // 60
        fr.append(sr / (lo + np.argmax(c[lo:hi])))
    return int(np.median(fr)) if fr else 0

def ouvir(a):
    global _m
    from faster_whisper import WhisperModel
    if _m is None: _m = WhisperModel("small", device="cpu", compute_type="int8")
    a16 = np.interp(np.arange(0, len(a), SR / 16000), np.arange(len(a)), a).astype(np.float32)
    return " ".join(x.text for x in _m.transcribe(a16, language="pt")[0])

def norm(t):
    t = unicodedata.normalize("NFKD", t.lower()); t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", t).split()

_m = None
def recorta(bid, a):
    global _m
    from faster_whisper import WhisperModel
    if _m is None: _m = WhisperModel("small", device="cpu", compute_type="int8")
    _, linhas = BLOCOS[bid]
    a16 = np.interp(np.arange(0, len(a), SR / 16000), np.arange(len(a)), a).astype(np.float32)  # whisper quer 16 kHz
    segs, _ = _m.transcribe(a16, language="pt", beam_size=5, word_timestamps=True)
    hyp = [(x, w.start, w.end) for s in segs for w in s.words for x in norm(w.word)]
    exp = [(x, i) for i, (_, _, t) in enumerate(linhas) for x in norm(t)]
    sm = difflib.SequenceMatcher(None, [x for x, _ in exp], [x for x, _, _ in hyp], autojunk=False)
    first = {}; last = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            li = exp[blk.a + k][1]; _, s, e = hyp[blk.b + k]
            first.setdefault(li, s); last[li] = e
    n = len(linhas); cuts = [0.0]
    for i in range(1, n):
        if i not in first or (i - 1) not in last:
            print("ALINHAMENTO FALHOU", bid, linhas[i][0]); return False
        cuts.append((last[i - 1] + first[i]) / 2)
    cuts.append(len(a) / SR)
    os.makedirs(f"{BASE}/anteriores", exist_ok=True)
    for i, (slug, _, _) in enumerate(linhas):
        if os.path.exists(f"{BASE}/{slug}.seg.wav") and not os.path.exists(f"{BASE}/anteriores/{slug}.seg.wav"):
            os.replace(f"{BASE}/{slug}.seg.wav", f"{BASE}/anteriores/{slug}.seg.wav")
        sf.write(f"{BASE}/{slug}.seg.wav", a[int(cuts[i] * SR):int(cuts[i + 1] * SR)], SR)
    print("ok", bid, [round(float(c), 1) for c in cuts])
    return True

if __name__ == "__main__":
    args = sys.argv[1:]
    takes = int(args[args.index("--takes") + 1]) if "--takes" in args else 1
    so_recorte = "--recortar" in args
    alvo = [k for x in args for k in BLOCOS if k == x or k.startswith(x + ".")] or list(BLOCOS)
    for bid in alvo:
        if so_recorte:
            a = sf.read(f"{OUT}/{bid}.wav", dtype="float32")[0]
        else:
            a = None
            for t in range(1, takes + 1):
                x = gera(bid, f".t{t}" if takes > 1 else "")
                if x is None: print("ABORT", bid); sys.exit(1)
                if a is None: a = x
            if takes > 1: sf.write(f"{OUT}/{bid}.wav", a, SR)
        if not recorta(bid, a) or so_recorte: continue
        for tent in range(4):  # timbre e o nome "Aurora": refaz o bloco se falhar
            prob = []
            for sl, f, t in BLOCOS[bid][1]:
                if f == "Aurora":  # falante trocado: a fala da Aurora saiu na voz do Josh
                    hz = f0(sf.read(f"{BASE}/{sl}.seg.wav", dtype="float32")[0])
                    if 0 < hz < 150: prob.append((sl, f"Aurora com {hz} Hz"))
                    continue
                if f != "Josh": continue  # Raj e outros não passam pela régua do Josh
                x = sf.read(f"{BASE}/{sl}.seg.wav", dtype="float32")[0]
                hz = f0(x)
                if hz > LIMITE_JOSH_HZ or 0 < hz < PISO_JOSH_HZ: prob.append((sl, f"{hz} Hz"))
                if "bibliotéca" in t and "biblioteca" not in norm(ouvir(x)): prob.append((sl, "biblioteca"))
                if "Aurôra" in t and "aurora" not in norm(ouvir(x)): prob.append((sl, "nome: " + ouvir(x)[:40]))
            if not prob: break
            if tent == 3: print("AINDA COM PROBLEMA (ouvir)", bid, prob); break
            print("REFAZENDO", bid, prob)
            a = gera(bid)
            if a is None or not recorta(bid, a): break
