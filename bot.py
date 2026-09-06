import os
import asyncio
import random
from threading import Thread
from datetime import datetime, timedelta, timezone

from flask import Flask
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

# ============================================================
# CONFIGURAÇÕES
# ============================================================

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = "@bubblewinofc"

LINK = "https://bubblewid.online?ref=s2otaxsb"

IMAGE_URL = "https://i.ibb.co/zVnHgFbS/Whats-App-Image-2026-09-06-at-18-04-29.jpg"

# Intervalo entre os sinais
MIN_WAIT = 30 * 60
MAX_WAIT = 90 * 60

# Tentativas
MIN_ATTEMPTS = 1
MAX_ATTEMPTS = 3

# Duração de cada sinal
SIGNAL_DURATION = 5

# Horário de Brasília (UTC-3)
BRAZIL_TZ = timezone(timedelta(hours=-3))


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
    # Sorteia as tentativas
    attempts = random.randint(MIN_ATTEMPTS, MAX_ATTEMPTS)

    if attempts == 1:
        attempt_text = "1 tentativa"
    else:
        attempt_text = f"{attempts} tentativas"

    # Horário do sinal
    start_time = datetime.now(BRAZIL_TZ)

    # Horário em que o sinal termina
    end_time = start_time + timedelta(minutes=SIGNAL_DURATION)

    start_text = start_time.strftime("%H:%M")
    end_text = end_time.strftime("%H:%M")

    # Mensagem
    caption = (
        "🚨 <b>SINAL LIBERADO</b>\n\n"
        f"🕐 <b>Início:</b> {start_text}\n"
        f"⏰ <b>Encerra:</b> {end_text}\n\n"
        f"🎯 <b>Tentativas: {attempt_text}</b>"
    )

    # Botão
    keyboard = [
        [
            InlineKeyboardButton(
                "🎮 CLIQUE AQUI PARA JOGAR",
                url=LINK
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Envia imagem + legenda + botão
    await bot.send_photo(
        chat_id=CHANNEL,
        photo=IMAGE_URL,
        caption=caption,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

    print(
        f"✅ Sinal enviado | "
        f"Início: {start_text} | "
        f"Fim: {end_text} | "
        f"Tentativas: {attempts}"
    )


# ============================================================
# LOOP DO BOT
# ============================================================

async def bot_loop():
    bot = Bot(token=TOKEN)

    print("🤖 Bubble Win Bot iniciado!")
    print(f"📢 Canal: {CHANNEL}")
    print("⏱️ Intervalo: 30–90 minutos")
    print("🎯 Tentativas: 1–3")
    print("⏰ Duração do sinal: 5 minutos")

    # Primeira mensagem imediatamente
    try:
        await send_message(bot)
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")

    while True:
        # Sorteia o próximo intervalo
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
# INICIA O BOT
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
