import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts6"
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
 ('w01', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo seis: A temporada.', 1.2),
 ('w02', 'N', 'Este capítulo é contado pelos olhos de Aurora Svensson. Filha única que restou de Raj Svensson, um homem de origem indiana que chegou menino a Copenhague e fez fortuna no comércio marítimo, e de Eleonora, filha de um barão dinamarquês. Aurora tinha a pele morena do pai, num país de gente loira, e a cidade sempre a olhara com uma curiosidade educada que nunca chegava a ser acolhida.', 0.4),
 ('w03', 'N', 'Desde a primavera, a temporada se aproximava: os bailes de verão em que as moças de boa família eram apresentadas à sociedade. E naquele ano, Aurora seria uma delas. Uma debutante. Era isso que a mãe tinha anunciado, semanas antes, na sala de costura. E era isso que agora a esperava, pendurado num cabide.', 0.6),
 ('w04', 'N', 'O vestido era verde. Não o verde dos campos que Josh descrevia nas histórias que contava ao pai dela no escritório, e que Aurora absolutamente não ficava ouvindo do corredor quando passava, por acaso, a caminho da sala de costura. Era um verde escuro, profundo, quase negro nas dobras. A modista, Madame Solberg, uma norueguesa que tratava tecidos com a reverência de um padre diante do altar, chamara a cor de verde floresta à meia-noite.', 0.4),
 ('w05', 'N', 'Duas semanas antes, no ateliê, com a boca cheia de alfinetes, ajustando a cintura do vestido no corpo de Aurora, Madame Solberg tinha decretado:', 0.25),
 ('w06', 'SOL', 'Perfeito. Com a sua pele, querida, cores profundas. Nunca pastéis. Pastéis são para loiras. Você precisa de drama.', 0.4),
 ('w07', 'N', 'Eleonora, sentada na poltrona do ateliê, as mãos cruzadas no colo, com a expressão de quem avalia uma aquisição importante, assentiu, e perguntou:', 0.2),
 ('w08', 'EL', 'E o decote?', 0.3),
 ('w09', 'N', 'Madame Solberg recuou dois passos, apertando os olhos como uma pintora diante da tela, e respondeu:', 0.2),
 ('w10', 'SOL', 'Quadrado. Recatado o suficiente para não escandalizar, generoso o suficiente para não ser esquecido. Essa menina tem ombros, senhora Svensson. Ombros e clavículas. Seria um crime escondê-los.', 0.4),
 ('w11', 'N', 'Aurora ficou parada no pedestal de madeira como uma estátua, enquanto duas mulheres discutiam os ombros dela como se ela não estivesse ali. Era o que mais a incomodava em debutar: a redução. O corpo deixava de ser corpo e virava terreno. Decote, cintura, postura. Cada parte medida e apresentada como argumento num julgamento, diante de um júri de senhoras de binóculo e cavalheiros cheios de opinião. Mas o vestido era bonito. Quando ela se olhou no grande espelho de moldura dourada, viu alguém que não reconheceu de imediato. A mesma pele cor de âmbar, os mesmos olhos de mel, os mesmos lábios cheios. Mas o verde escuro contra a pele morena criava um contraste dramático. A cor transformava o que a cidade via como diferente em algo que parecia deliberado. Não um acidente. Uma declaração.', 0.4),
 ('w13', 'N', 'Os ombros à mostra. As clavículas desenhando linhas até o decote quadrado. E no pescoço, Eleonora poria o colar de âmbar que tinha sido da avó de Raj: pedras douradas, translúcidas, que pareciam feitas da mesma matéria dos olhos de Aurora. A mãe olhou o conjunto e disse uma palavra só:', 0.2),
 ('w14', 'EL', 'Serve.', 0.4),
 ('w15', 'N', 'O que era, na linguagem contida de Eleonora, o equivalente a um elogio efusivo. Isso fora duas semanas antes. Agora o vestido estava pendurado na porta do guarda-roupa, e Aurora estava sentada na cama, de camisola, olhando para ele como quem olha um campo de batalha antes do primeiro tiro. O baile dos Frederiksen era no dia seguinte. Aurora não dormiu. Não só de nervoso. Era a consciência de que, no dia seguinte, ela deixaria de ser Aurora Svensson, a filha de Raj, a menina que perdeu o irmão. Seria uma debutante. Uma candidata. Um nome numa lista que pais e mães examinariam com a frieza de quem avalia investimentos. E Aarav não estaria lá.', 0.4),
 ('w17', 'N', 'Era isso que doía. Aarav, o irmão, que partira numa viagem ao Ceilão e nunca voltou, tinha prometido. Dois anos antes, quando ela tinha catorze anos e o baile de debutante parecia tão distante quanto a vida adulta, ele aparecera na porta do quarto dela, com aquele sorriso largo que iluminava qualquer cômodo. E Aurora ainda ouvia a conversa, como um eco:', 0.3),
 ('w18', 'NM', 'Ele dissera: Eu vou estar lá. Vou ser o primeiro a dançar com você. E vou ameaçar de morte qualquer idiota que se aproximar com más intenções. E ela respondera: Aarav, você não sabe ameaçar ninguém. E ele, rindo: Eu posso aprender. Tenho dois anos.', 0.6),
 ('w19', 'N', 'Ele não teve dois anos. Não teve nem um. Aurora virou de lado e abraçou o travesseiro. Não chorou. Já não chorava tão fácil. Talvez as lágrimas tivessem cansado de cair, e agora preferissem ficar onde estavam, pesadas, como nuvens que ameaçam e não se rompem. Pensou no banco do jardim. No banco que Aarav mandara fazer, e que Josh avisara que precisava de verniz. Desde aquela manhã de maio em que ela descera cedo e o encontrara reluzindo, ainda úmido, cheirando a resina, o banco brilhava ao sol. Josh não disse nada. Ela não disse nada. Como se o verniz tivesse se aplicado sozinho durante a noite. Mas Aurora sabia. E Josh sabia que ela sabia. E essa corrente de coisas sabidas e não ditas valia mais do que qualquer conversa.', 0.4),
 ('w21', 'N', 'Fechou os olhos. E pensou, contra toda prudência, em como Josh estaria no dia seguinte. Num baile. De casaco e gravata. Barbeado. Com aqueles olhos verdes. Abriu os olhos. E repreendeu a si mesma, para o teto, entre os dentes:', 0.25),
 ('w22', 'AU', 'Chega. Para com isso.', 0.3),
 ('w23', 'N', 'O teto, como o espelho, não obedecia ordens. O dia do baile amanheceu com aquele céu de junho que a Dinamarca oferece como compensação por seis meses de escuridão: um azul imenso, lavado, tão claro que parecia frágil. A casa entrou em preparação como uma máquina bem lubrificada. Fru Larsen, a cozinheira, serviu o almoço mais cedo. Helle, a criada, passou a tarde subindo e descendo escadas com baldes de água quente para os banhos. E Fru Dahl, a governanta que dava aulas a Aurora, apareceu fora de hora para repassar as regras de etiqueta, embora as duas soubessem que o verdadeiro motivo era ver a pupila vestida.', 0.4),
 ('w25', 'N', 'Eleonora assumiu o cabelo de Aurora. Era um ritual raro de afeto. A mãe, que costumava deixar tudo com Helle, fazia questão de pentear a filha nas ocasiões importantes. E o fazia em silêncio, as mãos leves entre as ondas escuras, com uma familiaridade que não vinha de cabelos parecidos, porque os dela eram lisos e finos, mas de anos de tentativa e erro. De um amor que se dizia em grampos e presilhas, quando as palavras faltavam. Erguendo a massa de cabelos, a mãe perguntou:', 0.2),
 ('w26', 'EL', 'Para cima. Quer ver?', 0.3),
 ('w27', 'N', 'No espelho da penteadeira, com o cabelo preso, o pescoço ficava exposto, longo e moreno, com o colar de âmbar na base, como uma constelação dourada. Aurora pediu:', 0.2),
 ('w28', 'AU', 'Solte algumas mechas. Aqui. Dos lados.', 0.3),
 ('w29', 'N', 'Eleonora soltou duas mechas onduladas sobre as têmporas, emoldurando o rosto como parênteses, e aprovou:', 0.2),
 ('w30', 'EL', 'Melhor.', 0.4),
 ('w31', 'N', 'Olharam-se pelo espelho. A dinamarquesa e a mestiça. A mãe cujos cabelos obedeciam, e a filha cujos cabelos tinham vontade própria. E Eleonora disse, baixo:', 0.2),
 ('w32', 'EL', 'Você está linda.', 0.4),
 ('w33', 'N', 'Aurora abriu a boca para devolver com ironia, como sempre fazia, porque receber elogio a deixava tão confortável quanto sapato apertado. Mas havia algo na voz da mãe. Não era elogio. Era constatação. A voz de uma mulher que olha a filha e percebe, entre orgulho e terror, que ela cresceu. Aurora engoliu a ironia e respondeu, simples:', 0.2),
 ('w34', 'AU', 'Obrigada, mamãe.', 0.4),
 ('w35', 'N', 'Eleonora apertou de leve os ombros da filha. Os olhos dela, no espelho, brilhavam. E então disse, e a voz enfim tremeu, só na última palavra, como a corda de um cravo quando se levanta o dedo da tecla:', 0.25),
 ('w36', 'EL', 'Aarav ia morrer de orgulho.', 0.5),
 ('w37', 'N', 'Aurora segurou a mão da mãe no ombro. Apertou. Não disseram mais nada. A família desceu às sete. O pai estava no hall de entrada, impecável: casaco preto, colete bordado, gravata branca, a pele escura radiante contra a roupa. Segurava uma bengala de que não precisava, porque em Copenhague bengala era acessório, não necessidade. Eleonora, ao lado dele, de azul-pálido e pérolas, parecia uma figura de porcelana que ganhou vida. E Josh estava ao pé da escada.', 0.4),
 ('w39', 'N', 'Aurora o viu antes que ele a visse. Do alto da escadaria, ajeitando a luva esquerda, o que lhe dava desculpa para olhar para baixo. Josh vestia preto. Todo preto. E em vez de sombrio, aquilo o deixava luminoso: contra tanto preto, a pele clara brilhava, o cabelo loiro-ruivo parecia em chamas, e os olhos verdes eram duas esmeraldas acesas. A barba feita. O cabelo penteado para trás, revelando a testa e o maxilar. E as mãos, que dois dias antes estavam arranhadas e sujas de terra e resina do jardim, agora vestiam luvas brancas. Mãos de campo em luvas de salão. Ele olhava o espelho do hall com a mesma expressão que tivera na carruagem, a caminho do chá da senhora Mikkelsen. Vulnerabilidade, disfarçada de compostura. Mas ali.', 0.4),
 ('w41', 'N', 'Então ele ouviu os passos dela na escada, e levantou os olhos. E o rosto dele mudou. Aurora viu acontecer, como quem vê o céu mudar de cor no crepúsculo. Os olhos se abriram um pouco, só o bastante para as pupilas dilatarem. A boca se abriu. Fechou. A mão esquerda, dentro da luva, se fechou ao lado do corpo. Ele engoliu em seco. E não disse nada.', 0.4),
 ('w42', 'N', 'Aquele silêncio, enquanto Aurora descia com o vestido verde, o colar de âmbar, as mechas soltas e os ombros à mostra, era diferente de todos os anteriores. Não era silêncio de quem observa. Era silêncio de quem foi atingido. O pai estendeu a mão para recebê-la ao pé da escada e disse, orgulhoso:', 0.2),
 ('w43', 'RAJ', 'Aurora, você está magnífica.', 0.3),
 ('w44', 'AU', 'Obrigada, papai.', 0.3),
 ('w45', 'N', 'E o pai, inocente, voltou-se para o afilhado:', 0.2),
 ('w46', 'RAJ', 'Josh, não concorda?', 0.3),
 ('w47', 'N', 'Era só um pai orgulhoso pedindo confirmação. Mas Josh precisou de um segundo. Um segundo inteiro, que sob a luz dos candelabros, com Aurora a dois metros dele, cheirando a jasmim e canela, vestida da cor da noite numa floresta, durou uma era geológica. Ele respondeu, atrapalhado:', 0.2),
 ('w48', 'JOSH', 'Sim. Está... sim.', 0.4),
 ('w49', 'N', 'Dylan, o irmão dele, teria gargalhado. Meridiana teria erguido uma sobrancelha. Matias teria corado. E Casandra, a mãe, teria guardado a informação em silêncio para uso futuro. Aurora fez a única coisa que podia fazer sem se comprometer: olhou para as luvas dele, e disse, num tom quase, quase brincalhão:', 0.2),
 ('w50', 'AU', 'Luvas brancas. Madame Solberg aprovaria.', 0.3),
 ('w51', 'N', 'Josh olhou para as próprias mãos como se as visse pela primeira vez, e explicou, meio sem jeito:', 0.2),
 ('w52', 'JOSH', 'São emprestadas. Do seu pai. As minhas não... Eu não tinha luvas de baile.', 0.3),
 ('w53', 'AU', 'Não se tem muitos bailes em Sorô, imagino.', 0.3),
 ('w54', 'JOSH', 'Não. No campo, as festas são ao ar livre. E ninguém usa luvas para dançar em volta de uma fogueira.', 0.4),
 ('w55', 'N', 'A imagem, Josh dançando em volta de uma fogueira, sem casaco, sem luvas, sem regras, surgiu na mente de Aurora com uma nitidez incômoda, e foi imediatamente arquivada entre os pensamentos que ela se recusava a examinar. O pai anunciou que a carruagem estava pronta. E saíram. A residência dos Frederiksen ficava na Kongens Nytorv, a praça mais elegante da cidade, onde o Teatro Real se erguia como um templo grego cercado de mansões. O casarão dos Frederiksen não era o maior, mas era o mais iluminado: cada janela ardia com centenas de velas, e a fachada brilhava como um navio em chamas navegando a noite. A fila de carruagens tomava a praça inteira. Aurora contou onze antes de desistir.', 0.4),
 ('w57', 'N', 'Quando a carruagem parou diante da porta, o estômago dela se contraiu. Não pela multidão, nem pelas luzes. Mas pela certeza de que, ao passar por aquela porta, a cidade inteira a olharia como sempre: admirando sem se aproximar, elogiando sem tocar. Achando-a linda como se acha linda uma pintura de museu: de longe, atrás de uma corda de veludo. Josh desceu por último. E quando pisou nas pedras da praça e se endireitou, alto, loiro, de preto, com aqueles olhos refletindo as velas das janelas, Aurora ouviu. O murmúrio. Um sussurro coletivo que correu a fila de carruagens como o vento corre um campo de trigo. Cabeças virando. Leques se abrindo, não por calor, mas para esconder bocas que cochichavam:', 0.3),
 ('w59', 'CR1', 'Quem é?', 0.2),
 ('w60', 'CR2', 'O afilhado dos Svensson.', 0.2),
 ('w61', 'CR1', 'Do campo?', 0.2),
 ('w62', 'CR2', 'De Sorô, parece.', 0.2),
 ('w63', 'CR3', 'Deus do céu.', 0.5),
 ('w64', 'N', 'Aurora ouviu tudo, com a precisão de quem passou a vida sendo observada. As moças olhavam. As mães das moças olhavam, e depois olhavam as filhas para ver se as filhas olhavam. Josh não percebeu. Ou não demonstrou. Caminhava ao lado do padrinho com uma postura que não era a rigidez ensinada dos cavalheiros da cidade, mas a fluidez natural de quem passa a vida ao ar livre, usando o corpo inteiro. E entraram. O salão dos Frederiksen era uma catedral de luz. Teto alto pintado com cenas mitológicas que ninguém olhava, paredes de seda dourada, três lustres enormes de cristal, cada um com mais velas do que Aurora conseguia contar. Atrás de um biombo de flores, uma orquestra tocava, e os violinos se misturavam ao burburinho e ao tilintar das taças de champanhe.', 0.4),
 ('w66', 'N', 'Aurora reconheceu rostos. A senhora Mikkelsen, aquela do chá, de roxo, com as três filhas em formação: Frederikke de branco, Lovise de azul, Astrid de rosa. Os Holst, com dois filhos que a mãe chamava de possibilidades, ou seja, pretendentes aceitáveis. E os Mortensen, cuja filha, Ingrid, era o mais perto de uma amiga que Aurora tinha. Uma aliança feita da solidão de ser jovem e diferente: Ingrid, por ter nascido com um pé torto que nenhum médico corrigira, e Aurora, por ser Aurora.', 0.4),
 ('w67', 'N', 'A anfitriã, a senhora Frederiksen, cumprimentou Aurora com aquele sorriso que dizia: você é bonita, querida, de um jeito tão exótico. Mas quando Josh se apresentou, curvando-se com correção, a senhora Frederiksen, com seus cinquenta e tantos anos, três filhos casados e fama de anfitriã imperturbável, fez algo que Aurora não esperava. Corou. Como uma debutante. Aurora observou, e arquivou na pasta que estava ficando perigosamente cheia: coisas sobre Josh que eu noto e não deveria notar. O baile começou. Aurora dançou a primeira com o pai, como mandava a tradição: o pai apresentando a filha à sociedade. Ele dançava muito bem, como fazia tudo. Mas Aurora percebeu que a mão dele na sua cintura apertava mais do que o necessário, e que os olhos, quando cruzavam os dela, estavam úmidos. Ele pensava em Aarav. O filho que deveria estar ali. O irmão que deveria ter sido o primeiro a dançar com ela. Aurora apertou a mão do pai. Ele apertou de volta.', 0.4),
 ('w69', 'N', 'A dança terminou, os aplausos vieram, medidos, como tudo em Copenhague. E então começou a fila. Aurora sabia que haveria uma fila. Uma debutante é novidade, e novidade atrai atenção. Mas a fila não era para ela. Era para Josh. Frederikke Mikkelsen foi a primeira, naturalmente. Aos dezenove anos e três temporadas de prática, atravessou o salão com desenvoltura de veterana e surgiu ao lado de Josh. Aurora, a dez metros, leu nos lábios mais do que ouviu: Senhor Russel, que prazer revê-lo, minha mãe ficou encantada com o senhor no chá. Frederikke riu, uma risada treinada que inclinava a cabeça e expunha o pescoço. Um gesto que Fru Dahl um dia tentara ensinar a Aurora, e Aurora respondera que preferia ser decapitada.', 0.4),
 ('w71', 'N', 'Depois vieram outras. Lovise. Uma moça de vestido amarelo que Aurora não conhecia. A filha dos Holst, tão sem graça que o próprio nome se recusava a grudar na memória. Aurora contou sete. Sete moças em meia hora. Sete sorrisos, sete risadas, sete pescoços inclinados. Josh era educado com todas. Igualmente atencioso. Igualmente distante. Mas a educação dele era tão calorosa que podia ser confundida com interesse, por quem não o conhecesse bem. Aurora o conhecia bem.', 0.4),
 ('w72', 'N', 'A percepção a pegou de surpresa, como um degrau no escuro. Eu o conheço bem. Dois meses. As manhãs na cozinha. A tesoura de poda. O livro de botânica. A pérgola. O verniz. O sorriso torto que ela nunca vira de frente, mas adivinhava pela voz. Isso a irritou. Não ele. Ela mesma. O próprio corpo, que se virava na direção dele como uma bússola para o norte: sem decidir, por pura física. Foi quando uma voz ao lado dela disse:', 0.2),
 ('w73', 'ING', 'Você está com cara de quem quer incendiar alguma coisa.', 0.3),
 ('w74', 'N', 'Era Ingrid Mortensen, a amiga, apoiada numa bengala fina de madeira escura que usava com a naturalidade de quem nasceu com ela. Baixa, sardenta, de cabelo ruivo mais curto do que a moda permitia, e olhos cinzentos afiados como lâmina. Aurora sentiu algo afrouxar no peito. Ingrid era a única pessoa na cidade com quem ela podia ser quase honesta. Perguntou:', 0.2),
 ('w75', 'AU', 'Ingrid. Quando você chegou?', 0.3),
 ('w76', 'ING', 'Há dez minutos. Tempo suficiente para contar os lustres, avaliar os canapés, e perceber que tem um rapaz novo no salão, e que você está fingindo não olhar para ele com tanto empenho que é o mesmo que pendurar no pescoço uma placa dizendo: estou olhando para ele.', 0.3),
 ('w77', 'AU', 'Eu não estou olhando para ninguém.', 0.2),
 ('w78', 'ING', 'Então por que você está vermelha?', 0.2),
 ('w79', 'AU', 'Não estou vermelha. Eu não fico vermelha. Eu fico...', 0.2),
 ('w80', 'N', 'Aurora procurou a palavra. Ingrid completou, com um sorriso ao mesmo tempo gentil e impiedoso:', 0.2),
 ('w81', 'ING', 'Cor de cobre. Você fica cor de cobre quando mente. É adorável. E completamente inútil como disfarce. Quem é ele?', 0.3),
 ('w82', 'AU', 'Joshua Russel. Afilhado do meu pai. Mora na nossa casa.', 0.3),
 ('w83', 'N', 'Ingrid repetiu, devagar, como se cada palavra fosse uma revelação separada:', 0.2),
 ('w84', 'ING', 'Mora. Na. Sua. Casa. Do campo, com essa cara, na sua casa. Aurora Svensson, eu quero cada detalhe. Desde o início. E não me poupe de nada.', 0.3),
 ('w85', 'AU', 'Não há nada para contar. Ele é educado. Estuda. Lê muito. Cuida das... Ele é o afilhado do meu pai. É só isso.', 0.3),
 ('w86', 'N', 'Ingrid a estudou com aqueles olhos cinzentos, e cedeu, mas só por enquanto:', 0.2),
 ('w87', 'ING', 'Está bem. Vamos falar de outra coisa. Você já percebeu que nenhum rapaz se aproximou de você?', 0.3),
 ('w88', 'N', 'Ingrid tinha razão. Desde a dança com o pai, nenhum cavalheiro a convidara. Havia olhares. Aurora os sentia como sol nas costas. Mas os olhares ficavam onde estavam, do outro lado da corda de veludo que a cidade pusera em volta dela desde que nasceu. Aurora admitiu, baixo: Eu sei. E Ingrid respondeu, com uma suavidade que não era gentileza, era raiva antiga, de quem também vivia do outro lado de uma corda:', 0.2),
 ('w89', 'ING', 'Não é porque não querem. É porque são covardes. Olhe para você. Você é a moça mais bonita deste salão, e eles sabem. Mas nenhum tem coragem de atravessar a sala, porque teria que explicar aos pais, e os pais aos amigos, por que o filho dançou com a filha de Ráge Svensson. Eu danço com você. Vai ser escandaloso e delicioso.', 0.3),
 ('w90', 'N', 'Aurora quase riu, e lembrou, com carinho, do pé da amiga. Ingrid deu de ombros:', 0.2),
 ('w91', 'ING', 'Meu pé dança perfeitamente, obrigada. O esquerdo é que tem opiniões próprias, mas a gente dá um jeito.', 0.3),
 ('w92', 'N', 'Aurora sentiu algo que não sentia havia tempo. Gratidão de verdade. A de quem está sozinha numa festa e encontra alguém que sabe o que é estar sozinha. Ingrid começou a contar uma fofoca sobre o suposto noivado da filha dos Holst, e por uns vinte minutos Aurora quase conseguiu não olhar para o lado do salão onde Josh estava. Quase. Na terceira vez que os olhos dela escaparam para lá, traidores, encontraram os dele. Josh estava olhando para ela. Não com a educação que dava às sete moças. Mas do outro lado do salão, por cima das cabeças, dos lustres e das taças, com uma expressão que ninguém nunca tinha dirigido a ela. Atenção. Intensidade. O olhar de quem está na margem de um rio e vê, do outro lado, algo que reconhece sem saber nomear. Durou três segundos. Talvez quatro.', 0.4),
 ('w94', 'N', 'Depois alguém falou com ele, Frederikke, provavelmente, e ele desviou. E ela desviou. Mas os quatro segundos ficaram. Como fica a imagem do sol depois que se olha direto para ele: um fantasma de luz, uma queimadura que não dói, mas marca. Ingrid chamou, duas vezes, e Aurora pediu desculpas, não tinha ouvido a pergunta. Ingrid olhou para Aurora. Depois para Josh. Depois para Aurora de novo. E disse, com um sorriso de sabedoria insuportável:', 0.2),
 ('w95', 'ING', 'Nada. Absolutamente nada.', 1.0),
 ('w96', 'N', 'Voltaram para casa às onze. Na carruagem, o pai comentou que o baile fora um sucesso, e Eleonora concordou, econômica como sempre. Ninguém mencionou que Aurora só dançara com o pai. Ninguém mencionou que Josh dançara com três moças: Frederikke, Lovise, e a do vestido amarelo, que Aurora agora sabia se chamar Birgitte Dahl, filha de um diplomata, e que tinha mãos bonitas. Coisa que Aurora preferia não ter notado. No vidro da carruagem, o reflexo de Josh estava lá, como naquela tarde de abril, na volta do chá. Mas desta vez ele não olhava para ela. Olhava para as mãos enluvadas nos joelhos, com uma expressão pensativa que ela não sabia ler. Chegaram em casa. Os pais subiram. Josh fez menção de subir também, mas parou no primeiro degrau, e chamou, baixo:', 0.2),
 ('w98', 'JOSHW', 'Diga em voz baixa e grave, quase num sussurro: Aurora.', 0.4),
 ('w99', 'N', 'Ela parou no hall. Não se virou inteira, seria demais. Virou só a cabeça. O bastante para vê-lo ao pé da escada, de preto, a gravata afrouxada, o cabelo se soltando do penteado, e duas pétalas de alguma flor do salão presas no ombro, sem que ele soubesse. Ele disse, simples, firme, sem a hesitação do começo da noite:', 0.2),
 ('w100', 'JOSH', 'Você estava linda esta noite.', 0.4),
 ('w101', 'N', 'Como se tivesse passado a noite inteira ensaiando a frase, e enfim encontrado a versão certa. E depois acrescentou, mais baixo:', 0.2),
 ('w102', 'JOSHW', 'Diga em voz baixa e grave, quase num sussurro: E eu lamento que nenhum deles tenha tido coragem de te convidar para dançar. Eles são idiotas.', 0.5),
 ('w103', 'N', 'Aurora sentiu o ar sair dos pulmões. Ele tinha visto. Do outro lado do salão, cercado de vestidos e convites, tinha visto que ela passara a noite inteira encostada na parede. E não dissera nada lá, porque dizer lá seria expô-la. Esperou estarem em casa, a sós, onde ela não precisaria se defender. Era, pensou Aurora, com uma clareza que doeu, exatamente o que Aarav teria feito. Ela respondeu apenas:', 0.2),
 ('w104', 'AU', 'Boa noite, Josh.', 0.4),
 ('w105', 'N', 'E subiu sem olhar para trás. Porque se olhasse, se visse os olhos verdes, a gravata afrouxada, as pétalas no ombro, e aquela cara de quem diz a verdade porque não sabe dizer outra coisa, algo dentro dela ia ceder. Algo que vinha segurando havia semanas. Talvez desde o primeiro dia, no alto daquela mesma escada, quando o viu, decidiu odiá-lo, e soube, no mesmo instante, que a decisão era mentira. Entrou no quarto. Fechou a porta. Encostou as costas na madeira. O coração batia como se tivesse dançado a noite inteira. Não dançara. Mas talvez algo mais perigoso que uma dança tivesse acontecido. No corredor, passos leves, subindo a escada, passando pela porta dela, seguindo até o quarto de Josh. Depois, silêncio.', 0.4),
 ('w107', 'N', 'E depois, o cheiro dela, jasmim e canela, e um cheiro novo, que era dele, tabaco, ar frio e sabão, misturados no corredor como duas vozes cantando a mesma nota sem ter combinado. Aurora ficou encostada na porta até o coração se acalmar. Levou tempo.', 0.0),
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
    sf.write(f"{SCR}/cap06-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap06-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap06-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
