import asyncio
import telebot
import subprocess
from telebot.async_telebot import AsyncTeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN
from db1 import DataBase

db = DataBase('test.db')

bot = AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['start'])
async def start(message: telebot.types.Message):
    if not db.true_user_id(message.from_user.id):
        db.register_users_id(message.from_user.id)
    await bot.send_message(message.from_user.id, 'Привет! Я MV AI. Пишу тексты песен по запросам и музыкальное сопровождение. Чтобы начать,\nвыберите режим.')

@bot.message_handler(commands=["help"])
async def start_help(message: telebot.types.Message):
    main_buttons = InlineKeyboardMarkup()
    how_generate_music = InlineKeyboardButton('1 вопрос', callback_data='var1')
    how_generate_music1 = InlineKeyboardButton('2 вопрос', callback_data='var2')
    how_generate_music2 = InlineKeyboardButton('3 вопрос', callback_data='var3')
    how_generate_music3 = InlineKeyboardButton('4 вопрос', callback_data='var4')
    main_buttons.add(how_generate_music, how_generate_music1, how_generate_music2, how_generate_music3)
    await bot.send_message(message.from_user.id, "Частые вопросы:\nКак сгенерировать песню?\nКак сгенерировать голос?\nГолос будет правдоподобным?\nМожно будет добавить свой голос?", reply_markup=main_buttons)

@bot.message_handler(commands=["setting"])
async def start_setting(message: telebot.types.Message):
    markup = InlineKeyboardMarkup()
    btn_main = InlineKeyboardButton("Язык", callback_data='lenguage')
    btn_main1 = InlineKeyboardButton("Пополнение баланса", callback_data='popolnenie') 

    markup.add(btn_main, btn_main1)
    await bot.send_message(message.from_user.id, 'Выберите функцию', reply_markup=markup)
    
'''@bot.message_handler()
async def start_mess(message: telebot.types.Message):
    if db.isDownload(message.from_user.id) == True:
        await bot.send_message(message.from_user.id, "Ваш вопрос очень важен для нас и мы пытаемся обработать его как можно скорее.") 
    elif db.isDownload == False:
        await bot.send_message(message.from_user.id, "У вас не хватка средств на балансе. Пополните счет и повторите попытку!") '''

@bot.message_handler()
async def start_mess(message: telebot.types.Message):
    if db.check_balance(db.get_balance(message.from_user.id), len(message.text), message.from_user.id):  
        db.or_balance(message.from_user.id, len(message.text), '-')
        print('test1') 
        '''args_list = [
                        'python3',
                        'api.py',
                        str(message.text),
                        f'MALE',
                        str(message.from_user.id), 
                        str(message.from_user.id), 
                    ]
        subprocess.Popen(args_list)'''
    else: 
        markup = InlineKeyboardMarkup()
        btn_main1= InlineKeyboardButton("Пополнение баланса", callback_data='popolnenie')
        markup.add(btn_main1)
        await bot.send_message(message.from_user.id, "У вас не хватка средств на балансе. Пополните счет и повторите попытку!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
async def start_callback(call):
    if call.data == 'var1':
        await bot.send_message(call.from_user.id, 'Вам нужно просто написать о чем будет песня, ключевые слова и любые другие характеристики.')
    if call.data == 'var2':
        print('hello')
        await bot.send_message(call.from_user.id, 'Выберите режим голоса, после чего отправьте нам текст песни.')
    if call.data == 'var3':
        print('hello')
        await bot.send_message(call.from_user.id, 'Результат может зависеть от качества источника звука и настройки параметров голоса. Я стараюсь создать натуральный звучащщий голос,который будет соответствовать вашим ожиданиям.')
    if call.data == 'var4':
        print('hello')
        await bot.send_message(call.from_user.id, 'Эта функция пока находится на разбработке.')

    if call.data == 'popolnenie':
        db.or_balance(call.from_user.id, 1000, '+')
        await bot.send_message(call.from_user.id,  f'Вы пополнили свой баланс на 1000 токенов. Ваш баланс: {db.get_balance(call.from_user.id)}')

    if call.data == 'lenguage':
        markup = InlineKeyboardMarkup()
        rus_btn = InlineKeyboardButton('RU 🇷🇺', callback_data='rus')
        eng_btn = InlineKeyboardButton('ENG 🇬🇧', callback_data='eng')
        fr_btn = InlineKeyboardButton('FR 🇫🇷', callback_data='fr')
        de_btn = InlineKeyboardButton('DE 🇩🇪', callback_data='de')

        markup.add(rus_btn, eng_btn, fr_btn, de_btn)
        await bot.send_message(call.from_user.id, 'Выберите язык:', reply_markup=markup)

    if call.data == 'rus':
        await bot.send_message(call.from_user.id, 'Вы изменили язык на русский', reply_markup=markup) 
        #написать запрос на изменение русского языка
        db.set_language('rus', call.from_user.id)

    if call.data == 'eng':
        await bot.send_message(call.from_user.id, 'Вы изменили язык на английский', reply_markup=markup)
        db.set_language('eng', call.from_user.id)
        
    if call.data == 'fr':
        await bot.send_message(call.from_user.id, 'Вы изменили язык на французский', reply_markup=markup)
        db.set_language('fr', call.from_user.id)

    if call.data == 'de':
        await bot.send_message(call.from_user.id, 'Вы изменили язык на немецкий', reply_markup=markup)
        db.set_language('de', call.from_user.id)

async def main():
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())