from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# 🔑 Встав свій токен сюди
TOKEN = "тут_твій_токен"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🎨 Кольори і стиль для повідомлень
GOLD_EMOJI = "✨"
BOLD = lambda text: f"<b>{text}</b>"
ITALIC = lambda text: f"<i>{text}</i>"

# 🏁 Команда /start
@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    text = (
        f"{GOLD_EMOJI} {BOLD('Вітаю!')} \n\n"
        "Радий бачити тебе тут.\n"
        "Це офіційний бот проекту з витриманим темним стилем і нотками золота 💫\n\n"
        f"{ITALIC('Оберіть дію нижче:')}"
    )

    # 🔘 Кнопки з посиланнями
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🌐 Перейти на сайт", url="https://твій_сайт.com"),
        InlineKeyboardButton("💎 Акції", url="https://твій_сайт.com/promo"),
        InlineKeyboardButton("📬 Підписатися на оновлення", callback_data="subscribe")
    )

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


# 📩 Обробка натискання "Підписатися"
@dp.callback_query_handler(lambda c: c.data == "subscribe")
async def subscribe_callback(callback_query: types.CallbackQuery):
    await callback_query.answer("Дякуємо! Ти підписаний на оновлення 💛", show_alert=True)


# ▶️ Запуск
if __name__ == "__main__":
    print("Бот запущений 🚀")
    executor.start_polling(dp, skip_updates=True)