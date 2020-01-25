import telebot

TOKEN = '1072903861:AAEooMCno1LK2Ap7WdCaTaMPcZ_A2L7XWAc'
need_extension = ['ogg','mp3']

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def process_start_command(message):
    bot.send_message(message.chat.id, "Привет!\nНапиши мне что-нибудь!")


@bot.message_handler(commands=['help'])
def process_help_command(message):
    bot.send_message(message.chat.id, "Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@bot.message_handler()
def echo_message(msg):
    bot.send_message(msg.from_user.id, msg.text)


@bot.message_handler(content_types=['voice'])
def load_audio(message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id

        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'C:/Users/Marsel/Desktop/bussiness/projects/Python/bots/tz_dsplabs/audio/' + file_info.file_id
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(content_types=['voice'])
def load_chat_audio(message):
    pass

if __name__ == '__main__':
    bot.polling()
