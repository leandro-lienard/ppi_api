import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import configparser
import ppi_api

Config = configparser.ConfigParser()
Config.read("config.config")   
TOKEN = Config.get("Telegram", "token")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
def format_list(data_list):
    return '\n\n'.join('\n'.join(f'{key}: {value}' for key, value in data.items()) for data in data_list)
        # result = '\n'.join(f'{key}: {value}' for key, value in data_dict.items())

    # return '\n'.join(str(item) for item in list)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=format_list(ppi_api.main()))
    print("CHAT ID:", update.effective_chat.id)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()