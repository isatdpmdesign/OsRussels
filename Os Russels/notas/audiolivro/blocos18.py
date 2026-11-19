"""Cap 18: regera os diálogos (sem o trecho Josh/Aurora da janela) em blocos contínuos,
multi-speaker, e recorta cada fala de volta para o seu {slug}.seg.wav."""
import json, base64, subprocess, os, sys, re, difflib, unicodedata, time
import numpy as np, soundfile as sf

BASE = os.environ.get("GTTS_BASE", "/tmp/gtts") + "/gtts18"
OUT = BASE + "/blocos"; os.makedirs(OUT, exist_ok=True)
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
VOZ = {"Aurora": "Leda", "Vibêke": "Laomedeia", "Eleonora": "Gacrux", "Senhora Lundgren": "Sulafat", "Josh": "Zubenelgenubi"}
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
 "B6a1": ('Perto da janela de um salão de baile, num intervalo entre danças. Os dois conversam em volume normal, médio, no mesmo nível um do outro: não sussurram, não cochicham e não falam alto. É uma conversa comum, com um incômodo por baixo. Josh tem vinte e um anos: voz de homem jovem, masculina, natural, calma, atenciosa; nunca animado, nunca simpático demais, nunca recitando. Aurora tem dezoito anos: voz suave e firme, sem infantilidade; está com ciúme e finge que não, responde seca, às vezes com afronta.',
        [('i076b', 'Josh', 'Tudo bem?'), ('i077', 'Aurora', 'Tudo bem, Josh.'), ('i078', 'Josh', 'Antes da valsa, a sua mãe me pediu pra trazer uma taça de água pra você.'), ('i079', 'Aurora', 'A minha mãe te mandou aqui?'), ('i080', 'Josh', 'Mandou, sim. Foi ela quem pediu.'), ('i081', 'Aurora', 'E por que ela faria isso?')]),
 "B6a2": ('Perto da janela de um salão de baile, num intervalo entre danças. Os dois conversam em volume normal, médio, no mesmo nível um do outro: não sussurram, não cochicham e não falam alto. É uma conversa comum, com um incômodo por baixo. Josh tem vinte e um anos: voz de homem jovem, masculina, natural, calma, atenciosa; nunca animado, nunca simpático demais, nunca recitando. Aurora tem dezoito anos: voz suave e firme, sem infantilidade; está com ciúme e finge que não, responde seca, às vezes com afronta.',
        [('i083', 'Josh', 'Eu não sei. Talvez porque ela viu você sozinha na janela.'), ('i084', 'Aurora', 'Eu estou bem sozinha na janela.'), ('i085', 'Josh', 'Eu sei que está.'), ('i086', 'Aurora', 'Você pode dizer a ela que cumpriu o recado.'), ('i087', 'Josh', 'Tudo bem. Mas você não vai querer a água?'), ('i088', 'Aurora', 'Não, Josh. Eu mesma posso me servir, se eu quiser. Obrigada.')]),
 "B6a3": ('Perto da janela de um salão de baile, num intervalo entre danças. Os dois conversam em volume normal, médio, no mesmo nível um do outro: não sussurram, não cochicham e não falam alto. É uma conversa comum, com um incômodo por baixo. Josh tem vinte e um anos: voz de homem jovem, masculina, natural, calma, atenciosa; nunca animado, nunca simpático demais, nunca recitando. Aurora tem dezoito anos: voz suave e firme, sem infantilidade; está com ciúme e finge que não, responde seca, às vezes com afronta.',
        [('i090', 'Josh', 'A Vibêke me contou que falou do Lauritz pra meia cidade em uma hora.'), ('i091', 'Aurora', 'Ela acabou de me contar a mesma coisa.'), ('i092', 'Josh', 'Eu não sei se ela percebe o que está fazendo.'), ('i094', 'Aurora', 'Não percebe, não.'), ('i095', 'Josh', 'Bom. É o que parece.'), ('i096', 'Aurora', 'Bom pra você, então.')]),
 "B6b1": ('Perto da janela de um salão de baile, num intervalo entre danças. Os dois conversam em volume normal, médio, no mesmo nível um do outro: não sussurram, não cochicham e não falam alto. É uma conversa comum, com um incômodo por baixo. Josh tem vinte e um anos: voz de homem jovem, masculina, natural, calma, atenciosa; nunca animado, nunca simpático demais, nunca recitando. Aurora tem dezoito anos: voz suave e firme, sem infantilidade; está com ciúme e finge que não, responde seca, às vezes com afronta. Agora ele pergunta o que está por trás do silêncio dela, com atenção sincera, no mesmo volume de antes.',
        [('i099', 'Aurora', 'Sim, Josh?'), ('i100', 'Josh', 'Tem alguma coisa te incomodando?'), ('i102', 'Aurora', 'Não. Nada.'), ('i103', 'Josh', 'Isso não é verdade.'), ('i104', 'Aurora', 'Não é mentira.'), ('i105', 'Josh', 'Eu acho que é, sim.'), ('i106', 'Aurora', 'Eu sei que você acha. Mas você acha errado.')]),
 "B6b2": ('Perto da janela de um salão de baile, num intervalo entre danças. Os dois conversam em volume normal, médio, no mesmo nível um do outro: não sussurram, não cochicham e não falam alto. É uma conversa comum, com um incômodo por baixo. Josh tem vinte e um anos: voz de homem jovem, masculina, natural, calma, atenciosa; nunca animado, nunca simpático demais, nunca recitando. Aurora tem dezoito anos: voz suave e firme, sem infantilidade; está com ciúme e finge que não, responde seca, às vezes com afronta. Agora ele pergunta o que está por trás do silêncio dela, com atenção sincera, no mesmo volume de antes.',
        [('i108', 'Aurora', 'Não tem motivo, Josh.'), ('i109', 'Josh', 'Eu sei que não tem.'), ('i110', 'Aurora', 'Ela é uma boa pessoa.'), ('i112', 'Josh', 'Tenho certeza disso.'), ('i113', 'Aurora', 'E ela é apaixonada pelo Lauritz.'), ('i114', 'Josh', 'É, sim. Muito.'), ('i115', 'Aurora', 'Então não tem motivo.')]),
 "B6b3": ('Perto da janela de um salão de baile, num intervalo entre danças. Os dois conversam em volume normal, médio, no mesmo nível um do outro: não sussurram, não cochicham e não falam alto. É uma conversa comum, com um incômodo por baixo. Josh tem vinte e um anos: voz de homem jovem, masculina, natural, calma, atenciosa; nunca animado, nunca simpático demais, nunca recitando. Aurora tem dezoito anos: voz suave e firme, sem infantilidade; está com ciúme e finge que não, responde seca, às vezes com afronta. Agora ele pergunta o que está por trás do silêncio dela, com atenção sincera, no mesmo volume de antes.',
        [('i116b', 'Josh', 'Você ter motivo, ou não ter motivo, não muda o que você está sentindo.'), ('i118', 'Aurora', 'Eu vou voltar pro meu lugar.'), ('i119', 'Josh', 'Eu sei. Pode ir.'), ('i120', 'Aurora', 'Você vai dançar com a Vibêke?'), ('i121', 'Josh', 'Provavelmente, sim.'), ('i122', 'Aurora', 'Boa noite, Josh.'), ('i123', 'Josh', 'A noite ainda não acabou.'), ('i124', 'Aurora', 'Eu sei que não.')])
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

LIMITE_JOSH_HZ = 130  # o Josh fica por volta de 100 Hz; acima de 130 já soa feminino

def f0(a, sr=SR):
    fr = []; n = 2048
    for i in range(0, len(a) - n, 1024):
        x = a[i:i + n]
        if np.sqrt((x ** 2).mean()) < 0.03: continue
        c = np.correlate(x, x, "full")[n - 1:]; lo, hi = sr // 350, sr // 60
        fr.append(sr / (lo + np.argmax(c[lo:hi])))
    return int(np.median(fr)) if fr else 0

def norm(t):
    t = unicodedata.normalize("NFKD", t.lower()); t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", t).split()

_m = None
def recorta(bid, a):
    global _m
    from faster_whisper import WhisperModel
    if _m is None: _m = WhisperModel("small", device="cpu", compute_type="int8")
    _, linhas = BLOCOS[bid]
    a16 = np.interp(np.arange(0, len(a), SR / 16000), np.arange(len(a)), a).astype(np.float32)
    segs, _ = _m.transcribe(a16, language="pt", beam_size=5, word_timestamps=True)
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
    so_recorte = "--recortar" in sys.argv
    for bid in ([x for x in sys.argv[1:] if not x.startswith("--")] or BLOCOS):
        if not so_recorte:
            for tent in range(3):
                a = gera(bid)
                if a is None or not recorta(bid, a): continue
                alto = [(sl, f0(sf.read(f"{OUT}/{sl}.seg.wav")[0])) for sl, f, _ in BLOCOS[bid][1] if f == "Josh"]
                alto = [x for x in alto if x[1] > LIMITE_JOSH_HZ]
                if not alto: break
                print("TIMBRE ALTO, refazendo", bid, alto)
            continue
        a = sf.read(f"{OUT}/{bid}.wav", dtype="float32")[0]
        if a is None: print("ABORT", bid); break
        recorta(bid, a)
