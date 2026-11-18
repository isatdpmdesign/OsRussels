import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts13"
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
 ('d001', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo treze: A distância.', 1.2),
 ('d002', 'N', 'Neste capítulo, voltamos a ver tudo pelos olhos de Josh. No capítulo anterior, Aurora descobriu que os conselhos dele tinham afastado, um a um, todos os seus pretendentes. Entrou no quarto dele, chamou-o de covarde, e pediu distância. Sem cozinha às seis da manhã. Sem conselhos. Sem olhares no jantar.', 0.6),
 ('d003', 'N', 'Josh obedeceu. Não porque fosse fácil. Nada que envolvesse Aurora era fácil, e Josh já tinha se conformado com o fato de que fácil e Aurora moravam em hemisférios opostos do vocabulário dele. Obedeceu porque ela pediu. Com os olhos de pedra, a voz de lâmina, e as mãos que tremiam enquanto ela fingia que não. E Josh entendeu que o tremor era o que aquilo custava. A raiva era o combustível. O tremor era o preço. Ele devia a ela a distância que ela pediu. Então se afastou.', 0.4),
 ('d004', 'N', 'Não desceu para a cozinha. Às cinco e quarenta e cinco, a hora em que o corpo dele acordava em qualquer lugar do mundo, Josh abriu os olhos e ficou deitado, ouvindo a casa. E às seis e dez, como um relógio, os passos de Aurora no corredor. Leves. Rápidos. Descendo a escada. Entrando na cozinha. Sozinha. Josh fechou os olhos, apertou os lençóis, e ficou ali até os passos voltarem, às seis e quarenta, e passarem pela porta dele.', 0.4),
 ('d005', 'N', 'Só então se levantou, e desceu para o café da manhã oficial, quando a família já estava sentada, e a presença de Aurora do outro lado da mesa era inevitável, e suportável apenas porque havia uma mesa inteira de distância entre eles. Aurora não olhou para ele. Nem uma vez. Josh contou, porque contar era o jeito dele de transformar dor em dados. Em cinco dias de distância, Aurora olhou para ele zero vezes. Zero. O número era preciso e brutal, e Josh o carregava como uma pedra no bolso.', 0.4),
 ('d006', 'N', 'No escritório, com o padrinho, a rotina continuou. Hegel. Kant. As discussões sobre constituição que Josh amava, e que agora conduzia com metade da atenção, porque a outra metade calculava se Aurora já tinha tomado o chá, e se o gato Kóngen tinha feito companhia a ela. O padrinho notou. Não de imediato, ocupado com um carregamento de especiarias atrasado no porto. Mas no terceiro dia, numa pausa sobre Rousseau, tirou os óculos, limpou-os com o lenço, e olhou para Josh com aqueles olhos escuros que viam através de paredes:', 0.25),
 ('d007', 'RAJ', 'Você está distraído, Joshua.', 0.2),
 ('d008', 'JOSH', 'Desculpe, senhor.', 0.2),
 ('d009', 'RAJ', 'Me chame de Ráge.', 0.2),
 ('d010', 'JOSH', 'Desculpe, Ráge.', 0.3),
 ('d011', 'RAJ', 'Você e a Aurora brigaram?', 0.4),
 ('d012', 'N', 'A pergunta foi direta. Sem rodeio. Josh sentiu o sangue gelar e ferver ao mesmo tempo. E negou:', 0.2),
 ('d013', 'JOSH', 'Não.', 0.3),
 ('d014', 'RAJ', 'Não minta pra mim, rapaz. Não nesta sala. Esta sala é o único lugar desta casa onde eu exijo verdade absoluta, e você sabe disso.', 0.4),
 ('d015', 'N', 'Josh olhou para o homem que o acolheu, que o ensinava, que o tratava, e ele engolia a palavra toda vez que ela subia, como filho. O homem por cuja filha Josh estava apaixonado, e cuja confiança ele estava traindo por omissão. E escolheu a palavra como quem manuseia explosivo:', 0.2),
 ('d016', 'JOSH', 'A gente teve um... desentendimento. Uma coisa que eu fiz incomodou ela. Ela pediu distância. Eu estou respeitando.', 0.2),
 ('d017', 'RAJ', 'E o que você fez?', 0.2),
 ('d018', 'JOSH', 'Dei um conselho que eu não devia ter dado. Com intenções que não eram... puras.', 0.4),
 ('d019', 'N', 'O padrinho ficou em silêncio. O relógio de bronze do escritório bateu duas vezes, com a autoridade de um juiz. E quando ele falou, a voz tinha mudado. Não era mais a voz do mentor. Era a voz do pai de Aurora:', 0.2),
 ('d020', 'RAJ', 'Joshua. Eu não vou perguntar mais do que você está preparado pra dizer. Mas eu vou dizer uma coisa, e quero que você ouça com atenção.', 0.3),
 ('d021', 'N', 'Josh assentiu. E o padrinho disse, sem drama, com a simplicidade de quem diz um fato tão fundamental que enfeitá-lo seria diminuí-lo:', 0.2),
 ('d022', 'RAJ', 'A Aurora é a coisa mais preciosa que eu tenho no mundo. Depois que o Aarav se foi, a Aurora é tudo. E eu trouxe você pra esta casa porque confio em você. Porque eu confiava no seu pai. Porque olhei pro filho do Henrik Russel e vi um homem decente.', 0.5),
 ('d023', 'N', 'Decente. A palavra caiu sobre Josh como um peso. Era o que ele queria ser. O que ele acreditava ser, até dois meses antes. E agora a palavra parecia um casaco que não servia mais. Ele disse, e acrescentou, porque a honestidade era a única coisa que ainda era dele:', 0.2),
 ('d024', 'JOSH', 'Eu sou. Ou estou tentando ser.', 0.4),
 ('d025', 'N', 'O padrinho o olhou mais um momento. Pôs os óculos. Abriu o livro, e voltou a Rousseau:', 0.2),
 ('d026', 'RAJ', 'O capítulo oito.', 0.35),
 ('d026b', 'RAJ', 'Diga em tom calmo de professor: Leia em voz alta.', 0.4),
 ('d027', 'N', 'Ele leu. E a voz não tremeu. Mas debaixo da mesa as mãos estavam fechadas com tanta força que as unhas deixaram marcas nas palmas.', 1.0),
 # --- os dias ---
 ('d028', 'N', 'Os dias passaram com a lentidão de quem tem consciência de cada hora. Josh reorganizou a rotina em volta da ausência de Aurora, como um rio contorna uma pedra. Não descia para a cozinha. Não ia ao jardim: o jardim era dela, e a distância incluía as roseiras, a pérgola e o banco envernizado. Não ficava na biblioteca depois do jantar. Subia direto para o quarto, com os livros, o silêncio, e a gaveta que guardava duas cartas não entregues e uma verdade escrita que ninguém leria.', 0.4),
 ('d029', 'N', 'A casa sentiu a mudança. Casas sempre sentem. E Fru Larsen, a cozinheira, foi a primeira a notar. Claro que foi. No quarto dia, quando Josh desceu para o café, ela estava na sala de jantar supervisionando Helle, a criada, coisa que nunca fazia, com o pano de prato no ombro e o olhar fixo em Josh, como quem tira uma radiografia. Ele cumprimentou:', 0.2),
 ('d029b', 'JOSH', 'Bom dia, Fru Larsen.', 0.3),
 ('d029c', 'N', 'E ela respondeu só com um som:', 0.2),
 ('d030', 'LARSEN', 'Diga como um resmungo de julgamento, curto: Hm.', 0.3),
 ('d031', 'N', 'O hm de Fru Larsen era diferente do hm de Eleonora. O de Eleonora era observação guardada para uso futuro. O de Fru Larsen era julgamento imediato, sentença proferida e executada num só som. Ela repetiu, e saiu para a cozinha. Aurora entrou dois minutos depois, sentou, e não olhou para ele. O café seguiu como seguia havia cinco dias, em silêncio. Helle trouxe mais pão. E, ao se inclinar para pôr a cesta na mesa, disse para Josh, bem baixinho, com o rubor de quem comete um ato de rebelião doméstica:', 0.2),
 ('d032', 'HELLE', 'Diga num tom bem baixo e tímido, sem sussurrar, em português do Brasil: O Kóngen está com saudade do senhor na cozinha.', 0.4),
 ('d033', 'N', 'Helle ficou vermelha até a raiz do cabelo, largou a cesta e fugiu para a cozinha como quem acaba de entregar um segredo de Estado. Josh quase sorriu. Porque a mensagem, fosse de Helle, de Fru Larsen ou do gato, era clara: a cozinha sentia falta dele. E se a cozinha sentia falta, alguém na cozinha sentia falta. Porque Kóngen era muitas coisas, mas sentimental não era uma delas.', 1.0),
 # --- a carta ---
 ('d034', 'N', 'No sexto dia, Josh escreveu à mãe. A carta de verdade. A que ele mandaria:', 0.3),
 ('d035', 'JOSH', 'Querida mãe. Eu fiz uma coisa errada, e estou pagando por isso. Não posso contar os detalhes, não nesta carta, talvez nunca. Mas eu traí a confiança de alguém que confiava em mim, e agora essa pessoa me pediu distância, e eu estou obedecendo. A senhora diria que obedecer não basta. E tem razão. Obedecer é o mínimo. Essa pessoa merece que eu entenda por que eu fiz o que fiz, e que eu garanta, a ela e a mim, que não vou fazer de novo.', 0.3),
 ('d036', 'JOSH', 'Eu sei por que fiz. A senhora também sabe, porque lê o que eu não escrevo com a mesma clareza com que lê o que eu escrevo. A questão não é o porquê. É o que eu faço agora. A senhora diria: faz o que é certo, Josh. E o que é certo geralmente é o que é difícil. Pois é. É difícil.', 0.3),
 ('d037', 'JOSH', 'Saudade de todos. Diz pro Joseph descansar. Diz pro Dylan que cêrca não se conserta sozinha. Diz pra Meridiana que as pereiras agradecem a conversa. E diz pro Matias que ser forte é diferente de não chorar, e que ele pode fazer as duas coisas. Com amor, Josh.', 0.5),
 ('d038', 'N', 'Selou, pôs na pilha, e entregou a Helle na sexta-feira. E esperou.', 1.0),
 # --- a canção ---
 ('d039', 'N', 'No décimo dia, algo mudou. Josh estava no escritório com o padrinho, numa tarde de quinta, discutindo Hegel, quando ouviu algo vindo do jardim. Não um barulho. Uma voz. Aurora estava cantando. Ele nunca a tinha ouvido cantar. Em quatro meses de convivência, de manhãs na cozinha, jantares, corredores, bailes, carruagens e silêncios de todas as texturas, Aurora nunca tinha cantado. Nem uma vez. Nem para si mesma.', 0.4),
 ('d040', 'N', 'A voz vinha pela janela entreaberta. Baixa. Quase um murmúrio. Uma melodia que Josh não reconheceu: talvez dinamarquesa, talvez algo que Aarav cantava, talvez algo que ela inventou. Era a mesma voz de sempre, grave para o tamanho dela, rouca, como seda sobre madeira. Mas cantando era outra coisa. Cantando era aberta. O padrinho parou de ler. Tirou os óculos. Olhou para a janela.', 0.4),
 ('d041', 'N', 'E Josh viu no rosto dele, no rosto severo e controlado de Raj Svensson, que Josh nunca tinha visto chorar, algo que quebrou alguma coisa dentro dele. O padrinho estava sorrindo. Um sorriso tão pequeno que talvez fosse só a memória mexendo nos músculos do rosto. Mas os olhos escuros, que guardavam bibliotecas inteiras, estavam úmidos. E ele disse, quase para si mesmo:', 0.2),
 ('d042', 'RAJ', 'Diga com a voz embargada e contida, quase para si mesmo: Ela não cantava desde que o Aarav partiu.', 0.6),
 ('d042b', 'N', 'E acrescentou, sem tirar os olhos da janela:', 0.2),
 ('d042c', 'RAJ', 'Diga com a voz embargada e contida: Hoje seria o aniversário dele. O Aarav faria vinte e dois anos. Ela deve estar cantando pro irmão.', 0.6),
 ('d043', 'N', 'Ficaram em silêncio. A voz de Aurora continuou, subindo, descendo, e Josh a gravou nota por nota no lugar onde guardava as coisas que importavam. A música parou. O jardim ficou em silêncio. O padrinho pôs os óculos, abriu o livro, e disse, com a voz perfeitamente controlada:', 0.2),
 ('d044', 'RAJ', 'Capítulo dez. Continue.', 0.4),
 ('d045', 'N', 'Josh continuou. Mas a melodia ficou nele. Grudada como pólen. Como o cheiro de jasmim que não saía do corredor, por mais que as janelas ficassem abertas.', 1.0),
 # --- a despensa ---
 ('d046', 'N', 'Naquela mesma noite, a distância rachou. Não por decisão. Por acidente, ou pelo que parecia acidente. Era noite, perto da meia-noite, e Josh estava acordado, porque o sono tinha virado um luxo que ele não podia pagar. Desceu para a cozinha. Não para encontrar Aurora: ela estaria dormindo, e a cozinha de madrugada não era de nenhum dos dois. Desceu porque precisava de água. De movimento. De qualquer coisa que não fosse o teto e o cheiro fantasma de jasmim.', 0.4),
 ('d047', 'N', 'A cozinha estava escura. Josh acendeu uma vela, encheu um copo de água e bebeu de pé, encostado no balcão. E então ouviu. Um som vindo da despensa, o cômodo pequeno e frio ao lado do fogão, onde Fru Larsen guardava as provisões. A porta estava entreaberta. E de dentro vinha um som que Josh reconheceria em qualquer lugar, em qualquer vida. Choro. Não um soluço alto. Um choro contido. Engolido, abafado, apertado até virar quase silêncio. Quase. Mas não.', 0.4),
 ('d048', 'N', 'Josh pousou o copo e empurrou a porta. Aurora estava sentada no chão frio de pedra, entre sacos de farinha e caixas de chá, os joelhos contra o peito, os braços em volta das pernas, o rosto escondido nos joelhos. O cabelo solto caía em volta dela como uma cortina escura. O corpo tremia. Ela ergueu o rosto. E na luz fraca da vela, Josh viu os olhos cor de mel inundados. As bochechas molhadas. Os lábios tremendo.', 0.4),
 ('d049', 'N', 'Não era choro por ele. Josh soube na hora. Não era a briga, nem os conselhos, nem a confiança traída. Era algo mais antigo. Mais fundo. O choro de quem perdeu alguém que não pode ser substituído e que, de vez em quando, no meio da noite, no fundo de uma despensa onde ninguém vê, deixa a perda doer inteira. Arav. Aurora chorava por Arav.', 0.4),
 ('d050', 'N', 'Josh ficou na porta um segundo. Dois. O tempo de uma decisão que não era decisão, porque o corpo já sabia o que fazer. Entrou. E sentou no chão, ao lado dela. Não de frente: de lado. Ombro a ombro. Sem tocar. Sem falar. Sem olhar para ela. Aurora não pediu que ele saísse. Nem que ficasse. Não levantou a muralha. Continuou chorando em silêncio, e Josh deixou que chorasse. Cinco minutos. Dez. Pela primeira vez em meses, ele não contou.', 0.4),
 ('d051', 'N', 'O choro foi diminuindo, como chuva que vai perdendo a força. E então, sem aviso, a cabeça dela tombou. Para o lado. Para o ombro dele. O peso era leve. O cabelo dela, com cheiro de jasmim, caiu sobre o braço dele. E Aurora ficou ali, encostada, os olhos fechados, a cabeça no ombro do rapaz que a tinha manipulado, que ela tinha mandado embora, e que apareceu no meio da noite e sentou no chão sem pedir nada.', 0.4),
 ('d052', 'N', 'Josh não se mexeu. Não ousou nada que alterasse aquele equilíbrio, tão frágil que uma respiração mais forte poderia quebrar. Ficou imóvel, com o coração batendo tão forte que ele tinha certeza de que ela sentia através da camisa. Depois de um tempo que ele não mediu, Aurora ergueu a cabeça, limpou o rosto com as costas da mão, e disse, olhando para a frente, com a voz crua, lavada, sem nenhuma camada:', 0.2),
 ('d053', 'AU', 'Diga num tom baixo e cansado de quem chorou, sem sussurrar, em português do Brasil: Era o aniversário dele. O Aarav faria vinte e dois anos hoje.', 0.5),
 ('d054', 'N', 'Ele sentiu o peito apertar. E disse:', 0.2),
 ('d055', 'JOSH', 'Diga com suavidade, num tom mais baixo, sem sussurrar: Eu sei.', 0.5),
 ('d056', 'N', 'Aurora se virou e olhou para ele pela primeira vez em dez dias. E os olhos inchados, vermelhos, sem armadura nenhuma, fizeram a pergunta que a boca não fez: como você sabe? Ele explicou:', 0.2),
 ('d057', 'JOSH', 'O seu pai comentou hoje à tarde. No escritório, enquanto você cantava no jardim. Eu guardei.', 0.5),
 ('d058', 'N', 'Eu guardei. Duas palavras que resumiam quem Josh era. O rapaz que guardava tudo. Até a data do aniversário de um morto que ele nunca conheceu, porque o morto era importante para alguém importante para ele. Aurora olhou para ele por um longo momento. O mais longo de todos. Sem estratégia, sem técnica, sem lição de flerte. Só uma moça e um rapaz no chão de uma despensa no meio da noite, olhando um para o outro com a honestidade de quem não tem mais força para fingir. Ela disse:', 0.2),
 ('d059', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Obrigada, Josh.', 0.2),
 ('d060', 'JOSH', 'Não precisa agradecer.', 0.2),
 ('d061', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Preciso, sim. Porque eu pedi distância, e você estava obedecendo. Mas quando me viu chorando, resolveu chegar perto pra me confortar.', 0.4),
 ('d062', 'N', 'Ela disse aquilo como se a frase explicasse tudo. E explicava. Então ele disse:', 0.2),
 ('d063', 'JOSH', 'Eu ouvi você chorando. Distância não é abandono. Eu posso te dar espaço e ainda estar aqui quando você precisa. As duas coisas existem ao mesmo tempo.', 0.5),
 ('d064', 'N', 'Aurora ficou em silêncio. Depois assentiu. E devagar, como quem testa a temperatura da água, encostou o ombro no ombro dele de novo. Não a cabeça. Só o ombro. Uma ponte feita do menor material possível. E ficaram assim. Na cozinha, a vela ardia. Kóngen dormia. O relógio de pêndulo batia as horas, indiferente aos dramas humanos. E lá fora, no jardim, as roseiras de Aarav dormiam sob a noite de julho, tão cheias, tão vermelhas, tão vivas, que ninguém adivinharia que tinham nascido de mãos que já não existiam.', 0.4),
 ('d065', 'N', 'Quando a vela apagou, os dois subiram em silêncio. No corredor escuro, os passos lado a lado, mais perto do que os quarenta centímetros da carruagem, quase juntos, duas sombras que o escuro fundia numa só. Na porta do quarto dela, pararam. E Aurora disse, e a voz, pela primeira vez em dez dias, não tinha lâmina:', 0.2),
 ('d066', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num tom sincero e contido, sem animação: Boa noite, Josh.', 0.2),
 ('d067', 'JOSH', 'Boa noite, Aurôra.', 0.5),
 ('d068', 'N', 'Ela entrou. O clique suave da porta. Josh foi para o quarto, mas não se deitou. Abriu a gaveta da escrivaninha e pegou a carta não enviada, a carta do eu estou apaixonado por ela, mãe. Não rasgou. Pôs de volta. Mas pegou outra folha, e escreveu uma única frase, no meio do papel, sem destinatário e sem assinatura. Uma frase só para ele: Distância não é abandono. Dobrou a folha e guardou na gaveta. E dormiu, pela primeira vez em dez dias, sem sonhar com nada. O que talvez seja o tipo mais gentil de descanso que existe.', 0.0),
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
    sf.write(f"{SCR}/cap13-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap13-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap13-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
