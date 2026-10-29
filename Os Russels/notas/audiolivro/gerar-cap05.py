import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts5"
SCR = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
# NOVAS vozes: Josh (Achird, jovem/caloroso), Dylan (Zubenelgenubi, casual/seco) — a AUDITAR com a autora
V = {"N": "Vindemiatrix", "AU": "Leda", "EL": "Gacrux", "RAJ": "Algieba",
     "JOSH": "Zubenelgenubi", "DYLAN": "Achird",
     "HELLE": "Achernar", "LARSEN": "Kore",
     "MIK": "Sulafat", "FRED": "Autonoe", "LOV": "Laomedeia", "CAS": "Pulcherrima"}
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
 # --- abertura: contexto mastigado para quem ouve ---
 ('v01', 'N', 'Você está ouvindo O Afilhado. Uma produção Romance no Bolso. Capítulo cinco: O que as mãos sabem.', 1.2),
 ('v02', 'N', 'Josh Russel tinha vinte e um anos e era o segundo dos cinco filhos de uma família de fazendeiros do interior, de uma fazenda perto de Sorô. O pai, Henrik, morrera havia quatro anos. Desde então, quem segurava a casa, a terra e os filhos era a mãe, Casandra Russel. E fora Casandra quem mandara Josh para a capital, para estudar sob a tutela do padrinho, o senhor Svensson, o pai de Aurora.', 0.5),
 ('v03', 'N', 'Fazia agora um mês que ele morava naquela casa da cidade. Um mês dividindo o teto com Aurora, a filha do padrinho, que ainda vestia o luto pelo irmão, Aarav, que partira numa viagem ao Ceilão e nunca mais voltara. Aurora, que no começo mal lhe dirigia a palavra.', 0.6),
 ('v04', 'N', 'Josh escrevia à mãe todas as noites. Não porque Casandra exigisse. Casandra Russel não exigia nada por escrito, porque tudo o que exigia estava costurado nos ossos dos filhos. Ele escrevia porque, nas horas entre o jantar e o sono, a casa dos Svensson mergulhava num silêncio de paredes grossas e cortinas pesadas, tão diferente do silêncio do campo. Lá, o silêncio era vivo, feito de grilos, de vento, do respirar dos animais no celeiro. Aqui era morto. Um silêncio de museu. E Josh sentia uma necessidade quase física de falar com alguém que o conhecesse inteiro.', 0.4),
 ('v05', 'N', 'Não a versão da cidade. Não o rapaz de casaco azul-marinho que segurava xícaras de porcelana e respondia com educação calculada às perguntas de senhoras perfumadas. O Josh de verdade. O que acordava antes do sol. O que sabia pelo cheiro da terra se ia chover. O que rachava troncos com três golpes de machado e dormia antes de a cabeça tocar o travesseiro. Esse Josh estava ficando embaçado. Como uma imagem refletida na água, quando alguém joga uma pedra.', 0.5),
 ('v06', 'N', 'Naquela noite, à luz de vela, ele molhou a pena e escreveu:', 0.4),
 ('v07', 'JOSH', 'Querida mãe. Já faz um mês. A cidade continua barulhenta, e os talheres continuam sendo mais do que qualquer pessoa razoável precisaria para comer. O padrinho me apresentou a algumas famílias. Gente educada, bem-vestida, com opiniões fortes sobre política, e opiniões ainda mais fortes sobre quem deve casar com quem. Parece que aqui casamento é o principal esporte, e todo mundo treina o ano inteiro para a temporada.', 0.4),
 ('v08', 'JOSH', 'Os estudos vão bem. Ráge me emprestou o segundo volume do Montesquiê, e estamos discutindo a separação dos poderes. Ele acha que a Dinamarca vai ter uma constituição em menos de vinte anos. Eu acho que ele é otimista, mas não digo isso, porque ele fica com uma cara de decepção, quando discordo, que me faz sentir como se tivesse chutado um cachorro.', 0.5),
 ('v09', 'N', 'Josh parou. Molhou a pena outra vez. O tinteiro de porcelana, presente do padrinho, mais elegante do que qualquer tinteiro que ele já tivesse visto na vida, captou a luz da vela e devolveu um brilho azulado. Ele começou a frase seguinte. A filha dele... E parou de novo. Olhou para o teto, procurando palavras que dissessem o suficiente sem dizer demais. O problema era que agora havia mais para não dizer.', 0.5),
 ('v10', 'N', 'Havia, por exemplo, as manhãs na cozinha. Ninguém combinou nada. Simplesmente aconteceu. Na manhã seguinte ao chá na casa da senhora Mikkelsen, aquela tarde de perguntas disfarçadas entre as senhoras da boa sociedade, Josh desceu à cozinha às seis e dez, e Aurora já estava lá. Na manhã depois dessa, Aurora desceu às seis, e Josh já estava lá. E assim por diante, dia após dia, como se os relógios dos dois tivessem se acertado em silêncio, sem consultar nenhum deles.', 0.4),
 ('v11', 'N', 'Não conversavam de verdade. Trocavam frases mínimas, como placas de estrada. A chaleira está quente. O chá está no pote da direita. Kóngen comeu um rato esta noite. Essa última foi de Josh: Kóngen era o gato enorme e cinzento de Fru Larsen, a cozinheira, e Josh encontrara a prova ao lado do fogão e achou que alguém deveria ser informado. Aurora respondia com frases curtas que eram, para os padrões dela, praticamente discursos.', 0.4),
 ('v12', 'N', 'Mas o silêncio entre as frases era diferente agora. Não era o silêncio de quem exclui. Era o silêncio de quem permite. Como dois animais que dividem a mesma sombra no calor: não são amigos, não são aliados, mas reconhecem que a sombra é melhor compartilhada do que disputada. Josh não escreveu nada disso para a mãe. Escreveu apenas:', 0.4),
 ('v13', 'JOSH', 'A filha dele é reservada, mas estamos nos acostumando um com o outro. A primavera chegou e o jardim está bonito. Mande notícias de todos. Como está o joelho do Joseph? O Dylan já consertou a cerca do pasto norte? A Meridiana está falando com as macieiras de novo? Saudades. Josh.', 0.5),
 ('v14', 'N', 'Joseph, o irmão mais velho. Dylan, o terceiro. Meridiana, a única menina, que conversava com as árvores do pomar. Josh dobrou a carta, selou, e juntou à pilha que entregava toda sexta-feira a Helle, a criada da casa, para o correio. Helle recebia as cartas com aquele rubor constante que Josh já desistira de evitar. Olhar para o chão não adiantava. Olhar para o lado não adiantava. Basicamente, existir na mesma sala que Helle não adiantava.', 0.4),
 ('v15', 'N', 'Ele apagou a vela, deitou-se, e pensou nas roseiras. As roseiras do jardim tinham sido plantadas por Aarav, o irmão que Aurora perdeu, e era ela quem cuidava delas agora. Em março, logo que chegou, Josh a vira podando e comentara, sem rodeios, que o corte tinha ficado uns três centímetros acima do ponto certo. Depois, na biblioteca, indicara a ela um tratado de botânica, terceira prateleira, capítulo nove, sobre rosas. Aurora não respondeu nada. Mas dias depois, os cortes estavam mais baixos. Três centímetros mais baixos.', 0.4),
 ('v16', 'N', 'Agora a primavera tinha acordado tudo. Os galhos nus que Aurora podara estavam cobertos de brotos verdes, minúsculos, que se abriam para a luz com aquela confiança cega que só as coisas muito jovens possuem. Josh os observava da janela do quarto. Nunca do jardim, nunca de perto, porque o jardim era de Aurora, e ele respeitava territórios como quem respeita cercas. E sabia, pelo formato dos brotos, que os cortes dela estavam funcionando.', 0.4),
 ('v17', 'N', 'Ela nunca mencionou o assunto. Ele nunca mencionou o assunto. O assunto existia entre os dois como uma moeda enterrada no fundo de um rio: ambos sabiam que estava lá, mas nenhum ia mergulhar para buscá-la. O cheiro de jasmim e canela, o perfume de Aurora, não estava no corredor naquela noite. Ela andava subindo mais cedo. Josh não sabia se isso era bom ou ruim. Dormiu.', 1.2),
 # --- a carta de Casandra ---
 ('v18', 'N', 'A resposta da mãe chegou numa terça-feira. Helle a trouxe numa bandeja de prata. Uma bandeja de prata, para uma carta. O que dizia tudo sobre a diferença entre a capital e a fazenda. Josh abriu o lacre com o canivete do pai, num gesto mais de fazendeiro abrindo um saco de sementes do que de cavalheiro abrindo correspondência. Ele conhecia aquela caligrafia firme, inclinada para a direita, como conhecia os veios da mesa da cozinha de casa: de memória, de tato, de coração.', 0.5),
 ('v19', 'N', 'E era como se ouvisse a voz dela, direta, sem enfeite nenhum:', 0.3),
 ('v20', 'CAS', 'Meu filho. Fico contente que esteja bem, e que Ráge esteja cuidando da sua educação. Não me surpreende. Ráge sempre foi homem de palavra, mesmo quando a palavra custa caro.', 0.4),
 ('v21', 'CAS', 'Joseph está bem. O joelho melhorou, mas ele não descansa, porque descansar, para o Joseph, é o mesmo que morrer devagar. Já disse isso a ele quinhentas vezes. Vai ser a quinhentas e uma. Dylan consertou a cerca. Depois derrubou. Depois consertou de novo. Seu irmão tem uma relação com cercas que eu não pretendo entender.', 0.4),
 ('v22', 'CAS', 'Meridiana não está falando com as macieiras. Está falando com as pereiras agora. Acho que as macieiras disseram alguma coisa que a ofendeu. E o Matias perguntou se pode visitar você no verão. Eu disse que não, porque se aquele menino puser os pés na capital não vai querer voltar, e eu preciso dele aqui. Pelo menos até ele aprender que vaca não se ordenha sozinha.', 0.4),
 ('v23', 'N', 'Matias era o caçula, de treze anos. Josh riu. Uma risada de verdade, aberta, que encheu o quarto, e que ele abafou na mesma hora com a mão, porque rir alto naquela casa parecia violar algum código não escrito. E continuou lendo. A carta mudava de tom:', 0.4),
 ('v24', 'CAS', 'Agora, Josh. Eu vou ser direta, porque não sou mulher de rodeios, e você sabe disso.', 0.4),
 ('v25', 'CAS', 'Nas suas cartas, você escreve sobre tudo. A casa, a comida, os livros, o padrinho, a cozinheira, até o gato. Mas sobre a filha do Ráge, escreve meia frase. E essa meia frase muda de carta para carta. Na primeira, ela era educada. Na segunda, reservada. Na terceira, estamos nos acostumando. Eu criei cinco filhos, Josh. Sei o que significa quando um homem fala pouco sobre uma mulher. Significa que pensa demais.', 0.5),
 ('v26', 'CAS', 'Não estou dizendo para não pensar. Estou dizendo para ter cuidado. Essa menina perdeu um irmão. Você mora na casa do pai dela. O seu lugar ali é de hóspede e de pupilo. Lembre disso.', 0.5),
 ('v27', 'CAS', 'Mas lembre também que você é um Russel. E Russels não fogem do que sentem. Apenas escolhem o momento certo de agir. Te amo. Coma direito. E escreva mais sobre você, e menos sobre talheres. Sua mãe.', 0.7),
 ('v28', 'N', 'Josh releu a carta três vezes. Depois guardou-a na gaveta da escrivaninha, junto com as outras, e ficou sentado um longo momento, as mãos nos joelhos, o olhar perdido na janela. Casandra via tudo. Sempre vira. Via através de paredes, de cartas, de silêncios, de meias frases. Via o que os filhos não diziam com a mesma clareza com que via o que diziam.', 0.4),
 ('v29', 'N', 'Sei o que significa quando um homem fala pouco sobre uma mulher. Josh esfregou o rosto com as mãos. A mãe estava certa. Claro que estava. Ele pensava em Aurora. Nas manhãs na cozinha. Nos olhos cor de mel que mudavam com a luz. Na voz rouca dizendo eu sei, já li, com aquela sombra impossível de sorriso. No reflexo dela no vidro da carruagem, na volta do chá, quando os olhares dos dois se encontraram no vidro. Nela entre as roseiras, de mãos sujas, sem luvas. Real.', 0.4),
 ('v30', 'N', 'Pensava nela o tempo todo. Como um rio pensa na gravidade: sem perceber, sem poder evitar, sem ter escolha. Mas a mãe também tinha razão sobre o resto. Sobre o cuidado. Sobre o lugar. Sobre o momento. Josh guardou a carta, lavou o rosto, e desceu para as aulas com o padrinho.', 1.2),
 # --- a pérgola (POV Josh) ---
 ('v31', 'N', 'Aconteceu numa quinta-feira. Às quintas, a senhora Eleonora, mãe de Aurora, tocava cravo. Bach, como sempre, às três da tarde, como sempre. E Fru Larsen fazia a grande limpeza da cozinha, o que significava que a casa inteira cheirava a sabão e vinagre, e que ninguém, sob pena de morte ou pior, podia pisar na cozinha entre as duas e as cinco.', 0.4),
 ('v32', 'N', 'Josh estava no jardim. Abril tinha virado maio, e maio, ele descobriu, era a vingança da cidade contra o inverno. Tudo explodia. No fundo do jardim havia uma pérgola: uma estrutura de vigas de madeira, como um telhado vazado, coberta de trepadeiras, com um banco embaixo. As glicínias que a cobriam tinham acordado de uma vez, em cachos roxo-lilás pendurados como candelabros, perfumando tudo com uma doçura pesada, quase de licor. A hera dos muros virara uma parede verde. O jardim estava mais fechado, mais secreto do que nunca.', 0.4),
 ('v33', 'N', 'E as roseiras de Aarav estavam florindo. Josh as observava de longe, sentado no degrau da porta dos fundos, com um livro no colo que não estava lendo, quando ouviu um barulho. Um barulho do jardim. Algo entre um estalo e um gemido, vindo da pérgola. Levantou-se, foi até lá, e viu o problema.', 0.4),
 ('v34', 'N', 'Uma das vigas de madeira, a lateral esquerda, a mais antiga, escurecida pela chuva e pelo tempo, tinha rachado. Não partido, ainda não. Mas cedido o bastante para que toda aquela lateral se inclinasse perigosamente, puxando as glicínias para baixo, ameaçando desabar sobre o banco de madeira onde Aurora costumava sentar.', 0.4),
 ('v35', 'N', 'Josh avaliou o estrago com o olho de quem nasceu consertando coisas. A viga precisava ser trocada, mas por enquanto dava para escorar. O problema era o peso das flores: os cachos, bonitos como eram, somavam quilos sobre uma estrutura já comprometida. Se ele não aliviasse aquele peso e não pusesse um apoio, a pérgola inteira cederia na próxima chuva forte.', 0.4),
 ('v36', 'N', 'No canto do jardim, junto ao muro, havia uma pilha de lenha, empilhada com a bagunça de quem não entende de lenha. Mas entre as toras havia duas peças retas o suficiente para servir de escora. Josh tirou o casaco. Dobrou as mangas da camisa até os cotovelos. E começou a trabalhar.', 0.4),
 ('v37', 'N', 'Era a primeira vez em mais de um mês que ele usava o corpo para alguma coisa além de andar, sentar, comer e dormir. Os músculos que passara anos construindo, não em esportes de cavalheiro, mas no trabalho de verdade, carregar, erguer, cortar, puxar, finalmente tinham o que fazer. E o corpo respondeu com alívio. Com a gratidão de uma máquina que volta a funcionar depois de semanas parada.', 0.4),
 ('v38', 'N', 'Ele carregou as toras até a pérgola, uma debaixo de cada braço, com o equilíbrio de quem já fez aquilo mil vezes. Firmou a primeira escora sob a viga rachada com pancadas precisas da base da mão. Depois subiu na estrutura, descalço, porque as botas escorregavam na madeira úmida, e começou a soltar os galhos mais pesados das glicínias, afastando-os da parte que cedia.', 0.4),
 ('v39', 'N', 'A madeira rangia. As flores caíam como chuva roxa. O suor escorria pelas têmporas e empapava a camisa branca, até ela grudar no corpo, quase transparente, desenhando os ombros e as costas. Josh não percebeu, e não se importaria se percebesse. Porque naquele momento ele não estava na cidade. Estava no campo. Estava em casa. Fazendo algo que fazia sentido, com um corpo que existia para isso. Ele não ouviu Aurora chegar.', 1.2),
 # --- a janela (POV Aurora) ---
 ('v40', 'N', 'Agora, do outro lado da casa, no andar de cima. Aurora estava no quarto quando ouviu o estalo. Mais exatamente, estava tentando ler pela terceira vez o capítulo nove do livro de botânica, porque as duas primeiras tentativas tinham sido sabotadas por uma incapacidade inexplicável de se concentrar. Que ela atribuía ao calor de maio. E a absolutamente nada mais. O som a fez levantar e ir até a janela.', 0.4),
 ('v41', 'N', 'A janela do quarto dela dava para o jardim. Era a melhor vista da casa inteira: dali, Aurora via tudo lá embaixo sem que ninguém soubesse que ela via. Um privilégio que ela usava mais do que gostaria de admitir. Principalmente nas manhãs em que Josh se sentava no degrau dos fundos, com um livro no colo, olhando as roseiras com uma expressão que ela não conseguia decifrar daquela distância. Mas que a fazia ficar na janela mais tempo do que qualquer roseira justificava.', 0.4),
 ('v42', 'N', 'Naquele momento, ela viu a pérgola inclinada. Viu as glicínias pendendo. E viu Josh. Sem casaco. Sem sapatos. A camisa arregaçada, o cabelo caindo na testa, uma tora debaixo de cada braço, como se fossem de palha e não de carvalho maciço. Viu-o firmar a escora com três pancadas da mão. Viu-o subir na estrutura com a agilidade de um gato. Um gato grande, ela concedeu. Mas ainda assim um gato.', 0.4),
 ('v43', 'N', 'Ele se esticou para alcançar os galhos mais altos, e a camisa subiu. Por uma fração de segundo, Aurora viu a pele da barriga dele, bronzeada, tensa, com uma linha de pêlos claros que descia do umbigo e sumia na cintura da calça. E desviou os olhos tão depressa que bateu o cotovelo na moldura da janela. A dor foi útil. Devolveu-a à realidade.', 0.4),
 ('v44', 'N', 'Ela recuou. Sentou-se na cama, a mão apertando o cotovelo latejante. O coração batia acelerado. Pelo susto. Pela dor. E por absolutamente nenhuma outra razão que ela estivesse disposta a reconhecer. Mas o corpo tem memória própria. E a imagem, Josh descalço na pérgola, os braços se contraindo sob a camisa molhada de suor, as mãos que ela sempre notara mas nunca vira trabalhando de verdade, ficou gravada nos olhos dela como um selo de cera quente.', 0.4),
 ('v45', 'N', 'Aurora ficou na cama exatamente três minutos. Depois lavou o rosto na bacia da cômoda e se olhou no espelho. A moça do espelho tinha os olhos cor de mel um pouco arregalados. E as bochechas morenas, que não ficavam vermelhas como as das dinamarquesas, mas que ganhavam, quando ela se perturbava, um tom mais quente, como cobre aquecido pelo sol, estavam exatamente nesse tom. Aurora ordenou a si mesma, diante do espelho, baixinho, entre os dentes:', 0.25),
 ('v46', 'AU', 'Para, Aurora.', 0.4),
 ('v47', 'N', 'O espelho não obedeceu. E pelo visto o corpo de Aurora também não, porque as bochechas continuaram quentes, e a imagem de Josh continuou ali, nítida, como um móvel que alguém pôs no meio do quarto e que não se consegue tirar do lugar.', 0.4),
 ('v48', 'N', 'Aurora desceu ao jardim. Não porque quisesse. Porque precisava verificar a pérgola. A pérgola era parte do jardim. O jardim era dela. Era uma questão de responsabilidade. De manutenção. De propriedade. Não tinha nada a ver com Josh.', 0.5),
 ('v49', 'N', 'Quando ela chegou, ele já tinha terminado. A pérgola estava escorada, firme, sustentada por duas toras postas com uma precisão que era conhecimento, não improviso. Os galhos das glicínias estavam amarrados com tiras de pano. Aurora olhou melhor: era o cinto do casaco dele. Josh cortara o cinto do próprio casaco para usar de amarra. O casaco estava pendurado no encosto do banco, sem cinto, e Josh estava sentado de volta no degrau, com o livro no colo, como se nada tivesse acontecido.', 0.4),
 ('v50', 'N', 'Exceto que o cabelo estava colado à testa de suor. A camisa estava úmida, com pétalas roxas grudadas no ombro esquerdo. Os pés descalços estavam sujos de terra. E as mãos, aquelas mãos que Aurora não conseguia parar de notar, tinham arranhões finos nos nós dos dedos, do tipo que se ganha lidando com madeira bruta. Ele levantou os olhos e disse, como quem comenta o tempo:', 0.25),
 ('v51', 'JOSH', 'A pérgola tinha uma viga comprometida. Escorei por agora, mas vai precisar de um carpinteiro para trocar a peça. Se quiser, eu falo com o seu pai.', 0.45),
 ('v52', 'N', 'Aurora olhou para a pérgola. Para as escoras. Para o cinto sacrificado. Para os arranhões nas mãos dele. Ninguém pedira que ele fizesse aquilo. Ninguém sequer sabia que a pérgola estava cedendo. Nem ela, que passava horas no jardim todos os dias, tinha percebido. Ele viu. Avaliou. Agiu. Sozinho. Com as mãos. Como se consertar coisas fosse tão natural quanto respirar. Porque, para ele, era. Aurora disse, simplesmente:', 0.25),
 ('v53', 'AU', 'Obrigada.', 0.4),
 ('v54', 'N', 'A palavra saiu diferente. Sem a camada de porcelana. Sem o verniz da boa educação com que ela costumava se proteger. Era só uma palavra, simples, despida. E Josh pareceu perceber, porque algo mudou no olhar dele. Como uma porta que se move um centímetro: não o bastante para entrar, mas o bastante para ver que há luz do outro lado. Ele respondeu, com a mesma simplicidade:', 0.25),
 ('v55', 'JOSH', 'Não tem de quê.', 0.4),
 ('v56', 'N', 'Aurora ficou parada. Queria dizer mais alguma coisa. Algo que fosse mais do que obrigada, e menos do que tudo o que vinha se acumulando atrás das muralhas dela. Apontou para o banco sob a pérgola. O banco onde ela lia, onde cuidava das roseiras. O trono do seu território. E disse, com a voz mais baixa:', 0.25),
 ('v57', 'AU', 'O banco. Aarav mandou fazer, quando a pérgola ficou pronta. Ele dizia que toda pérgola precisa de um banco. Porque de que adianta ter sombra, se não se tem onde sentar.', 0.45),
 ('v58', 'N', 'Josh olhou para o banco. Depois para ela. Os olhos verdes dele, alaranjados agora com a luz do fim da tarde, tinham uma expressão que Aurora começava a reconhecer. Atenção. Não a atenção educada dos salões. Atenção de verdade. A atenção de quem guarda. Ele disse, baixo:', 0.25),
 ('v59', 'JOSH', 'Ele estava certo.', 0.45),
 ('v60', 'N', 'Aurora assentiu, e virou-se para ir embora. Josh a chamou, formal, como sempre a chamava:', 0.2),
 ('v61', 'JOSH', 'Senhorita Svensson?', 0.4),
 ('v62', 'N', 'Ela parou. Não se virou. Ele continuou, prático:', 0.2),
 ('v63', 'JOSH', 'O banco precisa de uma mão de verniz antes do verão. A madeira está ressecada pelo inverno. Se não tratar, vai rachar.', 0.5),
 ('v64', 'N', 'Aurora ficou de costas para ele por três segundos. E então disse, como quem entrega uma chave:', 0.25),
 ('v65', 'AU', 'Me chame de Aurora.', 0.5),
 ('v66', 'N', 'Silêncio. E então Josh respondeu, e havia um sorriso na voz dele, aquele sorriso torto que Aurora nunca vira de frente, mas que suspeitava existir:', 0.25),
 ('v67', 'JOSH', 'Se a Fru Larsen me chama de Josh, a Helle me chama de Senhor Russel, e o gato não me chama de nada, parece justo que você decida como quer me chamar. Mas se eu sou Josh, você é Aurora.', 0.5),
 ('v68', 'N', 'Ela não se virou. Mas falou. E a voz não tinha porcelana, nem verniz, nem armadura. Tinha só ela:', 0.25),
 ('v69', 'AU', 'O verniz está no armário debaixo da escada. Terceira prateleira. Atrás das velas.', 0.5),
 ('v70', 'N', 'E saiu. Josh ficou olhando a porta por onde ela desaparecera. Depois o banco. Depois as próprias mãos arranhadas. Depois o céu de maio, que ficava cor de pêssego no horizonte, e que não se parecia em nada com o céu do campo. Mas que, naquele instante, com pétalas de glicínia nos ombros, terra nos pés, e o nome dela ainda vibrando no ar como a última nota de uma corda tocada e solta, pareceu a Josh o céu mais bonito que ele já vira na vida. Ele disse, para ninguém, testando o peso da palavra na língua:', 0.25),
 ('v71', 'JOSH', 'Aurora.', 0.5),
 ('v72', 'N', 'Três sílabas. Leves. Luminosas. Como o nome de uma coisa que nasce no horizonte. Kóngen, o gato da cozinheira, apareceu no canto do jardim. Olhou para Josh com aquele olho amarelo que julgava sem piedade. Bocejou. E foi embora, a cauda cinzenta balançando com a indiferença de quem já decidiu que humanos são uma espécie sem conserto. Josh sorriu. O sorriso torto. O de verdade.', 1.2),
 # --- fecho ---
 ('v73', 'N', 'Naquela noite, ele sentou-se à escrivaninha e pegou a pena. Pensou na mãe. Abriu a gaveta e releu a frase da carta dela, que ardia como brasa: Sei o que significa quando um homem fala pouco sobre uma mulher. E, logo abaixo: Russels não fogem do que sentem. Apenas escolhem o momento certo de agir. Fechou a gaveta.', 0.4),
 ('v74', 'N', 'Não escreveu à mãe naquela noite. Em vez disso, abriu o livro de botânica de Aurora. Capítulo nove, a parte sobre a poda de primavera. E leu até encontrar o trecho sobre verniz para madeira exposta ao tempo: tipos de resina, modo de aplicar, cuidados para não manchar.', 0.4),
 ('v75', 'N', 'Na manhã seguinte, às cinco e quarenta, antes que qualquer pessoa da casa acordasse, antes até de Aurora, que também acordava muito cedo, Josh desceu ao armário debaixo da escada. Terceira prateleira. Atrás das velas. Encontrou o verniz. E levou para o jardim.', 0.0),
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
    sf.write(f"{SCR}/cap05-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap05-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap05-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
