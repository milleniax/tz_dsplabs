import telebot
from config import TOKEN, PATH_AUDIO, PATH_PHOTO
from logic import get_audio_file, get_photo_file, get_user,write_audio_to_db, write_photo_to_db, write_to_folder, convert_to_wav, check_face

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
        audio, audio_id = get_audio_file(bot, message)

        user_key, PATH = get_user(message, PATH_AUDIO)

        write_to_folder(PATH, audio_id, audio)

        sound_name = convert_to_wav(PATH, audio_id, user_key)

        write_audio_to_db(sound_name, user_key)
        

        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(content_types=['photo'])
def load_image(message):
    try:
        photo, photo_id = get_photo_file(bot, message)

        user_key, PATH = get_user(message, PATH_PHOTO)

        write_to_folder(PATH, photo_id, photo)

        is_face, photo_name = check_face(PATH, photo_id)

        if is_face:
            write_photo_to_db(photo_name, user_key)
            bot.reply_to(message, "Пожалуй, я сохраню это")
        else:
            bot.reply_to(message, "Не вижу лица")

        
    except Exception as e:
        bot.reply_to(message, e)


if __name__ == '__main__':
    bot.polling()
