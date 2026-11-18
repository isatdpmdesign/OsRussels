import sys, difflib, re, unicodedata, numpy as np, subprocess
from faster_whisper import WhisperModel
src=open(sys.argv[1]).read().split('if __name__')[0]; ns={}; exec(src,ns)
m=WhisperModel('small',device='cpu',compute_type='int8')
def norm(t):
    t=unicodedata.normalize('NFKD',t.lower()); t=''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9 ]',' ',t).split()
def load16(p):
    out=subprocess.run(["ffmpeg","-i",p,"-ac","1","-ar","16000","-f","f32le","-","-loglevel","error"],capture_output=True).stdout
    return np.frombuffer(out,dtype=np.float32)
for slug,vk,text,g in ns["SEG"]:
    if text.startswith("Diga em voz baixa"): text=text.split(":",1)[1]
    segs,_=m.transcribe(load16(f"{ns['BASE']}/{slug}.seg.wav"),language='pt',beam_size=5)
    hyp=' '.join(x.text for x in segs)
    r=difflib.SequenceMatcher(None,norm(text),norm(hyp)).ratio()
    flag="  <<<" if r<0.85 else ""
    print(f"{slug} {vk} {r:.2f}{flag} | {hyp.strip()[:200]}", flush=True)
