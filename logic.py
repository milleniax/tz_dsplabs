import sqlite3
import os
import soundfile as sf

def get_file(bot, message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    return downloaded_file, file_info.file_id

def get_user(message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_key = username + '(id=' + str(user_id) + ')'
    return user_key

def write_to_folder(PATH, user_key, audio_id, audio):
    path = PATH + user_key + '/'
    try:
        os.mkdir(path)
    except OSError as e:
        pass

    src = path + str(audio_id)
    with open(src, 'wb') as new_file:
        new_file.write(audio)


def write_to_db(audio, user):
     con = sqlite3.connect('db.db')
     cursor = con.cursor()
     cursor.execute("INSERT INTO audio (audio) VALUES(?)",
                    (str(audio),))
     cursor.execute("INSERT INTO user (user_name) VALUES(?)",
                    (user,))
     con.commit()
     con.close()

def convert_to_wav(PATH, audio, user_key):
    pass
