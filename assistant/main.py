from speak import speak, play_wav
from recognize import *
from infinitetimer import InfiniteTimer
from yagpt import send_prompt
import glob_var

import os
import time
import sounddevice as sd
import vosk
import json
import queue

model = vosk.Model("model_stt/vosk-model-small-ru-0.22")      # Модель нейросети
samplerate = 44100                                            # Частота дискретизации микрофона
q = queue.Queue()                                             # Потоковый контейнер
default_voice = 'alexander'

def q_callback(indata, frames, time, status):
    q.put(bytes(indata))

def f_gpt_speak(request):
    r = send_prompt(
        'Ты ассистент \"наливатор\", рассказываешь анекдоты, тосты, шутки, пародии, как Гарик Харламов. Ответ должен быть без уточнений мест, имён или событий. ',
        request
    )
    speak(r, default_voice)

def f_about():
    f_gpt_speak('Поприветсвтуй гостей и расскажи о себе, кратко, не более 15 слов!')

def f_shutdown():
    speak('Выключаюсь...', default_voice)
    os.system('shutdown now')

def f_spill():
    os.system('gpio write  6 1')
    time.sleep(0.3)
    os.system('gpio write  6 0')
    play_wav('wav/notification.wav')

def voice_listen():
    def exit_listen():
        glob_var.set_bool_wake_up(False)
        play_wav('wav/cancel.wav')
        print("heard exit listen")

    def command_off():
        glob_var.set_bool_wake_up(False)
        t1.cancel()
        print("heard exit command")

    def command_processing(key: str, heard: str):
        command_off()
        if key == "help":
            # f_help()
            print('f_help()')
        elif key == "about":
            print('f_about()')
            f_about()
        elif key == "volup":
            # f_volup()
            print('f_volup()')
        elif key == "voldown":
            # f_voldown()
            print('f_voldown()')
        elif key == "volset":
            # f_volset()
            print('f_volset()')
        elif key == "tost":
            # f_tost()
            print('f_tost()')
        elif key == "spill":
            print('f_spill()')
            f_spill()
        elif key == "shutdown":
            print('f_shutdown()')
            f_shutdown()
        elif key == "change_voice":
            print('change_voice')
            global default_voice
            if default_voice == 'alexander':
                default_voice = 'alena'
            else:
                default_voice = 'alexander'
            speak('Привет!', default_voice)
        else:
            print('запрос в gpt')
            f_gpt_speak(heard)

    f_about()
    t_shutdown = InfiniteTimer(1800, f_shutdown) # 30 минут в простое
    t1 = InfiniteTimer(10, exit_listen)
    with sd.RawInputStream(callback=q_callback, channels=1, samplerate=samplerate, dtype='int16'):
        rec = vosk.KaldiRecognizer(model, samplerate)
        sd.sleep(-20)
        while True:
            heard = ''
            data = q.get()
            if rec.AcceptWaveform(data):
                heard = json.loads(rec.Result())["text"]
                if glob_var.read_bool_wake_up():
                    print(f"Фраза целиком: {heard}")
                    if heard and len(heard.split()) == 1 and name_recognize(heard):
                        play_wav('wav/notification.wav')
                        t1.start()
                    else:
                        if heard:
                            words = heard.split()
                            if name_recognize(words[0]):
                                words = words[1:]
                                heard = ' '.join(words)
                            command_processing(recognize_command(heard), heard)
                    t_shutdown.cancel()
                    t_shutdown.start()
                else:
                    continue
            else:
                heard = json.loads(rec.PartialResult())["partial"]
                if glob_var.read_bool_wake_up() == False and heard and name_recognize(heard):
                    glob_var.set_bool_wake_up(True)
                    print(f"Поток: {heard}  ::  {glob_var.read_bool_wake_up()}")

if __name__ == "__main__":
    os.system("gpio mode 6 out")
    voice_listen()