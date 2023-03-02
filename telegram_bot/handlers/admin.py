from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram import types,Dispatcher
from create_bot import dp,bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

#@dp.message_handler(commands=['moderator'],is_chat_admin=True)
async def make_changes_comand(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id,"What do you need, master?",reply_markup=admin_kb.button_case_admin)
    await message.delete()

# the beginning of the dialog and the loading of the menu item
#@dp.message_handler(commands='Load',state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Upload a photo')

# I catch the first answer and write it in the dictionary
#@dp.message_handler(content_types=['photo'],state=FSMAdmin.photo)
async def load_photo(message: types.Message,state:FSMContext):
    async with state.proxy() as data:
        if message.from_user.id == ID:
            data['photo'] = message.photo[0].file_id
            await FSMAdmin.next()
            await message.reply("Now write the name")

# we catch second answer
#@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message,state:FSMContext):
    async with state.proxy() as data:
        if message.from_user.id == ID:
            data['name'] = message.text
            await FSMAdmin.next()
            await message.reply("Write a description")

# we catch the third
#@dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message,state:FSMContext):
    async with state.proxy() as data:
        if message.from_user.id == ID:
            data['description'] = message.text
            await FSMAdmin.next()
            await message.reply("Write the price")

# we catch the last
#@dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message,state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)


        await sqlite_db.sql_add_command(state)
        await state.finish()  # will delete all

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} deleted.', show_alert=True)

@dp.message_handler(commands='Delete')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nDescription: {ret[2]}\nPrice: {ret[-1]}')
            await bot.send_message(message.from_user.id,text='^',reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Delete {ret[1]}',callback_data=f'del {ret[1]}')))


# the exit from the state
#@dp.message_handler(state='*',commands='cancellation')
#@dp.message_handler(Text(equals='cancellation',ignore_case = True),state='*')
async def cancel_handler(message:types.Message,state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')



def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start,commands=['Load'],state=None)
    dp.register_message_handler(load_photo,content_types=['photo'],state=FSMAdmin.photo)
    dp.register_message_handler(load_name,state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state='*',commands='cancellation')
    dp.register_message_handler(cancel_handler, Text(equals = 'cancellation',ignore_case = 'True'),state = '*')
    dp.register_message_handler(make_changes_comand,commands=['moderator'],is_chat_admin = True)
    #dp.register_message_handler(delete_item, commands='Delete', is_chat_admin=True)
    #dp.register_callback_query_handler(del_callback_run,commands="del ",is_chat_admin=True)
