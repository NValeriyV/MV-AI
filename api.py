import requests
import json
from config import TOKEN

def audio_ai(text, option, music_name, user_id):
    url = "https://api.edenai.run/v2/audio/text_to_speech"

    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzQ1MDZkNDAtMzA5OC00YzFlLTg4NDAtOGQ4NDUyMDIxZDAzIiwidHlwZSI6ImFwaV90b2tlbiJ9.2-C132_GY8FuaOdQ5lqQgZgPK0Atlob5xzeY8MJEdss"}
    data = {
        "providers": "microsoft,lovoai,google,ibm,amazon",
        "language": "fr",
        "text": f"{text}",
        "option": f"{option}",
        "settings": {}
    }

    response = requests.post(url, headers=headers, json=data)
    with open(f'{music_name}.json', 'w', encoding='utf-8') as file:
        file.write(response.text)

    with open(f'{music_name}.json', 'r') as file:
        json_data = json.load(file)

    music_file = json_data['microsoft']['audio_resource_url']

    res = requests.get(music_file)

    with open(f'{music_name}.mp3', 'wb') as file:
        file.write(res.content)

    print("Аудиофайл успешно сохранен как audio.mp3")

    bot_token = TOKEN

    # Путь к аудиофайлу
    audio_file_path = f'{music_name}.mp3'

    # URL для отправки аудиофайла
    url = f'https://api.telegram.org/bot{bot_token}/sendAudio'

    # Открытие аудиофайла в бинарном режиме
    with open(audio_file_path, 'rb') as audio:
        # Параметры запроса
        payload = {
            'chat_id': user_id,
            'title': 'Audio File',
            'parse_mode': 'Markdown'
        }
        
        # Файлы для отправки
        files = {
            'audio': audio
        }
        
        # Отправка POST-запроса на сервер Telegram
        response = requests.post(url, data=payload, files=files)
        
        # Проверка успешности отправки
        if response.status_code == 200:
            print('Аудиофайл успешно отправлен!')
        else:
            print('Ошибка при отправке аудиофайла:', response.text)

audio_ai(text='Patrik, shto tyi tut delaesh, kopayu. Zahem tyi nadel mou keplu - ne znaju', option='MALE', music_name='yola', user_id=5500790836)

