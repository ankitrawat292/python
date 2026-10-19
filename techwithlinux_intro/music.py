import numpy as np, wave
sr=44100; dur=12; t=np.arange(int(sr*dur))/sr
rng=np.random.default_rng(7)
def env(t0,a,d):
    x=t-t0; return np.where(x<0,0,np.where(x<a,x/a,np.exp(-(x-a)/d)))
out=np.zeros_like(t)
# pad chord (Am - F feel), swelling
for f in [110,164.81,220,261.63,329.63]:
    out+=0.05*np.sin(2*np.pi*f*t+np.sin(2*np.pi*0.3*t))*np.clip(t/3,0,1)
# typing clicks 0.3-1.3s
for k in np.arange(0.3,1.3,0.033):
    out+=0.25*rng.standard_normal(len(t))*env(k,0.001,0.006)*(rng.random()>0.2)
# OK beeps
for k in [1.5,1.9,2.3]: out+=0.15*np.sin(2*np.pi*1320*t)*env(k,0.005,0.06)
# whoosh into flash
noise=rng.standard_normal(len(t)); wh=np.convolve(noise,np.ones(40)/40,'same')
out+=0.6*wh*np.exp(-((t-3.4)/0.35)**2)
# impacts (sub boom)
for k,amp in [(3.6,0.9),(8.6,0.8)]:
    x=np.clip(t-k,0,None); out+=amp*np.sin(2*np.pi*(45+60*np.exp(-x*20))*x)*env(k,0.003,0.5)
# beat from 3.6s, 120bpm
for k in np.arange(3.6,11.6,0.5):
    x=np.clip(t-k,0,None); out+=0.5*np.sin(2*np.pi*(50+90*np.exp(-x*30))*x)*env(k,0.002,0.15)
for k in np.arange(3.85,11.6,0.5): out+=0.12*noise*env(k,0.001,0.03)
# letter ticks
for k in [5.2+i*.12 for i in range(8)]+[6.6+i*.16 for i in range(5)]:
    out+=0.12*np.sin(2*np.pi*(880+rng.integers(0,6)*110)*t)*env(k+0.4,0.003,0.08)
# sparkle at subscribe
for i,f in enumerate([1318.5,1568,1975.5,2637]): out+=0.1*np.sin(2*np.pi*f*t)*env(9.6+i*0.08,0.004,0.4)
out*=np.clip((12-t)/0.6,0,1)
out=out/np.max(np.abs(out))*0.9
st=np.stack([out,np.roll(out,200)],1)
with wave.open('music.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st*32767).astype(np.int16).tobytes())
