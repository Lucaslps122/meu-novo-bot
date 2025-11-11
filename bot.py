from flask import Flask, request
from telegram import Bot, Update
from telegram.constants import ParseMode
from datetime import datetime

# === CONFIGURAÇÃO ===
TOKEN = "8003613789:AAE8GMU2LMuelsPTwd5hdVSaOdfc65LbR1w"
ADMINS = [8450036914, 5851719492, 7628586863, 5870846984]
# =====================

app = Flask(__name__)
bot = Bot(token=TOKEN)

def avisar_admins(mensagem):
    for admin in ADMINS:
        bot.send_message(chat_id=admin, text=mensagem, parse_mode=ParseMode.HTML)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    if update.message and update.message.new_chat_members:
        for novo in update.message.new_chat_members:
            nome = f"{novo.first_name or ''} {novo.last_name or ''}".strip()
            username = f"@{novo.username}" if novo.username else "(sem username)"
            horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            grupo = update.message.chat.title

            msg = (
                f"<b>🚨 Novo membro no grupo!</b>\n\n"
                f"👥 <b>Grupo:</b> {grupo}\n"
                f"🧍 <b>Nome:</b> {nome}\n"
                f"🔗 <b>Username:</b> {username}\n"
                f"🆔 <b>ID:</b> <code>{novo.id}</code>\n"
                f"⏰ <b>Entrou em:</b> {horario}"
            )
            avisar_admins(msg)
    return "ok"

@app.route("/")
def home():
    return "Bot funcionando!"
