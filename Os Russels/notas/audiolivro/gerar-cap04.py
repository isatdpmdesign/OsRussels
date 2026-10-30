import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts4"
SCR = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
# NOVAS vozes: Josh (Achird, jovem/caloroso), Dylan (Zubenelgenubi, casual/seco) — a AUDITAR com a autora
V = {"N": "Vindemiatrix", "AU": "Leda", "EL": "Gacrux", "RAJ": "Algieba",
     "JOSH": "Zubenelgenubi", "DYLAN": "Achird",
     "HELLE": "Achernar", "LARSEN": "Kore",
     "MIK": "Sulafat", "FRED": "Autonoe", "LOV": "Laomedeia"}
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

SEG = [
 ('i00', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo quatro: O que a cidade vê.', 1.2),
 ('u01', 'N', 'A primavera chegou a Copenhague como chega a tudo na Dinamarca: com atraso, com relutância, e com uma beleza súbita que fazia parecer que o inverno jamais existira. Numa manhã de abril, Aurora abriu os olhos e percebeu que a luz era outra. Dourada, quente, atrevida, espalhando-se pelo quarto como um gato que se deita onde quer. Lá fora, os pássaros cantavam com aquela urgência absurda da primavera, como se o mundo pudesse acabar antes do refrão.', 0.5),
 ('u02', 'N', 'Aurora fechou os olhos. A primavera era a estação de Aarav. Fora na primavera que ele plantara as roseiras, e que trouxera para casa o primeiro livro de poesia que ela leu, declamando os versos no jardim com gestos teatrais que faziam a mãe erguer a sobrancelha e o pai esconder um sorriso atrás do jornal. E fora numa primavera que ele anunciara a viagem ao Ceilão, de onde nunca voltou.', 0.5),
 ('u03', 'N', 'Na primavera passada, a primeira sem ele, Aurora descobriu que as estações não se importam com o luto. Que as flores não deixam de abrir porque alguém morreu. Na época, achou aquilo insuportavelmente cruel. Agora, um ano depois, achava apenas verdadeiro.', 0.6),
 ('u04', 'N', 'Levantou-se e desceu à cozinha antes de todos, como sempre. Era o seu ritual secreto: aqueles minutos sozinha, com as mãos em volta da caneca quente, eram o único momento do dia em que não precisava ser nada para ninguém. Nem a filha do pai, nem a irmã de um morto, nem a anfitriã de um hóspede indesejado. Só Aurora. Mas naquela manhã, ao empurrar a porta com o ombro, ela parou. Havia luz acesa. E havia Josh.', 0.4),
 ('u05', 'N', 'Ele estava sentado à mesa de madeira bruta onde Fru Larsen amassava o pão, com uma caneca e um livro aberto. O cabelo despenteado de sono, nem loiro nem ruivo, algo entre os dois. A camisa com os punhos dobrados até os cotovelos. E Aurora, que não queria ter reparado, e que passaria a manhã inteira irritada consigo mesma por ter reparado, reparou nos antebraços dele, bronzeados e fortes de um jeito que os rapazes de Copenhague não tinham.', 0.4),
 ('u06', 'N', 'Ele levantou os olhos e a viu. E pareceu tão surpreso quanto ela. Os dois falaram ao mesmo tempo. Aurora começou:', 0.2),
 ('u07', 'AU', 'Eu...', 0.2),
 ('u08', 'N', 'E Josh, junto:', 0.2),
 ('u09', 'JOSH', 'Ah... desculpe.', 0.5),
 ('u10', 'N', 'Silêncio. O silêncio de duas pessoas que se flagram num território que ambas achavam secreto. Foi Josh quem falou primeiro. Claro que foi. Não por impulso, Aurora começava a perceber, mas por uma espécie de gentileza prática, como quem abre a porta para alguém porque é mais fácil para os dois.', 0.25),
 ('u11', 'JOSH', 'Eu acordo cedo. No campo, às cinco. Aqui eu consigo esperar até as seis, mas aí não aguento mais. Fru Larsen me mostrou onde fica o chá. Disse que eu podia me servir, desde que não mexesse nas panelas.', 0.45),
 ('u12', 'N', 'Uma parte de Aurora quis dar meia-volta e subir. Mas outra parte, a que tinha a ver com o livro de botânica na terceira prateleira, com os cortes mais baixos nas roseiras, com o jeito como ele não olhara para os olhos vermelhos dela na biblioteca, essa parte tinha curiosidade. Ela entrou sem dizer nada, serviu-se de chá, e sentou-se do outro lado da mesa, o mais longe possível dele. Mas à mesa.', 0.4),
 ('u13', 'N', 'Josh voltou ao livro. Ficaram assim vinte minutos, em silêncio, cada um no seu lado, dividindo o mesmo espaço pela primeira vez sem que o espaço doesse. Quando Aurora se levantou para sair, Josh disse, sem tirar os olhos da página:', 0.25),
 ('u14', 'JOSH', 'Capítulo nove. A parte sobre a poda de primavera é a melhor.', 0.4),
 ('u15', 'N', 'Aurora parou na porta. Não se virou. Respondeu:', 0.2),
 ('u16', 'AU', 'Eu sei. Já li.', 0.45),
 ('u17', 'N', 'E saiu. Mas nos lábios dela havia algo que não era exatamente um sorriso. Era menor que um sorriso. Era a possibilidade de um. Josh não viu. Só o gato de Fru Larsen, enrolado no canto da cozinha, abriu um olho amarelo, observou-a sair, e voltou a dormir.', 0.8),
 ('u18', 'N', 'A primavera trouxe também, para desgosto de Aurora, os convites. A sociedade de Copenhague funcionava por temporadas. A primavera era quando as portas se abriam e as famílias com filhas em idade de debutar se preparavam para o verão: a estação dos bailes, das óperas, e, inevitavelmente, dos noivados. E naquele ano, Aurora seria uma das debutantes.', 0.4),
 ('u19', 'N', 'A ideia era como ter engolido uma pedra. Debutar era ser vista, avaliada, apresentada. Numa tarde de abril, a mãe a chamou à sala de costura para uma conversa sobre o futuro. Eleonora disse, por cima da agulha de bordar:', 0.25),
 ('u20', 'EL', 'A temporada começa em junho. A senhora Frederiksen já confirmou o baile de abertura. Todas as famílias com filhas debutantes foram convidadas. Você está incluída, sertamenti.', 0.4),
 ('u21', 'N', 'Aurora repetiu, como quem repete uma sentença de morte:', 0.2),
 ('u22', 'AU', 'Sertamenti.', 0.35),
 ('u23', 'EL', 'Não faça drama, Aurora.', 0.3),
 ('u24', 'AU', 'Eu não estou fazendo drama. Estou repetindo o que a senhora disse.', 0.45),
 ('u25', 'N', 'Eleonora pousou o bordado no colo. Era um sinal: quando ela pousava o bordado, a conversa deixava de ser casual. Disse, e a voz não tremeu, mas diminuiu:', 0.25),
 ('u26', 'EL', 'Aurora. Eu sei que este não é o momento que você imaginava para o seu debute. Eu sei que você gostaria que Aarav estivesse aqui. Eu também gostaria. Mas ele não está. E a vida não parou de acontecer porque ele se foi, por mais que a gente quisesse que tivesse parado.', 0.5),
 ('u27', 'N', 'Aurora olhou para as mãos fechadas no colo, os nós dos dedos claros sob a pele escura. A mãe continuou:', 0.25),
 ('u28', 'EL', 'Seu pai quer que você tenha a temporada que merece. E eu também. Você é bonita, Aurora. Sei que a cidade nem sempre soube o que fazer com a sua aparência, mas...', 0.2),
 ('u29', 'AU', 'Mamãe. Por favor.', 0.45),
 ('u30', 'N', 'Eleonora se calou, estudou a filha, e retomou o bordado:', 0.25),
 ('u31', 'EL', 'Está bem. Vamos à modista na semana que vem. Três vestidos, no mínimo. E não, não vou deixar Fru Dahl escolher os tecidos de novo. Da última vez ela escolheu aquele tafetá horrível que fazia você parecer um repolho embrulhado.', 0.45),
 ('u32', 'N', 'Aurora quase sorriu. Quase. E então perguntou, e se arrependeu no mesmo instante, porque a pergunta revelava que ela pensava nele:', 0.25),
 ('u33', 'AU', 'E o Joshua? Ele vai participar da temporada?', 0.4),
 ('u34', 'EL', 'Naturalmente. Seu pai vai apresentá-lo à sociedade. Ele precisa de conexões, se quer entrar na universidade e na vida pública. E, morando na nossa casa, vai ser associado à nossa família.', 0.3),
 ('u35', 'N', 'Uma pausa milimétrica. E a mãe perguntou:', 0.2),
 ('u36', 'EL', 'Por que pergunta?', 0.35),
 ('u37', 'AU', 'Curiosidade.', 0.3),
 ('u38', 'N', 'Disse Aurora, num tom que pretendia ser casual e que soou como qualquer coisa menos casual. Eleonora respondeu só:', 0.2),
 ('u39', 'EL', 'Hum.', 0.4),
 ('u40', 'N', 'E aquela expressão, o hum de Eleonora, era perigosa. Na boca de Eleonora, era o som de uma mãe que viu alguma coisa e decidiu guardar a informação para depois. Aurora mudou de assunto. Falaram de tecidos, sapatos, penteados. Mas por dentro ela pensava em Josh na cozinha, com o cabelo despenteado e os punhos dobrados. E pensava que a temporada, com ele circulando pelos mesmos salões, seria muito mais complicada do que vestidos.', 0.8),
 ('u41', 'N', 'O primeiro evento a reunir os dois não foi um baile. Foi algo menor e mais traiçoeiro: um chá na casa da senhora Mikkelsen, esposa de um comerciante aliado do pai, mãe de três filhas em idade de casar, e uma força da natureza disfarçada de senhora baixinha de sorriso doce. Na teoria, os chás dela eram encontros para falar de música e bordado. Na prática, eram campos de batalha onde se negociavam casamentos e se destruíam reputações com a mesma elegância com que se servia o chá.', 0.4),
 ('u42', 'N', 'Aurora ia àqueles chás desde os catorze anos, e odiava cada segundo. Não pelo chá. Pelos olhares. Aqueles olhares que duravam um segundo a mais que o normal, como se as pessoas tentassem montar um quebra-cabeça cujas peças não se encaixavam. A filha do senhor Svensson: nem branca, nem morena, nada que se pudesse nomear. Bonita, sim, todos concordavam. Mas bonita de um jeito que deixava a cidade sem saber onde colocá-la. Aurora aprendera a erguer o queixo e a sorrir o sorriso perfeito que a mãe lhe ensinara. Aprendera a fingir tão bem que não se importava que às vezes quase acreditava.', 0.5),
 ('u43', 'N', 'Mas naquela tarde o chá tinha um ingrediente novo. Josh. O pai decidira apresentar o afilhado à sociedade antes da temporada, e Josh não protestou: aceitou com a mesma naturalidade com que se aceita a chuva. Foram na carruagem da família, os pais no banco da frente, Aurora e Josh atrás. Entre os dois, quarenta centímetros exatos. Aurora sabia, porque sentia cada um deles, como se sente a distância entre a mão e uma chama.', 0.4),
 ('u44', 'N', 'Josh estava de casaco novo, azul-marinho, ainda duro de tão pouco usado. E o azul fazia algo estranho com os olhos dele. Aurora nunca reparara que eles não eram só verdes: iam do musgo ao esmeralda conforme a luz. Ele também tinha feito a barba, e o rosto, descobriu ela com uma irritação que não sabia onde guardar, era escandalosamente bem construído. Maxilar marcado, maçãs altas, e um nariz com uma leve assimetria na ponta, quebrado talvez em algum trabalho da fazenda, que impedia a perfeição e, por isso mesmo, tornava o rosto mais interessante. Aurora olhou pela janela. E perguntou, de verdade, sem cortesia nenhuma:', 0.25),
 ('u45', 'AU', 'Está nervoso?', 0.35),
 ('u46', 'N', 'Josh olhou para ela, surpreso, e admitiu:', 0.2),
 ('u47', 'JOSH', 'Um pouco. Eu nunca fui a um chá.', 0.3),
 ('u48', 'AU', 'Nunca?', 0.3),
 ('u49', 'JOSH', 'No campo, chá é uma bebida. Não é um evento.', 0.45),
 ('u50', 'N', 'Aurora quase riu. Disfarçou o riso num sopro mais forte pelo nariz. E, sem saber por quê, já que não devia nada a ele, começou a explicar:', 0.25),
 ('u51', 'AU', 'As regras são simples. Cumprimente a anfitriã primeiro, sempre. Aceite o chá, mesmo que não goste. Não fale de política nem de dinheiro. Se uma senhora perguntar da sua família, seja breve e elogioso. E se uma moça fizer uma pergunta pessoal, responda com outra pergunta. Elas adoram falar de si mesmas.', 0.45),
 ('u52', 'N', 'Josh a olhou com algo que parecia reconhecimento, como quando se encontra, em terra estrangeira, alguém que fala o mesmo idioma. Disse:', 0.2),
 ('u53', 'JOSH', 'Obrigado.', 0.3),
 ('u54', 'AU', 'Não me agradeça. Estou protegendo a reputação da minha família, não a sua pessoa.', 0.45),
 ('u55', 'N', 'Era mentira, e tão transparente que Aurora quase corou. Mas Josh não contestou. Ficou olhando para as próprias mãos, grandes e calejadas, que não combinavam com o casaco novo. E Aurora reconheceu, com uma pontada no peito, o que havia na postura dele: vulnerabilidade. Ele estava entrando num mundo que não era o dele, um mundo generoso com quem se encaixa e implacável com quem não. Josh não se encaixava. Assim como ela. O pensamento a pegou desprevenida. Ela o espantou como quem espanta um inseto. Mas a picada já estava feita. E coçava.', 0.8),
 ('u56', 'N', 'O chá da senhora Mikkelsen foi, tecnicamente, um sucesso. Para Aurora, foi uma tortura requintada servida em porcelana fina. Josh foi impecável. Cumprimentou a anfitriã primeiro, aceitou o chá, segurou a xícara do jeito certo. E respondeu às senhoras com uma naturalidade desarmante, porque não tentava encantar ninguém: era simplesmente honesto. Falou do campo sem romantizar nem se diminuir, da mãe com respeito, dos irmãos com humor seco.', 0.4),
 ('u57', 'N', 'A senhora Mikkelsen, com o brilho nos olhos de quem avalia um pretendente para as filhas, perguntou:', 0.2),
 ('u58', 'MIK', 'E o senhor veio estudar?', 0.3),
 ('u59', 'JOSH', 'Sim, senhora. Na universidade.', 0.3),
 ('u60', 'MIK', 'Ciências? Direito?', 0.3),
 ('u61', 'JOSH', 'Ainda estou decidindo. O senhor Svensson tem sido generoso em me orientar.', 0.4),
 ('u62', 'N', 'A senhora Mikkelsen olhou para o pai de Aurora, do outro lado da sala, com uma admiração real e também calculada, e disse:', 0.2),
 ('u63', 'MIK', 'O senhor Svensson é um homem extraordinário. E o senhor é afilhado dele. Praticamente um filho.', 0.5),
 ('u64', 'N', 'Aurora sentiu o maxilar endurecer. Praticamente um filho. Ali estava a frase que a cidade inteira diria por meses: o substituto, o rapaz que mora na casa onde antes morava Aarav. Mas Josh pareceu desconfortável. Uma tensão nos ombros, um desvio no olhar. E respondeu, com delicadeza:', 0.25),
 ('u65', 'JOSH', 'O senhor Svensson é meu padrinho. E um mentor generoso. Sou grato por estar na casa dele.', 0.5),
 ('u66', 'N', 'Nada sobre ser filho. Nada sobre substituir ninguém. Uma resposta precisa como um corte de bisturi. Aurora olhou para ele. E percebeu, com um desconforto que se instalou no estômago como chá frio, que os dois tinham o mesmo sorriso de sobrevivência.', 0.8),
 ('u67', 'N', 'Mas o verdadeiro problema do chá foram as filhas da senhora Mikkelsen: Frederikke, de dezenove anos, Lovise, de dezessete, e Astrid, de quinze. Loiras, bonitas na medida certa, e com um faro para rapazes novos que rivalizava com o de um falcão para coelhos em campo aberto. Josh era o coelho. Frederikke, a mais velha e mais ousada, foi a primeira. Atravessou o salão, parou diante dele com um sorriso genuinamente bonito, e perguntou:', 0.25),
 ('u68', 'FRED', 'Senhor Russel, minha mãe diz que o senhor é do interior da Zelândia. Eu adoro o campo. Diga-me, como são as noites de primavera fora da cidade?', 0.4),
 ('u69', 'N', 'Aurora, da poltrona junto à janela, reconheceu a manobra: noites, primavera, campo, tudo junto, uma imagem que uma moça esperta criava de propósito. Mas Josh não pareceu perceber. Respondeu com a mesma naturalidade:', 0.25),
 ('u70', 'JOSH', 'Silenciosas. Muito escuras. Mas quando o céu está limpo, as estrelas compensam. No campo não há lampiões, então o céu fica... cheio.', 0.35),
 ('u71', 'FRED', 'Que coisa mais poética.', 0.4),
 ('u72', 'N', 'Josh coçou a nuca, um gesto tão fora de lugar naquele salão que era irresistivelmente sincero. Logo chegou Lovise, a do meio, para ajudar a irmã:', 0.25),
 ('u73', 'LOV', 'Frederikke, não monopolize o convidado. Senhor Russel, soube que vai entrar na universidade. Meu irmão mais velho estuda direito. Talvez se conheçam.', 0.4),
 ('u74', 'N', 'E por fim apareceu Astrid, a caçula, com a desculpa frágil de oferecer outro biscoito. Aurora assistiu a tudo da poltrona, com o chá na mão e o sorriso de porcelana pronto. Mas por dentro havia algo quente e apertado entre as costelas: quando Frederikke tocou o braço dele ao rir, quando Lovise se inclinou perto demais, quando Astrid corou com um simples obrigado.', 0.4),
 ('u75', 'N', 'Não era ciúme. Não podia ser. Ciúme seria querer alguma coisa, e Aurora não queria nada de Josh Russel. Absolutamente nada. Era zelo. Sim. Zelo pela reputação da família. Era só isso. Aurora tomou o último gole de chá. Estava frio.', 0.8),
 ('u76', 'N', 'Na carruagem de volta, o pai estava satisfeito, e disse:', 0.2),
 ('u77', 'RAJ', 'Você se saiu bem, Joshua. A senhora Mikkelsen ficou impressionada. Disse que você tem modos surpreendentemente polidos para alguém do campo.', 0.35),
 ('u78', 'N', 'Josh repetiu, seco:', 0.2),
 ('u79', 'JOSH', 'Surpreendentemente.', 0.35),
 ('u80', 'N', 'E o pai quase riu.', 0.25),
 ('u81', 'RAJ', 'A sociedade de Copenhague tem seus preconceitos. Você vai aprender a navegar por eles. O importante é que te viram, te conheceram e gostaram. No próximo evento, você não será mais um estranho.', 0.4),
 ('u82', 'N', 'Eleonora acrescentou, com a precisão de sempre:', 0.2),
 ('u83', 'EL', 'As meninas Mikkelsen, com certeza, gostaram.', 0.3),
 ('u84', 'N', 'O pai advertiu, suave:', 0.2),
 ('u85', 'RAJ', 'Eleonora, por favor.', 0.3),
 ('u86', 'EL', 'Estou constatando um fato, Ráge. Frederikke, em particular, pareceu bastante interessada.', 0.5),
 ('u87', 'N', 'Josh não disse nada. Aurora olhou pela janela. E o sol de abril, traiçoeiro, dourava o vidro de um jeito que tornava impossível não ver o rosto de Josh refletido nele. Ele estava olhando para ela. Para o reflexo dela no vidro. Os olhos se encontraram ali: o reflexo de mel no reflexo de verde. Por um instante tão breve que depois Aurora se perguntaria se o inventara, algo passou entre eles. Não uma faísca. Um reconhecimento. Como dois estrangeiros que se olham e percebem que falam a mesma língua. Josh desviou primeiro.', 0.8),
 ('u88', 'N', 'Naquela noite, Aurora desceu à cozinha mais cedo que o habitual. Não para fazer chá. Para verificar alguma coisa que não queria admitir que verificava. A cozinha estava vazia, escura, fria. Só o gato dormia no canto. Ela se sentiu ridícula. O que esperava encontrar? Nada. Não esperava nada. Subiu, deitou-se, fechou os olhos.', 0.4),
 ('u89', 'N', 'E pensou, contra a própria vontade, no jeito como ele corrigira a senhora Mikkelsen. Meu padrinho. Um mentor generoso. Nada sobre ser filho. Nada sobre substituir. Ele não tentava ocupar o lugar de Aarav. Nunca tentara. Aurora abraçou o travesseiro. E um pensamento pequeno e perigoso, como uma semente caindo em terra boa, se formou na cabeça dela: talvez eu tenha sido injusta. Não disse mais nada, nem para si mesma. Mas sementes não precisam de permissão para germinar.', 0.0),
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
            sf.write(seg_f, a, SR); src="novo"; time.sleep(2)
        parts.append(a)
        if gap>0: parts.append(sil(gap))
        print("ok", slug, src, f"{len(a)/SR:.1f}s")
    mix = np.concatenate(parts)
    pk = float(np.max(np.abs(mix)) or 1.0)
    if pk>0.97: mix *= 0.97/pk
    sf.write(f"{SCR}/cap04-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap04-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap04-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
