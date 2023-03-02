from aiogram import types,Dispatcher
from create_bot import dp,bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db


#@dp.message_handler(commands=['start','help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,"Bon appetit!",reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply("Communicating with the bot via PM, write to him: \nt.me/PizzaTest_12342334_bot")


#@dp.message_handler(commands=['Work_schedule'])
async def pizza_open_command(message: types.Message):
        await bot.send_message(message.from_user.id,"Monday-Saturday from 9:00 am to 22:00 pm , Sunday from 10:00 am to 18:00 pm")

#@dp.message_handler(commands=['Location'])
async def pizza_place_command(message: types.Message):
        await bot.send_message(message.from_user.id,"st. Example 15") #reply_markup=ReplyKeyboardRemove())

#@dp.message_handler(commands=['Menu'])
async def pizza_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)



def register_handlers_client(dp : Dispatcher ):
    dp.register_message_handler(command_start,commands=['start','help'])
    dp.register_message_handler(pizza_open_command,commands=['Work_schedule'])
    dp.register_message_handler(pizza_place_command,commands=['Location'])
    dp.register_message_handler(pizza_menu_command, commands=['Menu'])
