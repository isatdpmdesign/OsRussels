import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts10"
SCR = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
# NOVAS vozes: Josh (Achird, jovem/caloroso), Dylan (Zubenelgenubi, casual/seco) — a AUDITAR com a autora
V = {"N": "Vindemiatrix", "AU": "Leda", "EL": "Gacrux", "RAJ": "Algieba",
     "JOSH": "Zubenelgenubi", "DYLAN": "Achird",
     "HELLE": "Achernar", "LARSEN": "Kore",
     "MIK": "Sulafat", "FRED": "Autonoe", "LOV": "Laomedeia", "CAS": "Pulcherrima", "SOL": "Despina", "ING": "Aoede", "CR1": "Erinome", "CR2": "Callirrhoe", "CR3": "Zephyr", "JOSHW": "Zubenelgenubi", "NM": "Vindemiatrix", "ERIK": "Iapetus"}
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
BR = "Diga em português do Brasil, com sotaque brasileiro: "
SEG = [
 ('a001', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo dez: O pretendente certo.', 1.2),
 ('a002', 'N', 'Este capítulo volta aos olhos de Aurora. Depois do sarau dos Holst, Erik Mortensen, o irmão mais velho da amiga Ingrid, pediu permissão ao pai dela para visitá-la. Rico, culto, recém-chegado de Berlim: tudo o que a sociedade esperava. E na escada, naquela noite, Josh disse apenas boa noite, e deixou Aurora subir. A visita estava marcada para quarta-feira.', 0.6),
 ('a003', 'N', 'Erik Mortensen chegou às três da tarde, com um buquê de lírios brancos e uma pontualidade que Fru Larsen, a cozinheira, aprovou com um grunhido, o equivalente, na escala dela, a uma ovação de pé. Aurora o viu da janela do quarto. Viu a carruagem parar. Viu Erik descer, alto, de casaco cinza-claro, com o porte de quem nasceu descendo de carruagens em ruas elegantes. Viu-o ajeitar o casaco, tocar o cabelo castanho num gesto rápido de vaidade, e caminhar até a porta com os lírios numa mão e uma caixa pequena na outra.', 0.4),
 ('a004', 'N', 'Ela respirou fundo e se olhou no espelho. Usava um vestido bordô, não tão escuro quanto o cor de vinho do sarau, mas da mesma família. Madame Solberg aprovaria. Josh aprovaria. O pensamento veio, e Aurora o expulsou com a violência de quem espanta um pássaro que entrou pela janela. Josh não tinha nada a ver com aquilo. O professor tinha feito o trabalho dele. Agora a aluna aplicava o que aprendeu. Era assim que devia funcionar.', 0.4),
 ('a005', 'N', 'O fato de que o professor não tinha descido para a cozinha naquela manhã não queria dizer nada. Pela primeira vez em semanas, a cozinha às seis estava vazia, a caneca dele no lugar, fria, intocada. Ele devia ter dormido mal. Devia estar estudando. Devia ter mil razões perfeitamente razoáveis para não estar sentado à mesa de madeira bruta, com o livro aberto, os punhos dobrados até os cotovelos e o cabelo despenteado que Aurora não queria ver. E de que tinha sentido falta, com uma intensidade que a assustou. Ela desceu a escada.', 1.0),
 ('a006', 'N', 'A sala de visitas dos Svensson era um cômodo que Aurora quase nunca usava, e que a mãe mantinha sempre pronto, como um soldado que dorme fardado. Cortinas de seda cor de creme. Duas poltronas e um sofá em volta de uma mesa baixa. Flores frescas no aparador, trocadas por Helle a cada três dias. Era ali que se recebiam pretendentes. Aurora sabia porque tinha visto Aarav receber moças ali. Não muitas. Aarav espantava as pretendentes por ser honesto demais. Aurora espantava os dela por ser fechada demais. Agora era a vez dela. Do outro lado.', 0.4),
 ('a007', 'N', 'Eleonora estava presente, na poltrona junto à janela, com o bordado no colo, no papel de acompanhante: estar ali sem estar, ver sem ver, ouvir sem ouvir. O pai não estava. Ele sempre se retirava nas visitas de pretendentes, dizendo que essas coisas eram entre as mulheres, o que era mentira, porque o pai sabia tudo o que acontecia naquela casa, e provavelmente já tinha investigado Erik Mortensen até a terceira geração.', 0.4),
 ('a008', 'N', 'E Josh estava no escritório. Estudando. Com a porta fechada. Aurora tinha ouvido os passos dele na escada e depois a porta do escritório se fechando com um clique suave e definitivo, que soou aos ouvidos dela como uma frase inteira: eu não vou estar lá. A campainha tocou. Helle abriu. E Erik Mortensen entrou na sala com os lírios, a caixa, e um sorriso que era, Aurora admitia, genuinamente bonito. Ele se curvou e disse:', 0.25),
 ('a009', 'ERIK', 'Senhorita Svensson. Obrigado por me receber.', 0.2),
 ('a010', 'AU', BR+'O prazer é meu, senhor Mortensen. Por favor, sente-se.', 0.4),
 ('a011', 'N', 'Erik sentou na poltrona em frente. Pousou os lírios na mesa, com uma naturalidade de quem faz aquilo com frequência, e estendeu a caixa:', 0.2),
 ('a012', 'ERIK', 'Um presente. Nada extravagante. A Ingrid me disse que a senhorita aprecia literatura, e eu encontrei isto em Berlim.', 0.4),
 ('a013', 'N', 'Dentro, em papel de seda, havia um livro fino, encadernado em couro azul-marinho, com letras douradas. Poesia, em francês. Lamartine. Meditações poéticas. Aurora disse o nome do poeta com uma surpresa que não precisou fingir:', 0.2),
 ('a014', 'AU', BR+'Lamartine...', 0.4),
 ('a015', 'N', 'Lamartine era novo. Moderno. Romântico, no sentido literário, o movimento que varria a Europa, e que Aurora lia escondido, nos volumes que comprava numa livraria da cidade. Que Erik soubesse disso, por Ingrid, provavelmente, era ao mesmo tempo tocante e um pouco invasivo. Ele explicou, com uma modéstia bem calibrada, charmosa sem ser servil:', 0.2),
 ('a016', 'ERIK', 'A Ingrid comentou que a senhorita lê em francês. Achei que talvez fosse apreciar.', 0.2),
 ('a017', 'AU', BR+'É muito gentil. Obrigada.', 0.4),
 ('a018', 'N', 'Aurora pousou o livro no colo, olhou para Erik, e fez o que Josh tinha ensinado. O olhar, dos olhos à boca e de volta. Mas desta vez, ao contrário do sarau, o gesto foi mecânico. Não menos eficaz: Erik respondeu como qualquer homem responderia, endireitando um pouco os ombros, mais atento. Mas mecânico. Como tocar uma música de cor sem sentir a melodia. Aurora afastou o pensamento, se concentrou, e fez a pergunta, aberta, uma porta e não uma parede:', 0.25),
 ('a019', 'AU', BR+'Me conte da sua viagem.', 0.4),
 ('a020', 'N', 'E Erik contou. E contou bem. Era, Aurora descobriu nas duas horas seguintes, um excelente conversador: sabia contar histórias sem monopolizar, fazia pausas para o outro falar, escutava com os olhos. Falou de Berlim, dos cafés, dos debates de filosofia, da música. Falou da família com afeto: a propriedade na Jutlândia, a mãe que pintava aquarelas, o pai que colecionava mapas antigos. E falou de Ingrid com uma ternura protetora que Aurora reconheceu na hora, porque era a mesma que Aarav tinha por ela. A voz dele perdeu o verniz social, e ficou só honesta:', 0.25),
 ('a021', 'ERIK', 'A Ingrid é a pessoa mais corajosa que eu conheço. Nasceu com uma dificuldade que teria destruído qualquer outra pessoa, e transformou isso em... não sei. Em armadura. Em força. Ela não se esconde. Nunca se escondeu.', 0.3),
 ('a022', 'AU', BR+'Eu sei. É o que eu mais admiro nela.', 0.4),
 ('a023', 'N', 'Erik olhou para Aurora com a expressão de quem deixa de ver a superfície e começa a ver o que está embaixo. E disse:', 0.2),
 ('a024', 'ERIK', 'A Ingrid diz o mesmo sobre você.', 0.4),
 ('a025', 'N', 'Aurora piscou. Ele continuou:', 0.2),
 ('a026', 'ERIK', 'Ela diz que você é a pessoa mais corajosa que ela conhece. Que vive numa cidade que não sabe o que fazer com você, e que enfrenta isso todos os dias sem ceder um centímetro.', 0.4),
 ('a027', 'N', 'O elogio, vindo de Erik, que vinha de Ingrid, a única pessoa cuja opinião Aurora respeitava sem reservas, atingiu um lugar que ela não tinha blindado. Um lugar mole, exposto, atrás de toda a porcelana. Ela respondeu, e a voz falhou quase imperceptivelmente no fim:', 0.2),
 ('a028', 'AU', BR+'A Ingrid exagera.', 0.3),
 ('a029', 'ERIK', 'A Ingrid nunca exagera. É a pessoa mais precisa que eu conheço.', 0.3),
 ('a030', 'N', 'Erik sorriu. Um sorriso bom. Caloroso. Simétrico. Correto. E perguntou:', 0.2),
 ('a031', 'ERIK', 'Senhorita Svensson, posso ser direto?', 0.2),
 ('a032', 'AU', BR+'Por favor.', 0.3),
 ('a033', 'ERIK', 'Eu vim para Copenhague com a intenção de passar a temporada, conhecer pessoas, e talvez, talvez, encontrar alguém. Não tinha expectativas. Expectativas são armadilhas. Mas no sarau dos Holst, quando a gente conversou, eu senti uma coisa que não sentia havia muito tempo.', 0.3),
 ('a034', 'AU', BR+'E o que foi?', 0.3),
 ('a035', 'ERIK', 'Curiosidade. A senhorita me deixou curioso. E curiosidade, na minha experiência, é o começo de tudo o que importa.', 0.5),
 ('a036', 'N', 'Aurora olhou para Erik Mortensen. Vinte e três anos. Culto. Viajado. Rico. Bonito de um jeito que não exigia pensamento. Gentil de um jeito que não exigia esforço. Com uma irmã que era a melhor amiga dela, um Lamartine no colo dela, e olhos escuros que a olhavam com um interesse sem sombra de dúvida verdadeiro. Erik Mortensen era o pretendente certo.', 0.4),
 ('a037', 'N', 'A frase se formou na cabeça dela com a clareza de uma manchete. Era o que a sociedade esperava. O que o pai aprovaria. O que a mãe já aprovava: Aurora nem precisava olhar para saber que o bordado no colo de Eleonora não tinha avançado um ponto sequer na última meia hora. A mãe estava assistindo. E gostava do que via. Erik era a resposta lógica. O caminho que fazia sentido. E Aurora disse, com uma verdade parcial, mas verdade:', 0.2),
 ('a038', 'AU', BR+'Eu também senti curiosidade.', 0.4),
 ('a039', 'N', 'Erik a deixava curiosa como um bom livro deixa: dava vontade de virar a página. Mas. O mas estava lá. Silencioso, enorme, imóvel, como a cadeira de Aarav à cabeceira da mesa. O mas tinha olhos verdes. E um sorriso torto. E mãos calejadas. E uma caneca lascada que tinha ficado fria e intocada na cozinha naquela manhã. Aurora empurrou o mas para o lugar onde guardava tudo o que não cabia na versão dela que mostrava ao mundo. Empurrou com força. Com prática. Erik perguntou:', 0.25),
 ('a040', 'ERIK', 'A gente pode se ver de novo?', 0.2),
 ('a041', 'AU', BR+'Eu gostaria.', 0.4),
 ('a042', 'N', 'Erik sorriu, o sorriso simétrico, correto. E Aurora sorriu de volta. Mas desta vez, e ela sabia, com a parte dela que não mentia, a parte feita das manhãs na cozinha, do chá amargo e das mãos na terra, o sorriso não começou no canto esquerdo. Não subiu pelo rosto. Era o sorriso de porcelana. O antigo. O que recebe e expulsa ao mesmo tempo. Ela o usou mesmo assim.', 1.0),
 # --- depois da visita ---
 ('a043', 'N', 'Erik foi embora às cinco. Deixou os lírios, levou a caixa vazia e a promessa de voltar na semana seguinte. Eleonora o acompanhou até a porta. E o pai apareceu no último momento, como quem passa por acaso pelo hall, o que era tão acidental quanto uma manobra naval, e apertou a mão de Erik com uma firmeza que dizia: eu sei quem você é, de onde vem, quanto tem, e estou avaliando cada palavra que disse à minha filha. A carruagem partiu. A porta se fechou. O pai comentou:', 0.2),
 ('a044', 'RAJ', 'Rapaz admirável.', 0.2),
 ('a045', 'AU', BR+'Sim.', 0.2),
 ('a046', 'RAJ', 'A conversa pareceu boa.', 0.2),
 ('a047', 'AU', BR+'Foi, sim.', 0.2),
 ('a048', 'RAJ', 'Ele trouxe flores e um livro. Duas gentilezas distintas. Isso indica atenção.', 0.2),
 ('a049', 'AU', BR+'Indica, sim.', 0.4),
 ('a050', 'N', 'O pai olhou para a filha com aquela expressão que era ternura embrulhada em escrutínio:', 0.2),
 ('a051', 'RAJ', 'Aurora. Você está me respondendo com monossílabos.', 0.2),
 ('a052', 'AU', BR+'Eu estou cansada, papai. Duas horas de conversa cansam.', 0.2),
 ('a053', 'RAJ', 'Duas horas é um bom sinal. Quando a conversa é ruim, o pretendente vai embora em quarenta minutos.', 0.4),
 ('a054', 'N', 'Aurora quase sorriu. Quase. E pediu:', 0.2),
 ('a055', 'AU', BR+'Posso subir agora?', 0.4),
 ('a056', 'N', 'O pai assentiu. A mãe beijou a testa da filha, um gesto raro: lábios frios, mão quente na nuca, dois segundos que diziam mais que uma hora de conversa. Aurora subiu. No primeiro andar, o corredor estava silencioso. E a porta do escritório, onde Josh tinha passado a tarde inteira, estava aberta. Aurora parou. O escritório estava vazio. A escrivaninha arrumada, a cadeira afastada, os livros fechados. Ela olhou para o fim do corredor. A porta do quarto dele, fechada. Ele tinha se trancado no quarto.', 0.4),
 ('a057', 'N', 'E aquilo trouxe uma dor que ela não esperava. Não a dor de Aarav, que era um abismo, uma ausência tão grande que tinha gravidade própria. Uma dor menor, mais afiada. Uma dor de agulha, não de espada. A dor de perceber que alguém que estava sempre presente, nas manhãs, nos corredores, no jardim, nos olhares do jantar, tinha se ausentado de propósito. Josh estava evitando Aurora.', 0.4),
 ('a058', 'N', 'E ela sabia por quê. Porque ela tinha passado a tarde com Erik Mortensen. Porque o professor viu a aluna aplicar as lições com outro homem. Porque, e essa era a parte que ela não conseguia encarar, brilhante demais, como o sol no meio do dia, Josh se importava. Não como professor. Não como quase-irmão. Não como hóspede. Josh se importava como homem. Aurora encostou na parede do corredor e fechou os olhos. Eu não posso.', 0.4),
 ('a059', 'N', 'Não podia porque Josh era afilhado do pai. Porque morava na mesma casa. Porque a cidade os via como irmãos. Porque, se acontecesse qualquer coisa, um olhar a mais, uma palavra a mais, um toque, a consequência cairia sobre o pai, a mãe, a reputação da família, o futuro de Josh na universidade. Não podia porque Erik existia. Porque Erik tinha tudo o que a lógica pedia, e nada do que o coração queria. E Aurora odiava a palavra coração, a imprecisão, a vulgaridade romântica dela. Mas não achava outra.', 0.4),
 ('a060', 'N', 'E não podia porque Aarav não estava ali para aconselhá-la. Mas Aurora sabia o que ele diria, se estivesse encostado na parede ao lado dela, com aquele sorriso largo. Diria o que sempre dizia quando ela tentava resolver o mundo com lógica. E ela ouviu, como um eco:', 0.3),
 ('a061', 'NM', 'Aurora. Para de pensar. O que você sente?', 0.6),
 ('a062', 'N', 'Aurora abriu os olhos. O corredor estava vazio. A porta do quarto de Josh continuava fechada. Do outro lado, ele devia estar deitado, olhando para o dossel, pensando as mesmas coisas que ela, sentindo a mesma dor de agulha, engolindo o mesmo não posso. Porque Josh era como ela. Guardava. Protegia. Não dizia.', 0.4),
 ('a063', 'N', 'Aurora caminhou até a porta dele. Parou. Levantou a mão. Os dedos a centímetros da madeira. O coração, vulgar, impreciso, insistente, batendo nos ouvidos. Não bateu. Abaixou a mão, virou-se, e foi para o próprio quarto. Sentou na cama, abriu o livro de Lamartine numa página qualquer, e leu o primeiro verso que os olhos encontraram, em francês: Ainsi, toujours poussés vers de nouveaux rivages. Assim, sempre levados a novas margens. Fechou o livro.', 0.4),
 ('a064', 'N', 'Lá fora, as roseiras de Aarav, vermelhas na luz do fim da tarde. O banco envernizado. A pérgola escorada. E num canto, quase invisível na sombra do muro, uma forma cinzenta e peluda: Kóngen, enrolado como sempre, dormindo como se o mundo não estivesse pegando fogo em silêncio em volta dele. Aurora deitou-se. Sem trocar de roupa. Sem soltar o cabelo. Sem nenhum dos rituais que serviam de cerca entre o que ela sentia e o que o mundo tinha permissão de ver.', 0.4),
 ('a065', 'N', 'Ficou olhando o teto, com o livro no peito, o cheiro dos lírios no quarto, e o próprio cheiro de jasmim, o que ficava no corredor quando ela passava, e que Josh respirava quando achava que ninguém via, misturado com uma coisa que não era dela. Falta. A cozinha vazia. A caneca fria. A porta fechada. Não a ausência de Aarav, que era um abismo. A ausência de Josh, que era uma cadeira afastada da mesa: um lugar na paisagem de todo dia que de repente fica vazio, e só então a gente percebe o quanto dependia dele para a paisagem fazer sentido.', 0.4),
 ('a066', 'N', 'Aurora fechou os olhos. E respondeu à pergunta do irmão, em pensamento: Eu sinto falta dele, Aarav. E ele está a vinte passos de distância. E mesmo assim eu sinto falta.', 1.2),
 # --- a cozinha ---
 ('a067', 'N', 'Na manhã seguinte, quinta-feira, dia de cravo, dia de Bach, em que a mãe tocava as mesmas peças na mesma ordem como se a repetição pudesse manter o mundo nos trilhos, Aurora desceu à cozinha às seis e dez. Josh estava lá. No lugar de sempre, com a caneca de sempre, o livro aberto, o cabelo despenteado, os punhos dobrados. E os olhos verdes, quando se ergueram da página, tinham sombras embaixo: olheiras de quem não dormiu, ou dormiu sonhando com coisas que não deixam descansar.', 0.4),
 ('a068', 'N', 'Aurora parou na porta. O silêncio entre os dois era denso, carregado, tão diferente do silêncio confortável das últimas semanas que parecia outra língua. Ela entrou, serviu-se, sentou. Kóngen bocejou. Nenhum dos dois riu. O gato os olhou com aquele olho amarelo de quem está profundamente decepcionado com a espécie humana, e voltou a dormir. Josh fingia ler: a página não virava. Foi Aurora quem quebrou primeiro. Não com nada grande. Com a menor coisa possível. Olhando para a caneca, não para ele, ela disse:', 0.25),
 ('a069', 'AU', 'Diga baixo, sem olhar, com a voz contida, em português do Brasil: Fez falta.', 0.4),
 ('a070', 'N', 'Josh ficou imóvel. Ela continuou:', 0.2),
 ('a071', 'AU', BR+'Ontem. De manhã. Você não desceu.', 0.4),
 ('a072', 'N', 'Uma pausa, longa o bastante para o velho relógio de pêndulo da cozinha, que Fru Larsen tratava como alguém da família, bater duas vezes. Josh respondeu:', 0.2),
 ('a073', 'JOSH', 'Eu sei disso.', 0.2),
 ('a074', 'AU', BR+'E por que você não desceu?', 0.4),
 ('a075', 'N', 'Outra pausa. Josh olhou a caneca dele. Depois a dela. Depois o espaço entre as duas na mesa de madeira bruta: uns sessenta centímetros que guardavam, comprimido e invisível, tudo o que nenhum dos dois dizia. E disse, com uma honestidade que doía:', 0.2),
 ('a076', 'JOSH', 'Porque eu precisava de distância. E eu não confio em mim quando estou perto de você e não tenho distância.', 0.5),
 ('a077', 'N', 'As palavras caíram na cozinha como pedras num lago. Sem barulho. Mas com ondas, que se espalharam, bateram nas margens, voltaram, e não pararam. Aurora não respondeu na hora. Porque o que ele disse era tão exato na descrição do que ela mesma sentia, que responder seria concordar, e concordar seria admitir. Por fim, ela disse:', 0.2),
 ('a078', 'AU', BR+'Está bem.', 0.2),
 ('a079', 'N', 'Ele repetiu, sem entender:', 0.2),
 ('a080', 'JOSH', 'Está bem?', 0.2),
 ('a081', 'AU', BR+'Está bem que você precisou de distância. Eu entendo. Mas...', 0.3),
 ('a082', 'N', 'Ela levantou os olhos da caneca e encontrou os dele. Os olhos verdes, com sombras embaixo e veios de fogo por dentro. E disse:', 0.2),
 ('a083', 'AU', BR+'Não faça isso de novo.', 0.4),
 ('a084', 'N', 'Josh a olhou. Ela sustentou, e acrescentou:', 0.2),
 ('a085', 'AU', BR+'A cozinha é minha. Antes de ser sua. Eu cheguei primeiro. E se alguém tem o direito de se afastar, sou eu. Não você.', 0.4),
 ('a086', 'N', 'Era uma frase absurda. Uma reivindicação de território disfarçada de lógica. Era, se Aurora fosse completamente honesta, um pedido. Não vá embora. Não desta cozinha. Não desta manhã. Não de perto de mim. E Josh entendeu. Claro que entendeu. Josh entendia tudo, lia tudo, guardava tudo. Ele disse:', 0.2),
 ('a087', 'JOSH', 'Está bem. Eu não vou fazer de novo.', 0.5),
 ('a088', 'N', 'Aurora assentiu e voltou os olhos para a caneca. Josh voltou ao livro. A página virou. E o silêncio voltou. Não o silêncio denso de antes, mas um silêncio lavado. Que tinha atravessado alguma coisa e saído do outro lado mais limpo. Como o ar depois da chuva. Ainda não era o silêncio de antes. Talvez nunca mais fosse. Porque antes eles não sabiam, ou fingiam não saber. E agora sabiam. Os dois. Sem ter dito a palavra. Sem ter cruzado a linha. Mas sabendo.', 0.4),
 ('a089', 'N', 'Josh sabia que Aurora sentia falta dele quando ele não estava. Aurora sabia que Josh não confiava em si mesmo perto dela. E os dois sabiam que essas duas coisas juntas eram a coisa mais perigosa e mais bonita que existia naquela casa de regras, talheres e cadeiras vazias. Kóngen abriu um olho. Olhou para os dois. Fechou o olho. Se gatos pudessem suspirar, Kóngen teria suspirado.', 0.0),
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
    sf.write(f"{SCR}/cap10-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap10-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap10-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
