import json
import os
import requests
import time
import hmac
import hashlib
from config import api_key, api_secret
from db import Database

#вставьте необходимые данные для подключения к базе
db = Database(apiKey='', authDomain="", projectId="", storageBucket="", messagingSenderId="", appId="", measurementId="", databaseURL="")

class SetPrice():
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
    
    def get_orders(self, symbol): #получение ордеров. 
        api_params = f'category=inverse&symbol={symbol}'
        
        url = f"https://api.bybit.com/v5/order/realtime?{api_params}"

        def sign(secret, data):
            return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()
        
        timestamp = str(int(time.time() * 1000))
        recv_window = '20000'

        headers = {
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-TIMESTAMP': timestamp,
            'X-BAPI-RECV-WINDOW': recv_window,
            'X-BAPI-SIGN': sign(api_secret, f"{timestamp}{api_key}{recv_window}{api_params}")
        }

        response = requests.get(url, headers=headers)
        return response.json()
    
    def get_price(self, symbol): #получение актуальной цены 
        api_params = f'category=inverse&symbol={symbol}&interval=1'
        
        url = f"https://api.bybit.com/v5/market/mark-price-kline?{api_params}"

        def sign(secret, data):
            return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()
        
        timestamp = str(int(time.time() * 1000))
        recv_window = '20000'

        headers = {
            'X-BAPI-API-KEY': api_key,
            'X-BAPI-TIMESTAMP': timestamp,
            'X-BAPI-RECV-WINDOW': recv_window,
            'X-BAPI-SIGN': sign(api_secret, f"{timestamp}{api_key}{recv_window}{api_params}")
        }

        response = requests.get(url, headers=headers)
        return response.json()
    
    def get_balance(self, coin, type): #функция для принятия платежа
        # Установите метод и вызов API
        api_method = "GET"
        api_call = "v5/asset/transfer/query-account-coins-balance"

        # Установите параметры API
        account_type = type
        api_params = f"accountType={account_type}&coin={coin}"

        # Установите окно ожидания и отметку времени
        recv_window = 5000
        timestamp = str(int(time.time() * 1000))

        # Функция для создания подписи запроса
        def sign(secret, data):
            return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()

        # Создайте подпись с использованием секретного ключа и параметров API
        signature = sign(api_secret, f"{timestamp}{api_key}{recv_window}{api_params}")

        # Сформируйте URL и заголовки запроса
        url = f"https://api.bybit.com/{api_call}?{api_params}"
        headers = {
            "X-BAPI-API-KEY": api_key,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-SIGN": signature,
            "X-BAPI-RECV-WINDOW": str(recv_window)
        }

        # Выполните GET запрос
        response = requests.get(url, headers=headers)

        # Проверьте статус код ответа
        return response.json()
    
    def get_pnl(self, pare): #получение pnl
        # Установите метод и вызов API
        api_method = "GET"
        api_call = "v5/position/closed-pnl"

        # Установите параметры API
        account_type = type
        api_params = f"category=inverse&symbol={pare}"

        # Установите окно ожидания и отметку времени
        recv_window = 5000
        timestamp = str(int(time.time() * 1000))

        # Функция для создания подписи запроса
        def sign(secret, data):
            return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()

        # Создайте подпись с использованием секретного ключа и параметров API
        signature = sign(api_secret, f"{timestamp}{api_key}{recv_window}{api_params}")

        # Сформируйте URL и заголовки запроса
        url = f"https://api.bybit.com/{api_call}?{api_params}"
        headers = {
            "X-BAPI-API-KEY": api_key,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-SIGN": signature,
            "X-BAPI-RECV-WINDOW": str(recv_window)
        }

        # Выполните GET запрос
        response = requests.get(url, headers=headers)

        # Проверьте статус код ответа
        return response.json()
    
    def main(self, signal_number, amount_signals): #главный алгоритм
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage" #запрос на ТГ бота. 

        data = db.init_data() #подключаемся к базе
        data = data.get('signals', {}) #получаем данные о токенах

        list_token_database = [] #список токенов для БД

        for value in data['entities']: #получаем список всех ордеров с базы
            token = value['name'] #токен
            list_token_database.append(token) #добавляем в список. 

        while True: #начинаем цикл
            order_num = 0
            for pare in list_token_database: #проходимся по всему списку. 
                sl = None
                qty_tp1 = None
                qty_tp2 = None
                qty_sl = None
                tp = []
                qty_tp = []

                orders = self.get_orders(pare) # делаем запрос на получение ордера
                if orders['retCode'] == 0: # проверяем, если ли этот ордер на бирже. 
                    path = f'data/{pare}.json'
                    if not os.path.exists(path=path): # проверяем, если у нас json файл с сделками. 
                        with open(f'data/{pare}.json', 'w', encoding='utf-8') as file:
                            json.dump(orders, file, indent=4)

                    if len(orders['result']['list']) == 3: #проверяем кол-во ордеров. Если 3, значит есть 2 TP и SL
                        for key, value in orders.items():
                            if key == 'result': 
                                for item in value['list']:
                                    if item['stopOrderType'] == 'PartialTakeProfit':
                                        tp.append(item['triggerPrice']) #добавляем TP в список
                                        qty_tp.append(item['qty']) #добавляем qty

                                    elif item['stopOrderType'] == 'PartialStopLoss':
                                        sl = item['triggerPrice'] # устанавливаем sl в переменную 
                                        qty_sl = item['qty']

                        # определяем тейк-профиты. 1 тейк-профит меньший по цене. 
                        if tp[0] > tp[1]: 
                            tp2 = tp[0]
                            tp1 = tp[1]

                            qty_tp1 = qty_tp[1]
                            qty_tp2 = qty_tp[0]
                        else:
                            tp2 = tp[1]
                            tp1 = tp[0]

                            qty_tp1 = qty_tp[0]
                            qty_tp2 = qty_tp[1]

                        print(f'TP1 - {tp1}\nTP2 - {tp2}\nSL - {sl}')
                    
                    elif len(orders['result']['list']) == 2: #сработает, если tp1 закроется. 
                        
                        #тут напиши код который отошлёт уведомление об отправке кода

                        payload = {
                            "chat_id": self.chat_id, 
                            "text": f'''#{order_num} TP1 is closed
                                    Balance: {self.get_balance('USDT', 'CONTRACT')['result']['balance']['walletBalance']}
                                    Open trades qty: {qty_tp1}
                                    Unfixed P&L: {self.get_pnl(pare)['result']['list'][0]['closedPnL']}'''
                        }

                        headers = {
                            'Content-Type': 'application/json'
                        }

                        requests.get(url, json=payload, headers=headers)

                        with open(f'data/{pare}.json', 'w', encoding='utf-8') as file: #перезаписываем сделку
                            json.dump(orders, file, indent=4)

                        for key, value in orders.items():
                            if key == 'result': 
                                for item in value['list']:
                                    if item['stopOrderType'] == 'PartialTakeProfit':
                                        tp2 = item['triggerPrice']

                                    elif item['stopOrderType'] == 'PartialStopLoss':
                                        sl = item['triggerPrice']

                        print(f'TP2 - {tp2}\nSL - {sl}')

                    elif len(orders['result']['list']) == 0: #сработает, если закроется SL или TP
                        try: #пробуем запустить
                            os.remove(f'data/{pare}.json') #удаляем файл с сделкой
                        
                            last_price = self.get_price(pare)['result']['list'][-1][-1] #узнаём актуальную цену на токен

                            if abs(last_price - sl) < abs(last_price - tp2): #если цена будет ближе к прошлому стопу, отправит сообщение о срабатывании стоп-лосса
                                print('SL') #тут напиши код для отправки кода в тг
                                headers = {
                                    'Content-Type': 'application/json'
                                }

                                payload = {
                                    "chat_id": self.chat_id, 
                                    "text": f'''#{order_num} SL is closed
                                            Balance: {self.get_balance('USDT', 'CONTRACT')['result']['balance']['walletBalance']}
                                            Open trades qty: {qty_sl}
                                            Unfixed P&L: {self.get_pnl(pare)['result']['list'][0]['closedPnL']}'''
                                }

                                requests.get(url)
                            else: #если ближе к тейк-профиту, тогда отправит сообщение о срабатывании тейк-профита. 
                                headers = {
                                    'Content-Type': 'application/json'
                                }

                                payload = {
                                    "chat_id": self.chat_id, 
                                    "text": f'''#{order_num} TP2 is closed
                                            Balance: {self.get_balance('USDT', 'CONTRACT')['result']['balance']['walletBalance']}
                                            Open trades qty: {qty_tp2}
                                            Unfixed P&L: {self.get_pnl(self.pare)['result']['list'][0]['closedPnL']}'''
                                }
                                print('TP') #тут напиши код для отправки кода в тг
                        except:
                            print('Сделка не была создана!') #сработает, если сделка не велась и SL и TP не было при старте бота. 

                else: #сработает, если появится ошибка при запросе.
                    print('no')

                order_num += 1
                time.sleep(3)

if __name__ == "__main__":
    cl = SetPrice(bot_token='', chat_id='')