import telebot
import time
from config import TOKEN, PATH_AUDIO, PATH_PHOTO
from logic import get_audio_file, get_photo_file, get_user,write_audio_to_db, write_photo_to_db, write_to_folder, convert_to_wav, check_face, get_photo_from_db, get_audio_from_db

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start', 'help'])
def process_start_command(message):
    bot.send_message(message.chat.id, "Привет!\nЯ бот для сохранения твоих голосовых сообщений(формат wav)\nи фото(без лица сохранять не буду)!\n\nВывести все сохраненные аудио: /all_voices\nВывести все фото: /all_photo")


@bot.message_handler(commands=['all_photo'])
def get_all_photo(message):
    photo_list = get_photo_from_db(get_user(message))
    for photo in photo_list:
        file_photo = open(PATH_PHOTO + get_user(message) + 
                            '/' + str(*photo), 'rb')
        bot.send_photo(message.chat.id, file_photo)
        file_photo.close()


@bot.message_handler(commands=['all_voices'])
def get_all_audio(message):
    audio_list = get_audio_from_db(get_user(message))
    for voice in audio_list:
        voice = open(PATH_AUDIO + get_user(message) +
                          '/' + str(*voice), 'rb')
        bot.send_audio(message.chat.id, voice)
        voice.close()
        time.sleep(.25)


@bot.message_handler()
def echo_message(message):
    bot.send_message(message.from_user.id, "Отправь голосовое или фото(/help для полной информации)")


@bot.message_handler(content_types=['voice'])
def load_audio(message):
    try:
        bot.send_message(
            message.from_user.id, "Обрабатываю...")

        audio, audio_id = get_audio_file(bot, message)

        user_key = get_user(message)

        PATH = PATH_AUDIO + user_key + '/'

        write_to_folder(PATH, audio_id, audio)

        sound_name = convert_to_wav(PATH, audio_id, user_key)

        write_audio_to_db(sound_name, user_key)
        

        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(content_types=['photo'])
def load_image(message):
    
        bot.send_message(
        message.from_user.id, "Обрабатываю...")

        try:

            photo, photo_id = get_photo_file(bot, message)

        except Exception as e:
            print("1")
            bot.reply_to(message, e)

        try:

            user_key = get_user(message)

        except Exception as e:
            print("2")
            bot.reply_to(message, e)

        try:
            
            PATH = PATH_PHOTO + user_key + '/'

        except Exception as e:
            print("3")
            bot.reply_to(message, e)

        
        try: 
            write_to_folder(PATH, photo_id, photo)

        except Exception as e:
            print("4")
            bot.reply_to(message, e)

        try:

            is_face, photo_name = check_face(PATH, photo_id)

        except Exception as e:
            print("5")
            bot.reply_to(message, e)

        try:
            if is_face:
                write_photo_to_db(photo_name, user_key)
                bot.reply_to(message, "Пожалуй, я сохраню это")
            else:
                bot.reply_to(message, "Не вижу лица")

        except Exception as e:
            print("6")
            bot.reply_to(message, e)


if __name__ == '__main__':
    bot.polling()
