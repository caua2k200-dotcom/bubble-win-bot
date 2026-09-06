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

MIN_WAIT = 30 * 60  # 30 minutos
MAX_WAIT = 90 * 60  # 90 minutos

MIN_ATTEMPTS = 1
MAX_ATTEMPTS = 3


# ============================================================
# SERVIDOR WEB PARA O RENDER / UPTIMEROBOT
# ============================================================

app = Flask(__name__)


@app.route("/")
def home():
    return "Bubble Win Bot está online! 🤖", 200


@app.route("/health")
def health():
    return "OK", 200


def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


# ============================================================
# ENVIA MENSAGEM
# ============================================================

async def send_message(bot):
    attempts = random.randint(MIN_ATTEMPTS, MAX_ATTEMPTS)

    if attempts == 1:
        text = "1 tentativa"
    else:
        text = f"{attempts} tentativas"

    message = (
        "🎮 HORA DE JOGAR!\n\n"
        f"🔗 {LINK}\n"
        f"🎯 Tentativas: {text}"
    )

    await bot.send_message(
        chat_id=CHANNEL,
        text=message,
        disable_web_page_preview=False
    )

    print(f"Mensagem enviada: {attempts} tentativa(s)")


# ============================================================
# LOOP DO BOT
# ============================================================

async def bot_loop():
    bot = Bot(token=TOKEN)

    print("🤖 Bot iniciado!")
    print("📢 Canal:", CHANNEL)
    print("⏱️ Intervalo: 30–90 minutos")
    print("🎯 Tentativas: 1–3")

    # Primeira mensagem imediatamente
    await send_message(bot)

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
            print("Erro ao enviar mensagem:", e)


# ============================================================
# INICIALIZAÇÃO
# ============================================================

if __name__ == "__main__":
    web_thread = Thread(
        target=run_web_server,
        daemon=True
    )
    web_thread.start()

    asyncio.run(bot_loop())
