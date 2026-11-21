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
 ('p001', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo vinte: A escuta.', 1.2),
 ('p002', 'N', 'Este capítulo volta aos olhos de Josh. No capítulo anterior, na madrugada depois do baile dos Lundgren, ele e Aurora se beijaram pela primeira vez, na sala, contra uma estante de livros. E ele subiu sozinho para o quarto.', 0.8),
 ('p003', 'N', 'Josh não dormiu. Subiu para o quarto leste e deitou de costas, com o braço atravessado sobre o rosto. Não adiantou. A boca de Aurora continuava na boca dele. A nuca dela continuava na palma da mão direita. E a estante, Deus do céu, a estante balançando nas costas dela e o livro caindo no assoalho, e nenhum dos dois olhando. Tinha parado. Isso ele repetia para si mesmo no escuro, contando nos dedos: tinha parado. Tirou a boca antes que a boca o levasse, tirou a mão antes que a outra mão quisesse subir, e subiu a escada sozinho. Grande coisa.', 0.3),
 ('p004', 'N', 'Duas das paredes continuavam de pé, exatamente onde ele as tinha deixado na madrugada: ele não tinha um tostão, e se alguém descobrisse, quem pagava era o nome dela. A primeira parede era a que não deixava ele pregar o olho. O padrinho. O homem que o tirou de uma fazenda na Zelândia e deu a ele um quarto, uma mesa, os livros da própria biblioteca. E o pior de tudo era que Ráge nunca ia saber. Ia continuar dizendo meu rapaz com aquele orgulho contido, ia continuar emprestando os livros com a própria mão, e Josh ia continuar aceitando, sabendo. Ser pego, pelo menos, acabava com a mentira.', 0.3),
 ('p005', 'N', 'Levantou às quatro e dez. Lavou o rosto na bacia. Trocou a camisa de gola alta do baile, amassada de uma noite inteira de cama sem sono, por uma das camisas de algodão cru que usava nos dias comuns, a que parecia mais com a fazenda do que com a Brédigueide. Não calçou. A casa estava no silêncio mais fundo do dia, aquele em que até os ratos da despensa desistem de trabalhar. Desceu descalço. A cozinha estava fria. Fru Larsen só chegava às seis e quarenta e cinco. Josh acendeu uma vela, procurou o pote de café no armário pequeno, não achou o de sempre, achou outro, moeu devagar para o moedor não acordar ninguém e pôs a água no bule de ferro. Sentou no lado esquerdo da mesa de madeira bruta, no lugar que tinha virado dele sem ninguém decidir. O café ferveu. Ele serviu e ficou com a caneca entre as mãos, sem beber.', 0.3),
 ('p006', 'N', 'Ouviu os passos antes de qualquer outra coisa. Leves, curtos, com uma pausa mínima antes de cada apoio, de quem cresceu numa casa onde o assoalho dedurava. Ele conhecia aqueles passos melhor do que os de qualquer pessoa daquela casa, e naquele momento preferia não conhecer. Aurora apareceu na soleira de camisola e roupão. O roupão de algodão grosso, amarrado de qualquer jeito. Os cabelos soltos. O lado direito do tecido tinha escorregado e deixava o ombro à mostra, a clavícula à mostra, a mesma clavícula onde ele tinha estado com a boca quatro horas antes. Josh olhou para o fogão. Ela parou na porta. Ele não levantou. Nenhum dos dois sabia o que fazer com as mãos. Bom dia, disseram os dois juntos.', 0.3),
 ('p007', 'N', 'E pararam juntos. Aurora apertou o laço do roupão com força, e o roupão não tinha culpa nenhuma. Atravessou a cozinha, pegou a caneca azul de borda lascada no armário e encheu com o que tinha no bule. Sentou do outro lado da mesa. No lugar dela. Bebeu um gole e fez uma careta que não conseguiu esconder. Josh esperou que ela dissesse alguma coisa sobre o café. Ela não disse. Bebeu outro gole, por educação, e ficou olhando para a caneca. A vela estalou. Lá fora, um cachorro da rua latiu duas vezes e desistiu.', 0.3),
 ('p008', 'AU', 'Josh. Faz cinco meses que você mora aqui. E eu não sei quase nada de você. Me conta. Da sua casa, da sua família, de você.', 0.25),
 ('p009', 'N', 'Ele girou a caneca entre as mãos.', 0.3),
 ('p010', 'JOSH', 'Melhor não, Aurôra.', 0.25),
 ('p011', 'AU', 'Melhor não por quê?', 0.25),
 ('p012', 'JOSH', 'Porque se eu começar a te contar da minha vida, a gente fica mais perto. E eu não posso ficar mais perto de você.', 0.25),
 ('p013', 'N', 'Ela pousou a caneca. Devagar.', 0.3),
 ('p014', 'AU', 'Ontem você me disse que não ia fingir que não aconteceu. Você prometeu. E é exatamente isso que você está fazendo agora.', 0.25),
 ('p015', 'JOSH', 'Não é isso.', 0.25),
 ('p016', 'AU', 'É exatamente isso.', 0.25),
 ('p017', 'JOSH', 'Não é. Eu sei muito bem o que eu fiz. Eu não esqueci. Eu não vou esquecer, Aurôra, nem se eu quiser, e eu não quero. Mas eu sei pra onde esse caminho vai. É um caminho difícil, e errado, e quem paga no fim é você. Eu não vou te levar por ele. Eu não posso ser esse homem dentro da casa do seu pai.', 0.25),
 ('p018', 'AU', 'Ninguém está te pedindo pra me levar a lugar nenhum. Eu estou te pedindo pra conversar comigo.', 0.25),
 ('p019', 'JOSH', 'É assim que começa.', 0.25),
 ('p020', 'AU', 'Josh, eu perguntei da sua família. Não te pedi em casamento.', 0.25),
 ('p021', 'N', 'Ele quase riu. Segurou. Ela viu que ele segurou, e isso pareceu dar coragem a ela, porque se inclinou um pouco sobre a mesa.', 0.3),
 ('p022', 'AU', 'Não precisa esquecer. Eu não quero que você esqueça. Mas também não quero que você fuja de mim pelos corredores porque aconteceu. Se a gente não pode ser o que... então a gente pode ser amigos. Não pode?', 0.25),
 ('p023', 'JOSH', 'Amigos.', 0.25),
 ('p024', 'AU', 'Amigos.', 0.25),
 ('p025', 'N', 'Josh olhou para ela muito tempo. Era a pior ideia do mundo, e era a única que deixava ele ficar ali, naquela cozinha, do outro lado daquela mesa. Ele sabia disso. Achava que ela não sabia.', 0.3),
 ('p026', 'JOSH', 'Amigos, então', 0.25),
 ('p027', 'N', 'Aurora estendeu a mão por cima da mesa, formal, de fechar negócio. Josh olhou para a mão, olhou para ela, e apertou. Apertou rápido, e soltou mais rápido ainda.', 0.3),
 ('p028', 'AU', 'Muito bem Então, como sua amiga, eu preciso te dizer uma coisa.', 0.25),
 ('p029', 'JOSH', 'O quê?', 0.25),
 ('p030', 'AU', 'Esse café está horrível.', 0.25),
 ('p031', 'N', 'Ele olhou para ela. Ela manteve a cara séria por um, dois segundos, e perdeu.', 0.3),
 ('p032', 'JOSH', 'Eu achei o pó no armário pequeno', 0.25),
 ('p033', 'AU', 'O do armário pequeno é o que a Fru Larsen usa pra arear o bule.', 0.25),
 ('p034', 'JOSH', 'Você está brincando.', 0.25),
 ('p035', 'AU', 'Eu nunca brinco com o bule da Fru Larsen.', 0.25),
 ('p036', 'N', 'E Josh riu. Riu de verdade, com o ombro, alto demais para aquela hora, e teve que tapar a boca com a mão para não acordar a casa. Aurora ficou olhando para ele com uma cara que ele não soube ler. Satisfeita, e outra coisa.', 0.3),
 ('p037', 'JOSH', 'O que foi?', 0.25),
 ('p038', 'AU', 'Nada. No baile, você riu assim com a Vibêke.', 0.25),
 ('p039', 'JOSH', 'Ela me contou de um bode que o Lauritz tentou domar. Era impossível não rir.', 0.25),
 ('p040', 'AU', 'Você já foi meu professor. Já foi meu conselheiro. Agora eu quero que você seja meu amigo. Como você é amigo da Vibêke. Eu nunca vi você rir tão alto quanto você ri com ela.', 0.25),
 ('p041', 'N', 'Josh não soube o que responder. Bebeu o café horrível para ter onde pôr a boca.', 0.3),
 ('p042', 'AU', 'Então. Agora que somos amigos. Por que você resolveu fazer faculdade?', 0.25),
 ('p043', 'JOSH', 'Você não desiste.', 0.25),
 ('p044', 'AU', 'Não. Por quê?', 0.25),
 ('p045', 'JOSH', 'Como assim, por quê?', 0.25),
 ('p046', 'AU', 'Você é do campo, Josh. Você consertou a pérgola com as próprias mãos. Você fala de poda como se tivesse nascido podando. O Erik vai herdar as terras do pai, os Frederiksen vão herdar o nome, todo homem que eu conheço nasceu pra ficar onde está. Você podia ter ficado na fazenda e ninguém ia achar estranho. Mas atravessou a Zelândia pra estudar pra uma prova numa universidade. O que tem aqui que não tinha lá?', 0.25),
 ('p047', 'JOSH', 'Lugar.', 0.25),
 ('p048', 'AU', 'Lugar?', 0.25),
 ('p049', 'JOSH', 'Na fazenda não sobra lugar pra mim. E eu não falo isso com mágoa, falo como quem soma uma conta. O Joseph é o mais velho, então ele cuida da propriedade. A Meridiana cuida da casa e do pomar com a minha mãe. O Dylan vai ficar com a terra, porque é bom nisso e gosta, mesmo fingindo que não gosta de nada. O Matias ainda é criança. E eu sou o do meio. O do meio não tem função. Se eu ficasse, ia passar a vida fazendo o que sobrava do trabalho dos outros. Ia ser útil. Mas útil não é a mesma coisa que necessário. E um homem precisa de pelo menos um lugar onde façam falta dele.', 0.25),
 ('p050', 'AU', 'E a sua mãe deixou?', 0.25),
 ('p051', 'JOSH', 'A minha mãe viu antes de mim. Ela não empurra ninguém, ela espera a pessoa chegar sozinha onde ela já está. Quando eu finalmente disse que queria estudar, ela já tinha escrito pro seu pai havia um ano. Ele é meu padrinho. Prometeu ao meu pai que cuidaria da educação de um dos filhos se fizesse falta. Fez falta.', 0.25),
 ('p052', 'N', 'Aurora olhou para a mesa um momento. Ela sabia o que era não ter lugar. A mestiça de sangue indiano visível no rosto, numa cidade que olhava duas vezes quando ela entrava num salão. Ele viu que ela pensou nisso, e viu que ela decidiu não falar.', 0.3),
 ('p053', 'AU', 'E o que você quer estudar?', 0.25),
 ('p054', 'JOSH', 'Eu gosto de entender como as coisas funcionam. Quando eu era menino, eu desmontava tudo na fazenda pra ver o que tinha dentro. O meu pai brigava. A minha mãe dizia pra deixar, que eu ia montar de novo melhor do que estava. Lei, política, é tudo a mesma coisa. Só que agora o que eu quero desmontar é como os homens decidem viver juntos. O seu pai acha que a Dinamarca vai ter uma constituição antes de eu ficar velho. Eu quero estar na sala onde isso for discutido. Não na plateia. Na sala.', 0.25),
 ('p055', 'AU', 'Na sala Você é o primeiro da sua família a estudar, não é?', 0.25),
 ('p056', 'JOSH', 'Sou.', 0.25),
 ('p057', 'AU', 'Você atravessou a Zelândia sozinho pra abrir um caminho que ninguém da sua casa abriu. Sem ninguém pra te contar como é lá dentro. Pra você isso deve parecer simples, Josh. Pra mim parece coragem.', 0.25),
 ('p058', 'N', 'O sangue subiu pelo pescoço dele inteiro. Na fazenda aquilo nunca tinha tido nome de coragem. Tinha nome de "o que mais você ia fazer".', 0.3),
 ('p059', 'JOSH', 'Obrigado. É o café.', 0.25),
 ('p060', 'AU', 'O café está fraco, Josh. Está horrível, mas está fraco.', 0.25),
 ('p061', 'N', 'Ele escondeu a cara na caneca, e ela riu. Riu alto, com a mão na boca, e o riso dela encheu a cozinha de um jeito que a vela não dava conta. Ele nunca tinha ouvido Aurora rir assim. Nem uma vez em cinco meses. Amigos, Josh pensou. Amigos.', 0.3),
 ('p062', 'AU', 'Me conta dos seus irmãos', 0.25),
 ('p063', 'N', 'Ele sorriu, e sabia exatamente qual sorriso era, porque tinha nome.', 0.3),
 ('p064', 'AU', 'O que foi?', 0.25),
 ('p065', 'JOSH', 'Nada.', 0.25),
 ('p066', 'AU', 'Você está sorrindo de um jeito.', 0.25),
 ('p067', 'JOSH', 'O Dylan chama esse sorriso de cara de idiota satisfeito.', 0.25),
 ('p068', 'N', 'Aurora tapou a boca. Tarde demais.', 0.3),
 ('p069', 'AU', 'É exatamente isso.', 0.25),
 ('p070', 'JOSH', 'Eu sei. Ele inventou quando eu tinha quinze anos e nunca mais largou.', 0.25),
 ('p071', 'AU', 'Então começa por ele.', 0.25),
 ('p072', 'JOSH', 'O Dylan é o pior. Começo pelo Joseph, que é o mais fácil. Tem vinte e quatro. Assumiu a propriedade quando o meu pai morreu, e nunca reclamou uma vez. O problema é que ele assumiu junto a ideia de que quem carrega a casa não tem direito de sentir nada. Então ele trabalha. Do escuro ao escuro. Enquanto trabalha, ele não pensa, e enquanto não pensa, não sente falta do meu pai. Antes ele ria muito. Aprontava, dava trabalho pra minha mãe, namorava metade das moças da freguesia.', 0.25),
 ('p073', 'AU', 'Metade?', 0.25),
 ('p074', 'JOSH', 'A outra metade era prima.', 0.25),
 ('p075', 'N', 'Ela riu de novo. Depois parou, e perguntou com um cuidado que Josh reconheceu antes de entender:', 0.3),
 ('p076', 'AU', 'Ele se senta na cadeira do seu pai?', 0.25),
 ('p077', 'N', 'Josh entendeu de onde vinha a pergunta. Da cabeceira da mesa de jantar da Brédigueide. Da cadeira do Aráve.', 0.3),
 ('p078', 'JOSH', 'Não. Ninguém senta. Ninguém combinou, ninguém mandou, a cadeira simplesmente ficou ali, vazia. A minha mãe passa a mão no encosto antes de sentar na dela, todo jantar, todo santo dia. Não é um gesto grande. Mas é a coisa mais constante daquela casa. O Joseph assumiu tudo. As contas, a lida, as decisões. Tudo, menos aquela cadeira.', 0.25),
 ('p079', 'AU', 'A gente também tem uma A do Aráve. O papai passa o jantar inteiro sem olhar pra ela, e o esforço de não olhar faz mais barulho do que se ele olhasse.', 0.25),
 ('p080', 'JOSH', 'Eu sei. Eu vi, no primeiro almoço. Ninguém me explicou. Não precisou.', 0.25),
 ('p081', 'N', 'As duas casas, tão diferentes em tudo, guardavam o mesmo lugar vazio na mesa. Ficaram com isso um pouco, sem pressa de sair. Depois Aurora empurrou a caneca dele com a ponta dos dedos, de volta na direção dele, e disse:', 0.3),
 ('p082', 'AU', 'Agora o Dylan.', 0.25),
 ('p083', 'JOSH', 'Dezenove. Diz tudo o que a sala inteira está pensando e ninguém tem coragem de dizer, e diz com cara de quem está falando de chuva. Tem um canivete que ele afiou até a lâmina ficar mais fina que a do meu pai. E chuta a porteira do celeiro toda manhã quando passa. Toda. Nunca explicou pra ninguém por quê.', 0.25),
 ('p084', 'AU', 'E você gosta dele?', 0.25),
 ('p085', 'JOSH', 'Adoro. Mas se ele souber, fica insuportável. Com o Dylan, afeto é que nem cachorro bravo: sem movimento brusco.', 0.25),
 ('p086', 'AU', 'E a sua irmã?', 0.25),
 ('p087', 'JOSH', 'A Meridiana. Vinte anos. A minha mãe pôs esse nome porque já sabia, antes de ela nascer, que ela ia ser a do meio que segura a casa. E a Meridiana fala com as árvores.', 0.25),
 ('p088', 'AU', 'Fala com as árvores?', 0.25),
 ('p089', 'JOSH', 'Fala. Tem uma macieira velha no pomar, perto do tanque. O nome dela é Berta. A Meridiana conta o dia pra Berta, pede opinião. Ela acha que árvore guarda tudo o que aconteceu debaixo dela. A primeira vez que eu vi, achei que era brincadeira de criança. E essa é a parte que eu não conto pra ninguém. Às vezes eu falo com a Berta também.', 0.25),
 ('p090', 'AU', 'E ela responde?', 0.25),
 ('p091', 'JOSH', 'Ela é bem mais educada que o Dylan.', 0.25),
 ('p092', 'N', 'Aurora riu com a testa quase encostada na mesa. Quando levantou a cabeça, estava com os olhos molhados de rir.', 0.3),
 ('p093', 'AU', 'Eu queria conhecer a sua irmã.', 0.25),
 ('p094', 'JOSH', 'Vocês iam se dar bem. As duas escolhem o que dizem. Nenhuma fala sem pensar. Só que você aprendeu a ficar calada porque precisava. Numa rua inteira de Copenhague, você é a única com o rosto que tem, e desde menina descobriu que ser notada custa caro. A Meridiana é calada porque a fazenda é calada. Vocês iam reconhecer uma na outra o que falta e o que sobra.', 0.25),
 ('p095', 'N', 'Aurora não respondeu. Josh percebeu, tarde, que tinha dito sobre ela uma coisa que ninguém nunca tinha dito. Não voltou atrás. Ela também não pediu.', 0.3),
 ('p096', 'AU', 'Tem mais irmãos?', 0.25),
 ('p097', 'JOSH', 'O Matias. Treze anos. O caçula. É a parte da família que ainda não aprendeu a esconder o que sente, e a gente protege ele disso o quanto pode. Chora em livro triste sem vergonha nenhuma. Ri alto em livro engraçado. E faz pergunta de menino com a cabeça de quem tem trinta anos. Da morte, do tempo, de Deus. Pergunta no jantar, pergunta no terreiro, pergunta na porta do meu quarto antes de dormir. Foi com o Matias que eu aprendi a responder pergunta difícil sem mentir. Ele percebe na hora. E fica magoado. Não com a verdade. Com a tentativa de pouparem ele dela.', 0.25),
 ('p098', 'AU', 'E a sua mãe? A comadre do papai.', 0.25),
 ('p099', 'JOSH', 'A minha mãe é a pessoa mais difícil de explicar que eu conheço. Eu vou precisar de mais café.', 0.25),
 ('p100', 'AU', 'Desse café?', 0.25),
 ('p101', 'JOSH', 'De qualquer café.', 0.25),
 ('p102', 'N', 'Aurora levantou, foi até o fogão, e dessa vez procurou ela mesma. Achou o pote certo atrás de um saco de farinha, onde a Fru Larsen escondia de quem não merecia, e fez outro bule. Josh olhou as costas dela enquanto ela media o pó. Era a primeira vez em cinco meses que ele olhava para Aurora sem precisar fingir que olhava para outra coisa. Ela virou a cabeça no meio do gesto e pegou o olhar dele no ar. A cor subiu pelo pescoço dela, do lado direito primeiro. Nenhum dos dois desviou. Foi ela quem voltou para o café, e voltou depressa. Amigos. Ela encheu a caneca dele. Sentou. As orelhas ainda estavam vermelhas.', 0.3),
 ('p103', 'AU', 'A sua mãe', 0.25),
 ('p104', 'JOSH', 'Ela me escreve toda semana. Desde março, não passou uma semana sem carta. Escreve do joelho do Joseph, que está ruim de novo. Do Dylan, que ainda não consertou a cerca do pasto norte porque o Dylan não faz nada antes da terceira vez que pedem. Da Meridiana, que arrumou uma macieira nova pra conversar esse ano. Do preço do trigo. De um gato que apareceu na cozinha e que ninguém teve coragem de tirar. Conta tudo. Menos dela. Eu pergunto se a dor nas costas voltou, e ela responde estou bem e passa pro próximo parágrafo.', 0.25),
 ('p105', 'AU', 'E você aceita?', 0.25),
 ('p106', 'JOSH', 'Eu desisti de discutir com ela por carta. Ela ganha sempre. Ela leva tudo pra dentro pra não pôr nos outros. E é a única pessoa daquela casa que sabe puxar a orelha do Dylan na hora certa, e deixar o Matias em paz na hora certa, e saber quando o Joseph precisa de briga e quando precisa de silêncio. Fala pouco. Mas quando fala, parece que ensaiou a frase a semana inteira. Nunca erra. Eu cresci ouvindo conselho dela disfarçado de comentário. Ela nunca dizia faz isso. Dizia: o Pedersen pôs o filho mais novo pra cuidar do estábulo, e o estábulo melhorou. E era ela me mandando tomar conta da minha parte. Eu só fui entender lá pelos dezenove anos.', 0.25),
 ('p107', 'AU', 'Eu ia gostar dela.', 0.25),
 ('p108', 'JOSH', 'Ia. Ela ia gostar de você também. É isso que me preocupa.', 0.25),
 ('p109', 'N', 'Aurora fingiu não ouvir. Ele fingiu não ter dito. Sem que nenhum dos dois decidisse, a conversa chegou no pai dele. Josh contou pouco. A febre. Três semanas. O quarto fechado e a janela aberta de um lado só, porque a mãe dizia que o ar tinha que entrar mas o frio não. O Matias com nove anos, ele com dezessete. O pai que tinha refeito o telhado de palha da casa três vezes com as próprias mãos, e que na terceira vez errou a medida e passou o inverno inteiro jurando que a goteira da cozinha era culpa do vento.', 0.3),
 ('p110', 'JOSH', 'Ele brigava com a goteira De verdade. Ficava embaixo dela, apontando o dedo, dizendo que a culpa não era dele.', 0.25),
 ('p111', 'N', 'Aurora sorriu, e o sorriso dela ficou um pouco torto.', 0.3),
 ('p112', 'AU', 'Você quer saber do Aráve?', 0.25),
 ('p113', 'JOSH', 'Quero. Mas só o que você quiser me contar.', 0.25),
 ('p114', 'N', 'Ela contou. Contou do jardim primeiro, o retângulo de verde e pedra nos fundos da casa, fechado de hera, e as roseiras do canto direito, que tinham sido ideia do Aráve. Ele tinha convencido o pai a encomendar as mudas de um viveiro na Jutlândia e tinha anunciado, no jantar, com o copo levantado: rosas dinamarquesas, em solo dinamarquês, plantadas por mãos indianas. Contou que ele lia o Oxêlenguer no jardim fazendo teatro, com gestos, e que a mãe levantava a sobrancelha fingindo achar exagero, enquanto o pai escondia o riso atrás do jornal. Contou que ela cresceu achando que o mundo inteiro falava em poesia, e só descobriu que não quando ele se foi, e tudo em volta virou prosa de uma hora pra outra. Contou da expedição. O navio. A rota do Ceilão. E contou do dia da notícia.', 0.3),
 ('p115', 'AU', 'Chegou num envelope preto Um oficial da Marinha trouxe. Um homem grande, de farda, e ele não conseguiu olhar pro rosto do meu pai na hora de entregar. É disso que eu mais lembro. O homem grande encolhido. O barulho do envelope abrindo. O silêncio do meu pai, que foi pior do que qualquer barulho. E o grito da minha mãe. Um grito só. Curto. A minha mãe, que não deixa escapar nada no rosto, deu um grito que parecia rasgar a sala. Eu nunca mais ouvi ela fazer um som parecido. E não vou esquecer aquele, nem se eu quiser.', 0.25),
 ('p116', 'N', 'Josh não disse nada logo. Não encheu o silêncio de consolo, porque consolo ali seria tirar dela uma coisa que era dela. Esperou. Depois falou, baixo:', 0.3),
 ('p117', 'JOSH', 'Na minha casa a gente soube estando do lado da cama. Eu estava segurando a mão do meu pai e senti o instante em que ela parou de ser mão. Na sua, foi um oficial e um envelope preto. São jeitos diferentes de a mesma coisa chegar. Mas o que vem depois é igual. A cadeira que ninguém senta. A mãe carregando a casa inteira sem deixar ninguém ver. Eu não sei o tamanho da sua perda, Aurôra. Ela é sua. Mas eu sei como o ar de uma casa muda quando ela passa a ter um lugar vazio.', 0.25),
 ('p118', 'N', 'A mão dele estava aberta em cima da mesa. A dela também, do outro lado. Faltava pouco para as duas se encontrarem no meio. Josh olhou para aquele pouco. E puxou a mão de volta. Um dedo de distância, só o suficiente para saber que tinha puxado. Aurora viu. Respirou fundo, piscou depressa duas vezes, e quando falou a voz já estava limpa:', 0.3),
 ('p119', 'AU', 'Amigos fazem isso, sabia? Contam essas coisas.', 0.25),
 ('p120', 'JOSH', 'Eu sei.', 0.25),
 ('p121', 'AU', 'Então a gente está indo bem.', 0.25),
 ('p122', 'JOSH', 'A gente está indo muito bem', 0.25),
 ('p123', 'N', 'A vela estava no fim. Dava para ouvir a cera escorrendo. Josh olhou para a boca dela, uma vez só, e desviou para o ponto seguro acima do ombro. Bastava levantar, contornar a mesa, três passos. Ele sabia o número. Sabia que não ia dar nenhum. A porta da frente abriu às seis e dezessete. Réle. Os dois levantaram juntos. Aurora lavou a caneca no balde e virou de boca para baixo no escorredor. Josh fez o mesmo com a dele.', 0.3),
 ('p124', 'AU', 'Vou subir antes de a Réle chegar na cozinha', 0.25),
 ('p125', 'JOSH', 'Tudo bem. Eu vou depois de você. E... obrigado, Aurôra. Por ter dividido tanto comigo. E por ter me escutado.', 0.25),
 ('p126', 'N', 'Ela parou na porta. Olhou para ele por cima do ombro.', 0.3),
 ('p127', 'AU', 'De nada... amigo.', 0.25),
 ('p128', 'N', 'Teve uma pausa antes do amigo. Pequena. Ele ouviu.', 0.3),
 ('p129', 'JOSH', 'De nada, amiga', 0.25),
 ('p130', 'N', 'O cheiro dela ficou. Morno, de cama recém-deixada, mais fundo do que de costume. Josh ficou parado no meio da cozinha com as mãos abertas ao longo do corpo, e o corpo dele queria uma coisa só, simples e inteira: ir atrás, alcançar o pulso dela no corredor, puxar de volta. Não foi. Antes daquela madrugada ele só imaginava. Agora sabia como era. E saber, ele estava descobrindo, era muito pior do que imaginar, porque o que a gente imagina ainda dá pra negar. Amigos. Ele tinha aceitado ser amigo da mulher que ele beijou contra uma estante quatro horas antes. Apagou a vela. Subiu. Às nove da manhã, a biblioteca era o lugar mais quieto da casa. Fru Larsen estava na cozinha, Réle na sala de jantar, Aurora na sala de costura com Fru Dahl, na aula de francês, e Ráge no escritório, atrás de cartas e contas. A biblioteca, naquele intervalo, era de Josh.', 0.3),
 ('p131', 'N', 'A estante grande do canto leste ficava de lado para a janela e deixava, entre ela e a parede, um corredorzinho onde ele tinha se acostumado a sentar no chão com o livro do dia. Da porta, ninguém via quem estivesse ali. Ele tinha descoberto isso no segundo mês e guardado a descoberta como quem guarda um esconderijo de criança. Abriu o Grôcius que o padrinho tinha posto na lista da semana. Leu a primeira página duas vezes. Não entrou uma palavra. Entrava a cozinha. Entrava amigo, com a pausa antes. Foi quando a porta abriu. Sem cuidado nenhum. Os passos firmes de Ráge, de sapato, e atrás os de Eleonora, mais leves. E a voz dela já no meio de uma frase, num tom que Josh nunca tinha ouvido nela:', 0.3),
 ('p132', 'EL', ELP+'...e eu não vou deixar esse assunto morrer porque você decidiu que ele é desconfortável, Ráge.', 0.25),
 ('p133', 'N', 'Josh travou. O certo era levantar e aparecer. Mas antes de ele se mexer, ficou claro que era o meio de uma briga começada no escritório, que os dois falavam alto, e que nenhum dos dois tinha lembrado que a biblioteca às nove não era um cômodo vazio. Levantar agora era anunciar que tinha escolhido ficar. Ele não levantou. E, ao não levantar, escolheu.', 0.3),
 ('p134', 'RAJ', 'Eleonora Este não é o lugar pra essa conversa.', 0.25),
 ('p135', 'EL', ELP+'A nossa casa não tem lugar pra essa conversa. Essa conversa nem devia existir, Ráge. Foi você que fez ela existir, no dia em que apertou a mão do Linberg. Agora ela existe, e nós dois temos que decidir o que fazer com a Aurora antes que ela comece a existir pra ela também.', 0.25),
 ('p136', 'N', 'Linberg. Josh tinha ouvido aquele nome uma vez, no escritório, numa frase solta sobre rotas de navio.', 0.3),
 ('p137', 'RAJ', 'A Aurora não tem nada com isso', 0.25),
 ('p138', 'EL', ELP+'A Aurora vai ter tudo com isso se ficar nesta casa nas próximas semanas. Você vai receber o Linberg aqui. Vai receber os homens dele. Vai ter conversa de credor e devedor na sua biblioteca, na sua sala de jantar, com número em cima da mesa e cara de quem está perdendo. Eles vão ameaçar a sua vida se você não garantir que vai pagar. E a Aurora tem os olhos mais afiados desta casa e os ouvidos mais compridos. Em três dias ela entende tudo. E aí, Ráge, me escuta: ela não vai ficar só com medo. Ela vai querer ajudar.', 0.25),
 ('p139', 'N', 'Josh ouviu a poltrona perto da janela estalar. Ráge tinha sentado.', 0.3),
 ('p140', 'RAJ', 'Ela é uma menina.', 0.25),
 ('p141', 'EL', ELP+'Ela é uma menina que já enterrou um irmão e que viu, calada, o pai se despedaçar. Você acha que ela vai assistir de braços cruzados a casa cair de novo? Ela vai se oferecer. Vai chegar pra você com aquela cara de porcelana e dizer que casa com quem for preciso. Com o Linberg, com um sócio do Linberg, com qualquer velho rico que feche a conta. Ela vai se vender pra te salvar e vai chamar isso de dever. Eu não vou deixar a nossa filha chegar nesse ponto. Prefiro que ela não saiba de nada.', 0.25),
 ('p142', 'N', 'Atrás da estante, Josh apertou os punhos. Estava ouvindo o que não tinha o direito de ouvir. E estava ouvindo Eleonora, a dos bordados e do sorriso medido, brigar por uma coisa com uma fúria que ele não sabia que ela tinha.', 0.3),
 ('p143', 'RAJ', 'Então o que você sugere? Porque é simples: a casa não pode ter a Aurora dentro enquanto eu negocio. Preciso dela longe daqui umas duas semanas, sem que ela saiba por quê. A pergunta é: pra onde?', 0.25),
 ('p144', 'EL', ELP+'Eu sei qual é a pergunta.', 0.25),
 ('p145', 'RAJ', 'Então me ajuda a responder. Os Mortensen?', 0.25),
 ('p146', 'EL', ELP+'Os Mortensen, não.', 0.25),
 ('p147', 'RAJ', 'Por quê? O Erik visita às quartas, a família é boa, ele está interessado. E a Ingrid é o mais perto de uma amiga que a Aurora tem.', 0.25),
 ('p148', 'EL', ELP+'Por isso mesmo. O Erik é pretendente, sem nada firmado, e ela não vai aceitar, e você sabe. Manda a nossa filha solteira dormir duas semanas debaixo do teto do pretendente, e a cidade lê de dois jeitos. Ou estamos empurrando o noivado goela abaixo, ou tiramos a Aurora de casa às pressas, e o motivo mais provável é uma gravidez antes do casamento. Uma leitura humilha ela. A outra entrega você. As duas são veneno.', 0.25),
 ('p149', 'RAJ', 'Então os Lundgren.', 0.25),
 ('p150', 'EL', ELP+'A senhora Lundgren me adora, mas tem três filhas casadoiras e nenhum canto pra uma quarta moça. E mora a vinte minutos daqui. Vinte minutos não é distância, Ráge.', 0.25),
 ('p151', 'RAJ', 'A Karoline.', 0.25),
 ('p152', 'EL', ELP+'A Karoline me mandou a Vibêke pra conhecer outros rapazes antes de fechar o noivado com o tal Lauritz, que ela não engole. Se eu devolvo a Vibêke pra Viborg com a Aurora a tiracolo, no meio da temporada, sem explicação, a Karoline entende na hora que aconteceu coisa grave. E a minha irmã não guarda segredo nem da própria sombra. Em uma semana, meia Jutlândia está adivinhando.', 0.25),
 ('p153', 'RAJ', 'Então o que sobra?', 0.25),
 ('p154', 'EL', ELP+'Eu não sei o que sobra. Eu só sei o que não dá.', 0.25),
 ('p155', 'N', 'Teve uma pausa comprida. E Ráge disse o nome quase sem querer, chegando nele pela lista, por exclusão:', 0.3),
 ('p156', 'RAJ', 'Os Rássel.', 0.25),
 ('p157', 'N', 'Atrás da estante, Josh parou de respirar. A casa dele.', 0.3),
 ('p158', 'EL', ELP+'Sorô?', 0.25),
 ('p159', 'RAJ', 'Sim. É perfeito. A propriedade da Casandra. Duas semanas. A Aurora e a Vibêke juntas, uma acompanhando a outra. A Casandra recebe as duas como sobrinhas. O Josh vai junto. O pretexto se explica sozinho: convite de campo de uma amiga antiga, ar puro depois da temporada. A casa fica livre aqui, eu negocio com o Linberg sem a Aurora ouvir uma palavra, e em duas semanas elas voltam sem saber de nada.', 0.25),
 ('p160', 'N', 'As palavras chegaram fora de ordem e levaram um instante para fazer o sentido que Josh não queria que fizessem. Aurora em Sorô. Na casa dele. Debaixo do telhado de palha onde ele era o filho do meio e não o aluno do padrinho, onde se andava descalço e se falava alto e não havia uma única parede da cidade atrás da qual se esconder. E ele junto. Duas semanas. A parte dele que devia ter medo teve: era a pior decisão que os dois podiam tomar, e estavam tomando sem fazer ideia do que tomavam. Mas debaixo do medo, antes que ele tivesse tempo de proibir, subiu outra coisa. Quente. Sem vergonha nenhuma. A mesma que ele tinha passado a madrugada trancando, e que tinha acabado de rebatizar de amizade na cozinha. Essa coisa ouviu duas semanas e quis sorrir. Josh precisou travar o maxilar para não deixar.', 0.3),
 ('p161', 'EL', ELP+'Ráge Sorô é a casa do Josh.', 0.25),
 ('p162', 'N', 'Ela falou o nome dele como se fosse uma palavra feia.', 0.3),
 ('p163', 'RAJ', 'Eu sei. E qual é o problema? Sorô é a casa da Casandra. O Josh é afilhado. A Casandra é uma viúva séria, com cinco filhos e uma propriedade. Tem a Meridiana, tem criadagem. A Aurora vai estar mais cercada de gente direita lá do que em qualquer baile da temporada. Você tem alguma objeção?', 0.25),
 ('p164', 'EL', ELP+'Não. Nenhuma objeção.', 0.25),
 ('p165', 'RAJ', 'Então qual é o problema?', 0.25),
 ('p166', 'EL', ELP+'Não é problema. É desconforto. E não me peça pra explicar como se fosse uma conta, porque não é uma conta.', 0.25),
 ('p167', 'RAJ', 'Eleonora, você sempre tem um motivo. Diz de uma vez.', 0.25),
 ('p168', 'EL', ELP+'Dessa vez eu tenho um pressentimento. Eu sei que você não trabalha com pressentimento. Eu também não. Mas eu conheço a minha filha melhor do que qualquer pessoa viva, e ela anda diferente, Ráge. Diferente nas pausas. No tempo que leva pra responder uma pergunta simples. No jeito de olhar pra certas portas desta casa. Não as portas de onde nós saímos. As de onde um certo rapaz sai. Eu não sei dizer o que é. Mas mandar ela duas semanas pro campo, longe de mim, me deixa com uma coisa atravessada no peito.', 0.25),
 ('p169', 'RAJ', 'Você viu alguma coisa concreta?', 0.25),
 ('p170', 'EL', ELP+'Não. Nada que eu consiga apontar.', 0.25),
 ('p171', 'RAJ', 'Então é a temporada. É a Vibêke chegando. São três bailes em dez dias. Tudo isso explica.', 0.25),
 ('p172', 'EL', ELP+'Pode ser.', 0.25),
 ('p173', 'RAJ', 'Eu preciso que seja. Não tenho outra opção em cima da mesa.', 0.25),
 ('p174', 'EL', ELP+'Eu sei. Eu não estou te pedindo pra mudar de ideia. Estou te pedindo pra lembrar, depois, que eu avisei que não estava tranquila. Só isso.', 0.25),
 ('p175', 'RAJ', 'Fica lembrado. Mas é Sorô.', 0.25),
 ('p176', 'N', 'Foi aí que a perna direita de Josh, dobrada fazia quarenta minutos, começou a formigar e a tremer. Ele tentou segurar. Não segurou. O calcanhar bateu de leve no rodapé da estante, e o barulhinho atravessou a sala inteira. Ninguém respirou.', 0.3),
 ('p177', 'RAJ', 'Tem alguém aí', 0.25),
 ('p178', 'N', 'Josh pensou na porta lateral atrás da estante, a do corredor de serviço. Pensou e desistiu. Sair escondido depois de ouvir tudo era transformar um acidente numa mentira, e mentira ele não ia somar a tudo aquilo. Levantou. Saiu de trás da estante com as duas mãos abertas, desarmado.', 0.3),
 ('p179', 'JOSH', 'Sou eu, padrinho.', 0.25),
 ('p180', 'N', 'Ráge parou. Eleonora pôs a mão no encosto do sofá e não tirou mais.', 0.3),
 ('p181', 'RAJ', 'Josh. Há quanto tempo você está aí?', 0.25),
 ('p182', 'JOSH', 'Desde antes de o senhor e a senhora entrarem. Uns quarenta minutos. Eu vim ler o Grôcius no canto onde eu sempre leio. Eu devia ter levantado e aparecido na primeira frase. Não levantei. A primeira frase da senhora deixou claro que era assunto da família, e eu travei entre interromper e aparecer, e a dúvida durou tanto que virou escolha. A escolha foi errada. A culpa é minha. Inteira.', 0.25),
 ('p183', 'RAJ', 'Você ouviu tudo?', 0.25),
 ('p184', 'JOSH', 'Ouvi tudo. O Linberg. A dívida. Sorô. As casas que não serviam. Eu podia dizer que cheguei agora e o senhor não teria como saber. Mas eu prefiro que o senhor saiba exatamente o que eu sei.', 0.25),
 ('p185', 'N', 'O queixo de Ráge se contraiu, o jeito dele de refazer uma conta interrompida.', 0.3),
 ('p186', 'RAJ', 'Senta.', 0.25),
 ('p187', 'N', 'Josh sentou no sofá. Ráge na poltrona em frente. Eleonora ficou de pé atrás do marido, com a mão no encosto, como quem monta guarda.', 0.3),
 ('p188', 'RAJ', 'Josh, você acaba de saber duas coisas que não eram pra você saber. A dívida do Linberg, e que eu vou mandar a Aurora pra Sorô. Sobre a primeira, eu te explico o suficiente pra você não chegar na Casandra com meia informação. Depois, não agora. Agora eu preciso de uma resposta sua, e preciso que seja verdadeira, já que você acabou de me mostrar que diz a verdade até quando ela te custa.', 0.25),
 ('p189', 'JOSH', 'Pode perguntar.', 0.25),
 ('p190', 'RAJ', 'Você leva a Aurora e a Vibêke pra Sorô e me garante, com a sua palavra, que as duas voltam exatamente como saíram daqui?', 0.25),
 ('p191', 'N', 'A pergunta caiu na sala e ficou. Josh viu, pelo canto do olho, o ombro de Eleonora endurecer com aquela formulação. Ele respondeu com a única verdade que podia dar sem mentir e sem se condenar:', 0.3),
 ('p192', 'JOSH', 'Padrinho, eu levo a Aurôra e a Vibêke pra Sorô e trato as duas do jeito que a casa da minha mãe trata quem chega como hóspede. A minha mãe é uma mulher séria. Os meus irmãos são gente decente. Ela vai receber as duas com o cuidado que daria a parente. E eu respondo pelas duas com a minha palavra. É a única coisa que eu tenho pra dar, e é a única coisa que eu nunca dei à toa.', 0.25),
 ('p193', 'N', 'Não disse palavra de homem, nem palavra de Rássel. Disse a palavra dele, sem enfeite. Ráge olhou para Eleonora. Eleonora não falou. O queixo dela mexeu, o mínimo, o jeito dela de dizer anotado. Ráge voltou para Josh com o brilho de quem gostou do que ouviu, mas era pai, e pai pergunta de novo.', 0.3),
 ('p194', 'RAJ', 'Os seus irmãos.', 0.25),
 ('p195', 'JOSH', 'Pode perguntar dos três.', 0.25),
 ('p196', 'RAJ', 'O Joseph.', 0.25),
 ('p197', 'JOSH', 'Vinte e quatro anos, sério, responsável. Não chega perto da Aurôra. Se chegasse, seria pra perguntar se ela precisa de mais lenha na lareira.', 0.25),
 ('p198', 'RAJ', 'O Dylan. Atrevido, eu já te ouvi dizer.', 0.25),
 ('p199', 'N', 'Josh pensou no Dylan no alpendre, com cara de quem está só olhando o tempo, preparando a frase. Pensou em si mesmo cortando a frase antes da primeira sílaba.', 0.3),
 ('p200', 'JOSH', 'O Dylan vai provocar. É o jeito dele de existir no mundo. Mas provocar é o limite dele, e ele sabe. Se passar um dedo do que a cortesia permite, ele responde a mim antes de responder a qualquer um, e ele me conhece bem demais pra querer descobrir até onde isso vai. A Aurôra está mais segura do Dylan do que estaria de metade dos cavalheiros que ela cumprimentou na temporada.', 0.25),
 ('p201', 'RAJ', 'O Matias.', 0.25),
 ('p202', 'JOSH', 'Treze. Vai ser amigo das duas antes do segundo dia e vai mostrar pra Aurôra a coleção de poesia do meu pai sem ninguém pedir.', 0.25),
 ('p203', 'RAJ', 'E tem a sua irmã.', 0.25),
 ('p204', 'JOSH', 'A Meridiana. Vinte anos. E essa é a parte que o senhor talvez nem precisasse perguntar, mas é a que mais importa. A Aurôra não vai estar sozinha numa casa cheia de homens. Vai ter uma moça da idade dela, do lado dela, o tempo todo. A Meridiana vai cuidar da Aurôra antes de alguém pedir. É o que ela faz com tudo que chega na fazenda precisando de cuidado.', 0.25),
 ('p205', 'N', 'Ráge sustentou o olhar dele mais um tempo, e assentiu. O assentimento curto de decisão tomada.', 0.3),
 ('p206', 'RAJ', 'Ótimo. Eu escrevo hoje pra Casandra, com o convite e os preparativos. As meninas saem segunda de manhã. Vocês ficam duas semanas. Eu mando um recado pra Karoline dizendo que a Vibêke vai conhecer um pouco da Zelândia antes de voltar. E você faz a história circular do jeito certo. Uma palavra pra senhora Lundgren no chá de quinta, de passagem, que a Aurora aceitou um convite de campo, e em dois dias a cidade inteira sabe a história que a gente quer que ela saiba.', 0.25),
 ('p207', 'EL', ELP+'Eu cuido disso', 0.25),
 ('p208', 'RAJ', 'Josh. Mais uma coisa. Você podia ter mentido agora há pouco. Eu perguntei há quanto tempo você estava aí, e você podia ter encolhido a verdade pela metade, dito que pegou só o fim, e eu ia acreditar. Você não fez isso. Você disse que ouviu tudo, sabendo que ficava pior pra você. Eu confio em pouca gente, Josh. Em homem jovem, menos ainda. Mas é por coisas como essa que eu confio em você pra essa viagem. Não esquece disso.', 0.25),
 ('p209', 'N', 'O sangue subiu no rosto de Josh. Não de vergonha: de coisa pior. O padrinho estava confiando nele exatamente pela qualidade que ele tinha traído quatro horas antes, e cada palavra caía na consciência dele como sal em corte.', 0.3),
 ('p210', 'JOSH', 'Padrinho, dizer a verdade ali não teve mérito nenhum. Era o único jeito.', 0.25),
 ('p211', 'RAJ', 'Muita gente, no seu lugar, teria mentido. Por isso eu reparei.', 0.25),
 ('p212', 'N', 'Josh apertou a mão do padrinho. Eleonora não se mexeu. Continuou com a mão no encosto da poltrona, olhando para ele. E quando Josh virou para sair, encontrou os olhos da madrinha por um instante e leu neles a frase que ela nunca ia dizer: eu não te conheço tão bem quanto eu achava. E eu vou prestar atenção. Ele assentiu de leve para ela, sem que Ráge visse. Eu sei que a senhora desconfia. Eu não vou explicar. E a senhora vai esperar. Ela não devolveu o gesto. Josh saiu da biblioteca, fechou a porta sem barulho e subiu para o quarto leste. Sentou na escrivaninha, pegou papel, pena e tinteiro, e a pena ficou parada na folha um bom tempo. O padrinho ia escrever a carta de verdade, com o convite e a formalidade. A dele era outra. Escreveu para a mãe:', 0.3),
 ('p213', 'JOSH', 'Mãe. Quando esta carta chegar, o padrinho já vai ter escrito à senhora com tudo organizado, então eu não vou repetir. Vou escrever o que ele não vai. A Aurôra vem pra Sorô. A filha dele. Vem com a prima, a Vibêke, ficam duas semanas, e eu vou junto. Por um motivo que não me cabe contar nem nesta carta. A senhora vai gostar dela, mãe. Eu sei que vai. E é por isso que eu estou escrevendo agora, antes do meio-dia, com a cabeça zonza de uma noite sem dormir. Eu passei cinco meses aqui sendo uma versão de mim que cabe na cidade. Agora eu vou levar a Aurôra pra dentro da única versão de mim que é inteira, a dos pés na terra, a que a senhora conhece. E eu não sei o que acontece quando a pessoa que a gente mais quer no mundo vê a gente sem disfarce nenhum. A senhora vai entender o resto sem eu escrever. A senhora sempre entende.', 0.3),
 ('p214', 'JOSH', 'Diga ao Joseph que a casa vai ter visita longa. Diga ao Dylan que eu vou estar de olho. Diga ao Matias que separe a coleção do papai. E diga à Meridiana que eu contei da Berta pra alguém, e que esse alguém não riu. Riu, na verdade. Mas não da Berta. Do seu filho do meio, Josh', 0.3),
 ('p215', 'N', 'Selou e pôs na pilha do correio. Foi até a janela e abriu. Entrou o ar de agosto, morno, com cheiro de cavalo da cocheira e de pão da padaria três casas adiante. Lá embaixo, no pátio, Réle estendia um lençol. O vento encheu o lençol de ar, e por um instante ele ficou parado no alto, branco contra o céu, antes de cair sobre a corda. Josh pensou em Aurora do outro lado do andar, terminando o francês com Fru Dahl, sem saber que na segunda-feira ia entrar numa carruagem para uma fazenda na Zelândia. Pensou que faltavam pouco mais de dois meses para a prova, e que boa parte desse tempo ele ia passar debaixo de um telhado de palha, com ela dentro da mesma casa. Pensou que Eleonora desconfiava de uma coisa que não sabia nomear, que o padrinho não sabia de nada, e que ele sabia de tudo e não podia contar para nenhum dos dois. E pensou em amigo. Com a pausa antes.', 0.3),
 ('p216', 'N', 'Fechou a janela. Abriu o Grôcius pela quarta vez e conseguiu ler três parágrafos antes de a cabeça voltar para a cozinha. Não brigou com ela. Fechou o livro. Duas semanas eram pouco. E eram demais. E ele preferia mil vezes ter essas duas semanas a não ter nada.', 0.3),
]

def _falas_de_bloco():
    import importlib.util
    sp = importlib.util.spec_from_file_location("b19", os.path.join(os.path.dirname(os.path.abspath(__file__)), "blocos20.py"))
    b = importlib.util.module_from_spec(sp); sp.loader.exec_module(b)
    return {sl for _, (_, L) in b.BLOCOS.items() for sl, f, _ in L if f != "Raj"}  # Raj fala por fala (autora, 21/11)

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
