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


def job_exists(text):
  a = schedule.jobs
  for job in a:
    if job.job_func.args[0].args[0] == text:
      return True
  return False

def create_task(message, timer, edit=False):
  markup = types.InlineKeyboardMarkup(row_width=4)
  markup.row(
    types.InlineKeyboardButton('-30', callback_data='-30'),
    types.InlineKeyboardButton('-10', callback_data='-10'),
    types.InlineKeyboardButton('+10', callback_data='+10'),
    types.InlineKeyboardButton('+30', callback_data='+30')
    )
  markup.add(types.InlineKeyboardButton('✅ Schedule 🕒', callback_data='schedule'))
  if edit:
    bot.edit_message_text('*Set up time scheduler in minutes:*\nPost every {} min'.format(timer), message.chat.id,message.message_id, parse_mode='Markdown', reply_markup=markup)
  else:
    bot.reply_to(message, '*Set up time scheduler in minutes:*\nPost every {} min'.format(timer),parse_mode='Markdown',reply_markup=markup)


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
