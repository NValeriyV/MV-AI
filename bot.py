import asyncio
import telebot
from telebot.async_telebot import AsyncTeleBot
from db1 import DataBase

db = DataBase('test.db')

bot = AsyncTeleBot('6906669457:AAFBFgK4PUKJEu_M8tGNVBgxu_U0uskx4Zw')

@bot.message_handler(commands=['start'])
async def start(message: telebot.types.Message):
    if not db.true_user_id(message.from_user.id):
        db.register_users_id(message.from_user.id)
    await bot.send_message(message.from_user.id, 'Привет! Я MV AI. Пишу тексты песен по запросам и музыкальное сопровождение. Чтобы начать,\nвыберите режим.')

@bot.message_handler(commands=["help"])
async def start_help(message: telebot.types.Message):
    await bot.send_message(message.from_user.id, "Частные вопросы:\nкак сгенерировать песню?")

async def main():
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())