import os
import asyncio
import random
from threading import Thread

from flask import Flask
from telegram import Bot

# ============================================================
# CONFIGURAÇÕES
# ============================================================

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = "@bubblewinofc"
LINK = "https://bubblewid.online?ref=s2otaxsb"

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
# ENVIO DE MENSAGEM
# ============================================================

async def send_message(bot):
    attempts = random.randint(MIN_ATTEMPTS, MAX_ATTEMPTS)

    if attempts == 1:
        attempt_text = "1 tentativa"
    else:
        attempt_text = f"{attempts} tentativas"

    message = (
        "🎮 HORA DE JOGAR!\n\n"
        f"🔗 {LINK}\n"
        f"🎯 Tentativas: {attempt_text}"
    )

    await bot.send_message(
        chat_id=CHANNEL,
        text=message
    )

    print(f"✅ Mensagem enviada! Tentativas: {attempts}")


# ============================================================
# LOOP DO BOT
# ============================================================

async def bot_loop():
    bot = Bot(token=TOKEN)

    print("🤖 Bubble Win Bot iniciado!")
    print(f"📢 Canal: {CHANNEL}")

    # TESTE: envia uma mensagem imediatamente
    try:
        await send_message(bot)
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")

    while True:
        wait_seconds = random.randint(MIN_WAIT, MAX_WAIT)

        print(
            f"⏳ Próxima mensagem em "
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
