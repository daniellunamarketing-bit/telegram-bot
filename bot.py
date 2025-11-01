import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiohttp import web  # веб-сервер для Render

# 🔑 Токен бере з Environment Variables
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не заданий в Environment Variables!")

# 🧠 Ініціалізація
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

# 🎨 Кольори і стиль
GOLD_EMOJI = "✨"
BOLD = lambda text: f"<b>{text}</b>"
ITALIC = lambda text: f"<i>{text}</i>"

# 🏁 /start команда
@dp.message(Command("start"))
async def start_message(message: types.Message):
    text = (
        f"{GOLD_EMOJI} {BOLD('Вітаю!')} \n\n"
        "Радий бачити тебе тут.\n"
        "Це офіційний бот проекту з витриманим темним стилем і нотками золота 💫\n\n"
        f"{ITALIC('Оберіть дію нижче:')}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Перейти на сайт", url="https://твій_сайт.com")],
        [InlineKeyboardButton(text="💎 Акції", url="https://твій_сайт.com/promo")],
        [InlineKeyboardButton(text="📬 Підписатися на оновлення", callback_data="subscribe")]
    ])

    await message.answer(text, reply_markup=keyboard)

# 📩 Обробка натискання "Підписатися"
@dp.callback_query(F.data == "subscribe")
async def subscribe_callback(callback: types.CallbackQuery):
    await callback.answer("Дякуємо! Ти підписаний на оновлення 💛", show_alert=True)

# === Webhook частина ===
async def on_startup(app):
    webhook_url = f"{os.getenv('RENDER_EXTERNAL_URL')}/webhook/{TOKEN}"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook встановлено: {webhook_url}")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

async def handle_webhook(request):
    update = types.Update.model_validate(await request.json(), strict=False)
    await dp.feed_update(bot, update)
    return web.Response(status=200)

def main():
    app = web.Application()
    app.router.add_post(f"/webhook/{TOKEN}", handle_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    port = int(os.getenv("PORT", 5000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
