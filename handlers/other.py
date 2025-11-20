from aiogram import F, Router
from aiogram.types import Message
from keyboards.keyboards import LEXICON
from keyboards.keyboards import create_inline_kb
from services.services import get_land_code

other_router = Router()

@other_router.message()
async def process_start_command(message: Message):
    code = get_land_code(message)
    await message.answer(
        text=LEXICON[code]["invalid_command"],
        reply_markup=create_inline_kb(
            back_to_menu = LEXICON[code]["buttons"]["back"]
        )
        )