import json,base64,subprocess,os,sys,numpy as np,soundfile as sf
model=sys.argv[1]; out=sys.argv[2]
URL=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DIR=("Leia em português do Brasil, com sotaque brasileiro, como uma cena de audiolivro de romance, interpretada por dois atores. "
"É madrugada, numa sala escura, e os dois falam baixo para não acordar a casa. "
"Josh tem vinte e um anos: voz de homem, grave, baixa, aveludada, quase rouca, carregada de desejo e de tensão. Ele está no limite, tentando se segurar, e não consegue. Nunca animado, nunca simpático, nunca leve. Ele respira entre as frases. "
"Aurora tem dezessete anos: voz suave, firme, às vezes desafiadora, às vezes insegura, sem nenhuma infantilidade.\n\n")
TXT="""Josh: É melhor eu subir.
Aurora: Por quê? Me fala. Qual é o problema?
Josh: Porque eu não confio em mim com você... quando a casa inteira está dormindo.
Aurora: Você já pensou nisso antes?
Josh: Todo dia. Há dois meses. Todo santo dia, Aurora.
Aurora: Então por que está me dizendo agora?
Josh: Porque você perguntou desse jeito. Olhando pra mim desse jeito.
Aurora: E se eu der mais um passo?
Josh: Aurora... se você der mais um passo, eu não vou conseguir recuar.
Aurora: Eu sei.
Josh: Eu já não estou conseguindo."""
body={"contents":[{"parts":[{"text":DIR+TXT}]}],"generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"multiSpeakerVoiceConfig":{"speakerVoiceConfigs":[
 {"speaker":"Josh","voiceConfig":{"prebuiltVoiceConfig":{"voiceName":"Zubenelgenubi"}}},
 {"speaker":"Aurora","voiceConfig":{"prebuiltVoiceConfig":{"voiceName":"Leda"}}}]}}}}
json.dump(body,open(out+".req","w"))
k=os.environ.get("GKEY"); u=URL+("?key="+k if k else "")
subprocess.run(["curl","-sS","-X","POST",u,"-H","Content-Type: application/json","-d","@"+out+".req","-o",out+".json"],check=True,timeout=300)
d=json.load(open(out+".json"))
try:
  pcm=base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
except Exception: print(json.dumps(d)[:300]); sys.exit(1)
a=np.frombuffer(pcm,dtype=np.int16).astype(np.float32)/32768
sf.write(out+".wav",a,24000); subprocess.run(["ffmpeg","-y","-i",out+".wav","-q:a","2",out+".mp3","-loglevel","error"])
print(out, len(a)/24000)
