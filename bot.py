import os
import asyncio
import random
from datetime import datetime

from telegram import Bot

# ============================================================
# CONFIGURAÇÃO
# ============================================================

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = "@bubblewinofc"
LINK = "https://bubblewid.online?ref=s2otaxsb"

MIN_WAIT = 30 * 60       # 30 minutos
MAX_WAIT = 90 * 60       # 90 minutos

MIN_ATTEMPTS = 1
MAX_ATTEMPTS = 3


# ============================================================
# ENVIA UMA MENSAGEM
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
        text=message,
        disable_web_page_preview=False
    )

    print(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
        f"Mensagem enviada | {attempts} tentativa(s)"
    )


# ============================================================
# LOOP PRINCIPAL
# ============================================================

async def main():
    bot = Bot(token=TOKEN)

    print("🤖 Bubble Win Bot iniciado!")
    print(f"📢 Canal: {CHANNEL}")
    print("⏱️ Intervalo: 30–90 minutos")
    print("🎯 Tentativas: 1–3")

    # Envia a primeira mensagem imediatamente.
    await send_message(bot)

    while True:
        wait_seconds = random.randint(MIN_WAIT, MAX_WAIT)

        minutes = wait_seconds / 60

        print(
            f"⏳ Próxima mensagem em "
            f"{minutes:.1f} minutos."
        )

        await asyncio.sleep(wait_seconds)

        await send_message(bot)


if __name__ == "__main__":
    asyncio.run(main())
