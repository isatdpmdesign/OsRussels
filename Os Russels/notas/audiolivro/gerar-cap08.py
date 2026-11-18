import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts8"
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
J = "Diga com voz masculina grave e firme, de um homem de vinte e um anos: "
SEG = [
 ('y01', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo oito: A primeira lição.', 1.2),
 ('y02', 'N', 'Este capítulo volta aos olhos de Aurora. Dias antes, na cozinha, na manhã seguinte ao baile, Josh tinha feito uma proposta absurda: ensinar a ela como os rapazes funcionam. Como deixá-los à vontade para se aproximar, em vez de só olharem de longe. Em segredo, no jardim, depois das aulas com a governanta. E Aurora tinha respondido: está bem.', 0.6),
 ('y03', 'N', 'Ela passou três dias se arrependendo. Não um arrependimento contínuo, o que seria simples demais. Um arrependimento que ia e voltava como maré, aparecendo nas horas mais inconvenientes: no meio de uma conjugação de francês com Fru Dahl, que por ironia era justamente o verbo arrepender-se. Durante o bordado com a mãe. Ao escovar o cabelo à noite, diante do espelho que continuava não obedecendo ordens.', 0.4),
 ('y04', 'N', 'Aulas. De flerte. Com o afilhado do pai. Que morava na mesma casa. Que tinha olhos verdes que ficavam alaranjados no fim da tarde. Que tinha dito que ela era bonita de um jeito que exige pensamento, o que não é coisa que se diga a alguém a quem se quer ensinar a flertar com outros homens. A menos que ele quisesse dizer exatamente aquilo. E era isso que fazia Aurora enfiar o rosto no travesseiro à noite: a suspeita de que ele quisesse.', 0.4),
 ('y05', 'N', 'Mas ela tinha concordado. E Aurora Svensson, neta de um barão dinamarquês e de nobres do Rajastão, não voltava atrás. Não por coragem, embora tivesse. Mas porque voltar atrás exigiria explicar por quê, e explicar exigiria examinar os motivos, e examinar os motivos exigiria abrir portas que ela preferia manter trancadas. E, se possível, soldadas.', 0.5),
 ('y06', 'N', 'Na quarta manhã depois do pacto, uma segunda-feira de junho, com o sol já alto às nove e o jardim banhado naquela luz escandinava que parecia de vidro, Aurora terminou a aula de francês, subiu ao quarto e trocou o vestido formal por um mais simples. Azul escuro, sem rendas, sem broche. Um vestido de ficar em casa, que não queria dizer nada, e que ela escolheu com um cuidado que dizia tudo. E saiu para o jardim.', 0.4),
 ('y07', 'N', 'Josh já estava lá. Sentado no banco de Aarav, o banco que ele mesmo tinha envernizado e que agora brilhava ao sol como âmbar, as pernas esticadas, os braços cruzados, olhando as roseiras. A expressão de quem pensa em alguém e usa a paisagem como desculpa para não olhar para essa pessoa. Aurora parou na porta dos fundos. Respirou. Ajeitou uma mecha que não precisava ser ajeitada. E caminhou até a pérgola.', 0.4),
 ('y08', 'N', 'Josh ouviu os passos dela no cascalho, e se levantou. Ele disse:', 0.2),
 ('y09', 'JOSH', 'Bom dia.', 0.2),
 ('y10', 'AU', 'Bom dia.', 0.4),
 ('y11', 'N', 'Ficaram frente a frente, a um metro e meio, com as roseiras de um lado, as glicínias do outro, e o banco de Aarav entre eles como testemunha. A luz entrava pela pérgola em faixas diagonais de sombra e ouro. E veio o silêncio. Não o da cozinha, que já tinha endereço fixo. Um silêncio novo. De duas pessoas que combinaram de fazer algo que nenhuma das duas sabe como começar. Ela disse:', 0.2),
 ('y12', 'AU', 'Então.', 0.2),
 ('y13', 'JOSH', 'Então.', 0.4),
 ('y14', 'N', 'Mais silêncio. Aurora sentiu o ridículo da situação subir pela espinha como uma corrente de ar frio. Ela, Aurora Svensson, de pé num jardim, esperando que um rapaz do campo lhe ensinasse a seduzir outros rapazes. Se Aarav estivesse vivo, teria rido até chorar. Se Ingrid soubesse, usaria aquilo como chantagem pelo resto da vida. Aurora cruzou os braços, e disse:', 0.2),
 ('y15', 'AU', 'Talvez você pudesse começar me dizendo o que exatamente pretende ensinar. Porque eu concordei com uma coisa que, olhando com a clareza de quem dormiu três noites sobre o assunto, é bastante vaga.', 0.4),
 ('y16', 'N', 'Josh descruzou os braços e inclinou a cabeça, o gesto de quem organiza os pensamentos antes de falar:', 0.2),
 ('y17', 'JOSH', 'Está bem. No baile, eu observei o que as moças faziam quando se aproximavam de alguém. E observei o que você fazia. A diferença é clara.', 0.2),
 ('y18', 'AU', 'A diferença é que eu não faço nada.', 0.2),
 ('y19', 'JOSH', 'Exato. E não é porque você não quer. É porque ninguém te ensinou. A sua mãe te ensinou etiqueta. A Fru Dahl te ensinou francês e dança. O Aarav...', 0.3),
 ('y20', 'N', 'Josh hesitou no nome, testando se podia usá-lo. Aurora não reagiu, o que era permissão. Ele continuou:', 0.2),
 ('y21', 'JOSH', 'O Aarav te ensinou a ler e a pensar. Mas nenhum deles te ensinou o que toda moça que debuta nesta cidade aprende antes dos catorze anos: como se comportar quando está sendo observada por alguém que se interessa.', 0.4),
 ('y22', 'N', 'Aurora pensou em Frederikke Mikkelsen, a moça que tinha cercado Josh no baile. A risada musical. A cabeça inclinada. O toque no braço. E respondeu, seca:', 0.2),
 ('y23', 'AU', 'Eu sei o que elas fazem. Eu observo. Não sou cega.', 0.2),
 ('y24', 'JOSH', 'Eu sei que observa. Mas observar e fazer são coisas diferentes. Você observa como uma estrategista: vê as peças no tabuleiro, entende os movimentos. Mas nunca jogou.', 0.2),
 ('y25', 'AU', 'Porque ninguém me convidou para o jogo.', 0.2),
 ('y26', 'JOSH', 'E porque, quando alguém chega perto do tabuleiro, você espanta.', 0.4),
 ('y27', 'N', 'Aurora abriu a boca para protestar, e parou. Porque ele estava certo. E aquela maldita honestidade dele, que funcionava como um espelho que não distorce, não deixava espaço para fingir. Ela cedeu:', 0.2),
 ('y28', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Está bem. Eu espanto. Como se corrige isso?', 0.4),
 ('y29', 'N', 'Josh deu meio passo à frente. A distância entre eles caiu de um metro e meio para um metro, e Aurora sentiu a diferença na pele. Ele anunciou:', 0.2),
 ('y30', 'JOSH', 'Primeiro: o sorriso.', 0.2),
 ('y31', 'AU', 'Mas eu sorrio.', 0.2),
 ('y32', 'JOSH', 'Você faz uma coisa com a boca que se parece com um sorriso, que tecnicamente é um sorriso, e que faz a pessoa do outro lado sentir que está sendo recebida na porta de uma casa e expulsa pela janela ao mesmo tempo.', 0.4),
 ('y33', 'N', 'Aurora piscou, e admitiu:', 0.2),
 ('y34', 'AU', 'Isso foi... surpreendentemente preciso.', 0.3),
 ('y35', 'JOSH', 'Eu recebi esse sorriso no primeiro dia. Pode acreditar, eu conheço bem.', 0.3),
 ('y36', 'N', 'Ele deu mais meio passo. Agora a distância era menos de um metro. Aurora sentia o cheiro dele. Não o cheiro formal, de sabão e casaco, mas o de quem esteve ao sol, um cheiro de ar livre e pele quente que não combinava com a cidade, e que por isso mesmo era inconfundivelmente dele. Ele explicou:', 0.2),
 ('y37', 'JOSH', 'Um sorriso de verdade não é simétrico. Não é perfeito. Começa num canto da boca e puxa o outro. E chega aos olhos. Se não chegar aos olhos, não é sorriso. É máscara.', 0.3),
 ('y38', 'AU', 'E como se faz um sorriso chegar aos olhos?', 0.3),
 ('y39', 'JOSH', 'Pensando em alguma coisa que te faz feliz. Não uma coisa grande. Uma coisa pequena. Um chá quente no dia certo. O som de alguma coisa que te faz rir. A primeira rosa que abre na primavera.', 0.4),
 ('y40', 'N', 'Aurora olhou para ele. O sol da manhã atravessava a pérgola e tocava o rosto dele em faixas de luz, e os olhos, aqueles olhos verdes cujo mapa de cores ela poderia desenhar de olhos fechados, tinham veios de ouro que apareciam quando a luz batia direto. E Aurora pensou, sem querer, sem decidir: Ele tem sol nos olhos. E sorriu.', 0.4),
 ('y41', 'N', 'Não o sorriso de porcelana. Um sorriso involuntário, nascido do pensamento e não da vontade, que começou no canto esquerdo da boca, sempre o esquerdo, puxou o direito, subiu pelo rosto, e chegou aos olhos. E transformou o rosto de Aurora em algo que Josh nunca tinha visto de frente, àquela distância, naquela luz. Josh parou de falar. Dois segundos. Três. O professor tinha perdido o fio da lição, porque a aluna acabara de fazer exatamente o que ele pediu, e o resultado foi mais eficaz que qualquer técnica. Aurora perguntou, com uma faísca nova na voz, provocante:', 0.25),
 ('y42', 'AU', 'Diga num tom baixo, provocante e sensual, em português do Brasil: Assim?', 0.4),
 ('y43', 'N', 'Josh piscou. Recuperou-se. Mas a recuperação foi visível, como alguém que tropeça e finge que não tropeçou, traído pelo rubor que sobe pelo pescoço. Josh Russel, que não corava, que enfrentava salões e senhoras e xícaras de porcelana com compostura, estava corando. Ele pigarreou, desconcertado. E respondeu com a voz embargada, rouca, de quem ainda não se recuperou do que acabou de ver:', 0.2),
 ('y44', 'JOSH', 'Diga com a voz baixa, rouca e embargada, de um homem desconcertado e atraído, limpando a garganta antes de falar: Hum... Sim. Assim. Exatamente assim.', 0.4),
 ('y45', 'N', 'Aurora guardou aquilo no arquivo onde guardava tudo sobre Josh. Um arquivo que já era bem maior do que ela gostaria de admitir, e que crescia numa velocidade alarmante. Ela pediu:', 0.2),
 ('y46', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: O que mais?', 0.3),
 ('y47', 'N', 'Josh respirou. A postura se firmou. O professor voltou:', 0.2),
 ('y48', 'JOSH', 'Segundo: o olhar. Quando um homem fala com você, ele precisa sentir que está sendo ouvido. Não só com os ouvidos. Com os olhos. Mas não um olhar fixo, isso assusta. O olhar tem que ter movimento. Começa nos olhos da pessoa. Desce, não muito, só até a boca. E volta. A descida dura um instante. Menos de um segundo. Mas o instante basta.', 0.3),
 ('y49', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Descer até a boca.', 0.2),
 ('y50', 'JOSH', 'Da pessoa.', 0.2),
 ('y51', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Da pessoa. Certo. E isso comunica o quê?', 0.2),
 ('y52', 'JOSH', 'Que você está prestando atenção nele de um jeito que não é só educado. Que você está vendo ele. Não o casaco, não a família, não o título. Ele.', 0.4),
 ('y53', 'N', 'A teoria fazia sentido. Aurora tinha visto Frederikke fazer algo parecido, sem entender o mecanismo. Mas teoria era uma coisa. Prática era outra. Ela hesitou, e perguntou:', 0.2),
 ('y54', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Posso... Posso tentar? Com você?', 0.4),
 ('y55', 'N', 'Era uma pergunta lógica, prática. Nada de inadequado nela. Exceto que Aurora estava pedindo permissão para olhar para Josh de propósito, dos olhos à boca e de volta. E os dois sabiam que essa permissão transformava algo que ela já fazia escondido em algo que aconteceria à luz do dia, a menos de um metro, entre as roseiras de um irmão perdido e as glicínias que Josh tinha salvado com as próprias mãos. Josh demorou a responder. Engoliu em seco. E disse, a voz baixa e carregada:', 0.2),
 ('y56', 'JOSH', 'Diga devagar, com a voz baixa e carregada de tensão, depois de engolir em seco: Claro.', 0.4),
 ('y57', 'N', 'Aurora endireitou a postura, ergueu o queixo, e olhou nos olhos dele. De perto, os olhos de Josh eram mais complexos do que ela pensava. O verde tinha camadas: escuro na borda, como musgo em pedra molhada, clareando para um verde quase elétrico, e ao redor da pupila explodindo em veios alaranjados, como fogo visto através de folhas. Era isso que fazia os olhos dele parecerem mudar de cor.', 0.4),
 ('y58', 'N', 'Aurora desceu o olhar. Meio centímetro. Um centímetro. Até a boca. E a boca de Josh era, ela não achou palavra melhor, desconcertante. O lábio de cima mais fino, com um arco bem desenhado no centro, como o das estátuas gregas nos livros do pai. O de baixo mais cheio, um pouco assimétrico no canto direito, o canto do sorriso torto. A barba, feita naquela manhã, deixava uma sombra dourada em volta dos lábios que era, e Aurora dispensou a palavra antes que se formasse, e a palavra voltou mesmo assim, convidativa.', 0.4),
 ('y59', 'N', 'Subiu o olhar. Voltou aos olhos. Tudo durou menos de dois segundos. Josh não se mexeu. Não piscou. Ficou imóvel, como quem é examinado e sabe que qualquer movimento altera o resultado. Mas os olhos dele falaram. Escureceram. As pupilas dilataram, como quando se entra numa sala escura. Exceto que não estava escuro. Estava claro. Era junho. Era sol. As pupilas de Josh dilataram porque ele estava olhando para Aurora.', 0.4),
 ('y60', 'N', 'E Aurora percebeu, com um choque que atravessou o corpo da nuca aos pés, que aquilo não era técnica. Nunca seria técnica. Olhar para Josh daquele jeito não era praticar flerte com um professor. Era olhar para alguém que se deseja olhar. Ela recuou meio passo. O ar entre os dois, que por dois segundos parecera espesso, quase líquido, voltou a ser só ar. E ela perguntou, com a voz mais controlada do que se sentia, porque controle era herança de família:', 0.2),
 ('y61', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Assim?', 0.3),
 ('y62', 'N', 'Josh confirmou, com a voz também controlada. Mas o pescoço estava vermelho:', 0.2),
 ('y63', 'JOSH', 'Assim. Perfeito.', 0.3),
 ('y64', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Não foi difícil.', 0.4),
 ('y65', 'N', 'Mentira. Tinha sido a coisa mais fácil e mais difícil que ela já fizera. Fácil porque olhar para Josh era como respirar: o corpo sabia fazer sem instrução. Difícil porque cada segundo de olhar era um segundo de exposição, e Aurora detestava exposição como gato detesta água. Josh retomou, com a voz mais firme:', 0.2),
 ('y66', 'JOSH', 'Terceiro: o toque.', 0.3),
 ('y67', 'N', 'Aurora sentiu o estômago contrair, e repetiu, num fio de voz:', 0.2),
 ('y68', 'AU', 'Diga em tom normal e pensativo, como quem pensa em voz alta, sem sussurrar, em português do Brasil: O toque.', 0.2),
 ('y69', 'JOSH', 'Não é o que parece. É o toque social. Quando alguém diz alguma coisa engraçada, você encosta a mão no braço da pessoa. Não segura. Não aperta. Encosta. Um segundo, dois no máximo. E tira. É um gesto pequeno, mas comunica proximidade. Conforto. Permissão.', 0.2),
 ('y70', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Permissão pra quê?', 0.2),
 ('y71', 'JOSH', 'Pra chegar mais perto.', 0.4),
 ('y72', 'N', 'Aurora olhou o braço dele. O braço que as sete moças do baile tinham tocado. O braço que ela nunca tinha tocado, nem por acidente, nem de propósito, em dois meses na mesma casa. E disse:', 0.2),
 ('y73', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Isso não é uma coisa que eu consiga praticar com você.', 0.2),
 ('y74', 'JOSH', 'Por que não?', 0.4),
 ('y75', 'N', 'E Aurora pensou, sem dizer: Porque tocar você não seria exercício. Porque eu sei como as luvas brancas ficam nas suas mãos. Porque eu vi os seus antebraços na cozinha naquela manhã de abril, e a imagem não saiu. Porque eu sei que as suas mãos seguram duas toras de carvalho ao mesmo tempo. Porque se eu tocar o seu braço, Josh Russel, eu não vou tirar a mão em dois segundos. E nós dois sabemos disso. Mas o que ela disse em voz alta, mentirosa bem melhor do que gostaria, foi:', 0.25),
 ('y76', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Porque não é necessário. Eu entendi o conceito. Posso aplicar na situação real.', 0.4),
 ('y77', 'N', 'Josh a estudou um momento. Aurora sustentou o olhar com a calma de quem acabou de mentir e pretende levar a mentira até o túmulo. Ele cedeu:', 0.2),
 ('y78', 'JOSH', 'Está bem. A última por hoje.', 0.2),
 ('y79', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: E tem mais?', 0.2),
 ('y80', 'JOSH', 'Muito mais. Mas hoje, uma coisa de cada vez.', 0.3),
 ('y81', 'N', 'Josh recuou um passo. O ar ficou mais leve, e Aurora quase sentiu falta do peso. Ele continuou:', 0.2),
 ('y82', 'JOSH', 'A quarta é a mais importante. E é a que você já faz naturalmente. Só precisa fazer de propósito.', 0.2),
 ('y83', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: E qual é?', 0.2),
 ('y84', 'JOSH', 'Perguntar. Quando um homem fala, a maioria das moças escuta esperando a vez de falar. Ou finge que escuta, enquanto prepara a próxima coisa encantadora pra dizer. Mas quando alguém te faz uma pergunta de verdade, sobre algo que te importa, uma pergunta que mostra que a pessoa ouviu, isso é mais poderoso que qualquer sorriso, olhar ou toque. Porque o que todo mundo quer, homem, mulher, rei ou mendigo, é ser visto. E uma boa pergunta é a prova de que alguém te viu.', 0.5),
 ('y85', 'N', 'Aurora ficou em silêncio. Não processando a técnica, que era quase ofensivamente simples. Processando o fato de que Josh acabava de descrever, sem saber, exatamente o que ele fazia com ela. Toda manhã. Na cozinha, no jardim, nos corredores. Josh perguntava. Não as perguntas vazias da sociedade. Perguntas de verdade. É sempre assim? O que você quer? Por quê? Perguntas que a faziam se sentir vista. E ela disse, antes de conseguir se conter:', 0.2),
 ('y86', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Você faz isso.', 0.2),
 ('y87', 'JOSH', 'Eu faço o quê?', 0.2),
 ('y88', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Pergunta. Você sempre pergunta. Coisas de verdade. Não as perguntas que as pessoas fazem pra parecer educadas. Você pergunta porque quer saber a resposta.', 0.4),
 ('y89', 'N', 'Josh ficou parado. A confusão deu lugar a algo mais macio, parecido com vulnerabilidade, como se ela tivesse aberto, sem querer, uma porta que ele não esperava. Ele disse, devagar:', 0.2),
 ('y90', 'JOSH', 'Eu cresci numa família de cinco filhos e uma mãe viúva. Quando tem tanta gente em volta, é fácil desaparecer. O único jeito de existir é prestando atenção nos outros. Se você presta atenção, as pessoas te contam quem são. E se você sabe quem elas são, pode cuidar delas sem que percebam.', 0.4),
 ('y91', 'N', 'Cuidar delas sem que percebam. As roseiras. O verniz. A pérgola. O livro de botânica. O eles são idiotas, dito no hall quando ninguém mais podia ouvir. Cada gesto pequeno, invisível, não para ser agradecido, mas porque cuidar era a língua nativa de Josh Russel, como respirar é a língua dos pulmões. Aurora sentiu algo se mover dentro do peito. Algo lento, mas irreversível, como o chão que se move devagar, ano após ano, até mudar a forma dos continentes.', 0.4),
 ('y92', 'N', 'Ela disse o nome dele, sem saber o que viria depois:', 0.2),
 ('y93', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Josh...', 0.2),
 ('y94', 'JOSH', 'Sim?', 0.2),
 ('y95', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Obrigada. Por estar fazendo isso.', 0.4),
 ('y96', 'N', 'Josh olhou para ela. E o sorriso torto, o que ela nunca tinha visto de frente, o que o irmão dele chamava de cara de idiota, apareceu. Pela primeira vez. De frente. A menos de um metro. Era pior do que Aurora imaginava. Muito pior. Porque não era bonito. Bonito era pouco. Era devastador, como um amanhecer é devastador: não porque agride, mas porque revela.', 0.4),
 ('y97', 'N', 'Revelava os dentes, levemente imperfeitos, o canino esquerdo um milímetro mais alto. Revelava covinhas nas bochechas. Revelava os olhos, que se estreitavam e ganhavam linhas nos cantos: linhas de riso, linhas de sol, de quem passou anos ao ar livre franzindo os olhos contra a luz. Aurora absorveu o sorriso inteiro como quem absorve um golpe: calada, firme, sem mostrar o estrago. Recuou um passo, e perguntou:', 0.2),
 ('y98', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Amanhã? Na mesma hora?', 0.2),
 ('y99', 'JOSH', 'Sim. Na mesma hora.', 0.2),
 ('y100', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Eu vou... repassar o que aprendi.', 0.2),
 ('y101', 'JOSH', 'Sorriso, olhar, toque, pergunta.', 0.2),
 ('y102', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Sorriso, olhar, toque, pergunta.', 0.4),
 ('y103', 'N', 'Ela repetiu como quem decora uma fórmula. Como se fosse uma fórmula. Como se o sorriso não tivesse sido de verdade, e o olhar até a boca dele não tivesse sido de verdade, e a recusa de tocar o braço dele não tivesse sido a coisa mais honesta que ela dissera a manhã inteira. Ela já estava na porta dos fundos quando ele chamou:', 0.2),
 ('y104', 'JOSH', 'Diga com sotaque brasileiro, chamando por ela com calma: Aurôra?', 0.4),
 ('y105', 'N', 'Ela parou, meio virada. O bastante para vê-lo no jardim, entre as roseiras e as glicínias, com o sol de junho transformando o cabelo loiro-ruivo numa coroa de fogo suave. Ele disse:', 0.2),
 ('y106', 'JOSH', 'Quando praticar o sorriso, não pensa nas técnicas. Pensa na coisa que te fez sorrir de verdade hoje. É isso que vai funcionar.', 0.4),
 ('y107', 'N', 'Aurora não respondeu. Porque responder seria dizer em que tinha pensado quando sorriu. E ela não podia dizer: pensei que você tem sol nos olhos. Não podia, não devia, e não diria. Disse apenas:', 0.2),
 ('y108', 'AU', 'Diga em português do Brasil, com sotaque brasileiro: Até amanhã.', 0.6),
 ('y109', 'N', 'Entrou na casa. Subiu a escada. Entrou no quarto. Fechou a porta. E encostou as costas na madeira, como na noite do baile. E desta vez não tentou acalmar o coração. Deixou bater rápido, bater forte, como se quisesse sair do peito, descer até o jardim, e sentar no banco envernizado ao lado de um rapaz do campo com sol nos olhos e um sorriso torto devastador. Um rapaz que acabara de ensiná-la a flertar sem ter a menor ideia de que a única pessoa com quem ela queria usar o que aprendera era ele.', 0.4),
 ('y110', 'N', 'Ou talvez ele tivesse ideia. Talvez, e esse era o pensamento mais perigoso de todos, mais que o sorriso, mais que o olhar, mais que a boca dele a menos de um metro, Josh Russel soubesse exatamente o que estava fazendo. E talvez ela, Aurora Svensson, soubesse exatamente o que estava fazendo ao deixar.', 0.0),
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
    sf.write(f"{SCR}/cap08-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap08-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap08-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
