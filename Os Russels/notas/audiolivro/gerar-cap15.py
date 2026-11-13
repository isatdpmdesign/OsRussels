import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts15"
SCR = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
# NOVAS vozes: Josh (Achird, jovem/caloroso), Dylan (Zubenelgenubi, casual/seco) — a AUDITAR com a autora
V = {"N": "Vindemiatrix", "AU": "Leda", "EL": "Gacrux", "RAJ": "Algieba",
     "JOSH": "Zubenelgenubi", "DYLAN": "Achird",
     "HELLE": "Achernar", "LARSEN": "Kore",
     "MIK": "Sulafat", "FRED": "Autonoe", "LOV": "Laomedeia", "CAS": "Pulcherrima", "SOL": "Despina", "ING": "Aoede", "CR1": "Erinome", "CR2": "Callirrhoe", "CR3": "Zephyr", "JOSHW": "Zubenelgenubi", "NM": "Vindemiatrix", "ERIK": "Iapetus", "HJ": "Puck", "LYK": "Zephyr"}
NARR_AF = "asetrate=24000*0.88,aresample=24000,atempo=1.1364"  # narradora grave

def tts(slug, voice, text, tries=4):
    body = {"contents": [{"parts": [{"text": text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    reqf = f"{BASE}/{slug}.req"; outf = f"{BASE}/{slug}.json"
    json.dump(body, open(reqf, "w"))
    for t in range(tries):
        try:
            subprocess.run(["curl", "-sS", "--retry", "3", "-X", "POST", URL+("?key="+os.environ["GKEY"] if os.environ.get("GKEY") else ""),
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
AI = "Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: "
SEG = [
 ('f001', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo quinze: A festa.', 1.2),
 ('f002', 'N', 'Este capítulo é contado pelos olhos de Josh. No capítulo anterior, Ingrid convidou Aurora para uma festa dos jovens, sem pais e sem chaperona, na casa dos Eriksen. Aurora mentiu em casa, mandou fazer um vestido amarelo, e pediu a Josh que não a impedisse. Ele respondeu que não ia impedir, mas que ia junto. E na casa de Ingrid, ao ver Aurora de amarelo, com o cabelo solto, ele esqueceu como falar.', 0.6),
 ('f003', 'N', 'A casa dos Ériksen não era uma casa. Era um celeiro. Um celeiro reformado nos fundos de uma propriedade em Kristiánshaun, o bairro do outro lado do canal, onde as ruas eram mais estreitas, os prédios mais coloridos, e a respeitabilidade da Brédigueide parecia coisa de outro país. Os três caminhavam para lá. Ingrid na frente, com o passo decidido de quem já tinha feito aquele trajeto outras vezes. Aurora no meio, o vestido amarelo brilhando absurdo sob os lampiões, as ondas escuras do cabelo balançando nos ombros. E Josh atrás das duas, com as mãos nos bolsos, consciente de que ia entrar num lugar para o qual nada na vida dele o tinha preparado. Ingrid avisou, sem se virar:', 0.2),
 ('f004', 'ING', 'Diga em português do Brasil, com sotaque brasileiro: Três quarteirões. Aliás, dois e meio. Se ouvirem música, é ali.', 0.4),
 ('f005', 'N', 'Eles ouviram. Não a música formal dos salões. Não era violino e cravo. Era violino e acordeão, um ritmo rápido, sujo, vivo, com um pé batido no fundo que ele reconheceu antes de a cabeça entender. Era o pé das festas do campo. Das colheitas, dos casamentos da roça, das tardes em que o pai dele, Henrik Russel, quando ainda havia um Henrik Russel para fazer essas coisas, tirava uma vizinha para dançar no celeiro da família, e o menino Josh achava o barulho das botas no chão de madeira a melhor coisa do mundo. Aurora virou o rosto para trás. Os olhos de mel, sob o lampião da esquina, estavam dourados:', 0.2),
 ('f006', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Está ouvindo? É música de festa de verdade.', 0.2),
 ('f007', 'JOSH', 'É música do campo.', 0.2),
 ('f008', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Ah. Então você sabe dançar.', 0.2),
 ('f009', 'JOSH', 'Sei dançar isso. Não sei dançar valsa.', 0.2),
 ('f010', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Você dança valsa pessimamente.', 0.3),
 ('f011', 'N', 'Ele perguntou, com um sorriso se abrindo no canto da boca, gostando de saber que ela tinha reparado nele:', 0.2),
 ('f012', 'JOSH', 'Como você sabe, se nunca dançou comigo?', 0.2),
 ('f013', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Eu vi você dançando com a Frederikke no sarau dos Holst. E não foi bonito. Parecia que você estava pisando nos pés dela de propósito.', 0.2),
 ('f014', 'JOSH', 'Ei! Eu não pisei nos pés dela em momento nenhum. Ela que pisou nos meus!', 0.2),
 ('f015', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Isso só confirma que você não sabe dançar!', 0.2),
 ('f016', 'JOSH', 'Claro que não! Isso não quer dizer que eu não sei dançar. Só que eu não sei dançar valsa!', 0.3),
 ('f017', 'N', 'Ingrid, dois passos à frente, soltou um som que era meio riso, meio reclamação:', 0.2),
 ('f018', 'ING', 'Diga em português do Brasil, com sotaque brasileiro: Pelo amor de Deus, vocês dois. Se vocês conversarem assim a noite inteira, eu vou precisar de muito mais ponche do que eu esperava.', 0.4),
 ('f019', 'N', 'Aurora riu e voltou a andar. E ele, atrás, observou, sem conseguir evitar, como o amarelo do vestido capturava cada lampião e o devolvia como uma vela acesa, como se Aurora caminhasse acompanhada da própria luz.', 0.4),
 ('f020', 'N', 'A casa dos Eriksen apareceu na curva: um sobrado modesto, o portão aberto, lampiões pendurados em fios cruzados iluminando o caminho de pedras até os fundos, onde o celeiro reformado se erguia, baixo e largo, com as janelas amareladas e o som transbordando pelas frestas como água de uma represa cheia. Quem abriu o portão foi um dos filhos da casa: Iálmar Eriksen, um rapaz alto, mais ou menos da idade de Ingrid, com a camisa fora da calça e a cara satisfeita de quem já estava na segunda cerveja antes do começo oficial dos trabalhos. Ele abriu os braços:', 0.2),
 ('f021', 'HJ', 'Diga em português do Brasil, com sotaque brasileiro: Ingrid! Você veio. Eu disse pra Lúque que você vinha. E quem é o cordeiro?', 0.2),
 ('f022', 'N', 'Ingrid passou direto pelo abraço, com a eficiência de quem cumpre a primeira etapa de uma operação maior, e fez as apresentações:', 0.2),
 ('f023', 'ING', 'Diga em português do Brasil, com sotaque brasileiro: Aurora Svensson. Josh Russel. Iálmar Eriksen, sem maiores graças.', 0.3),
 ('f024', 'N', 'Iálmar fingiu se ofender com o sem maiores graças, e esqueceu o assunto no mesmo segundo. Olhou para Aurora. Olhou para o vestido amarelo. Levou três segundos para lembrar de fechar a boca:', 0.2),
 ('f025', 'HJ', 'Diga em português do Brasil, com sotaque brasileiro: Aurora Svensson? A própria Aurora Svensson?', 0.2),
 ('f026', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Existe outra?', 0.2),
 ('f027', 'HJ', 'Diga em português do Brasil, com sotaque brasileiro: Não que eu saiba. Bem-vindos. O ponche é horrível. A cerveja é decente. A comida é melhor do que vocês imaginam, porque a Lúque fez uma parte. A Lúque está lá dentro, vai vir dizer oi.', 0.2),
 ('f028', 'N', 'E olhou para Josh de cima a baixo, devagar, sem pressa e sem nenhuma vergonha, com um interesse que não tinha nada de avaliação de rival. Ele percebeu. E percebeu também, com uma surpresa que guardou para si, que não se incomodou. No campo, aquilo não se dizia, mas existia. E Iálmar parecia ter decidido, ao menos ali, nos fundos do próprio quintal, não esconder.', 0.2),
 ('f029', 'HJ', 'Diga em português do Brasil, com sotaque brasileiro: Russel, prazer. Muito prazer. Tem gente no quintal jogando uma coisa que parece dardos, mas que na verdade é um crime. Se quiser participar.', 0.2),
 ('f030', 'JOSH', 'Talvez mais tarde.', 0.4),
 ('f031', 'N', 'Iálmar deu de ombros e voltou ao portão, para receber quem vinha atrás. Os três atravessaram o caminho de pedras. Uma menina pequena, de uns dez anos, passou correndo no sentido contrário com um prato vazio nas mãos e a trança balançando. Outra Eriksen, presumivelmente. Aquela família tinha filhos de todos os tamanhos, e nenhum deles parecia incomodado com a festa no fundo do quintal. Era um jeito de viver que Josh reconheceu como quase do campo, uma coisa no meio do caminho, que a cidade em geral não permitia.', 0.4),
 ('f032', 'N', 'A porta do celeiro se abriu, e uma onda de luz alaranjada, barulho e calor caiu sobre os três. Lanternas de papel penduradas em fios de parede a parede. Velas em garrafas espalhadas pelo chão e pelas mesas improvisadas: tábuas sobre cavaletes, com toalhas que já tinham visto dias melhores. Um canto com barris de cerveja e uma tina enorme de ponche, de uma cor inquietante, de líquido com ambições medicinais. E num canto, o violinista e o acordeonista, tocando aquela melodia que fazia os pés quererem se mexer antes de o cérebro autorizar.', 0.4),
 ('f033', 'N', 'Umas quarenta pessoas. Talvez cinquenta. Ele tentou contar e desistiu: tudo se mexia demais. Casais girando no meio. Grupinhos encostados nas paredes, de caneca na mão. Três rapazes cantando alguma coisa que devia ser obscena, pelas risadas das moças mais perto. Uma moça ruiva sentada num barril, com os pés balançando no ar, contando uma história para três amigas de boca aberta. E em todas as direções, ele percebeu na mesma fração de segundo, cabeças começaram a virar. Para Aurora.', 0.4),
 ('f034', 'N', 'Não pelo nome. Ali, o sobrenome dela não significava nada. Era o vestido. O cabelo. O conjunto. A maioria das moças usava vestidos simples, de cores neutras, com o cabelo meio preso. E no meio delas, Aurora, de amarelo girassol, as ondas escuras até o meio das costas, e aquele porte que a mãe costurou nela desde os seis anos, e que nem um celeiro do outro lado do canal conseguia desfazer. Aurora chamava atenção de um jeito que fazia uma sala inteira parar. E Aurora, e esse foi o detalhe que ele guardou por muito tempo, não pareceu se importar. Olhou em volta com curiosidade aberta. Sem o queixo erguido de defesa. Sem o sorriso medido de salão. Como quem olha uma cidade nova pela janela de uma carruagem que está chegando.', 0.4),
 ('f035', 'N', 'Lúque Eriksen apareceu no caminho: uma das filhas da casa, vinte e poucos anos, vestido vermelho e uma fita atrevidamente solta no cabelo. Agarrou o braço de Ingrid:', 0.2),
 ('f036', 'LYK', 'Diga em português do Brasil, com sotaque brasileiro: Ingrid! E Aurora Svensson. E o famoso Josh Russel.', 0.2),
 ('f037', 'N', 'E olhou para Aurora com a admiração franca de mulher para mulher:', 0.2),
 ('f038', 'LYK', 'Diga em português do Brasil, com sotaque brasileiro: Foi a Madame Solberg que cortou essa maravilha?', 0.2),
 ('f039', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Foi a Madame Solberg, sim.', 0.2),
 ('f040', 'LYK', 'Diga em português do Brasil, com sotaque brasileiro: Diz pra ela que eu vou aparecer no ateliê na segunda-feira, gritando por uma coisa parecida.', 0.2),
 ('f041', 'N', 'Lúque se virou para Josh, com a caneca de ponche que vinha segurando o tempo todo:', 0.2),
 ('f042', 'LYK', 'Diga em português do Brasil, com sotaque brasileiro: Rapaz, bebe isso aqui. Quem chega sóbrio em festa minha sai me devendo.', 0.2),
 ('f043', 'JOSH', 'Que tipo de cobrança?', 0.2),
 ('f044', 'N', 'Lúque piscou um olho, e respondeu:', 0.2),
 ('f045', 'LYK', 'Diga em português do Brasil, com sotaque brasileiro: Cobrança pessoal. E é melhor pagar logo.', 0.3),
 ('f046', 'N', 'Ele aceitou a caneca. Bebeu. O ponche era exatamente o que ele esperava: doce, medicinal, com promessa firme de dor de cabeça antes do amanhecer. Lúque observou o gole com a expressão divertida de quem já viu muitos rapazes fazerem a mesma careta, e gostou de todas as vezes:', 0.2),
 ('f047', 'LYK', 'Diga em português do Brasil, com sotaque brasileiro: Sobreviveu. Promissor. Bem-vindos, todos. Eu fico devendo uma conversa. O Iálmar me mata se eu não voltar pra cozinha. E a pista é livre. Ninguém precisa pedir licença pra ninguém. Esse é o ponto da festa.', 0.4),
 ('f048', 'N', 'E sumiu. Aurora ficou parada ao lado dele um instante. Olhou o salão. Olhou Ingrid, que já estava a três metros, conversando com duas moças que tinham surgido do nada. E ele disse, baixo:', 0.2),
 ('f049', 'JOSH', 'Diga com voz de homem jovem, grave, baixa e aveludada, calma, sem animação: Pode ir. Vai lá, aproveita.', 0.2),
 ('f050', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Você não vem?', 0.2),
 ('f051', 'JOSH', 'Vai. Você veio pra isso. Não veio pra ficar perto da porta com um rapaz do campo. Vai conhecer gente. Dançar. Ver o que essa festa tem. Eu fico aqui.', 0.2),
 ('f052', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Você fica aqui?', 0.2),
 ('f053', 'N', 'Ele levantou um pouco a caneca terrível, e respondeu:', 0.2),
 ('f054', 'JOSH', 'Eu fico aqui. Eu e esse ponche. Tenho um inimigo pra enfrentar.', 0.4),
 ('f055', 'N', 'Ela considerou. Houve um segundo em que ele viu a hesitação dela: o impulso de ficar, de não se separar, de continuar ao lado dele, onde se sentia segura. E houve o segundo seguinte, em que ela entendeu o que ele estava oferecendo: permissão para ser, naquela festa, só Aurora. Ela respondeu:', 0.2),
 ('f056', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Está bem.', 0.2),
 ('f057', 'JOSH', 'Diga com voz de homem jovem, grave, baixa e aveludada, calma, sem animação: Mas espera.', 0.2),
 ('f058', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: O que foi?', 0.2),
 ('f059', 'JOSH', 'Diga com voz de homem jovem, grave, baixa e aveludada, calma, sem animação: Se alguém te incomodar, eu estou aqui. Estou de olho em você.', 0.4),
 ('f060', 'N', 'Ela sorriu, o sorriso real, o do canto esquerdo, e se afastou. E ele ficou encostado na parede do celeiro, com o ponche horrível na mão, e fez o que tinha ido fazer naquela noite. Observou.', 0.6),
 ('f061', 'N', 'Aurora dançou primeiro com as moças. Uma roda de quatro, que começou quando o violino acelerou e Ingrid a arrastou para o meio. Aurora não sabia o passo. Errou. Riu do próprio erro, com a leveza de quem aprende na hora. As outras acharam graça. Em três minutos, ela dançava como se sempre tivesse dançado aquilo. O cabelo solto voava a cada giro. O vestido amarelo se abria como uma flor. E ele, contra a parede, percebeu que estava sorrindo com uma boca que não tinha autorizado a sorrir.', 0.4),
 ('f062', 'N', 'Depois um rapaz a convidou. Um desconhecido. Magro, alto, de camisa azul, do tipo que dança bem e sabe disso. Aurora aceitou com a leveza de quem aceita um copo de água. Dançaram. O rapaz tentou conversar. Josh viu a boca dele se mexer, a postura se inclinar um pouco mais do que precisava, a mão dele na cintura dela, numa posição tecnicamente correta, mas que, aos olhos de Josh, era uma fronteira sendo testada. Aurora respondeu com sorrisos cordiais, respostas curtas, o queixo erguido na medida exata das aulas no jardim. O rapaz desistiu depois de uma música. Agradeceu. E foi embora. Josh bebeu o ponche.', 0.4),
 ('f063', 'N', 'Aurora dançou com mais duas pessoas. Conversou com Ingrid, com três moças desconhecidas, com Iálmar, que voltou da cozinha com pão e queijo e que, debaixo da camisa fora da calça, era hospitaleiro de um jeito que Josh aprovou. Em algum momento ela provou o ponche, só pelo gosto, e fez uma careta de horror que fez Iálmar e Ingrid rirem juntos. E em algum momento, ele não soube dizer quanto tempo depois, porque o tempo dentro daquele celeiro era outro, Aurora voltou para perto dele:', 0.2),
 ('f064', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Aqui está você.', 0.2),
 ('f065', 'JOSH', 'Aqui estou eu.', 0.2),
 ('f066', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Você ainda não dançou.', 0.2),
 ('f067', 'N', 'Ele deu de ombros, e respondeu:', 0.2),
 ('f068', 'JOSH', 'Não. E não vou dançar.', 0.2),
 ('f069', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Por que não? No caminho você disse que sabe dançar. Só não sabe valsar!', 0.2),
 ('f070', 'N', 'Ele olhou para ela com um sorriso leve, atrevido, que fez os olhos dela ficarem de um tom mais quente, de uma curiosidade genuína que ele nunca tinha visto:', 0.2),
 ('f071', 'JOSH', 'Eu sei dançar. Mas estou observando.', 0.2),
 ('f072', 'N', 'Sem poder confessar que, na verdade, era ela quem ele observava com atenção demais. Aurora quis saber, interessada:', 0.2),
 ('f073', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: E já chegou a alguma conclusão?', 0.2),
 ('f074', 'N', 'Ele pensou por um instante, e respondeu:', 0.2),
 ('f075', 'JOSH', 'Que os rapazes daqui são mais corajosos do que os do baile dos Frederiksen.', 0.2),
 ('f076', 'N', 'Aurora ergueu o queixo, e provocou:', 0.2),
 ('f077', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Coragem ou despreparo?', 0.2),
 ('f078', 'JOSH', 'Os dois. Os dois costumam viajar juntos.', 0.4),
 ('f079', 'N', 'Aurora riu, o riso aberto que tinha começado a aparecer na roda das moças, agora um pouco mais largo, como se a festa estivesse liberando uma versão dela que vivia esperando autorização. Os músicos passaram para uma coisa mais lenta. Não era valsa. Não era nada que Madame Solberg aprovaria num salão. Era uma melodia popular que ele conhecia vagamente do campo. As pessoas começaram a formar pares. Ela perguntou:', 0.2),
 ('f080', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Você sabe essa?', 0.2),
 ('f081', 'JOSH', 'Conheço, sim. Essa eu conheço.', 0.2),
 ('f082', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Eu duvido.', 0.2),
 ('f083', 'JOSH', 'Sei o suficiente pra não pisar nos seus pés.', 0.2),
 ('f084', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Esse é um padrão muito baixo.', 0.2),
 ('f085', 'JOSH', 'É o padrão da casa.', 0.3),
 ('f086', 'N', 'E Aurora estendeu a mão. Ele olhou para ela um segundo a mais do que devia. A mão pequena, aberta no ar entre os dois, esperando. Eles nunca tinham dançado juntos. Em quatro meses de cozinha, de jardim, de lições e de brigas, nunca. E ele soube, antes de tocar, que aquela não ia ser uma dança qualquer, numa festa qualquer. Pegou a mão dela.', 0.4),
 ('f086b', 'N', 'Os dedos dela se fecharam nos dele. Ele levou a outra mão à cintura dela devagar, como quem avisa antes de tocar, e sentiu o tecido amarelo, fino, e debaixo dele o calor. Aurora prendeu a respiração. Ele ouviu. Ela pousou a mão livre no ombro dele, e o peso era quase nada. E mesmo assim, aquele quase nada atravessou a camisa.', 0.4),
 ('f086c', 'N', 'Começaram. Não bem. Ela pisou no pé dele no primeiro compasso, ele pisou no dela no terceiro e no sétimo, e os dois fingiram que aquilo era um sucesso. Ela riu baixo, com a testa quase encostada no peito dele, e o riso subiu pela camisa como calor. Ele fez um esforço deliberado de pensar em coisas neutras, Montesquiê, a colheita de aveia, a quantidade de talheres de um jantar formal, para o corpo não trair a cabeça mais do que já traía. Não adiantou.', 0.4),
 ('f086d', 'N', 'Porque no meio da música, Aurora ergueu os olhos. E não desviou. Na luz alaranjada das lanternas, o mel dos olhos dela tinha virado âmbar escuro, e ele viu ali a mesma pergunta que vinha se fazendo a noite inteira: quanto tempo se pode olhar para alguém assim, antes que o olhar vire uma resposta? Ele não sabia. Contou, porque contar era o que ele fazia quando não sabia. Um segundo. Dois. Três. No quarto, a mão dela deslizou do ombro para a nuca dele. Um centímetro, talvez dois, como se tivesse escorregado sem querer. Não tinha sido sem querer. Ele soube pelo jeito como ela corou, e não tirou a mão. E ela disse, baixinho:', 0.2),
 ('f086e', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Você disse que não pisava nos pés de ninguém.', 0.3),
 ('f086f', 'N', 'E a voz dele saiu mais rouca do que devia:', 0.2),
 ('f086g', 'JOSH', 'Diga com voz de homem jovem, grave, baixa e aveludada, calma, sem animação: Eu menti. É que é difícil olhar pro chão com você olhando pra mim desse jeito.', 0.5),
 ('f086h', 'N', 'O cabelo solto roçou o braço dele quando ela girou. Cheiro de jasmim e de verão. Em volta deles, o celeiro continuava: o violino, o acordeão, as botas no chão de madeira, Ingrid rindo num canto. Mas para ele, o mundo tinha encolhido até caber entre as duas mãos.', 0.4),
 ('f087', 'N', 'Quando a música acabou, ele não soltou na hora. Ela também não recuou. Por uns três segundos, ele contou, ele sempre contava, os dois ficaram parados, como se a música ainda tocasse. E ela disse, num tom mais baixo:', 0.2),
 ('f088', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Quer me mostrar o resto do celeiro?', 0.2),
 ('f089', 'JOSH', 'Eu não conheço o resto do celeiro.', 0.2),
 ('f090', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Eu também não. Por isso eu quero ver.', 0.4),
 ('f091', 'N', 'Ela foi na frente. Ele atrás. Atravessaram o salão sem pressa, porque pressa seria visível. No caminho, Aurora trocou uma frase curta com Ingrid. E Ingrid olhou para Josh por cima do ombro da amiga com aquele meio sorriso das pessoas que sabem mais do que contam. Não disse nada. Voltou a conversar com a moça do lado.', 0.4),
 ('f092', 'N', 'A porta dos fundos dava num corredor estreito, com cheiro de feno antigo e madeira úmida. Quase sem luz: uma única lanterna num gancho, a uns dez metros, com a chama baixa. Quando a porta se fechou, os sons da festa viraram um zumbido distante, como se a noite acontecesse em outro andar. O corredor terminava num pequeno depósito. Paredes de pedra, teto baixo, cheiro de pó e palha. Sacos empilhados num canto, e uma janela alta, de vidro grosso, por onde a lua entrava em diagonal, deixando uma faixa de luz prateada no chão de pedra. Aurora parou no meio dessa faixa.', 0.4),
 ('f093', 'N', 'Ficou de costas para ele por um momento. Os braços descobertos pelas mangas curtas, o cabelo escuro caindo, o amarelo do vestido virando ouro pálido sob a lua. Ele ficou na entrada, sem saber se entrava ou se ficava. A regra do corpo dizia para entrar. A regra da cabeça dizia para ficar. Aurora se virou. E chamou, baixinho:', 0.2),
 ('f094', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Josh.', 0.2),
 ('f095', 'JOSH', 'Diga com voz de homem jovem, grave, baixa e aveludada, calma, sem animação: Fala. Eu estou ouvindo.', 0.2),
 ('f096', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Se eu te pedisse uma coisa, você faria?', 0.4),
 ('f097', 'N', 'Ele sentiu o ar mudar. Não o ar de verdade, que continuava cheirando a palha. Mas o que estava em volta deles deixou de ser ambiente e virou consequência. Cada respiração contava. Cada milímetro contava. Ele respondeu, com cuidado:', 0.2),
 ('f098', 'JOSH', 'Depende do que é.', 0.2),
 ('f099', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Não depende.', 0.2),
 ('f100', 'JOSH', 'CLIP:josh_aurora_intenso', 0.3),
 ('f100b', 'N', 'Não era um chamado. Era um aviso. Olha o caminho que você está pegando. Mas ela insistiu:', 0.2),
 ('f101', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Não depende. É sim ou não.', 0.3),
 ('f102', 'N', 'Ela hesitou um instante. E então continuou, baixinho:', 0.2),
 ('f103', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Eu nunca fui beijada. Todas as moças da minha idade já foram. Eu só queria saber como é.', 0.4),
 ('f104', 'N', 'Ela deu um passo na direção dele. Não dois. Um. A faixa de luz prateada se quebrou sobre o ombro dela. Ele respirou fundo, devagar, sabendo que estava ganhando tempo. Examinou o rosto dela. Na penumbra, o âmbar dos olhos tinha quase sumido: restavam as pupilas grandes. Não estavam molhados. Não estavam suplicando. Estavam decididos. E a parte dele que sabia ler as pessoas, a que aprendeu com a mãe a temperatura de um silêncio, e com o pai o estado de uma colheita antes da chuva, entendeu que Aurora não estava pedindo um beijo do jeito que uma moça de dezessete anos pede um beijo. Estava pedindo uma resposta. A uma pergunta que vinha fazendo a si mesma havia semanas.', 0.3),
 ('f105', 'N', 'E isso era pior. Um beijo, ele podia recusar por cortesia. Uma resposta, só podia recusar por princípio. Quando ele falou, a voz saiu mais baixa do que pretendia, com aquela aspereza rouca que ela tinha quando ele estava muito cansado ou muito emocionado, e que ele odiava, porque era fácil de ler:', 0.2),
 ('f106', 'JOSH', 'Diga com voz de homem jovem, grave, baixa e aveludada, calma, sem animação: Você acha que eu não quero? Eu passei a noite inteira contando as vezes que você girou naquele salão. Se eu te beijar agora, eu não vou saber parar no beijo. Eu me conheço. E você merece que a primeira vez seja de alguém que pode te beijar de dia, na frente do mundo. Não de um rapaz escondido num depósito, debaixo do teto do homem que confiou a filha a ele.', 0.4),
 ('f107', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Eu não estou pedindo o mundo.', 0.2),
 ('f108', 'JOSH', 'Diga em português do Brasil, com sotaque brasileiro, num tom baixo, quase uma súplica: Por favor, Aurôra...', 0.3),
 ('f111', 'N', 'Ela deu outro passo. Estava perto o bastante para ele sentir o cheiro de jasmim e canela, cortado por alguma coisa que era só pele e calor. E disse:', 0.2),
 ('f112', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Eu sei o que eu quero. Há semanas eu sei. Eu durmo todas as noites com a certeza de que eu sei. E o que me destrói não é saber. É não ter dito. Eu não estou pedindo o mundo, Josh. Estou pedindo você.', 0.5),
 ('f113', 'N', 'Era a frase contra a qual ele não tinha defesa nenhuma. A mão dela tocou a mão dele. Os dedos dela, frios. A ponta dos dedos dele tremendo um milímetro, e ele se odiou por isso. Não era um tremor que ela fosse ver. Mas existia. E ele o reconhecia: era o tremor que vinha antes das decisões em que ele pouco confiava em si mesmo. Ele disse, e já não era argumento. Era quase uma súplica:', 0.2),
 ('f114', 'JOSH', 'Diga com voz de homem jovem, grave, baixa e aveludada, calma, sem animação: Você não sabe o que está me pedindo.', 0.3),
 ('f115', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Por favor. Estou pedindo. Me beija.', 0.6),
 ('f122', 'N', 'Ele se inclinou. Era impossível não se inclinar. Depois de oito semanas de regras internas, doze contagens de passos e cinco lições no jardim de Aarav, o corpo dele finalmente respondeu sem pedir licença ao cérebro. Ela ergueu o rosto. O cabelo escorregou do ombro descoberto para a clavícula. E ele sentiu, com uma precisão que doía, o ar entre os lábios dos dois. Alguns centímetros. Depois menos que centímetros. Depois milímetros. Depois quase nada. Mas uma voz o interrompeu, vinda do salão. Um chamado claro, masculino, descontraído, do tipo que já espera resposta:', 0.2),
 ('f123', 'ERIK', 'Diga em português do Brasil, com sotaque brasileiro: Aurora? Aurora? Eu acabei de falar com a Ingrid, ela disse que você estava aqui. Eu estou no celeiro principal.', 0.4),
 ('f124', 'N', 'Erik Mortensen. Aurora congelou. Não recuou de imediato. Mas o corpo dela mudou, e ele sentiu antes de ver. A respiração dela parou. Os dedos dela apertaram a mão dele por um instante, depois afrouxaram. E os olhos, ele ainda estava perto o bastante para vê-los na meia-luz, passaram de decididos para outra coisa. Pânico, talvez. Não pânico de menina. Pânico de quem ouve, no meio de uma fuga, a porta da própria casa se abrir lá longe. Ela sussurrou o nome dele:', 0.2),
 ('f125', 'AU', 'Diga em português do Brasil, num sussurro aflito: Josh...', 0.2),
 ('f126', 'JOSH', 'Diga com voz de homem jovem, grave, baixa e aveludada, calma, sem animação: Vai. Ele está te procurando.', 0.2),
 ('f127', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Eu...', 0.2),
 ('f128', 'JOSH', 'Diga com voz de homem jovem, grave, baixa e aveludada, calma, sem animação: Pode ir. Eu fico aqui, está tudo bem.', 0.4),
 ('f129', 'N', 'Ela recuou. Um passo. Dois. A faixa de luz da janela passou pelo ombro dela, pelas costas, pelo cabelo, enquanto ela se virava e atravessava o depósito. A mão dela soltou a dele com uma lentidão que doeu mais do que devia. Na porta, ela parou. Não olhou para trás:', 0.2),
 ('f130', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Me desculpa.', 0.2),
 ('f131', 'JOSH', 'Não tem por quê.', 0.2),
 ('f132', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Tem, sim.', 0.2),
 ('f133', 'JOSH', 'Diga com voz de homem jovem, grave, baixa e aveludada, calma, sem animação: Tudo bem. Você não tem culpa de nada.', 0.5),
 ('f134', 'N', 'A porta do corredor se abriu e se fechou. O zumbido da festa voltou por um segundo, e foi cortado. Ele ficou no meio do depósito, com a lua entrando pela janela e a faixa prateada agora vazia no chão de pedra. E contou até cem antes de se mexer.', 0.6),
 ('f135', 'N', 'Quando atravessou o corredor de volta, a chama da lanterna ainda balançava da passagem dela. Quando empurrou a porta do celeiro, a festa já tinha engolido Aurora. Ela estava com Erik, num canto da pista, sorrindo aquele sorriso medido de salão, que voltou como uma luva que se calça num gesto. Erik tinha uma mão no cotovelo dela. Uma mão respeitosa, casual, do tipo que diz aos outros homens: está comigo, tudo em ordem. Ele não tinha vindo como invasor, Josh entendeu de longe. Tinha vindo como protetor. Tinha ouvido em algum lugar que Aurora estava num lugar como aquele, e o Erik que Josh conhecia, educado, correto, tinha vindo conferir. Não por ciúme. Por preocupação. E isso era pior que ciúme. Era cortejo de boa-fé. Aurora sorriu, disse alguma coisa que ele não ouviu, e os dois entraram na dança seguinte.', 0.4),
 ('f136', 'N', 'Ele não tinha o direito de odiar Erik Mortensen. Erik não tinha feito nada de errado. Era um rapaz educado, alto, de cabelo castanho claro, casaco bem cortado e reputação cordial, e a cidade gostava dele com a tranquilidade com que gosta das coisas que conhece bem. Erik estava cumprindo o papel dele. Josh sabia disso. Entendia. Num lugar bem distante da cabeça, até respeitava. Mas a mão de Erik no cotovelo de Aurora era a mão de Erik no cotovelo de Aurora. E a mesma regra que o impediu de beijá-la cinco minutos antes era a regra que agora o impedia de atravessar o salão e dar um soco no rosto do rapaz educado.', 0.4),
 ('f137', 'N', 'Ele cruzou o salão até Ingrid. Ela estava na mesa de pão e queijo, fingindo escolher um pedaço de queijo que já tinha escolhido três vezes. Ergueu os olhos:', 0.2),
 ('f138', 'ING', 'Diga em português do Brasil, com sotaque brasileiro: Você está bem?', 0.2),
 ('f139', 'N', 'Ele indicou Aurora com um movimento da cabeça, e disse:', 0.2),
 ('f140', 'JOSH', 'Estou bem. Estou indo embora.', 0.2),
 ('f141', 'ING', 'Diga em português do Brasil, com sotaque brasileiro: Quer que eu cuide dela?', 0.2),
 ('f142', 'JOSH', 'Por favor.', 0.2),
 ('f143', 'ING', 'Diga em português do Brasil, com sotaque brasileiro: Eu cuido. Ah, e mais uma coisa.', 0.2),
 ('f144', 'JOSH', 'Pode falar.', 0.2),
 ('f145', 'ING', 'Diga em português do Brasil, com sotaque brasileiro: Eu não chamei o Erik. Só pra constar. Eu não disse a ninguém que ela estaria aqui. A mãe dela deve ter comentado com a mãe dele que a Aurora ia dormir lá em casa, e o Erik fez a conta sozinho.', 0.2),
 ('f146', 'JOSH', 'Eu imaginei.', 0.2),
 ('f147', 'ING', 'Diga em português do Brasil, com sotaque brasileiro: Eu sei que você sabe. Mas eu queria dizer.', 0.4),
 ('f148', 'N', 'Ele assentiu. Olhou uma última vez o salão: Aurora girando, o amarelo se abrindo, o cabelo solto, o sorriso medido que ela tinha voltado a vestir, e Erik com a postura correta de quem já conduziu cem moças por cem salões. Era uma cena bonita. Absolutamente correta. E doía como dói uma luz forte nos olhos depois do escuro.', 0.2),
 ('f149', 'JOSH', 'Boa noite, Ingrid.', 0.2),
 ('f150', 'ING', 'Diga em português do Brasil, com sotaque brasileiro: Boa noite pra você também.', 0.6),
 ('f151', 'N', 'Ele saiu. Não pela porta principal: pela lateral, a mesma por onde a menina pequena tinha passado correndo no começo da noite. Atravessou o quintal sem olhar para trás. Passou pelo portão. Entrou na rua estreita do outro lado do canal, com os prédios coloridos engolidos pela noite e as pedras brilhando úmidas sob os lampiões. E caminhou.', 0.4),
 ('f152', 'N', 'A volta até a Brédigueide, a pé, era longa: mais de uma hora. Em outra noite, ele teria pegado um dos barcos que cortavam o canal por uma moeda. Naquela noite, preferiu a ponte. O ar do canal era frio mesmo em agosto, uma friagem úmida que o ponche tinha ajudado a esconder e que agora entrava de volta pelos punhos e pela gola aberta da camisa. Ele gostou do frio. Era um problema que tinha solução: bastava chegar em casa e fechar uma porta. Os outros problemas não cabiam em portas.', 0.4),
 ('f153', 'N', 'Caminhou. Pensou no rosto de Aurora quando ela pediu. Pensou no rosto dela quando ouviu a voz de Erik. Pensou na própria mão sobre a dela por dois segundos, na maciez do polegar dela. E lembrou da mãe, Casandra, anos antes, quando ele tinha catorze anos e quase quebrou uma vidraça de raiva. Ela disse, na época: Russels não fogem do que sentem. Mas Russels também não fazem nada do que sentem antes de pensar. Pensar. Ele pensou.', 0.6),
 ('f154', 'N', 'A Brédigueide apareceu. Devagar, depois mais perto, depois ali. O casarão dos Svensson, o tijolo vermelho preto àquela hora, o frontão parecendo maior sob o céu sem lua, a aldrava de leão em bronze. Ele entrou pela porta lateral dos criados, que Helle, a criada, deixava destrancada para ele desde a terceira semana, por iniciativa dela. A casa estava em silêncio. O padrinho e a madrinha deviam ter dormido cedo. Kóngen, o gato, estava no patamar da escada, com os olhos amarelos abertos só o bastante para registrar a entrada dele, e os fechou de novo.', 0.4),
 ('f155', 'N', 'Ele subiu para o quarto. Tirou as botas. Tirou a camisa amassada da noite, e vestiu uma limpa, porque a velha cheirava a ponche, e ele não queria levar aquele cheiro para a cama. Sentou à escrivaninha. Acendeu uma vela. E escreveu: Querida mãe. A pena parou ali. Ele olhou o teto. Olhou o tinteiro de porcelana do padrinho, que captava a luz da vela e devolvia um brilho azulado. Escreveu de novo: Querida mãe, há coisas que. E parou. Riscou. Recomeçou: Querida mãe, hoje eu. Riscou de novo.', 0.4),
 ('f156', 'N', 'Pousou a pena. Levantou. Foi até a janela. Lá fora, telhados de ardósia, chaminés e, ao longe, uma faixa de céu sobre o mar, escuro sobre escuro. Ficou ali sem pensar em nada, com a testa encostada no vidro frio.', 0.4),
 ('f157', 'N', 'Em algum lugar, a uns três quilômetros, do outro lado do canal, Aurora estava deitada no quarto de hóspedes da casa de Ingrid, com o vestido amarelo dobrado numa cadeira e o gosto do ponche ainda no fundo da boca. E Erik, provavelmente, já em casa, com a consciência tranquila de quem cumpriu seu papel, sem ideia da fronteira que tinha cruzado sem cruzar. Aurora, provavelmente, não estava dormindo. Provavelmente estava acordada, deitada de costas, de olhos abertos no escuro. Lembrando. Ele esperava que ela estivesse lembrando. Era a única coisa que ele podia esperar.', 0.0),
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
    sf.write(f"{SCR}/cap15-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap15-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap15-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
