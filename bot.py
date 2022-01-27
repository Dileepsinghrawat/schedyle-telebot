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

bot.polling(none_stop=True)
