import json, base64, subprocess, os, wave, time, numpy as np, soundfile as sf

BASE = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad/gtts3"
SCR = "/tmp/claude-0/-home-user/02172d33-003a-562c-8c14-54fc7ca69dd4/scratchpad"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
SR = 24000
# NOVAS vozes: Josh (Achird, jovem/caloroso), Dylan (Zubenelgenubi, casual/seco) — a AUDITAR com a autora
V = {"N": "Vindemiatrix", "AU": "Leda", "EL": "Gacrux", "RAJ": "Algieba",
     "JOSH": "Zubenelgenubi", "DYLAN": "Achird",
     "HELLE": "Achernar", "LARSEN": "Kore"}
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
 ("t01","N","Na casa dos Svensson havia regras. Não regras escritas, penduradas na parede, mas regras costuradas nos hábitos e nos gestos de cada pessoa daquele casarão, invisíveis como raízes, e essenciais. Josh aprendeu a primeira na manhã seguinte à sua chegada.",0.5),
 ("t02","N","A mesa era posta às sete e quarenta e cinco. Nem um minuto antes, nem um depois. Quem mandava nisso era Fru Larsen, a cozinheira: uma mulher de sessenta e tantos anos, baixa e larga como um barril, de mãos vermelhas e olhos azuis muito claros, que comandava a cozinha como um general comanda um exército.",0.5),
 ("t03","N","Josh, acostumado a levantar às cinco no campo, desceu às sete e meia. Encontrou a sala vazia, e Helle, a criada, uma moça tímida de bochechas vermelhas, quase derrubou a bandeja de prata ao vê-lo. Ela gaguejou:",0.25),
 ("t04","HELLE","Senhor Russel! O café ainda não está...",0.35),
 ("t05","JOSH","Eu sei. Desculpe. Posso esperar aqui?",0.35),
 ("t06","N","Helle respondeu, aflita:",0.25),
 ("t07","HELLE","O senhor pode esperar na sala de estar. Ou na biblioteca. Os senhores costumam...",0.3),
 ("t08","N","Josh interrompeu, com simplicidade:",0.25),
 ("t09","JOSH","Posso ajudar a pôr a mesa?",0.4),
 ("t10","N","Helle olhou para ele como quem recebe um objeto cuja função desconhece, e repetiu:",0.25),
 ("t11","HELLE","Ajudar?",0.3),
 ("t12","JOSH","A pôr a mesa. Eu sei pôr uma mesa. Provavelmente não do jeito de vocês, mas eu aprendo depressa.",0.45),
 ("t13","N","Da cozinha veio uma voz grave e imperativa. Era Fru Larsen:",0.25),
 ("t14","LARSEN","Quem está aí, Helle?",0.3),
 ("t15","HELLE","O senhor Russel, Fru Larsen. Ele quer ajudar a pôr a mesa.",0.45),
 ("t16","N","Passos pesados. A cozinheira apareceu na porta, secando as mãos num pano de prato, e olhou para Josh como quem examina um corte de carne no açougue. Disse, só para confirmar que tinha ouvido direito:",0.25),
 ("t17","LARSEN","Pôr a mesa.",0.3),
 ("t18","JOSH","Se não for incômodo, senhora.",0.3),
 ("t19","LARSEN","O senhor é hóspede nesta casa.",0.3),
 ("t20","N","Josh respondeu:",0.2),
 ("t21","JOSH","Sim, senhora. Mas um hóspede com duas mãos funcionando.",0.45),
 ("t22","N","Algo se mexeu no canto da boca de Fru Larsen. Não chegou a ser um sorriso; aquele rosto parecia considerar sorrisos um desperdício. Mas foi uma concessão. Ela apontou o aparador:",0.25),
 ("t23","LARSEN","Garfos à esquerda. Facas e colheres à direita. Se colocar o garfo de peixe onde vai o de carne, eu vou saber. E o senhor vai se arrepender de ter saído da cama.",0.5),
 ("t24","N","Josh pôs a mesa. Errou o garfo de peixe. Fru Larsen corrigiu sem dizer uma palavra, movendo o garfo dois centímetros para a esquerda. Quando os Svensson desceram, a mesa estava impecável, e Josh estava sentado no seu lugar: à direita do padrinho, de frente para Aurora.",0.5),
 ("t25","N","Aurora entrou às sete e quarenta e cinco em ponto, num vestido azul-claro com um broche de prata na gola, os cabelos presos num arranjo que deixava o pescoço à mostra. Josh não olhou para o pescoço dela. Ou melhor: olhou, por menos de um segundo, e depois fixou os olhos no prato como quem encara um inimigo. Ela disse, para a mesa em geral, sem olhar para ninguém:",0.25),
 ("t26","AU","Bom dia.",0.3),
 ("t27","N","E Josh respondeu do mesmo jeito, para a mesa em geral:",0.2),
 ("t28","JOSH","Bom dia.",0.4),
 ("t29","N","O padrinho abriu o jornal. Eleonora serviu o chá. E o café prosseguiu em silêncio educado, só com o tilintar das xícaras. Josh reparou que Aurora comia pouco e bebia o chá sem açúcar: amargo, sem concessões. Ela não olhou para ele nem uma vez. Josh sabia, porque estava contando.",0.7),
 ("t30","N","A segunda regra era sobre os espaços. A biblioteca era de todos, mas na prática era do padrinho. O escritório era só dele. A sala de costura, de Eleonora. A cozinha, de Fru Larsen. E o jardim... o jardim era de Aurora.",0.5),
 ("t31","N","Josh descobriu isso no segundo dia, quando saiu para caminhar depois do almoço, como fazia no campo, e encontrou Aurora ajoelhada entre as roseiras, de costas, sem luvas, as mãos na terra. Estava podando. Sabia onde cortar, mas a tesoura tremia antes de cada corte, como se ela pedisse desculpa à planta antes de feri-la.",0.4),
 ("t32","N","Era tão diferente da Aurora da sala de jantar que parecia outra pessoa: uma Aurora desarmada. Então ela virou a cabeça e o viu, e a transformação foi instantânea, como assistir alguém vestir uma armadura. Os ombros se retesaram, o queixo subiu, os olhos de mel ganharam um brilho metálico. Ela se levantou, limpando as mãos no avental, e disse:",0.25),
 ("t33","AU","Senhor Russel. Posso ajudá-lo em alguma coisa?",0.35),
 ("t34","N","Que era o jeito educado de dizer: o que você está fazendo no meu espaço. Josh se desculpou:",0.25),
 ("t35","JOSH","Desculpe. Não sabia que havia alguém aqui. Costumo caminhar depois do almoço. Vou voltar para dentro.",0.35),
 ("t36","N","Já estava se virando quando o olhar caiu sobre as roseiras. E o fazendeiro dentro dele falou antes que a prudência pudesse intervir:",0.25),
 ("t37","JOSH","O corte está um pouco alto.",0.5),
 ("t38","N","O silêncio que se seguiu tinha a qualidade de um fósforo aceso perto de pólvora. Aurora perguntou, gelada:",0.25),
 ("t39","AU","Perdão?",0.35),
 ("t40","N","Josh devia recuar. Mas era filho de Casandra Russel, e Casandra não criava filhos que engoliam a verdade por conveniência. Ele explicou, apontando a roseira:",0.25),
 ("t41","JOSH","O corte ficou uns três centímetros acima do nó. Assim, o galho novo nasce fraco e virado para dentro, sombreia o centro da planta e atrapalha o ar. No verão, isso vira fungo.",0.5),
 ("t42","N","Aurora olhou para a roseira. Para Josh. Para a roseira de novo. Havia raiva no rosto dela. Mas, debaixo da raiva, Josh viu outra coisa, tão enterrada que só alguém muito atento perceberia: dúvida. Porque as roseiras eram do irmão morto, e ela tentava cuidar delas como ele cuidava, mas ela não era Aarav. Ela disse, numa voz tão controlada que parecia passada a ferro:",0.25),
 ("t43","AU","Obrigada pela observação, Senhor Russel. Vou considerar.",0.35),
 ("t44","N","Josh corrigiu:",0.2),
 ("t45","JOSH","Josh. Meu nome é Josh. Senhor Russel era o meu pai.",0.45),
 ("t46","N","Os olhos dela mudaram, quase nada, como uma pedra jogada num lago muito fundo. Ela repetiu o nome, testando-o como quem testa a água com a ponta do pé:",0.25),
 ("t47","AU","Josh.",0.35),
 ("t48","N","E logo acrescentou, apressada, como se o som do nome a tivesse assustado:",0.25),
 ("t49","AU","O jantar é às sete. Não se atrase. Fru Larsen considera atraso uma ofensa pessoal.",0.45),
 ("t50","N","E saiu do jardim sem olhar para trás, as mãos ainda sujas de terra. Josh ficou entre as roseiras. O corte estava alto, como ele dissera. Mas ele não tocou nas plantas. Aquilo não era dele.",0.8),
 ("t51","N","Os dias foram passando, e Josh foi aprendendo as outras regras observando. Que o padrinho tomava café sozinho no escritório antes de descer. Que Eleonora tocava cravo às terças e quintas, sempre as mesmas peças, como quem reza. Que Fru Larsen tinha um gato enorme e cinzento, tratado como um rei. E foi aprendendo, dia após dia, os rituais de Aurora.",0.5),
 ("t52","N","Ela acordava cedo e descia à cozinha antes de todos, para fazer o próprio chá amargo. De manhã tinha aulas de francês com Fru Dahl, a governanta. Depois desaparecia, e só voltava no almoço, com aquele sorriso de porcelana. À tarde, ia às roseiras. Josh a via da janela do quarto leste. No quarto dia, notou que os cortes estavam mais baixos. Três centímetros mais baixos. Ele não disse nada.",0.7),
 ("t53","N","Na primeira semana, os dois trocaram exatamente trinta e duas frases. Josh sabia, porque contava tudo nas cartas que escrevia à mãe toda noite, à luz de vela. Escreveu assim:",0.3),
 ("t54","JOSH","Querida mãe. A casa é grande e bonita, e tem mais talheres do que pessoas. O padrinho é exatamente como a senhora descreveu: sério por fora, bom por dentro. A esposa dele toca cravo como se estivesse rezando. A cozinheira é uma tirana que comanda a casa de verdade. E a filha...",0.4),
 ("t55","N","Ali ele sempre parava. Molhava a pena. Olhava para o teto. Como descrever Aurora Svensson para Casandra Russel, que lia gente como Josh lia paisagens, sem que a mãe percebesse que o filho pensava demais numa garota que mal lhe dava bom-dia? Acabou escrevendo:",0.3),
 ("t56","JOSH","A filha é educada. Perdeu o irmão há pouco mais de um ano, e sente minha presença na casa como uma invasão, o que é compreensível. Estou dando espaço. Ela cuida das roseiras do irmão e bebe chá sem açúcar. Não se preocupe comigo. Estou me adaptando.",0.6),
 ("t57","N","E estava mesmo. O padrinho o inscrevera na universidade para o semestre de outono, e começara a orientá-lo pessoalmente, em filosofia e direito. As tardes no escritório, com cheiro de tabaco e couro, eram para Josh como encontrar água no deserto. Numa dessas tardes, o padrinho disse:",0.25),
 ("t58","RAJ","Você tem uma mente boa, Joshua. Ágil. Curiosa. Seu pai era assim.",0.4),
 ("t59","N","Josh engoliu o nó na garganta, e perguntou:",0.25),
 ("t60","JOSH","O senhor conheceu bem o meu pai?",0.35),
 ("t61","N","O padrinho tirou os óculos de leitura e limpou-os no lenço, um gesto que Josh já sabia anunciar algo sério:",0.25),
 ("t62","RAJ","O suficiente para saber que ele teria orgulho de você estar aqui. Henrik não tinha estudo, mas tinha o que a universidade não ensina: bom senso, senso de justiça. E uma teimosia monumental que, pelo visto, passou para o filho do meio.",0.4),
 ("t63","N","Josh quase sorriu:",0.2),
 ("t64","JOSH","Minha mãe diria que a teimosia é dela.",0.35),
 ("t65","N","E o padrinho, com uma sombra rara de sorriso:",0.25),
 ("t66","RAJ","E estaria certa. Casandra é a mulher mais teimosa que já conheci. Quando você nasceu, seu pai me escreveu: nasceu o do meio, vai ser o que dá mais trabalho. Eu ri, na época. Acho que ele tinha razão.",0.4),
 ("t67","JOSH","Eu não dou trabalho.",0.3),
 ("t68","RAJ","Dá, Joshua. O melhor tipo de trabalho. O que vale a pena.",0.5),
 ("t69","N","Josh guardou essas palavras no lugar onde guardava as coisas importantes, como um baú trancado no fundo do peito.",0.8),
 ("t70","N","No décimo dia, aconteceu a primeira rachadura. Pequena, quase invisível, como uma trinca num copo que ainda segura a água. Foi à noite. O jantar tinha sido silencioso: Eleonora, com enxaqueca, subira cedo, e Aurora pedira licença antes da sobremesa. Josh ficou na biblioteca, como já era seu hábito, lendo junto à lareira.",0.4),
 ("t71","N","Lia um tratado de botânica. Não por obrigação: queria entender as roseiras de Aurora. E queria, embora não admitisse, ter alguma coisa para dizer a ela que não fosse sobre talheres. Passava das dez. A casa dormia. As brasas pulsavam devagar.",0.5),
 ("t72","N","Então ele ouviu passos. Leves, descalços. Pararam na porta. A porta abriu devagar, e Aurora apareceu. Não a Aurora do dia: essa usava uma camisola branca até os tornozelos e um xale cinzento, os cabelos soltos até o meio das costas, os pés descalços no assoalho frio. E trazia um livro na mão. Vinha trocar um livro.",0.4),
 ("t73","N","Ela o viu, e ficou paralisada na porta como um cervo diante de uma tocha. Pela primeira vez, a voz dela não estava controlada. Estava crua:",0.25),
 ("t74","AU","Eu... eu não sabia que havia alguém aqui.",0.4),
 ("t75","N","Josh fez a única coisa que lhe pareceu certa. Fechou o livro, levantou-se, e disse:",0.25),
 ("t76","JOSH","Desculpe. Já estava de saída.",0.4),
 ("t77","N","Não estava. Mas, ao passar por ela na porta, mais perto do que jamais tinham estado, Josh viu que os olhos de mel estavam vermelhos. Ela tinha chorado. Sozinha, no quarto. E descido por um livro, porque não conseguia dormir. Josh conhecia aquilo. Era o jeito de Joseph, o irmão mais velho. O jeito da mãe. O jeito dele mesmo.",0.4),
 ("t78","N","Ele não disse nada sobre os olhos vermelhos. Não olhou para eles. Só parou ao lado dela e disse, num tom casual, sem fazer dela o centro de nada:",0.25),
 ("t79","JOSH","O tratado de botânica, na terceira prateleira, segunda fileira. Tem um capítulo sobre rosas que é muito bom. O capítulo nove, se não me engano.",0.5),
 ("t80","N","Silêncio. Não o silêncio de quem levanta muros: o silêncio de quem recebeu algo que não esperava, e ainda não sabe o que fazer com aquilo. Josh se despediu:",0.25),
 ("t81","JOSH","Boa noite, senhorita Svensson.",0.5),
 ("t82","N","E subiu para o quarto, sem olhar para trás. Sentou na cama, no escuro. E lá de baixo, quase inaudível, veio o som de um livro sendo tirado da estante. Terceira prateleira. Segunda fileira. Josh fechou os olhos. Não, disse a si mesmo, pela centésima vez em dez dias. Mas o não estava ficando menor. E Aurora estava ficando maior dentro dele.",0.5),
 ("t83","N","Ele acendeu a vela e escreveu outra carta:",0.3),
 ("t84","JOSH","Querida mãe. Tudo bem por aqui. A cidade é barulhenta, mas bonita. O padrinho me trata como filho. Estou lendo muito. As roseiras do jardim vão precisar de cuidados quando a primavera chegar. Acho que vou me oferecer para ajudar. Diga ao Matias que não chorar é diferente de ser forte. Ele vai entender. Com amor, Josh.",0.6),
 ("t85","N","Selou a carta e pousou-a na escrivaninha, ao lado da carta lacrada da mãe, que ele ainda não entregara ao padrinho. Porque, no fundo, desconfiava que aquela carta não era para o padrinho. Era para ele. Para quando precisasse de coragem. Soprou a vela. E no escuro do corredor, o cheiro de jasmim e canela pairava como uma promessa que ninguém tinha feito.",0.0)
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
    sf.write(f"{SCR}/cap03-completo.wav", mix, SR)
    subprocess.run(["ffmpeg","-y","-i",f"{SCR}/cap03-completo.wav","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11","-codec:a","libmp3lame","-q:a","2",
        f"{SCR}/cap03-completo.mp3","-loglevel","error"],check=True)
    print("TOTAL", f"{len(mix)/SR:.1f}s")
