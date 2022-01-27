import functools
import queue
import re
import schedule
import telebot
import threading
import time
from telebot import types
from credentials import token, admins

bot = telebot.TeleBot(token)
timers = ['-10', '+10', '-30', '+30']


@bot.message_handler(commands=['start'])
def start_command(message):
  bot.send_message(message.chat.id, '<b>Hello {}</b>\n'.format(message.from_user.first_name),parse_mode='HTML')


@bot.message_handler(commands=['add'])
def post_command(message):
  markup = types.ForceReply(selective=False)
  bot.send_message(message.chat.id, 'Reply me with message you want to schedule', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def text_handling(message):
  if message.reply_to_message:
    if message.reply_to_message.text == 'Reply me with message you want to schedule':
      if not job_exists(message.text):
        create_task(message, 60)
      else:
        bot.send_message(message.chat.id, '*Post with the same text already exists!*',parse_mode='Markdown')
    else:
      bot.send_message(message.chat.id, text = 'Alhil',parse_mode='Markdown')
      

bot.polling(none_stop=True)
