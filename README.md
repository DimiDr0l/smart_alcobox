# smart_alcobox

Ассистент "Наливатор" для застолья, умееет рассазывать шутки, анекдоты и т.п. так же преспособлен для наливания стопок)

помогли следующие статьи:
* [Моя б̶е̶з̶умная колонка или бюджетный DIY голосового ассистента для умного дома](https://habr.com/ru/companies/timeweb/articles/772080)
* [Моя б̶е̶з̶умная колонка: часть вторая // программная](https://habr.com/ru/companies/timeweb/articles/817929)
* [Адаптация языковой модели vosk](https://habr.com/ru/articles/735480)
* [holo-assistant](https://github.com/jessp/holo-assistant/tree/main/serverAudio)


## install:
```bash
apt update && apt upgrade
apt install python3-dev ffmpeg vim portaudio19-dev alsa-base alsa-utils -y
pip3 install -r requirements.txt
#export Yandex api key
export API_KEY=AQVN...
python3 main.py
```
