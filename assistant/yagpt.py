import requests
import os
import json

API_KEY = os.environ.get('API_KEY', '')
CATALOG = "b1g3v2u3uhn4v5pt4avc" #идентификатор_каталога
GPT_MODEL = "yandexgpt/latest"

def send_prompt(system_text: str, user_text: str):
    prompt = {
        "modelUri": f"gpt://{CATALOG}/{GPT_MODEL}",
        "completionOptions": {
            "stream": False,
            "temperature": 0.4,
            "maxTokens": "1000"
        },
        "messages": [
            {
                "role": "system",
                "text": f"{system_text}"
            },
            {
                "role": "user",
                "text": f"{user_text}"
            },
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.text
    json_data = json.loads(result)
    for alternative in json_data["result"]["alternatives"]:
        if alternative["status"] == "ALTERNATIVE_STATUS_FINAL":
            text = alternative["message"]["text"]
            return(text)

if __name__ == '__main__':
    print(
        send_prompt(
            'Ты ассистент \"наливатор\", рассказываешь анекдоты, тосты, шутки, пародии, как Гарик Харламов. Ответ должен быть без уточнений мест, имён или событий. ',
            'расскажи тост'
        )
    )

