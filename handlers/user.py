from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram import F
from keyboards.keyboards import create_inline_kb
from keyboards.keyboards import create_menu_kb
from keyboards.keyboards import create_links_kb

from aiogram.types import FSInputFile, InputMediaPhoto
from keyboards.keyboards import LEXICON
from database.language_db import users_lang, users_clicks, adress_clicks
from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from services.services import get_text_with_promocode, get_land_code


user_router = Router()

@user_router.message(CommandStart())
async def process_start_command(message: Message):
    if not message.from_user.id in users_clicks:
        users_clicks[message.from_user.id] = 0
    if not message.from_user.id in users_lang:
        code = message.from_user.language_code
        if not (code in ("ru", "tg","ky", "uz")):
            code = "ru"
        users_lang[message.from_user.id] = code

    code = users_lang[message.from_user.id]


    await message.answer(LEXICON[code]["/start"])
    await message.answer(LEXICON[code]["menu"], reply_markup=create_menu_kb(
        adress_click = LEXICON[code]["buttons"]["adresses"],
        services_click = LEXICON[code]["buttons"]["services"],
        tg_link = LEXICON[code]["buttons"]["tg_channel"],
        lang_click = LEXICON[code]["buttons"]["language"],
        bonus_click = LEXICON[code]["buttons"]["bonus"],
        #help_link = LEXICON[code]["buttons"]["help"]
    ))

@user_router.callback_query(F.data == "back_to_menu")
@user_router.callback_query(F.data == "help_back_click")
@user_router.callback_query(F.data == "bonus_back_click")
@user_router.callback_query(F.data == "adress_back_click")
@user_router.callback_query(F.data == "lang_back_click")
@user_router.callback_query(F.data == "services_back_click")
async def show_menu(callback: CallbackQuery):
    code = get_land_code(callback)

    await callback.message.answer(
        text=LEXICON[code]["menu"],
        reply_markup=create_menu_kb(
        adress_click = LEXICON[code]["buttons"]["adresses"],
        services_click = LEXICON[code]["buttons"]["services"],
        tg_link = LEXICON[code]["buttons"]["tg_channel"],
        lang_click = LEXICON[code]["buttons"]["language"],
        bonus_click = LEXICON[code]["buttons"]["bonus"],
        #help_link = LEXICON[code]["buttons"]["help"]
    ))
    await callback.answer()

# поменять язык тут тоже
@user_router.callback_query(F.data == "uz_lang_click")
@user_router.callback_query(F.data == "ky_lang_click")
@user_router.callback_query(F.data == "tg_lang_click")
@user_router.callback_query(F.data == "ru_lang_click")
async def change_lang(callback: CallbackQuery):

    users_lang[callback.from_user.id] = callback.data[:2]

    code = get_land_code(callback)
    await callback.answer(LEXICON[code]["change_lang_alert"], show_alert=True)
    await callback.message.answer(
        text=LEXICON[code]["menu"],
        reply_markup=create_menu_kb(
        adress_click = LEXICON[code]["buttons"]["adresses"],
        services_click = LEXICON[code]["buttons"]["services"],
        tg_link = LEXICON[code]["buttons"]["tg_channel"],
        lang_click = LEXICON[code]["buttons"]["language"],
        bonus_click = LEXICON[code]["buttons"]["bonus"],
        #help_link = LEXICON[code]["buttons"]["help"]
    ))

@user_router.callback_query(F.data == "back_to_services")
@user_router.callback_query(F.data == "back_jobs_click")
@user_router.callback_query(F.data == "any_service_back_click")
@user_router.callback_query(F.data == "services_click")
async def show_services(callback: CallbackQuery):
    code = get_land_code(callback)

    await callback.message.answer(
        text=LEXICON[code]["services"],
        reply_markup=create_inline_kb(
            biometrics_click = LEXICON[code]["buttons"]["biometrics"],
            bank_card_click = LEXICON[code]["buttons"]["bank_card"],
            sim_card_click = LEXICON[code]["buttons"]["sim_card"],
            credit_card_click = LEXICON[code]["buttons"]["credit_card"],
            jobs_click = LEXICON[code]["buttons"]["jobs"],
            services_back_click = LEXICON[code]["buttons"]["back"]
        )
    )
    await callback.answer()

@user_router.callback_query(F.data == "adress_click")
@user_router.callback_query(F.data == "back_to_adress")
@user_router.callback_query(F.data == "gorchakovo_adress_back_click")
async def show_adress(callback: CallbackQuery):
    code = get_land_code(callback)
    users_clicks[callback.from_user.id] += 1

    await callback.message.answer(
        text=LEXICON[code]["adress"],
        reply_markup=create_inline_kb(
            tushino_adress_click = LEXICON[code]["buttons"]["tushino"],
            gorchakovo_adress_click = LEXICON[code]["buttons"]["gorchakovo"],
            adress_back_click = LEXICON[code]["buttons"]["back"]
        )
    )
    await callback.answer()

@user_router.callback_query(F.data == "bonus_click")
async def show_bonus(callback: CallbackQuery):
    code = get_land_code(callback)

    await callback.message.answer(
        text=LEXICON[code]["bonus"],
        reply_markup=create_links_kb(
            url_buttons={
                LEXICON[code]["buttons"]["subscribe"]: "t.me/Easy_Biometry"
            },
            callback_buttons={
                LEXICON[code]["buttons"]["check_subscribe"]: "check_sub_click",
                LEXICON[code]["buttons"]["back"]: "bonus_back_click"
            }
        )
    )
    await callback.answer()

@user_router.callback_query(F.data == "help_click")
async def show_help(callback: CallbackQuery):
    code = get_land_code(callback)

    await callback.message.answer(
        text=LEXICON[code]["help"],
        reply_markup=create_inline_kb(
            help_back_click = LEXICON[code]["buttons"]["back"]
        )
    )
    await callback.answer()

@user_router.callback_query(F.data == "service_id")
async def show_any_service(callback: CallbackQuery):
    code = get_land_code(callback)

    await callback.message.answer(
        text=LEXICON[code]["any_services"],
        reply_markup=create_inline_kb(
            any_service_back_click = LEXICON[code]["buttons"]["back"]
        )
    )
    await callback.answer()

@user_router.callback_query(F.data == "gorchakovo_adress_click")
async def show_gorchakovo_adress(callback: CallbackQuery):
    adress_clicks[0] += 1
    code = get_land_code(callback)
    await callback.message.answer("Загружаем маршрут...")
    await callback.answer()
    photo1 = FSInputFile("images/gorchakovo_route_1.png")
    photo2 = FSInputFile("images/gorchakovo_route_2.png")
    media = [
        InputMediaPhoto(media=photo1, caption=LEXICON[code]["where_gorchakovo"]),
        InputMediaPhoto(media=photo2)
    ]
    # Отправляем новое сообщение с фото
    await callback.message.answer_media_group(
        media=media
        )
    await callback.message.answer(
        text=LEXICON[code]["see_on_map"],
        reply_markup=create_links_kb(
            url_buttons={
                LEXICON[code]["buttons"]["maps_yandex"]: "https://yandex.ru/maps/-/CLGDjWNk",
                LEXICON[code]["buttons"]["maps_google"]: "https://maps.app.goo.gl/SFyuQS4729uSbgMS7?g_st=atm"
            },
            callback_buttons={
                LEXICON[code]["buttons"]["back"]: "gorchakovo_adress_back_click"
            }
        ))

# тушино
@user_router.callback_query(F.data == "tushino_adress_click")
async def show_gorchakovo_adress(callback: CallbackQuery):
    code = get_land_code(callback)
    adress_clicks[1] += 1

    await callback.message.answer("Загружаем маршрут...")
    await callback.answer()
    photo1 = FSInputFile("images/tushino_1.jpg")
    photo2 = FSInputFile("images/tushino_2.jpg")
    photo3 = FSInputFile("images/tushino_3.jpg")
    media = [
        InputMediaPhoto(media=photo1, caption=LEXICON[code]["where_tushino"]),
        InputMediaPhoto(media=photo2),
        InputMediaPhoto(media=photo3)
    ]
    # Отправляем новое сообщение с фото
    await callback.message.answer_media_group(
        media=media
        )
    await callback.message.answer(
        text=LEXICON[code]["see_on_map_tushino"],
        reply_markup=create_links_kb(
            url_buttons={
                LEXICON[code]["buttons"]["maps_yandex"]: "https://yandex.ru/maps?whatshere%5Bpoint%5D=37.402657%2C55.837849&whatshere%5Bzoom%5D=19.664007&ll=37.402705280866456%2C55.837959740446095&z=19.664007&si=rp3nebh226x6fef0jq72pbg7zw",
                LEXICON[code]["buttons"]["maps_google"]: "https://www.google.ru/maps/place/Тот+самый+Хмель/@55.8378666,37.4019809,19.05z/data=!4m6!3m5!1s0x46b5471126008ba3:0xa9c41a851d0f8822!8m2!3d55.8379238!4d37.40259!16s%2Fg%2F11r91v4wyq!5m1!1e1?entry=ttu&g_ep=EgoyMDI1MTExNy4wIKXMDSoASAFQAw%3D%3D"
            },
            callback_buttons={
                LEXICON[code]["buttons"]["back"]: "back_to_adress"
            }
        ))

@user_router.callback_query(F.data == "jobs_click")
async def show_jobs(callback: CallbackQuery):
    code = get_land_code(callback)

    await callback.message.answer(
        text=LEXICON[code]["jobs"],
        reply_markup=create_links_kb(
            url_buttons={
                LEXICON[code]["buttons"]["yandex_food"]: "https://reg.eda.yandex.ru/?advertisement_campaign=forms_for_agents&user_invite_code=861e6529474e4e819941d2d261aba049&utm_content=blank",
                LEXICON[code]["buttons"]["lenta"]: "https://trk.xplink.io/click?pid=10426&offer_id=2587",
                LEXICON[code]["buttons"]["sber_market"]: "https://trk.xplink.io/click?pid=10426&offer_id=2052"
            },
            callback_buttons={
                LEXICON[code]["buttons"]["back"]: "back_jobs_click"
            }
        )
    )
    await callback.answer()

@user_router.callback_query(F.data == "lang_click")
async def show_lang(callback: CallbackQuery):
    code = get_land_code(callback)

    await callback.message.answer(
        text=LEXICON[code]["language"],
        reply_markup=create_inline_kb(
            ru_lang_click = "Русский",
            tg_lang_click = "Тоҷикӣ",
            ky_lang_click = "Кыргыз",
            uz_lang_click = "O'zbek",
            lang_back_click = LEXICON[code]["buttons"]["back"]
        )
    )
    await callback.answer()

# Новые хендлеры

@user_router.callback_query(F.data == "biometrics_click")
async def show_biometrics(callback: CallbackQuery):
    code = get_land_code(callback)

    await callback.message.answer(
        text=LEXICON[code]["biometrics"],
        reply_markup=create_inline_kb(
            adress_click = LEXICON[code]["buttons"]["adresses"],
            back_to_services = LEXICON[code]["buttons"]["back"]
        )
    )
    await callback.answer()

@user_router.callback_query(F.data == "bank_card_click")
async def show_bank_card(callback: CallbackQuery):
    code = get_land_code(callback)

    await callback.message.answer(
        text=LEXICON[code]["bank_card"],
        reply_markup=create_inline_kb(
            adress_click = LEXICON[code]["buttons"]["adresses"],
            back_to_services = LEXICON[code]["buttons"]["back"]
        )
    )
    await callback.answer()

@user_router.callback_query(F.data == "sim_card_click")
async def show_sim_card(callback: CallbackQuery):
    code = get_land_code(callback)

    await callback.message.answer(
        text=LEXICON[code]["sim_card"],
        reply_markup=create_inline_kb(
            adress_click = LEXICON[code]["buttons"]["adresses"],
            back_to_services = LEXICON[code]["buttons"]["back"]
        )
    )
    await callback.answer()

@user_router.callback_query(F.data == "credit_card_click")
async def show_credit_card(callback: CallbackQuery):
    code = get_land_code(callback)

    await callback.message.answer(
        text=LEXICON[code]["credit_card"],
        reply_markup=create_links_kb(
            url_buttons={
                LEXICON[code]["buttons"]["credit_europe"]: "https://trk.xpgoal.io/click?pid=10426&offer_id=1503",
                LEXICON[code]["buttons"]["credit_tbank"]: "https://trk.xplink.io/click?pid=10426&offer_id=2513",
                LEXICON[code]["buttons"]["credit_zenit"]: "https://trk.xpgoal.io/click?pid=10426&offer_id=1061",
                LEXICON[code]["buttons"]["credit_ural_sib"]: "https://trk.xplink.io/click?pid=10426&offer_id=1841",
                LEXICON[code]["buttons"]["credit_baibol"]: "https://trk.xplink.io/click?pid=10426&offer_id=2737"
            },
            callback_buttons={
                LEXICON[code]["buttons"]["adresses"]: "adress_click",
                LEXICON[code]["buttons"]["back"]: "back_to_services"
            }
        )
    )
    await callback.answer()

@user_router.callback_query(F.data == "check_sub_click")
async def check_sub(callback: CallbackQuery, bot: Bot):
    code = get_land_code(callback)
    try:
        member = await bot.get_chat_member(chat_id="@Easy_Biometry", user_id=callback.from_user.id)
        is_sub = member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR
        ]
    except Exception:
        is_sub = False

    if is_sub:
        await callback.message.answer(
            text=get_text_with_promocode(code),
            reply_markup=create_inline_kb(
                back_to_menu = LEXICON[code]["buttons"]["back"]
            ))
    else:
        await callback.message.answer(
        text=LEXICON[code]["dont_subscribe"],
        reply_markup=create_links_kb(
            url_buttons={
                LEXICON[code]["buttons"]["subscribe"]: "t.me/Easy_Biometry"
            },
            callback_buttons={
                LEXICON[code]["buttons"]["check_subscribe"]: "check_sub_click",
                LEXICON[code]["buttons"]["back"]: "bonus_back_click"
            }
        )
    )
    await callback.answer()
