import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts17"
SCR = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
# NOVAS vozes: Josh (Achird, jovem/caloroso), Dylan (Zubenelgenubi, casual/seco) — a AUDITAR com a autora
V = {"N": "Vindemiatrix", "AU": "Leda", "EL": "Gacrux", "RAJ": "Algieba",
     "JOSH": "Zubenelgenubi", "DYLAN": "Achird",
     "HELLE": "Achernar", "LARSEN": "Kore",
     "MIK": "Sulafat", "FRED": "Autonoe", "LOV": "Laomedeia", "CAS": "Pulcherrima", "SOL": "Despina", "ING": "Aoede", "CR1": "Erinome", "CR2": "Callirrhoe", "CR3": "Zephyr", "JOSHW": "Zubenelgenubi", "NM": "Vindemiatrix", "ERIK": "Iapetus", "HJ": "Puck", "LYK": "Zephyr", "VIB": "Laomedeia"}
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
 ('h001', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo dezessete: A prima.', 1.2),
 ('h002', 'N', 'Este capítulo é contado pelos olhos de Josh. Desde a festa do celeiro, ele e Aurora quase não se falam: ela pediu um beijo, ele resistiu, e a cozinha das seis da manhã ficou vazia. No jantar do capítulo anterior, Eleonora anunciou que a sobrinha, Vibêke, filha da irmã Karoline, vinha de Viborg passar dois meses na casa. E, sem disfarçar muito, sugeriu que Vibêke seria uma boa companhia para Josh.', 0.6),
 ('h003', 'N', 'A carruagem chegou na quarta-feira, às onze e quinze. Josh ouviu as rodas nas pedras da rua lá do quarto, no segundo andar, onde terminava uma leitura de direito romano que o padrinho tinha passado para a semana. Pousou o livro e foi até a janela. Lá embaixo, o cocheiro descia para abrir a porta, e Helle, a criada, já estava no portão, com Fru Larsen, a cozinheira, logo atrás, prontas para o ritual de recepção que aquela casa executava com a precisão de uma orquestra afinada.', 0.4),
 ('h004', 'N', 'Da carruagem saíram três pessoas. Primeiro, uma criada de viagem, baixinha, de avental limpo, com o cansaço de quem dormiu sentada por dois dias. Depois, uma senhora idosa, que não podia ser Vibêke: uma acompanhante, talvez. E por último, uma moça loira, alta, de vestido azul-claro, que pisou na rua e esticou os braços para o céu, como quem se espreguiça depois de uma viagem longa. Aquela era Vibêke.', 0.4),
 ('h005', 'N', 'Ele nem precisava de apresentação. Pela descrição da madrinha no jantar, pelo gesto, e pelo jeito como a moça se virou para a fachada da casa, com aquele entusiasmo aberto de quem nunca aprendeu a esconder o que sente, era óbvio. Ele se afastou da janela. Fechou o livro. E decidiu, com a frieza prática de quem precisa de um plano antes de descer uma escada, que o papel dele naquele dia seria simples: cumprimentar, sair de cena, e ficar à disposição. Aurora receberia a prima. A madrinha a hospedaria. O padrinho seria o tio cordial. O afilhado da casa não era figura de palco numa chegada de prima. Era figura de bastidor. E bastidor era o lugar dele na cidade, desde março. Desceu a escada às onze e vinte e cinco.', 1.0),
 ('h006', 'N', 'Eleonora estava no hall, com Aurora ao lado. Aurora usava o vestido bordô das visitas, o broche de prata, o cabelo preso. Era a roupa que ela vestia quando queria avisar à mãe que estava cumprindo o protocolo sem reclamar, e que, em troca, ninguém comentasse nada sobre nada. Josh atravessou o hall e parou três passos atrás delas, perto da coluna decorativa que ele sempre achou exagerada, e que naquela manhã agradeceu por existir, como apoio para uma postura que ele não tinha certeza de conseguir manter sozinho. A porta abriu. E a moça entrou, exclamando:', 0.2),
 ('h007', 'VIB', VB+'Tia Eleonora! Tio Ráge! Que saudade!', 0.3),
 ('h008', 'N', 'Por um segundo, Vibêke pareceu tomar conta do hall inteiro. Não pela altura, embora fosse alta. Pela voz. Pela presença. Pelo movimento. Abraçou Eleonora com uma intimidade que ele nunca tinha visto ninguém usar com a madrinha, e Eleonora, para seu crédito eterno, aceitou o abraço com um sorriso pequeno, mas genuíno. Depois apertou a mão do padrinho com tanto calor que o braço dele balançou. O padrinho perguntou:', 0.2),
 ('h009', 'RAJ', 'Vibêke. A viagem foi boa?', 0.2),
 ('h010', 'VIB', VB+'Horrível. A carruagem tinha uma mola quebrada, choveu dois dias, e a senhora Lindgren roncava. Mas eu estou aqui, então não conta.', 0.3),
 ('h011', 'N', 'E se virou para a prima:', 0.2),
 ('h012', 'VIB', VB+'Aurora! Você cresceu!', 0.2),
 ('h013', 'AU', BR+'Você também.', 0.2),
 ('h014', 'VIB', VB+'Eu cresci de lado. Você cresceu de jeito.', 0.4),
 ('h015', 'N', 'Aurora deu um sorriso pequeno. Não o de porcelana. Um sorriso mais cauteloso, tímido, encolhido diante do elogio. Vibêke abriu os braços, e Aurora, depois de uma fração de segundo de hesitação que talvez só Josh tenha visto, aceitou o abraço. Foi um abraço curto. Vibêke pareceu satisfeita assim mesmo, sem cobrar mais. Depois se virou para ele:', 0.2),
 ('h016', 'VIB', VB+'E você deve ser o Josh.', 0.2),
 ('h017', 'JOSH', 'Senhorita Bierg. É um prazer.', 0.2),
 ('h018', 'VIB', VB+'Vibêke. Eu pretendo te chamar de Josh, então é justo você me chamar de Vibêke. A mamãe disse que você é o afilhado do tio Ráge, e que está estudando direito.', 0.2),
 ('h019', 'JOSH', 'Ciências, na verdade. O direito é uma das matérias.', 0.2),
 ('h020', 'VIB', VB+'Tanto faz. Eu não entendo nada de nenhuma das duas.', 0.3),
 ('h021', 'N', 'Outro sorriso, largo e fácil, sem calibragem nenhuma. E ela se virou de novo para a tia, dispensando Josh com a leveza de quem risca um item de uma lista mental:', 0.2),
 ('h022', 'VIB', VB+'Tia, onde eu posso me instalar?', 0.2),
 ('h023', 'EL', ELP+'No quarto azul. A Helle vai te ajudar com a mala.', 0.2),
 ('h024', 'VIB', VB+'Maravilha. Vou subir e tirar essa roupa. Estou cheirando a estrada.', 0.4),
 ('h025', 'N', 'Vibêke subiu a escada conversando com Helle sobre a viagem, sobre uma fazenda perto de Órus onde tinham parado para almoçar, sobre um cachorro que apareceu no estábulo da hospedaria. E Helle, que nunca dirigia mais de três palavras a ninguém, riu duas vezes nos primeiros dez degraus. Josh olhou para Aurora. Ela olhava a escada vazia, com uma expressão que ele não conseguiu nomear. Não era incômodo. Não era alívio. Era alguma coisa no meio, mais perto de surpresa. Ela começou:', 0.2),
 ('h026', 'AU', AI+'Ela é... ela é muito...', 0.2),
 ('h027', 'N', 'E a mãe completou, confirmando, num tom entre a sinceridade e a ironia:', 0.2),
 ('h028', 'EL', ELP+'É, sim. A Karoline criou bem.', 0.4),
 ('h029', 'N', 'E foi para a sala de costura sem acrescentar mais nada. Josh olhou para Aurora. Aurora encontrou os olhos dele por meio segundo. E o que passou entre os dois, no hall vazio, às onze e meia da manhã, foi uma frase inteira que nenhum precisou dizer: isso vai ser interessante.', 1.0),
 ('h030', 'N', 'O almoço foi servido à uma. Vibêke desceu de vestido lilás, com uma trança de lado que parecia feita em dez minutos e, mesmo assim, ficava mais arrumada do que qualquer penteado que Aurora levava horas para fazer. Sentou, agradeceu a Fru Larsen pela sopa com um entusiasmo que arrancou da cozinheira um raríssimo hum de aprovação, e começou a comer com a fome honesta de quem dormiu mal por dois dias e não pretendia fingir o contrário. O padrinho presidia a mesa, divertido. E perguntou:', 0.2),
 ('h031', 'RAJ', 'E como anda a Karoline?', 0.2),
 ('h032', 'VIB', VB+'A mamãe está bem. Reclama do clima, do papai, da minha letra, do estado da igreja e do prefeito de Viborg, que ela acha incompetente. Mas a saúde está boa.', 0.2),
 ('h033', 'RAJ', 'E o seu pai?', 0.2),
 ('h034', 'VIB', VB+'O papai está sumido na fazenda há três semanas. Diz que precisa supervisionar a colheita, mas a gente sabe que ele só está fugindo da mamãe. Eu faria o mesmo, se pudesse.', 0.4),
 ('h035', 'N', 'Josh, que tinha acabado de levar o copo de suco à boca, engasgou. Um engasgo curto, daqueles que a gente empurra para baixo para não cuspir, e que ainda assim escapa pelo nariz feito um pigarro mal disfarçado. Tossiu no guardanapo. Aurora olhou para ele de relance, e o canto da boca dela tremeu no esforço de não rir. Não conseguiu segurar inteiro: um riso curto escapou pelo nariz, e ela levou o guardanapo aos lábios depressa, como quem tenta engolir o som de volta. Foi a primeira risada que ele ouvia dela em semanas.', 0.4),
 ('h036', 'N', 'O padrinho também riu de verdade, sem se segurar. Um riso curto, mas aberto, do tipo que Josh raramente ouvia naquela sala. Eleonora sorriu por trás do guardanapo, e até Helle, servindo o pão, abaixou a cabeça e mordeu o lábio. O padrinho disse:', 0.2),
 ('h037', 'RAJ', 'Você é igualzinha ao seu pai, Vibêke.', 0.2),
 ('h038', 'VIB', VB+'A mamãe diz isso quando quer me ofender. Eu aceito como elogio.', 0.4),
 ('h039', 'N', 'Aurora, que tinha tomado três colheradas de sopa em silêncio, olhou para a prima. Não com hostilidade. Com curiosidade.', 0.2),
 ('h040', 'AU', BR+'Vibêke, você lembra da última vez que esteve aqui?', 0.2),
 ('h041', 'N', 'A prima pousou a colher, pensando:', 0.2),
 ('h042', 'VIB', VB+'Eu tinha sete anos. Lembro pouca coisa. Lembro do jardim, que eu achei que era um campo inteiro. Lembro da Fru Larsen me dando um doce com mel por cima, que eu carreguei o resto do dia na palma da mão, porque tinha medo de comer e acabar. E lembro do tio Ráge me dando uma moeda dinamarquesa antiga. Eu achei que era a coisa mais bonita que eu já tinha visto na vida.', 0.3),
 ('h043', 'N', 'O padrinho sorriu:', 0.2),
 ('h044', 'RAJ', 'Eu me lembro da moeda. Era do tempo do rei Cristiano Sexto.', 0.2),
 ('h045', 'VIB', VB+'Eu ainda tenho ela.', 0.2),
 ('h046', 'RAJ', 'Você guardou?', 0.2),
 ('h047', 'N', 'Vibêke encolheu os ombros, como quem diz o óbvio:', 0.2),
 ('h048', 'VIB', AI+'Claro que guardei. A gente guarda as coisas que vêm das pessoas que importam.', 0.6),
 ('h049', 'N', 'Houve um silêncio pequeno na mesa. Não constrangido. Só o silêncio de quem registra uma frase boa antes de seguir em frente. Josh viu o padrinho fazer para a madrinha um gesto mínimo com o queixo, que na língua dos dois queria dizer: essa menina é boa. Eleonora devolveu meio sorriso. Aurora olhou para a sopa.', 0.4),
 ('h050', 'N', 'E Josh entendeu, na mesma fração de segundo, que Vibêke não era só a sobrinha alegre que a madrinha tinha descrito. Era inteligente. De um jeito que se disfarçava de espontaneidade. Era um tipo de inteligência que ele respeitava, porque conhecia: era a mesma de Meridiana, a irmã dele, que conversava com as árvores e, ao mesmo tempo, administrava a despensa da fazenda. Inteligência de quem não precisa provar nada. Vibêke ia ser uma boa companhia para Aurora. E ia ser, ele percebeu com uma clareza um pouco desconfortável, uma péssima peça para qualquer plano de casamento da madrinha, porque a moça era de uma astúcia impressionante.', 1.0),
 ('h051', 'N', 'O assunto começou na sobremesa. Foi Eleonora quem puxou. Josh viu a pergunta se formar antes de sair, porque já conhecia o jeito dela de montar a frase: uma pausa para a conversa pousar no neutro, um olhar rápido ao marido, como quem confere a autorização, e um educado: e me diga.', 0.2),
 ('h052', 'EL', ELP+'E me diga, Vibêke. O rapaz de Viborg. Como ele se chama?', 0.2),
 ('h053', 'VIB', VB+'Lauritz. Lauritz Brandt.', 0.2),
 ('h054', 'EL', ELP+'Brandt. Família de Viborg?', 0.2),
 ('h055', 'VIB', VB+'De Viborg, sim. O pai dele tem terras a oeste, perto de Skive. A mãe é de Ólborg, mas mora em Viborg desde que casou.', 0.2),
 ('h056', 'N', 'O padrinho processou:', 0.2),
 ('h057', 'RAJ', 'Os Brandt de Skive. Eu negociei com um Brandt, há uns dez anos. Trigo?', 0.2),
 ('h058', 'VIB', VB+'Cevada. Esse era o tio do Lauritz. O pai dele cuida das terras.', 0.2),
 ('h059', 'RAJ', 'Hum. Têm plantações sólidas.', 0.2),
 ('h060', 'VIB', VB+'Sólidas, sim. O Lauritz não vai me deixar passar fome.', 0.4),
 ('h061', 'N', 'Eleonora pousou a colher de sobremesa com aquela delicadeza que era o jeito dela de pisar com calma antes de pisar com força:', 0.2),
 ('h062', 'EL', ELP+'E você está... certa?', 0.2),
 ('h063', 'VIB', VB+'Certa de quê, tia?', 0.2),
 ('h064', 'EL', ELP+'Do Lauritz.', 0.4),
 ('h065', 'N', 'Vibêke parou de comer. Olhou para a tia. Não com indignação. Com uma serenidade que Josh, do outro lado da mesa, achou desconcertante. Tinha pouco mais de um ano a mais do que Aurora, e uma firmeza por dentro que muitas moças de vinte e cinco anos da cidade não tinham. E respondeu:', 0.2),
 ('h066', 'VIB', AI+'Tia. O Lauritz ainda não pediu formalmente. Eu sei que, pela regra, é por isso que ninguém em Viborg considera certo. Mas eu estive no celeiro dos Brandt no inverno passado. E na geada de fevereiro. E na primeira ceifa de junho. Eu vi. Está certo.', 0.4),
 ('h067', 'N', 'O rosto de Eleonora corou de leve com as descrições da menina. Só Deus sabia o que Vibêke e Lauritz tinham feito no celeiro e na primeira ceifa de junho. Eleonora perguntou:', 0.2),
 ('h068', 'EL', ELP+'Está certo para você?', 0.2),
 ('h069', 'VIB', AI+'Está certo para nós dois.', 0.4),
 ('h070', 'N', 'Eleonora sustentou o olhar da sobrinha por mais um segundo. Depois assentiu. Um assentimento curto, neutro, sem aprovação nem desaprovação visíveis. Mas Josh, que passou meses estudando a economia do rosto da madrinha, viu o que aquilo queria dizer na contabilidade dela: informação anotada, plano em revisão. E ela disse:', 0.2),
 ('h071', 'EL', ELP+'Bom. A Karoline preferia que você viesse à cidade antes de ter certeza de vez sobre esse noivado.', 0.2),
 ('h072', 'N', 'Vibêke sorriu, com aquela combinação rara de respeito e teimosia:', 0.2),
 ('h073', 'VIB', VB+'A mamãe me mandou, e eu vim. E prometi me abrir para conhecer outros rapazes. E vou. Mas eu não vou trocar.', 0.2),
 ('h074', 'EL', ELP+'Ela não está pedindo que você troque, querida. Só que confirme se é isso mesmo que você quer.', 0.2),
 ('h075', 'VIB', VB+'Eu entendo. A mamãe me avisou, ainda em Viborg, que se eu chegasse aqui com o Lauritz escrito na testa, todo mundo ia querer apagar. Então eu prometi a ela que ia tirar ele da testa e guardar dentro do casaco. Mas ele continua lá.', 0.4),
 ('h076', 'N', 'O padrinho riu de novo, mais aberto. Um riso que arrastou Josh junto, e por um segundo os dois homens riam no mesmo compasso, coisa que ele não lembrava de ter acontecido uma vez sequer naquela sala desde março. Aurora ergueu os olhos da sobremesa pela primeira vez, a boca ainda meio escondida atrás do guardanapo, e olhou para a prima com alguma coisa nova no rosto, que Josh classificou, com alívio, como reconhecimento.', 0.4),
 ('h077', 'N', 'Eleonora pegou a colher. Provou a sobremesa. E olhou para ele:', 0.2),
 ('h078', 'EL', ELP+'Josh, querido.', 0.3),
 ('h079', 'N', 'Ele sentiu o que vinha um segundo antes da frase. E não pôde fazer nada para impedir. Aurora também ergueu os olhos.', 0.2),
 ('h080', 'JOSH', 'Sim, madrinha?', 0.2),
 ('h081', 'EL', ELP+'A Vibêke chegou hoje, e provavelmente vai passar a manhã se acomodando. Mas amanhã à noite os Lundgren dão um dos bailes da temporada, e ela ainda não conhece quase ninguém na cidade. Você poderia, gentilmente, acompanhá-la? Apresentar algumas pessoas, ajudá-la a circular?', 0.4),
 ('h082', 'N', 'Na superfície, era uma cortesia. Por baixo, era a segunda etapa do plano que a madrinha tinha plantado no jantar de quarta. Ele já reconhecia o desenho. Acompanhar era a versão diluída de aproximar. Algumas pessoas incluía Josh por perto a noite inteira. E circular queria dizer que os dois seriam vistos juntos, por gente que ia comentar que os dois tinham sido vistos juntos. Era uma manobra elegante. E ele não tinha desculpa pronta para recusar.', 0.2),
 ('h083', 'JOSH', 'Claro, madrinha. Vai ser um prazer.', 0.3),
 ('h084', 'N', 'Vibêke se virou para ele, com aquele entusiasmo aberto que, ele já tinha entendido, era o estado natural dela:', 0.2),
 ('h085', 'VIB', VB+'Ah, que ótimo! Eu não conheço quase ninguém mesmo. A única pessoa que a mamãe me indicou na cidade é uma senhora Ériksen, do outro lado do canal, mas ela está na casa de campo esta semana e não deve ir ao baile. Você vai me salvar!', 0.2),
 ('h086', 'N', 'E ele respondeu, curto, ao notar que as mãos de Aurora tinham se recolhido para debaixo da mesa:', 0.2),
 ('h087', 'JOSH', 'Faço o que eu puder.', 0.2),
 ('h088', 'VIB', VB+'Você dança?', 0.2),
 ('h089', 'JOSH', 'Mal. Muito mal, na verdade.', 0.2),
 ('h090', 'VIB', VB+'Eu também. Então a gente combina. Tia, eu posso trocar de roupa oito vezes amanhã antes de decidir o que vestir?', 0.2),
 ('h091', 'N', 'A madrinha estreitou os olhos:', 0.2),
 ('h092', 'EL', ELP+'Pode... Mas que tipo de pergunta é essa?', 0.2),
 ('h093', 'VIB', VB+'Que ótimo! É só um jeito de já avisar que eu costumo me atrasar. Hummm, essa torta tem ameixa de verdade?', 0.2),
 ('h094', 'N', 'Perguntou, mudando de assunto na mesma velocidade de uma carruagem virando a esquina. E a tia respondeu:', 0.2),
 ('h095', 'EL', ELP+'Tem. A Fru Larsen vai a Frederiksberg comprar as ameixas no fim do verão. É um ritual.', 0.2),
 ('h096', 'VIB', VB+'Eu preciso conhecer a Fru Larsen!', 0.2),
 ('h097', 'EL', ELP+'Mas você mesma disse que conhece a Fru Larsen desde os sete anos.', 0.2),
 ('h098', 'VIB', VB+'Eu preciso conhecer de verdade. Ver ela preparar a comida. Sentir o cheiro! Provar a fruta direto da árvore!', 0.4),
 ('h099', 'N', 'Dessa vez Aurora não conseguiu se segurar, e soltou um som pelo nariz. Não chegou a ser um riso. Foi o começo de um. E Josh viu Aurora olhar para a prima, pela primeira vez no almoço inteiro, com alguma coisa perto de afeto e diversão. Ele gostou do que viu. Vibêke ia ficar dois meses na casa. E talvez, ele começava a desconfiar, esses dois meses não fossem tão complicados quanto pareceram no jantar do anúncio.', 1.0),
 ('h100', 'N', 'Depois do almoço, Eleonora subiu para descansar. O padrinho foi para o escritório com uma desculpa que era, claramente, uma desculpa. Vibêke disse que precisava desfazer a mala inteira, e sumiu com Aurora escada acima. Josh ficou na sala de estar, com um livro que não estava lendo. Uns vinte minutos depois, Aurora desceu. Sozinha. Parou na soleira da porta e olhou para ele com aquela expressão que ele já conhecia: quero te dizer uma coisa, mas não vou, porque desde o celeiro a gente não se fala. Ele fechou o livro, e falou primeiro:', 0.2),
 ('h101', 'JOSH', 'Ela está desfazendo a mala?', 0.2),
 ('h102', 'AU', AI+'Tirando vestido por vestido, e contando uma história sobre cada um. Eu pedi licença pra buscar um lenço. Já vou voltar.', 0.2),
 ('h103', 'JOSH', 'Quantos vestidos faltam?', 0.2),
 ('h104', 'AU', AI+'Cinco. Faltam cinco.', 0.2),
 ('h105', 'JOSH', 'Cinco histórias?', 0.2),
 ('h106', 'N', 'Aurora encostou o ombro no batente, os olhos ainda na escada:', 0.2),
 ('h107', 'AU', AI+'Pelo menos. Ela falou do baile dos Lundgren, lá no quarto.', 0.2),
 ('h108', 'JOSH', 'E o que ela disse?', 0.2),
 ('h109', 'AU', AI+'Disse que estava animada pra você acompanhar ela. Que vocês combinam, porque os dois vieram do interior, da fazenda, e que nas fazendas o jeito de dançar é mais solto. Sem coreografia.', 0.2),
 ('h110', 'N', 'E se inclinou um pouco na direção dele, como quem vai contar um segredo:', 0.2),
 ('h111', 'AU', 'Diga em português do Brasil, com sotaque brasileiro, num cochicho, como quem conta um segredo: Como na festa do celeiro?', 0.2),
 ('h112', 'JOSH', P1+'Sim. É como na festa do celeiro.', 0.2),
 ('h113', 'AU', AI+'Então as pessoas são mais felizes no interior?', 0.2),
 ('h114', 'JOSH', P1+'Mais felizes, eu não sei. Mas mais livres, eu acho que sim.', 0.4),
 ('h115', 'N', 'Aurora ficou em silêncio. Olhou para o livro fechado no colo dele, depois para ele. Não havia pergunta no rosto dela. Havia um registro pequeno, neutro. E ela constatou:', 0.2),
 ('h116', 'AU', AI+'Você vai acompanhar a Vibêke ao baile.', 0.2),
 ('h117', 'N', 'Ele estreitou os olhos, tentando ler o que vinha por trás da frase:', 0.2),
 ('h118', 'JOSH', 'Vou, sim. Vou acompanhar.', 0.2),
 ('h119', 'AU', AI+'Eu sei.', 0.2),
 ('h120', 'JOSH', 'A sua mãe pediu na frente de todo mundo, depois de a Vibêke dizer que não conhece quase ninguém. Recusar ali seria uma cena. E eu não saberia fazer uma cena sem magoar a Vibêke, que não merece.', 0.2),
 ('h121', 'AU', AI+'Eu sei, Josh. Eu não queria que você tivesse recusado.', 0.2),
 ('h122', 'JOSH', 'Então qual é o problema?', 0.2),
 ('h123', 'AU', AI+'Não tem problema nenhum. Eu só estou dizendo.', 0.4),
 ('h124', 'N', 'Aurora respirou fundo. Não foi um suspiro. Foi a respiração de quem organiza alguma coisa por dentro, e precisa do ar para fazer a conta. E disse, baixo:', 0.2),
 ('h125', 'AU', AI+'A mamãe não vai parar. Ela vai achar outro caminho.', 0.2),
 ('h126', 'N', 'Ele sabia o que ela queria dizer. Mas queria que ela dissesse:', 0.2),
 ('h127', 'JOSH', P1+'Outro caminho pra quê?', 0.2),
 ('h128', 'N', 'E Aurora ergueu a cabeça, como quem desafia:', 0.2),
 ('h129', 'AU', AI+'Pra te aproximar da Vibêke. Mas talvez seja isso que você quer.', 0.4),
 ('h130', 'N', 'Ele olhou em volta, como quem procura as palavras certas no ar:', 0.2),
 ('h131', 'JOSH', P1+'Aurôra. Não é isso que eu quero. Eu mal conheço a sua prima. E você sabe muito bem, mesmo que finja que não sabe, que o que eu quero, na verdade...', 0.4),
 ('h132', 'N', 'E se calou. Não podia. E sabia de cor em quantos níveis não podia dizer. Era uma cena para confirmar o que os dois já sabiam, e deixar o resto onde estava: do lado de fora, entre o corredor vazio e a soleira da porta. Por fim, disse, com a voz mais baixa:', 0.2),
 ('h133', 'JOSH', P1+'O que eu quero não vem ao caso. Mas não fica preocupada com o baile.', 0.2),
 ('h134', 'N', 'Aurora encolheu os ombros:', 0.2),
 ('h135', 'AU', AI+'Eu não estou preocupada.', 0.4),
 ('h136', 'N', 'Foi a pior atuação que ela tinha feito naquela casa em semanas, e os dois souberam. Ele mudou a rota do assunto:', 0.2),
 ('h137', 'JOSH', 'A Vibêke gostou de você.', 0.2),
 ('h138', 'AU', AI+'Como você sabe?', 0.2),
 ('h139', 'JOSH', 'Pelo abraço. Pelo jeito como ela falou o seu nome na hora de cumprimentar. Pelo você cresceu de jeito. Ela escolheu cada palavra.', 0.4),
 ('h140', 'N', 'Aurora pensou naquilo. Olhou de novo para a escada. E admitiu:', 0.2),
 ('h141', 'AU', AI+'Acho que eu também gostei dela.', 0.2),
 ('h142', 'JOSH', P1+'Eu vi. Eu vi, sim.', 0.6),
 ('h143', 'N', 'Ela ficou na soleira mais um segundo. Depois subiu de novo, para o quarto onde a prima a esperava com cinco vestidos ainda na mala e cinco histórias acumuladas. E onde, ele imaginava, nas próximas horas, o nome de Lauritz Brandt seria dito uma vez a mais do que o estritamente necessário. Josh ficou na sala. Reabriu o livro, mas não leu.', 0.4),
 ('h144', 'N', 'E pensou, com uma certeza que já não tentava combater, que Vibêke era a melhor coisa que tinha acontecido àquela casa em meses. Não porque resolvia o que precisava ser resolvido. Não resolvia. Aurora continuaria sendo Aurora. Erik continuaria visitando às quartas. A madrinha continuaria observando. E a coisa entre ele e Aurora continuaria sendo o que era: uma coisa sem nome, num corredor sem saída. Mas Vibêke trazia ar. Trazia luz. E depois de cinco meses naquela casa, ele sabia o bastante para reconhecer que ar e luz, ali, eram bens escassos, que não se desperdiçavam.', 0.4),
 ('h145', 'N', 'Largou o livro. Levantou. Foi até a janela. Lá fora, o sol de agosto continuava como sempre: alto, longo, paciente. Depois subiu para o quarto, fechou a porta, sentou à escrivaninha, e escreveu, pela primeira vez em três semanas, uma carta para a mãe sem riscar nenhuma frase:', 0.4),
 ('h146', 'JOSH', 'Querida mãe. A prima da Aurora chegou. Vibêke. Vai ficar dois meses. A mãe da Aurora tem ideias sobre ela e sobre mim que a Vibêke, em quinze minutos de almoço, desmontou sem perceber que estava desmontando. Eu já gosto dela. A Aurora também, eu acho. Estou bem. Nem tanto. Mas bem.', 0.4),
 ('h147', 'JOSH', 'Diz pro Matias que eu mando lembranças. Diz pro rabugento do Joseph escrever mandando notícias. Diz pra Meridiana que as roseiras que eu cuidei por aqui estão floridas, e que eu sinto saudade dos cravos que ela colocava de enfeite. E diz pro pestinha do Dylan que eu sinto falta das implicâncias dele. Com amor, Josh.', 0.5),
 ('h148', 'N', 'Fechou a carta com o lacre. Pôs na pilha. E desceu para o jantar pensando que a vida, às vezes, mandava diversão na forma de moças loiras de Viborg, que riam alto e não tinham aprendido a esconder ninguém na manga do casaco.', 0.0),
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
    sf.write(f"{SCR}/cap17-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap17-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap17-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
