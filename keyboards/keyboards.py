from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon import LEXICON

# ///////////////////////////////////////////////////////////////////////////

# Генерируем вертикальную клавиатуру
def create_inline_kb(**kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    # Запоняем
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()

# Генерируем главное меню

def create_menu_kb(**kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    # Запоняем
    if kwargs:
        for button, text in kwargs.items():
            if (button == "tg_link"):
                buttons.append(InlineKeyboardButton(text=text, url="t.me/Easy_Biometry"))
            elif (button == "help_link"):
                buttons.append(InlineKeyboardButton(text=text, url="https://t.me/Danya_Efrem?text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5.%20%D0%A3%20%D0%BC%D0%B5%D0%BD%D1%8F%20%D0%B2%D0%BE%D0%BF%D1%80%D0%BE%D1%81%20%D0%BF%D0%BE%20%D0%BE%D1%84%D0%BE%D1%80%D0%BC%D0%BB%D0%B5%D0%BD%D0%B8%D1%8E%20%D1%83%D1%81%D0%BB%D1%83%D0%B3%D0%B8"))
            else:
                buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    kb_builder.add(*buttons)
    kb_builder.adjust(1, 2, 2, 1)
    return kb_builder.as_markup()

# Создаёт вертикальную клавиатуру с ссылками и кнопкой назад

def create_links_kb(url_buttons: dict = None, callback_buttons: dict = None) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if url_buttons:
        for text, url in url_buttons.items():
            buttons.append(InlineKeyboardButton(text=text, url=url))

    if callback_buttons:
        for text, callback_data in callback_buttons.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=callback_data))

    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()