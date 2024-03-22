from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message,ChatPermissions,FSInputFile,URLInputFile,InputContactMessageContent,InlineQuery,InlineQueryResultArticle,InputTextMessageContent,InputLocationMessageContent
from data import config
import asyncio
import logging
import sys
from menucommands.set_bot_commands  import set_default_commands
from baza.sqlite import Database
from filterss.admin import IsBotAdminFilter
from filterss.check_sub_channel import IsCheckSubChannels
from keyboard_buttons import admin_keyboard
from aiogram.fsm.context import FSMContext
from middlewares.throttling import ThrottlingMiddleware #new
from states.reklama import Adverts
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import time 

ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN
CHANNELS = config.CHANNELS

dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message:Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        db.add_user(full_name=full_name,telegram_id=telegram_id)
        await message.answer(text="Assalomu alaykum bu bot inline bot")
    except:
        await message.answer(text="Assalomu alaykum bu bot inlini bot")



@dp.message(IsCheckSubChannels())
async def kanalga_obuna(message:Message):
    text = ""
    inline_channel = InlineKeyboardBuilder()
    for index,channel in enumerate(CHANNELS):
        ChatInviteLink = await bot.create_chat_invite_link(channel)
        inline_channel.add(InlineKeyboardButton(text=f"{index+1}-kanal",url=ChatInviteLink.invite_link))
    inline_channel.adjust(1,repeat=True)
    button = inline_channel.as_markup()
    await message.answer(f"{text} kanallarga azo bo'ling",reply_markup=button)





#Admin panel uchun
@dp.message(Command("admin"),IsBotAdminFilter(ADMINS))
async def is_admin(message:Message):
    await message.answer(text="Admin menu",reply_markup=admin_keyboard.admin_button)


@dp.message(F.text=="Foydalanuvchilar soni",IsBotAdminFilter(ADMINS))
async def users_count(message:Message):
    counts = db.count_users()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)

@dp.message(F.text=="Reklama yuborish",IsBotAdminFilter(ADMINS))
async def advert_dp(message:Message,state:FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin !")




@dp.message(F.text=="/help")
async def yordam(message:Message):
    # await state.set_state(Adverts.adverts)
    await message.answer(text="Bu bot nima qilishini uzim ham bilmiman hozirch kiyin bir ikkita funksiya qushib urgaaman")

@dp.message(Adverts.adverts)
async def send_advert(message:Message,state:FSMContext):
    
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = await db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0],from_chat_id=from_chat_id,message_id=message_id)
            count += 1
        except:
            pass
        time.sleep(0.5)
     
    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")
    await state.clear()


@dp.inline_query()
async def inlini_surov(inlin_query:InlineQuery):
    result = [
        InlineQueryResultArticle(
            id="1",
            title = "ISIFAT",
            input_message_content=InputTextMessageContent(message_text="ISIFAT"),
            description="Sifat uquv markazi Navoidagi birinchi bulib uzing tekin python kursi bn ajralib turgan va unda malakali uqituvchilar dars beradi\nttps://i.ibb.co/p3gBWM1/photo-2024-03-06-15-05-42.jpg",
            thumbnail_url="https://i.ibb.co/p3gBWM1/photo-2024-03-06-15-05-42.jpg"
            ),

            InlineQueryResultArticle(
            id="2",
            title = "SENSORIKA",
            input_message_content=InputTextMessageContent(message_text="Sensorika ham yaxshi uquv markaz\nhttps://i.ibb.co/GpB0tx2/sensorika.jpg"),
            description="Sensorika ham yaxshi uquv markaz",
            thumbnail_url="https://i.ibb.co/GpB0tx2/sensorika.jpg"
            ),

            InlineQueryResultArticle(
            id="3",
            title = "IT PARK",
            input_message_content=InputTextMessageContent(message_text="IT park ham yaxshi uquv markaz edi yaqinda qayta boshdan ochildi\nhttps://i.ibb.co/kShZv5K/it-parki.jpg"),
            description="IT park ham yaxshi uquv markaz edi yaqinda qayta boshdan ochildi",
            thumbnail_url="https://i.ibb.co/kShZv5K/it-parki.jpg"
            ),
            InlineQueryResultArticle(
            id="4",
            title = "Gorni Institut",
            input_message_content=InputTextMessageContent(message_text="Gorni instetut navoidagi yirik va talabalari soni buyicha yuqori urinda turadi\nhttps://i.ibb.co/PZk8fxc/Screenshot-2024-03-13-164011.png"),
            description="Gorni instetut navoidagi yirik va talabalari soni buyicha yuqori urinda turadi",
            thumbnail_url="https://i.ibb.co/PZk8fxc/Screenshot-2024-03-13-164011.png"
            ),
            InlineQueryResultArticle(
            id="5",
            title = "Tompson",
            input_message_content=InputTextMessageContent(message_text="Tompson uquv markazi yirik markaz\nhttps://i.ibb.co/ScYsWHf/Screenshot-2024-03-13-164345.png"),
            description="Tompson invirsty  xususiy talim maskani",
            thumbnail_url="https://i.ibb.co/ScYsWHf/Screenshot-2024-03-13-164345.png"
            ),
            InlineQueryResultArticle(
            id="6",
            title = "IT ILTS SCHOLL",
            input_message_content=InputTextMessageContent(message_text="IT ILTS SCHOLL\nbu yerda ham IT ham ILTS buyicha uqishingiz mumkin\nhttps://i.ibb.co/g6jkdb4/Screenshot-2024-03-13-164954.png"),
            description="bu yerda ham IT ham ILTS buyicha uqishingiz mumkin",
            thumbnail_url="https://i.ibb.co/g6jkdb4/Screenshot-2024-03-13-164954.png"
            ),

            # InlineQueryResultArticle(
            # id="7",
            # title = "ILTS GENESES ",
            # input_message_content=InputTextMessageContent(message_text="ILTS GENESES ingliz tilini biz bilan urganing"),
            # description="ILTS GENESES ingliz tilini biz bilan urganing",
            # thumbnail_url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fieltsmaterial.com%2Fielts-full-form%2F&psig=AOvVaw2VyaORWyvSFu67lv7ey6aT&ust=1711180087255000&source=images"
            # ),


            # InlineQueryResultArticle(
            # id="8",
            # title = "sanat kolliji",
            # input_message_content=InputTextMessageContent(message_text="Sanat kolliji yoshlarni sanatga tayorlashda va yaxshi sanatkor bo'lib yetishib chiqishi yulida kurashadi"),
            # description="Sanat kolliji yoshlarni sanatga tayorlashda va yaxshi sanatkor bo'lib yetishib chiqishi yulida kurashadi",
            # thumbnail_url="rasm quyishim kerak"
            # ),


     ]
    await inlin_query.answer(results=result)






@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)

#bot ishga tushganini xabarini yuborish
@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishdan to'xtadi!")
        except Exception as err:
            logging.exception(err)




async def main() -> None:
    global bot,db
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    db = Database(path_to_db="main.db")
    db.create_table_users()
    await set_default_commands(bot)
    dp.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))
    await dp.start_polling(bot)
    




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
