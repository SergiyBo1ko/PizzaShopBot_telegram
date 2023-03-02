from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove


b1 = KeyboardButton('/Work_schedule')
b2 = KeyboardButton('/Location')
b3 = KeyboardButton('/Menu')
#b4 = KeyboardButton('Send my number',request_contact=True)
#b5 = KeyboardButton('Send my location',request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1).add(b2).add(b3)#.row(b4,b5)

