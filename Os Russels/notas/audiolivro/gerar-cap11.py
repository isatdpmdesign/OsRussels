import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts11"
SCR = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
# NOVAS vozes: Josh (Achird, jovem/caloroso), Dylan (Zubenelgenubi, casual/seco) — a AUDITAR com a autora
V = {"N": "Vindemiatrix", "AU": "Leda", "EL": "Gacrux", "RAJ": "Algieba",
     "JOSH": "Zubenelgenubi", "DYLAN": "Achird",
     "HELLE": "Achernar", "LARSEN": "Kore",
     "MIK": "Sulafat", "FRED": "Autonoe", "LOV": "Laomedeia", "CAS": "Pulcherrima", "SOL": "Despina", "ING": "Aoede", "CR1": "Erinome", "CR2": "Callirrhoe", "CR3": "Zephyr", "JOSHW": "Zubenelgenubi", "NM": "Vindemiatrix", "ERIK": "Iapetus"}
NARR_AF = "asetrate=24000*0.88,aresample=24000,atempo=1.1364"  # narradora grave

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
            if t < tries - 1: time.sleep(5); continue
            print("CURL FALHOU", slug); return None
        d = json.load(open(outf))
        try:
            pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            return np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
        except Exception:
            if "RESOURCE_EXHAUSTED" not in json.dumps(d) and not text.startswith('"'):
                text = '"' + text + '"'
                body["contents"][0]["parts"][0]["text"] = text
                json.dump(body, open(reqf, "w"))
            if t < tries - 1:
                time.sleep(20 if "RESOURCE_EXHAUSTED" in json.dumps(d) else 4); continue
            print("FALHOU", slug, json.dumps(d)[:160]); return None

def apply_af(a, slug, af):
    sf.write(f"{BASE}/{slug}_raw.wav", a, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{BASE}/{slug}_raw.wav","-af",af,
                    f"{BASE}/{slug}_p.wav","-loglevel","error"],check=True)
    b,_ = sf.read(f"{BASE}/{slug}_p.wav", dtype="float32")
    return b.mean(axis=1) if b.ndim>1 else b

def load(p):
    b,_ = sf.read(p, dtype="float32"); return b.mean(axis=1) if b.ndim>1 else b

def sil(sec): return np.zeros(int(sec*SR), dtype=np.float32)

MEM_AF = "highpass=f=240,lowpass=f=3200,aecho=0.8:0.6:55:0.3,volume=0.72"
J = "Diga com voz masculina grave e firme, de um homem de vinte e um anos: "
BR = "Diga em português do Brasil, com sotaque brasileiro: "
SEG = [
 ('b001', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo onze: O conselheiro.', 1.2),
 ('b002', 'N', 'Este capítulo volta aos olhos de Josh. Depois da visita de Erik Mortensen, e daquela manhã na cozinha em que Aurora pediu que ele não sumisse de novo, os dois tinham voltado às manhãs de sempre. Mas agora Aurora tinha pretendentes. E Josh, o professor das aulas secretas, continuava sendo a pessoa a quem ela pedia conselhos.', 0.6),
 ('b003', 'N', 'Começou com Erik. Ou melhor: começou com algo que Josh disse sobre Erik numa manhã de cozinha, três dias depois da primeira visita. Aurora mencionou, como quem fala do tempo, com uma casualidade tão estudada que Josh a reconheceu na hora como o contrário de casual, que Erik voltaria na sexta-feira. Ela disse, soprando o chá:', 0.25),
 ('b004', 'AU', BR+'Ele vai trazer a irmã. A Ingrid vem junto. O papai sugeriu um passeio nos jardins do Rosenborg.', 0.4),
 ('b005', 'N', 'Josh virou a página do livro. Não estava lendo.', 0.2),
 ('b006', 'JOSH', 'Bom. A Ingrid é boa companhia.', 0.2),
 ('b007', 'AU', BR+'É. E o Erik quer me mostrar um manuscrito que trouxe da Alemanha. Uma tradução de Schiller.', 0.2),
 ('b008', 'JOSH', 'Ah, Schiller.', 0.2),
 ('b009', 'AU', BR+'É. Ele gosta de poesia alemã. Diz que os românticos alemães são superiores aos franceses, o que é uma posição polêmica, mas ele argumenta bem.', 0.4),
 ('b010', 'N', 'Josh tomou um gole de chá. Quente demais. Queimou a língua. Ele não se importou. E disse:', 0.2),
 ('b011', 'JOSH', 'Cuidado com homem que tem opinião muito forte sobre poesia.', 0.2),
 ('b012', 'AU', BR+'E por quê?', 0.2),
 ('b013', 'JOSH', 'Porque normalmente eles estão mais interessados em parecer sensíveis do que em ser sensíveis. Poesia é fácil de citar. Difícil de viver.', 0.4),
 ('b014', 'N', 'A frase saiu com a naturalidade de quem comenta o tempo. Desinteressada. Quase filosófica. E Josh, que se conhecia o bastante para saber quando estava sendo honesto e quando estava sendo estratégico, sentiu, no instante em que as palavras saíram, um desconforto que não tinha nada a ver com o chá quente.', 0.4),
 ('b015', 'N', 'Porque a observação era verdadeira. Em geral. Valia para centenas de homens que usam poesia para seduzir. Mas Josh não a fez por amor à verdade. Fez porque Erik Mortensen tinha trazido Lamartine, ia trazer Schiller, e Aurora olhava esses presentes com um brilho nos olhos que Josh queria, egoísta, mesquinha, humanamente, apagar. Aurora inclinou a cabeça, pensou, e respondeu:', 0.2),
 ('b016', 'AU', BR+'O Erik não me parece o tipo que cita poesia pra parecer sensível. Ele parece verdadeiro.', 0.2),
 ('b017', 'JOSH', 'Pode ser. Eu não conheço ele.', 0.2),
 ('b018', 'AU', 'Diga firme, com uma precisão cortante, em português do Brasil: Não. Você não conhece.', 0.4),
 ('b019', 'N', 'A frase teve um peso que Josh mereceu. Ela estava dizendo, com aquela precisão de cirurgiã: você não tem o direito de julgar alguém que eu conheço e você não. E estava certa. Tudo o que Josh sabia sobre Erik vinha do sarau: duas horas de observação de longe, filtradas por um ciúme que ele se recusava a nomear, mas que pulsava dentro dele como um segundo coração. Ele recuou:', 0.2),
 ('b020', 'JOSH', 'Você tem razão. Desculpa. Não é da minha conta.', 0.4),
 ('b021', 'N', 'Aurora o estudou um momento. Os olhos dela, que nas últimas semanas tinham perdido camadas de armadura e ganhado camadas de algo mais perigoso, confiança, proximidade, o brilho de quem sabe que está sendo vista e começou a gostar, o examinaram. E ela disse, com aspas invisíveis, mas também com algo verdadeiro:', 0.2),
 ('b022', 'AU', BR+'Você é o meu conselheiro. Se eu não quisesse a sua opinião, eu não falaria do Erik na cozinha às seis da manhã.', 0.4),
 ('b023', 'N', 'Conselheiro. Não professor. A palavra tinha mudado em algum ponto, sem que ninguém decidisse. Conselheiro era mais. Era alguém cujo julgamento importa. Alguém que pode, com uma frase na hora certa, mudar o rumo de uma decisão. Josh tomou outro gole. Agora a temperatura estava certa. E escolheu cada palavra como quem posiciona peças num tabuleiro:', 0.2),
 ('b024', 'JOSH', 'Então, como conselheiro, eu sugiro que, da próxima vez que o Erik falar de poesia alemã, você pergunte qual poema marcou ele mais, e por quê. Não qual ele acha mais bonito. Qual marcou. A diferença é importante. Bonito é estético. Marcar é pessoal. Se ele responder com um poema famoso e uma análise de professor, está representando. Se responder com algo inesperado, e uma história da vida dele, é de verdade.', 0.4),
 ('b025', 'N', 'Aurora ouviu e assentiu. E Josh viu, com a culpa de quem planta uma semente envenenada no jardim dos outros, que ela guardou o conselho como guardava todos: com seriedade, com confiança, com a intenção de usar. O conselho era bom. Tecnicamente impecável. E estrategicamente devastador. Porque Josh sabia que a maioria dos homens como Erik, cultos, viajados, encantadores, recuava diante de uma pergunta pessoal de verdade. Não por desonestidade. Por hábito.', 0.4),
 ('b026', 'N', 'Se Erik recuasse, Aurora notaria. Notando, começaria a duvidar. Duvidando, criaria distância. E a distância seria o que Josh queria, sem querer querer. E na cabeça dele, a voz da mãe, como sempre: O que você está fazendo, Josh? Estou dando um conselho honesto. Honesto com que intenção? Josh não respondeu à mãe. Virou a página. Desta vez, leu de verdade.', 1.0),
 # --- os outros pretendentes ---
 ('b027', 'N', 'Mas não parou com Erik. Frederik Holst, o filho mais novo dos donos da casa do sarau, apareceu num chá três dias depois da segunda visita de Erik. Vinte anos, loiro como trigo, maxilar quadrado, e mãos de quem nunca segurou nada mais pesado que uma raquete. Sentou-se ao lado de Aurora com a confiança cega de quem acha que sobrenome e dinheiro substituem personalidade.', 0.4),
 ('b028', 'N', 'Josh observava do outro lado da sala, conversando com o Professor Andersen sobre Hegel, com metade da cabeça, enquanto a outra metade rastreava Aurora com a precisão de um cão de caça. Frederik falou. Aurora ouviu, perguntou. Frederik respondeu. Aurora sorriu. Mas não o sorriso de verdade, o que começa no canto esquerdo. O sorriso educado. O que dizia: estou tentando. Na volta, na carruagem, ela comentou, no tom de quem descreve um móvel útil:', 0.2),
 ('b029', 'AU', BR+'Ele é simpático. Sem profundidade, mas simpático.', 0.2),
 ('b030', 'JOSH', 'Simpático não basta?', 0.2),
 ('b031', 'AU', BR+'Pra conversar num chá, basta. Pra mais do que isso, não.', 0.2),
 ('b032', 'JOSH', 'E o que falta?', 0.4),
 ('b033', 'N', 'Aurora pensou. A carruagem sacudia nas pedras, e a luz do fim da tarde transformava tudo em ouro e sombra. Ela respondeu:', 0.2),
 ('b034', 'AU', BR+'Substância. O Frederik fala de coisas. Cavalos, ópera, a temporada. Mas não fala de si mesmo. Não se expõe. É como conversar com uma fachada. Bonita, bem pintada, mas sem nada por trás.', 0.4),
 ('b035', 'N', 'E a pergunta de Josh saiu antes que ele pudesse segurar. Com mais interesse do que devia. Com fome:', 0.2),
 ('b036', 'JOSH', 'E o Erik, então?', 0.4),
 ('b037', 'N', 'Aurora o olhou de um jeito que dizia: eu sei o que você está fazendo ao perguntar isso agora. E vou responder mesmo assim.', 0.2),
 ('b038', 'AU', BR+'O Erik tem substância. Mas...', 0.2),
 ('b039', 'JOSH', 'Mas o quê?', 0.2),
 ('b040', 'AU', BR+'Quando eu perguntei qual poema marcou ele mais, ele citou um poema de Goethe, O Rei dos Elfos. E quando eu perguntei por quê, ele disse que o pai lia pra ele quando era criança. E ficou quieto. Por um momento.', 0.4),
 ('b041', 'N', 'Josh sentiu o estômago afundar. E disse a verdade, porque Casandra não tinha criado mentirosos:', 0.2),
 ('b042', 'JOSH', 'Isso é bom. Isso é de verdade.', 0.2),
 ('b043', 'AU', BR+'Eu sei bem.', 0.4),
 ('b044', 'N', 'E Aurora olhou pela janela. Josh também. E viu, no reflexo, o próprio rosto, com uma expressão que não devia estar ali. O contrário de orgulho pelo sucesso do conselho. Decepção. O conselho tinha funcionado, mas não do jeito que ele queria. Em vez de expor Erik como superficial, a pergunta revelou que Erik era de verdade. Que Erik, maldito Erik Mortensen e seu Goethe de infância, era um candidato legítimo.', 0.4),
 ('b045', 'N', 'Josh encostou a cabeça no vidro e fechou os olhos. E a voz da mãe disse, na cabeça dele: Bem feito. É o que acontece quando se planta veneno num jardim. Às vezes o veneno vira remédio.', 1.0),
 ('b046', 'N', 'Mas Josh não parou. A coisa sem nome que crescia dentro dele, teimosa como as roseiras de Aarav, não deixava. O método era sempre o mesmo. Sutil. Nunca uma crítica direta, ele era inteligente demais para isso. Sempre um conselho. Uma observação que parecia objetiva, e que era, na verdade, uma lente posicionada com cuidado para mostrar defeitos que talvez nem existissem.', 0.4),
 ('b047', 'N', 'Quando Aurora contou que o sobrinho dos Lundgren, um rapaz chamado Anders, de vinte e dois anos, estudante de direito, de sorriso fácil, a tinha convidado para caminhar nos jardins do Kastellet, Josh disse:', 0.2),
 ('b048', 'JOSH', 'Caminhar é bom. Mas repara no ritmo dele. Homem que caminha muito depressa num passeio está mais preocupado com o destino do que com a companhia. E homem que caminha devagar demais está tentando esticar uma coisa que devia fluir sozinha. O ritmo certo é o que se adapta ao seu.', 0.4),
 ('b049', 'N', 'Aurora caminhou com Anders, e reparou no ritmo. Anders andava depressa. Ela voltou dizendo que ele era agradável, mas apressado. Quando contou que um rapaz chamado Niels, filho de um diplomata, recém-chegado de Viena, a convidara para ver a coleção de pinturas dos Frederiksen durante um sarau, Josh disse:', 0.2),
 ('b050', 'JOSH', 'Pintura é pretexto. Quando um homem te leva pra ver arte, ele não quer que você veja a arte. Quer te ver vendo a arte. É um teste: ele quer saber se você se impressiona fácil. O truque é não reagir à pintura que ele quer que você admire. Reage a outra. Uma que ele não espera. Mostra que você vê com os seus próprios olhos.', 0.4),
 ('b051', 'N', 'Aurora viu as pinturas com Niels. Ignorou o Rembrandt que ele apontou com orgulho. Parou diante de uma natureza-morta escondida num canto e disse algo sobre a luz e a solidão dos objetos que deixou Niels calado por quinze segundos. Segundo Aurora, ele ficou com cara de quem esperava um gato e encontrou um tigre. Josh sentiu orgulho e nojo em partes iguais.', 0.4),
 ('b052', 'N', 'Porque o conselho funcionou. De novo. Não do jeito que ele queria, mas funcionou no sentido de que Aurora não estava se encolhendo. Não estava se moldando ao que cada rapaz esperava. Estava sendo ela: feroz, inteligente, imprevisível. E os rapazes, um por um, ficavam desnorteados diante de uma moça que não seguia o roteiro. Alguns recuavam. Anders não voltou a convidar. Niels voltou, mas com uma cautela que Aurora entendeu como falta de interesse.', 0.4),
 ('b053', 'N', 'Erik, porém, não recuava. Erik absorvia cada surpresa que Aurora oferecia, como quem gosta de ser surpreendido. Erik não queria uma moça que seguisse o roteiro. Queria exatamente o que Aurora era. E Josh, manhã após manhã, conselho após conselho, via a distância entre Aurora e Erik diminuir. Via Aurora falar de Erik com mais frequência. Com mais detalhe. Até que, numa manhã de julho, ela disse:', 0.2),
 ('b054', 'AU', BR+'O Erik me perguntou sobre o Aarav.', 0.4),
 ('b055', 'N', 'Josh sentiu algo gelado descer pela espinha. E perguntou:', 0.2),
 ('b056', 'JOSH', 'Perguntou o quê?', 0.3),
 ('b057', 'AU', BR+'Como ele era. Do que gostava. Como era a gente, os dois. Ninguém na cidade me pergunta do Aarav. Ninguém. As pessoas falam dele como se fosse um assunto proibido. Como se dizer o nome dele fosse me machucar.', 0.3),
 ('b058', 'N', 'Ela olhou para a caneca com uma expressão que Josh não via havia semanas: vulnerabilidade sem armadura. A Aurora da biblioteca, de olhos vermelhos. E continuou, mais baixo:', 0.2),
 ('b059', 'AU', 'Diga num tom mais baixo e emocionado, sem sussurrar, em português do Brasil: Mas o Erik perguntou. E eu respondi. E foi... bom. Foi como abrir uma janela num quarto que estava fechado fazia muito tempo.', 0.5),
 ('b060', 'N', 'Josh ficou em silêncio por muito tempo. Não por falta do que dizer. Porque tudo o que ele queria dizer era mesquinho, egoísta. Eu também quero te perguntar do Aarav. Eu quero ser a janela, não ele. Eu cuido das roseiras do seu irmão toda manhã antes de você acordar. Eu envernizei o banco. Eu escorei a pérgola. Eu sei onde ficam a tesoura de poda, o verniz e as velas debaixo da escada. Eu conheço cada canto desse jardim que era dele, que agora é seu, e que de algum jeito virou meu também.', 0.4),
 ('b061', 'N', 'Queria dizer tudo isso. E não podia. E não disse. E a contenção, a maldita contenção dos Russel, a de quem escolhe o momento certo e descobre que o momento certo nunca chega, doía como queimadura. Ele disse, pela segunda vez sobre Erik, com gosto de cinza na boca:', 0.2),
 ('b062', 'JOSH', 'Diga com a voz um pouco oca, sem convicção: Isso é bom. É importante poder falar do Aarav.', 0.5),
 ('b063', 'N', 'Aurora assentiu. E Josh viu, nos olhos dela, que ela tinha percebido. Que a resposta dele estava oca. As palavras certas, o tom errado. Tecnicamente correto, e emocionalmente falso, como o sorriso de porcelana dela. Ela não comentou. Levantou, lavou a caneca, e foi até a porta. E parou, como sempre parava. O ritual deles: ela parada na porta, dizendo uma última coisa, e saindo.', 0.4),
 ('b064', 'N', 'Mas desta vez ela não disse nada. Ficou parada dois segundos. Três. E saiu sem falar. E o silêncio, a falta da última coisa, foi mais alto do que qualquer palavra.', 1.2),
 # --- a carta ---
 ('b065', 'N', 'Josh escreveu à mãe naquela noite. Não a carta de sempre, de novidades e evasivas sobre a filha do padrinho. Uma carta que ele nunca mandaria. E escreveu:', 0.4),
 ('b066', 'JOSH', 'Querida mãe. Eu estou fazendo uma coisa errada. Não errada como roubar ou mentir, embora talvez seja mentir, de certo modo. Eu estou usando o que eu sei pra influenciar alguém. Estou dando conselhos que são verdadeiros por fora e envenenados por dentro. Estou fazendo isso porque eu não suporto ver a pessoa de quem eu gosto se aproximar de outra pessoa.', 0.3),
 ('b067', 'JOSH', 'E o pior, o verdadeiramente pior, é que ela confia em mim. Confia nos meus conselhos. Usa o que eu digo pra tomar decisões sobre a vida dela. E eu traio essa confiança cada vez que abro a boca.', 0.3),
 ('b068', 'JOSH', 'Diga em português do Brasil, com sotaque brasileiro: A senhora diria que eu sei o que fazer. E eu sei. Eu devia parar. Devia deixar as coisas seguirem. Esse rapaz, o Erik, provavelmente é bom pra ela. Ele perguntou do Aarav, quando eu nunca tive coragem de perguntar. Ele faz ela rir e falar de coisas que ela não fala com mais ninguém.', 0.3),
 ('b069', 'JOSH', 'Mas eu também sei que ela sentiu a minha falta quando eu não desci pro café. Sei que ela me pediu pra não fazer de novo. E sei que, quando ela me olha na cozinha às seis da manhã, com aqueles olhos que mudam de cor com a luz, acontece alguma coisa que eu nunca senti antes, que eu não sei descrever, e que me assusta, porque é enorme.', 0.3),
 ('b070', 'JOSH', 'A senhora disse que os Russel não fogem. Mas não disse o que fazer quando o inimigo é a gente mesmo. Eu estou apaixonado por ela, mãe. E não tenho o direito. Seu filho, Josh.', 0.6),
 ('b071', 'N', 'Ele leu a carta uma vez. Duas. Três. Dobrou, não selou, e não pôs na pilha do correio. Abriu a gaveta da escrivaninha, a gaveta das cartas da mãe, onde, no fundo, debaixo de tudo, estava a carta selada que ele trouxe no primeiro dia: a carta da mãe para o padrinho, que nunca tinha sido entregue. Pôs a carta não enviada ao lado da carta não entregue. E fechou a gaveta.', 0.4),
 ('b072', 'N', 'Ficou sentado no escuro, com o cheiro de jasmim no corredor e o som distante do cravo de Eleonora, que naquela noite, por algum motivo, não tocava Bach, mas algo mais lento, mais triste, que parecia uma canção de ninar para gente grande. Eu estou apaixonado por ela. A frase ficou no ar do quarto como fumaça. Josh respirou. Sentiu nos pulmões. E deixou existir. Não combateu. Não negou. Não trancou atrás de portas. Pela primeira vez desde que chegou à cidade, Josh Russel deixou a verdade simplesmente existir.', 0.4),
 ('b073', 'N', 'Não resolveu nada. Não mudou nada. Mas trouxe uma coisa que ele não esperava. Alívio. Como soltar uma pedra carregada por tempo demais. A pedra continua no chão. O problema continua. Mas os braços estão livres. Ele não sabia o que faria com os braços livres. Se pararia de sabotar. Se confessaria. Se ficaria, fugiria, ou só continuaria existindo no mesmo corredor que ela, morrendo devagar e em silêncio toda manhã às seis.', 0.4),
 ('b074', 'N', 'Mas sabia uma coisa. Eu estou apaixonado por ela. E dali em diante, tudo o que fizesse, cada conselho, cada silêncio, cada olhar, seria feito por alguém que sabe o que sente. E isso muda tudo.', 0.0),
]

if __name__ == "__main__":
    os.makedirs(BASE, exist_ok=True)
    parts = []
    for slug, vk, text, gap in SEG:
        seg_f = f"{BASE}/{slug}.seg.wav"; pf = f"{BASE}/{slug}_p.wav"
        if os.path.exists(seg_f):
            a = load(seg_f); src="cache"
        elif vk == "N" and os.path.exists(pf):
            a = load(pf); src="cache_p"
        else:
            a = tts(slug, V[vk], text)
            if a is None: print("ABORT em", slug); break
            if vk == "N": a = apply_af(a, slug, NARR_AF)
            elif vk == "NM": a = apply_af(a, slug, NARR_AF + "," + MEM_AF)
            sf.write(seg_f, a, SR); src="novo"; time.sleep(2)
        parts.append(a)
        if gap>0: parts.append(sil(gap))
        print("ok", slug, src, f"{len(a)/SR:.1f}s")
    mix = np.concatenate(parts)
    pk = float(np.max(np.abs(mix)) or 1.0)
    if pk>0.97: mix *= 0.97/pk
    sf.write(f"{SCR}/cap11-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap11-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap11-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
