import sqlite3
import os
import audiosegment
import numpy as np
import cv2
from PIL import Image
from config import PATH_CV2
import datetime

def get_photo_file(bot, message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    return downloaded_file, file_info.file_id


def get_audio_file(bot, message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    return downloaded_file, file_info.file_id


def get_user(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    if username != None:
        user_key = username + '(id=' + user_id + ')'
        return user_key
    else:
        return user_id

def write_to_folder(PATH, doc_id, doc):
    try:
        os.mkdir(PATH)
    except OSError as e:
        pass

    src = PATH + str(doc_id)
    with open(src, 'wb') as new_file:
        new_file.write(doc)


def write_audio_to_db(sound_name, user_key):
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    cursor.execute("INSERT INTO audio (audio) VALUES(?)",
                (sound_name,))
    cursor.execute("INSERT OR REPLACE INTO user (user_name) VALUES(?)",
                (user_key,))
    cursor.execute("INSERT INTO user_audio (ua_user, ua_audio) VALUES(?, ?)",
                (user_key, sound_name))
    con.commit()
    con.close()


def write_photo_to_db(photo_name, user_key):
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    cursor.execute("INSERT INTO photo (photo) VALUES(?)",
                   (photo_name,))
    cursor.execute("INSERT OR REPLACE INTO user (user_name) VALUES(?)",
                   (user_key,))
    cursor.execute("INSERT INTO user_photo (up_user, up_photo) VALUES(?, ?)",
                   (user_key, photo_name))
    con.commit()
    con.close()

def convert_to_wav(PATH, audio_id, user_key):
    i = len(os.listdir(PATH))

    sound = audiosegment.from_file(PATH + audio_id).resample(sample_rate_Hz=16000)
    sound_name = "audio{}({}).wav".format(i, datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S"))
    sound.export(PATH + sound_name, format="wav")

    os.remove(PATH + audio_id)

    return sound_name

def check_face(PATH, photo_id):
    photo = cv2.imread(PATH + photo_id)
    gray = cv2.cvtColor(cv2.UMat(photo), cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(PATH_CV2 + 'haarcascade_frontalface_default.xml')
    try:
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
        )
    except Exception as identifier:
        print(identifier)

    im = Image.open(PATH + photo_id)
    rgb_im = im.convert('RGB')
    os.remove(PATH + photo_id)
    i = len(os.listdir(PATH)) + 1
    photo_name = "photo{}({}).png".format(i,datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S"))

    if len(faces) > 0:
        rgb_im.save(PATH + photo_name)
        return True, photo_name
    else:
        return False, photo_name
    
def get_photo_from_db(user_key):
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    cursor.execute("SELECT up_photo from user_photo where up_user == ?",
                   (user_key,))
    photo_list = cursor.fetchall()
    con.commit()
    con.close()
    return photo_list


def get_audio_from_db(user_key):
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    cursor.execute("SELECT ua_audio from user_audio where ua_user == ?",
                   (user_key,))
    audio_list = cursor.fetchall()
    con.commit()
    con.close()
    return audio_list

