from time import time
import cv2
from gtts import gTTS
import tempfile
from pygame import mixer

lastTime = time()
print(lastTime)
def speak(sentence, lang):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts=gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play(1)
while(True):
    if (time()-lastTime)<3:
        print('<3')
    elif (time()-lastTime)>3 :
        lastTime = time()
        speak("左手打平",'zh-tw')