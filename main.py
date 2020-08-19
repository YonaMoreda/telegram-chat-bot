import logging
import atexit
import cleverbotfree.cbfree
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

cb = cleverbotfree.cbfree.Cleverbot()
cb.browser.get(cb.url)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot_token = '1210596258:AAHoV9p4zpsj9nF0A5Lvg9Ft7-k4MMyZ2_E'
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi, I'm that one dumb friend that is always there to talk with you. ;)")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def chat(update, context):
    cb.get_form()
    cb.send_input(update.message.text)
    response = cb.get_response()
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def exit_handler():
    cb.browser.close()


atexit.register(exit_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), chat)
dispatcher.add_handler(echo_handler)

updater.start_polling()
