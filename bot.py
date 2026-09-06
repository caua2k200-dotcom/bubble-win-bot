import os
import asyncio
import random
from threading import Thread

from flask import Flask
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

# ============================================================
# CONFIGURAÇÕES
# ============================================================

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = "@bubblewinofc"

LINK = "https://bubblewid.online?ref=s2otaxsb"

IMAGE_URL = "https://i.ibb.co/zVnHgFbS/Whats-App-Image-2026-09-06-at-18-04-29.jpg"

MIN_WAIT = 30 * 60
MAX_WAIT = 90 * 60

MIN_ATTEMPTS = 1
MAX_ATTEMPTS = 3


# ============================================================
# SERVIDOR WEB
# ============================================================

app = Flask(__name__)


@app.route("/")
def home():
    return "Bubble Win Bot está online! 🤖", 200


@app.route("/health")
def health():
    return "OK", 200


# ============================================================
# ENVIA FOTO + MENSAGEM + BOTÃO
# ============================================================

async def send_message(bot):
    attempts = random.randint(MIN_ATTEMPTS, MAX_ATTEMPTS)

    if attempts == 1:
        attempt_text = "1 tentativa"
    else:
        attempt_text = f"{attempts} tentativas"

    caption = (
        "🚨 <b>SINAL LIBERADO</b>\n\n"
        f"🎯 <b>Tentativas: {attempt_text}</b>"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🎮 CLIQUE AQUI PARA JOGAR",
                url=LINK
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await bot.send_photo(
        chat_id=CHANNEL,
        photo=IMAGE_URL,
        caption=caption,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

    print(f"✅ Sinal enviado! Tentativas: {attempts}")


# ============================================================
# LOOP DO BOT
# ============================================================

async def bot_loop():
    bot = Bot(token=TOKEN)

    print("🤖 Bubble Win Bot iniciado!")
    print(f"📢 Canal: {CHANNEL}")

    # Primeira mensagem imediatamente
    try:
        await send_message(bot)
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")

    while True:
        wait_seconds = random.randint(MIN_WAIT, MAX_WAIT)

        print(
            f"⏳ Próximo sinal em "
            f"{wait_seconds / 60:.1f} minutos."
        )

        await asyncio.sleep(wait_seconds)

        try:
            await send_message(bot)
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")


# ============================================================
# INICIA O BOT EM SEGUNDO PLANO
# ============================================================

def start_bot():
    asyncio.run(bot_loop())


bot_thread = Thread(
    target=start_bot,
    daemon=True
)

bot_thread.start()


# ============================================================
# SERVIDOR FLASK
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
