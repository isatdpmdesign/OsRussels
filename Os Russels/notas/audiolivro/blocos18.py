"""Cap 18: regera os diálogos (sem o trecho Josh/Aurora da janela) em blocos contínuos,
multi-speaker, e recorta cada fala de volta para o seu {slug}.seg.wav."""
import json, base64, subprocess, os, sys, re, difflib, unicodedata, time
import numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts18"
OUT = BASE + "/blocos"; os.makedirs(OUT, exist_ok=True)
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
VOZ = {"Aurora": "Leda", "Vibêke": "Laomedeia", "Eleonora": "Gacrux", "Senhora Lundgren": "Sulafat"}
GERAL = ("Leia em português do Brasil, com sotaque brasileiro, como uma cena de audiolivro de romance de época, "
         "interpretada por duas atrizes, com naturalidade, como conversa de verdade, sem ler. ")
BLOCOS = {
 "B1": ("Fim de tarde, no quarto de Aurora. Vibêke, a prima de dezenove anos, é alegre, espontânea, fala com entusiasmo. "
        "Aurora responde seca, rápida, mas com carinho escondido.",
        [("i004","Vibêke","O verde ou o lilás?"),("i005","Aurora","E é pra quem?"),("i006","Vibêke","Pra mim! Pro baile."),
         ("i008","Aurora","O verde, com certeza."),("i009","Vibêke","Por quê? Me conta tudo."),
         ("i010","Aurora","Porque o lilás é... é um vestido que pede que olhem pra você. E você já vai chamar atenção sem ele."),
         ("i012","Vibêke","Você está dizendo isso como prima ou como conselheira?"),
         ("i013","Aurora","Como prima. Eu tenho certeza de que você não vai querer chamar atenção, por causa do Lauritz. Estou certa?"),
         ("i014","Vibêke","Está certa, sim. Então é o verde. Se você estivesse me aconselhando como conselheira, eu ia saber que era o que você não escolheu. Mas como prima, eu confio.")]),
 "B2": ("Dentro da carruagem, a caminho do baile. Eleonora, a tia, senhora madura, voz grave e contida, elegante, com humor seco. "
        "Vibêke, a sobrinha, alegre e sincera, sem filtro.",
        [("i020","Eleonora","Os Lundgren são boa gente. A senhora Lundgren foi colega de infância da minha mãe. O salão deles é o segundo maior da cidade, depois do Teatro Real. Não fique impressionada."),
         ("i021","Vibêke","Eu vou ficar impressionada."),("i022","Eleonora","Então fique sem deixar transparecer."),
         ("i023","Vibêke","Tia, sabe de uma coisa?"),("i024","Eleonora","Sim, querida?"),("i025","Vibêke","Eu não consigo.")]),
 "B3a": ("Entrada do salão de baile. A senhora Lundgren, anfitriã, senhora madura, calorosa e elegante. Eleonora, senhora madura, voz grave e contida, apresentando a sobrinha.",
        [("i028","Senhora Lundgren","Então esta é a sobrinha de Viborg."),("i029","Eleonora","Vibêke Bierg. A filha da Karoline.")]),
 "B3b": ("Entrada do salão de baile. A senhora Lundgren, anfitriã, senhora madura, lembra o passado com um sorriso de verdade. Vibêke, jovem, alegre, espirituosa.",
        [("i031","Senhora Lundgren","A Karoline. Eu dancei em roda com a sua mãe num baile em Ólborg, quando a gente tinha vinte anos. Ela pisou no meu pé três vezes."),
         ("i032","Vibêke","A mamãe ainda pisa no pé do papai três vezes por dança!"),
         ("i033","Senhora Lundgren","Então não mudou nada. Senhor Rássel. Sejam bem-vindos.")]),
 "B4": ("No salão, sentadas lado a lado, falando num tom mais baixo, sem sussurrar, para ninguém ouvir. Eleonora, a mãe, grave, contida, observadora, sem olhar para a filha. "
        "Aurora, a filha, disfarçando o incômodo, respostas curtas e educadas.",
        [("i040","Eleonora","Aurora, querida."),("i041","Aurora","Sim, mamãe?"),("i042","Eleonora","Você está bem?"),
         ("i043","Aurora","Estou, sim."),("i044","Eleonora","Você está se abanando com a energia de quem está prestes a desmaiar."),
         ("i045","Aurora","É que está calor."),("i047","Eleonora","Está calor para todo mundo, querida. Mas só você está se abanando desse jeito."),
         ("i049","Aurora","Melhor assim?"),("i050","Eleonora","Melhor, sim.")]),
 "B5": ("Perto de uma janela do salão, no intervalo entre duas danças. Vibêke, a prima, nervosa e falante, ri de si mesma, fala depressa. "
        "Aurora, mais contida, divertida por dentro, carinhosa.",
        [("i056","Vibêke","Aurora! Eu acabei de contar do Lauritz pra senhora Lundgren."),("i057","Aurora","Você contou mesmo?"),
         ("i059","Vibêke","Eu acho que ela nem tinha perguntado. Acho que eu enfiei a história sem precisar. Eu vou ter que aprender a esperar."),
         ("i060","Aurora","Foi assim no almoço também?"),
         ("i061","Vibêke","No almoço foi pior. Eu falei do Lauritz três vezes pra mãe de uma moça que eu nem sei o nome. Pra moça eu já contei. Pro senhor Holst também. Acho que eu estou nervosa. Quando eu fico nervosa, eu falo do Lauritz. É um vício."),
         ("i062","Aurora","É um vício útil."),("i063","Vibêke","E por que seria útil?"),
         ("i065","Aurora","Porque metade do salão já sabe que você tem dono. E isso vai te poupar de um monte de conversa boba."),
         ("i067","Vibêke","Eu não tinha pensado nisso."),("i068","Aurora","Eu sei que não."),
         ("i069","Vibêke","E agora, você está sendo prima ou conselheira?"),("i070","Aurora","As duas coisas."),
         ("i072","Vibêke","Você é boa, sabia?")]),
}

def gera(bid):
    direc, linhas = BLOCOS[bid]
    falantes = sorted({f for _, f, _ in linhas})
    texto = GERAL + direc + "\n\n" + "\n".join(f"{f}: {t}" for _, f, t in linhas)
    body = {"contents": [{"parts": [{"text": texto}]}], "generationConfig": {"responseModalities": ["AUDIO"],
            "speechConfig": {"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": [
                {"speaker": f, "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOZ[f]}}} for f in falantes]}}}}
    req = f"{OUT}/{bid}.req"; js = f"{OUT}/{bid}.json"; json.dump(body, open(req, "w"))
    k = os.environ.get("GKEY"); u = URL + ("?key=" + k if k else "")
    for t in range(3):
        subprocess.run(["curl", "-sS", "-X", "POST", u, "-H", "Content-Type: application/json", "-d", "@" + req, "-o", js], timeout=300)
        d = json.load(open(js))
        try:
            pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            a = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
            sf.write(f"{OUT}/{bid}.wav", a, SR); return a
        except Exception:
            print("falhou", bid, json.dumps(d)[:200]); time.sleep(10)
    return None

def norm(t):
    t = unicodedata.normalize("NFKD", t.lower()); t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", t).split()

_m = None
def recorta(bid, a):
    global _m
    from faster_whisper import WhisperModel
    if _m is None: _m = WhisperModel("small", device="cpu", compute_type="int8")
    _, linhas = BLOCOS[bid]
    segs, _ = _m.transcribe(a, language="pt", beam_size=5, word_timestamps=True)
    hw = [(w.word, w.start, w.end) for s in segs for w in s.words]
    hyp = [];
    for w, s, e in hw:
        for x in norm(w): hyp.append((x, s, e))
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
    for i, (slug, _, _) in enumerate(linhas):
        p = a[int(cuts[i] * SR):int(cuts[i + 1] * SR)]
        sf.write(f"{OUT}/{slug}.seg.wav", p, SR)
    print("ok", bid, [round(c, 1) for c in cuts])
    return True

if __name__ == "__main__":
    for bid in (sys.argv[1:] or BLOCOS):
        a = gera(bid)
        if a is None: print("ABORT", bid); break
        recorta(bid, a)
