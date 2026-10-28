import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts"
SCR = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
V = {"N": "Vindemiatrix", "AU": "Leda", "EL": "Gacrux", "RAJ": "Algieba"}
# narradora grave = Vindemiatrix com tom baixado
NARR_AF = "asetrate=24000*0.88,aresample=24000,atempo=1.1364"
MEM_AF  = NARR_AF + ",highpass=f=240,lowpass=f=3200,aecho=0.8:0.6:55:0.3,volume=0.72"

def tts(slug, voice, text, tries=4):
    body = {"contents": [{"parts": [{"text": text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    reqf = f"{BASE}/{slug}.req"; outf = f"{BASE}/{slug}.json"
    json.dump(body, open(reqf, "w"))
    for t in range(tries):
        try:
            subprocess.run(["curl", "-sS", "--retry", "3", "-X", "POST", URL,
                            "-H", "Content-Type: application/json",
                            "-d", "@" + reqf, "-o", outf], check=True, timeout=180)
        except subprocess.SubprocessError:
            if t < tries - 1:
                time.sleep(5); continue
            print("CURL FALHOU", slug); return None
        d = json.load(open(outf))
        try:
            pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            return np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
        except Exception:
            if t < tries - 1:
                time.sleep(20 if "RESOURCE_EXHAUSTED" in json.dumps(d) else 4); continue
            print("FALHOU", slug, json.dumps(d)[:160]); return None

def apply_af(a, slug, af):
    sf.write(f"{BASE}/{slug}_raw.wav", a, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{BASE}/{slug}_raw.wav","-af",af,
                    f"{BASE}/{slug}_p.wav","-loglevel","error"],check=True)
    b,_ = sf.read(f"{BASE}/{slug}_p.wav", dtype="float32")
    return b.mean(axis=1) if b.ndim>1 else b

def sil(sec): return np.zeros(int(sec*SR), dtype=np.float32)

SEG = [
 ("c01","N","A cadeira continuava ali. À cabeceira esquerda da mesa de jantar, entre o castiçal de prata que a mãe de Aurora nunca deixava apagar e a janela que dava para os jardins de buxo, a cadeira de Aarav Svensson permanecia em seu posto como um soldado fiel esperando o general que jamais voltaria. Ninguém se sentava nela, nem os criados ousavam movê-la.",0.6),
 ("c02","N","Aurora olhava para a cadeira todas as manhãs. Não com a intenção de olhar; isso ela jamais admitiria. Eram apenas dois segundos, às vezes três, o suficiente para sentir o aperto no peito, respirar fundo e voltar ao pão com manteiga. Do outro lado da mesa, a mãe dela, Eleonora, levantou os olhos do bordado e disse, com doçura:",0.3),
 ("c03","EL","Está frio lá fora hoje. Você deveria usar o xale de lã quando for ao jardim.",0.4),
 ("c04","N","Aurora respondeu sem levantar os olhos do prato, a voz fria:",0.25),
 ("c05","AU","Não pretendo ir ao jardim.",0.35),
 ("c06","N","A mãe insistiu, serena:",0.25),
 ("c07","EL","Pretendia ontem também. E acabou ficando duas horas entre as roseiras.",0.5),
 ("c08","N","Aurora não respondeu. As roseiras eram o único lugar da propriedade onde ela ainda conseguia sentir Aarav por perto. Tinham sido ideia dele. O irmão costumava dizer, ainda vivo:",0.35),
 ("c09","N","Rosas dinamarquesas em solo dinamarquês, plantadas por mãos indianas.",0.55),
 ("c10","N","Aarav tinha essa mania de transformar qualquer coisa ordinária em poesia. Fazia dezoito meses desde que o navio que o levava numa expedição ao Ceilão fora engolido por uma tempestade no Índico. A notícia chegou num envelope preto. E depois, o vazio: um vazio tão grande que parecia ter corpo próprio, que se sentava à mesa com eles, caminhava pelos corredores, respirava dentro das paredes. Aurora odiava os ecos.",0.8),
 ("c11","N","O pai de Aurora, Ráge Svensson, era um homem que parecia ter sido esculpido por duas mãos diferentes. A primeira, indiana, dera-lhe a pele cor de terra molhada, os olhos escuros como café, os cabelos negros começando a pratejar nas têmporas. A segunda, dinamarquesa por décadas de convivência, dera-lhe o porte e a forma precisa de falar, cada palavra medida como quem distribui ouro.",0.5),
 ("c12","N","Filho dos Kapoor, nobres do Rajastão, fora mandado a Copenhague aos catorze anos, e nunca voltou. Casou-se com Eleonora, construiu uma fortuna no comércio marítimo, ganhou o respeito que o dinheiro compra. Mas, debaixo de tudo, carregava uma solidão que só Aarav, de alguma forma, preenchia. Porque Aarav era o filho, o herdeiro, o rapaz que embarcara naquela expedição justamente porque queria ver com os próprios olhos a terra de onde a família viera.",0.5),
 ("c13","N","E agora Ráge, que jamais chorava, passava horas trancado no escritório. Aurora sabia: pelos olhos vermelhos no jantar, pelo modo como segurava o garfo com força demais, pelo modo como ele não olhava para a cadeira vazia. O pai estava se despedaçando por dentro, como um navio que afunda sem fazer barulho.",0.8),
 ("c14","N","Foi numa dessas manhãs de março que Ráge anunciou a notícia durante o café, a voz com uma espécie de propósito que a filha não ouvia havia meses:",0.3),
 ("c15","RAJ","Recebi uma carta de Casandra Russel. O filho dela, Joshua, precisa vir a Copenhague para seus estudos na universidade. Eu ofereci nossa casa.",0.45),
 ("c16","N","O garfo de Aurora parou no ar. A mãe pousou a xícara de chá e perguntou, cuidadosa:",0.25),
 ("c17","EL","Joshua. O segundo filho?",0.4),
 ("c18","N","O pai confirmou, tranquilo:",0.25),
 ("c19","RAJ","O do meio. Tem vinte e um anos. Eu sou padrinho dele, Eleonora. Faz anos que prometo a Casandra que cuidaria da educação de um dos filhos, se fosse necessário.",0.5),
 ("c20","N","A mãe traduziu, com aquela precisão nórdica que não era maldade:",0.25),
 ("c21","EL","Rústicos.",0.3),
 ("c21b","N","O pai corrigiu, firme:",0.25),
 ("c21c","RAJ","Do campo.",0.3),
 ("c22","N","Ele pediu, só com o olhar, que ela não começasse. Aurora não tinha falado. As palavras estavam entaladas entre o peito e a garganta, disputando espaço com algo quente e afiado que ela reconhecia como raiva. Um rapaz, na casa deles, no espaço de Aarav. Até que perguntou, a voz controlada demais:",0.3),
 ("c23","AU","Por quanto tempo?",0.35),
 ("c24","N","O pai respondeu, com ternura e firmeza:",0.25),
 ("c25","RAJ","O tempo que for necessário. Pode ser um ano. Podem ser dois. Três. Ele fica até estar pronto.",0.45),
 ("c26","N","Aurora repetiu, a voz baixa e apertada:",0.25),
 ("c27","AU","Três anos. Na nossa casa.",0.4),
 ("c28","N","Ela olhou para a cadeira de Aarav e perguntou:",0.25),
 ("c29","AU","E onde ele vai dormir?",0.35),
 ("c30","N","O silêncio durou um instante, mas foi o suficiente. Ráge respondeu, desviando o olhar pela primeira vez:",0.25),
 ("c31","RAJ","No quarto do andar de cima. O quarto leste.",0.45),
 ("c32","N","O quarto leste, o de hóspedes. Não o quarto de Aarav. Era aceitável, era suportável. Aurora respirou, dobrou o guardanapo, e levantou-se, cortês e gelada:",0.25),
 ("c33","AU","Com licença. Vou ao jardim.",0.4),
 ("c34","N","Eleonora olhou para o marido. Ráge olhou para a cadeira vazia. Ninguém disse nada.",0.8),
 ("c35","N","O jardim dos Svensson era um retângulo de verde e pedra nos fundos do casarão, protegido por muros altos cobertos de hera. No canto direito, as roseiras de Aarav dormiam sob a última geada do inverno. Aurora sentou-se no banco. O frio mordia suas mãos sem luvas, mas ela não se importava. O frio era honesto. O frio não tentava ocupar o lugar de ninguém.",0.5),
 ("c36","N","Joshua Russel. Ela virou o nome na boca como quem prova algo e não tem certeza se gosta do sabor. Viria para Copenhague, tropeçaria nas regras de etiqueta, usaria o talher errado no jantar. E todos na Brédigueide iriam olhar para ele morando na casa dos Svensson e pensar a mesma coisa: o novo filho de Ráge. O substituto.",0.5),
 ("c37","N","Mas ninguém substituía Aarav. Aarav era insubstituível como o sol é insubstituível: pode-se acender mil velas, mas nenhuma delas aquece como ele. Aurora olhou para as roseiras adormecidas e sussurrou, feroz e baixa:",0.3),
 ("c38","AU","Ninguém vai sentar na sua cadeira, Aarav. Eu prometo.",0.4),
 ("c39","N","O vento de março levou suas palavras, mas Aurora tinha certeza, absoluta, inabalável, de que o irmão ouvira.",0.8),
 ("c40","N","Os quinze dias passaram como passam todas as coisas que não queremos que cheguem: rápido demais. O assunto estava em toda parte: nas instruções que a mãe dava aos criados para preparar o quarto leste, nas conversas sussurradas das criadas sobre o rapaz do campo que ia chegar, nos olhares que o pai lançava para Aurora durante o jantar, cheios de algo que ela recusava interpretar como esperança.",0.5),
 ("c41","N","Na véspera da chegada, Eleonora entrou no quarto de Aurora enquanto ela escovava os cabelos diante do espelho. Sentou-se na beirada da cama e disse, baixo:",0.25),
 ("c42","EL","Amanhã cedo. A carruagem dele chega antes do meio-dia.",0.4),
 ("c43a","AU","Eu sei.",0.3),
 ("c43b","N","A mãe continuou:",0.25),
 ("c44","EL","Seu pai espera que você seja cortês.",0.4),
 ("c45","N","Aurora respondeu, meio sêca:",0.25),
 ("c46","AU","Eu sou sempre cortês, mamãe.",0.35),
 ("c47","N","A mãe insistiu, com suavidade:",0.25),
 ("c48","EL","Cortês de verdade, Aurora. Não essa sua cortesia gelada que faz as pessoas sentirem que estão sendo recebidas e expulsas ao mesmo tempo.",0.5),
 ("c49","N","Aurora quase sorriu, e disse, com um fio de ternura cansada:",0.25),
 ("c50","AU","Eu vou me comportar, mamãe. Pode dormir tranquila.",0.45),
 ("c51","N","Eleonora hesitou. Abriu a boca como se fosse dizer algo mais, algo que talvez envolvesse Aarav e saudade e a necessidade de seguir em frente, mas pensou melhor. Levantou-se, beijou o topo da cabeça da filha, e saiu com o mesmo silêncio com que entrara.",0.6),
 ("c52","N","Aurora ficou olhando o próprio reflexo por um longo tempo. Cortês, pensou. Eu posso ser cortês. Posso ser a anfitriã mais cortês que Joshua Russel já encontrou na vida. Mas isso não significa que vou gostar dele.",0.6),
 ("c53","N","Pousou a escova. Apagou a vela. Deitou-se na escuridão do quarto e ficou ouvindo o vento da noite empurrar os galhos da tília contra a janela. Amanhã tudo mudaria. Ela só não sabia o quanto.",0.0),
]

def load(p):
    b,_ = sf.read(p, dtype="float32"); return b.mean(axis=1) if b.ndim>1 else b

parts = []
for slug, vk, text, gap in SEG:
    seg_f = f"{BASE}/{slug}.seg.wav"; pf = f"{BASE}/{slug}_p.wav"
    if os.path.exists(seg_f):
        a = load(seg_f); src = "cache"
    elif vk == "N" and os.path.exists(pf):
        a = load(pf); src = "cache_p"
    else:
        a = tts(slug, V[vk], text)
        if a is None:
            print("ABORT em", slug); break
        if slug == "c09":
            a = apply_af(a, slug, MEM_AF)
        elif vk == "N":
            a = apply_af(a, slug, NARR_AF)
        sf.write(seg_f, a, SR); src = "novo"; time.sleep(2)
    parts.append(a)
    if gap>0: parts.append(sil(gap))
    print("ok", slug, src, f"{len(a)/SR:.1f}s")

mix = np.concatenate(parts)
pk = float(np.max(np.abs(mix)) or 1.0)
if pk>0.97: mix *= 0.97/pk
sf.write(f"{SCR}/cap01-completo-v3.wav", mix, SR)
subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap01-completo-v3.wav","-af",
    "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
    f"{SCR}/cap01-completo-v3.mp3","-loglevel","error"],check=True)
print("TOTAL", f"{len(mix)/SR:.1f}s")
