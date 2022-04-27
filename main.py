import os
import shelve
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from santa_chat import generate_santa_response

load_dotenv()

db = None # This gets initialized later

updater = Updater(token=os.getenv('TELEGRAM_BOT_KEY'))
dispatcher = updater.dispatcher

def fetch_history(db, chat_id):
	if str(chat_id) not in db:
		db[str(chat_id)] = []
	return db[str(chat_id)]

def start(update, context):
	db[str(update.effective_chat.id)] = []
	context.bot.send_message(chat_id=update.effective_chat.id, text="Hey, I am Santa Clause. TheCakeIsALie convinced me to chat with you for a bit… So ask me anything, about Christmas, life, … You name it.")

def about(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="I am a bot that answers questions about Christmas. If I ever stop working that means Patrick messed something up!")

def reset(update, context):
	db[str(update.effective_chat.id)] = []
	context.bot.send_message(chat_id=update.effective_chat.id, text="Reset history.")

def santa_answer(update, context):
	history = fetch_history(db, update.effective_chat.id)#[-10:]

	new_user_input = update.message.text
	answer = generate_santa_response(new_user_input, history)

	context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

	history.append({'input': new_user_input, 'response': answer})
	

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('about', about))
dispatcher.add_handler(CommandHandler('reset', reset))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, santa_answer))

if __name__ == '__main__':
	db = shelve.open('santa_chat.db', writeback=True)

	updater.start_polling()
	updater.idle()

	db.close()