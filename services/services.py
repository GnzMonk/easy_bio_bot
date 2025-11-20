from random import randint
from lexicon.lexicon import LEXICON
from database.language_db import users_lang
from aiogram.types import Message, CallbackQuery

def generate_promocode():
    length = 6
    postfix = "200"
    alphabet = [chr(i) for i in range(65, 91)]
    result = ""
    for _ in range(length):
        result += alphabet[randint(0,len(alphabet))-1]
    return result + postfix

def get_text_with_promocode(lang):
    text = LEXICON[lang]["bonus_code"]
    return text.replace("ABCDEF200", "<tg-spoiler>"+generate_promocode()+"</tg-spoiler>")

def get_land_code(callback: CallbackQuery | Message):
    return users_lang[callback.from_user.id]