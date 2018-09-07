# -*- coding: utf-8 -*-
import config # bot's token
import telebot
from telebot import types

import shutil
import time
import sys
import os
sys.path.insert(0, '/home/surv_proj')
import moovm_det

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["start"])
def send_photo(message): 
    keyb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyb.row('Send photo 📷', 'Send video 🎥')
    keyb.row('Start surveillance ▶')
    keyb.row('Stop surveillance ⛔')
    keyb.row('Save images 📁', 'Pi Settings ⚙')
    bot.send_message(message.chat.id, "Here are your commands", reply_markup=keyb)

@bot.message_handler(content_types=["text"])
def text_handler (message):

	if message.text == "Send photo 📷":
	    moovm_det.snap()
	    bot.send_photo(message.chat.id, open('/home/surv_proj/bot/ph.jpeg','rb'))

	elif  message.text == "Send video 🎥":
	    keyb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	    keyb.row('Send 10s video')
	    keyb.row('Send 30s video')
	    keyb.row('Go back ⬅')
	    bot.send_message(message.chat.id, "Choose video lenght.", reply_markup=keyb)

	elif  message.text == "Send 10s video":
	    keyb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	    keyb.row('Send 10s video')
	    keyb.row('Send 30s video')
	    keyb.row('Go back ⬅')
	    bot.send_message(message.chat.id, "Recording and sending 10s video.", reply_markup=keyb)
	    moovm_det.vid(10)
	    bot.send_video(message.chat.id, open('/home/surv_proj/bot/vidmp4.mp4','rb'))
	  
	elif  message.text == "Send 30s video":
	    keyb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	    keyb.row('Send 10s video')
	    keyb.row('Send 30s video')
	    keyb.row('Go back ⬅')
	    bot.send_message(message.chat.id, "Recordind and sending 30s video.", reply_markup=keyb)
	    moovm_det.vid(30)
	    bot.send_video(message.chat.id, open('/home/surv_proj/bot/vidmp4.mp4','rb'))

	elif  message.text == "Go back ⬅":
	    keyb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	    keyb.row('Send photo 📷', 'Send video 🎥')
	    keyb.row('Start surveillance ▶')
	    keyb.row('Stop surveillance ⛔')
	    keyb.row('Save images 📁', 'Pi Settings ⚙')
	    bot.send_message(message.chat.id, "Going back", reply_markup=keyb)
	    
	elif  message.text == "Start surveillance ▶":
	    moovm_det.flag = False
	    moovm_det.mymessage = message
	    bot.send_message(message.chat.id, "Starting surveillance... To stop, choose /stop_surv")
	    moovm_det.surv(bot,message)

	elif  message.text == "Stop surveillance ⛔":
	    moovm_det.flag = True
	    bot.send_message(message.chat.id, "Stopping surveillance...")

	elif  message.text == "Save images 📁":
	    fpath = moovm_det.save_ims()
	    bot.send_message(message.chat.id, "Iamges successfully saved to " + fpath + " directiry on Rasperry Pi. Table truncated")

	elif  message.text == "Pi Settings ⚙":
	    keyb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	    keyb.row('CPU temperature 🌡')
	    keyb.row('Occupied space ⭕')
	    keyb.row('Delete temp files 🗑', 'Truncate SQL table ✂')
	    keyb.row('Go back ⬅')
	    bot.send_message(message.chat.id, "Bot settings", reply_markup=keyb)

	elif message.text == "CPU temperature 🌡":
	    tmp = os.popen("vcgencmd measure_temp").readline()
	    keyb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	    keyb.row('CPU temperature 🌡')
	    keyb.row('Occupied space ⭕')
	    keyb.row('Delete temp files 🗑', 'Truncate SQL table ✂')
	    keyb.row('Go back ⬅')
	    bot.send_message(message.chat.id, tmp, reply_markup=keyb)

	elif message.text == "Occupied space ⭕":
	    tmp1 = os.popen("du -sh /home/surv_proj").readline() + "\n" + os.popen("du -sh /var/lib/mysql/det_frames/").readline()
	    
	    keyb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	    keyb.row('CPU temperature 🌡')
	    keyb.row('Occupied space ⭕')
	    keyb.row('Delete temp files 🗑', 'Truncate SQL table ✂')
	    keyb.row('Go back ⬅')
	    bot.send_message(message.chat.id, tmp1, reply_markup=keyb)	 

	elif message.text == "Delete temp files 🗑":
	    shutil.rmtree('/var/lib/mysql/det_frames')
	    os.mkdir('/var/lib/mysql/det_frames')

	    keyb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	    keyb.row('CPU temperature 🌡')
	    keyb.row('Occupied space ⭕')
	    keyb.row('Delete temp files 🗑', 'Truncate SQL table ✂')
	    keyb.row('Go back ⬅')
	    bot.send_message(message.chat.id, "All detected frames deleted", reply_markup=keyb)

	elif message.text == "Truncate SQL table ✂":
	    moovm_det.trunc_table()
	    keyb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	    keyb.row('CPU temperature 🌡')
	    keyb.row('Occupied space ⭕')
	    keyb.row('Delete temp files 🗑', 'Truncate SQL table ✂')
	    keyb.row('Go back ⬅')
	    bot.send_message(message.chat.id, "Table truncated", reply_markup=keyb)

	else:
	    keyb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	    keyb.row('Send photo 📷', 'Send video 🎥')
	    keyb.row('Start surveillance ▶')
	    keyb.row('Stop surveillance ⛔')
	    keyb.row('Save images 📁', 'Pi Settings ⚙')
	    bot.send_message(message.chat.id, "Command not recognized. Choose one below", reply_markup=keyb)


@bot.callback_query_handler(func=lambda call:True)
def call_bb(call):
    moovm_det.send_uncropped(call, bot, call.data)  



if __name__ == '__main__':
    #bot.polling(none_stop=True, timeout=123)
    
    while True:
        try:
                bot.polling(none_stop=True, timeout=123)
                #bot.infinity_polling(True)
        except Exception as err:

                logging.error(err)

 
                print ("Internet error!")
                


