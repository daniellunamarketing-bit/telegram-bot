from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

# 🔑 Встав свій токен сюди
TOKEN = "fuck_you"

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

# 🎨 Кольори і стиль для повідомлень
GOLD_EMOJI = "✨"
BOLD = lambda text: f"<b>{text}</b>"
ITALIC = lambda text: f"<i>{text}</i>"

# 🏁 Команда /start
@dp.message(Command(commands=["start"]))
async def start_message(message: types.Message):
    text = (
        f"{GOLD_EMOJI} {BOLD('Вітаю!')} \n\n"
        "Радий бачити тебе тут.\n"
        "Це офіційний бот проекту з витриманим темним стилем і нотками золота 💫\n\n"
        f"{ITALIC('Оберіть дію нижче:')}"
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🌐 Перейти на сайт", url="https://твій_сайт.com"),
        InlineKeyboardButton(text="💎 Акції", url="https://твій_сайт.com/promo")
    )
    keyboard.add(InlineKeyboardButton(text="📬 Підписатися на оновлення", callback_data="subscribe"))

    await message.answer(text, reply_markup=keyboard.as_markup())

# 📩 Обробка натискання "Підписатися"
@dp.callback_query(lambda c: c.data == "subscribe")
async def subscribe_callback(callback_query: types.CallbackQuery):
    await callback_query.answer("Дякуємо! Ти підписаний на оновлення 💛", show_alert=True)

# ▶️ Запуск
async def main():
    print("Бот запущений 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
