import telebot
import random
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

owm = OWM('774cb6fdebf1630ed52ddeffec8907fe')
mgr = owm.weather_manager()

text = ''

bot = telebot.TeleBot("1182353327:AAGB6SVaVoiIxnpherd6IML5eh49mxBHVtE")

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.from_user.id, "Привет, вот список моих команд:\n/weather - Информация о погоде \n/flip - Подбросить монетку")

@bot.message_handler(commands=["weather"])
def weather(message) :
  msg = bot.send_message(message.from_user.id, "Введи название города")
  bot.register_next_step_handler(msg, city)
def city(message) :
  try : 
    chat_id = message.chat.id
    text = message.text
    owm = OWM('774cb6fdebf1630ed52ddeffec8907fe')
    mgr = owm.weather_manager()
    
    if text == '/weather' :
      text = ''
      weather(message) 
    elif text == '/start' :
      text = ''
      start(message)
    elif text == '/flip' :
      text = ''
      flip(message)
    else :
      observation = mgr.weather_at_place(text)
      w = observation.weather
                      
      a = w.temperature('celsius')['temp']   #Температура в переменную

      if a > 22 :
       bot.send_message(message.from_user.id,'На улице жарко, примерно: ' + str(int(a)) + "°")
      elif a > 18 :
        bot.send_message(message.from_user.id,'На улице тепло, примерно: ' + str(int(a)) + "°")
      elif a > 10 :
        bot.send_message(message.from_user.id,'На улице прохладно, примерно: ' + str(int(a)) + "°")
      elif a > 0 :
        bot.send_message(message.from_user.id,'На улице холодно, примерно: ' + str(int(a)) + "°")
      elif a <= 0 :
        bot.send_message(message.from_user.id,'На улице мороз, оденься теплее примерно: ' + str(int(a)) + "°")        #проверка температуры          
         
      r = str(w.rain)
      if r != "{}" :
        bot.send_message(message.from_user.id,"дождливо")          #проверка на дождь

      if w.detailed_status == 'fog' :
        bot.send_message(message.from_user.id,'Туман')                     #проверка на туман

      bot.send_message(message.from_user.id,'Влажность воздуха:' + str(w.humidity))          #влажность

      if w.clouds > 66 :
        bot.send_message(message.from_user.id,'Облачно')   
      elif w.clouds > 33 :
        bot.send_message(message.from_user.id,'Местами облачно')
      elif w.clouds > 0 :
        bot.send_message(message.from_user.id,'Небо чистое')          #проверка на облачность
      weather(message)  
        
  except Exception: 
    bot.send_message(message.from_user.id,"Попробуй ввести название города на английском")
    weather(message)

@bot.message_handler(commands=["flip"]) 
def flip(message) :
  bot.send_message(message.from_user.id,"Подбросить монетку?\n")
  bot.register_next_step_handler(message, fl)
def fl(message) :
  chat_id = message.chat.id 
  text = message.text
  if text == '/weather' :
    text  = ''
    weather(message) 
  elif text  == '/start' :
    text  = ''
    start(message)
  elif text  == "Да" :
    c = random.randint(0, 1)  
    if c == 1 :
      bot.send_message(message.from_user.id,"Орёл")
      text = ''
      flip(message)
    else :
      bot.send_message(message.from_user.id,"Решка")
      text  = ''
      flip(message)
  elif text  == "Нет" :
      bot.send_message(message.from_user.id,"Как хочешь")
      text  = ''
      start(message)
  else :
    bot.send_message(message.from_user.id,"Я тебя не понимаю")
    text  = ''
    flip(message)

bot.polling(none_stop=True, interval=0)   