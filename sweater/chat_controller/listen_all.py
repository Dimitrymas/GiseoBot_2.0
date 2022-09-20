from sweater import bot
from sweater.chat_controller.callbackdata_listen import listen_callback
from sweater.chat_controller.chat_listen import listen_text
from sweater.chat_controller.commands_listen import listen_commands


@bot.message_handler(commands=['start', 'menu', 'diary'])
def command(message):
    listen_commands(message)
@bot.message_handler(content_types=['text'])
def text(message):
    listen_text(message)
@bot.callback_query_handler(func=lambda c:True)
def callback(message):
    listen_callback(message)