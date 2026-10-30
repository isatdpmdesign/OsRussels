import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts7"
SCR = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
# NOVAS vozes: Josh (Achird, jovem/caloroso), Dylan (Zubenelgenubi, casual/seco) — a AUDITAR com a autora
V = {"N": "Vindemiatrix", "AU": "Leda", "EL": "Gacrux", "RAJ": "Algieba",
     "JOSH": "Zubenelgenubi", "DYLAN": "Achird",
     "HELLE": "Achernar", "LARSEN": "Kore",
     "MIK": "Sulafat", "FRED": "Autonoe", "LOV": "Laomedeia", "CAS": "Pulcherrima", "SOL": "Despina", "ING": "Aoede", "CR1": "Erinome", "CR2": "Callirrhoe", "CR3": "Zephyr", "JOSHW": "Zubenelgenubi", "NM": "Vindemiatrix"}
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
SEG = [
 ('x01', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo sete: O que não se diz no café da manhã.', 1.2),
 ('x02', 'N', 'Este capítulo volta para os olhos de Josh. É a mesma noite do baile dos Frederiksen, o baile em que Aurora estreou na sociedade de vestido verde, e passou a noite inteira encostada na parede, sem que nenhum rapaz a tirasse para dançar. A noite em que Josh, ao pé da escada, disse a ela que estava linda. E que os outros eram idiotas.', 0.6),
 ('x03', 'N', 'Josh não dormiu. Não foi por causa da cama. A cama dos Svensson, com aquele dossel absurdo e lençóis de linho que deviam custar mais que uma vaca leiteira, era obscenamente confortável. Também não foi o barulho: a cidade, à meia-noite, era quase tão quieta quanto o campo. Foi por causa do verde.', 0.4),
 ('x04', 'N', 'O verde do vestido de Aurora, gravado nos olhos dele como uma marca de ferro em gado. Aquele verde escuro, quase negro, que fazia a pele dela parecer ouro líquido. O verde que descia pelos ombros. Os ombros que Josh não deveria ter olhado, que tentou não olhar, e que olhou, como se olha o sol quando ele rompe as nuvens: não por decisão, mas porque a luz é mais forte que a vontade.', 0.4),
 ('x05', 'N', 'Deitado no escuro, os braços cruzados atrás da cabeça, Josh revisitou a noite como quem desmonta um relógio para entender as engrenagens. O momento na escada: Aurora descendo, e ele perdendo a capacidade de formar frases, como um idiota. Sim, claro... linda. O salão. As sete moças que vieram até ele com sorrisos ensaiados e toques no braço, e que ele respondeu no piloto automático, educado e distante. Porque a única pessoa com quem ele queria falar estava a dez metros, encostada na parede. Sozinha.', 0.4),
 ('x06', 'N', 'Era isso que ele não conseguia parar de pensar. Não o vestido. Não os ombros. A solidão. Aurora ficara sozinha a noite inteira, como uma pintura que ninguém tem permissão de tocar. E Josh vira cada minuto. Cada olhar dos rapazes na direção dela, que nunca virava passo. Cada volta da dança em que ele a procurava pelo canto do olho, e a encontrava no mesmo lugar, com aquela dignidade feroz que era a coisa mais bonita e mais triste que ele já tinha visto.', 0.4),
 ('x07', 'N', 'E veio a raiva. Uma raiva limpa, não violenta. A raiva de quem vê uma injustiça cometida em câmera lenta por gente que nem sabe que está sendo injusta. Porque os rapazes daquele salão não eram maus. Eram covardes. Do tipo mais comum: o que olha para Aurora Svensson e pensa linda, depois pensa diferente, depois pensa o que meu pai diria, e depois não pensa mais nada, porque é mais fácil.', 0.4),
 ('x08', 'N', 'No campo não havia muitos assim. No campo, se um rapaz achava uma moça bonita, ele dizia, e as consequências que viessem. Mas Josh tinha lido e observado o bastante para saber que a civilização, com todas as suas porcelanas e talheres, tinha um efeito colateral: transformar a honestidade num luxo que poucos podiam pagar.', 0.4),
 ('x09', 'N', 'E ele tinha dito, no hall. Que ela estava linda. Que eles eram idiotas. E a expressão no rosto dela, o instante em que a armadura rachou e ele viu, por uma fração de segundo, não a Aurora de porcelana, mas a Aurora real, a do chá amargo na cozinha e das mãos sujas de terra, ficou gravada nele com a mesma força do vestido verde.', 0.4),
 ('x10', 'N', 'Josh virou de lado e afundou o rosto no travesseiro. Na cabeça, a frase da carta da mãe: Russels não fogem do que sentem. Apenas escolhem o momento certo de agir. Ele murmurou para o travesseiro, com ironia:', 0.25),
 ('x11', 'JOSH', 'Obrigado, mãe. Muito útil.', 0.5),
 ('x12', 'N', 'Dormiu às três. Acordou às cinco e meia. E desceu para a cozinha com olheiras.', 1.0),
 # --- a cozinha ---
 ('x13', 'N', 'Aurora já estava lá. No lugar de sempre, do lado esquerdo da mesa de madeira bruta, as mãos em volta da caneca, o olhar na janela. E os cabelos estavam soltos. Era a segunda vez que Josh a via assim, depois daquela noite na biblioteca, e o efeito era o mesmo: uma desorientação breve, como tropeçar no escuro. Os cabelos ondulados caíam pelos ombros e emolduravam o rosto de um jeito mais suave, mais jovem. Mais próximo de quem ela era quando ninguém estava olhando. Exceto que alguém estava. E ela sabia. Sem se virar, ela disse:', 0.25),
 ('x14', 'AU', 'Bom dia.', 0.3),
 ('x15', 'JOSH', 'Bom dia.', 0.4),
 ('x16', 'N', 'Josh pegou a caneca de sempre, a segunda da esquerda, com uma lasca na borda que Fru Larsen, a cozinheira, se recusava a trocar porque ainda servia. Serviu-se da chaleira, sentou do seu lado da mesa e abriu o livro. Silêncio. O silêncio de todas as manhãs. Mas naquele dia ele tinha outra textura. Mais denso. Como o ar antes de uma tempestade: não há vento, não há chuva, mas a pele sabe que algo está vindo.', 0.4),
 ('x17', 'N', 'Josh lia sem ler. Aurora bebia sem beber: encostava a caneca nos lábios, mas não engolia. Segurava a caneca no rosto como um escudo. Então Kóngen, o gato enorme e cinzento da cozinheira, bocejou no canto. Um bocejo tão alto no silêncio que os dois se sobressaltaram. Aurora soltou um sopro que podia ter sido quase uma risada. Josh comentou, olhando o gato:', 0.25),
 ('x18', 'JOSH', 'Ele faz isso de propósito.', 0.3),
 ('x19', 'AU', 'Faz. O Kóngen considera que qualquer silêncio de mais de cinco minutos é uma ofensa pessoal contra ele.', 0.4),
 ('x20', 'N', 'Ela olhava o gato. E nos lábios dela, os lábios que Josh não se permitia olhar, e olhava, havia algo. Não um sorriso. Ainda não. A vizinhança de um sorriso. O quarteirão onde o sorriso morava. Ele disse o nome dela:', 0.25),
 ('x21', 'JOSH', 'Diga com calma, chamando a atenção dela: Aurora.', 0.3),
 ('x22', 'N', 'Ela se virou. E Josh viu nos olhos dela a sombra do baile. Não dor, exatamente. Algo mais quieto. Resignação. A aceitação de uma coisa que dói mas já não surpreende. Ele disse, com cuidado:', 0.2),
 ('x23', 'JOSH', 'Eu queria te perguntar uma coisa. Mas não sei como perguntar sem que soe errado.', 0.3),
 ('x24', 'N', 'Aurora ergueu uma sobrancelha. Na língua dela, uma sobrancelha erguida queria dizer: continue, mas com cuidado. Josh mediu cada palavra, como o padrinho tinha ensinado a medir argumentos:', 0.2),
 ('x25', 'JOSH', 'No baile... Eu vi que os rapazes... que ninguém...', 0.3),
 ('x26', 'N', 'Ela cortou. E a voz tinha voltado, em parte, à textura de porcelana. A armadura se armando de novo:', 0.2),
 ('x27', 'AU', 'Eu sei o que você viu. Não precisa descrever.', 0.3),
 ('x28', 'JOSH', 'Não estou descrevendo. Estou tentando entender.', 0.2),
 ('x29', 'AU', 'Entender o quê?', 0.2),
 ('x30', 'JOSH', 'Se é sempre assim.', 0.5),
 ('x31', 'N', 'Foi o silêncio mais longo que eles já tinham tido naquela cozinha. Kóngen parou de lamber a pata e ficou olhando os dois, como quem assiste a uma peça de teatro particularmente chata. Aurora pousou a caneca na mesa, devagar, com as duas mãos, como quem pousa uma arma antes de responder. E disse:', 0.25),
 ('x32', 'AU', 'Sim. É sempre assim.', 0.5),
 ('x33', 'N', 'Josh deixou a palavra assentar. Deixou o peso dela preencher o espaço entre os dois: dois anos de chás e jantares em que Aurora Svensson, a moça mais bonita da cidade, ficava encostada na parede, porque a cidade não sabia o que fazer com uma beleza que não cabia nas categorias que conhecia. Então perguntou, simplesmente:', 0.2),
 ('x34', 'JOSH', 'E por quê?', 0.3),
 ('x35', 'N', 'Aurora o olhou como se ele tivesse feito a pergunta mais ingênua e mais cruel do mundo ao mesmo tempo:', 0.2),
 ('x36', 'AU', 'Você sabe por quê.', 0.2),
 ('x37', 'JOSH', 'Sei. Mas quero ouvir você dizer.', 0.4),
 ('x38', 'N', 'Outra pausa. Aurora olhou para as próprias mãos na caneca. Mãos morenas, dedos finos. E quando falou, a voz estava limpa de tudo. Sem porcelana, sem verniz, sem armadura. Era a voz da cozinha às seis da manhã, antes de as defesas se armarem:', 0.25),
 ('x39', 'AU', 'Porque eu sou diferente. Não diferente como a Ingrid, que tem o pé, e que todos aceitam porque ela é dinamarquesa e o pé é um acidente. Diferente de nascença. Diferente de um jeito que lembra a todos que o meu pai é indiano, e que eu sou a prova viva de que aconteceu uma coisa que muitos consideram... inadequada.', 0.3),
 ('x40', 'AU', 'E eles me acham bonita. Eu sei que acham. Mas beleza que incomoda é pior do que feiura, Josh. Feiura se ignora. Beleza que incomoda não dá pra ignorar, e não dá pra aceitar. E aí as pessoas ficam presas nesse lugar horrível entre o querer e o não poder. E o resultado é exatamente o que você viu ontem. Olhares sem passos. Admiração sem coragem.', 0.5),
 ('x41', 'N', 'Josh ficou quieto por muito tempo. Não por falta do que dizer. Por excesso. Porque o que ela acabara de descrever, com uma lucidez impressionante e devastadora, não era só sobre bailes. Era sobre a vida inteira dela. Cada salão em que ela entrava, sentindo os olhos, e sabendo que os olhos ficariam onde estavam. Por fim, ele perguntou:', 0.2),
 ('x42', 'JOSH', 'E você? O que você quer?', 0.3),
 ('x43', 'N', 'Aurora piscou. Não era a pergunta que ela esperava. Ela repetiu: O que eu quero? E ele explicou:', 0.2),
 ('x44', 'JOSH', 'Dos rapazes. Da temporada. Do baile de estreia. O que você quer que aconteça?', 0.3),
 ('x45', 'N', 'Aurora abriu a boca. Fechou. Abriu de novo. Josh conhecia o gesto: era o que ele mesmo fazia quando a mãe perguntava algo cuja resposta o deixaria exposto. Ela respondeu devagar, como quem anda em terreno minado:', 0.2),
 ('x46', 'AU', 'Eu quero o que toda debutante quer. Dançar. Ser vista. Ser convidada. Ser... escolhida. Não pra casar com um homem de quarenta anos por conveniência, que é o que o meu pai provavelmente vai arranjar se a temporada não der em nada. Mas ser escolhida por alguém da minha idade. Alguém que me olhe e não veja uma complicação.', 0.5),
 ('x47', 'N', 'Complicação. A palavra saiu com um peso que fez Josh apertar a caneca. Aurora se via como uma complicação. Não como uma moça de dezessete anos de olhos cor de mel, com uma inteligência afiada e uma coragem silenciosa capaz de pôr de joelhos qualquer homem com meio cérebro. Uma complicação. Uma conta que não fecha. Josh sentiu a raiva de novo. E junto com a raiva, uma ideia. Ainda não formada. Uma semente. Como o primeiro broto que aparece na terra, quando se planta algo sem ter certeza de que vai nascer.', 0.4),
 ('x48', 'N', 'Aurora olhava a caneca de novo, com cara de quem se arrependeu de ter falado demais. Josh perguntou:', 0.2),
 ('x49', 'JOSH', 'Posso te dizer uma coisa?', 0.2),
 ('x50', 'AU', 'Depende do que for.', 0.2),
 ('x51', 'JOSH', 'Ontem, no baile, eu dancei com três moças.', 0.3),
 ('x52', 'N', 'Aurora não reagiu. Mas o maxilar endureceu, um movimento mínimo que só alguém que passava as manhãs a dois metros dela notaria. Josh continuou:', 0.2),
 ('x53', 'JOSH', 'E as três fizeram a mesma coisa. Riram de coisas que não tinham graça. Inclinaram a cabeça quando falavam. Tocaram no meu braço. Fizeram perguntas cuja resposta já sabiam. E quando eu respondia, olhavam para os meus olhos, não para o que eu dizia. É uma técnica. Funciona. Provavelmente funciona com noventa em cada cem homens.', 0.3),
 ('x54', 'N', 'A pergunta escapou de Aurora antes que ela pudesse segurar, rápida e nua:', 0.2),
 ('x55', 'AU', 'E funciona com você?', 0.3),
 ('x56', 'N', 'E ela imediatamente olhou para a janela, como se a pergunta tivesse sido feita pela janela, e não por ela. Josh escolheu responder com honestidade, a única língua que ele falava fluentemente:', 0.2),
 ('x57', 'JOSH', 'Não. Porque eu cresci numa fazenda, com uma mãe que não tolera fingimento e uma irmã que conversa com árvores. Eu sei a diferença entre alguém que está sendo de verdade e alguém que está representando. Você nunca representa. Esse é o seu problema.', 0.3),
 ('x58', 'N', 'Aurora virou-se devagar, e repetiu, com o começo de uma indignação: Meu problema? Josh precisava desarmar aquilo antes que virasse muralha:', 0.2),
 ('x59', 'JOSH', 'Não é um problema de verdade. É o oposto. Mas, para os rapazes daqui, é. Eles estão acostumados com o jogo. Com a risada ensaiada, o toque no braço, a pergunta que já sabe a resposta. E quando encontram alguém que não joga, que olha direto, que fala direto, eles não sabem o que fazer. Não é que não te queiram. É que não sabem como chegar.', 0.4),
 ('x60', 'N', 'Aurora ficou em silêncio. Josh via as engrenagens girando, os olhos dela indo de um lado para o outro, como sempre que ela processava algo que contrariava a história que tinha construído sobre si mesma. Então ela testou a teoria dele, com desafio na voz:', 0.2),
 ('x61', 'AU', 'E a minha aparência? Não tem a ver com a minha aparência?', 0.3),
 ('x62', 'JOSH', 'Tem. Tem tudo a ver. Mas não do jeito que você pensa. Não é que a sua aparência afaste eles. É que ela atrai, e eles não sabem lidar com a atração, porque ela vem embrulhada em algo que não reconhecem. Se você fosse bonita do jeito que eles esperam, loira, pálida, previsível, eles chegariam sem pensar. Mas você é bonita de um jeito que exige pensamento. E pensar assusta.', 0.5),
 ('x63', 'N', 'Só depois de terminar Josh percebeu que tinha dito mais do que pretendia. Muito mais. Que você é bonita de um jeito que exige pensamento não era análise da sociedade. Era uma confissão disfarçada. E Aurora, que nunca tinha sido boba, que era talvez a pessoa menos boba que ele já conhecera, percebeu.', 0.4),
 ('x64', 'N', 'O tom de cobre voltou às bochechas dela. Aquela cor quente que a amiga, Ingrid, tinha descrito no baile, e que Josh via de perto pela primeira vez, a dois metros, na luz limpa da cozinha às seis e meia da manhã. Era a coisa mais honesta que o rosto de Aurora sabia produzir. Ela perguntou, com a voz só um pouquinho mais aguda que o normal:', 0.2),
 ('x65', 'AU', 'Então o que você sugere? Que eu aprenda a representar?', 0.3),
 ('x66', 'JOSH', 'Não. Que você aprenda a deixar eles à vontade, sendo você mesma.', 0.2),
 ('x67', 'AU', 'E como se faz isso?', 0.4),
 ('x68', 'N', 'Josh olhou para ela. Ela olhou para ele. A cozinha, com a mesa de madeira bruta, as canecas lascadas, o gato cinzento e a chaleira morna, ficou suspensa num daqueles momentos em que o tempo não para, mas engrossa, como mel saindo do pote. E ele disse:', 0.2),
 ('x69', 'JOSH', 'Eu posso te mostrar.', 0.4),
 ('x70', 'N', 'As palavras saíram antes de serem pensadas. Como tinha saído o comentário sobre as roseiras. Como tinha saído o eles são idiotas, no hall. Vinham de um lugar que não era estratégia. Era instinto. O instinto de quem vê alguém preso e quer abrir a porta. Aurora piscou, e repetiu: Me mostrar? Ele explicou:', 0.2),
 ('x71', 'JOSH', 'O que os rapazes esperam. Como eles pensam. O que faz um homem se sentir à vontade o bastante para chegar perto, em vez de só olhar de longe.', 0.3),
 ('x72', 'AU', 'Você quer me ensinar a flertar.', 0.4),
 ('x73', 'N', 'Dito em voz alta, soava absurdo. Presunçoso, certamente. Quem era ele, um rapaz do campo, hóspede na casa dela, para se oferecer como professor de algo que mal dominava? Mas Josh tinha crescido numa fazenda. E numa fazenda, quando se vê um problema, não se fica parado discutindo quem é o mais qualificado. Resolve-se. Com as mãos. Com o que se tem. Ele corrigiu:', 0.2),
 ('x74', 'JOSH', 'Flertar, não. Eu sou péssimo em flertar. A Meridiana diz que o meu jeito de flertar é olhar pra pessoa como se estivesse avaliando gado.', 0.4),
 ('x75', 'N', 'E Aurora fez um som. Breve, inesperado, algo entre um sopro e um engasgo, que Josh, depois de um instante de espanto, reconheceu como riso. Aurora Svensson tinha rido. Não uma gargalhada. Um estilhaço de riso, que escapou antes que ela pudesse segurar. Curto, rouco, surpreso com a própria existência. E foi a coisa mais extraordinária que Josh tinha ouvido desde que chegara à cidade.', 0.4),
 ('x76', 'N', 'Ela pareceu tão surpresa quanto ele. Levou a mão à boca, como se pudesse empurrar o riso de volta para dentro. E Josh sentiu o sorriso torto, o de verdade, o que o irmão Dylan chamava de cara de idiota, puxar o canto da boca. Desta vez ele não segurou. Completou, com o sorriso na voz:', 0.2),
 ('x77', 'JOSH', 'Avaliando gado, não. Mas posso te ensinar o que eu sei. Que não é muito. Mas é honesto. E pelo que eu vi ontem, honestidade é a última coisa que aquele salão espera. O que talvez seja exatamente o que funcione.', 0.4),
 ('x78', 'N', 'Aurora tirou a mão da boca. O riso tinha passado, mas deixou uma abertura. Uma porta entreaberta, um centímetro, o bastante para a luz passar. Ela tentou usar a voz de porcelana, e não conseguiu, porque o riso ainda ecoava, como um sino depois que para de tocar:', 0.2),
 ('x79', 'AU', 'Deixa eu entender. Você está se oferecendo pra me ensinar a conquistar rapazes.', 0.3),
 ('x80', 'JOSH', 'Estou me oferecendo pra te mostrar como os rapazes funcionam. O que você faz com isso é problema seu.', 0.2),
 ('x81', 'AU', 'E o que você ganha com isso?', 0.4),
 ('x82', 'N', 'Era uma pergunta justa. O que ele ganhava? A gratidão dela? Uma convivência melhor? Algum senso de justiça? Ou algo menos nobre, que ele não podia dizer em voz alta, talvez nem para si mesmo. Estar perto dela. Ser necessário para ela. Ocupar na vida dela um lugar que não fosse o de intruso, nem de hóspede, nem de quase-irmão. Algo que ele não sabia nomear. Ele respondeu:', 0.2),
 ('x83', 'JOSH', 'Ganho parar de ver a moça mais interessante da cidade encostada na parede, enquanto as mais sem graça dançam a noite inteira.', 0.4),
 ('x84', 'N', 'E soube, ao dizer, que era verdade, e que era mentira, e que a proporção entre as duas coisas era perigosa. Aurora o estudou com aquela eficiência que ele conhecia desde o primeiro dia, a de quem avalia cavalos na feira. Mas havia algo a mais. Uma hesitação que não era dela. Ela estava considerando. De verdade. Pesando riscos e custos, com a seriedade com que o pai pesava negócios. E disse:', 0.2),
 ('x85', 'AU', 'Teria que ser segredo. Segredo absoluto. Se os meus pais souberem...', 0.2),
 ('x86', 'JOSH', 'Não vão saber.', 0.2),
 ('x87', 'AU', 'Se a Fru Larsen souber...', 0.2),
 ('x88', 'JOSH', 'A Fru Larsen não vai saber. Embora eu desconfie que a Fru Larsen sabe de tudo que acontece nesta casa antes de acontecer.', 0.4),
 ('x89', 'N', 'O canto esquerdo da boca de Aurora, era sempre o esquerdo, Josh anotou, se mexeu. Não um sorriso. A possibilidade de um. E ela perguntou:', 0.2),
 ('x90', 'AU', 'Quando?', 0.2),
 ('x91', 'JOSH', 'Quando você quiser.', 0.2),
 ('x92', 'AU', 'E onde?', 0.3),
 ('x93', 'N', 'Josh pensou. Precisavam de um lugar reservado. A cozinha, não: Fru Larsen chegava às seis e quarenta e cinco e tinha ouvido de morcego. A biblioteca, não: qualquer um podia entrar. Os quartos, impensável. O escritório do padrinho, sagrado. Ele decidiu:', 0.2),
 ('x94', 'JOSH', 'O jardim. Depois das suas aulas com a Fru Dahl, antes do almoço. Ninguém vai lá nesse horário.', 0.4),
 ('x95', 'N', 'Aurora olhou para ele um longo momento. Depois para a caneca. Depois para Kóngen, que dormia com a majestade de quem já sabe como essa história termina. E disse:', 0.25),
 ('x96', 'AU', 'Está bem.', 0.4),
 ('x97', 'N', 'Duas palavras. O som mais perigoso e mais promissor que Josh tinha ouvido em vinte e um anos de vida. Ele repetiu, porque não sabia o que mais dizer, e porque repetir as palavras dela era um jeito de firmá-las, antes que ela mudasse de ideia:', 0.2),
 ('x98', 'JOSH', 'Está bem.', 0.4),
 ('x99', 'N', 'Aurora se levantou, lavou a própria caneca no tanque, um gesto só dela, porque ninguém mais da família lavava a própria louça, e secou as mãos no pano de prato. Na porta, parou, e chamou o nome dele:', 0.2),
 ('x100', 'AU', 'Josh.', 0.2),
 ('x101', 'JOSH', 'Sim?', 0.3),
 ('x102', 'AU', 'Se você me ensinar a avaliar gado, eu vou saber que a Meridiana tinha razão.', 0.5),
 ('x103', 'N', 'E saiu. Josh ficou olhando a porta vazia. Depois Kóngen. Depois a caneca na própria mão, apertada com tanta força que os nós dos dedos estavam brancos. Soltou a caneca. Soltou o ar. E olhou o teto da cozinha, de vigas escuras, sem dossel, sem enfeite, sem nada que não fosse honesto. E na cabeça dele, como sempre que fazia algo ao mesmo tempo certo e perigoso, falou a voz da mãe: O que você está fazendo, Josh?', 0.4),
 ('x104', 'N', 'Ele respondeu em pensamento: Estou ajudando alguém que precisa de ajuda. Que não pediu. Que merece mais do que está recebendo. E o fato de ela ter olhos cor de mel e cheiro de jasmim não tem nada a ver. Fechou os olhos. Tem tudo a ver, mãe. Eu sei. E vou fazer assim mesmo. Porque Russels não fogem. Mas, Deus me ajude, eu devia fugir.', 0.5),
 ('x105', 'N', 'Abriu os olhos. Tomou o resto do chá. Estava frio. No campo, chá frio queria dizer que se ficou parado tempo demais. Josh levantou, lavou a caneca no tanque, como Aurora fazia, secou e guardou. E subiu para se arrumar para o café da manhã oficial. No corredor, o cheiro de jasmim e canela. Fresco. Ela tinha acabado de passar.', 0.4),
 ('x106', 'N', 'Josh respirou fundo, soltou devagar, e continuou andando. A primavera estava terminando. O verão vinha chegando. E algo que não tinha nome, que não pedia licença, e que crescia com a mesma teimosia das roseiras de Aarav, estava começando.', 0.0),
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
    sf.write(f"{SCR}/cap07-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap07-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap07-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
