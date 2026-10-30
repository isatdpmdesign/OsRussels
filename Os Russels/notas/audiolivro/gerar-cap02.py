import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts2"
SCR = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
# NOVAS vozes: Josh (Achird, jovem/caloroso), Dylan (Zubenelgenubi, casual/seco) — a AUDITAR com a autora
V = {"N": "Vindemiatrix", "AU": "Leda", "EL": "Gacrux", "RAJ": "Algieba",
     "JOSH": "Zubenelgenubi", "DYLAN": "Achird"}
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

SEG = [
 ('i00', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo dois: O rapaz do campo.', 1.2),
 ("s01","N","A última coisa que Josh viu antes da estrada engolir o horizonte foi a figura da mãe parada na varanda. Casandra Russel não chorava; não era do feitio dela. Chorar era coisa que acontecia para dentro, como chuva que cai em poço fundo. Ao lado dela, encostado no pilar com os braços cruzados, estava Matias, treze anos, o caçula, o que menos sabia disfarçar qualquer coisa.",0.5),
 ("s01b","N","Josh Russel tinha vinte e um anos e era o filho do meio de cinco irmãos, criados numa fazenda perto de Sorô, no interior da Zelândia. Joseph, o mais velho, de vinte e quatro anos, cuidava da terra. Depois vinha Josh. Depois Meridiana, de vinte, a única menina. Depois Dylan, de dezenove. E por fim Matias, o caçula, de treze. O pai, Henrik, tinha morrido havia quatro anos, e desde então a mãe, Casandra, levava tudo sozinha.",0.5),
 ("s02","N","Dentro da carruagem, olhando pela janela traseira, estava Dylan, dezenove anos, com aquela capacidade irritante de dizer exatamente o que todos pensavam. Ele disse:",0.25),
 ("s03","DYLAN","Ele vai chorar. Aposto meu canivete que o Matias chora antes de a gente virar a curva.",0.4),
 ("s04","N","Josh respondeu sem olhar:",0.25),
 ("s05","JOSH","Não aposta nada. E deixa o garoto em paz.",0.4),
 ("s06","DYLAN","Eu não estou fazendo nada com o garoto. Estou fazendo uma observação científica. Você que vai estudar ciências, devia apreciar.",0.5),
 ("s07","N","Josh não respondeu. Estava ocupado gravando na memória cada detalhe da paisagem que se afastava: a casa de pedra e madeira com o telhado de palha que o pai reconstruíra três vezes antes de morrer; o celeiro onde Joseph já trabalhava, porque Joseph trabalhava sempre; o pomar de macieiras que Meridiana cuidava como quem conversa. Tudo aquilo ficando pequeno, cabendo na janela de uma carruagem, virando lembrança.",0.6),
 ("s08","N","Dylan o acompanhava só até Roskilde. Depois de um tempo, comentou:",0.25),
 ("s09","DYLAN","Você está com cara de quem vai vomitar.",0.4),
 ("s10","JOSH","Estou bem.",0.3),
 ("s11","DYLAN","Está verde.",0.3),
 ("s11b","N","Josh respondeu, sem se abalar:",0.25),
 ("s12","JOSH","É o reflexo das árvores.",0.45),
 ("s13","N","Dylan riu. Um riso curto, seco, muito parecido com o do pai, ou com o que Josh lembrava do riso do pai, que com o tempo ia ficando menos nítido, como uma pintura exposta ao sol tempo demais.",0.5),
 ("s14","N","Henrik Russel morrera quando Matias tinha nove anos. Uma febre que começou como nada e terminou como tudo. Josh tinha dezessete, e lembrava de ter segurado a mão do pai no final, e de sentir o exato momento em que a força daquela mão se esvaiu como água escorrendo entre os dedos.",0.6),
 ("s15","N","Depois disso, tudo mudou e nada mudou. A terra continuou precisando ser arada. Joseph assumiu a propriedade; Meridiana, a casa; Dylan, o papel de dizer o que ninguém queria ouvir; Matias, o de precisar de todos. E Josh ficou no meio, como sempre, sem saber qual era o seu lugar. O meio era o lugar de quem observa, de quem nota, de quem guarda. E Josh guardava tudo.",0.5),
 ("s16","N","Guardava o modo como a mãe passava a mão no encosto da cadeira do pai antes de se sentar. Guardava o cheiro de maçã e terra molhada que era o cheiro de Meridiana. E guardava as perguntas que Matias, o caçula, fazia de noite, no escuro do quarto que dividiam. O menino perguntava, baixinho:",0.3),
 ("s17","N","Josh, você acha que o pai sabe que a gente tá bem?",0.5),
 ("s18","N","E agora Josh ia guardar Copenhague.",0.7),
 ("s19","N","Ele nunca tinha visto a cidade. Sabia dela pelos livros do pastor da aldeia: que era a capital do reino, que ficava numa ilha, que tinha canais e palácios e uma universidade antiga. Mas saber e ver eram coisas tão diferentes quanto ler sobre fogo e colocar a mão na chama.",0.5),
 ("s20","N","A carruagem entrou em Copenhague pelo portão oeste, e Josh sentiu a cidade antes de vê-la. Pelo chão: o cascalho da estrada deu lugar às pedras da cidade, e a carruagem tremia num ritmo mais rápido, mais impaciente. Pelo som: o silêncio do campo deu lugar a uma sinfonia desordenada de vozes, cascos, rodas e sinos. Pelo cheiro: em vez de terra e feno, peixe do porto, pão assando, fumaça de carvão.",0.5),
 ("s21","N","E então viu. Prédios, mais prédios do que Josh achava possível, erguendo-se dos dois lados da rua como paredes de um cânion. Centenas de janelas olhando para a rua como olhos curiosos. E pessoas em toda parte, mais pessoas do que ele via em um mês inteiro no campo. Ele engoliu em seco.",0.5),
 ("s22","N","Dylan já tinha descido em Roskilde, com um tapa no ombro e um não morra que era o equivalente Russel de te amo, irmão. Agora Josh estava sozinho. Sozinho pela primeira vez na vida.",0.5),
 ("s23","N","O cocheiro guiou a carruagem por ruas cada vez mais largas e elegantes, até uma avenida arborizada que Josh não sabia ser a Brédigueide, mas que sentiu, de imediato, ser um lugar onde gente como ele não pertencia. As casas ali não eram casas: eram declarações. Fachadas de pedra lavrada, portões de ferro, jardins entrevistos por entre grades como segredos bem guardados.",0.5),
 ("s24","N","Josh olhou para as próprias mãos. Mãos grandes, calejadas, que sabiam empunhar um machado e guiar um arado, e que não combinavam com os punhos brancos da camisa que a mãe insistira que ele usasse. Ela dissera:",0.3),
 ("s25","N","Você não vai chegar na casa do seu padrinho parecendo que acabou de sair da lavoura, Joshua Russel.",0.5),
 ("s26","N","A carruagem parou. Josh olhou pela janela e viu o casarão: tijolos vermelhos, frontão neoclássico, janelas altas e simétricas, uma porta de carvalho escuro com aldrava de bronze em forma de leão. Respirou fundo, abriu a porta, desceu. E a porta do casarão se abriu.",0.7),
 ("s27","N","O padrinho era exatamente como Josh imaginava, e nada como Josh imaginava, ao mesmo tempo. O homem que saiu pela porta de carvalho tinha uma presença que preenchia o espaço ao redor como perfume forte preenche um cômodo. Não era alto, mas parecia ocupar mais lugar no mundo do que o corpo justificava. E o rosto: a pele escura, os olhos que pareciam conter bibliotecas inteiras, os traços fortes que se impunham com uma autoridade que nenhum rosto dinamarquês ao redor igualaria.",0.4),
 ("s28","N","Ele disse, a voz grave e medida, com uma calidez escondida sob camadas de compostura:",0.25),
 ("s29","RAJ","Joshua. Você cresceu.",0.4),
 ("s30","N","Josh curvou-se ligeiramente, como a mãe o instruíra:",0.25),
 ("s31","JOSH","Senhor Svensson. Obrigado por me receber.",0.4),
 ("s32","N","O homem estendeu a mão e corrigiu:",0.25),
 ("s33","RAJ","Ráge. Seu pai me chamava de Ráge. Você também vai.",0.45),
 ("s34","N","A mão era firme e seca, o aperto breve mas significativo. Josh sentiu algo se soltar dentro do peito, uma corda que ele nem sabia estar tensionada.",0.3),
 ("s35","RAJ","Entre. Eleonora preparou tudo.",0.45),
 ("s36","N","Josh entrou e sentiu, pela primeira vez na vida, o que significava estar dentro de uma casa que era bonita de propósito. Na fazenda, tudo tinha uma função; ali, havia coisas que existiam apenas para serem bonitas. Um espelho dourado que não refletia nada de útil. Um tapete tão limpo que Josh teve vergonha de pisar.",0.6),
 ("s37","N","Eleonora apareceu no topo da escadaria como uma aparição nórdica: loira, pálida, impecável, com um sorriso educado sem ser caloroso e caloroso sem ser íntimo. Desceu os degraus e disse:",0.3),
 ("s38","EL","Bem-vindo, Joshua. Espero que a viagem não tenha sido muito cansativa.",0.4),
 ("s39","JOSH","Não, senhora. Foi tranquila.",0.3),
 ("s40","N","Mentira. Foram oito horas de estrada com o estômago embrulhado. Eleonora continuou:",0.25),
 ("s41","EL","Ótimo. Fru Larsen preparou um almoço leve. Você deve estar com fome.",0.4),
 ("s42","N","Josh estava com fome. O pai olhou para a escadaria, com uma expressão que Josh não soube ler, e perguntou:",0.25),
 ("s43","RAJ","E a Aurora?",0.35),
 ("s44","N","Eleonora respondeu, com um tom que continha multidões:",0.25),
 ("s45","EL","Descendo.",0.6),
 ("s46","N","Ela apareceu no topo da escada e Josh esqueceu como respirar. Não foi dramático: foi um esquecimento simples, mecânico, como quando se tropeça num degrau. Porque Aurora Svensson não era nada do que Josh esperava.",0.4),
 ("s47","N","Ele esperava, se é que esperava algo, uma versão jovem da mãe. Uma dinamarquesa loira e pálida que se confundiria com qualquer outra garota daquela rua. Aurora não se confundiria com ninguém.",0.4),
 ("s48","N","Descia a escadaria com uma postura claramente ensinada, costas retas, queixo erguido, mas que não escondia algo selvagem por baixo. Algo que lembrava os cavalos jovens da fazenda, os que obedecem às rédeas mas mantêm nos olhos uma fagulha que diz: eu estou escolhendo obedecer, e posso mudar de ideia a qualquer momento.",0.4),
 ("s49","N","E os olhos. Grandes, amendoados, castanhos como mel, como âmbar, como o centro de uma chama prestes a se apagar. A pele de um tom que Josh nunca vira: nem o branco da mãe, nem o escuro do pai, algo entre os dois, como ouro misturado com bronze e uma gota de sol. Era a pessoa mais bonita que Josh já tinha visto na vida. E estava olhando para ele como se ele fosse uma mancha no tapete.",0.4),
 ("s50","N","O pai disse, com um orgulho impossível de esconder:",0.25),
 ("s51","RAJ","Aurora, este é Joshua Russel. Filho de Henrik e Casandra. Meu afilhado.",0.4),
 ("s52","N","Aurora chegou ao último degrau e parou. Os olhos percorreram Josh de cima a baixo com uma eficiência clínica. Ela disse:",0.25),
 ("s53","AU","Senhor Russel.",0.35),
 ("s54","N","A voz era inesperada, mais grave do que Josh anteciparia, com uma qualidade ligeiramente rouca. Josh curvou-se:",0.25),
 ("s55","JOSH","Senhorita Svensson. É um prazer.",0.35),
 ("s56","AU","Certamente.",0.4),
 ("s57","N","E então sorriu. Um sorriso tecnicamente perfeito, que dizia ao mesmo tempo eu estou sendo educada e você não é bem-vindo, sem que os pais percebessem. Josh percebeu. E, inexplicavelmente, quase sorriu de volta, o sorriso torto, o de verdade, porque algo naquela garota minúscula e furiosa era irresistivelmente interessante. Conteve-se a tempo, e seguiu o padrinho até a sala de jantar.",0.4),
 ("s58","N","Ao passar por ela, sentiu, ou imaginou sentir, o cheiro dela: algo floral e quente, como jasmim misturado com canela, que não combinava com nada que Josh conhecesse, e que por isso mesmo ficou grudado na memória dele como tinta em tecido branco.",0.7),
 ("s59","N","O almoço foi uma aula de sobrevivência. Não pela comida, que era extraordinária. A aula de sobrevivência era Aurora. Ela o tratava com uma cortesia tão impecável que beirava a crueldade. Passou-lhe a cesta de pão com um sorriso que não chegava aos olhos, e perguntou:",0.3),
 ("s60","AU","O senhor veio de longe, Senhor Russel?",0.4),
 ("s61","JOSH","Do interior da Zelândia. Perto de Sorô.",0.4),
 ("s62","AU","Sorô. Conheço apenas por referência. É muito... bucólico, dizem.",0.45),
 ("s63","N","Josh reconheceu o eufemismo. No vocabulário de Copenhague, bucólico significava atrasado. Ele disse, simplesmente:",0.25),
 ("s64","JOSH","É bonito. Diferente daqui.",0.4),
 ("s65","AU","Imagino que sim. Copenhague deve ser bastante diferente para quem está acostumado ao campo.",0.45),
 ("s66","N","Ela disse campo do mesmo modo que alguém diria lama. Josh prestava atenção. Olhou-a diretamente nos olhos de mel e respondeu:",0.25),
 ("s67","JOSH","É. Mas eu me adapto rápido.",0.4),
 ("s68","N","Algo cintilou nos olhos de Aurora: surpresa, talvez, por ele não ter recuado. Durou um instante. Depois o véu de cortesia voltou ao lugar.",0.3),
 ("s69","AU","Que bom. Copenhague pode ser implacável com quem não se adapta.",0.4),
 ("s70","N","O pai interveio, num tom suave que era claramente um aviso:",0.25),
 ("s71","RAJ","Aurora.",0.3),
 ("s72","AU","Sim, papai?",0.35),
 ("s73","RAJ","Passe a manteiga ao Joshua, por favor.",0.4),
 ("s74","N","Aurora passou a manteiga, segurando o prato o mais longe possível da mão dele, como se o contato pudesse contaminá-la. Mas a distância foi pequena o suficiente para Josh perceber como as mãos dela eram pequenas, morenas, de dedos finos que tremiam quase imperceptivelmente.",0.4),
 ("s75","N","Ela está nervosa, pensou Josh. Não é raiva. É medo. Não medo dele, mas do que ele representava: o espaço que ele ia ocupar, o lugar que alguém antes dele ocupara e que ela guardava com a ferocidade de quem protege um túmulo. Josh olhou para a cadeira vazia. E entendeu.",0.8),
 ("s76","N","O quarto leste era maior do que o quarto que Josh dividia com Matias na fazenda. Havia uma cama de casal com dossel, uma escrivaninha de mogno sob a janela, e uma estante vazia que Josh olhou com uma fome que não tinha nada a ver com comida.",0.5),
 ("s77","N","Ele pousou no chão a única mala de couro surrado que continha tudo o que possuía: três camisas, o casaco bom, cinco livros, o canivete do pai, e um lenço bordado por Meridiana com as iniciais J.R. num canto. Sentou-se na cama; as molas rangeram sob seu peso, afrontadas, como se não estivessem acostumadas a sustentar alguém como ele.",0.5),
 ("s78","N","Aurora Svensson. Ela não gostava dele; isso estava claro. O que não estava claro era por que isso o incomodava tanto. A mãe o avisara:",0.3),
 ("s79","N","Você vai estar ocupando um espaço que pertenceu a outra pessoa, Josh. Tenha paciência. Tenha delicadeza.",0.5),
 ("s80","N","Ele teria paciência. Teria delicadeza. Mas havia um mas que ele não conseguia calar. Um mas com olhos de mel e um sorriso feito de gelo e espinhos, que mesmo assim era a coisa mais fascinante que Josh já encontrara em vinte e um anos de vida.",0.5),
 ("s81","N","Não, disse a si mesmo, indo até a janela. Ele estava ali para estudar, para honrar o nome da família, porque era o filho do meio, o que não tinha terra para herdar nem papel definido para cumprir, e que por isso precisava inventar o próprio caminho. Não estava ali para ficar fascinado pela filha do padrinho.",0.5),
 ("s82","N","Abriu a mala, tirou os livros, e colocou-os na estante vazia, um por um, com o cuidado de quem arruma as peças num tabuleiro antes de uma partida que ainda não sabe se vai ganhar. Em algum lugar daquela casa, entre as roseiras adormecidas de um irmão morto, Aurora certamente planejava novas formas de fazê-lo sentir que não pertencia ali. Josh sorriu para si mesmo.",0.4),
 ("s83","N","Tudo bem, pensou. Eu não pertenço mesmo. Mas estou aqui. E não vou embora.",0.7),
 ("s84","N","Do bolso do casaco, tirou a última coisa que a mãe pusera em suas mãos: uma carta selada, endereçada ao seu padrinho, na caligrafia firme e ligeiramente torta de Casandra. Cuide do meu menino, Josh imaginava que dizia. Ou talvez dissesse algo completamente diferente; com Casandra Russel, nunca se sabia. Ele pousou a carta na escrivaninha, foi lavar o rosto para o jantar, e a água era quente. Na fazenda, a água era fria. Josh pensou que poderia se acostumar com isso. Com a água quente, pelo menos. O resto, a garota de olhos de mel, a cadeira vazia, o cheiro de jasmim nos corredores, era outra questão.",0.0),
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
            sf.write(seg_f, a, SR); src="novo"; time.sleep(2)
        parts.append(a)
        if gap>0: parts.append(sil(gap))
        print("ok", slug, src, f"{len(a)/SR:.1f}s")
    mix = np.concatenate(parts)
    pk = float(np.max(np.abs(mix)) or 1.0)
    if pk>0.97: mix *= 0.97/pk
    sf.write(f"{SCR}/cap02-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap02-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap02-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
