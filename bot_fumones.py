import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ['BOT_TOKEN']
NOTION_TOKEN = os.environ['NOTION_TOKEN']
DATABASE_ID = os.environ['DATABASE_ID']

niveles = [
    {"nombre": "Bronce", "min": 0, "max": 249},
    {"nombre": "Plata", "min": 250, "max": 499},
    {"nombre": "Oro", "min": 500, "max": 999},
    {"nombre": "Platino", "min": 1000, "max": 100000}
]

def obtener_nivel(puntos):
    for nivel in niveles:
        if nivel["min"] <= puntos <= nivel["max"]:
            return nivel["nombre"]
    return "Sin nivel"

def obtener_usuarios():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    data = response.json()
    ids = []
    for item in data["results"]:
        try:
            id_texto = item["properties"]["title"]["title"][0]["text"]["content"]
            ids.append(id_texto)
        except:
            continue
    return ids

async def nivel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    usuarios = obtener_usuarios()
    if user_id in usuarios:
        puntos = 100
        nivel_usuario = obtener_nivel(puntos)
        await update.message.reply_text(f"Tu nivel es {nivel_usuario} ({puntos} puntos)")
    else:
        await update.message.reply_text("No estás registrado en el sistema.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("nivel", nivel))
app.run_polling()
