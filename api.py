import requests
import json
from config import TOKEN
from db1 import DataBase

db = DataBase("test.db")

def audio_ai(text, option, music_name, user_id):
    while True:
        url = "https://api.edenai.run/v2/audio/text_to_speech"
        list_token = db.get_tokens_true()
        
        headers = {"Authorization": f"Bearer {list_token[0]}"}
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
            
        try:
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
                
                break

        except:     #запрос на изменение токена
            db.change_status_token(list_token[0])
            pass

#audio_ai(text='Patrik, shto tyi tut delaesh, kopayu. Zahem tyi nadel mou keplu - ne znaju', option='MALE', music_name='yola', user_id=5500790836)
