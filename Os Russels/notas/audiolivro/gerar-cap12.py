import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts12"
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
 ('c001', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo doze: O padrão.', 1.2),
 ('c002', 'N', 'Este capítulo volta aos olhos de Aurora. Nas últimas semanas, antes de cada encontro com um pretendente, ela tinha ouvido os conselhos de Josh. Sobre Erik e a poesia. Sobre Anders e o ritmo da caminhada. Sobre Niels e as pinturas. Conselhos que pareciam sábios. Aurora não sabia que, na noite anterior, Josh tinha escrito à mãe uma carta que nunca mandaria, confessando que esses conselhos eram envenenados.', 0.6),
 ('c003', 'N', 'Foi Ingrid quem acendeu o fósforo. Não de propósito. Ou talvez de propósito, porque com Ingrid Mortensen nunca se sabia onde terminava a observação casual e começava a cirurgia calculada. Ingrid tinha o dom de dizer verdades como quem comenta o tempo: de leve, de passagem, sem parecer perceber que acabava de arrancar o chão debaixo dos pés de alguém.', 0.4),
 ('c004', 'N', 'Era uma tarde de julho. Quente. O verão dinamarquês, quando resolvia ser verão de verdade, era surpreendentemente feroz. Aurora e Ingrid estavam no jardim dos Mortensen, menor e mais bagunçado que o dos Svensson, com uma natureza selvagem que Aurora sempre preferiu à simetria da mãe. Bebiam limonada debaixo de uma tília enorme, que fazia sombras rendadas na toalha. Ingrid estava deitada de costas na grama, a bengala ao lado, os olhos fechados. E disse, sem abri-los:', 0.25),
 ('c005', 'ING', BR+'O Erik perguntou ao meu pai se pode te convidar pro recital dos Frederiksen.', 0.2),
 ('c006', 'AU', BR+'Eu sei. Ele me escreveu.', 0.2),
 ('c007', 'ING', BR+'Escreveu. Que formal. Que encantador. Que terrivelmente adequado.', 0.3),
 ('c008', 'N', 'Ingrid abriu um olho, e perguntou:', 0.2),
 ('c009', 'ING', BR+'Você vai?', 0.2),
 ('c010', 'AU', BR+'Provavelmente.', 0.2),
 ('c011', 'ING', BR+'Provavelmente. Não sim, estou ansiosa. Não sim, mal posso esperar. Provavelmente.', 0.4),
 ('c012', 'N', 'Aurora tomou um gole de limonada. Estava morna. O gelo dinamarquês, sempre pouco, sempre derretendo, já tinha se rendido ao calor. Ela disse:', 0.2),
 ('c013', 'AU', BR+'Eu gosto do Erik, Ingrid.', 0.2),
 ('c014', 'ING', BR+'Eu sei que gosta. Ele é meu irmão. É impossível não gostar dele. É como não gostar de pão quente ou de filhote de cachorro. A questão não é se você gosta. A questão é se você gosta o suficiente.', 0.4),
 ('c015', 'N', 'Aurora não respondeu. Ingrid se sentou, com o esforço extra que sentar exigia do corpo dela, a perna torta se ajeitando com aquela mistura de paciência e teimosia que definia Ingrid. E olhou para Aurora com os olhos cinzentos, afiados como lâmina:', 0.2),
 ('c016', 'ING', BR+'Posso te dizer uma coisa?', 0.2),
 ('c017', 'AU', BR+'Você vai dizer de qualquer jeito.', 0.2),
 ('c018', 'ING', BR+'Verdade. Então eu vou dizer. Nas últimas três semanas, você rejeitou o Anders Lundgren, desencorajou o Niels Dahl, foi gelada com o Frederik Holst, e está mantendo o meu irmão, que é a melhor opção que você vai encontrar nesta temporada, e talvez na vida, a uma distância educada o bastante pra não ser grosseria, e grande o bastante pra não ser compromisso. Quatro pretendentes em três semanas. É uma taxa de rejeição impressionante pra alguém que supostamente quer ser escolhida.', 0.4),
 ('c019', 'N', 'Aurora sentiu o estômago se contrair, e se defendeu:', 0.2),
 ('c020', 'AU', BR+'Eu não rejeitei ninguém. O Anders é que não me convidou de novo. O Niels...', 0.2),
 ('c021', 'ING', BR+'O Niels ficou apavorado depois do sarau das pinturas. Disse pro meu pai que você é fascinante, mas assustadora. O que, admito, é um elogio. Mas não é o tipo de elogio que leva a um segundo convite.', 0.2),
 ('c022', 'AU', BR+'Eu só fui honesta.', 0.2),
 ('c023', 'ING', BR+'Você foi mais do que honesta. Você foi... estratégica. E o curioso é que você nunca foi estratégica antes. Antes do baile dos Frederiksen, você era o contrário. Era espontânea a ponto de espantar as pessoas sem querer. E agora, de repente, você tem técnica. Tem método. Sabe exatamente o que dizer, quando dizer, como posicionar o corpo, pra onde olhar.', 0.3),
 ('c024', 'N', 'Ingrid fez uma pausa. E perguntou:', 0.2),
 ('c025', 'ING', BR+'Quem te ensinou?', 0.5),
 ('c026', 'N', 'O ar saiu dos pulmões de Aurora como se alguém tivesse empurrado o peito dela com as duas mãos. Ela negou:', 0.2),
 ('c027', 'AU', BR+'Ninguém me ensinou.', 0.2),
 ('c028', 'ING', BR+'Aurora.', 0.2),
 ('c029', 'AU', BR+'Ninguém me...', 0.3),
 ('c030', 'N', 'Ingrid usou o nome completo, o que queria dizer que a conversa tinha deixado de ser casual e virado uma intimação amigável:', 0.2),
 ('c031', 'ING', BR+'Aurora Svensson. Eu te conheço há sete anos. Sete. Eu sei quando você está mentindo, porque a sua narina dilata um milímetro pra esquerda. E agora ela está dilatada o bastante pra eu ver dentro do seu crânio. Quem. Te. Ensinou.', 0.5),
 ('c032', 'N', 'Aurora olhou para a limonada. Para a tília. Para as nuvens. Para qualquer coisa que não fossem os olhos de Ingrid, implacáveis como os de um cirurgião antes do primeiro corte. E disse o nome, pequeno, quase sem voz, como uma confissão relutante, inevitável, aliviada:', 0.2),
 ('c033', 'AU', 'Diga num tom mais baixo, relutante, sem sussurrar, em português do Brasil: Josh.', 0.5),
 ('c034', 'N', 'Ingrid não reagiu na hora. Ficou imóvel, como uma máquina que recebe os dados e precisa de um momento para calcular. E repetiu:', 0.2),
 ('c035', 'ING', BR+'O Josh. O afilhado do seu pai. Que mora na sua casa. O rapaz do campo com cara de deus nórdico que todas as moças da cidade querem, e que você finge que não nota.', 0.2),
 ('c036', 'AU', BR+'Eu não finjo que não noto.', 0.2),
 ('c037', 'ING', BR+'Ah, então nota. Ótimo. Progresso. Conta. Tudo. Desde o começo.', 0.5),
 ('c038', 'N', 'Ingrid se ajeitou na grama, como quem se acomoda para uma história longa. E Aurora contou. Não tudo. Não a cozinha às seis da manhã, não a caneca fria, não o fez falta, não o eu não confio em mim perto de você. Essas coisas eram dela e de Josh, e de mais ninguém, nem de Ingrid. Mas contou das aulas. Do sorriso, do olhar, do toque, da pergunta. Do jardim. E dos conselhos que Josh dava antes de cada encontro com um pretendente.', 0.4),
 ('c039', 'N', 'Ingrid ouviu em silêncio, com uma atenção feroz que transformava o simples ato de ouvir num raio-X. Quando Aurora terminou, Ingrid ficou quieta o tempo de dois pássaros pousarem na tília, brigarem, e irem embora. E então falou, com outra voz. Não a da amiga brincalhona. A de alguém que via algo que a outra não via:', 0.2),
 ('c040', 'ING', BR+'Aurora. Eu vou te perguntar uma coisa, e quero que você pense antes de responder.', 0.2),
 ('c041', 'AU', BR+'Está bem.', 0.2),
 ('c042', 'ING', BR+'Dos conselhos que o Josh te deu antes dos encontros, todos, pensa em todos: quantos te aproximaram de alguém?', 0.6),
 ('c043', 'N', 'Silêncio. Aurora pensou. Conselho por conselho. Erik: cuidado com homem que tem opinião forte sobre poesia. O conselho plantou uma dúvida. A dúvida se desfez quando Erik respondeu com Goethe. Mas a dúvida existiu. Porque Josh a plantou. Anders: repara no ritmo. Aurora reparou. Anders andava depressa. O conselho a fez se fixar num detalhe que, sem a lente de Josh, talvez nem importasse.', 0.4),
 ('c044', 'N', 'Niels: reage a uma pintura que ele não espera. Aurora reagiu. Niels ficou desnorteado. O conselho a fez brilhante, sim. Mas brilhante de um jeito que assustava. Frederik: Josh não deu conselho sobre Frederik. Mas, na manhã do chá, falou de rapazes que falam de coisas em vez de falar de si mesmos. E Aurora levou esse filtro para a conversa, e viu Frederik através dele. Cada conselho. Sem exceção. Nenhum a aproximou. Todos, de jeitos diferentes, sutis, inteligentes, impecáveis, a afastaram.', 0.4),
 ('c045', 'N', 'A percepção se formou devagar, como uma imagem que aparece num negativo de fotografia. Primeiro os contornos. Depois os detalhes. Depois a imagem inteira, nítida, inegável. Josh não estava ajudando Aurora a conquistar pretendentes. Josh estava afastando todos eles. Ela disse só uma sílaba, o som mais silencioso do mundo, e dentro dele, um terremoto. Ah.', 0.5),
 ('c047', 'N', 'Ingrid a observou com a paciência de quem acende uma vela e espera a cera derreter. Aurora disse:', 0.2),
 ('c048', 'AU', BR+'Eu preciso ir.', 0.2),
 ('c049', 'ING', BR+'Agora? Já?', 0.2),
 ('c050', 'AU', BR+'Agora mesmo.', 0.2),
 ('c051', 'ING', BR+'Aurora, espera...', 0.3),
 ('c052', 'N', 'Mas Aurora já estava de pé, ajeitando o vestido, caminhando. Não correndo, porque Aurora Svensson não corria; correr era descontrole. Mas caminhando depressa, com um propósito e uma fúria contida que Ingrid reconheceu, pelo jeito como se calou e não tentou segui-la, como o tipo de fúria que não se interrompe.', 1.0),
 # --- a volta ---
 ('c053', 'N', 'A carruagem levou vinte minutos da casa dos Mortensen até a casa dos Svensson. Vinte minutos em que Aurora ficou com as mãos no colo, o olhar na janela, e o cérebro em combustão. Ela revisitou tudo. Cada manhã na cozinha. Cada conselho. Cada olhar de Josh quando ela falava de Erik. Aquele olhar que ela atribuía a proteção, a preocupação de conselheiro. E que era, agora ela via, com a clareza brutal de quem tira uma venda, ciúme.', 0.4),
 ('c054', 'N', 'Ciúme disfarçado de sabedoria. Sabotagem vestida de conselho. Manipulação embrulhada em honestidade. E subia uma raiva que ela não sentia desde o dia em que o pai anunciou a chegada de Josh. Uma raiva de lava, não de gelo. Não por ele ter sentido ciúme. Ciúme ela entendia. Era humano. Ela sabia o que havia entre os dois, sabia do fez falta e do eu não confio em mim. Sabia que Josh a amava, sem que nenhum dos dois tivesse usado a palavra. A raiva era pela confiança traída.', 0.4),
 ('c055', 'N', 'Aurora tinha confiado em Josh como não confiava em mais ninguém. Não na mãe, que a amava, mas não a entendia. Não no pai, que a entendia, mas não a alcançava. Não em Ingrid, que a via, mas não a segurava. Josh era o único que fazia tudo isso ao mesmo tempo, com as mesmas mãos calejadas que envernizavam bancos e escoravam pérgolas. E ele tinha usado esse acesso, que ela deu porque confiava, para manipulá-la.', 0.4),
 ('c056', 'N', 'A carruagem parou. Aurora entrou, passou pelo hall sem cumprimentar Helle, subiu a escada, atravessou o corredor. A porta do quarto de Josh estava aberta. Ele estava na escrivaninha, escrevendo algo, outra carta, provavelmente, cheia de meias verdades para a mãe. E levantou os olhos ao ouvir os passos. E viu Aurora. E pelo jeito como o rosto dele mudou, a cor recuando, os olhos se abrindo com o reconhecimento de quem vê a tempestade chegar tarde demais para fechar as janelas, Josh soube. Ele disse, com a voz de quem vai prestar contas:', 0.2),
 ('c057', 'JOSH', 'Aurora...', 0.4),
 ('c058', 'N', 'Ela entrou e fechou a porta atrás de si. Fechar a porta do quarto de um homem solteiro com ela lá dentro era escandaloso. Se a mãe visse. Se o pai soubesse. Mas Aurora não se importava. O decoro podia esperar. A porcelana podia esperar. E ela perguntou, com a voz baixa, controlada e terrível, como uma lâmina saindo da bainha:', 0.2),
 ('c059', 'AU', 'Diga com a voz baixa, firme, controlada e ameaçadora, sem sussurrar, em português do Brasil: Há quanto tempo. Há quanto tempo você está fazendo isso.', 0.5),
 ('c060', 'N', 'Josh não fingiu não entender. A favor dele, o pouco que Aurora estava disposta a conceder naquele momento, ele não fingiu:', 0.2),
 ('c061', 'JOSH', 'Desde o começo.', 0.2),
 ('c062', 'AU', BR+'Desde o começo. Desde o primeiro conselho.', 0.2),
 ('c063', 'JOSH', 'Desde o Erik. Desde o conselho sobre poesia.', 0.4),
 ('c064', 'N', 'Aurora fechou os olhos um instante, para conter a lava. Quando abriu, os olhos estavam duros. Opacos. Sem a mudança de luz, sem os veios de ouro. Pedra. E disse:', 0.2),
 ('c065', 'AU', BR+'Você me usou. Eu confiei em você. Pedi a sua ajuda. Abri portas que eu não abro pra ninguém. E você usou cada conselho que me deu pra afastar qualquer pessoa que chegasse perto de mim.', 0.2),
 ('c066', 'JOSH', 'Aurora...', 0.2),
 ('c067', 'AU', BR+'Não. Não diga o meu nome como se pudesse consertar alguma coisa dizendo o meu nome. Não funciona assim. Não comigo.', 0.4),
 ('c068', 'N', 'Josh se levantou. Não para se aproximar. Para ficar de pé. Para não ter a conversa mais importante da vida dele sentado, enquanto ela estava de pé. Era instinto, Russel até a medula: enfrentar de pé, olhar nos olhos, não se esconder. Ele disse:', 0.2),
 ('c069', 'JOSH', 'Eu não vou me justificar. Não tem justificativa. O que eu fiz foi errado.', 0.4),
 ('c070', 'N', 'Aurora soltou a palavra como quem cospe algo amargo:', 0.2),
 ('c071', 'AU', BR+'Errado. Errado é uma palavra muito pequena pro que você fez, Josh. Errado é usar o garfo de peixe errado no jantar. Errado é chegar atrasado. O que você fez foi...', 0.3),
 ('c072', 'N', 'Ela parou. Procurou a palavra. E quando achou, a palavra veio carregada de tudo: da raiva, da dor, da confiança traída, do medo de ter sido feita de boba:', 0.2),
 ('c073', 'AU', 'Diga com desprezo e dor contida, em português do Brasil: Covarde.', 0.6),
 ('c074', 'N', 'Josh recebeu a palavra como um soco. O corpo inteiro reagiu: um recuo mínimo, os ombros se contraindo, uma sombra passando pelos olhos verdes como nuvem diante do sol. Covarde. De todas as palavras, era a que cortava mais fundo. Porque Josh, que enfrentava, que não fugia, que carregava lenha e escorava pérgolas, e que segurou a mão do pai enquanto ele morria, ser chamado de covarde pela pessoa cuja opinião mais importava no mundo era uma dor que não se descreve em língua nenhuma. Ele admitiu:', 0.2),
 ('c075', 'JOSH', 'Sim. Foi covarde.', 0.4),
 ('c076', 'AU', BR+'Você podia ter me dito. Podia ter sido honesto. Podia ter dito: Aurora, eu não quero que você fique com o Erik, porque eu sinto alguma coisa por você e não sei lidar com isso. Teria sido difícil. Teria sido complicado. Teria me colocado numa posição impossível. Mas pelo menos seria verdade.', 0.2),
 ('c077', 'AU', BR+'Em vez disso, você se escondeu atrás de conselhos. Usou a minha confiança como ferramenta. Me transformou num tabuleiro, e mexeu as peças sem eu saber que estava num jogo.', 0.5),
 ('c078', 'N', 'Cada frase era um corte. Preciso. Limpo. Sem tremor. Aurora Svensson não tremia quando estava com raiva. Ficava mais firme. Mais ela. E Josh não se defendeu. Não disse eu te amo, embora as palavras estivessem ali, queimando na garganta. Não agora. Dizer eu te amo agora seria usar a verdade como escudo. E Josh, acusado de manipulação, se recusava a manipular de novo. Nem com a verdade. Ele perguntou:', 0.2),
 ('c079', 'JOSH', 'O que você quer que eu faça?', 0.2),
 ('c080', 'AU', BR+'Quero que você reconheça o que fez. Sem rodeio. Sem embrulho.', 0.4),
 ('c081', 'JOSH', 'Eu sabotei os seus pretendentes. Cada conselho que eu dei foi pensado pra criar distância entre você e qualquer homem que chegasse perto. Eu fiz isso porque eu sou...', 0.2),
 ('c082', 'N', 'Ele parou. Engoliu em seco. E continuou:', 0.2),
 ('c083', 'JOSH', 'Porque eu sou ciumento. E egoísta. E porque a ideia de te ver com outro homem me faz sentir uma coisa que eu não sei controlar. E em vez de lidar com o que eu sinto como um adulto, eu usei a sua confiança pra manipular a situação. E isso é imperdoável.', 0.5),
 ('c084', 'N', 'Aurora ouviu cada palavra. Cada pausa. E sentiu, debaixo da raiva, debaixo da lava, algo que não queria sentir. Algo que tornava impossível simplesmente odiá-lo, ir embora, e nunca mais descer para a cozinha às seis da manhã. Porque Josh tinha dito a verdade. Toda. Sem se esconder. Sem usar o amor como desculpa. Tinha ficado de pé, olhado nos olhos dela, e dito: fui covarde, egoísta, e o que eu fiz é imperdoável.', 0.4),
 ('c085', 'N', 'E essa honestidade, brutal, completa, sem rede, era exatamente o que Aurora mais admirava nele. Desde o primeiro dia. Desde o comentário sobre o corte das roseiras, que a irritou, e que ela seguiu, e que salvou as roseiras de Aarav. Josh era honesto. Até quando confessava desonestidade, era honesto. Era o paradoxo mais irritante e mais bonito do mundo.', 0.4),
 ('c086', 'N', 'Os dois se olharam. O quarto, com a cama de dossel, a escrivaninha de mogno, os cinco livros na estante e o canivete do pai na gaveta, ficou suspenso num silêncio diferente de todos os outros. Não o da cozinha, que era conforto. Não o do jardim, que era cumplicidade. O silêncio que vem depois de uma explosão, quando a poeira ainda está no ar e ninguém sabe se o que ficou de pé basta para reconstruir. Aurora disse:', 0.2),
 ('c087', 'AU', BR+'Eu vou sair deste quarto agora. E não quero que você me siga. Não quero que você desça pra cozinha amanhã. Não quero conselhos. Não quero olhares na mesa do jantar. Eu preciso de tempo pra decidir se consigo confiar em você de novo. E pra isso, eu preciso de distância.', 0.5),
 ('c088', 'N', 'Distância. A mesma palavra que Josh usou na manhã depois do sarau. Aurora a devolveu de propósito. Com o mesmo peso. Com a mesma lâmina. Josh assentiu. Não disse nada. Não pediu perdão. Não implorou. Ficou de pé, os braços ao lado do corpo, as mãos abertas, como quem mostra que não carrega arma. E a deixou ir.', 0.4),
 ('c089', 'N', 'Aurora saiu e fechou a porta. No corredor, encostou na parede. O coração batia tão forte que ela sentia nas têmporas. As mãos tremiam. As mãos que não tremiam, que seguravam tesoura de poda, caneca de chá e dezessete anos de armadura com firmeza, tremiam. Foi até o quarto. Desta vez não encostou as costas na porta. Foi até a janela e abriu. O ar de julho, quente, perfumado de rosas, glicínias e verão, entrou como uma onda. Aurora respirou.', 0.4),
 ('c090', 'N', 'E percebeu, com a clareza que só vem depois que a raiva queima e sobra o que é verdade, que o que mais doía não era a manipulação. Nem a traição. Era que Josh tinha feito tudo aquilo porque a amava. E que ela sabia. E saber tornava impossível transformar a raiva em ódio. Porque ódio exige não entender o outro. E Aurora entendia Josh tão completamente quanto entendia a si mesma.', 0.4),
 ('c091', 'N', 'Ele foi covarde. Sim. Ele a manipulou. Sim. Traiu a confiança dela. Sim. Mas ele a amava. E o amor, o maldito, inconveniente, irracional, impossível amor, não era desculpa. Mas era explicação. E explicações, ao contrário das desculpas, não podem ser recusadas. Só compreendidas.', 0.4),
 ('c092', 'N', 'Aurora fechou a janela, sentou na cama, e abriu o livro de Lamartine na mesma página de sempre. Ainsi, toujours poussés vers de nouveaux rivages. Desta vez, leu o verso seguinte. Dans la nuit éternelle emportés sans retour. Na noite eterna, levados sem retorno. Fechou o livro e deitou. Não chorou. Aurora Svensson não chorava. Ou chorava para dentro, como Casandra Russel, embora não soubesse que dividia isso com uma mulher que nunca tinha conhecido.', 0.4),
 ('c093', 'N', 'Dormiu. E pela primeira vez em meses, não sonhou com Aarav. Sonhou com olhos verdes. Com mãos abertas. Com uma voz que dizia é imperdoável, e que, justamente por dizer isso, tornava o perdão possível. Mas não agora. Não ainda. Primeiro, a distância.', 0.0),
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
    sf.write(f"{SCR}/cap12-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap12-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap12-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
