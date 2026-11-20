import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = os.environ.get("GTTS_BASE", "/tmp/gtts") + "/gtts18"
SCR = os.environ.get("GTTS_BASE", "/tmp/gtts")
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
SEG = [
 ('i001', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo dezoito: O baile.', 1.2),
 ('i002', 'N', 'Este capítulo volta aos olhos de Aurora. No capítulo anterior, a prima dela, Vibêke, chegou de Viborg para passar dois meses na casa, alegre, sem filtro, e apaixonada por um rapaz de lá, Lauritz Brandt. No almoço, Eleonora pediu a Josh que acompanhasse Vibêke ao baile dos Lundgren. E Aurora, na porta da sala, disse a ele que a mãe não ia parar.', 0.6),
 ('i003', 'N', 'Aurora soube que a noite ia ser difícil quando, às seis e meia da tarde, Vibêke entrou no quarto dela sem bater, com dois vestidos pendurados nos braços e uma pergunta que Aurora não esperava:', 0.2),
 ('i004', 'VIB', VB+'O verde ou o lilás?', 0.2),
 ('i005', 'AU', BR+'E é pra quem?', 0.2),
 ('i006', 'VIB', VB+'Pra mim. Pro baile.', 0.3),
 ('i007', 'N', 'Aurora olhou os dois vestidos. O verde era escuro, sério, de uma elegância que pedia salão grande e atenção contida. O lilás era mais claro, de manga curta, de um tom que ficava bonito em moças loiras de pele clara, e que ia chamar a atenção do tipo de homem que olha o vestido antes de olhar o rosto. Ela respondeu, sem pensar:', 0.2),
 ('i008', 'AU', BR+'O verde, com certeza.', 0.2),
 ('i009', 'VIB', VB+'Por quê? Por que o verde?', 0.2),
 ('i010', 'AU', BR+'Porque o lilás é... é um vestido que pede que olhem pra você. E você já vai chamar atenção sem ele.', 0.3),
 ('i011', 'N', 'Vibêke pensou. Olhou os dois vestidos no braço. Olhou para a prima:', 0.2),
 ('i012', 'VIB', VB+'Você está dizendo isso como prima ou como conselheira?', 0.2),
 ('i013', 'AU', BR+'Como prima. Eu tenho certeza de que você não vai querer chamar atenção, por causa do Lauritz. Estou certa?', 0.2),
 ('i014', 'VIB', VB+'Está certa, sim. Então é o verde. Se você estivesse me aconselhando como conselheira, eu ia saber que era o que você não escolheu. Mas como prima, eu confio.', 0.4),
 ('i015', 'N', 'E saiu do quarto. Aurora ficou na cadeira da penteadeira mais um minuto, com a escova na mão, olhando o próprio reflexo. Não era a resposta que tinha planejado. Não era a resposta que teria dado três dias antes. Mas tinha sido a verdadeira. E a verdade, ela percebeu com uma pontada que ainda não sabia nomear, era que já gostava da prima o bastante para querer que ela chegasse bem ao baile. Só que Aurora não tinha pensado, na verdade tinha esquecido, que chegar ao baile também queria dizer: chegar de braço dado com Josh.', 1.0),
 ('i016', 'N', 'A carruagem dos Svensson saiu da Brédigueide às sete e quarenta. O pai ao lado da mãe num banco. Aurora ao lado da prima no outro. E Josh no canto, com o sobretudo dobrado no colo, em silêncio. Aurora tentou não olhar para ele. Conseguiu por uns três minutos. Olhou pela janela, para as casas conhecidas passando devagar, para a luz da lanterna batendo no vidro embaçado pelo hálito dos cinco. Deu tudo certo por três minutos. Depois ela olhou.', 0.4),
 ('i017', 'N', 'Ele estava com a camisa de gola alta. A que a mãe dele tinha bordado, com aquele pequeno desenho discreto na lapela que Aurora viu pela primeira vez no primeiro jantar dele na casa, e que guardava na memória como se fosse um endereço. Era a camisa de que ela mais gostava. Não por causa dela: Aurora sabia que não. Tinha sido pela ocasião. Mas o registro entrou. E o aperto entrou junto, naquele lugar entre as costelas e a base do pescoço que ela ainda não tinha nome para chamar.', 0.4),
 ('i018', 'N', 'Olhou de novo, mais devagar. A mão direita dele estava no colo, sobre o sobretudo. Aurora viu o calo na lateral do dedo médio, onde a pena apertava quando ele escrevia. Um calo que ela tinha visto se formar nos últimos cinco meses, em horas de leitura na biblioteca, ou de cartas escritas para casa. Sabia exatamente em que mês o calo tinha aparecido: uma informação que ela não devia ter. Olhou o queixo dele, virado para a outra janela. Um ângulo um pouco quadrado, que pegava a luz da lanterna e fazia uma sombra fina descendo até o pescoço. Aurora seguiu a sombra com os olhos por dois segundos. E voltou para o colo.', 0.4),
 ('i019', 'N', 'Enquanto isso, a mãe dizia a Vibêke:', 0.2),
 ('i020', 'EL', ELP+'Os Lundgren são boa gente. A senhora Lundgren foi colega de infância da minha mãe. O salão deles é o segundo maior da cidade, depois do Teatro Real. Não fique impressionada.', 0.2),
 ('i021', 'VIB', VB+'Eu vou ficar impressionada.', 0.2),
 ('i022', 'EL', ELP+'Então fique sem deixar transparecer.', 0.2),
 ('i023', 'VIB', VB+'Tia, sabe de uma coisa?', 0.2),
 ('i024', 'EL', ELP+'Sim, querida?', 0.2),
 ('i025', 'VIB', VB+'Eu não consigo.', 0.4),
 ('i026', 'N', 'A mãe deu um sorriso pequeno. O pai ergueu uma sobrancelha. E Josh, no canto, soltou um som pelo nariz que Aurora reconheceu como o começo do riso dele, engolido a tempo. Era o segundo riso engolido que ela contava naquele dia. Estava começando a contar. Vinte minutos depois, a carruagem parou diante da casa dos Lundgren.', 1.0),
 ('i027', 'N', 'O salão era exatamente como a mãe tinha descrito. Pé-direito altíssimo. Quatro lustres de cristal enfileirados no teto. Uma pintura na cúpula central, de algum pintor italiano, talvez. A pista no centro, cercada de colunas claras, e uma orquestra de oito músicos no canto, afinando. A senhora Lundgren os recebeu na entrada com a deferência cordial de quem sabe administrar o próprio prestígio. Cumprimentou o pai, a mãe, Aurora. E quando chegou em Vibêke, olhou para Eleonora:', 0.2),
 ('i028', 'LUN', ELP+'Então esta é a sobrinha de Viborg.', 0.2),
 ('i029', 'EL', ELP+'Vibêke Bierg. A filha da Karoline.', 0.2),
 ('i030', 'N', 'A senhora Lundgren deu um sorriso de verdade, e estendeu a mão:', 0.2),
 ('i031', 'LUN', ELP+'A Karoline. Eu dancei em roda com a sua mãe num baile em Ólborg, quando a gente tinha vinte anos. Ela pisou no meu pé três vezes.', 0.2),
 ('i032', 'VIB', VB+'A mamãe ainda pisa no pé do papai três vezes por dança.', 0.2),
 ('i033', 'LUN', ELP+'Então não mudou nada. Senhor Russel. Sejam bem-vindos.', 0.4),
 ('i034', 'N', 'Vibêke já estava de braço dado com Josh. Aurora viu o gesto. Natural, sem peso, do jeito que a prima fazia tudo. Com dois irmãos mais velhos, Aurora imaginou, Vibêke devia dar o braço a rapazes a vida inteira sem dar a isso significado nenhum. Mas Aurora viu o braço dele. O músculo se contraindo dentro da camisa. O jeito de oferecer o cotovelo, levemente para fora, com a mão fechada: uma postura que a mãe tinha ensinado nos últimos meses, e que ele já fazia como coisa sua. Aurora viu. E o registro foi físico: o ombro dele, a linha do braço dele, a leveza com que ele recebeu ali a mão da prima. Respirou pelo nariz uma vez. Sorriu o sorriso medido. E entrou no salão atrás dos dois.', 1.0),
 ('i035', 'N', 'Os primeiros quinze minutos foram do tipo que ela sabia fazer de cor. Cumprimentou Ingrid, que estava com um vestido roxo emprestado da mãe e um olhar que pedia uma conversa adiada. Cumprimentou a senhora Holst, que falou do tempo. Cumprimentou um senhor cujo nome não lembrava. Aceitou uma taça de limonada. Erik Mortensen estava do outro lado do salão, conversando com o pai. Aurora encontrou os olhos dele por um segundo e fez o aceno mínimo de quem reconhece. Ele retribuiu e voltou ao pai. E Aurora seguiu adiante, agradecendo a Deus por ele não vir até ela. E procurou Josh com os olhos, sem que a procura parecesse procura.', 0.4),
 ('i036', 'N', 'Encontrou. Do outro lado, perto de uma coluna, com Vibêke. A prima gesticulava, a mão levantada, descrevendo o tamanho de alguma coisa. Ele ouvia com o canto da boca já subindo, esperando o final. E quando o final chegou, Josh riu. Riu alto, sem se controlar. Uma risada aberta, de ombro balançando, de peito subindo e descendo duas vezes antes de a respiração voltar ao normal. Do tipo que ele riu com o pai dela na sobremesa do dia anterior, e que Aurôra tinha registrado como a primeira vez que o ouvia rir assim, aberto, dentro daquela casa.', 0.4),
 ('i037', 'N', 'Aurora sentiu o aperto. Nas costelas. No peito. Um aperto físico, com forma, que ela podia apontar com a mão, se fosse educado fazer isso num salão. Não era ciúme. Aurora repetiu para si mesma três vezes que não era ciúme. Vibêke amava Lauritz. Josh sabia. A casa inteira sabia. Não era ciúme. Mas o aperto não pediu licença para existir. A mão dela se fechou no leque. O calor subiu pelo pescoço e chegou à orelha. Ela abriu o leque e se abanou duas vezes. Olhou para o chão.', 0.4),
 ('i038', 'N', 'Aquele riso, ele nunca tinha soltado com ela. Nenhuma vez, em nenhuma conversa entre os dois, ela percebeu pela segunda vez, com uma honestidade desconfortável. Até ali, achava que não era do feitio dele gargalhar. Mas era. Pelo menos tinha sido, dois minutos antes, com a prima. Ele tinha se soltado. Mas não com ela. Não com Aurora.', 1.0),
 ('i039', 'N', 'A voz da mãe veio baixa, ao lado dela:', 0.2),
 ('i040', 'EL', ELP+'Aurora, querida.', 0.2),
 ('i041', 'AU', BR+'Sim, mamãe?', 0.2),
 ('i042', 'EL', ELP+'Você está bem?', 0.2),
 ('i043', 'AU', BR+'Estou, sim.', 0.2),
 ('i044', 'EL', ELP+'Você está se abanando com a energia de quem está prestes a desmaiar.', 0.2),
 ('i045', 'AU', BR+'É que está calor.', 0.2),
 ('i046', 'N', 'A mãe não olhou para ela. Olhava para a pista, onde os primeiros casais se posicionavam:', 0.2),
 ('i047', 'EL', ELP+'Está calor para todo mundo, querida. Mas só você está se abanando desse jeito.', 0.3),
 ('i048', 'N', 'Aurora diminuiu o ritmo do leque, e perguntou:', 0.2),
 ('i049', 'AU', BR+'Melhor assim?', 0.2),
 ('i050', 'EL', ELP+'Melhor, sim.', 0.4),
 ('i051', 'N', 'A mãe não disse mais nada. Mas Aurora sabia, com a precisão de quem foi criada por aquela mulher, que a observação tinha sido feita, anotada e arquivada. Eleonora Svensson não comentava o leque da filha por acaso. Estava medindo alguma coisa. E o leque era o termômetro. Aurora fechou o leque, pousou no colo, e sentou um centímetro mais reta. A orquestra começou a tocar.', 1.0),
 ('i052', 'N', 'A primeira dança era uma quadrilha simples, do tipo que se usa para abrir o baile sem prender ninguém num par. Aurora viu Josh estender a mão para Vibêke. A prima aceitou, e os dois entraram na pista. Aurora ficou na cadeira. Tinha aceitado, na carruagem, que ia dançar pelo menos duas vezes, para não dar o que falar. Mas a primeira, não. A primeira era para olhar. E ela olhou.', 0.4),
 ('i053', 'N', 'Ele não dançava tão mal quanto tinha avisado no almoço. Acertava o passo, e atrasava o giro para acompanhar a prima, que era bem desengonçada. Dançava com a aplicação séria de quem faz o melhor que pode. E Vibêke ria de cada erro próprio, com a alegria de quem não liga para o julgamento alheio. Ela era livre. E talvez isso fosse o que mais machucava Aurora: o jeito espontâneo, natural, da prima, tão diferente dela mesma, sempre vestida de armadura para se proteger da sociedade. Os dois se entendiam na pista como se entendiam fora dela: sem manobra, sem cálculo, sem peso.', 0.4),
 ('i054', 'N', 'Aurora reparou no jeito como ele segurava a mão da prima. Leve. A mão dele só tocava a dela, sem fechar, sem prender. Uma mão de cortesia, não de envolvimento. Aurora sabia distinguir as duas, e o detalhe devia ter aliviado. Não aliviou. Porque a mão dele, mesmo de cortesia, era a mão dele. E Aurora conhecia aquela mão. O calo da pena. O jeito de fechar no batente quando ele se encostava na porta da biblioteca. O jeito de pousar sobre a mesa da cozinha quando ele lia, ou fingia ler, nas manhãs que eram só dos dois. E ver aquela mão tocando a de outra moça, mesmo sem fechar, era uma informação nova que o corpo de Aurora recebia pela primeira vez na vida. E o corpo dela não estava lidando bem com isso.', 1.0),
 ('i055', 'N', 'No intervalo entre a primeira e a segunda dança, Vibêke encontrou Aurora perto da janela:', 0.2),
 ('i056', 'VIB', VB+'Aurora! Eu acabei de contar do Lauritz pra senhora Lundgren.', 0.2),
 ('i057', 'AU', BR+'Você contou mesmo?', 0.2),
 ('i058', 'N', 'Vibêke fez a careta de quem descobre um defeito em si mesma:', 0.2),
 ('i059', 'VIB', VB+'Eu acho que ela nem tinha perguntado. Acho que eu enfiei a história sem precisar. Eu vou ter que aprender a esperar.', 0.2),
 ('i060', 'AU', BR+'Foi assim no almoço também?', 0.2),
 ('i061', 'VIB', VB+'No almoço foi pior. Eu falei do Lauritz três vezes pra mãe de uma moça que eu nem sei o nome. Pra moça eu já contei. Pro senhor Holst também. Acho que eu estou nervosa. Quando eu fico nervosa, eu falo do Lauritz. É um vício.', 0.2),
 ('i062', 'AU', BR+'É um vício útil.', 0.2),
 ('i063', 'VIB', VB+'Útil por quê?', 0.2),
 ('i064', 'N', 'Aurora hesitou. Olhou para a prima, que esperava a resposta com aquele olhar de criança grande, sem segunda intenção. E disse, baixo:', 0.2),
 ('i065', 'AU', AI+'Porque metade do salão já sabe que você tem dono. E isso vai te poupar de um monte de conversa boba.', 0.3),
 ('i066', 'N', 'Vibêke pensou. Olhou para o próprio leque. E sorriu:', 0.2),
 ('i067', 'VIB', VB+'Eu não tinha pensado nisso.', 0.2),
 ('i068', 'AU', BR+'Eu sei que não.', 0.2),
 ('i069', 'VIB', VB+'E agora, você está sendo prima ou conselheira?', 0.2),
 ('i070', 'AU', BR+'As duas coisas.', 0.2),
 ('i071', 'N', 'Vibêke apertou de leve o braço de Aurora:', 0.2),
 ('i072', 'VIB', VB+'Você é boa, sabia?', 0.4),
 ('i073', 'N', 'E saiu para a próxima dança, onde Josh já esperava com a mão estendida, e onde mais três casais se posicionavam para uma valsa lenta que Aurora ia ter de assistir inteira.', 1.0),
 ('i074', 'N', 'A valsa durou seis minutos. Aurora contou. Não porque quisesse. Os olhos dela continuavam achando o relógio no canto do salão, sem que ela tivesse dado permissão ao próprio cérebro. Seis minutos. Em algum momento, ele olhou na direção dela. Um olhar de relance, do tipo que quem dança lança quando passa pelo ponto de onde se vê o canto em que a outra pessoa está. Não foi um olhar carregado. Foi um registro: você ainda está aí. Aurora, de propósito, não retribuiu. Continuou olhando o relógio.', 0.4),
 ('i075', 'N', 'Quando a valsa acabou, ele agradeceu a Vibêke com a mesura curta que a mãe dela tinha ensinado, e a prima respondeu com a reverência da Karoline. Vibêke foi para um grupo de moças. E Josh atravessou o salão. Em diagonal. Sem correr. E parou ao lado de Aurora, na distância correta. Antes de olhar, ela sentiu o cheiro do salão no casaco dele: cera de vela, perfume das moças com quem ele cruzou nas trocas de par, e, por baixo de tudo, o sabão da casa, o que Helle usava na roupa dele, e que Aurora cheirava toda semana sem querer cheirar, quando a lavanderia ficava de porta aberta. Ele disse:', 0.2),
 ('i076', 'JOSH', 'CLIP:josh_aurora', 0.15),
 ('i076b', 'JOSH', P1+'Tudo bem?', 0.2),
 ('i077', 'AU', 'CLIP:take-cap18-i077-aurora', 0.3),
 ('i078', 'JOSH', P1+'A sua mãe me pediu pra trazer uma água pra você. Antes da valsa.', 0.2),
 ('i079', 'AU', AI+'A minha mãe te mandou aqui? Por quê?', 0.3),
 ('i082', 'N', 'Ele hesitou. Olhou de relance para o canto onde a mãe dela conversava com a senhora Lundgren, sem olhar para os dois, mas com o corpo num ângulo que dizia que estava prestando atenção em outra direção:', 0.2),
 ('i083', 'JOSH', P1+'Acho que ela te viu sozinha nessa janela e ficou preocupada.', 0.2),
 ('i084', 'AU', AI+'Pode dizer a ela que eu estou ótima sozinha. E que você cumpriu o recado.', 0.2),
 ('i087', 'JOSH', P1+'E a água? Você não vai querer?', 0.2),
 ('i088', 'AU', AI+'Não, Josh. Se eu quiser, eu mesma busco. Obrigada.', 0.4),
 ('i089', 'N', 'Mas ele não saiu. Ficou ali, ao lado dela, segurando a taça que ela não tinha pedido. Aurora reparou nas mãos dele. A direita no copo. A esquerda no bolso do casaco. As duas paradas, com a precisão de quem está controlando a respiração. Ele comentou:', 0.2),
 ('i090', 'JOSH', P1+'A Vibêke contou do Lauritz pra meia Copenhague em uma hora.', 0.2),
 ('i091', 'AU', AI+'Pra mim também. Ela fala dele quando fica nervosa.', 0.2),
 ('i092', 'JOSH', P1+'Então ela passou a valsa inteira nervosa. Não falou de outra coisa.', 0.2),
 ('i096', 'AU', AI+'Vocês, pelo visto, conversaram bastante durante a valsa.', 0.4),
 ('i097', 'N', 'Ele olhou para ela. E não desviou os olhos logo:', 0.2),
 ('i098', 'JOSH', 'CLIP:josh_aurora', 0.2),
 ('i100', 'JOSH', P1+'Tem alguma coisa te incomodando?', 0.4),
 ('i101', 'N', 'A pergunta veio sem aviso. Aurora não estava preparada. Olhou para ele. Ele olhava para ela, e tinha perguntado como quem pergunta do tempo. Ela respondeu:', 0.2),
 ('i102', 'AU', AI+'Não. Não tem nada.', 0.2),
 ('i103', 'JOSH', P1+'Você passou a valsa inteira olhando pro relógio. Eu vi.', 0.4),
 ('i107', 'N', 'Aurora respirou fundo. Olhou para a limonada intocada na mão. Pousou a taça no parapeito da janela. E disse:', 0.2),
 ('i108', 'AU', AI+'Eu não tenho motivo nenhum pra estar incomodada, Josh. A Vibêke é uma boa pessoa. E ela é apaixonada pelo Lauritz.', 0.2),
 ('i109', 'JOSH', P1+'Eu nunca disse que você tinha motivo.', 0.2),
 ('i111', 'N', 'Ele balançou a cabeça, e um fio se soltou do cabelo preso com pomada, caindo na testa. Aurora encerrou:', 0.2),
 ('i115', 'AU', AI+'Então pronto.', 0.3),
 ('i116', 'JOSH', 'CLIP:josh_aurora', 0.25),
 ('i116b', 'JOSH', P1+'Ter motivo ou não ter motivo não muda o que você está sentindo.', 0.6),
 ('i117', 'N', 'Aurora ficou em silêncio. Não conseguiu olhar para ele. A orquestra começou a se reposicionar para a dança seguinte. A senhora Lundgren bateu palmas duas vezes, pedindo atenção para anunciar o compositor da próxima peça. Os casais voltavam para a pista. Ela disse:', 0.2),
 ('i118', 'AU', AI+'Eu vou voltar pro meu lugar. Você vai dançar com ela de novo?', 0.2),
 ('i121', 'JOSH', P1+'Vou. A sua mãe me pediu pra acompanhar a Vibêke a noite toda.', 0.2),
 ('i122', 'AU', AI+'Boa noite, Josh.', 0.2),
 ('i123', 'JOSH', P1+'A noite ainda não acabou.', 0.2),
 ('i124', 'AU', AI+'Eu sei que não.', 0.6),
 ('i125', 'N', 'Aurora atravessou o salão de volta para a cadeira ao lado da mãe. Sentou. Pegou o leque. E não ficou ali muito tempo. Erik Mortensen apareceu antes do segundo compasso. Não com a postura de quem cobra. Com a postura de quem cumpre. Inclinou-se diante da cadeira dela, estendeu a mão com a moderação cordial de sempre, e pediu o prazer da dança. A mãe, ao lado, não disse nada. Nem precisava: o sim de Aurora vinha embutido no protocolo da noite desde que ela entrou no salão.', 0.4),
 ('i126', 'N', 'Aurora disse sim. Entrou na pista com Erik, e dançou. Erik dançava bem. Previsível. A mão firme e leve no lugar certo da cintura. Em qualquer outra noite, Aurora teria agradecido a quietude de dançar com alguém que não exigia nada. Naquela noite, a quietude foi outra coisa: um espaço vazio que a cabeça encheu com tudo o que ela tinha decidido não pensar. Os olhos continuaram, sem autorização, achando o canto onde a prima e Josh riam de alguma coisa nova, e voltando para o ombro de Erik, com a obediência mecânica de quem cumpre o trecho. Erik não comentou. Não perguntou nada. Conduziu até o fim, agradeceu com a mesura curta, e a devolveu à cadeira.', 0.4),
 ('i127', 'N', 'A segunda dança foi com um rapaz que ela não conhecia, primo dos Lundgren, apresentado pela mãe com uma frase de uma linha. Dançava pior. Falava demais. Comentou três vezes o calor do salão, e duas vezes o vestido dela, como se fossem a mesma coisa. Aurora sorriu o sorriso medido, respondeu com meias frases, e viu, por cima do ombro dele, Josh dando um giro atrasado que fez a prima rir alto. Quando a música acabou, ela agradeceu, voltou para a cadeira, pegou o leque, e dessa vez não levantou mais. Não olhou mais para a pista pelo resto do baile.', 1.0),
 ('i128', 'N', 'A carruagem voltou para casa às onze e quarenta. Vibêke conversava com a tia sobre a senhora Lundgren, sobre o vestido lilás de uma moça da mesa do bufê, sobre uma história da mãe lembrada por um comentário da senhora Holst. O pai escutava com o sorriso de quem está cansado, mas contente. Josh, no canto, em silêncio de novo. E Aurora ao lado da prima, com o rosto virado para a janela. As casas conhecidas começaram a aparecer. A esquina dos Holst. A casa dos Mortensen. O portão da casa. E a carruagem parou.', 0.4),
 ('i129', 'N', 'Helle abriu a porta. Vibêke desceu primeiro, contando alguma coisa para a criada no caminho. A mãe desceu depois, de braço com o pai. Aurora desceu por último, antes dele. E, ao passar pela porta da carruagem, o sobretudo dele roçou no braço dela. Não foi nada. Um centímetro de tecido. Lã grossa, de inverno, embora fosse agosto: ele usava porque a cidade esfriava à noite, e a mãe dele tinha posto o casaco na mala com ordem de usar. O tecido estava morno do corpo dele. Aurora sentiu o calor através da manga do vestido, no antebraço, antes de o casaco se afastar e o contato se desfazer. Meio segundo. Foi tudo. Aurora subiu para o quarto sem olhar para ele.', 1.0),
 ('i130', 'N', 'No quarto, se trocou sozinha: tinha pedido a Helle que ajudasse a prima primeiro. Trocou o vestido pela camisola. Escovou o cabelo. Tirou os brincos. Deitou. E ficou de olhos abertos, olhando o teto, o desenho de gesso que conhecia desde criança, a sombra do cortinado da cama que a vela projetava. Apagou a vela, e continuou olhando o teto no escuro. E pensou em três coisas, uma depois da outra. E em cada uma encontrou uma camada nova de incômodo.', 0.4),
 ('i131', 'N', 'Primeira: ele tinha rido aberto com Vibêke. Nunca tinha rido assim com ela, nem uma vez, em cinco meses. Por quê? Segunda: o sobretudo dele tinha roçado nela por meio segundo, e ela tinha sentido o calor através do vestido. Meio segundo era pouco. Mas era informação suficiente para o corpo dela continuar acordado, agora, na cama, no escuro. Terceira: ele tinha perguntado, na janela, se alguma coisa a incomodava. Ela disse que não. Ele disse que não era verdade. E depois disse uma frase que ainda estava no teto do quarto dela, e que ela não conseguia tirar dos olhos por mais que apagasse a vela: você ter motivo, ou não ter motivo, não muda o que você está sentindo.', 0.4),
 ('i132', 'N', 'Aurora virou na cama. Virou de novo. Sentou. Acendeu a vela. Levantou. Foi até a cômoda e abriu a primeira gaveta. Tirou um livro pequeno, de capa marrom gasta, com uma fita azul marcando as páginas trinta e sete e trinta e oito. Era um volume de poesia de Ólenchlêguer, o poeta dinamarquês, que tinha sido de Aráve. Aráve lia em voz alta no jardim, com gestos teatrais que faziam a mãe levantar uma sobrancelha. Aurora tinha tirado o livro da prateleira do escritório do pai duas semanas depois de a expedição não voltar. Tinha guardado na cômoda. Não tinha lido. Só guardado.', 0.4),
 ('i133', 'N', 'Naquela noite, segurou o livro com as duas mãos por um minuto. Olhou para a vela. Olhou para a porta. Pôs um xale sobre a camisola. Calçou os chinelos. Pegou a vela e o livro. E desceu, só de meias, pela escada que conhecia tão bem que sabia em que degrau pisar mais firme para ele não ranger. A casa estava em silêncio. Os pais no quarto, de porta fechada. A prima no quarto azul, de porta fechada. Josh no quarto dele, de porta fechada. Todos dormiam, ou ao menos estavam atrás de portas fechadas, o que para Aurora bastava.', 0.4),
 ('i134', 'N', 'Ela atravessou o corredor e entrou na sala de estar. Pousou a vela na mesinha lateral. Sentou no chão, ao lado da poltrona, com o xale nos ombros e o livro aberto no colo, na página da fita azul. E ficou ali. Sozinha. Lendo. À luz de uma vela só. Às doze e dez da noite.', 0.0),
]

RITMO_DIALOGO = 0.92
# pausa interna de fala de bloco: no máximo ~0,4 s (o "Por quê?" do i079 veio depois de um silêncio enorme)
SILENCIO_MAX = "silenceremove=stop_periods=-1:stop_duration=0.45:stop_threshold=-40dB:stop_silence=0.4"
import blocos18 as _B
# Vibêke e as senhoras voltam ao método do cap 17 (fala por fala, com prefixo): no bloco a voz da
# Vibêke ficava igual à da Aurora (autora, 19/11). Diálogo contínuo só nas cenas do Josh.
# só as falas do Josh vão em bloco (autora, 19/11): Eleonora/Aurora voltam a fala por fala
BLOCOS_USADOS = [k for k in _B.BLOCOS if k.startswith('B6')]
_P = {sl for k in BLOCOS_USADOS for sl,_,_ in _B.BLOCOS[k][1]}
_order=[x[0] for x in SEG]
# pausas do roteiro mantidas também entre falas de bloco (antes 0,05 s: diálogo atropelado — autora, 19/11)

if __name__ == "__main__":
    os.makedirs(BASE, exist_ok=True)
    parts = []
    for slug, vk, text, gap in SEG:
        seg_f = f"{BASE}/{slug}.seg.wav"; pf = f"{BASE}/{slug}_p.wav"
        if text.startswith("CLIP:"):
            ref = os.path.join(os.path.dirname(os.path.abspath(__file__)), {"josh_aurora_intenso": "ref-josh-aurora-intenso.wav", "josh_aurora": "josh_aurora.wav"}.get(text[5:], text[5:] + ".wav"))
            subprocess.run(["ffmpeg","-y","-i",ref,"-ac","1","-ar",str(SR),seg_f,"-loglevel","error"],check=True)
        if os.path.exists(seg_f):
            a = load(seg_f); src="cache"
            if slug in _P:  # fala de bloco: o diálogo contínuo sai depressa demais (autora, 19/11)
                a = apply_af(a, slug + "_lento", SILENCIO_MAX + ",atempo=" + str(RITMO_DIALOGO))
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
    sf.write(f"{SCR}/cap18-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap18-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-ar","44100","-codec:a","libmp3lame","-b:a","192k",
        f"{SCR}/cap18-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
