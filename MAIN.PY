from telebot import TeleBot
import threading
import os

bot = TeleBot("7373105149:AAE_PPxgz6ku6gdF5QJX8HJ252fOLW3Nifo")  # API kalitini o'zgartiring

def send_photo(chat_id):
    if os.path.exists("1.jpg"):
        with open("1.jpg", "rb") as photo: 
            bot.send_photo(chat_id, photo)
    else:
        bot.send_message(chat_id, "Rasm topilmadi.")

def send_video(chat_id):
    if os.path.exists("1.mp4"):
        with open("1.mp4", "rb") as video: 
            bot.send_video(chat_id, video)
    else:
        bot.send_message(chat_id, "Video topilmadi.")

def send_music(chat_id):
    if os.path.exists("1.m4a"):
        with open("1.m4a", "rb") as music:  
            bot.send_audio(chat_id, music)
    else:
        bot.send_message(chat_id, "Musiqa topilmadi.")

def send_media(chat_id):
    send_photo(chat_id)
    send_video(chat_id)
    send_music(chat_id)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! /media buyruğini kiriting.")

@bot.message_handler(commands=['media'])
def media_handler(message):
    chat_id = message.chat.id
    threading.Thread(target=send_media, args=(chat_id,)).start()
    bot.send_message(chat_id, "Media yuborilmoqda...")

bot.polling()

