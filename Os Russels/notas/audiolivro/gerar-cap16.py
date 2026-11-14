import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts16"
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
ELP = "Diga com voz de senhora madura, grave e contida: "
SEG = [
 ('g001', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo dezesseis: O que não aconteceu.', 1.2),
 ('g002', 'N', 'Este capítulo volta aos olhos de Aurora. No capítulo anterior, na festa clandestina do celeiro, Aurora e Josh dançaram pela primeira vez. Depois, no depósito, ela pediu que ele a beijasse. Ele resistiu, disse que ela merecia alguém que a beijasse de dia, na frente do mundo, e mesmo assim se inclinou. Mas a voz de Erik Mortensen chamou do salão. Aurora voltou para a festa, e Josh foi embora a pé, sozinho. Aurora passou a noite na casa de Ingrid, que é também a casa de Erik: os dois são irmãos.', 0.6),
 ('g003', 'N', 'Aurora acordou às quatro e meia da manhã. Não havia relógio no quarto de hóspedes dos Mortensen. Ela soube a hora pela luz: aquela primeira luz de agosto, cinza-azulada, que ainda não era o sol, mas o anúncio dele, entrando por uma fresta da cortina como quem testa o terreno antes de invadir. Era a luz mais traiçoeira do verão. Convencia o corpo de que o dia tinha começado, mesmo que o corpo, ainda colado ao colchão, soubesse muito bem que não.', 0.4),
 ('g004', 'N', 'E o corpo dela sabia outras coisas. Sabia que os lábios formigavam. Não os lábios inteiros: só o de baixo, num ponto pequeno e exato no meio, como se alguém tivesse pressionado ali o polegar e esquecido de tirar. Sabia que a pele do antebraço, onde os dedos dele tinham tocado por dois segundos no depósito, estava mais quente do que a do outro braço. Sabia que o cheiro da palha do celeiro ainda estava no cabelo. Palha de festa. Palha de quase. Ela prendeu uma mecha entre os dedos, levou ao nariz, e confirmou: palha. Palha e o fantasma de jasmim e canela, que era o cheiro dela mesma, e que naquela manhã, pela primeira vez, ela não reconheceu como seu.', 0.4),
 ('g005', 'N', 'O corpo dela sabia que tinha pedido. Isso, sobretudo, o corpo sabia. Ficou deitada de costas, olhando o teto branco, com a rosácea de gesso no centro de onde um dia tinha pendido um lustre. Ingrid uma vez explicou que a mãe achava lustre em quarto de hóspedes excessivo: hóspedes não precisam ser impressionados antes de dormir. E sem lustre, a rosácea era só um desenho no teto, que Aurora podia estudar sem distração enquanto remontava, peça por peça, o que tinha feito.', 0.4),
 ('g006', 'N', 'Tinha pedido. Não do jeito que uma moça da Brédigueide pede uma xícara de chá. Do jeito que uma pessoa se aproxima da outra e diz: eu quero isto, e quero agora, e quero de você, especificamente de você. Tinha pedido com o corpo inteiro. Com o vestido amarelo, o cabelo solto, os ombros descobertos. Com o passo à frente. Com a mão na mão dele. E com aquela confissão que escapou antes que a cabeça pudesse censurar: eu nunca fui beijada. Deitada ali, no escuro azulado, Aurora reconhecia que tinha sido a coisa mais corajosa que já tinha dito a alguém. E também a mais idiota. Tinha pedido. E ele tinha dito não.', 0.6),
 ('g007', 'N', 'O não de Josh. Ela fechou os olhos e o repetiu na cabeça. A voz dele tinha ficado rouca. A respiração tinha desacelerado. E os dedos tinham tremido. Ela sentiu, porque segurava a mão dele. O tremor era sutil, mas existia. E Aurora, filha de um pai que percebia tudo nos mínimos detalhes, notou que ele tremeu. O tremor tinha sido a coisa mais bonita da noite. Mais bonita que a luz das lanternas. Mais bonita que o riso que ela riu sem cuidado. Mais bonita até, e isso era o mais traiçoeiro, do que o beijo teria sido, se tivesse acontecido.', 0.4),
 ('g008', 'N', 'Porque o tremor era a prova. A prova de que ele queria. A prova de que o não dele não tinha sido desinteresse. Tinha sido excesso. Excesso de cuidado, de princípio, de respeito por uma coisa que ela ainda não sabia nomear, uma coisa que ele chamou de: de dia, na frente do mundo. Uma coisa que ele se recusou a estragar, mesmo com o consentimento dela na boca e o corpo dela a um milímetro do dele.', 0.4),
 ('g009', 'N', 'Aurora abriu os olhos. O teto continuava lá. A rosácea continuava lá. A luz um pouco mais clara, prometendo um sol que ainda ia demorar duas horas. Ela rolou de lado, afundou o rosto no travesseiro, e disse, baixinho, contra o pano, um palavrão que a mãe não sabia que ela conhecia. Disse de novo, um pouco mais alto. Não ajudou.', 1.0),
 ('g010', 'N', 'O resto da noite tinha sido pior. Ela tinha voltado ao salão depois de deixar Josh no depósito. Atravessou o corredor, ajeitou uma mecha que não precisava de ajeite, parou um segundo na porta para chamar de volta o sorriso medido, a primeira armadura dela, e entrou no salão como se nunca tivesse saído dali. Como se não tivesse acabado de pedir um beijo a um homem que se recusou a dar.', 0.4),
 ('g011', 'N', 'Erik estava num canto da pista. Mais alto do que ela lembrava. Mais formal também, com o casaco bom, cinza-claro, o das visitas oficiais. Não a roupa solta dos outros rapazes. E Aurora viu, na mesma fração de segundo, que ele tinha se preocupado de verdade. A mãe deve ter comentado que Aurora ia dormir na casa deles, ela calculou, e ele deduziu o resto: que Aurora Svensson estava do outro lado do canal, numa festa não oficial. E Erik Mortensen calçou os sapatos sociais e atravessou a cidade no escuro para conferir.', 0.4),
 ('g012', 'N', 'Aurora sentiu três coisas ao mesmo tempo, em camadas. Primeiro, irritação. Erik não era pai dela. Não era irmão. Não tinha autorização nenhuma para ir atrás dela num lugar em que ela tinha decidido estar. Era uma reivindicação disfarçada de gentileza, e Aurora reconhecia o disfarce. Segundo, ternura. Pequena, contrariada, mas real. Erik se importava. Tinha feito o que ninguém pediu, porque, no código dele, era o certo: cuidar da irmã e da amiga da irmã. E ser cuidada, mesmo sem pedir, tocava num lugar dela que estava órfão havia quase dois anos. Terceiro, medo. Não dele. Do que ele teria visto se chegasse três minutos depois.', 0.4),
 ('g013', 'N', 'Erik viu Aurora e sorriu. Atravessou o espaço entre os dois e pousou a mão no cotovelo dela, respeitosa, sem pressionar, como quem cumpre uma cortesia diante de uma plateia invisível. E perguntou:', 0.2),
 ('g014', 'ERIK', BR+'Aurora. Eu te assustei?', 0.2),
 ('g015', 'AU', BR+'Um pouco.', 0.2),
 ('g016', 'ERIK', BR+'Eu sei. Desculpa. Eu não pretendia aparecer assim. A Ingrid não tem culpa, eu insisti.', 0.2),
 ('g017', 'AU', BR+'Como você soube?', 0.2),
 ('g018', 'ERIK', BR+'A minha mãe comentou, antes de viajar, que você ia dormir lá em casa esta noite. A Ingrid me avisou que vocês iam ficar fora até tarde. Ela faz isso de vez em quando, nas semanas em que os nossos pais estão viajando. Não queria me contar onde, mas eu insisti, e ela acabou dizendo que vocês viriam pra cá.', 0.3),
 ('g019', 'N', 'Erik olhou em volta, para o celeiro, as lanternas, o ponche, com a discreta avaliação de quem colhe informação para um relatório mental. E disse, com um sorriso polido e a testa levemente franzida, como quem testa uma hipótese:', 0.2),
 ('g020', 'ERIK', BR+'Não é o tipo de festa em que eu esperava te ver.', 0.2),
 ('g021', 'AU', BR+'Não é. Por isso eu vim.', 0.4),
 ('g022', 'N', 'Aurora viu o canto da boca dele subir um milímetro: divertimento contido, uma aprovação que ele não podia mostrar. Erik gostava dela justamente pelos lados que a Brédigueide preferia que ela escondesse. E isso, num rapaz tão bem-educado, tão bem encaminhado para ser exatamente o que a família esperava, era quase comovente. Aurora teria gostado de Erik se Erik fosse a única opção que ela conhecia. Esse era o problema. Ele pediu:', 0.2),
 ('g023', 'ERIK', BR+'Dança comigo. Assim eu posso dizer à minha mãe, com toda a verdade, que estive numa festa entediante e dancei uma vez antes de ir embora.', 0.2),
 ('g024', 'AU', BR+'A sua mãe e os meus pais não podem saber que a Ingrid e eu estivemos numa festa clandestina.', 0.2),
 ('g025', 'ERIK', BR+'Eu sei. Mas eu sou maior de idade, e não tem nada de errado em eu estar aqui.', 0.2),
 ('g026', 'AU', BR+'Então eu vou ser a sua mentira.', 0.2),
 ('g027', 'ERIK', BR+'Você vai ser a única coisa boa da minha noite.', 0.4),
 ('g028', 'N', 'Aurora sorriu o sorriso medido, o de salão, e pôs a mão sobre a dele. E dançaram. Erik dançava bem. Erik dançava tudo bem: valsa, mazurca, polca. Tinha aulas desde os onze anos, e o corpo dele tinha decorado a coreografia social com a mesma facilidade com que decorou três línguas e o nome de cada talher de um jantar formal. Era um corpo educado. Competente. Confiável. Não era um corpo que tremia.', 0.4),
 ('g029', 'N', 'E ali, na metade do segundo giro, com a mão de Erik na cintura dela, a postura dele exatamente correta, a um decoroso centímetro de distância, Aurora entendeu, com a clareza de uma conta que finalmente fecha, o que Josh tinha feito que ninguém mais tinha feito. No celeiro, os dois tinham pisado nos pés um do outro. Mas não por falta de jeito: tinha sido porque os dedos dele, quando seguraram a mão dela, tremeram. O tremor era a confissão honesta de que tocá-la era uma coisa que ele não conseguia atravessar sem sentir.', 0.4),
 ('g030', 'N', 'Erik não tremia. E o pior era que Aurora não conseguia desejar que ele tremesse. Erik era inteiro do jeito que era. Não reprimia nada. Ela o respeitava. Mais do que isso: gostava dele. De um jeito que não tinha nada a ver com calor de pele. E esse, dizia o corpo dela agora, às quatro e meia da manhã, desmontando a noite minuto a minuto, esse era exatamente o problema.', 0.4),
 ('g031', 'N', 'Ela dançou três músicas com Erik. Quando a terceira acabou, procurou Josh pela primeira vez desde que tinha voltado. Não o viu. Procurou de novo, fingindo desinteresse no rosto, enquanto o corpo procurava com a precisão da agulha de uma bússola. A porta principal. A lateral. A dos fundos, atrás da qual ela o tinha deixado. Nada. Ele tinha ido embora. E Aurora sentiu uma coisa se abrir dentro dela. Não dor, exatamente. Um espaço. Uma sala vazia que ela não sabia que tinha no peito, e que se acendia agora, vasta e fria, com a certeza de que ele tinha visto a cena dela com Erik e decidido não ficar.', 0.4),
 ('g032', 'N', 'E ainda assim, ele tinha avisado Ingrid antes de sair. Aurora teve certeza, porque Ingrid agora atravessava a pista na direção dela, com aquele meio sorriso cifrado. E disse, alto o bastante para Erik ouvir:', 0.2),
 ('g033', 'ING', BR+'Aurora? Já passa da uma. Já dancei tudo o que tinha pra dançar. Vamos?', 0.3),
 ('g034', 'N', 'Os olhos cinzentos de Ingrid eram impossíveis de ler, a não ser que você fosse Aurora e tivesse passado três anos aprendendo. Ingrid estava resgatando. Tirando Aurora da pista antes que ela precisasse explicar a Erik o que ele já sabia em silêncio: que ela não estava nem um pouco interessada naquela dança. Ingrid deu a última ordem:', 0.2),
 ('g035', 'ING', BR+'Erik, vamos embora.', 0.2),
 ('g036', 'ERIK', BR+'Vamos, sim.', 0.4),
 ('g037', 'N', 'Para Erik, era o irmão acatando a irmã que tinha marcado a hora. Para Aurora, era a amiga tirando a amiga da água antes do segundo afogamento. Atravessaram o canal num daqueles barcos que levavam gente por uma moeda. Aurora no banco do meio, Ingrid de um lado, Erik do outro, a água escura embaixo e as estrelas tímidas do verão escandinavo em cima. Erik falava de um amigo da universidade que tinha viajado para Hamburgo, e Aurora respondia só por educação: hum, ah, que interessante. E Ingrid, em silêncio, com a mão muito perto da mão de Aurora, sem encostar. Perto o bastante para Aurora saber que estava ali.', 0.4),
 ('g038', 'N', 'O barco encostou perto da casa dos Mortensen. Erik pagou o barqueiro. Ingrid abriu a porta com a chave da bolsa, e os três entraram. O hall estava escuro, com uma única vela acesa numa mesinha, e dava para ouvir, lá dos fundos, o ronco do velho cozinheiro. Erik disse, no pé da escada:', 0.2),
 ('g039', 'ERIK', BR+'Boa noite, então.', 0.2),
 ('g040', 'N', 'E as duas responderam quase ao mesmo tempo: boa noite. Erik subiu primeiro, sem fazer barulho na escada. Ingrid pegou a vela, levou Aurora pelo corredor até o quarto azul, acendeu a lamparina da cabeceira, e disse, baixinho, da porta:', 0.2),
 ('g041', 'ING', BR+'Amanhã a gente conversa, se você quiser. Se não quiser, eu finjo que não aconteceu nada. Boa noite, mocinha.', 0.2),
 ('g042', 'AU', AI+'Boa noite, Ingrid.', 0.4),
 ('g043', 'N', 'A porta se fechou. Aurora ficou sozinha.', 1.0),
 ('g044', 'N', 'A casa estava silenciosa porque, naquelas semanas, era uma casa esvaziada. O pai de Ingrid estava fora havia três semanas, visitando uma irmã idosa que tinha decidido, nas palavras de Ingrid, a pessoa menos sentimental que Aurora conhecia, começar finalmente a morrer. A mãe tinha ido junto, oficialmente para ajudar a cunhada. Na prática, porque a casa de campo de lá tinha um cordeiro que ela considerava o melhor da Dinamarca. A casa ficou com Ingrid, três criadas e um cozinheiro velho que dormia feito pedra desde as nove e era surdo do ouvido direito. Resultado: Ingrid tinha, naquelas semanas de agosto, uma liberdade que Aurora, a filha do homem que sabia de tudo, só podia descrever, com uma inveja que não confessava, como obscena.', 0.4),
 ('g045', 'N', 'Aurora tinha trocado o vestido amarelo pela camisola. Tinha escovado o cabelo e se deitado. E ali estava, havia três horas, sem ter dormido nem meia hora, com o cheiro de palha nas narinas e o tremor do polegar dele ainda na ponta dos dedos. Levantou. Vestiu o róbe de Ingrid, que tinha dito: use, eu não tenho nada que sirva direito em você, mas o róbe é grande. Abriu a porta com o cuidado de quem conhece o ponto em que cada porta range. E desceu para a cozinha.', 0.4),
 ('g046', 'N', 'A cozinha dos Mortensen era de outro mundo, comparada à da Brédigueide. Menor. Mais bagunçada. Tigelas no escorredor, um pano de prato no encosto da cadeira, cheiro de pão da véspera e do café que o cozinheiro deixava pronto para a manhã. Era uma cozinha que admitia ser cozinha. A da Brédigueide, sob o comando de Fru Larsen, era um teatro onde a cozinha era encenada. Aurora gostou da cozinha dos Mortensen.', 0.4),
 ('g047', 'N', 'Sentou à mesa de madeira bruta. Acendeu uma vela. Olhou o pão. Não comeu. Apoiou a testa nos braços cruzados. A primeira lágrima escapou antes que ela soubesse que estava perto de chorar. Uma lágrima sozinha, de lado, que escorreu para dentro do nariz e fez coçar. Ela puxou o ar, ergueu a cabeça, limpou o rosto com a manga do róbe, e ficou parada, esperando a próxima. A próxima não veio.', 0.4),
 ('g048', 'N', 'Ela respirou fundo. Olhou a chama da vela. E pensou, pela primeira vez naquela noite, com clareza, em Arav. Não no Arav da saudade. No Arav do conselho. O irmão prático, que lia as situações antes de todo mundo, que sentaria na frente dela daquele jeito dele, cotovelos na mesa e o queixo nas mãos, e diria, com aquela voz meio debochada:', 0.2),
 ('g049', 'NM', 'Então, mocinha. Quer me contar o que aconteceu?', 0.4),
 ('g050', 'N', 'E Aurora respondeu a ele em silêncio. Sem palavras, nem na cabeça.', 0.2),
 ('g051', 'AU', AI+'Eu pedi um beijo.', 0.3),
 ('g052', 'N', 'Imaginou o irmão sorrindo.', 0.2),
 ('g053', 'AU', AI+'Eu pedi, e ele disse não.', 0.3),
 ('g054', 'N', 'Imaginou o irmão inclinando a cabeça, o gesto dele quando estava pensando.', 0.2),
 ('g055', 'AU', AI+'E agora eu não sei se eu quero ele mais, porque ele disse não, ou se eu quero menos.', 0.3),
 ('g056', 'N', 'Imaginou Arav rindo. Não com desprezo. Com aquele riso curto, conhecido, que ele dava quando alguém acabava de dizer uma verdade desconfortável sem perceber. E ele diria:', 0.2),
 ('g057', 'NM', 'Aurora. Você quer mais. Você sempre vai querer mais. Esse é o problema.', 0.5),
 ('g058', 'N', 'A vela tremulou. A primeira luz de verdade entrou pela janela alta da cozinha. E Aurora apoiou de novo a testa nos braços e ficou ali, com o irmão imaginário sentado à frente dela, até que Ingrid desceu, uma hora depois, com o cabelo desfeito e a cara amassada de sono, parou na porta, e a olhou sem dizer nada por um momento. Depois falou:', 0.2),
 ('g059', 'ING', BR+'Você não dormiu.', 0.2),
 ('g060', 'AU', AI+'Não. Não dormi.', 0.4),
 ('g061', 'N', 'Ingrid sentou. Pegou um pedaço de pão e mordeu sem manteiga, sem geleia, com a indiferença de quem usa o pão só para ocupar o estômago enquanto pensa. E perguntou:', 0.2),
 ('g062', 'ING', BR+'Você quer me contar?', 0.2),
 ('g063', 'AU', AI+'Não. Não quero.', 0.2),
 ('g064', 'ING', BR+'Você precisa me contar!', 0.3),
 ('g065', 'N', 'Aurora pensou. E respondeu:', 0.2),
 ('g066', 'AU', AI+'Mas eu prefiro não.', 0.2),
 ('g067', 'ING', BR+'Então não conta. Mas eu vou te dizer duas coisas, e você pode aceitar ou recusar.', 0.2),
 ('g068', 'AU', AI+'Pode dizer.', 0.2),
 ('g069', 'ING', BR+'Primeira: o Erik é um bom homem. E bom homem é coisa rara. Eu sei disso porque eu cresci com ele, e vi muito homem ruim de perto. Segunda: você está apaixonada pelo Josh Russel. Isso eu sei porque eu tenho olhos.', 0.5),
 ('g070', 'N', 'Aurora não respondeu. Não havia o que responder. Cada uma das duas frases era uma verdade que ela tinha conseguido manter debaixo da língua até aquele momento. Ouvir as duas ditas por outra pessoa, numa cozinha bagunçada de uma casa sem adultos, na luz cinzenta de uma manhã que se recusava a virar dia, era uma espécie de violência leve. Ingrid continuou comendo o pão. Depois de um tempo, disse:', 0.2),
 ('g071', 'ING', BR+'Você não precisa decidir nada hoje. Esse é o ponto. As pessoas acham que essas coisas exigem decisão na hora. Não exigem. Exigem tempo. E você tem tempo.', 0.2),
 ('g072', 'AU', AI+'Eu tenho?', 0.2),
 ('g073', 'ING', BR+'Tem. Você tem dezessete anos. Tem dois pais que te adoram. Tem uma temporada inteira pela frente. Tem um pretendente que dança valsa, e o afilhado do seu pai. Nenhum dos dois vai fugir da Dinamarca esta semana.', 0.4),
 ('g074', 'N', 'Aurora ergueu os olhos para a amiga. Ingrid sustentou o olhar com a calma sólida que era a marca dela.', 0.2),
 ('g075', 'AU', AI+'Obrigada, Ingrid.', 0.2),
 ('g076', 'ING', BR+'Não me agradeça. Eu sou parcial.', 0.2),
 ('g077', 'AU', AI+'Parcial pra qual lado?', 0.2),
 ('g078', 'ING', BR+'Pro lado em que você estiver, Aurora. Esse é o único lado em que eu vou estar, em qualquer coisa que aconteça com você, até o fim. Só pra constar.', 1.0),
 ('g079', 'N', 'A volta para a Brédigueide foi às nove. Aurora vestiu o vestido azul de casa e dobrou o amarelo com cuidado dentro da bolsa. O cabelo voltou ao coque, com a ajuda de Ingrid e dois grampos. A pele tinha a cor lavada de quem não dormiu. A carruagem dos Mortensen a levou. Ingrid não foi junto. A casa estava como sempre: tijolos vermelhos, o frontão, a aldrava de leão. Helle, a criada, abriu a porta com a bochecha levemente vermelha, a cara que fazia quando alguma coisa a tinha perturbado e ela não podia dizer. Aurora não perguntou. Subiu, trocou de roupa, lavou o rosto. E desceu para o almoço.', 0.4),
 ('g080', 'N', 'O pai estava no escritório, de porta fechada. Desde a escada, Aurora ouviu uma conversa em voz baixa, que parou de repente quando os passos dela passaram. Conversa de negócios, presumivelmente. Mas houve uma intensidade naquele silêncio forçado que ela registrou, e guardou, sem pensar. A mãe estava na sala de estar, com o bordado. E perguntou:', 0.2),
 ('g081', 'EL', ELP+'Você dormiu bem na casa da Ingrid?', 0.2),
 ('g082', 'AU', BR+'Dormi, sim.', 0.2),
 ('g083', 'EL', ELP+'A Helle disse que você parecia cansada.', 0.2),
 ('g084', 'AU', BR+'Não dormi muito. A gente conversou até tarde.', 0.4),
 ('g085', 'N', 'A mãe olhou para ela por meio segundo. Não disse mais nada. Aurora reconheceu o gesto: o gesto Svensson de notar e não comentar, que ela herdou da mãe e vinha usando contra a própria mãe havia seis anos. E perguntou, com toda a indiferença que conseguiu juntar:', 0.2),
 ('g086', 'AU', BR+'O Josh está em casa?', 0.2),
 ('g087', 'EL', ELP+'No escritório, com o seu pai.', 0.2),
 ('g088', 'AU', BR+'Ah, sei.', 0.4),
 ('g089', 'N', 'Aurora sentou na poltrona em frente à mãe e pegou o próprio bordado, um lenço inacabado que estava no cesto havia três semanas. Era melhor segurar aquilo do que ficar de mãos vazias. Bordaram em silêncio. Aurora agradeceu pelo silêncio. A mãe, calada, conseguia dizer dezenas de coisas: preocupação, paciência, espera, julgamento contido, afeto não dito. E Aurora preferia isso às palavras. Palavras eram perigosas. Palavras tinham mandado Aurora ao depósito do celeiro com uma frase na boca que ela ainda não tinha lavado nem da memória nem do lábio.', 0.4),
 ('g090', 'N', 'A conversa no escritório terminou pouco antes do almoço. A porta abriu. Passos. Não dois pares: três. O pai. Josh. E um terceiro que ela não reconheceu. Vozes baixas no hall, uma despedida cordial, a porta da rua se fechando, os passos do pai voltando. Aurora não levantou os olhos do bordado. Mas soube, pelo silêncio que passou pela porta da sala, denso, paterno, que o pai tinha parado um segundo, olhado para ela, visto as olheiras de quem não dormiu, e seguido para o escritório sem dizer nada.', 1.0),
 ('g091', 'N', 'Josh não desceu para o almoço. A mãe comentou, só comentou, sem inflexão nenhuma, que ele tinha pedido a bandeja no quarto: queria adiantar a leitura da universidade. O pai assentiu, como se fosse a coisa mais natural do mundo. Aurora também assentiu. E os três comeram o salmão e a salada de pepino com a etiqueta de sempre, falando do parlamento, do preço do trigo e de um livro que a mãe tinha começado na véspera. Não havia, em nenhum momento, qualquer sinal de que algo estivesse fora do lugar. Aurora pensou que talvez fosse esse o talento mais hereditário da família: fingir, em volta de uma mesa, que nada estava acontecendo, enquanto absolutamente tudo estava.', 1.0),
 ('g092', 'N', 'À tarde, Aurora foi ao jardim. Era a única coisa daquela casa que ela conseguia tocar sem se sentir encenando. As roseiras de Arav. O cascalho da pérgola. O banco recém-envernizado. Não levou nem um livro. Foi só para sentar. Sentou, cruzou as mãos no colo, e ficou. Em algum momento, ouviu, lá em cima, no segundo andar, o som de uma janela se abrindo. Não olhou. Sabia, sem olhar, qual janela era. A do quarto dele.', 0.4),
 ('g093', 'N', 'Aurora não olhou. Não levantou. Não fez sinal nenhum. Mas ergueu o queixo um milímetro. E teve a certeza absoluta, pelo tamanho do silêncio que veio depois do som da janela, de que Josh Russel estava parado ali em cima, olhando para o jardim. Sentiu as bochechas esquentarem, mas não levantou os olhos. E ficou no banco mais tempo do que pretendia.', 1.0),
 ('g094', 'N', 'A manhã na cozinha não aconteceu. Nem no dia seguinte. Nem no outro, nem no outro. No primeiro dia depois da festa, Aurora desceu às seis. A cozinha estava vazia. A caneca com a lasca, a dele, estava no escorredor, de boca para baixo, a água ainda escorrendo. O livro dele não estava na mesa. Kóngen, o gato, enrolado no canto, abriu um olho amarelo, avaliou Aurora por exatos quatro segundos e fechou, com aquela expressão felina de: eu sei o que está acontecendo, e não vou me envolver. Aurora se serviu de chá. Sentou. Soprou. Esperou. Ninguém veio.', 0.4),
 ('g095', 'N', 'No segundo dia, ela desceu mais cedo, às cinco e quarenta e cinco, para tentar chegar antes dele. A cozinha continuava vazia. Aurora se sentiu ridícula. Bebeu o chá em silêncio, com a caneca dele ainda no escorredor, de boca para baixo, como se Helle, que sabia mais do que admitia, tivesse decidido não devolver a caneca à prateleira até segunda ordem. No terceiro dia, Aurora não desceu. Ficou na cama até as sete e tomou o chá no quarto.', 0.4),
 ('g096', 'N', 'Foi um pequeno luto. Ela reconheceu, deitada, com a caneca quente entre as mãos e Kóngen nos pés, porque o gato tinha aparecido de madrugada e resolvido ficar: tinha começado, sem aviso, a sofrer a perda da única rotina com Josh que tinha sido completamente honesta. A cozinha às seis. O silêncio compartilhado. O chá. O livro. A presença sem cobrança. Aquilo tinha morrido com o pedido dela no depósito. E Aurora não conseguia decidir se o pedido tinha valido a perda. Honestamente: ainda não.', 1.0),
 ('g097', 'N', 'Cinco dias depois da festa, no jantar de quarta-feira, a mãe fez um anúncio. Os quatro estavam à mesa. O pai na cabeceira, a mãe à direita, Aurora à esquerda, e Josh em frente a Aurora, no lugar dele desde a primeira semana. Ele tinha voltado a descer para as refeições havia três dias, mas falava o estritamente necessário e olhava para o prato como quem decifra um mapa. Aurora não olhava para ele. Ele não olhava para ela. Era assim, agora. Aurora cortava o peixe quando a frase da mãe atravessou a sala, com a leveza de quem dá uma informação prática:', 0.2),
 ('g098', 'EL', ELP+'A minha irmã Karoline escreveu. A Vibêke vem para a temporada.', 0.2),
 ('g099', 'N', 'O pai ergueu os olhos do prato:', 0.2),
 ('g100', 'RAJ', 'A Vibêke?', 0.2),
 ('g101', 'EL', ELP+'A Vibêke, a minha sobrinha. A filha da Karoline. Você lembra dela. Tem dezoito anos agora, quase dezenove. Naquela festa em Viborg, dois anos atrás, nos oitenta anos da minha mãe, você dançou com ela.', 0.3),
 ('g102', 'N', 'Aurora não olhou para Josh. Mas registrou, com o canto do olho, que ele tinha parado de cortar o peixe.', 0.2),
 ('g103', 'RAJ', 'Ah, sim. Agora eu lembro. A loirinha.', 0.2),
 ('g104', 'EL', ELP+'Todas as filhas da Karoline são loirinhas. Seja mais específico.', 0.2),
 ('g105', 'RAJ', 'A loirinha de olhos azuis.', 0.2),
 ('g106', 'EL', ELP+'Todas têm olhos azuis.', 0.2),
 ('g107', 'RAJ', 'Aquela que ri muito.', 0.2),
 ('g108', 'EL', ELP+'Pronto. Essa mesma.', 0.3),
 ('g109', 'N', 'Aurora pousou o garfo no prato:', 0.2),
 ('g110', 'AU', BR+'A Vibêke vem para a temporada?', 0.2),
 ('g111', 'N', 'A mãe olhou para a filha:', 0.2),
 ('g112', 'EL', ELP+'Vem, sim. A Karoline acha que está na hora de a Vibêke conhecer a capital antes de se casar. Ela tem um pretendente em Viborg, e deve se casar no ano que vem. A minha irmã quer que a menina passe a temporada em sociedade aqui, antes de se enterrar na Jutlândia pelo resto da vida. Palavras dela, não minhas.', 0.2),
 ('g113', 'AU', BR+'E quando ela chega?', 0.2),
 ('g114', 'EL', ELP+'Na próxima quarta. Daqui a uma semana.', 0.2),
 ('g115', 'AU', BR+'Por quanto tempo?', 0.2),
 ('g116', 'N', 'A mãe soltou um suspiro curto, que, nela, era o equivalente sonoro a um sorriso:', 0.2),
 ('g117', 'EL', ELP+'Pelo restante da temporada. Talvez dois meses.', 0.2),
 ('g118', 'N', 'E Aurora repetiu, devagar:', 0.2),
 ('g119', 'AU', BR+'Dois meses.', 0.2),
 ('g120', 'EL', ELP+'Sim. Ela vai ficar no quarto azul, eu já avisei a Helle. Você vai precisar dividir Fru Dahl em algumas manhãs: a Karoline pediu que a Vibêke retome o francês, que estava esquecendo. Eu disse que sim.', 0.4),
 ('g121', 'N', 'Aurora pegou o garfo de novo. Cortou um pedaço de peixe que não tinha vontade de comer, pôs na boca, e mastigou. O pai comentou:', 0.2),
 ('g122', 'RAJ', 'A Vibêke é simpática. Eu lembro dela rindo o jantar inteiro de alguma coisa que tinha acontecido antes do jantar. Eu nunca soube o que era, mas a risada era boa.', 0.2),
 ('g123', 'EL', ELP+'A Karoline pôs nela tudo o que não conseguiu pôr em si mesma. É uma menina alegre. Alegre demais para o meu gosto, mas isso é problema meu, não dela.', 0.2),
 ('g124', 'AU', BR+'Mãe, faz tempo que eu não vejo a Vibêke. Ela mudou muito?', 0.2),
 ('g125', 'N', 'E a mãe riu:', 0.2),
 ('g126', 'EL', ELP+'Dois anos é tempo. Com certeza cresceu. Ficou comprometida. Está com a cabeça em véu e bolo, segundo a Karoline. Acho que ela vai te agradar e te aborrecer em horários diferentes do mesmo dia.', 0.2),
 ('g127', 'N', 'Aurora forçou um sorriso que mostrava exatamente o que ela esperava dos próximos dois meses: a prima falando de noivado, casamento, bailes, tudo o que ela não queria discutir. E respondeu, só:', 0.2),
 ('g128', 'AU', BR+'Hum. Vamos ver.', 0.4),
 ('g129', 'N', 'Tudo o que Aurora queria era que as coisas entre ela e Josh voltassem ao normal. Que o pedido fosse apagado. Ou esquecido. Ou que pelo menos os dois fingissem esquecer. Mas como esquecer o tremor dele? Como esquecer que ele disse não, e ainda assim aproximou o rosto do dela, como quem ia ceder? Aquela noite não saía da cabeça dela. E o rapaz que tinha quase cumprido o pedido estava ali, sentado na frente dela, sem lhe dar a menor atenção.', 0.4),
 ('g130', 'N', 'E por que ela tinha pedido aquilo? O que ele devia estar pensando dela? Claro que ele percebeu o interesse dela. Ela, a filha do padrinho dele. E, isso era para Aurora como a morte, ela sabia, com a clareza da água, que ele sabia que ela o queria, do mesmo jeito que ela sabia que ele a queria. E mesmo assim, ele disse não. Por ser tão íntegro quanto se esperava que Josh Russel fosse. A voz da mãe a tirou dos pensamentos:', 0.2),
 ('g131', 'EL', ELP+'Vocês vão se dar bem.', 0.4),
 ('g132', 'N', 'Aurora tomou um gole de água. Quando pousou o copo, viu, sem olhar direto, que ele tinha voltado a cortar o peixe. Devagar. Sem levantar os olhos. A mãe cortou um pedaço de salmão, pousou a faca, e olhou para o marido:', 0.2),
 ('g133', 'EL', ELP+'Pensando bem, a Vibêke chega numa boa hora.', 0.2),
 ('g134', 'RAJ', 'Como assim?', 0.2),
 ('g135', 'EL', ELP+'A Karoline acha que está tudo certo com o rapaz de Viborg. Mas não está. É pretendente, ainda não é noivo. Se a Vibêke encontrar alguém melhor por aqui, a Karoline vai considerar.', 0.2),
 ('g136', 'N', 'A mãe endireitou as costas e ergueu o queixo. Era a postura exata que ela assumia quando queria provar uma teoria, ou ao menos arrancar alguma informação que confirmasse uma suspeita. O pai sorriu, paciente:', 0.2),
 ('g137', 'RAJ', 'Eleonora, aonde você quer chegar?', 0.2),
 ('g138', 'N', 'E a mãe respondeu, com a precisão de uma flecha que acerta o cervo em plena caçada:', 0.2),
 ('g139', 'EL', ELP+'No Josh.', 0.4),
 ('g140', 'N', 'Aurora ergueu os olhos antes de conseguir não erguer. Josh ergueu os olhos antes de conseguir não erguer. Os dois olharam para a mãe e, no instante seguinte, para o lado. Eleonora não era inocente. Como toda mãe, conhecia a filha como ninguém, e observava aquela casa com a discrição de um camaleão: notava tudo sem ser notada. As conversas entre Aurora e Josh tinham diminuído desde que a filha voltou da casa de Ingrid. E, curiosamente, ela também tinha reparado que Josh esteve fora de casa na mesma noite em que Aurora foi dormir na amiga. Não tinha como ter certeza. Mas havia uma hipótese. E os olhares que os dois tinham acabado de trocar confirmavam um ponto da tese.', 0.2),
 ('g141', 'EL', ELP+'Os dois vêm de fora da capital. Têm hábitos parecidos. São estudiosos. A Vibêke é alegre, o Josh é sério: se equilibram. E o Josh está aqui na nossa casa, sem a família por perto, já em idade de casar. E já que a Aurora e o Josh mal se falam, a Vibêke seria uma boa companhia para os dois.', 0.3),
 ('g142', 'N', 'E deu de ombros, como quem não está plantando uma semente envenenada. Aurora engoliu em seco e sentiu o pescoço esquentar. Pior: sentiu que esquentava de um jeito visível, porque a mãe era a pessoa que mais notava pescoço vermelho em qualquer mesa. O pai se virou para Josh, com a sobrancelha levantada e a voz divertida:', 0.2),
 ('g143', 'RAJ', 'Joshua. Pelo visto, eu acabei de ver a sua madrinha tentar casar você de verdade.', 0.3),
 ('g144', 'N', 'Josh ergueu os olhos. Olhou para o padrinho. Não olhou para Aurora. E respondeu:', 0.2),
 ('g145', 'JOSH', 'Eu agradeço a consideração, padrinho. Mas eu não estou em condições de pensar em casamento. Estou estudando. E tenho responsabilidades com a minha mãe e os meus irmãos, no campo.', 0.3),
 ('g146', 'N', 'A mãe deixou o assunto cair, com a naturalidade de quem já tinha plantado o que queria plantar:', 0.2),
 ('g147', 'EL', ELP+'Claro. Eu só comentei.', 0.4),
 ('g148', 'N', 'Mas tinha comentado. E Aurora pensou que, dali a uma semana, uma prima loira de dezoito anos ia dormir no quarto azul, ao lado do dela. Uma prima alegre, simples, sem complicações. Uma prima que a mãe, em três frases num jantar de quarta-feira, já tinha empurrado na direção de Josh. E pensou que, se já era difícil esconder o cansaço, a culpa, o pedido, o quase, e a cozinha que não acontecia mais, com mais um par de olhos azuis dentro da casa ia ficar pior. Pior ainda se a mãe resolvesse ajudar. Aurora pousou o garfo no prato e disse:', 0.2),
 ('g149', 'AU', BR+'Está bem.', 0.2),
 ('g150', 'EL', ELP+'Está bem o quê?', 0.2),
 ('g151', 'AU', BR+'Está bem que ela venha.', 0.2),
 ('g152', 'EL', ELP+'Eu não estava pedindo permissão, querida.', 0.2),
 ('g153', 'AU', BR+'Eu sei. Estou só registrando.', 0.4),
 ('g154', 'N', 'A mãe sustentou o olhar da filha por um segundo. Depois assentiu, pediu mais salada a Helle, e o jantar continuou. E em algum momento, durante o resto do peixe, Aurora ergueu os olhos para a cadeira vazia de Arav, onde o castiçal de prata e a janela para o jardim desenhavam a moldura permanente da ausência. E fez, em silêncio, a única promessa que ainda conseguia fazer àquela cadeira.', 0.2),
 ('g155', 'AU', AI+'Eu vou aguentar. Eu não sei como. Mas eu vou.', 0.5),
 ('g156', 'N', 'A cadeira não respondeu. A cadeira nunca respondia. Mas a luz da tarde, aquela luz interminável de agosto que se recusava a ir embora antes das nove e meia da noite, entrou pela janela e caiu sobre a cadeira vazia. E por uma fração de segundo, a madeira polida do encosto brilhou, como se alguém tivesse acabado de se levantar dali. Aurora ergueu o queixo. Pegou o garfo. E continuou comendo o peixe que não queria comer. E lá fora, em algum lugar entre Viborg e a capital, uma carruagem levava uma moça loira de olhos azuis, rindo pelas estradas da Zelândia, em direção a uma casa com mais segredos do que um cofre.', 0.0),
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
    sf.write(f"{SCR}/cap16-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap16-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap16-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
