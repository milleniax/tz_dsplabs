import telebot
from logic import get_file, get_user, write_to_db, write_to_folder, convert_to_wav

TOKEN = '1072903861:AAEooMCno1LK2Ap7WdCaTaMPcZ_A2L7XWAc'
PATH = 'C:/Users/Marsel/Desktop/bussiness/projects/Python/bots/tz_dsplabs/audio/'

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
        audio, audio_id = get_file(bot, message)

        user_key = get_user(message)

        write_to_folder(PATH, user_key, audio_id, audio)

        write_to_db(audio_id, user_key)
        
        convert_to_wav(PATH, audio, user_key)
        

        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, e)

if __name__ == '__main__':
    bot.polling()
