import speech_recognition as sr     # pip install SpeechRecognition
from witkeys import *   # 32 karakterlik bir string
import webbrowser       # pip install webbrowser
from gtts import gTTS   # pip install gtts
import pyttsx3          # pip install pyttsx3
import os
from datetime import datetime
import time
 
uyku = True
pyttsx3_kullan=False
speech_engine = pyttsx3.init()
speech_engine.setProperty('rate', 150)
speech_engine.setProperty('language', 'tr')
say = 0
 
def seslendir(mesaj):
    if pyttsx3_kullan:
        speech_engine.say(mesaj)
        speech_engine.runAndWait()
        return
 
    global say
    say += 1
    print("Asistan : ", mesaj)
 
    dosya = f"zz{say}.mp3"
    print(dosya)
    seslendirilecek = gTTS(text=mesaj, lang='tr')
    try:
        seslendirilecek.save(dosya)
        print(dosya+ " kaydedildi")
        komut = f"mpg123 -q {dosya}"
        os.system(komut)
        time.sleep(1)
 
        os.remove(dosya)
    except Exception as e:
        print(e)
 
def dingdong():
    komut = f"mpg123 -q ding-dong.mp3"
    os.system(komut)
 
def komutal(uyku):
    # create a Recognizer() instance and assign it to r
    r = sr.Recognizer()
    audio = ''
    # sr.Microphone() nesnesini oluştur ve source adı ver
    with sr.Microphone() as source:
        # enerji eşik değerini otomatik olarak belirle
        # eğer gürültüsüz bir ortamdaysanız buna gerek olmayabilir
        r.adjust_for_ambient_noise(source, duration=1)
 
        # konuşması için kullanıcıyı uyar
        if uyku == False:
            dingdong()
 
        # bekleme süresini 5 sn ile sınırlayarak dinlemeye başla
        # konuşma uzunluğunu 5 sn ile sınırla
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        print('Sesi aldım')
        simdi = datetime.now()
        filename=simdi.strftime("cumleler/%Y%m%d_%H%M%S")+".wav"
        with open(filename,"wb") as f:
            f.write(audio.get_wav_data())
        print('Sesi kaydettim')
        # try-except bloğu başlat
        try:
            # yakalanan sesleri varsayılan ön değerlerle facebook'a gönder
            # geri dönen stringi mesaj değişkenine ata ve ekrana bas
            print("Şimdi lütfen bekle... wit.ai çözümleme yapıyor.")
            mesaj = r.recognize_wit(audio, key=5HBECFHLX4WMRLY436RXNVILQXB7MW5B)
            mesaj = mesaj.lower().strip()
            if len(mesaj)>0:
                print("ÇÖZÜM: ",mesaj)
                print('Ses çözümlendi.')
            return mesaj
 
        # istisnaları denetle
        except sr.WaitTimeoutError:
            print("Süre aşımı.")
        except sr.UnknownValueError:
            print("Wit.ai Speech Recognition sesli mesajı anlayamadı")
        except sr.RequestError as e:
            print(f"Wit.ai Speech Recognition servisi yanıt vermiyor: {e}")
        except Exception as ee:
            print(f"Hata: {ee}")
 
if __name__ == '__main__': 
    while True:
        komut = komutal(uyku)
        if "stop" in komut: break
        if "bitti" in komut: break
        if "bitir" in komut: break
        if "merhaba" in komut: uyku = False
        if "günaydın" in komut: uyku = False
        if "uyu" in komut: uyku = True
        if "hoşça kal" in komut: uyku = True
        if uyku:
            print("uyku modu")
            continue
        print("asistan komut bekliyor (sorgula/stop/bitti/bitir/uyu/hoşça kal/facebook/youtube)")
 
        if "sorgula" in komut:
            try:
                kelimeler = komut.split()
                endeks = kelimeler.index("sorgula")
                sorgu=""
                i = endeks + 1
                while i < len(kelimeler):
                    sorgu += " " + kelimeler[i]
                    i += 1
                print("sorgu= ", sorgu)
                webbrowser.open(f"https://yandex.com.tr/search/?text='{sorgu}'")
                uyku = True
            except:
                webbrowser.open("https://yandex.com.tr/")
 
        elif "facebook" in komut:
            webbrowser.open("https://www.facebook.com")
            uyku = True
        elif "youtube" in komut:
            webbrowser.open("https://www.youtube.com")
            uyku = True
