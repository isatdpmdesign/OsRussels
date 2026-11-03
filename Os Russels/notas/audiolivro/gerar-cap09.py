import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts9"
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
BR = "Diga em português do Brasil, com sotaque brasileiro: "
EL_ = "Diga com voz de senhora madura, grave e contida: "
SEG = [
 ('z01', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo nove: O que se ensina e o que se aprende.', 1.2),
 ('z02', 'N', 'Este capítulo volta aos olhos de Josh. Desde aquela primeira manhã no jardim, as aulas tinham continuado, em segredo: depois da aula de francês de Aurora, antes do almoço, quarenta minutos só deles, sob a pérgola. Ele ensinando o que tinha prometido: como os rapazes funcionam. Ela aprendendo depressa demais.', 0.6),
 ('z03', 'N', 'As aulas viraram o centro secreto dos dias de Josh. Não o centro oficial. Oficialmente, o centro era o estudo. As tardes no escritório do padrinho, onde Montesquiê dava lugar a Rousseau, e Rousseau a Hegel, e Josh sentia o cérebro crescer como um músculo que finalmente encontra o peso certo. As manhãs na biblioteca. As noites na escrivaninha, com as cartas para a mãe ficando mais longas e mais vagas ao mesmo tempo: mais longas sobre filosofia e a universidade que se aproximava, mais vagas sobre todo o resto.', 0.4),
 ('z04', 'N', 'Mas o centro de verdade, o eixo invisível que organizava as horas, eram aqueles quarenta minutos em que o jardim era só deles, e o mundo ficava do outro lado do muro de hera. A segunda aula foi sobre conversa. Josh estava sentado no banco de Aarav, e Aurora de pé diante dele, olhando-o de cima, o que fazia algo estranho com a respiração de Josh. Ele disse:', 0.25),
 ('z05', 'JOSH', 'O erro mais comum é tentar ser interessante.', 0.2),
 ('z06', 'AU', BR+'E o que se deveria tentar?', 0.2),
 ('z07', 'JOSH', 'Estar interessada. As pessoas confundem as duas coisas. Acham que, pra atrair alguém, precisam ser brilhantes, engraçadas, impressionantes. Mas a verdade é mais simples e mais difícil: precisam fazer a outra pessoa se sentir brilhante, engraçada e impressionante. E isso se faz com perguntas. Com escuta. Com silêncio na hora certa.', 0.3),
 ('z08', 'AU', BR+'Você está descrevendo manipulação.', 0.4),
 ('z09', 'N', 'Josh pensou, e respondeu:', 0.2),
 ('z10', 'JOSH', 'Estou descrevendo atenção. A diferença entre manipulação e atenção é a intenção. Se você presta atenção pra conseguir alguma coisa, é manipulação. Se presta atenção porque a pessoa merece, é generosidade. E generosidade é a coisa mais atraente que existe.', 0.4),
 ('z11', 'N', 'Aurora inclinou a cabeça. O sol de junho caiu sobre o cabelo dela, e Josh viu, pela centésima vez, a luz tirar tons de bronze e cobre das ondas escuras, como se houvesse fios de metal precioso trançados ali. Ela disse, com ironia:', 0.2),
 ('z12', 'AU', BR+'Então eu deveria ser generosa.', 0.2),
 ('z13', 'JOSH', 'Você já é generosa. Só esconde bem.', 0.4),
 ('z14', 'N', 'Aurora fez aquela cara que Josh tinha classificado como a de quando ela quer discordar e não acha argumento: sobrancelhas um pouco franzidas, lábios apertados, olhos estreitos. Era, sem querer, a expressão mais adorável do repertório dela. E Josh precisava parar de catalogar as expressões de Aurora Svensson como um naturalista classificando espécies. Ela pediu:', 0.2),
 ('z15', 'AU', BR+'Me dá um exemplo. De como seria uma conversa boa. Do tipo que faz um homem querer continuar conversando.', 0.4),
 ('z16', 'N', 'Josh olhou as roseiras, vermelhas e cheias, e depois para ela. Levantou do banco, ajeitou o casaco, pigarreou, e assumiu uma postura empertigada, a melhor imitação que conseguia de um cavalheiro da cidade. E disse, afetado:', 0.2),
 ('z17', 'JOSH', 'Diga com um tom formal e afetado, imitando um cavalheiro esnobe: Senhorita Svensson, que noite agradável. A senhorita aprecia a música?', 0.4),
 ('z18', 'N', 'Aurora apertou os lábios para segurar o riso. Josh sentiu uma satisfação desproporcional. Ela entrou no jogo, com uma seriedade desmentida pelo brilho nos olhos, e respondeu, formal:', 0.2),
 ('z19', 'AU', BR+'Sim, aprecio. E o senhor?', 0.3),
 ('z20', 'JOSH', 'Resposta educada. Correta. E completamente morta. Ninguém sabe o que fazer com e o senhor? É uma parede, não uma porta. Tenta de novo.', 0.4),
 ('z21', 'N', 'Aurora pensou. Josh viu as engrenagens. E viu ela morder o lábio de baixo, um gesto que ela fazia quando pensava, e que Josh desejava ardentemente que ela parasse de fazer, porque aquele lábio não era coisa que ele devesse ficar olhando com tanta atenção. Ela tentou de novo:', 0.2),
 ('z22', 'AU', BR+'A música é bonita, mas confesso que prefiro quando os violinos se calam e dá pra ouvir as conversas. As conversas numa festa são sempre mais interessantes que a orquestra.', 0.3),
 ('z23', 'N', 'E acrescentou que, aí, olharia para o rapaz e perguntaria:', 0.2),
 ('z24', 'AU', BR+'O senhor já ouviu alguma coisa interessante esta noite?', 0.5),
 ('z25', 'N', 'Josh ficou em silêncio. Ela perguntou, insegura: O que foi? Foi ruim? E ele respondeu:', 0.2),
 ('z26', 'JOSH', 'Não. Não foi ruim. Foi extraordinário.', 0.3),
 ('z27', 'AU', BR+'Extraordinário?', 0.2),
 ('z28', 'JOSH', 'Você acabou de fazer três coisas em cinco segundos. Mostrou personalidade, porque preferir conversa a música é uma opinião, e opinião atrai. Criou cumplicidade, porque transformou vocês dois em observadores da festa, o que é mais íntimo do que ser participante. E abriu uma porta, porque a pergunta é verdadeira, é pessoal, e faz o rapaz querer responder algo à altura dela.', 0.4),
 ('z29', 'N', 'Aurora absorveu aquilo com uma surpresa que parecia ser com a própria competência. Ou algo mais. Ela disse:', 0.2),
 ('z30', 'AU', BR+'Eu não pensei em nada disso. Eu só... disse o que eu diria.', 0.2),
 ('z31', 'JOSH', 'É isso. Você não precisa aprender a conversar. Precisa parar de se impedir de conversar.', 1.0),
 # --- terceira aula ---
 ('z32', 'N', 'A terceira aula foi sobre movimento. Estavam de pé, frente a frente, sob a pérgola. O cheiro das glicínias, àquela altura de junho, era quase embriagante: pesado, doce, insistente. Josh tentava ignorar o cheiro e se concentrar na aula. Tentava. Ele explicou:', 0.2),
 ('z33', 'JOSH', 'As pessoas subestimam o corpo. Acham que a conversa acontece com a boca. Mas noventa por cento do que a gente comunica é antes de abrir a boca. Como a gente entra num salão. Onde se coloca. A distância que mantém.', 0.3),
 ('z34', 'JOSH', 'No baile, você ficou encostada na parede a noite inteira. A parede é uma fortaleza. Diz: estou aqui, mas não quero ser abordada. O centro do salão é o contrário: diz estou disponível. O ideal é o meio. Perto de alguma coisa, uma mesa, uma coluna, um grupo, mas sem encostar. Com o corpo virado pro salão. E com espaço em volta. Espaço convida.', 0.4),
 ('z35', 'AU', BR+'Então eu deveria simplesmente ficar de pé no meio de um salão. Sozinha. Olhando pro nada.', 0.2),
 ('z36', 'JOSH', 'Não pro nada. Pra festa. Com interesse. Com aquele sorriso que você descobriu que tem. Com os ombros abertos, não cruzados. Olhando em volta como quem está se divertindo, e não como quem espera ser resgatada.', 0.2),
 ('z37', 'AU', BR+'Eu não espero ser resgatada.', 0.2),
 ('z38', 'JOSH', 'Eu sei. Mas a postura de parede diz que espera. E as pessoas leem o corpo antes de ler o rosto.', 0.4),
 ('z39', 'N', 'Aurora descruzou os braços. E Josh viu a mudança. Os ombros desceram. O peito se abriu. O queixo subiu meio centímetro. E de repente, sem mexer os pés, Aurora ocupou mais espaço. Como se tivesse ficado dois centímetros mais alta só por decidir que merecia. Ele disse, mais baixo do que pretendia:', 0.2),
 ('z40', 'JOSH', 'Assim.', 0.4),
 ('z41', 'N', 'E Josh percebeu, com um atraso que seria cômico se não fosse desesperador, que Aurora nunca tinha precisado de aulas. Precisava de permissão. Permissão para ser o que já era, magnética, inteligente, ferozmente presente, sem o peso do medo, da armadura e do luto. E ele estava dando essa permissão. Aula por aula. E cada aula a aproximava, não de um pretendente futuro num salão, mas dele. Do rapaz do campo que, na verdade, estava cavando a própria cova com entusiasmo e uma pá cada vez maior.', 0.4),
 ('z42', 'N', 'E na cabeça dele falou a voz da mãe, como sempre: O que você está fazendo, Josh? E ele respondeu, em pensamento: Estou destruindo a minha própria paz. E não consigo parar.', 1.0),
 # --- quarta aula ---
 ('z43', 'N', 'A quarta aula foi sobre vestir. Foi a mais difícil. Tecnicamente era simples. Mas emocionalmente era um campo minado. Josh escolheu as palavras com o cuidado de quem segura cristal:', 0.2),
 ('z44', 'JOSH', 'No baile, você usou verde escuro. E estava... adequado.', 0.3),
 ('z45', 'N', 'Aurora ergueu a sobrancelha, e repetiu:', 0.2),
 ('z46', 'AU', BR+'Adequado?', 0.2),
 ('z47', 'JOSH', 'Mais do que adequado. O que eu quero dizer é que a cor foi acertada. As outras debutantes usavam branco, azul claro, rosa. Cores que somem. Você usou uma cor que se destaca.', 0.2),
 ('z48', 'AU', BR+'Quem escolheu foi a Madame Solberg.', 0.2),
 ('z49', 'JOSH', 'A Madame Solberg tem razão. Cores profundas na sua pele são... mais eficazes do que cores claras.', 0.3),
 ('z50', 'N', 'Aurora repetiu, com uma nota na voz que ele não soube decifrar. Diversão? Provocação? Teste?', 0.2),
 ('z51', 'AU', 'Diga num tom provocante, em português do Brasil: Eficazes.', 0.2),
 ('z52', 'N', 'Josh tropeçou nas próprias palavras, como um potro em chão escorregadio:', 0.2),
 ('z53', 'JOSH', 'Pra chamar atenção, quero dizer.', 0.2),
 ('z54', 'AU', BR+'Você está dizendo que eu sou bonita de verde escuro.', 0.2),
 ('z55', 'JOSH', 'Estou dizendo que verde escuro combina com o seu tom de pele.', 0.2),
 ('z56', 'AU', 'Diga num tom provocante, com um meio sorriso, em português do Brasil: Que é a mesma coisa que dizer que eu sou bonita de verde escuro.', 0.4),
 ('z57', 'N', 'Josh olhou para ela. E ela o olhava de volta com aqueles olhos cor de mel que sabiam exatamente o que estavam fazendo. Estavam aplicando a segunda lição. O olhar. Dos olhos dele à boca dele. E de volta. Ela estava praticando com ele. De propósito. Sabendo muito bem o efeito. E mentir naquele ponto seria uma ofensa à inteligência dos dois. Ele admitiu:', 0.2),
 ('z58', 'JOSH', 'Sim. Você é bonita de verde escuro.', 0.4),
 ('z59', 'N', 'Aurora sustentou o olhar mais um segundo. Depois desviou. E Josh viu o tom de cobre subir às bochechas morenas. Ela disse apenas:', 0.2),
 ('z60', 'AU', BR+'Obrigada.', 0.4),
 ('z61', 'N', 'E passaram para o assunto dos penteados. Que era um pouco menos letal.', 1.0),
 # --- as cinco aulas ---
 ('z62', 'N', 'Foram cinco aulas ao todo. Cinco manhãs de junho no jardim, com Kóngen, o gato da cozinheira, como única testemunha, instalado na sombra mais próxima como quem comprou ingresso na primeira fila. Cinco manhãs em que Josh ensinou Aurora a sorrir, olhar, tocar, só na teoria, conversar, se posicionar e se vestir. E em que ela, brilhante por natureza, absorveu tudo, questionou tudo, e devolveu a ele versões melhores do que ele tinha ensinado.', 0.4),
 ('z63', 'N', 'E entre as aulas, a coisa entre os dois mudou. Não de um jeito que os pais percebessem. Nos detalhes. Aurora parou de chamá-lo de Senhor Russel. Em qualquer situação, até na frente dos pais. Agora era Josh no café da manhã, Josh no jantar, Josh quando pedia o pão. E o nome, na boca dela, tinha peso. Tinha textura. Tinha, e talvez Josh estivesse enlouquecendo, carinho.', 0.4),
 ('z64', 'N', 'E Josh parou de desviar o olhar. Antes, quando se pegava olhando para ela por tempo demais, desviava para o prato, para o livro, para a janela. Agora, quando os olhares se cruzavam no jantar, ele sustentava. Um segundo a mais. Dois. E ela sustentava de volta. Depois os dois desviavam ao mesmo tempo, como quem dança junto há tempo bastante para conhecer os passos. O pai comentava o preço do trigo, a mãe pedia mais vinho, e ninguém sabia que, debaixo dos talheres e das conversas educadas, algo silencioso e enorme estava crescendo.', 1.0),
 # --- o sarau ---
 ('z65', 'N', 'O teste veio no fim de junho. Um sarau na casa dos Holst: menor que o baile dos Frederiksen, mais íntimo. E com a presença garantida de uma dúzia de rapazes em idade de casar, entre eles, como Eleonora informou no jantar da véspera, Erik Mortensen, o irmão mais velho de Ingrid, a amiga de Aurora, que acabava de voltar de uma temporada em Berlim. A mãe disse, com aquela casualidade fabricada de quem sugere algo fingindo que não sugere:', 0.2),
 ('z66', 'EL', EL_+'O Erik é um rapaz excelente. Estudado, viajado, e com uma fortuna considerável. A Ingrid me disse que ele perguntou por você no último chá.', 0.4),
 ('z67', 'N', 'Aurora não respondeu. E Josh, do outro lado da mesa, cortou o salmão com mais força do que o salmão merecia.', 0.6),
 ('z68', 'N', 'Agora, na carruagem a caminho dos Holst, Josh estava calado. Aurora ia ao lado dele, nos mesmos quarenta centímetros de sempre, que não eram suficientes e eram demais ao mesmo tempo. Usava um vestido cor de vinho. Escuro, profundo, que fazia a pele dela parecer bronze polido. E Josh, que tinha sugerido cores escuras na quarta aula, olhava aquilo com o arrependimento de quem construiu uma arma e a entregou ao mundo errado. Ele perguntou, baixo, para os pais no banco da frente não ouvirem:', 0.2),
 ('z69', 'JOSH', 'Nervosa?', 0.3),
 ('z70', 'N', 'Aurora olhou para ele. Os olhos dela tinham uma luz que não existia antes das aulas. Uma confiança pequena, nova, frágil como broto. Ela admitiu:', 0.2),
 ('z71', 'AU', BR+'Um pouco. Mas não tanto quanto antes.', 0.2),
 ('z72', 'JOSH', 'Lembra do que a gente praticou.', 0.2),
 ('z73', 'AU', BR+'Sorriso, olhar, toque, pergunta. Lugar no salão. Ombros abertos.', 0.2),
 ('z74', 'JOSH', 'E o que mais?', 0.2),
 ('z75', 'AU', BR+'E ser eu mesma. Só que... destrancada.', 0.4),
 ('z76', 'N', 'Josh sentiu o peito apertar. Destrancada. Ela tinha escolhido a palavra perfeita. Era exatamente isso que ele tentara fazer: não transformá-la em outra pessoa, mas abrir as portas que o medo, o luto e a cidade tinham trancado. Ele disse:', 0.2),
 ('z77', 'JOSH', 'Perfeita.', 0.3),
 ('z78', 'N', 'Ela o olhou um instante a mais, e respondeu, com uma ironia tão carinhosa que o sorriso torto dele escapou sem pedir licença:', 0.2),
 ('z79', 'AU', 'Diga com uma ironia carinhosa, em português do Brasil: Obrigada, professor.', 0.4),
 ('z80', 'N', 'Aurora viu o sorriso. Os olhos dela desceram, dos olhos à boca, e voltaram. O olhar que ele tinha ensinado. Usado nele. E Josh pensou, com a clareza de quem acabou de pisar numa armadilha que ele mesmo armou: Eu estou completamente perdido.', 1.0),
 ('z81', 'N', 'A casa dos Holst era menor que a dos Frederiksen, mas mais quente, nos dois sentidos. Salas menores, tetos mais baixos, convidados mais próximos. Não havia salão de baile: só uma sala de música com um quarteto de cordas e espaço para dançar, e uma sala de estar ao lado. Josh cumprimentou os anfitriões, pegou uma taça de champanhe que não pretendia beber, e se posicionou junto a uma coluna, perto da entrada. Um posto de vigia. Porque naquela noite ele não era participante. Era o treinador. O homem dos bastidores. E o espetáculo era Aurora.', 0.4),
 ('z82', 'N', 'Ela entrou e fez, com a naturalidade de quem respira, cada coisa que ele tinha ensinado. Ombros abertos, queixo erguido, corpo voltado para o salão. Perto da mesa de bebidas, com espaço em volta. E o sorriso. Deus, o sorriso. Ingrid apareceu ao lado dela quase na mesma hora, como um satélite em volta de um planeta. Riu de alguma coisa, cochichou outra, e olhou na direção de Josh com uma expressão perigosamente divertida. Josh concluiu que Ingrid Mortensen sabia de alguma coisa.', 0.4),
 ('z83', 'N', 'A primeira meia hora não teve importância. Música. Champanhe. Josh conversou com o padrinho, com o senhor Holst, e com um professor da universidade, um homem magro e intenso chamado Professor Andersen, que olhou para Josh como quem avalia um exemplar raro. E então aconteceu. Erik Mortensen se aproximou de Aurora.', 0.4),
 ('z84', 'N', 'Josh viu de longe, como quem assiste a uma peça cujo roteiro escreveu, mas cujo terceiro ato não controla. Erik era, Josh admitia com objetividade amarga, impressionante. Alto. Moreno para um dinamarquês, de cabelo castanho ondulado e olhos escuros de quem morou em cidades grandes. Vestia-se com a elegância descuidada de quem tem dinheiro demais para precisar se esforçar. Erik parou diante de Aurora e disse alguma coisa. Ela olhou para ele. E sorriu. O sorriso de verdade. O que começa no canto esquerdo e chega aos olhos.', 0.4),
 ('z85', 'N', 'Josh sentiu algo se partir. Não como vidro que quebra. Em silêncio, como uma costura que cede. Um fio que arrebenta num tecido esticado. Pequeno. Mas estrutural. E a palavra apareceu na cabeça dele com a clareza de um diagnóstico: ciúme. Não irritação. Não instinto de proteção. Ciúme puro, irracional. O ciúme de quem ensinou alguém a sorrir e vê o sorriso ser entregue a outro. Josh tomou um gole do champanhe. Estava morno, doce, e não ajudou em absolutamente nada.', 0.4),
 ('z86', 'N', 'Aurora conversava com Erik, e era tudo o que Josh tinha ensinado, executado com uma maestria que o fez sentir orgulho e nojo de si mesmo ao mesmo tempo. Os ombros abertos. O olhar, dos olhos à boca e de volta, aquele olhar que ela praticara com ele no jardim. O corpo levemente inclinado para dentro da conversa. E Erik respondia. Claro que respondia. Porque Erik era o que a sociedade aprovava, dinamarquês, rico, bonito de um jeito que não exigia pensamento. E porque Aurora, destrancada, era a pessoa mais magnética de qualquer sala.', 0.4),
 ('z87', 'N', 'Por quinze minutos, Josh os viu conversar. Viu Aurora rir, não o estilhaço de riso da cozinha, mas uma risada inteira, com corpo e som. Viu Erik se inclinar para falar mais perto. Viu Aurora não recuar. E então viu a coisa que quase o fez largar a taça. Aurora tocou o braço de Erik. O toque. O que ela tinha se recusado a praticar com Josh. O que tinha dito que não era necessário. E agora tocava Erik Mortensen. De leve. Um segundo. Dois. E tirou a mão. Exatamente como Josh ensinou.', 0.4),
 ('z88', 'N', 'A costura cedeu mais. Outro fio. Outro. Toda a construção cuidadosa de não, não, não, que Josh repetia para si mesmo desde o primeiro dia, tremia como a pérgola antes de ser escorada. Então uma voz ao lado dele disse:', 0.2),
 ('z89', 'FRED', BR+'Você está com uma cara horrível.', 0.3),
 ('z90', 'N', 'Era Frederikke Mikkelsen, de vestido branco, com uma taça igual à dele. Josh respondeu: Estou bem. E ela insistiu:', 0.2),
 ('z91', 'FRED', BR+'Está olhando pra Aurora Svensson como se ela tivesse roubado alguma coisa sua.', 0.3),
 ('z92', 'N', 'Josh sentiu o sangue subir ao rosto, e começou a negar. Mas Frederikke o interrompeu, usando o primeiro nome dele com uma familiaridade que ele não tinha autorizado:', 0.2),
 ('z93', 'FRED', BR+'Josh. Todo mundo está olhando pra Aurora Svensson esta noite. Ela está diferente. Eu não sei o que mudou, mas ela está... acesa.', 0.4),
 ('z94', 'N', 'Acesa. A palavra o atingiu como um tapa. Ele tinha feito aquilo. Ele tinha acendido Aurora. E agora ela brilhava para um salão inteiro, e não só para ele. Que era, Josh reconhecia com a honestidade impiedosa que a mãe lhe ensinara, exatamente o que ele tinha se proposto a fazer. Ajudar Aurora a conquistar rapazes. Aurora estava conquistando um rapaz. Missão cumprida. Frederikke perguntou:', 0.2),
 ('z95', 'FRED', BR+'Posso te convidar pra dançar?', 0.4),
 ('z96', 'N', 'Josh olhou para Aurora. Ela ria de algo que Erik dizia e não olhava para ele. Talvez não soubesse que ele olhava. Talvez não se importasse. Ele respondeu a Frederikke:', 0.2),
 ('z97', 'JOSH', 'Claro.', 0.4),
 ('z98', 'N', 'Dançaram. Frederikke dançava bem: leve, fluida, e conversava sem parar. Falou da temporada, de um livro de poesia, fez perguntas sobre a universidade. Tocou o ombro dele ao mudar de direção. Riu de algo que ele disse. Josh respondeu, conduziu, sorriu. E durante a dança inteira manteve Aurora no canto do olho, como um marinheiro mantém o farol. Aurora não olhou para ele. Nem uma vez.', 1.0),
 # --- a volta ---
 ('z99', 'N', 'Voltaram à meia-noite. Na carruagem, o pai estava radiante, na medida contida em que ele conseguia ser radiante. Disse à mulher:', 0.2),
 ('z100', 'RAJ', 'Erik Mortensen. Rapaz excelente. Estudou em Berlim, fala três línguas, e tem uma propriedade considerável na Jutlândia. A Ingrid me disse que ele se interessou pela Aurora. Dançaram duas vezes.', 0.3),
 ('z101', 'EL', EL_+'Duas vezes.', 0.4),
 ('z102', 'N', 'Eleonora repetiu, porque entendia a aritmética social da cidade: uma dança era cortesia, duas era intenção. Josh olhou pela janela. A noite de junho era absurdamente clara: aquela meia-luz escandinava que não é dia nem noite, um crepúsculo sem fim que parecia feito de propósito para tornar impossível qualquer emoção simples. Aurora ia em silêncio ao lado dele. Josh não olhava para ela. Não confiava no que o próprio rosto diria. O padrinho se voltou para ele:', 0.2),
 ('z103', 'RAJ', 'E você, Joshua? Vi que dançou com a Frederikke Mikkelsen.', 0.2),
 ('z104', 'JOSH', 'Sim, senhor.', 0.2),
 ('z105', 'RAJ', 'Boa família. Boa moça.', 0.4),
 ('z106', 'N', 'Josh assentiu, e disse algo de que não se lembraria depois. Chegaram. Os pais subiram. Aurora fez menção de subir. E Josh ficou no hall. Desta vez não a chamou. Não disse que estava linda. Não disse que alguém era idiota. Ficou parado ao pé da escada e deixou Aurora subir. Três degraus. Quatro. Cinco. E no sexto, Josh contou, porque contar era o jeito que a cabeça achava de lidar com o que o peito não conseguia, ela parou.', 0.4),
 ('z107', 'N', 'Não se virou inteira. Virou a cabeça, o pescoço, o ombro, o bastante para Josh ver o perfil dela à luz da vela do hall. E disse, baixo:', 0.2),
 ('z108', 'AU', 'Diga baixo, com a voz contida, em português do Brasil: Funcionou.', 0.2),
 ('z109', 'JOSH', 'Eu vi.', 0.2),
 ('z110', 'AU', BR+'O Erik é... gentil. Culto. Fácil de conversar.', 0.2),
 ('z111', 'JOSH', 'Eu sei.', 0.2),
 ('z112', 'AU', BR+'Ele vai me visitar na quarta-feira. Pediu permissão ao meu pai.', 0.4),
 ('z113', 'N', 'Josh sentiu cada palavra como um prego entrando na madeira. Devagar. Um de cada vez. Ele disse:', 0.2),
 ('z114', 'JOSH', 'Que bom. É bom.', 0.4),
 ('z115', 'N', 'Aurora ficou parada no sexto degrau. E Josh viu, porque via tudo, que os dedos dela no corrimão estavam brancos. Apertando a madeira com a mesma força com que ela apertara a caneca na cozinha. Ela não estava contente. Não do jeito que deveria estar. Ela estava esperando que Josh dissesse alguma coisa. E ele sabia o quê, porque queria dizer o mesmo. Não vá. Não ele. Eu te ensinei a sorrir, e você sorriu pra ele, e eu nunca vou me recuperar disso.', 0.4),
 ('z116', 'N', 'Mas Josh era filho de Casandra Russel. E Casandra criava filhos que sabiam a diferença entre o que se quer dizer e o que se pode dizer. Ele disse apenas:', 0.2),
 ('z117', 'JOSH', 'Boa noite, Aurora.', 0.4),
 ('z118', 'N', 'Ela sustentou o olhar mais um segundo. Dois. E Josh viu, nos olhos cor de mel, à luz da vela, algo que parecia decepção. Ela respondeu:', 0.2),
 ('z119', 'AU', BR+'Boa noite, Josh.', 0.5),
 ('z120', 'N', 'Subiu o resto da escada. A porta do quarto se fechou com um clique suave. Josh ficou no hall, olhando as próprias mãos. Sem luvas, arranhadas de novo, porque na véspera tinha ajudado Fru Larsen a carregar lenha. Mãos de campo. Mãos que não pertenciam a casacos azul-marinho, nem a salões de champanhe, nem aos quarenta centímetros que o separavam de uma moça com cheiro de jasmim. Ele disse para si mesmo, baixo:', 0.2),
 ('z121', 'JOSH', 'Idiota.', 0.5),
 ('z122', 'N', 'A palavra ecoou no hall vazio. O espelho de moldura dourada devolveu o reflexo de um rapaz de vinte e um anos, com olheiras, os ombros caídos, e a cara de quem acaba de perceber que construiu uma ponte para outra pessoa atravessar, e ficou do lado errado.', 0.4),
 ('z123', 'N', 'Josh subiu. Não acendeu a vela. Não escreveu à mãe. Deitou-se vestido na cama e ficou ouvindo o silêncio do corredor, até o silêncio engolir tudo: o ciúme, a raiva, a decepção, o som do nome dela na própria voz. E o sono, finalmente, veio. Mas mesmo dormindo, no fundo do sono, onde não havia cidade nem bailes nem olhos cor de mel, Josh sonhou com algo que cheirava a jasmim. E acordou sabendo que nada, absolutamente nada, seria simples a partir de agora.', 0.0),
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
    sf.write(f"{SCR}/cap09-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap09-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap09-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
