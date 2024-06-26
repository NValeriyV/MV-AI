import requests
import json
import sys
import asyncio
from config import TOKEN
from db1 import DataBase

db = DataBase('test.db')

async def audio_ai(text, option, music_name, leng, user_id):
    while True:
        # отправляем запрос неиронке
        print('Отправляем запрос на генерацию песни!')
        url = "https://api.edenai.run/v2/audio/text_to_speech"
        list_token = db.get_tokens_true()

        headers = {"Authorization": f"Bearer {list_token[0]}"}
        data = {
            "providers": "openai",
            "language": f"{leng}",
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
            music_file = json_data['openai']['audio_resource_url']

            res = requests.get(music_file)

            with open(f'{music_name}.mp3', 'wb') as file:
                file.write(res.content)

            print("Аудиофайл успешно сохранен как audio.mp3")
            
            # отправляет в телеграмм
            bot_token = TOKEN

            # Путь к аудиофайлу
            #audio_file_path = f'{music_name}.mp3'
            audio_file_path = f'{music_name}.mp3'
            print('test')

            # URL для отправки аудиофайла
            url = f'https://api.telegram.org/bot{bot_token}/sendAudio'

            # Открытие аудиофайла в бинарном режиме
            print(user_id)
            with open(audio_file_path, 'rb') as f:
                files = {
                    'audio': f
                }
                data = {'chat_id': user_id}
                
                # Отправка POST-запроса на сервер Telegram
                response = requests.post(url, data=data, files=files)
                
                # Проверка успешности отправки
                if response.status_code == 200:
                    print('Аудиофайл успешно отправлен!')
                else:
                    print('Ошибка при отправке аудиофайла:', response.text)
                
                break

        except:
            #запрос на изменение статуса токена в False (Валера)
            db.change_status_token(list_token[0])

async def main():
    await audio_ai(text='filles, garcons, doux comme des caramels ', option='MALE', music_name='yola', user_id=5500790836)

asyncio.run(main())


'''if __name__ == "__main__":
    args = sys.argv[1:]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(audio_ai(*args))'''
