import sys, numpy as np, soundfile as sf, subprocess
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8')
def load16(p):
    out=subprocess.run(["ffmpeg","-i",p,"-ac","1","-ar","16000","-f","f32le","-","-loglevel","error"],capture_output=True).stdout
    return np.frombuffer(out,dtype=np.float32)
for p in sys.argv[1:]:
    segs,_=m.transcribe(load16(p),language='pt',beam_size=5)
    print(p.split('/')[-1],'|',' '.join(x.text.strip() for x in segs))
