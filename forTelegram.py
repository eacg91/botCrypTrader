from config import * #Importamos el token de config.py en el mismo directorio
from index import *
import telebot
import threading

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=["convert","convertir"])
def cmd_start(message):
	txt = " {} USD".format( convert2(1,"BTC",'USD') )
	bot.reply_to(message,message.text.split(commands)[1])
	
@bot.message_handler(commands=["start","inicia"])
def cmd_start(message):
	bot.reply_to(message, "hola! ")

@bot.message_handler(content_types=["text"])
def bot_mensajes_texto(message):
	if message.text.startswith("/"):
		comand = message.text.split('/')[1]
		txt = " {} USD".format( convert2(1,comand,'USD') )
		#if command.startswith("convert") == ""
		#bot.send_message(message.chat.id,txt)
		bot.reply_to(message,txt)

crypto = crypto()
hilo = threading.Thread(target=test)
if __name__ == "__main__":
	print("Iniciando Bot")
	hilo.start()
	bot.infinity_polling()
	print("Fin")
