import requests
import json
import sys
import asyncio
from config import TOKEN

async def audio_ai(text, option, music_name, user_id):
    while True:
        # отправляем запрос неиронке
        url = "https://api.edenai.run/v2/audio/text_to_speech"
        list_token = ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMGQzZGFmODMtYjA5OS00YmE1LThiMTAtYWUxZGFlY2ViYTY3IiwidHlwZSI6ImFwaV90b2tlbiJ9.Vk-laUTs95-2OM38H4xxP4T9rHBycqT-731J0PTvpk0'] #тут должен быть запрос Валеры

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
            pass

if __name__ == "__main__":
    args = sys.argv[1:]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(audio_ai(*args))
'''async def main():
    await audio_ai(text='Patrik, shto tyi tut delaesh, kopayu. Zahem tyi nadel mou keplu - ne znaju', option='MALE', music_name='yola', user_id=5500790836)

asyncio.run(main())
'''
