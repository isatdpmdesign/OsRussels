import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts14"
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
SEG = [
 ('e001', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo catorze: O mundo do outro lado do muro.', 1.2),
 ('e002', 'N', 'Este capítulo é contado pelos olhos de Aurora. No capítulo anterior, depois de dez dias de distância, ela e Josh se reencontraram no chão da despensa, na noite do aniversário de Aarav. Ela chorava pelo irmão. Ele sentou ao lado dela, sem falar. E disse que distância não é abandono.', 0.6),
 ('e003', 'N', 'Na manhã seguinte, Aurora desceu para a cozinha e encontrou Josh sentado no lugar de sempre. Ela não disse nada. Ele não disse nada. A chaleira estava quente. As canecas estavam nos lugares de sempre: a dele, com a lasca, a dela, sem. E Kóngen, o gato da cozinha, enrolado no canto, abriu um olho, observou os dois por exatos quatro segundos, e o fechou, com a satisfação preguiçosa de quem vê a ordem natural das coisas ser restaurada.', 0.4),
 ('e004', 'N', 'Aurora se serviu. Sentou. Soprou o chá. Ele virou a página do livro. E a cozinha, que por dez dias tinha sido um cômodo vazio com canecas frias e um gato solitário, voltou a ser o que era. Não exatamente o que era antes, porque antes não existia mais. O que existia agora era um depois. E o depois tinha cicatrizes, como tem toda coisa que quebrou e foi remendada: visíveis, irregulares, mas sólidas. Às vezes mais sólidas do que o original.', 0.4),
 ('e005', 'N', 'Ficaram em silêncio por vinte minutos. Não o silêncio fácil de antes. Um silêncio cuidadoso, de quem caminha sobre um lago congelado e testa cada passo. Mas era silêncio compartilhado. E depois de dez dias de silêncio sozinha, o compartilhado bastava. Na porta, Aurora parou. O ritual. A última coisa. E disse, sem se virar:', 0.3),
 ('e006', 'AU', BR+'Não me dê mais conselhos sobre pretendentes. Sobre nada mais. Mas sobre pretendentes, não.', 0.3),
 ('e007', 'JOSH', 'Está bem.', 0.3),
 ('e008', 'AU', BR+'E, Josh?', 0.2),
 ('e009', 'JOSH', 'Sim? O que foi?', 0.3),
 ('e010', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Obrigada. Pelo chão da despensa.', 0.6),
 ('e011', 'N', 'Silêncio. E ele respondeu, devagar:', 0.2),
 ('e012', 'JOSH', 'Quando você precisar. Mesmo que tenha me mandado embora. Mesmo que me mande embora de novo. Quando precisar, eu vou estar lá.', 0.5),
 ('e013', 'N', 'Aurora saiu sem responder. Mas subiu a escada com algo no peito que não era raiva, nem dor, nem luto, nem medo. Era algo mais leve. Como uma manhã de primavera depois de um inverno longo: não quente ainda, não completamente luminosa, mas com a promessa de que o pior já tinha passado.', 1.0),
 ('e014', 'N', 'Julho virou agosto. O verão dinamarquês chegou ao auge: semanas de luz sem fim, em que o crepúsculo durava horas e a noite era só uma pausa educada entre dois dias. A cidade fervia. A temporada estava no clímax. Bailes, saraus, piqueniques, recitais, passeios de barco nos canais. O calendário era tão cheio que Eleonora, a mãe de Aurora, mantinha uma agenda só para convites, numa caligrafia minúscula e meticulosa, que era a arma dela contra o caos.', 0.4),
 ('e015', 'N', 'E Aurora atravessava a temporada com uma competência que surpreendia a mãe e encantava o pai. As aulas de Josh, mesmo com a origem contaminada, mesmo com a confiança traída, tinham efeito real. Aurora sabia sorrir. Sabia olhar. Sabia se posicionar num salão. Sabia conversar. Sabia ser ela mesma de um jeito que não espantava, mas intrigava. Não da noite para o dia. Mas a corda de veludo, aquela barreira invisível em volta dela, estava mais fina. Um rapaz a convidava para dançar. Outro puxava conversa perto da mesa de bebidas. Um terceiro pedia ao pai dela permissão para visitá-la.', 0.4),
 ('e016', 'N', 'E Erik Mortensen, o pretendente que sobreviveu aos conselhos, continuava. Constante. Presente. Toda semana na sala de visitas, com flores diferentes, livros novos, e aquela conversa que corria como rio, sem nenhum dos solavancos que Aurora sentia quando falava com Josh. A ausência de solavancos, ela começava a perceber, era o problema.', 0.4),
 ('e017', 'N', 'Com Erik, tudo era suave. Previsível. Correto. Os silêncios eram confortáveis. Os sorrisos, simétricos. Erik nunca a surpreendia, porque Erik era exatamente o que parecia ser. E o que parecia ser era bom. Genuinamente bom. Mas Aurora, que passou meses sendo surpreendida por um rapaz que corrigia podas de roseira, escrevia cartas que não mandava e sentava no chão de despensas sem falar, descobriu que precisava de surpresa como precisava de chá amargo de manhã. Não por prazer. Por necessidade. Por ser quem era.', 0.4),
 ('e018', 'N', 'Ela não disse isso a ninguém. Nem a Ingrid. Nem a si mesma, nas conversas silenciosas com o espelho antes de dormir. Mas o pensamento estava ali, crescendo como crescem as coisas que não se dizem: devagar, em silêncio, com raízes cada dia mais fundas.', 1.0),
 ('e019', 'N', 'Foi Ingrid, a melhor amiga de Aurora, mais uma vez, quem abriu a porta. Não a porta dos sentimentos: essa ela já tinha aberto. Desta vez era uma porta quase literal. Numa tarde de agosto, as duas caminhavam pelos jardins do Kástelet, a velha fortaleza da cidade, sob um sol que parecia ter decidido que aquele dia existia para ser perfeito. E Ingrid anunciou, com ar de conspiração:', 0.3),
 ('e020', 'ING', BR+'Tem uma festa. Na sexta. Na casa dos Eriksen. Não os Frederiksen, os Eriksen, que são outra família, primos de não sei quem.', 0.3),
 ('e021', 'AU', BR+'Eu não conheço nenhum Eriksen.', 0.3),
 ('e022', 'N', 'Ingrid baixou a voz, embora o caminho estivesse vazio, a não ser por um pato que as observava com a desconfiança razoável de quem lida com humanos todo dia:', 0.2),
 ('e023', 'ING', BR+'Ninguém conhece os Eriksen oficialmente. Esse é o ponto. É uma festa dos jovens. Sem pais. Sem chaperona. Sem convite oficial. Alguém conta pra alguém, que conta pra alguém, e na sexta à noite aparece quem quiser aparecer.', 0.3),
 ('e024', 'N', 'Aurora parou de andar. E repetiu, devagar:', 0.2),
 ('e025', 'AU', BR+'Sem chaperona.', 0.3),
 ('e026', 'ING', BR+'Sem chaperona. Sem a sua mãe. Sem Fru Dahl. Sem ninguém com mais de vinte e cinco anos olhando por cima do ombro pra ver se o seu decote está adequado. E, pra sua sorte, os meus pais estão viajando há semanas, no sul do país. A tia idosa decidiu finalmente morrer, e a mamãe foi junto ajudar. A casa fica comigo, três criadas e um cozinheiro que dorme feito pedra desde as nove. Saída fácil. Volta fácil. Sem testemunhas.', 0.3),
 ('e027', 'AU', BR+'Ingrid, isso é...', 0.2),
 ('e028', 'ING', BR+'Escandaloso? Impróprio? Deliciosamente perigoso? Sim. Tudo isso. E também é a única coisa real que acontece nesta temporada. O resto, os bailes, os chás, os saraus, é teatro. Você sabe tão bem quanto eu. E a maioria das moças da nossa idade vai a essas festas desde os quinze anos.', 0.3),
 ('e029', 'AU', BR+'Eu nunca fui.', 0.3),
 ('e030', 'ING', BR+'Eu sei que você nunca foi. Por isso estou te convidando.', 0.4),
 ('e031', 'N', 'Aurora olhou para a amiga. Ingrid estava apoiada na bengala, com aquela inclinação desafiadora do corpo que era a marca dela: os ombros para trás, o queixo para cima, os olhos cinzentos brilhando, misturando provocação e afeto. Impossível de resistir. Aurora tentou mesmo assim:', 0.2),
 ('e032', 'AU', BR+'Os meus pais nunca permitiriam.', 0.3),
 ('e033', 'ING', BR+'Os seus pais não precisam saber.', 0.3),
 ('e034', 'AU', BR+'Ingrid. O meu pai é o Ráge Svensson. Ele sabe de tudo.', 0.3),
 ('e035', 'ING', BR+'O seu pai sabe de tudo que acontece dentro da casa dele. Fora da casa dele, ele depende de informação. E se a informação que chegar for que você vai passar a noite na minha casa, o que tecnicamente vai ser verdade, porque você vai dormir na minha casa, só não antes da meia-noite, então o seu pai não tem motivo nenhum pra se preocupar.', 0.4),
 ('e036', 'N', 'Aurora pensou. O plano era arriscado. Irresponsável. O tipo de coisa que Aarav faria sem pensar duas vezes, e que Aurora jamais tinha feito, porque pensar duas vezes era o jeito dela. Mas. A palavra mas estava ficando frequente demais na vida de Aurora. Mais frequente que os nãos. E cada mas abria uma fresta por onde entrava luz. Ou perigo. Ou vida. Ou alguma coisa que ela não sabia nomear, mas que sentia como fome. Ela disse:', 0.2),
 ('e037', 'AU', BR+'Eu vou pensar.', 0.3),
 ('e038', 'ING', BR+'Pensa rápido. Sexta é depois de amanhã.', 1.0),
 ('e039', 'N', 'Aurora pensou. Pensou durante o jantar, cortando o salmão, enquanto o pai discorria sobre o parlamento e a mãe acrescentava observações precisas que ninguém pedia e todos valorizavam. Pensou no chá depois do jantar, na sala de estar, enquanto a mãe bordava, o pai lia, e Josh, no canto, com um livro, sempre com um livro, como se os livros fossem uma barricada entre ele e o mundo, virava as páginas com aquela lentidão que Aurora já sabia ler: está pensando em outra coisa.', 0.4),
 ('e040', 'N', 'Pensou na cama, no escuro, com o teto como plateia. A festa dos jovens era tudo o que ela nunca teve. Liberdade. Invisibilidade. A chance de ser Aurora sem o peso do sobrenome, da pele, e da cadeira vazia do irmão. De rir sem que alguém medisse o volume da risada. De dançar sem que alguém contasse quantas vezes. De conversar sem que alguém calculasse o valor de casamento de cada palavra.', 0.4),
 ('e041', 'N', 'E havia a parte que ela tentou não pensar, e que o cérebro, com a teimosia de um gato que sobe onde não deve, insistiu em pensar: a chance de ver o mundo em que as outras moças da idade dela já viviam. O mundo dos beijos, dos flertes, dos toques que não eram exercício no jardim. Aurora nunca tinha beijado ninguém. Nunca. Em dezessete anos, quase dezoito, os lábios dela nunca tinham tocado outros lábios além dos da mãe na testa e dos do pai na bochecha. E aquilo, que aos quinze era normal e aos dezessete era compreensível, começava a parecer uma lacuna. Não social. Pessoal. Um capítulo que todas já tinham lido, e que ela pulou.', 0.4),
 ('e042', 'N', 'Ingrid já tinha beijado. Contou a Aurora, num cochicho escandalizado, dois anos antes: um rapaz chamado Peter, filho de um ferreiro, nos fundos de uma igrêja, numa festa de São João. Foi molhado, confuso e maravilhoso, ela disse, com os olhos brilhando. E eu não me arrependo de nada. Aurora queria saber como era. Não com Erik: com Erik seria oficial, seria compromisso, um passo que ela não estava pronta para dar. Não com nenhum pretendente. Só saber. Como se sabe o gosto de uma fruta que se vê há anos na árvore e nunca se colheu.', 0.4),
 ('e043', 'N', 'Virou de lado na cama. E o pensamento seguinte veio sem convite. Indesejado. Inevitável. Josh. A boca dele. O lábio de baixo, um pouco torto. O canto do sorriso torto. A sombra dourada da barba em volta dos lábios. Aurora afundou o rosto no travesseiro e disse uma palavra que a mãe ficaria horrorizada de saber que a filha conhecia.', 1.0),
 ('e044', 'N', 'Na manhã seguinte, quarta-feira, dois dias antes da festa, Aurora desceu para a cozinha com uma decisão tomada e um plano pela metade. Ele estava lá, como em todas as manhãs desde que os dois fizeram as pazes. Caneca, livro, cabelo despenteado, punhos dobrados. A normalidade restaurada, que era ao mesmo tempo conforto e tortura. Aurora sentou. Se serviu. Soprou. E disse:', 0.2),
 ('e045', 'AU', BR+'Eu preciso da sua ajuda.', 0.4),
 ('e046', 'N', 'Josh levantou os olhos do livro. A expressão era cautelosa, de um jeito novo: o jeito de quem foi repreendido e não quer errar de novo. Os olhos verdes perguntavam sem perguntar: que tipo de ajuda? Aurora acrescentou, depressa:', 0.2),
 ('e047', 'AU', BR+'Não é conselho. É cobertura.', 0.3),
 ('e048', 'N', 'E ele repetiu, devagar:', 0.2),
 ('e049', 'JOSH', 'Dar cobertura?', 0.3),
 ('e050', 'AU', BR+'Tem uma festa na sexta à noite. Uma festa não oficial. De jovens. Sem pais. Sem chaperona. Na casa de alguém que eu não conheço. A Ingrid me convidou. E eu quero ir.', 0.4),
 ('e051', 'N', 'Josh pousou o livro. A expressão passou de cautelosa a uma mistura de preocupação, curiosidade e, escondida debaixo das duas, mas ali, diversão. E ele resumiu:', 0.2),
 ('e052', 'JOSH', 'Você quer ir a uma festa clandestina.', 0.3),
 ('e053', 'AU', BR+'Eu não usaria a palavra clandestina.', 0.3),
 ('e054', 'JOSH', 'Sem pais. Sem chaperona. Na casa de alguém que você não conhece. Clandestina é a palavra certa.', 0.3),
 ('e055', 'N', 'Aurora ergueu o queixo:', 0.2),
 ('e056', 'AU', BR+'A maioria das moças da minha idade vai a essas festas sempre. Eu nunca fui. Porque o Aarav me protegia, e depois que o Aarav se foi, não tinha ninguém pra me dar cobertura. Os meus pais são conservadores. O meu pai me ama, mas me sufoca. E eu tenho dezessete anos e nunca dancei sem alguém contando quantas vezes e com quem.', 0.4),
 ('e057', 'N', 'Josh a olhou. Aurora sustentou o olhar. Sabia o que estava fazendo: pedindo ajuda justamente à pessoa que tinha mais motivos para dizer não. A pessoa que, se fosse egoísta como foi com os conselhos, recusaria, com o argumento legítimo de que era perigoso. Mas Aurora também sabia, e apostava nisso, em tudo o que aprendeu sobre ele em cinco meses de convivência, que ele não era egoísta daquele jeito. Não de novo. Não depois da despensa.', 0.3),
 ('e058', 'N', 'Ele ficou em silêncio. Aurora viu as engrenagens: a linha na testa que se vincava quando ele pesava alguma coisa, o polegar esfregando a lateral da caneca. Viu o momento em que a decisão foi tomada: os ombros relaxando um mínimo, uma expiração quase imperceptível. E ele perguntou:', 0.2),
 ('e059', 'JOSH', 'O que você precisa?', 0.3),
 ('e060', 'AU', BR+'Preciso que você diga aos meus pais que a Ingrid me convidou pra dormir na casa dela. Que confirme, se perguntarem. E preciso... preciso que você não me impeça.', 0.4),
 ('e061', 'N', 'A última frase tinha peso. Não me impeça. Depois dos conselhos envenenados, depois da sabotagem dos pretendentes, Aurora estava dizendo: me deixa viver. Mesmo que o que eu vá viver te assuste. Mesmo que te machuque. Ele sustentou o olhar dela por um longo momento. E respondeu, firme:', 0.2),
 ('e062', 'JOSH', 'Eu não vou te impedir. Mas eu vou com você.', 0.3),
 ('e063', 'N', 'Aurora piscou, surpresa:', 0.2),
 ('e064', 'AU', BR+'Você vai...', 0.2),
 ('e065', 'JOSH', 'Não pra te acompanhar. Não pra ser o seu par. Não pra ser seu guarda-costas. Eu vou porque a Ingrid provavelmente já me convidou, ela é esperta o bastante pra saber que a cobertura funciona melhor se eu também estiver fora de casa. E porque, se alguma coisa der errado, é melhor ter por perto alguém que sabe dar um soco.', 0.3),
 ('e066', 'N', 'Aurora repetiu, incrédula:', 0.2),
 ('e067', 'AU', BR+'Dar um soco.', 0.3),
 ('e068', 'N', 'E o canto direito da boca dele, o do sorriso torto, fez um movimento mínimo:', 0.2),
 ('e069', 'JOSH', 'Eu cresci no campo com quatro irmãos. Não sou violento, mas sei dar um soco. Considera um serviço extra de segurança. Sem custo. Sem conselho. Sem opinião.', 0.4),
 ('e070', 'N', 'Aurora olhou para ele. E sentiu, debaixo da cautela, debaixo da cicatriz ainda fresca, o fantasma de alguma coisa quente, que não era raiva nem mágoa, e que parecia perigosamente com o que ela sentia antes da briga. Ela provocou:', 0.2),
 ('e071', 'AU', BR+'Sem opinião mesmo? Você é capaz de ficar numa festa sem ter opinião sobre nada?', 0.3),
 ('e072', 'JOSH', 'Provavelmente não. Mas vou guardar as opiniões pra mim. Menos sobre o ponche. Se o ponche for ruim, eu vou comentar. Isso é inegociável.', 0.4),
 ('e073', 'N', 'E Aurora fez o som. O som de antes da briga. O fragmento de riso, curto, rouco, surpreso com a própria existência. O som que ele fez nascer num jardim, com uma piada sobre avaliar gado, e que ela achava ter perdido para sempre. Ele ouviu. E alguma coisa aconteceu no rosto dele que Aurora viu, e guardou, e que ficaria guardada por muito tempo: alívio. Um alívio tão fundo e tão visível que era como ver alguém sair da água depois de prender a respiração por tempo demais. Ela então combinou os detalhes:', 0.2),
 ('e074', 'AU', BR+'Sexta. Oito horas. A gente sai junto. Você diz ao meu pai que vai a um encontro do grupo de estudos da universidade. Eu digo que vou dormir na Ingrid. A gente se encontra na esquina, perto de casa, na Brédigueide.', 0.3),
 ('e075', 'JOSH', 'Combinado, está certo.', 0.3),
 ('e076', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: E, Josh?', 0.2),
 ('e077', 'JOSH', 'Sim? O que foi?', 0.3),
 ('e078', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Obrigada. Por não me impedir.', 0.4),
 ('e079', 'N', 'Ele olhou para ela com aqueles olhos que tinham sol, e fogo, e musgo, e tudo o que Aurora não devia saber de cór, mas sabia. E disse, com a voz leve, mas com pedra por baixo da leveza:', 0.2),
 ('e080', 'JOSH', 'Eu aprendi a lição. As coisas que você faz, os lugares aonde você vai, as pessoas com quem você escolhe estar, são suas. Eu posso sentar do seu lado quando você precisar. Mas não posso escolher por você. Nunca mais.', 0.4),
 ('e081', 'N', 'Aurora assentiu. Levantou. Levou a caneca ao tanque. Lavou. Secou. E na porta, o ritual. Ela avisou:', 0.2),
 ('e082', 'AU', BR+'O ponche dessas festas é sempre ruim. A Ingrid me avisou.', 0.3),
 ('e083', 'JOSH', 'Então eu vou preparar a minha cara de desgosto com antecedência.', 0.5),
 ('e084', 'N', 'Aurora saiu. Subiu a escada. Entrou no quarto. Fechou a porta. E sorriu. O sorriso real. O do canto esquerdo, o que subia pelas maçãs do rosto e chegava aos olhos. Sexta-feira. Dois dias. Ela abriu o guarda-roupa. Os vestidos da temporada, verde-floresta, bordô, azul-marinho, cor de vinho, pendurados em ordem como soldados em formação. Nenhum servia. Eram vestidos de baile, de salão, de porcelana. Vestidos de quem está sendo avaliada. Aurora queria um vestido de quem está vivendo.', 0.4),
 ('e085', 'N', 'Fechou o guarda-roupa. Pensou. Depois desceu a escada, atravessou o hall, e bateu na porta do escritório do pai:', 0.2),
 ('e086', 'AU', BR+'Papai? Posso entrar?', 0.2),
 ('e087', 'RAJ', 'Pode, sim. O que aconteceu?', 0.2),
 ('e088', 'AU', BR+'Posso ir amanhã à modista? Eu preciso de um vestido novo.', 0.2),
 ('e089', 'RAJ', 'Pra quê, filha?', 0.2),
 ('e090', 'N', 'E Aurora mentiu, com a fluidez alarmante de quem descobriu que mentir, quando necessário, é uma habilidade e não um pecado:', 0.2),
 ('e091', 'AU', BR+'Pro recital dos Frederiksen, na semana que vem.', 0.2),
 ('e092', 'RAJ', 'Você já tem vestidos suficientes pra três temporadas, Aurora.', 0.2),
 ('e093', 'AU', BR+'Mas nenhum amarelo.', 0.3),
 ('e094', 'N', 'O pai ergueu os olhos dos papéis:', 0.2),
 ('e095', 'RAJ', 'Amarelo? Você nunca usa amarelo.', 0.2),
 ('e096', 'AU', BR+'Exatamente. Está na hora de mudar.', 0.3),
 ('e097', 'N', 'O pai a estudou por um momento. Depois assentiu:', 0.2),
 ('e098', 'RAJ', 'Peça à sua mãe que te acompanhe.', 0.4),
 ('e099', 'N', 'Aurora encontrou a mãe na sala de costura e comunicou o plano. Eleonora ergueu uma sobrancelha, a sobrancelha Svensson, que Aurora herdou, e que queria dizer: estou notando alguma coisa, e vou fingir que não noto, por enquanto. E concordou. Amanhã, a modista. Sexta, a festa. E um vestido amarelo que ainda não existia, mas que Aurora já via na mente. Não o amarelo pálido das debutantes tímidas. Não o amarelo dourado das senhoras ricas. Um amarelo vivo. Quente. Amarelo de girassol. Um amarelo que dizia: estou aqui, e não estou pedindo desculpas. Madame Solberg, a modista, ia adorar.', 1.0),
 ('e100', 'N', 'Quinta-feira foi o dia mais longo da vida de Aurora. Não só pela espera. Era como se o mundo tivesse decidido se apresentar em detalhe demais. A aula de francês com Fru Dahl, a professora particular, pareceu durar três horas. O almoço, uma eternidade. E a visita à modista com a mãe, que Aurora normalmente suportava como quem suporta uma pequena cirurgia, foi surpreendentemente boa. Madame Solberg, a norueguesa, fez exatamente o que Aurora esperava. Se entusiasmou, com alfinetes na boca e os olhos brilhando:', 0.2),
 ('e101', 'SOL', 'Amarelo! Finalmente. Eu disse à senhora Svensson, na primeira prova, que essa menina precisa de cores vivas. Verde escuro é lindo, sim. Mas esta menina não é só drama. Tem sol nela.', 0.4),
 ('e102', 'N', 'Tem sol nela. Aurora ouviu a frase e pensou, inevitavelmente, nele. Em: ele tem sol nos olhos. Em como as coisas que a gente pensa sobre os outros às vezes são as coisas que os outros pensam sobre a gente. O vestido foi cortado e ajustado em tempo recorde. Contra a pele cor de âmbar de Aurora, o efeito era, ela viu no espelho e, pela primeira vez, não discutiu com o que via, deslumbrante. Aurora instruiu:', 0.2),
 ('e103', 'AU', BR+'Mais simples que os outros. Sem rendas. Sem broche. Mangas curtas. Uma saia que permita movimento.', 0.2),
 ('e104', 'N', 'Madame Solberg ergueu uma sobrancelha:', 0.2),
 ('e105', 'SOL', 'Movimento? Que tipo de movimento?', 0.2),
 ('e106', 'AU', BR+'Pra dançar.', 0.4),
 ('e107', 'N', 'Madame Solberg sorriu, o sorriso de quem entende mais do que se diz. E Eleonora, da poltrona, observava tudo com o equivalente materno de um gato que vê um pássaro pela janela: atenção total disfarçada de desinteresse absoluto. Na volta, na carruagem, a mãe disse, só:', 0.2),
 ('e108', 'EL', 'Diga com voz de senhora madura, grave e contida: Amarelo, então.', 0.3),
 ('e109', 'AU', BR+'Amarelo, sim.', 0.3),
 ('e110', 'EL', 'Diga com voz de senhora madura, grave e contida: É uma escolha ousada.', 0.2),
 ('e111', 'AU', BR+'É uma cor, mamãe.', 0.2),
 ('e112', 'EL', 'Diga com voz de senhora madura, grave e contida: Cores nunca são apenas cores, Aurora. São declarações. E amarelo é uma declaração particularmente... visível.', 0.4),
 ('e113', 'N', 'Aurora olhou para a mãe. Eleonora olhava pela janela, com aquele perfil nórdico que podia ter sido esculpido em gelo: perfeito, sereno, impenetrável. Mas os lábios tinham uma curva. Mínima. Quase invisível. Eleonora estava satisfeita.', 1.0),
 ('e114', 'N', 'Sexta-feira. Oito da noite. Na esquina da Brédigueide, perto de casa. Aurora tinha saído de casa às sete e quarenta e cinco, depois de um jantar em que mentiu duas vezes. Para o pai, sobre o grupo de estudos de Josh: eu sei que ele vai, papai, ele me disse. E para a mãe, sobre dormir na Ingrid: ela pediu companhia, o pai dela está viajando, a gente pode bordar junto de manhã. As mentiras saíram com uma facilidade que a assustou e que, ao mesmo tempo, a fez sentir algo que não sentia desde Aarav: cumplicidade com o perigo.', 0.4),
 ('e115', 'N', 'Carregava uma bolsa pequena com o vestido amarelo. Usava o vestido azul escuro de casa: ia trocar na casa de Ingrid. O coração batia depressa. Não era medo. Era antecipação. A sensação de estar prestes a cruzar uma fronteira que não se descruza. Ele apareceu na esquina às oito em ponto. E Aurora quase não o reconheceu.', 0.4),
 ('e116', 'N', 'Sem casaco formal. Sem gravata. Nada do rapaz dos bailes e dos chás. Uma camisa branca simples, os botões de cima abertos, as mangas dobradas até os cotovelos, os antebraços bronzeados, como naquela manhã de abril na cozinha que Aurora nunca ia esquecer. Uma calça escura. As botas boas, as botas do campo, que a irmã dele, Meridiana, poliu antes da viagem. E o cabelo solto, sem pomada, caindo na testa com a desordem natural que a manhã revelava e o dia escondia. Era o rapaz do campo. O que existia antes da cidade. E esse, Aurora reconhecia com a clareza impiedosa de quem finalmente para de mentir para si mesma, era o que ela preferia.', 0.3),
 ('e117', 'JOSH', 'Boa noite.', 0.3),
 ('e118', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Boa noite.', 0.4),
 ('e119', 'N', 'Olharam-se na luz do crepúsculo de agosto, aquela luz escandinava que não é dia nem noite e que transforma tudo em ouro e lilás. Ele olhou para a bolsa e perguntou:', 0.2),
 ('e120', 'JOSH', 'Vestido novo?', 0.2),
 ('e121', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: É amarelo.', 0.3),
 ('e122', 'N', 'Ele ergueu as sobrancelhas. Aurora viu o raciocínio: amarelo, cores vivas, Madame Solberg, uma declaração de intenção que ele não conhecia, mas intuía. E ele repetiu, com uma nota na voz que ela não decifrou por completo. Aprovação? Curiosidade? Alguma coisa mais quente que as duas?', 0.2),
 ('e123', 'JOSH', 'Amarelo, é?', 0.3),
 ('e124', 'AU', BR+'Vamos. A Ingrid está esperando.', 0.5),
 ('e125', 'N', 'Caminharam lado a lado pelas ruas da cidade. Sem carruagem. Sem acompanhantes. Sem ninguém, pela primeira vez na vida de Aurora, dizendo aonde ir, como andar, o que vestir, quanto sorrir. Só dois corpos andando pela cidade no crepúsculo, com o som dos passos nas pedras da rua, o cheiro do porto ao longe, e o calor do verão na pele. Aurora sentiu alguma coisa se expandir no peito. Algo que não tinha a ver só com ele. Tinha a ver com ela mesma. Com o simples, extraordinário, revolucionário ato de andar por uma rua sem que ninguém a observasse. Liberdade. A palavra era essa. Simples. Enorme.', 0.4),
 ('e126', 'N', 'Ele andava ao lado dela naquele passo natural, nem rápido nem devagar, ajustado ao dela, como ele mesmo tinha ensinado que o ritmo certo devia ser. Aurora percebeu. E quase disse alguma coisa. E não disse. Porque nem tudo precisa ser dito para ser reconhecido. Chegaram à casa de Ingrid. Ingrid abriu a porta com um vestido verde e um sorriso de pura travessura concentrada, olhando de um para o outro com a satisfação de uma diretora de teatro vendo o elenco pronto:', 0.2),
 ('e127', 'ING', BR+'Vocês dois. Entrem. Aurora, o meu quarto: você precisa trocar de roupa. Josh, a sala. Tem ponche. É horrível.', 0.4),
 ('e128', 'N', 'Ele olhou para Aurora. Aurora olhou para ele. E naquele olhar rápido, naquela fração de segundo na porta da casa de Ingrid, com a amiga no meio, o crepúsculo atrás e a noite inteira pela frente, passou alguma coisa que era ao mesmo tempo promessa e aviso. Esta noite vai mudar alguma coisa. Os dois sabiam. Nenhum dos dois disse.', 0.4),
 ('e129', 'N', 'Aurora subiu para o quarto de Ingrid. Tirou o vestido azul. Vestiu o amarelo. E se olhou no espelho da amiga, menor que o dela, manchado na borda, com uma rachadura no canto. Mas a imagem era clara. Aurora Svensson, de vestido amarelo de girassol, com o cabelo solto, pela primeira vez fora de casa, sem coque, sem grampos, só as ondas escuras caindo pelos ombros e pelas costas como uma cortina de seda negra. Os olhos de mel brilhando à luz das velas. A pele cor de âmbar contra o amarelo vivo, como ouro contra fogo. Não parecia uma debutante. Parecia alguém prestes a viver.', 0.4),
 ('e130', 'N', 'Ingrid apareceu na porta. Parou. Olhou. E soltou:', 0.2),
 ('e131', 'ING', BR+'Santa mãe de Deus.', 0.2),
 ('e132', 'AU', BR+'É demais?', 0.2),
 ('e133', 'ING', BR+'É perfeito. O Josh vai ter um aneurisma.', 0.2),
 ('e134', 'AU', BR+'Ingrid, para com isso.', 0.2),
 ('e135', 'ING', BR+'É um fato médico. Estou sendo científica. Vamos?', 0.4),
 ('e136', 'N', 'Aurora pegou a mão da amiga, e as duas desceram. Na sala, ele estava de pé perto da janela, com um copo de ponche na mão e a expressão de quem acabou de beber algo que desafia as leis da decência culinária. Ouviu os passos. Virou. E pela segunda vez, a primeira tinha sido na escada da casa, na noite do baile, com o vestido verde-floresta e o colar de âmbar, ele olhou para Aurora e esqueceu como falar.', 0.4),
 ('e137', 'N', 'Mas desta vez foi pior. Porque não era o vestido verde de drama, num salão de cristais. Era o amarelo. Era o cabelo solto. Era a ausência de toda armadura e a presença de tudo o que era Aurora. A moça da cozinha às seis da manhã, a das mãos na terra, a dos pés descalços na biblioteca, a do chão da despensa. Só que de pé, vestida de girassol, sorrindo. E o sorriso era o real. O do canto esquerdo. O que chegava aos olhos.', 0.4),
 ('e138', 'N', 'Ele pousou o copo de ponche. Devagar. Com a concentração de quem precisa ter certeza de que a mão obedece ao cérebro, porque naquele momento cérebro e corpo estavam em lados diferentes da fronteira. E disse, com a voz rouca. Pigarreou. E tentou de novo:', 0.2),
 ('e139', 'JOSH', 'O ponche... o ponche é realmente horrível.', 0.4),
 ('e140', 'N', 'E Aurora riu. Não o fragmento. Uma risada. Pequena, sim. Contida, sim. Mas inteira. Com som, corpo e calor. Ingrid olhou de um para o outro com a expressão de quem assiste a uma explosão controlada, fascinada, de uma distância segura, tomando notas. E decretou:', 0.2),
 ('e141', 'ING', BR+'Vamos antes que eu morra de diabetes olhando vocês dois. A festa é a três quarteirões.', 0.5),
 ('e142', 'N', 'Saíram os três, na noite de agosto, sob o crepúsculo que se recusava a acabar. Em direção a uma casa que Aurora não conhecia, numa rua que nunca tinha pisado, para uma festa onde ninguém a esperava, ninguém saberia o sobrenome dela, e ninguém mediria a cor da pele dela numa escala que ela não escolheu. E ao lado dela, sempre ao lado, nunca à frente, nunca atrás, ele caminhava com as mãos nos bolsos, o cabelo solto, e uma expressão que era, se Aurora o olhasse de relance, e olhou, a de alguém ao mesmo tempo feliz e apavorado. A noite começava. E com ela, tudo o que viria depois.', 0.0),
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
    sf.write(f"{SCR}/cap14-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap14-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap14-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
