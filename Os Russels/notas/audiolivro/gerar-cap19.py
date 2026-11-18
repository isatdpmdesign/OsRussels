import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts19"
SCR = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
# NOVAS vozes: Josh (Achird, jovem/caloroso), Dylan (Zubenelgenubi, casual/seco) — a AUDITAR com a autora
V = {"N": "Vindemiatrix", "AU": "Leda", "EL": "Gacrux", "RAJ": "Algieba",
     "JOSH": "Zubenelgenubi", "DYLAN": "Achird",
     "HELLE": "Achernar", "LARSEN": "Kore",
     "MIK": "Sulafat", "FRED": "Autonoe", "LOV": "Laomedeia", "CAS": "Pulcherrima", "SOL": "Despina", "ING": "Aoede", "CR1": "Erinome", "CR2": "Callirrhoe", "CR3": "Zephyr", "JOSHW": "Zubenelgenubi", "NM": "Vindemiatrix", "ERIK": "Iapetus", "HJ": "Puck", "LYK": "Zephyr", "VIB": "Laomedeia", "LUN": "Sulafat"}
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
ELP = "Diga com voz de senhora madura, grave e contida: "
VB = "Diga em português do Brasil, com sotaque brasileiro, com alegria espontânea: "
P1 = "Diga com voz de homem jovem, grave, baixa e aveludada, calma, sem animação: "
INT = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/ref/josh_aurora_intenso.wav"
SEG = [
 ('m001', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo dezenove: A madrugada.', 1.2),
 ('m002', 'N', 'Este capítulo continua nos olhos de Aurora, na mesma noite. No baile dos Lundgren, Josh dançou com a prima dela, Vibêke, e Aurora passou a noite na cadeira, ao lado da mãe. Perto da janela, ele perguntou se alguma coisa a incomodava, e ela disse que não. Em casa, sem conseguir dormir, Aurora desceu sozinha à sala de estar, depois da meia-noite, com um livro de poesia que tinha sido do irmão morto, Arav.', 0.6),
 ('m003', 'N', 'A primeira página do volume de Ólenchlêguer tinha uma mancha de tinta no canto inferior direito. Aurora viu a mancha antes de ler qualquer palavra. Era tinta da pena de Arav, desses borrões que a pena soltava quando a mão de quem escrevia atrasava o gesto. Estava ali havia anos. Aurora não tinha lembrança do dia em que aquilo aconteceu, mas o livro lembrava por ela. O livro guardava o que ela não podia.', 0.3),
 ('m004', 'N', 'Sentou-se mais reta no chão. Apertou o xale nos ombros. Olhou para a vela na mesa lateral. A vela durava no máximo mais quarenta minutos. Aurora sabia, porque conhecia velas, e a chama daquela tinha um ritmo levemente nervoso, de queima rápida. Quarenta minutos. Era o que ela tinha de sala de estar sozinha, antes que a escuridão a obrigasse a voltar para a cama.', 0.3),
 ('m005', 'N', 'Estava no chão, encostada na poltrona. Naquela noite, desprezara o conforto. Queria ficar ali, atrás da poltrona mais alta do que o ombro dela, como se o móvel fosse um casulo que a protegia do resto do mundo. O chão era duro, mas firme. O xale segurava o frio da noite de agosto, que na Brédigueide, de madrugada, virava qualquer mês mais frio. Aurora não tinha pressa de subir. Quanto mais tempo ali, menos tempo revirando na cama, com a frase de Josh se repetindo na cabeça, e o sobretudo dele ainda morno na lembrança da manga do vestido.', 0.4),
 ('m006', 'N', 'Abriu o livro. Página trinta e sete, onde estava a fita azul. Aurora tinha posto a fita ali sem ler. Talvez Arav tivesse parado naquela página. Talvez fosse por acaso. Não importava agora. Aurora começou a ler. A primeira linha era um verso em dinamarquês antigo, do tipo que Arav lia em voz alta no jardim, com gestos teatrais que faziam a mãe levantar uma sobrancelha e rir. Aurora reconheceu o ritmo antes mesmo de entender as palavras. E a frase soou na cabeça dela com a voz do irmão:', 0.4),
 ('m007', 'NM', 'O que é viver, senão arder.', 0.6),
 ('m008', 'N', 'Na lembrança, a voz de Arav estava mais rouca do que ela lembrava, talvez porque a memória já estivesse perdendo um pouco do timbre dele e improvisando o resto. Aurora segurou a página com mais firmeza. Foi nesse momento que ouviu o degrau ranger.', 1.0),
 ('m009', 'N', 'O décimo segundo degrau era o que rangia. Tinha sido trocado numa reforma da escada, três anos antes, e ficara meio milímetro mais largo que o original. Aurora aprendera a evitá-lo quando descia de noite para pegar água na cozinha. Quem não conhecia a escada não evitava. Vibêke não conhecia a escada. Josh também não conhecia tão bem assim. Mas Aurora sabia, antes de virar a cabeça para a porta, que era ele quem descia. Sabia pelo peso do passo, pelo intervalo entre os passos, e pelo fato de que naquela casa, depois da meia-noite, só duas pessoas tinham insônia suficiente para descer descalças: ela e ele. E ela já estava ali.', 0.4),
 ('m010', 'N', 'A vela tremeu quando ele entrou na sala. Estava de camisa, a mesma de gola alta do baile, agora aberta nos dois primeiros botões, amassada de quem tinha deitado mas não dormido. Calças dobradas na canela. Pés descalços. O cabelo desarrumado de um lado e achatado do outro, de quem vira na cama a cada vinte minutos durante duas horas. Na mão, uma vela apagada. Pelo jeito, tinha desistido de acendê-la quando viu a luz vinda da sala. Os olhos dele encontraram os olhos dela. Ele disse, já se virando para sair:', 0.2),
 ('m011', 'JOSH', P1+'Desculpe... Eu não queria...', 0.2),
 ('m012', 'AU', AI+'Tudo bem. Você não precisa ir.', 0.3),
 ('m013', 'N', 'Por meio segundo, Aurora pensou em fechar o livro. Não fechou. Deixou que ele visse o livro aberto, o xale, a vela, o chão. Deixou que ele entendesse, sem que ela precisasse dizer, que ela não estava ali por acaso. Josh entrou. Pousou a vela apagada na mesa lateral, ao lado da que Aurora tinha acendido. Não tentou acender a dele na chama dela, embora pudesse. Olhou para o livro no colo de Aurora e disse, como quem reconhece um conhecido na rua sem saber se deve cumprimentar:', 0.2),
 ('m014', 'JOSH', P1+'Isso é Ólenchlêguer.', 0.2),
 ('m015', 'AU', AI+'Era do Arav.', 0.2),
 ('m016', 'JOSH', P1+'Eu sei. Eu sei que era.', 0.2),
 ('m017', 'AU', AI+'Como é que você sabe?', 0.2),
 ('m018', 'N', 'Josh ficou em silêncio por um segundo. Aurora viu o canto da boca dele subir, só um pouco, antes de responder, com a cautela de quem oferece uma informação que pode magoar.', 0.2),
 ('m019', 'JOSH', P1+'O Arav lia Ólenchlêguer no jardim. O seu pai me contou, uma noite, no começo. Disse que era o poeta preferido do filho. Me emprestou um volume do escritório, pra eu ler. Eu gostei. Quando devolvi, ele me disse que outro volume do mesmo poeta tinha sumido da estante duas semanas depois que a notícia do navio chegou. Não disse quem ele achava que tinha levado.', 0.3),
 ('m020', 'N', 'Josh olhou para o livro no colo dela, e completou:', 0.2),
 ('m021', 'JOSH', P1+'Acho que esse é o que sumiu.', 0.4),
 ('m022', 'N', 'Aurora não respondeu logo. A vela tremeu uma vez. Ela passou o polegar pela mancha de tinta na primeira página, devagar, sem pensar. E então disse, mudando de assunto sem aviso:', 0.2),
 ('m023', 'AU', AI+'Você me viu chorar uma vez. Foi pouco depois de você chegar. Eu desci à biblioteca naquela noite. Eu não sabia que tinha alguém ali.', 0.2),
 ('m024', 'JOSH', P1+'Eu sei. Eu lembro.', 0.2),
 ('m025', 'AU', AI+'Você não olhou pra mim.', 0.2),
 ('m026', 'JOSH', P1+'Não me cabia olhar.', 0.2),
 ('m027', 'AU', AI+'Você apontou um livro com o queixo, sem virar o corpo. O tratado de botânica. Terceira prateleira, segunda fileira, capítulo nove.', 0.2),
 ('m028', 'JOSH', P1+'Eu lembro do número.', 0.2),
 ('m029', 'AU', AI+'Eu peguei o livro. Depois que você subiu.', 0.2),
 ('m030', 'JOSH', P1+'Eu ouvi. Fiquei no quarto, com a porta entreaberta, esperando ouvir.', 0.2),
 ('m031', 'AU', AI+'E por quê?', 0.2),
 ('m032', 'N', 'Josh começou e parou. A boca se mexeu antes de a voz sair.', 0.2),
 ('m033', 'JOSH', P1+'Porque me importava saber se você pegaria o livro que eu indiquei.', 0.2),
 ('m034', 'AU', AI+'É? E por que importava eu me interessar pelo livro que você indicou?', 0.2),
 ('m035', 'JOSH', P1+'Eu gosto de cuidar das pessoas, Aurôra. Sempre cuidei. E te ver chorando me deu vontade de te ajudar. Mas você quase não me olhava naquela época. O livro foi o jeito que eu achei.', 0.2),
 ('m036', 'N', 'Ele fez uma pausa, e continuou:', 0.2),
 ('m037', 'JOSH', P1+'Se você pegasse, significaria que eu, de algum jeito, era importante pra você.', 0.3),
 ('m038', 'N', 'Aurora não disse nada. Esperou. Depois perguntou:', 0.2),
 ('m039', 'AU', AI+'E se eu não pegasse?', 0.2),
 ('m040', 'JOSH', P1+'Significaria que você não me notava.', 0.2),
 ('m041', 'AU', AI+'E você não quis saber por que eu chorava?', 0.2),
 ('m042', 'JOSH', P1+'Claro que eu queria saber. Mas não me cabia perguntar. Mesmo que eu já desconfiasse.', 0.3),
 ('m043', 'N', 'Aurora pousou a mão sobre a página trinta e sete, com cuidado, como quem fecha uma janela sem querer fazer barulho. Não fechou o livro. Só pousou.', 0.2),
 ('m044', 'AU', AI+'Mas talvez, se você perguntasse, eu teria contado.', 0.2),
 ('m045', 'N', 'Ele deu uma risadinha curta:', 0.2),
 ('m046', 'JOSH', 'Ou teria me dito que não era da minha conta. Quer dizer, você não era das mais receptivas naquela época.', 0.2),
 ('m047', 'N', 'Aurora riu, de verdade.', 0.2),
 ('m048', 'AU', BR+'É verdade. Mas você nunca entra em assunto que acha que não te cabe, não é?', 0.2),
 ('m049', 'JOSH', P1+'É. Não entro.', 0.2),
 ('m050', 'AU', AI+'Você não pergunta o que não te cabe. Mas eu pergunto. Por que você desceu hoje?', 0.3),
 ('m051', 'N', 'Ele a encarou por um segundo. Não respondeu de imediato. Aurora viu o queixo dele se contrair e relaxar: o gesto pequeno que ele fazia quando estava engolindo uma frase de volta, porque tinha decidido, naquele meio segundo, que ainda não era a hora.', 0.3),
 ('m052', 'N', 'Josh sentou no chão também. Não de frente para ela. Na diagonal, com a poltrona entre os dois, mas só meio entre: o ângulo deixava as pernas dele à mostra, e o caminho dos olhos dela livre até o rosto dele, se ela quisesse subir. As pernas dobradas, os antebraços apoiados nos joelhos, a mão direita aberta no ar, como quem espera autorização para fazer alguma coisa que ainda não decidiu o que vai ser. Aurora disse:', 0.2),
 ('m053', 'AU', AI+'Você não conseguiu dormir.', 0.2),
 ('m054', 'JOSH', P1+'Não. Não consegui.', 0.2),
 ('m055', 'AU', AI+'E por quê, Josh?', 0.2),
 ('m056', 'JOSH', P1+'Você sabe por quê.', 0.2),
 ('m057', 'AU', AI+'Eu quero te ouvir dizer.', 0.3),
 ('m058', 'N', 'Aurora não tinha pensado na frase antes de dizer. Saiu como se estivesse pronta havia semanas, esperando o gatilho. Josh olhou para o chão entre os dois. O assoalho era de madeira clara, com uma emenda na altura da poltrona que sempre tinha incomodado a mãe dela e que ninguém nunca tinha consertado direito. Josh ficou olhando para a emenda como se fosse a coisa mais importante do cômodo. Quando falou, a voz dele saiu mais grave do que até ali:', 0.2),
 ('m059', 'JOSH', P1+'Aurôra, eu vi você na cadeira a noite inteira.', 0.2),
 ('m060', 'AU', AI+'Você estava dançando.', 0.2),
 ('m061', 'JOSH', P1+'Estava. Estava dançando e olhando.', 0.2),
 ('m062', 'AU', AI+'Eu não vi você olhando.', 0.2),
 ('m063', 'JOSH', P1+'Eu sei. Você escolheu não ver.', 0.3),
 ('m064', 'N', 'Aurora abriu a boca para responder. Fechou. Aquilo era verdade, e a verdade tinha um peso que tornava qualquer resposta imediata uma traição. Deixou a frase dele ocupar o cômodo por uns dois segundos. Depois falou, e notou, enquanto falava, que a voz não tremia. Estava firme. Não a firmeza confortável da Aurora de porcelana, mas a firmeza desconfortável de quem diz a verdade pela primeira vez, sem ensaiar:', 0.2),
 ('m065', 'AU', AI+'Eu dancei com o Érik porque a mamãe queria que eu dançasse com alguém. Dancei com um primo dos Lundgren cujo nome eu não consegui guardar nem enquanto ele me dizia. Olhei pra pista uma vez por dança, e voltei o rosto pro ombro de quem dançava comigo. E quando a carruagem chegou em casa, eu fui pro quarto, deitei, e a minha cabeça não parou de pensar. Aí eu desci. É por isso que eu estou aqui no chão, com um livro do meu irmão morto, a essa hora da noite. E você, Josh? Por que você está?', 0.3),
 ('m066', 'N', 'Josh ficou um tempo sem responder. Quando respondeu, foi com a frase que Aurora não esperava.', 0.2),
 ('m067', 'JOSH', P1+'Você contornou, mas não disse a verdade. A verdade é que você está aqui porque a sua cabeça não parou de pensar. Pensar em quê?', 0.2),
 ('m068', 'N', 'Aurora soltou, num ímpeto irritado:', 0.2),
 ('m069', 'AU', BR+'Em você dançando a noite toda com a Vibêke, e não comigo!', 0.4),
 ('m070', 'N', 'Josh não se moveu. A resposta tinha sido dita. E só Deus sabia o quanto ele teria preferido passar aquela noite dançando com Aurora, sentindo o corpo dela perto do seu, a mão na cintura dela, conduzindo-a pelo salão. Só Deus sabia o quanto ele tinha desejado aquilo, e não tinha podido. Ele se endireitou para levantar, e disse:', 0.2),
 ('m071', 'JOSH', P1+'É melhor eu subir.', 0.2),
 ('m072', 'N', 'Aurora soltou um riso curto, sarcástico.', 0.2),
 ('m073', 'AU', AI+'Por quê? Você realmente não gosta da minha companhia, não é? Naquela noite no celeiro, em que eu...', 0.2),
 ('m074', 'N', 'Aurora parou. Não soube como dizer que tinha pedido um beijo. E terminou:', 0.2),
 ('m075', 'AU', AI+'Enfim. Você também fugiu.', 0.2),
 ('m076', 'JOSH', P1+'Eu não fugi. O Érik chegou.', 0.2),
 ('m077', 'AU', AI+'Mas você fugiria, não é?', 0.3),
 ('m078', 'N', 'Josh desistiu de levantar. Virou o corpo na direção dela e a encarou. Via nos olhos dela a dúvida e o medo do que ele ia responder, atravessando a pupila cor de mel.', 0.2),
 ('m079', 'JOSH', P1+'Sim, eu fugiria. Sempre vou fugir. Agora mesmo eu estou fugindo, e é o melhor que eu consigo fazer.', 0.2),
 ('m080', 'N', 'Ele se pôs de cócoras, já pronto para levantar. Mas Aurora o interrompeu, com angústia em cada palavra:', 0.2),
 ('m081', 'AU', BR+'Por quê? Qual é o problema? Fala! Eu preciso saber.', 0.3),
 ('m082', 'JOSH', P1+'Eu vou subir agora, porque eu não confio em mim com você quando a casa está dormindo.', 0.5),
 ('m083', 'N', 'A frase pousou na sala como uma vela trocada. Aurora sentiu o calor subir pela nuca, naquele ponto onde o cabelo encontrava a pele e onde tudo o que ela sentia acontecia antes que a cabeça autorizasse. Apertou o xale. E perguntou:', 0.2),
 ('m084', 'AU', AI+'Você já pensou nisso antes?', 0.2),
 ('m085', 'JOSH', P1+'O tempo todo. Todo dia. Há dois meses.', 0.2),
 ('m086', 'AU', AI+'E por que está me dizendo agora?', 0.2),
 ('m087', 'JOSH', P1+'Porque você acabou de me implorar pra dizer.', 0.2),
 ('m088', 'AU', AI+'Eu pergunto há semanas. Você não responde.', 0.2),
 ('m089', 'JOSH', P1+'Eu sei. Eu sei que não respondo.', 0.2),
 ('m090', 'AU', AI+'Então o que mudou?', 0.2),
 ('m091', 'N', 'Josh olhou para ela de frente, pela primeira vez desde que tinha entrado. Não o relance de antes. Olhou como quem ia pagar o preço de olhar.', 0.2),
 ('m092', 'JOSH', P1+'A forma como você perguntou.', 1.0),
 ('m093', 'N', 'Aurora pousou o livro de Arav no chão, ao lado da poltrona. Não pousou depressa. Pousou com a calma de quem está liberando as duas mãos para uma coisa que ainda não tinha nome, mas que já estava decidida. O xale escorregou um pouco do ombro esquerdo, e ela não puxou de volta. Sentiu o ar frio encostar na pele descoberta, entre a manga da camisola e a queda do xale. Um frio de pele, não de corpo. Um frio que sabia muito bem que o resto dela estava em outra temperatura.', 0.3),
 ('m094', 'N', 'Josh viu o gesto. Não comentou. Continuou no chão, mas o corpo dele mudou de postura na hora em que o livro saiu do colo dela. Aurora viu o ombro dele se tensionar um milímetro, o antebraço firmar no joelho. Era a postura de quem se prepara para uma coisa que sabe que não vai conseguir evitar. Ele disse o nome dela:', 0.2),
 ('m095', 'JOSH', 'CLIP:josh_aurora_intenso', 0.2),
 ('m096', 'AU', AI+'Sim. Estou ouvindo.', 0.2),
 ('m097', 'JOSH', P1+'Antes de você dizer o que você vai dizer, eu preciso te dizer uma coisa. Três coisas, na verdade. Eu preciso que você saiba das três antes de qualquer outra coisa acontecer nesta sala.', 0.3),
 ('m098', 'N', 'Aurora ficou em silêncio. Era a frase mais longa que Josh tinha dito em meses, e tinha o tom de uma conversa que ele repetira dentro da própria cabeça centenas de vezes, mas nunca dissera em voz alta para ninguém.', 0.2),
 ('m099', 'AU', AI+'Está bem. Pode falar.', 0.3),
 ('m100', 'N', 'Josh respirou fundo. Aurora viu o peito dele subir, segurar dois segundos, descer. A camisa aberta deixava ver a base do pescoço, e a clavícula aparecia e sumia conforme ele respirava. Aurora seguiu o movimento. Não desviou. Quando ele começou, a voz saiu rouca, como se ele tivesse passado dias sem usá-la:', 0.2),
 ('m101', 'JOSH', P1+'A primeira. Eu sou afilhado do seu pai.', 0.2),
 ('m102', 'AU', AI+'Eu sei disso.', 0.2),
 ('m103', 'JOSH', P1+'Eu sei que você sabe. Mas saber e dizer em voz alta não são a mesma coisa. Eu nunca disse em voz alta. Estou dizendo agora. Eu sou afilhado do Ráge. Ele me trouxe pra essa cidade. Me deu o quarto leste. Me empresta os livros da biblioteca com a mão dele. Eu durmo numa cama que ele pagou, como na mesa dele, leio à luz das velas dele. E você é a única filha dele.', 0.3),
 ('m104', 'N', 'Josh parou um instante. Aurora viu o canto da boca dele tremer.', 0.2),
 ('m105', 'JOSH', P1+'Eu não consigo ser o homem que recebe tudo isso e, em troca, leva a filha dele pra sala de estar numa madrugada qualquer. Não consigo. Esse homem não é honesto. Os Rássels não são desonestos. Eu não posso ser o primeiro.', 0.4),
 ('m106', 'N', 'Aurora abriu a boca. Não disse nada. Fechou. Esperou. Josh continuou, a voz um pouco mais firme agora, como se dizer a primeira tivesse dado licença para as outras saírem:', 0.2),
 ('m107', 'JOSH', P1+'A segunda. Você é Svensson. Eu sou Rássel. Essas duas palavras não pesam o mesmo nessa cidade, e você sabe disso melhor do que eu. Você é herdeira da Brédigueide, do nome, da fortuna marítima que o seu pai construiu com a vida inteira dele. Eu sou o segundo filho de uma viúva da Zelândia, que cuida sozinha de terras que dão pra alimentar a família, mas não dão pra te sustentar do jeito que você vive.', 0.2),
 ('m108', 'N', 'Ele tropeçou na palavra seguinte, e recuperou:', 0.2),
 ('m109', 'JOSH', P1+'Se isso fosse uma coisa pra valer, você desceria. Socialmente. Materialmente. Aos olhos da sua mãe. Aos olhos dessa cidade. E a sua mãe veria primeiro. Eu não consigo te pedir pra descer.', 0.2),
 ('m110', 'AU', AI+'Eu desço se eu quiser descer.', 0.2),
 ('m111', 'JOSH', P1+'Você acha que quer. Mas você ainda tem dezoito anos, Aurôra.', 0.2),
 ('m112', 'AU', BR+'Ter dezoito anos não me torna burra.', 0.2),
 ('m113', 'N', 'Josh estendeu a mão no ar, como quem tenta parar uma carruagem em movimento sem encostar nela.', 0.2),
 ('m114', 'JOSH', P1+'Eu sei. Não é isso que eu estou dizendo. Eu estou dizendo que descer é uma decisão que precisa ser tomada com a vida inteira pela frente. E a sua vida inteira ainda não tem nem o nome dos próximos cinco anos.', 0.3),
 ('m115', 'N', 'Aurora ficou em silêncio. A vela pulsou. A chama nervosa deu um daqueles tremores curtos que vêm antes de o pavio começar a apagar. Faltava menos vela do que ela tinha calculado. Ela perguntou, sem levantar a voz:', 0.2),
 ('m116', 'AU', AI+'Tem mais?', 0.2),
 ('m117', 'JOSH', P1+'Tem. Tem mais uma.', 0.2),
 ('m118', 'AU', AI+'Então diga de uma vez.', 0.3),
 ('m119', 'N', 'Josh respirou. Olhou para o chão. Olhou para ela. Olhou para a própria mão direita, pousada no joelho, com o calo da pena visível no dedo médio. Quando voltou a falar, a voz estava mais grave que nas duas anteriores.', 0.2),
 ('m120', 'JOSH', P1+'A terceira é a que me mata. Eu te quero feliz, Aurôra. Eu te quero casada com alguém que te leve pra um lugar que honre o que o Arav deixou de herdar. Que honre a vida que o seu pai construiu pra você. Que honre o que a sua mãe quer pra você, mesmo que ela não saiba dizer o que quer com clareza. Eu fiz essa conta vinte vezes no quarto leste, nesses cinco meses, e a conta nunca fecha do meu lado. Você merece subir. Comigo, você desce.', 0.2),
 ('m121', 'N', 'Os olhos dele estavam marejados. Não chorando, mas naquela parte de cima do choro, a que ainda dá para conter se a pessoa segurar firme.', 0.2),
 ('m122', 'JOSH', P1+'Eu não posso ser o homem que pede pra você descer. Eu não consigo me olhar no espelho sendo esse homem.', 0.5),
 ('m123', 'N', 'Aurora ficou em silêncio mais um tempo. A sala estava muito quieta. Era a quietude da madrugada na Brédigueide: quando os passos de quem trabalhava dentro da casa já tinham acabado, os de quem trabalhava fora ainda não tinham começado, e o que sobrava era o assoalho assentando, a vela queimando e a respiração dos dois. Aurora ouviu o próprio coração na altura da garganta. Não estava acelerado. Estava forte.', 0.2),
 ('m124', 'AU', AI+'E então? Você terminou?', 0.2),
 ('m125', 'JOSH', P1+'Terminei. É isso.', 0.2),
 ('m126', 'AU', AI+'São três paredes.', 0.2),
 ('m127', 'JOSH', P1+'São, sim. Três.', 0.2),
 ('m128', 'AU', AI+'Você ensaiou isso.', 0.2),
 ('m129', 'JOSH', P1+'Centenas de vezes.', 0.2),
 ('m130', 'AU', AI+'E você ensaiou sozinho?', 0.2),
 ('m131', 'JOSH', P1+'Sozinho. No quarto leste.', 0.3),
 ('m132', 'N', 'Aurora respirou fundo. Não foi um suspiro. Foi a respiração de quem põe alguma coisa no lugar dentro do peito antes de se mexer.', 0.2),
 ('m133', 'AU', AI+'Josh.', 0.2),
 ('m134', 'JOSH', P1+'Sim. Estou aqui.', 0.2),
 ('m135', 'AU', AI+'Eu vou responder. Mas eu não vou responder no chão.', 0.3),
 ('m136', 'N', 'E se levantou do chão.', 1.0),
 ('m137', 'N', 'O xale caiu inteiro quando ela se levantou. Aurora não tentou pegar. Deixou o xale no chão, ao lado do livro de Arav, com a naturalidade de quem larga o casaco numa cadeira depois de um dia comprido. Ficou de pé no meio da sala, com a camisola de algodão claro até os tornozelos, os pés descalços no assoalho frio, e os cabelos soltos pela terceira vez na presença dele em cinco meses. A primeira tinha sido na biblioteca, na noite do livro de botânica. A segunda, na festa do celeiro. Esta era a terceira. Aurora sabia. Sabia que ele também sabia.', 0.3),
 ('m138', 'N', 'Josh continuou no chão por dois segundos. Depois levantou também. A distância entre os dois era de dois passos. Aurora calculou. Não um cálculo de matemática: um cálculo de corpo, do tipo que sabe a quantos centímetros está o outro antes de qualquer medida. Dois passos. Talvez menos. Ela falou, e a voz saiu mais firme do que esperava, porque a voz, ela estava descobrindo, ficava firme quando o resto do corpo estava decidido:', 0.2),
 ('m139', 'AU', AI+'Eu não tenho resposta pras três paredes. Eu não posso te garantir que o papai vai aceitar. Não posso te garantir que a mamãe vai aceitar. Não posso te garantir que essa cidade vai aceitar. Eu não tenho garantia nenhuma pra te dar, Josh. Eu tenho dezoito anos, e a única coisa que eu sei com certeza no mundo, nesse momento, é o que está dentro desse cômodo.', 0.3),
 ('m140', 'N', 'Josh não respondeu. Aurora continuou:', 0.2),
 ('m141', 'AU', AI+'Você quer que eu finja que eu não te quero, porque acha que fingindo me poupa. Mas não me poupa. Me deixa pior. Você não está sendo justo com a sua segunda parede, porque ela só funciona se eu não souber o que estou escolhendo. Eu sei. E eu não estou escolhendo descer. Eu estou escolhendo você. Não é a mesma coisa.', 0.2),
 ('m142', 'N', 'Ele disse o nome dela, mas ela o cortou:', 0.2),
 ('m143', 'AU', AI+'Espera. Eu não terminei.', 0.2),
 ('m144', 'N', 'Josh fechou a boca.', 0.2),
 ('m145', 'AU', AI+'A primeira parede é a que eu mais respeito. A lealdade ao papai. Eu sei o que o papai fez por você, e eu sei o tamanho do que ele te deu. Eu não vou te dizer que isso não importa. Importa. Mas a primeira parede não é uma parede entre nós dois. É uma parede entre você e ele. E você vai ter que conversar com ele, em algum momento. Não hoje. Eu não vou te pedir hoje. Mas em algum momento.', 0.3),
 ('m146', 'N', 'Josh fechou os olhos por um segundo. Quando abriu, estavam mais úmidos. Aurora baixou a voz, porque a terceira parede era a que tinha doído nela também:', 0.2),
 ('m147', 'AU', AI+'E a terceira é mentira. Não é mentira sua. É mentira do mundo. Você não tem o direito de decidir o que honra o Arav. Quem decide o que honra o Arav sou eu. E eu te digo agora: o Arav teria gostado de você. Ele teria te levado pro jardim e te dado um galho de roseira pra plantar. Ele teria escrito poesia sobre o seu jeito de cuidar das coisas. Você não rebaixa a memória dele. Você é o que a memória dele queria pra mim, mesmo que o mundo ainda não tenha palavras pra entender isso.', 0.4),
 ('m148', 'N', 'A vela tremeu de novo. Faltava muito pouco. Aurora deu um passo. Josh não recuou. A voz dele rachou um pouquinho na primeira sílaba:', 0.2),
 ('m149', 'JOSH', P1+'Aurôra, se você der mais um passo, eu não consigo recuar.', 0.2),
 ('m150', 'AU', AI+'Eu sei.', 0.2),
 ('m151', 'JOSH', P1+'Eu já não estou conseguindo recuar.', 0.2),
 ('m152', 'AU', AI+'Eu sei, Josh.', 0.2),
 ('m153', 'JOSH', P1+'Você precisa entender que eu não estou conseguindo recuar não é porque eu desisti das paredes. As paredes continuam de pé. Eu continuo achando o que eu acho. Mas eu sou um homem, Aurôra, e eu te quero há cinco meses. E tem coisa que o corpo não consegue mais segurar, mesmo quando a cabeça ainda está segurando.', 0.2),
 ('m154', 'AU', AI+'Eu sei. Eu sei, Josh.', 0.2),
 ('m155', 'JOSH', P1+'Então fica claro: se você não se afastar, o que vai acontecer agora, entre nós dois, não resolve nada.', 0.2),
 ('m156', 'AU', AI+'Fica claro, Josh.', 0.2),
 ('m157', 'JOSH', P1+'Mas vai acontecer.', 0.2),
 ('m158', 'AU', AI+'Vai, sim. Vai acontecer.', 0.3),
 ('m159', 'N', 'Aurora deu o segundo passo.', 1.0),
 ('m160', 'N', 'Estava a um palmo dele. Sentiu o calor do corpo dele antes do toque. Não tinha encostado ainda, e já sentia a temperatura. O cheiro do sabão da casa misturado com alguma coisa mais quente, de corpo, vindo da base do pescoço, onde a camisa estava aberta. Aurora levantou os olhos. O queixo dele estava ali, um pouco quadrado, com a sombra fina descendo até a clavícula. Ela seguiu a sombra até onde ela morria. Voltou os olhos para o rosto dele.', 0.3),
 ('m161', 'N', 'A mão dela subiu sozinha. Encostou primeiro nos dedos dele. Só os dedos, palma contra palma, sem fechar, porque Aurora queria conhecer a textura primeiro, sem o peso da decisão por cima. Foi nesse segundo, palma contra palma, sem tecido nenhum entre eles, que ela sentiu o calo na lateral do dedo médio dele. Era mais áspero do que ela tinha imaginado, em todas as vezes que tinha imaginado, em silêncio, nos últimos meses.', 0.2),
 ('m162', 'N', 'Um pedacinho de pele endurecido pelo trabalho de escrever. E Aurora sentiu, com uma clareza meio desconcertante, que aquele calo dava vontade de chorar e de rir ao mesmo tempo. Porque era a prova física de que ele existia. De que tinha um corpo, com hábitos e com tempo. E de que a vida dele estava acontecendo ao lado da vida dela havia cinco meses inteiros. Josh fechou os olhos. E disse o nome dela:', 0.2),
 ('m163', 'JOSH', 'CLIP:josh_aurora_intenso', 0.2),
 ('m164', 'AU', AI+'Eu sei, Josh. Eu sei.', 0.3),
 ('m165', 'N', 'A mão dele virou. Os dedos dela escorregaram entre os dedos dele, e fecharam. Foi a primeira vez que as mãos dos dois se prenderam. Não cortesia. Não condução de dança. Prenderam. Aurora sentiu o aperto firme dos dedos dele nas costas dos dela. Sentiu o polegar dele subir até a base do pulso, e parar ali, onde o pulso batia. Ele ficou com o polegar ali por meio segundo, sentindo a batida. Aurora soube, porque viu o queixo dele se afrouxar de leve quando ele encontrou o ritmo.', 0.2),
 ('m166', 'N', 'A outra mão dela subiu pela camisa dele, no peito, sem pousar. Só seguiu o caminho do tecido até a base do pescoço, onde o botão estava aberto, e parou ali, com a ponta dos dedos no osso da clavícula. Era pele, desta vez. Não tecido. Pele quente, mais quente do que a do braço dela, com aquela diferença de temperatura que ela nunca tinha tido a chance de comprovar. Josh abriu os olhos, e disse o nome dela mais uma vez.', 0.2),
 ('m167', 'JOSH', 'CLIP:josh_aurora_intenso', 0.2),
 ('m168', 'AU', AI+'Me beija.', 1.0),
 ('m169', 'N', 'Ele baixou a cabeça primeiro. A boca dele encostou na dela com um cuidado que era também impaciência: a impaciência de quem tinha esperado tempo demais e precisava, agora, não estragar o primeiro toque. Foi um beijo curto. Lábios contra lábios. Por uns dois segundos. Aurora sentiu os lábios dele mais cheios do que tinha imaginado, levemente rachados de um lado, do jeito dos homens que esquecem de beber água no fim do verão.', 0.2),
 ('m170', 'N', 'Depois Josh recuou meio centímetro, sem soltar a mão dela, e olhou nos olhos dela.', 0.2),
 ('m171', 'JOSH', P1+'Você tem certeza?', 0.2),
 ('m172', 'AU', AI+'Eu já disse que tenho.', 0.2),
 ('m173', 'JOSH', P1+'Eu precisava ouvir de novo.', 0.2),
 ('m174', 'N', 'Aurora baixou a voz, sem sussurrar:', 0.2),
 ('m175', 'AU', AI+'Tenho, sim. Me beija de novo.', 0.4),
 ('m176', 'N', 'Na segunda vez, a boca dele desceu mais firme. Aurora abriu os lábios por reflexo, sem ter decidido, no exato instante em que soltou o ar que vinha prendendo havia uns dez segundos. O suspiro dela saiu entre os lábios dele. E Aurora sentiu, com uma clareza que nunca tinha tido sobre o próprio corpo, que a coisa entre as costelas e a base do pescoço, que ela não sabia nomear, acabava de receber um nome.', 0.3),
 ('m177', 'N', 'A mão dele soltou a dela e foi para a cintura. Pousou do lado direito, aberta inteira contra o tecido da camisola. Aurora sentiu a pressão firme, larga, o peso da mão dele através do algodão, de um jeito que ela nunca tinha pensado que se pudesse sentir. A mão dele era maior do que ela tinha imaginado. Cobria a lateral inteira da cintura. Os dedos abertos quase alcançavam as costas, e o polegar apertava o lugar logo abaixo da costela.', 0.2),
 ('m178', 'N', 'A outra mão dele subiu para a nuca dela. A mão direita. A do calo. Aurora sentiu os dedos dele entrarem por baixo do cabelo solto, separarem os fios e fecharem onde o cabelo encontrava a pele. Não fechou forte. Fechou o suficiente para ela entender que ele estava ali, que estava segurando, que não ia soltar tão cedo. Aurora fechou os olhos sem ter decidido fechar. A pele inteira das costas reagiu como se tivesse sido tocada de uma vez só, de cima a baixo, e o calor passou pela cintura, onde estava a outra mão dele, e voltou.', 0.2),
 ('m179', 'N', 'Aurora ouviu o próprio suspiro. Um som que escapou sem permissão, baixo, do tipo que ela não sabia que sabia fazer. Josh ouviu também. Ela sentiu o peito dele responder: uma respiração mais funda, mais rápida, contra o peito dela. A mão dela subiu para o cabelo dele. Era a primeira vez. Era mais grosso do que ela tinha imaginado. Mais quente. Os dedos dela entraram por trás da orelha dele, subiram, e fecharam na nuca. Com a mesma força que ele tinha usado nela: a força que não é para machucar, mas para dizer: eu estou aqui, eu não vou sair.', 0.2),
 ('m180', 'N', 'A boca dele desceu para o canto da boca dela. Depois para a linha do queixo. Depois para a base do pescoço, onde o xale tinha estado antes de cair. Aurora sentiu os lábios dele na clavícula, e o calor que subiu não foi pela nuca, nem pelo pescoço. Foi por baixo da pele inteira, ao mesmo tempo. Uma onda que ela nunca tinha sentido na vida, e que ela soube, no segundo em que sentiu, que ia dividir o tempo dela em antes e depois. Aurora segurou o rosto dele com as duas mãos. Trouxe de volta para a boca dela. E desta vez, foi ela quem beijou primeiro.', 1.2),
 ('m181', 'N', 'Em algum momento, eles pararam. Aurora não soube quanto tempo tinha passado. Podiam ter sido dois minutos, podiam ter sido dez. A vela ainda estava acesa, a chama ainda nervosa. O livro de Arav estava no chão. O xale também. A camisola estava em ordem: ele não tinha tocado o que não devia. A cintura, a nuca, o cabelo, o pescoço, a clavícula. Nada mais. Aurora reconheceu, com uma honestidade que quase achou engraçada, que ele tinha feito o cálculo até no meio do beijo.', 0.2),
 ('m182', 'N', 'Josh tinha a testa encostada na dela. Os dois respirando. A respiração dele estava mais alta que a dela. Não muito. Mas o suficiente para Aurora perceber, e para uma vaidade pequena e meio absurda registrar. Ele disse o nome dela, baixinho:', 0.2),
 ('m183', 'JOSH', 'CLIP:josh_aurora_intenso', 0.2),
 ('m184', 'AU', AI+'Sim, Josh.', 0.2),
 ('m185', 'JOSH', P1+'Eu não consigo voltar disso.', 0.2),
 ('m186', 'AU', AI+'Eu sei. Nem eu.', 0.2),
 ('m187', 'JOSH', P1+'E eu também não quero voltar disso. Eu preciso te dizer isso antes de subir.', 0.2),
 ('m188', 'AU', AI+'Está dito, Josh. Eu ouvi.', 0.2),
 ('m189', 'JOSH', P1+'Mas eu vou subir.', 0.2),
 ('m190', 'AU', AI+'Eu sei que vai.', 0.3),
 ('m191', 'N', 'Ele afastou a testa. Olhou para ela. Tinha os olhos marejados de um jeito que Aurora nunca tinha visto. Não era choro. Era o que vem antes do choro, a parte que ainda dá para conter. Aurora levantou a mão. Tocou o canto do olho direito dele com o polegar. Não enxugou nada, porque não havia lágrima para enxugar. Só pousou ali, como quem deixa um selo.', 0.2),
 ('m192', 'JOSH', P1+'E amanhã...', 0.2),
 ('m193', 'AU', AI+'Amanhã o quê?', 0.2),
 ('m194', 'JOSH', P1+'Amanhã não vai ser fácil.', 0.2),
 ('m195', 'AU', AI+'Eu sei disso.', 0.2),
 ('m196', 'JOSH', P1+'Eu não sei o que eu vou fazer amanhã, Aurôra. Eu vou acordar e a casa vai estar como sempre. O seu pai vai estar tomando café com o jornal. A sua mãe vai estar com a Vibêke na sala de costura. E eu vou ter que olhar pro seu pai sabendo o que eu fiz. E eu não sei se eu consigo.', 0.2),
 ('m197', 'AU', AI+'Você consegue.', 0.2),
 ('m198', 'JOSH', P1+'Como? Me diz como.', 0.2),
 ('m199', 'AU', AI+'Porque a única coisa pior do que olhar pro meu pai sabendo o que você fez é olhar pra mim fingindo que não fez. E eu sei que você não vai me fazer isso. Eu sei que você não vai voltar a me tratar como me trata desde a festa do celeiro. Esse é o único jeito que eu sei que você consegue.', 0.3),
 ('m200', 'N', 'Josh ficou um segundo sem responder. Depois assentiu, com um movimento muito pequeno do queixo. Aurora viu. Ele se afastou devagar. Recuou um passo. Os dedos dele soltaram o cabelo dela com a mesma lentidão com que tinham entrado. A mão da cintura saiu por último. Aurora sentiu o frio voltar onde a mão dele tinha estado, do mesmo jeito que tinha sentido o calor antes do toque.', 0.3),
 ('m201', 'AU', AI+'Josh.', 0.2),
 ('m202', 'JOSH', P1+'Sim. Pode falar.', 0.2),
 ('m203', 'AU', AI+'Boa noite, Josh.', 0.2),
 ('m204', 'JOSH', P1+'Boa noite, Aurôra.', 0.4),
 ('m205', 'N', 'Ele pegou a vela apagada da mesa lateral. Não acendeu: ia fazer o caminho de volta de cor. Olhou para ela mais uma vez. Não disse nada. Saiu descalço pelo corredor. E Aurora ouviu o décimo segundo degrau ranger de novo, mais devagar dessa vez, do jeito que range quando um homem sobe a escada sem pressa, porque não quer chegar ao quarto.', 1.0),
 ('m206', 'N', 'Aurora ficou sozinha. Sentou no chão de novo. Pegou o livro. Pegou o xale. Pôs o xale de volta nos ombros. O xale estava frio. A pele dela estava quente. O contraste foi tão imediato que ela teve que fechar os olhos por dois segundos, para o corpo aceitar que aquela mudança de temperatura era real. A vela continuava na mesa lateral. A chama tinha começado, enfim, a baixar. O pavio se inclinava. Restava talvez um minuto.', 0.2),
 ('m207', 'N', 'Aurora abriu o livro na página trinta e sete. Procurou de novo o verso. E leu, baixo, mas alto o bastante para ouvir o próprio som no cômodo vazio. Não com a voz de Arav. Com a voz dela.', 0.3),
 ('m208', 'AU', AI+'O que é viver, senão arder.', 0.5),
 ('m209', 'N', 'Foi a primeira vez na vida que ela leu o irmão com a própria voz, e não com a voz dele. E Aurora pensou, com uma pontada que era tristeza e mais alguma coisa que ela ainda não sabia nomear, que talvez fosse esse o jeito de Arav continuar existindo: deixar de ser uma voz emprestada, e virar uma frase própria.', 0.4),
 ('m210', 'N', 'Fechou o livro. Apagou a vela. Subiu descalça pela escada que conhecia tão bem que sabia em que degrau pisar com mais peso para não fazer barulho. Pulou o décimo segundo. Entrou no quarto. Fechou a porta sem barulho. Deitou. E ficou de olhos abertos, no escuro, com a mão direita pousada na cintura, onde a mão dele ainda parecia estar, e a mão esquerda pousada nos lábios, onde os dele tinham estado havia pouco.', 0.0),
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
    sf.write(f"{SCR}/cap19-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap19-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap19-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
