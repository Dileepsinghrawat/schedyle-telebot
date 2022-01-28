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

ALL_TIMES = ["0:22:10"]

def send_hi(akhil):
  bot.send_message(admins,text="Good")


def worker_main():
    while True:
        job_func = jobqueue.get()
        job_func()
        jobqueue.task_done()
 
 
jobqueue = queue.Queue()
worker_thread = threading.Thread(target=worker_main)
worker_thread.start()
 
def scheduler_func():
    while True:
        schedule.run_pending()
        time.sleep(1)
 
sched_thread = threading.Thread(name='scheduler', target=scheduler_func)
sched_thread.start()
 
for scheduled_post in ALL_TIMES:
  schedule.every().day.at(scheduled_post).do(send_hi)
  
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
      
@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
  if call.message:
    if call.data in timers:
      m = re.search(' [0-9]* ', call.message.text)
      if m:
        newtimer = eval((m.group(0) + call.data))
        if newtimer < 10:
          bot.answer_callback_query(call.id, 'Minimal time for post schedule is 10 minutes!', show_alert=True)
        else:
          create_task(call.message, newtimer, True)
  elif call.data == 'schedule':
    m = re.search(' [0-9]* ', call.message.text)
    if m:
      p.set(str(int(m.group(0))) + 'post' + str(call.id), call.message.reply_to_message.text)
     schedule.every(int(m.group(0))).minutes.do(jobqueue.put,
                                                           functools.partial(announce,
                                                                             call.message.reply_to_message.text))
                bot.answer_callback_query(call.id, 'Will be posted every {} minutes'.format(m.group(0)))
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('🚫 Cancel 🕒', callback_data='cancel'))
                bot.edit_message_text('*Will be posted every {} minutes*'.format(m.group(0)), call.message.chat.id,
                                      call.message.message_id, parse_mode='Markdown', reply_markup=markup)



bot.polling(none_stop=True)
