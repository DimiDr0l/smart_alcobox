import io
import sys
import os
import grpc
import pydub
import sounddevice as sd
import soundfile as sf

import yandex.cloud.ai.tts.v3.tts_pb2 as tts_pb2
import yandex.cloud.ai.tts.v3.tts_service_pb2_grpc as tts_service_pb2_grpc

API_KEY = os.environ.get('API_KEY', '')

mic = 3                                                 # адрес аудиоустройства микрофона
on_mic  = f'amixer -c {mic} set Mic cap > /dev/null'    # команда отключения глушилки
off_mic = f'amixer -c {mic} set Mic nocap > /dev/null'  # команда на глушение микрофона

# Задайте настройки синтеза.
def synthesize(api_key, text, s_voice) -> pydub.AudioSegment:
    request = tts_pb2.UtteranceSynthesisRequest(
        text=text + '..',
        output_audio_spec=tts_pb2.AudioFormatOptions(
            container_audio=tts_pb2.ContainerAudio(
                container_audio_type=tts_pb2.ContainerAudio.WAV
            )
        ),
        # Параметры синтеза
        hints=[
            tts_pb2.Hints(voice=s_voice),  # (Опционально) Задайте голос. Значение по умолчанию marina
            tts_pb2.Hints(role='good'),  # (Опционально) Укажите амплуа, только если голос их имеет
            tts_pb2.Hints(speed=1.1),  # (Опционально) Задайте скорость синтеза
        ],
        unsafe_mode=True,
        loudness_normalization_type=tts_pb2.UtteranceSynthesisRequest.LUFS
    )

    # Установите соединение с сервером.
    cred = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel('tts.api.cloud.yandex.net:443', cred)
    stub = tts_service_pb2_grpc.SynthesizerStub(channel)

    # Отправьте данные для синтеза.
    it = stub.UtteranceSynthesis(request, metadata=(
        ('authorization', f'Api-Key {api_key}'),
    ))

    # Соберите аудиозапись по порциям.
    try:
        audio = io.BytesIO()
        audio_length_ms = 0
        for response in it:
            audio.write(response.audio_chunk.data)
            audio_length_ms += response.length_ms
        audio.seek(0)
        return pydub.AudioSegment.from_wav(audio), audio_length_ms
    except grpc._channel._Rendezvous as err:
        print(f'Error code {err._state.code}, message: {err._state.details}')
        raise err

def speak(text, voice = 'alexander'):
    if API_KEY == '':
        print("API_KEY no define")
        sys.exit()
    os.system(off_mic)        # глушим микрофон
    audio, audio_length_ms = synthesize(API_KEY, text, voice)
    samples = audio.get_array_of_samples()
    print(f'length_ms: {audio_length_ms}')
    sd.play(samples, samplerate=audio.frame_rate)
    sd.wait()
    del audio
    os.system(on_mic)         # отключаем глушилку микрофона

def play_wav(file: str):
    # Чтение WAV-файла
    data, samplerate = sf.read(file, dtype='int16')
    os.system(off_mic)
    # Воспроизведение WAV-файла
    sd.play(data, samplerate)
    sd.wait()  # Ожидание завершения воспроизведения
    # sd.stop()
    os.system(on_mic)

if __name__ == '__main__':
    speak('Встретились два друга, и один говорит:\n\n— Ты представляешь, вчера встретил своего старого знакомого, так он мне столько интересного рассказал!\n\n— И что же? — спрашивает второй.\n\n— Да так, ничего особенного, просто он считает, что жизнь — это как коробка шоколадных конфет: никогда не знаешь, какая начинка тебе попадётся.')
    play_wav('wav/otification.wav')
