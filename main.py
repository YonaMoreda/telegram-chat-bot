import logging
import atexit
import configparser
import cleverbotfree.cbfree
from telegram import ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

config = configparser.ConfigParser()
config.read('configuration.ini')


cb = cleverbotfree.cbfree.Cleverbot()
cb.browser.get(cb.url)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot_token = config['TOKEN']['BotToken']
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi 🙂,\n\n"
                                  "I am RecVel, a simple blabbering bot.\n\n"
                                  "I won't read your messages unless you @ me 😩\n - @RecVel_bot")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def chat(update, context):
    cb.get_form()
    received_msg = update.message.text

    if '@RecVel_bot' in received_msg:
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        cb.send_input(received_msg.replace('@RecVel_bot', ''))
        response = cb.get_response()
        context.bot.send_message(chat_id=update.effective_chat.id, text=response,
                                 reply_to_message_id=update.message.message_id)


def exit_handler():
    cb.browser.close()
    print("exited bot")


atexit.register(exit_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), chat)
dispatcher.add_handler(echo_handler)

updater.start_polling()
print("Started bot")
