from flask import Flask, render_template, request, url_for, Response
from telegram import Update, ForceReply, Bot
#from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
import yfinance as yf
import configparser
import ppi_api

app = Flask(__name__)   
Config = configparser.ConfigParser()
Config.read("config.config")   
TOKEN = Config.get("Telegram", "token")
BOT = Bot(token=TOKEN)


# @app.route('/')
# async def hello_world():
#     chat = 5617168866
#     hola = await BOT.sendMessage(chat_id=chat, text='Hola desde flask')
#     return Response('generic ok', status=200)

@app.route('/start')
async def hello_world2():
    bot = Bot(token=TOKEN)
    chat = 5617168866
    hola = await bot.sendMessage(chat_id=chat, text="ppi.main()") ##TODO: descomentar y que mande el informe de ppi_api
    return Response('start ok', status=200)

@app.route('/precio/<accion>')
async def precio(accion):
    chat = 5617168866
    data = yf.download(accion, start="2023-07-31", end="2023-08-01")
    valor = str(data['Close'].iloc[-1])
    mensaje = f"El valor actual de {accion} es: {valor}"
    hola = await BOT.sendMessage(chat_id=chat, text=mensaje)
    return render_template("index.html")



# To Get Chat ID and message which is sent by client
def message_parser(message):
    chat_id = message['message']['chat']['id']
    text = message['message']['text']
    print("Chat ID: ", chat_id)
    print("Message: ", text)
    return chat_id, text


@app.route('/', methods=['GET', 'POST'])
async def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, text_recieved = message_parser(msg)
        answer = text_recieved
        hola = await BOT.sendMessage(chat_id=chat_id, text=answer)

        return Response('ok', status=200)
    else:
        return "<h1>Something went wrong</h1>"








if __name__ == "__main__":
    app.run(debug=True)