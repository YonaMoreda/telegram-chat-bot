import sys
import logging
import atexit
import configparser
import cleverbotfree.cbfree
from telegram import ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

config = configparser.ConfigParser()
config.read('configuration.ini')

cb = cleverbotfree.cbfree.Cleverbot()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

"""
function for '/start' command
"""


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi,\n\n"
                                  "I am RecVel, a simple blabbering bot based on cleverbot.com\n\n"
                                  "Use @RecVel_bot for me to read your message.\n")


"""
function for handling messages that are not commands
"""


def chat(update, context):
    try:
        cb.get_form()
    except Exception as e:
        sys.exit(e)

    received_msg = update.message.text

    if '@RecVel_bot' in received_msg:
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        cb.send_input(received_msg.replace('@RecVel_bot', ''))
        response = cb.get_response()
        context.bot.send_message(chat_id=update.effective_chat.id, text=response,
                                 reply_to_message_id=update.message.message_id)


"""
cleaning up function when exiting the bot
"""


def exit_handler():
    cb.browser.close()
    print("exited bot")


"""
main starter function, register the function handlers and start the polling the bot
"""


def main():
    bot_token = config['TOKEN']['BotToken']
    atexit.register(exit_handler)

    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    try:
        cb.browser.get(cb.url)  # for using clever bot
    except Exception as e:
        cb.browser.close()
        sys.exit(e)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), chat)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    print("Started bot")


if __name__ == '__main__':
    main()
