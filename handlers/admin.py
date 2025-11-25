from aiogram.types import Message
from aiogram import F, Router
from aiogram.filters import BaseFilter, Command
from keyboards.keyboards import LEXICON
from database.language_db import users_clicks, adress_clicks

admin_router = Router()

admins = [1121984521, 541620409]

# Собственный фильтр, проверяющий юзера на админа
class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        # В качестве параметра фильтр принимает список с целыми числами
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


@admin_router.message(IsAdmin(admins), Command(commands="admin"))
async def process_start_command(message: Message):
    office_clicks = 0
    for val in users_clicks.values():
        office_clicks += val
    await message.answer(f"Число кликов на Старт: {len(users_clicks)}\nЧисло кликов на офисы: {office_clicks}\nГорчаково: {adress_clicks[0]}\nТушино: {adress_clicks[1]}")
