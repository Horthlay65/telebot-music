import os
import telebot
from pytube import YouTube
from moviepy.editor import VideoFileClip

bot = telebot.TeleBot('6895521670:AAH3FLojwhtKjtrt0Da25_zo9s5_FTUS0j8')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to yotubebot!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        download_video(message)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

def download_video(message):
    try:
        url = message.text
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()

        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        file_path = os.path.join('downloads', video.default_filename)
        video.download(output_path='downloads')

        convert_to_audio(file_path, yt.title, message)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

def convert_to_audio(video_path, title, message):
    try:
        audio_path = os.path.join('downloads', f"{title}.mp3")
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path)

        with open(audio_path, 'rb') as audio_file:
            bot.send_audio(message.chat.id, audio_file, timeout=300)  # Increase timeout value

        bot.reply_to(message, f"Converted '{title}' video to audio successfully")
    except TimeoutError:
        bot.reply_to(message, "Sending audio timed out. Please try again later.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

bot.polling()
