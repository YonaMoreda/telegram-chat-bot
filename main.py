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


def start(update, context):
    """
    function for '/start' command
    :param update: telegram library object
    :param context: telegram library object for bot actions
    :return:
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi, I am bot RecVel.\n\nA simple blabbering bot based on CleverBot (cleverbot.com)."
                                  "\n\nUse @RecVel_bot for me to read your message.\n")


def chat(update, context):
    """
    function for handling messages that are not commands
    :param update: telegram library object
    :param context: telegram library object for bot actions
    :return:
    """
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


def exit_handler():
    """
    cleaning up function when exiting the bot
    :return:
    """
    cb.browser.close()
    print("exited bot")


def main():
    """
    main starter function, register the function handlers and start the polling the bot
    :return:
    """
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
