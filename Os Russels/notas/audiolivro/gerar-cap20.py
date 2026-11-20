import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = os.environ.get("GTTS_BASE", "/tmp/gtts") + "/gtts20"
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
INT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ref-josh-aurora-intenso.wav")
SEG = [
 # ---------- abertura ----------
 ('j001', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo vinte: A escuta.', 1.2),
 ('j002', 'N', 'Este capítulo volta aos olhos de Josh. No capítulo anterior, na madrugada depois do baile dos Lundgren, ele e Aurora se beijaram pela primeira vez, na sala, à luz de uma vela. E ele subiu sozinho para o quarto.', 0.8),
 ('j003', 'N', 'Josh não dormiu. Subiu para o quarto leste e deitou-se de costas, com o braço direito atravessado sobre o rosto, como se o braço fosse capaz de bloquear alguma coisa. Não bloqueou. A boca dela ainda estava nas pontas dos dedos dele. Morna, intacta. Ele ficou meia hora tentando esvaziar a cabeça. Não esvaziou.', 0.4),
 ('j004', 'N', 'A cabeça ficou onde tinha estado a noite inteira, em pedaços que ele não conseguia ordenar. Aurora perto demais, quente, o cheiro de jasmim e canela chegando antes do toque. O polegar dele encontrando, sem procurar, o ponto exato do pulso dela, sentindo a batida acelerar de um lado e a dele acelerar do outro. O primeiro suspiro dela escapando entre os lábios dele. E, quando a língua dele encontrou a dela e a mão subiu pela nuca, por baixo do cabelo solto, ele sentiu, com uma clareza assustadora, que a parte dele que queria continuar era muito mais funda do que a parte que sabia parar.', 0.3),
 ('j005', 'N', 'Tinha parado mesmo assim. Tinha tirado a boca antes que a boca o levasse. Tinha tirado a mão antes que a outra, a da cintura, quisesse subir. Tinha recuado um passo, e ouvido a própria respiração na sala como se tivesse corrido.', 0.5),
 ('j006', 'N', 'Ficou mais meia hora fazendo a única coisa que sabia fazer naquela noite: calcular. A frieza de contador que herdara da mãe, que ele costumava usar para pesar argumentos de filosofia, aplicada agora a si mesmo.', 0.3),
 ('j007', 'N', 'Eram três paredes. Ele as tinha dito a Aurora na madrugada, uma por uma. E duas continuavam de pé, exatamente onde estavam: a distância entre o que ela era e o que ele era, e o escândalo que cairia sobre o nome dela se alguém descobrisse. Essas duas eram razões. E razão não se trai: no máximo, se ignora. E ele não tinha ignorado nenhuma.', 0.4),
 ('j008', 'N', 'A primeira parede era outra coisa. Não era razão. Era confiança. A confiança de um homem que o tirara de uma fazenda na Zelândia e lhe dera um quarto, uma mesa, livros, e a promessa de um futuro que a mãe dele não tinha como pagar. E confiança não se ignora. Ou se trai, ou se honra. Não existe meio-termo.', 0.6),
 ('j009', 'N', 'Ele tinha traído.', 0.6),
 ('j010', 'N', 'E o pior, Josh pensou, de costas no escuro, era que o padrinho não saberia. Não havia testemunha. Não havia carta, recado, fofoca de criada. O que tinha acontecido na sala ficava entre ele e Aurora. O padrinho ia continuar tratando Josh como afilhado, ia continuar emprestando os livros com a própria mão, ia continuar dizendo: meu rapaz, com aquele orgulho contido. E Josh ia continuar recebendo tudo isso sabendo o que tinha feito. Era pior do que ser pego. Ser pego, pelo menos, acabava com a mentira.', 0.6),
 ('j011', 'N', 'Levantou-se às quatro e dez. Lavou o rosto na bacia. Tirou a camisa de gola alta do baile, amassada de uma noite de cama sem sono, e vestiu uma das camisas simples de algodão cru, a de gola baixa, a que lembrava as camisas da fazenda. Não calçou. A casa estava no silêncio mais fundo do dia, aquele que vem entre as três e as cinco, quando até os ratos da despensa decidem dormir. Josh desceu descalço.', 1.0),
 # ---------- a cozinha ----------
 ('j012', 'N', 'A cozinha estava fria. Fru Larsen, a cozinheira, não chegaria antes das seis e quarenta e cinco. Josh acendeu uma vela na mesa, moeu café para uma caneca no moedor de manivela, devagar, para o ruído não subir pela casa, e pôs a água no bule de ferro. Sentou-se no lado esquerdo da mesa de madeira bruta, no lugar que era, agora, oficialmente dele. Cinco meses de cozinha às horas em que ninguém estava acordado, e o lugar tinha sido absorvido pela rotina como se ele tivesse nascido sentando ali.', 0.3),
 ('j013', 'N', 'O café ferveu. Ele serviu, e ficou com a caneca quente entre as duas mãos. Foi nesse momento que ouviu os passos. Leves. Rápidos. Descalços. Josh reconheceu o som antes de qualquer outra coisa, porque era um som que ele tinha aprendido nos primeiros meses na Brédigueide sem nunca ter decidido aprender: os pés de Aurora no assoalho. Curtos e exatos, com uma pausa minúscula antes de cada apoio, como se ela calculasse o peso para o assoalho não denunciá-la. Passos de quem cresceu numa casa que escutava.', 0.3),
 ('j014', 'N', 'Ela apareceu na soleira. De camisola e roupão de algodão grosso, amarrado de qualquer jeito. Os cabelos soltos. E a primeira coisa que Josh viu, antes mesmo do rosto, foi a curva do ombro dela no vão do tecido frouxo, a clavícula à mostra, do mesmo jeito que estivera quatro horas antes, quando ele tinha encostado a boca ali. Josh desviou o olhar. Devagar. Devagar, para não ser dramático.', 0.3),
 ('j015', 'AU', 'Bom dia, Josh.', 0.2),
 ('j016', 'JOSH', 'Bom dia, Aurôra.', 0.3),
 ('j017', 'N', 'Ela atravessou a cozinha sem hesitar. Pegou a caneca dela, a azul de borda lascada, a que ninguém mais usava, tirou o café que sobrou no bule e sentou-se no lado direito da mesa. No lugar dela. Bebeu um gole. Pousou a caneca. E disse:', 0.2),
 ('j018', 'AU', 'Você não dormiu.', 0.2),
 ('j019', 'JOSH', 'Não consegui. Fiquei rolando na cama até desistir, e desci porque o quarto tinha ficado pequeno. É o que eu faço na fazenda quando não durmo. Desço antes de todo mundo. Lá tem o curral pra olhar, aqui tem a cozinha. Mas é a mesma coisa: sair de um teto que está perto demais.', 0.3),
 ('j020', 'N', 'Aurora deu o meio-sorriso pequeno, de lábios fechados, o que ela dava quando uma coincidência ficava grande demais para ser ignorada.', 0.2),
 ('j021', 'AU', 'Eu também não dormi. E eu desci porque imaginei que você ia estar aqui.', 0.4),
 ('j022', 'N', 'Josh sentiu uma coisa morna se acomodar entre as costelas. Ela tinha descido porque esperava encontrá-lo. Não comentou. Não deixou aparecer no rosto. Mas guardou, no lugar que reservava para as coisas que importavam. Aurora bebeu mais um gole, devagar, como quem ganha tempo para montar a primeira pergunta de verdade. E a pergunta veio:', 0.2),
 ('j023', 'AU', 'Por que você resolveu fazer faculdade, Josh?', 0.2),
 ('j024', 'JOSH', 'Como assim, Aurôra?', 0.2),
 ('j025', 'AU', 'Você é do campo. Nasceu no campo, cresceu no campo, sabe fazer as coisas do campo. Eu vi você consertar a pérgola com as próprias mãos, vi você falar de poda como especialista. A maioria dos homens que eu conheço nasceu pra ficar onde está. O Érik vai herdar as terras do pai. Os filhos dos Frederiksen vão herdar o nome. Você podia ter ficado na fazenda com os seus irmãos, e ninguém ia achar estranho. Mas você atravessou a Zelândia inteira pra estudar pra uma prova de ingresso numa universidade. Por quê? O que tem na academia que não tinha lá?', 0.3),
 ('j026', 'N', 'Josh ficou um tempo sem responder. Não porque não tivesse resposta. Porque ninguém nunca tinha feito aquela pergunta a ele. Aurora era a primeira.', 0.2),
 ('j027', 'JOSH', 'Tem o lugar. Na fazenda não sobra lugar pra mim, Aurôra. E eu não digo isso com mágoa, digo como quem faz uma conta. O Joseph é o mais velho, então ele dirige a propriedade. A Meridiana cuida da casa e do pomar, junto com a minha mãe. O Dylan vai ficar com a lida da terra, porque é bom nisso e gosta, mesmo fingindo que não gosta de nada. O Matias ainda é criança. E eu sou o do meio. O do meio não tem função óbvia. Se eu ficasse, ia passar a vida ocupando o lugar que sobrava do trabalho dos outros. Ia ser útil. Mas útil não é a mesma coisa que necessário. E um homem precisa de pelo menos um lugar onde ele seja necessário.', 0.3),
 ('j028', 'JOSH', 'A minha mãe viu isso antes de mim. Ela não me mandou fazer nada. Esperou que eu percebesse sozinho, porque ela é assim, não força ninguém a entender o que ela já sabe. Quando eu finalmente disse em voz alta que queria estudar, ela já tinha a solução pronta havia um ano. Escreveu pro seu pai. Ele é meu padrinho. Prometeu ao meu pai que cuidaria da educação de um dos filhos, se fizesse falta. E fez falta.', 0.4),
 ('j029', 'N', 'Aurora olhou para o chão. Ela sabia muito bem o que era não pertencer. Tinha vivido isso a vida inteira: a mestiça, com o sangue indiano visível no rosto, diferente de tudo o que a Dinamarca estava acostumada a ver. Disse, sem levantar os olhos:', 0.2),
 ('j030', 'AU', 'Eu entendo. É ruim quando a gente não pertence a um lugar. Eu sei bem como é. E o que você quer estudar?', 0.2),
 ('j031', 'JOSH', 'Eu gosto de entender como as coisas funcionam. Quando eu era menino, eu desmontava as coisas da fazenda só pra ver o que tinha dentro. O meu pai brigava, mas a minha mãe dizia pra ele deixar, porque eu ia montar de novo melhor do que estava. Lei, política, filosofia natural, é tudo a mesma coisa. Só que a coisa que eu desmonto agora é como os homens decidem viver juntos. E a Dinamarca está no meio dessa decisão. O seu pai acha que ela vai ter uma constituição antes de eu ficar velho. Eu quero estar na sala onde isso vai ser discutido. Não na plateia. Na sala.', 0.4),
 ('j032', 'N', 'Aurora o olhou diferente. Não com a avaliação de sempre. Com admiração, como se uma peça dele tivesse acabado de encaixar num lugar que estava vazio. E perguntou, mais devagar:', 0.2),
 ('j033', 'AU', 'Você é o primeiro da sua família a fazer faculdade, não é?', 0.2),
 ('j034', 'JOSH', 'Sou, sim. O primeiro.', 0.2),
 ('j035', 'AU', 'Você atravessou a Zelândia inteira sozinho pra abrir um caminho que ninguém da sua casa abriu antes. Sem ter quem te contasse como é. Eu sei que pra você isso pode parecer simples, Josh. Mas pra mim parece coragem.', 0.4),
 ('j036', 'N', 'Josh sentiu o sangue subir. Não estava habituado a ouvir a palavra coragem perto do próprio nome. Na fazenda, sair para estudar tinha sido o que lhe restava, e ele aprendera a chamar aquilo de necessidade. Aurora chamou de outro jeito, e o outro jeito o tocou. Um quase-sorriso subiu pela mandíbula dele. A palavra saiu mais rouca do que ele queria:', 0.2),
 ('j037', 'JOSH', 'Obrigado, Aurôra.', 0.3),
 ('j038', 'N', 'Ela não desviou os olhos. Sorriu curto. Não perguntou pela rouquidão. Josh percebeu que ela tinha notado, e que tinha decidido deixar passar.', 1.0),
 ('j039', 'N', 'Aurora levantou-se para fazer mais café. E Josh, sentado, olhou as costas dela com a liberdade de saber que ninguém ia entrar na cozinha pelos próximos quarenta minutos. Um luxo que ele não tinha tido em cinco meses: olhar para Aurora sem disfarçar. Olhou. Não disfarçou. E ela, que sentia um olhar nas costas como quem sente a temperatura mudar num cômodo, virou a cabeça meio de lado e o flagrou.', 0.2),
 ('j040', 'N', 'Os olhos dos dois se encontraram por um segundo inteiro, sem disfarce de nenhum dos lados. Josh viu a cor subir pelo pescoço dela, pelo lado direito primeiro, aquele rubor que ela não conseguia controlar, e que ele tinha aprendido a ler como o único relatório honesto que o corpo dela emitia. Foi Aurora quem voltou os olhos para o café primeiro. Não por vergonha. Para ter onde pôr o que aquele segundo tinha feito subir. Voltou com o bule. Encheu as duas canecas. Sentou. As orelhas dela ainda estavam vermelhas, e Josh teve que se segurar para não sorrir.', 0.3),
 ('j041', 'AU', 'Josh. Faz cinco meses que você mora nesta casa. Cinco meses sentando à mesa do meu pai, andando pelos mesmos corredores que eu, dividindo esta cozinha de madrugada. E eu sei três coisas sobre você. Que é afilhado do meu pai. Que veio de Sorô. E que veio estudar. Hoje, numa caneca de café, eu aprendi uma quarta: que você veio porque precisa de um lugar que seja seu desde o começo. Quatro coisas, Josh. Em cinco meses. Me fala da sua família. Eu quero te conhecer. Me fala dos seus irmãos.', 0.3),
 ('j042', 'N', 'Josh sorriu o sorriso abobado, como o irmão Dylan diria. Todas as amarras de Aurora pareciam ter se desfeito. Ela falava mais, sorria mais, e queria, de verdade, saber da vida dele. E não havia nada melhor que ele pudesse desejar.', 0.2),
 ('j043', 'JOSH', 'Claro. Vou começar pelo Joseph, o mais velho. Tem vinte e quatro. Assumiu a propriedade quando o meu pai morreu, sem reclamar uma vez sequer. O problema é que assumiu junto a ideia de que sentir é um luxo que o homem que carrega a casa não pode pagar. Então ele trabalha. Do escuro ao escuro. Porque enquanto trabalha, ele não pensa. E enquanto não pensa, não sente a falta do meu pai. Antes, o Joseph ria muito. Aprontava, namorava metade das moças da freguesia sem que nenhuma desconfiasse das outras. Depois parou. Não de tristeza. De responsabilidade.', 0.3),
 ('j044', 'N', 'Aurora perguntou com um cuidado especial. Josh entendeu de onde vinha o cuidado: ela estava perguntando do Joseph, mas pensando na cadeira de Aráve, o irmão que ela tinha perdido, na cabeceira da mesa de jantar da Brédigueide.', 0.2),
 ('j045', 'AU', 'E ele se senta na cadeira do seu pai?', 0.2),
 ('j046', 'JOSH', 'Não. Ninguém senta. A cadeira do meu pai continua na cabeceira, vazia, e ninguém nunca decidiu isso em voz alta. Simplesmente ninguém senta. A minha mãe passa a mão no encosto antes de sentar na cadeira dela, todo jantar, todo santo dia. Não é um gesto grande. É quase nada. Mas é a coisa mais constante daquela casa. O Joseph assumiu tudo. A lida, as contas, as decisões. Tudo, menos aquela cadeira.', 0.4),
 ('j047', 'N', 'Aurora ficou muito quieta. Por fim, disse:', 0.2),
 ('j048', 'AU', 'A gente também tem uma. A do Aráve. Na sala de jantar. Ninguém senta. Ninguém fala. O papai não olha pra ela o jantar inteiro, e o esforço de não olhar é mais barulhento do que se ele olhasse.', 0.2),
 ('j049', 'JOSH', 'Eu sei. Eu vi, no primeiro almoço. Ninguém me explicou. Não precisou.', 0.4),
 ('j050', 'N', 'Os dois ficaram em silêncio. E o silêncio agora tinha uma coisa nova: as duas casas, tão diferentes em tudo, guardavam o mesmo lugar vazio na mesma posição da mesa, com o mesmo acordo mudo em volta. Aurora foi a primeira a sair dele:', 0.2),
 ('j051', 'AU', 'Continua. O próximo.', 0.2),
 ('j052', 'JOSH', 'O Dylan. Dezenove. É o tipo que diz o que todo mundo na sala está pensando e ninguém vai dizer, com cara de quem está comentando o tempo. Tem um canivete que ele afiou tanto que a lâmina ficou mais fina que a do meu pai. Chuta a porteira do celeiro toda manhã, e nunca explicou pra ninguém por quê. É o mais difícil de gostar. E o mais fácil também, dependendo do dia.', 0.2),
 ('j053', 'AU', 'Você gosta dele?', 0.2),
 ('j054', 'JOSH', 'Eu adoro. Mas tenho que negar na frente dele, senão ele fica insuportável. O Dylan trata afeto como quem trata cachorro bravo: melhor não fazer movimento brusco.', 0.3),
 ('j055', 'N', 'Aurora riu. Um riso baixo, curto. Mas era um riso.', 0.3),
 ('j056', 'JOSH', 'A Meridiana tem vinte. É a filha do meio, e o nome vem disso. A minha mãe já sabia, antes de ela nascer, que ela ia ser a que segura o equilíbrio da casa. E a Meridiana fala com as árvores.', 0.2),
 ('j057', 'AU', 'Como assim, fala com as árvores?', 0.2),
 ('j058', 'JOSH', 'Fala. Tem uma macieira velha no pomar, perto do tanque, que ela chama de Berta. Conversa com a Berta como se a Berta respondesse. Conta o dia, pede opinião às vezes. A primeira vez, eu achei que era brincadeira de criança. Depois de uns anos entendi que não era. A Meridiana acha que árvore guarda memória. E essa é a parte que eu não conto pra qualquer um: depois de um tempo, eu comecei a achar que ela podia ter razão.', 0.3),
 ('j059', 'AU', 'Eu gostaria de conhecer a sua irmã.', 0.2),
 ('j060', 'JOSH', 'Vocês iam se dar bem. Acho até que iam ser amigas rápido. A Meridiana ia gostar de você.', 0.2),
 ('j061', 'AU', 'Você acha? Por quê?', 0.2),
 ('j062', 'JOSH', 'Porque vocês escolhem o que dizem. Nenhuma das duas fala sem pensar. A diferença é que você aprendeu cedo a guardar silêncio porque o silêncio te protege. Você é a única numa rua inteira de Copenhague com o sangue indiano visível no rosto, e desde criança aprendeu que ser notada cobra um preço. O silêncio da Meridiana é outro. Ela é calada porque a fazenda é calada. Vocês iam reconhecer uma na outra o que falta e o que sobra. É disso que nascem as amizades que prestam.', 0.4),
 ('j063', 'N', 'Josh viu o rosto dela mudar de leve, e percebeu, com um pequeno atraso, que tinha dito em voz alta uma coisa que ela talvez nunca tivesse ouvido: que o silêncio dela era proteção. Não voltou atrás. A frase era verdadeira, e Aurora não a recusou. Bebeu. Pousou a caneca.', 0.2),
 ('j064', 'AU', 'Tem mais irmãos?', 0.2),
 ('j065', 'JOSH', 'O caçula, o Matias. Treze anos. É a parte da minha família que ainda não aprendeu a esconder o que sente, e a gente protege ele desse aprendizado o quanto pode. Chora num livro triste sem vergonha nenhuma. Faz pergunta de menino com a profundidade de quem tem trinta anos. Pergunta da morte, do tempo, de Deus. O Matias é a razão de eu ter aprendido a responder pergunta difícil sem mentir. Porque com ele não dá. Ele percebe na hora, e fica magoado. Não com a verdade. Com a tentativa de pouparem ele dela.', 0.3),
 ('j066', 'N', 'Aurora o olhava com uma expressão que ele demorou a nomear. Era inveja. Não a feia. A inveja mansa de quem cresceu sem irmãos pequenos e ouve falar de uma casa cheia.', 0.2),
 ('j067', 'AU', 'E a sua mãe? A comadre do papai.', 0.2),
 ('j068', 'JOSH', 'A minha mãe é a pessoa mais difícil de descrever numa frase que eu conheço. Eu vou precisar de mais café pra começar.', 0.3),
 ('j069', 'N', 'Aurora encheu a caneca dele.', 0.2),
 ('j070', 'JOSH', 'Ela me escreve toda semana. Desde que eu cheguei, em março, não passou uma semana sem carta. Escreve do joelho do Joseph, que está ruim de novo. Do Dylan, que ainda não consertou a cerca do pasto norte, porque o Dylan nunca faz nada antes da terceira vez que pedem. Dos vizinhos, do preço do trigo, de um gato que apareceu na cozinha e que ninguém teve coragem de tirar. Conta tudo. Menos dela. Eu pergunto como ela está. Se a dor nas costas voltou. Ela responde de lado, ou não responde. Diz: estou bem, e passa pro próximo parágrafo.', 0.3),
 ('j071', 'N', 'Aurora riu pelo nariz, baixinho.', 0.2),
 ('j072', 'JOSH', 'Ela leva tudo pra dentro pra não pôr nos outros. E é a única pessoa daquela casa que sabe puxar a orelha do Dylan na hora certa, e sabe quando o Matias precisa ser deixado em paz. Eu cresci ouvindo conselho dela disfarçado de comentário. Ela nunca dizia: faz isso. Dizia: olha, o vizinho pôs o filho mais novo pra cuidar do estábulo, e o estábulo melhorou. E era ela me mandando tomar conta da minha parte. Eu só entendi lá pelos dezenove anos. E percebi que ela tinha me criado inteiro desse jeito, sem eu ver.', 0.4),
 ('j073', 'N', 'Josh ficou um tempo olhando para a caneca.', 0.2),
 ('j074', 'JOSH', 'Você ia gostar dela, Aurôra.', 0.3),
 ('j075', 'N', 'Aurora sorriu.', 1.0),
 ('j076', 'N', 'Em algum momento, Josh contou da morte do pai, Henrik. Não em detalhe. O suficiente: a febre, três semanas, o quarto fechado, a janela aberta de um lado só. Matias com nove anos, ele com dezessete, Joseph com vinte. O pai que reconstruíra o telhado de palha da casa três vezes com as próprias mãos. E a mãe carregando o luto da casa inteira nas costas sem deixar ninguém ver o peso. Aurora ouviu sem interromper, com a mão em volta da caneca. Quando ele terminou, ela perguntou:', 0.2),
 ('j077', 'AU', 'Você quer saber do Aráve?', 0.2),
 ('j078', 'JOSH', 'Claro que quero. Mas quero saber o que você quiser me contar dele. Não mais do que isso.', 0.4),
 ('j079', 'N', 'Aurora respirou. E contou. Contou do jardim primeiro: o retângulo de verde e pedra nos fundos da casa, fechado por muros de hera, com o caminho de cascalho branco que levava à pérgola coberta de glicínias. As roseiras do canto direito, que tinham sido ideia do Aráve. Ele convencera o pai a importar as mudas da Jutlândia, e dissera, com aquela mania de transformar qualquer coisa em frase: rosas dinamarquesas em solo dinamarquês, plantadas por mãos indianas.', 0.3),
 ('j080', 'N', 'Contou que o Aráve lia o Oxêlenguer em voz alta no jardim, com gestos de teatro, e que a mãe levantava uma sobrancelha, fingindo achar exagero, enquanto o pai escondia um sorriso atrás do jornal. Que ela cresceu achando que o mundo inteiro falava assim, em poesia, e só descobriu que não quando ele se foi, e tudo em volta virou prosa de uma hora para a outra. Contou da expedição. O navio. A rota do Ceilão. O irmão embarcando porque queria ver com os próprios olhos a terra de onde a família do pai tinha vindo. E contou do dia da notícia. A voz dela ficou mais grave, mas não tremeu:', 0.2),
 ('j081', 'AU', 'Chegou num envelope preto. Um oficial da Marinha Real trouxe. Era um homem grande, fardado, e ele não conseguiu olhar pro rosto do meu pai na hora de entregar. Eu lembro disso mais do que de qualquer outra coisa: o homem grande encolhido, sem coragem de levantar os olhos. Lembro do som do envelope sendo aberto. Do silêncio do meu pai, que foi pior do que qualquer barulho. E lembro do grito da minha mãe. Um grito só. Agudo, curto. A minha mãe, que controla cada músculo do rosto, deu um grito que pareceu rasgar o mundo. Eu nunca mais ouvi ela fazer um som parecido. E eu sei que nunca vou esquecer aquele.', 0.4),
 ('j082', 'N', 'Josh não disse nada de imediato. Não preencheu o silêncio com consolo, porque consolo, ali, seria tirar dela uma coisa que era dela. Esperou o tempo que a frase pedia. Depois falou:', 0.2),
 ('j083', 'JOSH', 'A minha casa soube da morte do meu pai do lado da cama dele. Três semanas de febre, e no fim eu segurando a mão dele, sentindo o instante exato em que aquela mão parou de ser mão e virou só peso. A sua casa soube por um oficial e um envelope preto. São jeitos diferentes da mesma coisa chegar. Mas o que vem depois é igual nas duas. A casa que sempre tem alguém faltando. A cadeira que ninguém senta. A mãe carregando o luto de todo mundo sem deixar ver. Eu te entendo, Aurôra, porque eu carrego a mesma coisa. Não a sua. A sua é sua. Mas eu sei como o ar de uma casa muda quando ela passa a ter um lugar que ninguém quer preencher.', 0.4),
 ('j084', 'N', 'Aurora segurou o olhar dele. Os olhos marejaram. Ela piscou depressa, duas vezes, sem deixar a lágrima cair. Respirou fundo. E, quando voltou a falar, a voz estava limpa:', 0.2),
 ('j085', 'AU', 'Josh? Eu não quero falar do que aconteceu hoje de madrugada. Não agora, não nesta cozinha, com a Helle prestes a chegar e a casa prestes a acordar. Mas eu preciso que você entenda uma coisa, e que entenda direito, sem aquela sua mania de transformar o que eu digo em outra coisa mais segura. Eu não me arrependo. Não foi um erro que eu queira corrigir. Não foi um momento que eu queira fingir que não aconteceu. As suas paredes continuam de pé, eu sei. Mas elas são suas. O que eu sinto é meu. E eu não vou pedir desculpa por uma coisa que é minha.', 0.4),
 ('j086', 'N', 'Josh ficou olhando para ela. Dessa vez, não procurou a saída segura. Deixou a frase dela inteira no ar, e respondeu inteiro:', 0.2),
 ('j087', 'JOSH', 'Eu também não me arrependo.', 0.4),
 ('j088', 'N', 'A mão dele estava aberta em cima da mesa. A dela também, do outro lado, e a distância entre as duas era curta. Josh viu a distância. Não fechou a mão.', 0.2),
 ('j089', 'JOSH', 'E é aí que está o meu problema, Aurôra. Porque seria muito mais fácil se eu me arrependesse. Se eu acordasse hoje achando que foi um erro, eu saberia o que fazer. Erro a gente conserta. Eu sei consertar quase tudo. Mas isso não foi erro. E eu não tenho ferramenta pra uma coisa que não está quebrada, e que mesmo assim não pode existir.', 0.3),
 ('j090', 'N', 'Ele obrigou a própria mão a recuar. Meio centímetro. Só o suficiente para saber que tinha recuado.', 0.2),
 ('j091', 'JOSH', 'Então não, eu não vou desfazer. Eu não consigo. Eu só não sei ainda o que se faz com uma coisa que a gente não desfaz e não pode ter. Quando eu souber, eu te digo.', 0.4),
 ('j092', 'N', 'Foi a coisa mais sem filtro que ele tinha dito desde que ela descera. Aurora recebeu cada palavra sem interromper, e assentiu uma vez, devagar. Não era concordância. Era recebimento.', 0.3),
 ('j093', 'N', 'Por um instante, nenhum dos dois se mexeu. A vela estava quase no fim, e a cozinha tão silenciosa que dava para ouvir a cera escorrer. Josh olhou para a boca dela. Uma vez, meio segundo, o tempo exato de saber que tinha olhado. E desviou. Bastava levantar, contornar a mesa, dar três passos. Ele sabia o número. Sabia que não ia dar nenhum. E aprendeu, ali sentado, que querer e não fazer pesavam, e que ele ia ter de carregar isso sozinho.', 0.3),
 ('j094', 'N', 'A porta da frente abriu às seis e dezessete. Era Helle, a criada. Aurora levantou-se primeiro, lavou a caneca no balde e a virou de boca para baixo no escorredor. Josh fez o mesmo.', 0.2),
 ('j095', 'AU', 'Eu vou subir. Antes da Helle chegar na cozinha.', 0.2),
 ('j096', 'JOSH', 'Vai, sim. Pode ir.', 0.3),
 ('j097', 'N', 'Ela passou perto dele na saída. Não o tocou. Mas passou perto o bastante para o cheiro dela chegar: jasmim e canela, um cheiro que não combinava com a Dinamarca, nem com agosto, e que tinha grudado na memória dele desde o primeiro dia, como tinta em tecido branco. Naquela manhã veio mais fundo, mais quente, misturado ao morno da cama que ela tinha acabado de deixar.', 0.2),
 ('j098', 'N', 'Josh fechou os olhos por meio segundo. E o que o corpo dele queria, naquele escuro de pálpebra, era simples e inteiro: virar, alcançar o pulso dela antes que ela cruzasse a porta, puxá-la de volta, e recomeçar o que a madrugada tinha começado. Ele não virou. Ficou imóvel, as mãos abertas ao longo do corpo. Antes daquela madrugada, ele só tinha imaginado como seria tocar Aurora. Agora tinha provado. E provar, ele descobria ali, era muito pior do que imaginar. Porque o que a gente imagina, ainda consegue negar. O que o corpo já descobriu, não.', 0.4),
 ('j099', 'N', 'Aurora saiu. Josh ficou na cozinha mais um minuto. Olhou para a vela. Apagou. Subiu.', 1.2),
 # ---------- a biblioteca ----------
 ('j100', 'N', 'Às nove da manhã, a biblioteca era o lugar mais silencioso da casa. Fru Larsen estava na cozinha, Helle na sala de jantar, Aurora na sala de costura, na aula de francês com Fru Dahl. Eleonora, a mãe de Aurora, resolvia o que precisava resolver. E Raj, o padrinho, estava no escritório, atrás de cartas e contas. Naquele intervalo, a biblioteca era de Josh.', 0.3),
 ('j101', 'N', 'Ele foi até a estante grande do canto leste. Ela ficava perpendicular à janela, e criava, entre ela e a parede, um corredorzinho de uns dois metros, onde Josh se acostumara a sentar no chão com o livro do dia. Da porta, não dava para ver quem estivesse ali. Ele tinha descoberto isso no segundo mês, e guardado a descoberta como quem guarda um esconderijo de infância.', 0.3),
 ('j102', 'N', 'Sentou no canto e abriu o tratado de Grôcius, sobre o direito da guerra e da paz, que o padrinho tinha posto na lista da semana. Leu a primeira página. Leu de novo. Não absorveu uma palavra. A cabeça estava na cozinha, no rubor subindo pelo pescoço dela, na frase: o que eu sinto é meu. E, mais atrás, na sala da madrugada. Foi nesse momento que a porta da biblioteca se abriu.', 0.3),
 ('j103', 'N', 'Não foi um abrir cuidadoso. Foi o de quem entra num cômodo sem reparar se já tem alguém dentro, porque tem a cabeça em outra coisa. Os passos firmes do padrinho, de sapato. Atrás deles, os passos mais leves de Eleonora. E a voz dela, já no meio de uma frase, num tom que Josh nunca tinha ouvido nela:', 0.2),
 ('j104', 'EL', ELP+'E eu não vou deixar esse assunto morrer porque você decidiu que ele é desconfortável, Ráge.', 0.3),
 ('j105', 'N', 'Josh ficou imóvel. O certo era levantar e se apresentar. Mas, antes que ele se mexesse, entendeu que aquilo era a continuação de uma discussão começada em outro cômodo. Os dois falavam alto. O ânimo tinha passado na frente da prudência. Levantar agora era anunciar que tinha escolhido ficar. Josh ficou imóvel. E, ao ficar, escolheu. E soube que tinha escolhido. O padrinho disse, contido:', 0.2),
 ('j106', 'RAJ', 'Eleonora. Este não é o lugar pra essa conversa.', 0.2),
 ('j107', 'EL', ELP+'A nossa casa não tem lugar pra essa conversa. Na verdade, ela nem devia existir, Ráge. Foi você que fez ela existir, no dia em que apertou a mão do Lindberg. Agora ela existe. E nós dois temos que decidir o que fazer com a Aurora antes que ela comece a existir pra ela também.', 0.3),
 ('j108', 'N', 'Lindberg. Josh já tinha ouvido aquele nome uma vez, no escritório, numa frase solta do padrinho sobre rotas marítimas.', 0.2),
 ('j109', 'RAJ', 'A Aurora não tem nada com isso.', 0.2),
 ('j110', 'EL', ELP+'A Aurora vai ter tudo com isso se ficar nesta casa nas próximas semanas. Você vai receber o Lindberg aqui. Vai receber os homens dele. Vai ter conversa de devedor e credor na sua biblioteca, na sua sala de jantar, com números em cima da mesa e tom de quem está perdendo. Eles vão ameaçar a sua vida se você não garantir que vai pagar a dívida. E a Aurora tem os olhos mais afiados desta casa, e os ouvidos mais apurados. Ela vai entender em três dias. E aí, Ráge, me escuta bem: ela não vai ficar só com medo. Ela vai querer ajudar.', 0.3),
 ('j111', 'N', 'Josh ouviu o padrinho sentar. A poltrona perto da janela estalou de leve.', 0.2),
 ('j112', 'RAJ', 'Ela é uma menina.', 0.2),
 ('j113', 'EL', ELP+'Ela é uma menina que já enterrou um irmão, e que assistiu, calada, o pai se despedaçar de luto. Você acha que ela vai assistir de braços cruzados a casa ruir uma segunda vez? Ela vai se oferecer, Ráge. Vai chegar pra você com aquela cara de porcelana e dizer que aceita casar com quem for preciso. Com o Lindberg, com um sócio dele, com qualquer homem velho e rico que feche a conta. Ela vai se vender pra salvar você, e vai chamar isso de dever. Eu não vou deixar a nossa filha chegar nesse ponto. Eu prefiro que ela não saiba de nada.', 0.3),
 ('j114', 'N', 'Atrás da estante, Josh fechou os olhos por um segundo. Estava ouvindo o que não tinha permissão de ouvir. E estava ouvindo Eleonora, a dos bordados e do meio-sorriso, brigar por uma coisa com uma ferocidade que ele nunca tinha visto nela. O padrinho falou, cansado:', 0.2),
 ('j115', 'RAJ', 'Então o que você sugere? Porque o que está em jogo é simples: a casa não pode ter a Aurora dentro enquanto eu negocio. Eu preciso dela longe daqui por umas duas semanas, sem que ela saiba por quê. A pergunta é: pra onde?', 0.2),
 ('j116', 'EL', ELP+'Eu sei qual é a pergunta.', 0.2),
 ('j117', 'RAJ', 'Então me ajuda a responder, em vez de só me dizer onde ela não pode ir. Pros Mortensen?', 0.2),
 ('j118', 'EL', ELP+'Pros Mortensen, não.', 0.2),
 ('j119', 'RAJ', 'Por quê? O Érik visita ela às quartas. A família é boa. Ele parece ter interesse sincero em noivar com a Aurora. E a Ingrid é o mais perto de uma amiga que a Aurora tem.', 0.2),
 ('j120', 'EL', ELP+'Por isso mesmo. O Érik é pretendente, sem nada firmado. E ela não vai aceitar, e você sabe disso. Manda a nossa filha solteira dormir duas semanas debaixo do teto do pretendente, e a cidade lê de dois jeitos. Ou estamos empurrando o noivado goela abaixo, ou tiramos a Aurora de casa às pressas, e o motivo mais provável seria uma gravidez antes do casamento. Uma leitura humilha ela. A outra denuncia você. As duas são veneno.', 0.3),
 ('j121', 'RAJ', 'Os Lundgren, então.', 0.2),
 ('j122', 'EL', ELP+'A senhora Lundgren me adora, mas tem três filhas casadeiras e nenhum canto pra uma quarta moça. E mora a vinte minutos daqui. Vinte minutos não é distância, Ráge.', 0.2),
 ('j123', 'RAJ', 'A Karoline.', 0.2),
 ('j124', 'N', 'Karoline, a irmã de Eleonora, mãe de Vibêke. Eleonora soltou o ar:', 0.2),
 ('j125', 'EL', ELP+'A Karoline me mandou a Vibêke pra conhecer outros rapazes antes de fechar o noivado com o tal Lauritz, que ela não engole. Esse é o acordo. Se eu devolvo a Vibêke pra Viborg com a Aurora junto, no meio da temporada, sem explicação, a Karoline entende na hora que aconteceu coisa grave aqui. E a Karoline não guarda segredo nem da própria sombra. Em uma semana, meia Jutlândia está adivinhando o motivo.', 0.3),
 ('j126', 'RAJ', 'Então, o que sobra?', 0.4),
 ('j127', 'EL', ELP+'Eu não sei o que sobra. Eu só sei o que não dá.', 0.3),
 ('j128', 'N', 'Foi então que o padrinho falou o nome, quase no automático, rodando a lista na cabeça e caindo nele por exclusão:', 0.2),
 ('j129', 'RAJ', 'Os Rássel.', 0.5),
 ('j130', 'N', 'Atrás da estante, Josh parou de respirar. A casa dele. Eleonora demorou a responder. E respondeu num tom que Josh decifrou na hora: o de quem ouve uma proposta que cabe na conta e que, ao mesmo tempo, esbarra num desconforto que ela não sabe nomear.', 0.2),
 ('j131', 'EL', ELP+'Sorô?', 0.2),
 ('j132', 'RAJ', 'Sim! É perfeito. A propriedade da Casandra. Duas semanas. A Aurora e a Vibêke juntas, a Vibêke como acompanhante natural. A Casandra recebe as duas como sobrinhas. O Josh acompanha. O pretexto se sustenta sozinho: convite de campo de uma amiga antiga, ar puro depois da temporada. A casa fica livre aqui. Eu negocio com o Lindberg sem a Aurora ouvir uma palavra. Em duas semanas elas voltam, e ela não soube de nada.', 0.3),
 ('j133', 'N', 'As palavras chegaram fora de ordem para Josh, e levaram um instante para se juntarem no sentido que ele não queria que tivessem. Aurora ia para Sorô. Para a casa dele, a da mãe, Casandra. Para debaixo do telhado de palha onde ele era o filho do meio e não o aluno do padrinho, onde se andava descalço e se falava alto, e não havia uma única parede de cidade atrás da qual se esconder. E ele iria junto.', 0.2),
 ('j134', 'N', 'A parte dele que devia sentir pavor sentiu na hora: era a pior coisa que os dois podiam ter decidido, e tinham decidido sem fazer ideia do que decidiam. Mas, debaixo do pavor, antes que ele tivesse tempo de proibir, subiu outra coisa. Quente, sem vergonha, viva. A mesma que ele tinha passado a madrugada jurando a Aurora que continuava trancada atrás das paredes. Essa coisa ouviu: duas semanas, e não sentiu pavor nenhum. Teve vontade de sorrir. E Josh, no escuro atrás da estante, precisou apertar o maxilar para não deixar.', 0.3),
 ('j135', 'N', 'Eleonora chamou o marido, num tom baixo, quase como se dissesse uma palavra feia:', 0.2),
 ('j136', 'EL', ELP+'Ráge. Sorô é a casa do Josh.', 0.2),
 ('j137', 'RAJ', 'Eu sei. E qual é o problema? Sorô é a casa da Casandra. O Josh é afilhado. A Casandra é uma viúva responsável, com cinco filhos e uma propriedade. Tem a Meridiana lá, tem a própria Casandra, tem criadagem. A Aurora vai estar mais cercada de gente séria lá do que em qualquer baile da temporada. Você tem alguma objeção?', 0.2),
 ('j138', 'EL', ELP+'Não. Eu não tenho nenhuma objeção.', 0.2),
 ('j139', 'RAJ', 'Então qual é o problema?', 0.2),
 ('j140', 'EL', ELP+'Não é problema. É desconforto. E não, eu não sei explicar. Então não me peça pra explicar como se fosse uma conta, porque não é uma conta.', 0.2),
 ('j141', 'RAJ', 'Eleonora, você sempre tem um motivo. Diga de uma vez!', 0.3),
 ('j142', 'N', 'A resposta dela veio mais lenta:', 0.2),
 ('j143', 'EL', ELP+'Dessa vez, eu tenho um pressentimento. Eu sei que você não trabalha com pressentimento. Eu também não. Mas eu conheço a minha filha melhor do que conheço qualquer pessoa viva. E a minha filha anda diferente, Ráge. Diferente nas pausas. No tempo que ela leva pra responder uma pergunta simples. No jeito que ela olha pra certas portas desta casa. Não as portas de onde nós saímos. As portas de onde um certo rapaz sai. Eu não sei dizer o que é. Mas mandar ela pra duas semanas no campo, longe do meu olho, me deixa com uma coisa atravessada no peito.', 0.4),
 ('j144', 'RAJ', 'Você viu alguma coisa concreta?', 0.2),
 ('j145', 'EL', ELP+'Não. Nada que eu consiga apontar.', 0.2),
 ('j146', 'RAJ', 'Então é a temporada. É a Vibêke chegando. São três bailes em dez dias, e o primeiro debute dela. Tudo isso explica, Eleonora.', 0.2),
 ('j147', 'EL', ELP+'Pode ser. Talvez seja.', 0.2),
 ('j148', 'RAJ', 'Eu preciso que seja. Porque eu não tenho outra opção em cima da mesa.', 0.2),
 ('j149', 'EL', ELP+'Eu sei. Eu não estou te pedindo pra mudar de ideia. Estou te pedindo pra registrar, na sua decisão, que eu não estou tranquila. Só isso. Que conste.', 0.2),
 ('j150', 'RAJ', 'Consta. Mas a decisão continua sendo Sorô.', 0.4),
 ('j151', 'N', 'Foi nesse momento que a perna direita de Josh, dobrada havia mais de quarenta minutos atrás da estante, começou a tremer, com aquela formigação de músculo parado tempo demais. Ele tentou conter. Não conteve. O calcanhar bateu de leve no rodapé da estante, e o som, pequeno, mas existente, atravessou a sala. Silêncio. E o padrinho disse, não como pergunta:', 0.2),
 ('j152', 'RAJ', 'Tem alguém aí.', 0.5),
 ('j153', 'N', 'Josh pensou, por dois segundos, na porta lateral atrás da estante, a do corredor de serviço. Pensou e descartou. Sair escondido depois de ter ouvido tudo era transformar um acidente numa mentira. E mentira era a única coisa que ele não ia acrescentar àquela situação. Levantou-se. Saiu de trás da estante, com as duas mãos abertas ao lado do corpo, desarmado.', 0.2),
 ('j154', 'JOSH', 'Sou eu, padrinho.', 0.3),
 ('j155', 'N', 'O padrinho parou. Eleonora pôs a mão na beirada do encosto do sofá, e não a tirou.', 0.2),
 ('j156', 'RAJ', 'Josh. Há quanto tempo você está aí?', 0.2),
 ('j157', 'JOSH', 'Desde antes de o senhor e a senhora entrarem. Uns quarenta minutos. Eu vim ler o Grôcius no canto onde eu costumo ler, e quando os senhores entraram eu já estava sentado. Eu devia ter me levantado e me anunciado no primeiro instante. Não me levantei. A primeira frase da senhora deixou claro que era assunto particular, e eu travei entre interromper e aparecer, e a hesitação durou tempo demais até virar escolha. A escolha foi errada. A culpa é minha. Inteira. E eu não vou tentar diminuir.', 0.3),
 ('j158', 'RAJ', 'Você ouviu tudo?', 0.2),
 ('j159', 'JOSH', 'Ouvi tudo. O Lindberg. A dívida. Sorô. Os motivos de cada casa descartada. Eu podia dizer ao senhor que cheguei agora, que não ouvi nada, e o senhor não teria como saber. Mas eu prefiro que o senhor saiba exatamente o que eu sei. Ouvi tudo.', 0.3),
 ('j160', 'N', 'Josh viu o queixo do padrinho se contrair de leve: o gesto de quem recalcula uma rota interrompida por uma variável nova.', 0.2),
 ('j161', 'RAJ', 'Senta.', 0.3),
 ('j162', 'N', 'Josh sentou no sofá. O padrinho, na poltrona em frente. Eleonora ficou de pé atrás da poltrona do marido, com a mão no encosto, como quem monta guarda.', 0.2),
 ('j163', 'RAJ', 'Josh. Você acaba de saber duas coisas que não eram pra você saber. A dívida do Lindberg, e a minha intenção de mandar a Aurora pra Sorô. Sobre a primeira, eu vou te explicar o suficiente pra você não levar informação pela metade pra Casandra. Mas depois, não agora. Agora eu preciso de uma resposta sua. E preciso que ela seja verdadeira, porque você acabou de me mostrar que diz a verdade mesmo quando ela te custa.', 0.2),
 ('j164', 'JOSH', 'Pode perguntar, padrinho.', 0.2),
 ('j165', 'RAJ', 'Você leva a Aurora e a Vibêke pra Sorô, e me garante, com a sua palavra, que as duas voltam exatamente como saíram daqui?', 0.5),
 ('j166', 'N', 'A pergunta caiu na sala como uma vela trocada. Josh ouviu o peso embaixo dela. E percebeu, pelo canto do olho, que Eleonora tinha endurecido o ombro um milímetro com aquela formulação. Ele respondeu com a única verdade que podia dar sem mentir e sem se condenar:', 0.2),
 ('j167', 'JOSH', 'Padrinho, eu levo a Aurora e a Vibêke pra Sorô, e trato as duas como a casa da minha mãe trata quem entra como hóspede. A minha mãe é uma mulher séria. Os meus irmãos são gente decente. A minha mãe vai receber as duas com o cuidado que daria a parentes. E eu respondo pelas duas com a minha palavra. Que é a única coisa que eu tenho pra dar, e a única coisa que eu nunca dei à toa.', 0.4),
 ('j168', 'N', 'Não disse: minha palavra de homem. Disse a palavra dele, sem adjetivo. O padrinho olhou para Eleonora. Ela não falou, mas Josh viu o queixo dela se mexer, na versão dela de: anotado, plano em revisão. O padrinho voltou-se para Josh, com um pequeno brilho de admiração nos olhos. Mas, como pai, precisava de mais:', 0.2),
 ('j169', 'RAJ', 'Os seus irmãos.', 0.2),
 ('j170', 'JOSH', 'Pode perguntar dos três.', 0.2),
 ('j171', 'RAJ', 'O Joseph.', 0.2),
 ('j172', 'JOSH', 'Tem vinte e quatro anos. Sério, responsável. Não vai chegar perto da Aurora. E se chegasse, seria pra perguntar se ela precisa de mais lenha na lareira.', 0.2),
 ('j173', 'RAJ', 'O Dylan. Atrevido, eu já te ouvi dizer.', 0.2),
 ('j174', 'N', 'Josh fez uma pausa de meio segundo.', 0.2),
 ('j175', 'JOSH', 'O Dylan vai provocar. É o jeito dele de existir no mundo. Mas provocar é o limite, e ele sabe disso. Se ele passar um dedo do que a cortesia permite, ele responde a mim antes de responder a qualquer um. E ele me conhece o bastante pra não querer descobrir até onde isso vai. A Aurora está mais segura do Dylan do que estaria de metade dos cavalheiros que ela cumprimentou na temporada.', 0.2),
 ('j176', 'RAJ', 'O Matias.', 0.2),
 ('j177', 'JOSH', 'Treze anos. O caçula. Vai virar amigo das duas antes do segundo dia, e vai mostrar pra Aurora a coleção de poesia do meu pai sem que ninguém peça.', 0.2),
 ('j178', 'RAJ', 'E tem a sua irmã.', 0.2),
 ('j179', 'JOSH', 'A Meridiana. Vinte anos. Essa é a parte que talvez o senhor nem precisasse perguntar, padrinho, mas que importa mais do que as outras. A Aurora não vai estar sozinha num lugar cheio de homens. Vai ter uma moça da idade dela na casa, do lado dela, o tempo todo. A Meridiana vai cuidar da Aurora antes mesmo de alguém pedir. É o que ela faz com tudo que chega na fazenda precisando de cuidado.', 0.4),
 ('j180', 'N', 'O padrinho sustentou o olhar dele mais um tempo. Depois assentiu. O assentimento curto de decisão tomada.', 0.2),
 ('j181', 'RAJ', 'Ótimo. Eu escrevo pra Casandra hoje, com o convite e os preparativos. As meninas saem na segunda de manhã. Vocês ficam duas semanas. Eu mando um recado pra Karoline avisando que a Vibêke vai conhecer um pouco da Zelândia antes de voltar. E você, Eleonora, cuida de fazer a história circular do jeito certo. Uma palavra pra senhora Lundgren no chá de quinta, como quem comenta de passagem que a Aurora aceitou um convite de campo, e em dois dias a cidade inteira sabe a história que a gente quer que ela saiba.', 0.2),
 ('j182', 'EL', ELP+'Eu cuido disso.', 0.3),
 ('j183', 'N', 'Foi a primeira concordância dela na conversa inteira. E veio sem entusiasmo. O padrinho chamou Josh mais uma vez, com uma atenção nova:', 0.2),
 ('j184', 'RAJ', 'Josh. Mais uma coisa. Você podia ter mentido agora há pouco. Eu perguntei há quanto tempo você estava aí, e você podia ter encolhido a verdade pela metade, dito que pegou só o fim, e eu ia acreditar. Você não fez isso. Você me disse que ouviu tudo, sabendo que aquilo te punha numa posição pior. Eu confio em pouca gente, Josh. E menos ainda em homem jovem. Mas é exatamente o que você acabou de fazer que me faz confiar em você pra essa viagem. Não esquece disso.', 0.3),
 ('j185', 'N', 'Josh sentiu o sangue subir no rosto. Não era vergonha. Era peso. Porque o padrinho estava confiando nele exatamente pela qualidade que ele tinha traído quatro horas antes. E o elogio caiu sobre a consciência dele como sal em corte.', 0.2),
 ('j186', 'JOSH', 'Padrinho, dizer a verdade ali não teve mérito nenhum. Foi só o que dava pra fazer.', 0.2),
 ('j187', 'RAJ', 'Tem gente que não acha que dá. Por isso eu reparei.', 0.3),
 ('j188', 'N', 'O padrinho levantou-se e estendeu a mão. Josh a apertou. Eleonora não se mexeu. Continuou com a mão no encosto da poltrona, olhando para Josh, calada. E, ao se virar para sair, Josh encontrou os olhos da madrinha por meio segundo, e leu neles uma frase que ela jamais diria em voz alta: eu não te conheço tão bem quanto eu pensava. E eu vou prestar atenção.', 0.3),
 ('j189', 'N', 'Josh assentiu de leve para ela, sem que o padrinho visse. Era a resposta possível: eu sei que a senhora desconfia de alguma coisa. Eu não vou explicar. E a senhora vai esperar. Eleonora não devolveu o gesto. Josh saiu da biblioteca, fechou a porta sem fazer barulho, e subiu para o quarto leste.', 1.2),
 # ---------- a carta ----------
 ('j190', 'N', 'O quarto leste estava na luz pálida do meio da manhã. Josh sentou-se à escrivaninha. Pegou papel limpo, pena, tinteiro. A pena ficou encostada na folha uns vinte segundos sem produzir letra. O padrinho ia escrever a carta de verdade, o convite, a formalidade. O que Josh tinha para escrever era outra coisa. Escreveu para a mãe, Casandra:', 0.4),
 ('j191', 'JOSH', 'Mãe. Quando esta carta chegar, o padrinho provavelmente já terá escrito à senhora com tudo organizado. Então eu não vou repetir o que ele disser. Vou escrever o que ele não vai. A Aurora vem pra Sorô. A filha dele. Vem com a prima, a Vibêke, e ficam duas semanas, e eu vou junto. Ele precisa que a casa daqui fique sem a Aurora por um tempo, por um motivo que não me cabe contar nem nesta carta.', 0.3),
 ('j192', 'JOSH', 'A senhora vai gostar dela, mãe. Eu sei que vai. E é por isso que eu estou escrevendo agora, antes do meio-dia, com a cabeça pesada de uma madrugada sem sono. Eu passei cinco meses nesta casa sendo uma versão de mim que cabe na cidade. E agora eu vou levar a Aurora pra dentro da única versão de mim que é inteira. A do campo. A dos pés na terra. A que a senhora conhece. E eu não sei o que fazer com isso, mãe. Não sei o que acontece quando a pessoa que a gente mais quer no mundo vê a gente no lugar onde a gente não tem disfarce. A senhora vai entender o resto sem eu escrever. A senhora sempre entende.', 0.3),
 ('j193', 'JOSH', 'Diga ao Joseph que a casa vai ter visita longa. Diga ao Dylan, da minha parte, que eu vou estar de olho. Diga ao Matias que separe a coleção do papai. E diga à Meridiana que eu já contei pra alguém sobre a Berta, e que essa alguém não riu. Não vou mentir dizendo que está tudo certo. A senhora leria a mentira daqui mesmo. Vou dizer só o que é verdade inteira: por mais pesado que ande, eu estou de pé. E o que me conforta é que eu estou indo pra casa. Do seu filho do meio. Josh.', 0.6),
 ('j194', 'N', 'Selou a carta. Pôs na pilha do correio do dia. Foi até a janela e abriu. O ar de agosto entrou, morno, com o cheiro de cavalo da cocheira e de pão da padaria três casas adiante. Lá embaixo, no pátio, Helle estendia um lençol no varal. O lençol balançou no vento, branco contra o céu cinza-azulado, e ficou um segundo parado no ar antes de cair sobre a corda.', 0.3),
 ('j195', 'N', 'Josh pensou em Aurora do outro lado do andar, terminando o francês, sem saber ainda que na segunda-feira ia entrar numa carruagem com a prima, rumo a uma fazenda na Zelândia. Pensou que faltavam pouco mais de dois meses para a prova de ingresso, e que boa parte desse tempo ele ia passar debaixo de um telhado de palha, com Aurora dentro da mesma casa. Pensou que Eleonora desconfiava de alguma coisa que não conseguia nomear. Que o padrinho não sabia de nada. E que ele, Josh, sabia de tudo, e não podia dizer nada a nenhum dos dois.', 0.3),
 ('j196', 'N', 'Fechou a janela. Abriu o Grôcius na primeira página pela quarta vez, e dessa vez leu três parágrafos antes de a cabeça voltar para a cozinha, para o rubor no pescoço dela, para o cheiro de jasmim e canela que tinha passado e ficado. Não brigou com a cabeça. Fechou o livro. Olhou para o teto. E ficou ali, com a tarde inteira pela frente, pensando que, se duas semanas eram pouco e eram muito ao mesmo tempo, ele ainda preferia ter as duas semanas a não ter nada.', 0.5),
]

def _falas_de_bloco():
    import importlib.util
    sp = importlib.util.spec_from_file_location("b19", os.path.join(os.path.dirname(os.path.abspath(__file__)), "blocos20.py"))
    b = importlib.util.module_from_spec(sp); sp.loader.exec_module(b)
    return {sl for _, (_, L) in b.BLOCOS.items() for sl, _, _ in L}

if __name__ == "__main__":
    _P = _falas_de_bloco()
    os.makedirs(BASE, exist_ok=True)
    parts = []
    for slug, vk, text, gap in SEG:
        seg_f = f"{BASE}/{slug}.seg.wav"; pf = f"{BASE}/{slug}_p.wav"
        if text.startswith("CLIP:"):
            ref = INT if text[5:] == "josh_aurora_intenso" else os.path.join(os.path.dirname(INT), "josh_aurora.wav")
            subprocess.run(["ffmpeg","-y","-i",ref,"-ac","1","-ar",str(SR),seg_f,"-loglevel","error"],check=True)
        if os.path.exists(seg_f):
            a = load(seg_f); src="cache"
            if slug in _P:  # fala de bloco: o diálogo contínuo sai depressa demais (autora, 19/11)
                a = apply_af(a, slug + "_lento", "silenceremove=stop_periods=-1:stop_duration=0.45:stop_threshold=-40dB:stop_silence=0.4,atempo=0.92")
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
    sf.write(f"{SCR}/cap20-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap20-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-ar","44100","-codec:a","libmp3lame","-b:a","192k",
        f"{SCR}/cap20-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
