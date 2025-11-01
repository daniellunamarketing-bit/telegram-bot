import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from aiogram.filters import Command
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не заданий в Environment Variables!")

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

GOLD_EMOJI = "✨"
BOLD = lambda t: f"<b>{t}</b>"
ITALIC = lambda t: f"<i>{t}</i>"

# ------------------- Команди -------------------

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    text = (
        f"{GOLD_EMOJI} {BOLD('Вітаю у VIP Advisor!')}\n\n"
        "💫 Ми допоможемо тобі отримати максимум від гри.\n"
        f"{ITALIC('Обери розділ нижче:')}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Акції", url="https://yourvipadvisor.com/promo")],
        [InlineKeyboardButton(text="🔥 VIP Програма", url="https://yourvipadvisor.com/vip")],
        [InlineKeyboardButton(text="📩 Підписатися на оновлення", callback_data="subscribe")]
    ])

    await message.answer(text, reply_markup=keyboard)

@dp.message(Command("info"))
async def info_cmd(message: types.Message):
    text = (
        f"ℹ️ {BOLD('Про проект')}\n\n"
        "Ми — команда VIP Advisor.\n"
        "🎰 Спеціалізуємось на бонусах, акціях і VIP-пропозиціях у гральній сфері.\n\n"
        f"{ITALIC('Підписуйся, щоб не пропустити вигідні оновлення!')}"
    )
    await message.answer(text)

@dp.message(Command("promo"))
async def promo_cmd(message: types.Message):
    text = (
        f"💎 {BOLD('Актуальні акції:')}\n\n"
        "🔥 100% бонус на перший депозит\n"
        "🎁 Безкоштовні спіни кожного понеділка\n"
        "💰 Кешбек до 15%\n\n"
        f"Деталі на сайті: https://yourvipadvisor.com/promo"
    )
    await message.answer(text)

@dp.message(Command("vip"))
async def vip_cmd(message: types.Message):
    text = (
        f"👑 {BOLD('VIP Клуб')}\n\n"
        "💼 Персональні бонуси\n"
        "🎁 Подарунки до свят\n"
        "📞 Приватна підтримка 24/7\n\n"
        f"Приєднуйся: https://yourvipadvisor.com/vip"
    )
    await message.answer(text)

# ------------------- Inline Callback -------------------

@dp.callback_query(F.data == "subscribe")
async def subscribe_callback(callback: types.CallbackQuery):
    await callback.answer("Дякуємо! Ти підписаний на оновлення 💛", show_alert=True)

# ------------------- Webhook -------------------

async def on_startup(app):
    webhook_url = f"{os.getenv('RENDER_EXTERNAL_URL')}/webhook/{TOKEN}"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook встановлено: {webhook_url}")

    # ✅ Реєструємо команди у Telegram меню
    commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="info", description="Про проект"),
        BotCommand(command="promo", description="Актуальні акції"),
        BotCommand(command="vip", description="VIP програма"),
    ]
    await bot.set_my_commands(commands)
    print("✅ Команди додано в Telegram меню")

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
