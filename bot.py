import asyncio
import telebot
from telebot.async_telebot import AsyncTeleBot
from db1 import DataBase

db = DataBase('test.db')

bot = AsyncTeleBot('6906669457:AAFBFgK4PUKJEu_M8tGNVBgxu_U0uskx4Zw')
import asyncio
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN
from api import audio_ai
from db1 import DataBase

bot = AsyncTeleBot(TOKEN)
db = DataBase()

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

@bot.message_handler()
async def start_mess(message: telebot.types.Message):
    if db.check_balance(db.get_balance(), len(message.text), message.from_user.id):             
        print('SUCCES BALANCE')
    await audio_ai(text=message.text, option='MALE', music_name=message.from_user.id, user_id=message.from_user.id)
    if db.isDownload == True:
        await bot.send_message(message.from_user.id, "Ваш вопрос очень важен для нас и мы пытаемся обработать его как можно скорее.") 
    elif db.isDownload == False:
        await bot.send_message(message.from_user.id, "У вас не хватка средств на балансе. Пополните счет и повторите попытку!") 

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

async def main():
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())
