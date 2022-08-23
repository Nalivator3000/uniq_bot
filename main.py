import random

from PIL import Image, ImageDraw
import telebot
import numpy as np
from skimage.util import random_noise


bot = telebot.TeleBot('5565884556:AAHnnNgmJF7rGAXBgDjQ95se4YZzEze8yKA')


@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, 'Send your image')
    bot.register_next_step_handler(msg, save_image)


@bot.message_handler(content_types=['document'])
def save_image(message):
    try:
        msg = message
        chat_id = message.chat.id
        #file_id = message.photo[0].file_id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'files/' + file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "I got it")

        image_file = open(src, mode="rb")
        image = Image.open(image_file)  # next 3 lines strip exif
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        image_without_exif.save(src + '_without_exif.png')

        src = str(src + '_without_exif.png')
        image = Image.open(src)  # Открываем изображение.
        draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
        width = image.size[0]  # Определяем ширину.
        height = image.size[1]  # Определяем высоту.
        pix = image.load()  # Выгружаем значения пикселей.

        factor = 10
        for i in range(width):
            for j in range(height):
                rand = random.randint(-factor, factor)
                a = pix[i, j][0] + rand
                b = pix[i, j][1] + rand
                c = pix[i, j][2] + rand
                if (a < 0):
                    a = 0
                if (b < 0):
                    b = 0
                if (c < 0):
                    c = 0
                if (a > 255):
                    a = 255
                if (b > 255):
                    b = 255
                if (c > 255):
                    c = 255
                draw.point((i, j), (a, b, c))
        src = str(src + '_noysed.png')
        image.save(src)

        bot.send_message(message.chat.id, 'Here is your uniq image')
        new_file = open(src, mode="rb")
        bot.send_document(message.chat.id, new_file)
    except Exception as e:
        bot.reply_to(message, e)


def delete_meta(message):
    image_file = open(file_info.file_path, mode="rb")
    image = Image.open(image_file)  # next 3 lines strip exif
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image_without_exif.save(message.document.file_id + '_without_exif')


bot.polling(none_stop=True, interval=0)