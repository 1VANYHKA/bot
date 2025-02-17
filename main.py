#Импортирование моделей для работы бота
import telebot
import config
import json
import time
import mysql.connector

#Импортирование классов из модулей
from threading import Thread
from telebot import types

#Импортирование класса из файла DB.py
from DB import DB as D
 
#Подключение к телеграмм боту
bot = telebot.TeleBot(config.TOKEN)
#Подключение к базе данных
DB = D(config.mysql)

#ID = Ваш телеграмм id

#Отправка сообщения пользователю
bot.send_message(ID, "Start Bot")

#Загрузка json данных, при неудаче загрузка не происходит
def json_loads(data):
    try:
        return json.loads(data)
    except:
        return None
#Получение данных о пользователе, если он имеется в базе данных, иначе создание нового пользователя
def get_student(message):
    data = DB.select('students', ['ID'], [['id', '=', message.chat.id]], 1)
    data = DB.select('status', ['status'], [['id', '=', message.chat.id]], 1)
    if (data):
        return {"id": data[9][1], "status": data[8][1],}

#Ведение логов о том, что вводили пользователи
def log(message, student):
    query = "INSERT INTO log (text) VALUES (%s)"

#Обновление статуса пользователя, в параметры передаётся данные пользователя и статус на который надо поменять
def student_update(student, status=None):
    DB.update('Users', {'status': status}, [['id', '=', student['id']]])

#Создание кнопок, в параметры передаётся массив из кнопок
def markups(buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b = []
    for i in buttons:
        b.append(types.KeyboardButton(i))
    markup.add(*b)
    return markup

#Создание кнопок для меню, в параметры передаётся только данные пользователя
def menu_markups(student):
    answer = markups(["Регистрация"])
    return answer

#После того как пользователь введёт команду 'start', телеграмм бот отправит ему сообщение и обновит его статус до 'menu'
@bot.message_handler(commands=['start'])
def start_message(message):
    student = get_student(message)
    if(student["status"] != "menu"):
        bot.send_message(message.chat.id,"Привет, давай соберём твоё портфолио" reply_markup=menu_markups(student))
        log(message, student)
        student_update(student, "menu")
    else:
        bot.send_message(student["id"], reply_markup=markups(['Регистрация','Олимпиада']))

#Перезапуск кнопок и отправка сообщение об этом
@bot.message_handler(commands=['restart'])
def start_message(message):
    student = get_student(message)
    bot.send_message(message.chat.id,"Ержан, вставай Эй!", reply_markup=menu_markups(student))
    log(message, student)
    student_update(student, "menu")
###########################################################################################################################################################################################
#Главный класс
class MessageHandler:
    #Класс в котором находятся основные функции бота
    class Main:
        #Отправка пользователя в меню
        def to_menu(bot, message, student):
            bot.send_message(student["id"], "Хорошего дня!", reply_markup=menu_markups(student))
            student_update(student, status="menu")
            return True
        
  class Reg:
    def reg_menu(bot, message, student, db):
        # Проверяем ввод пользователя
        if message.text.upper() == "LOGIN":
            # Обновляем статус пользователя
            student_update(student, status="reg_login")
            # Отправляем сообщение
            bot.send_message(student["id"], "Введите ваш логин", reply_markup=markups(['Назад']))
            # Возвращаем результат
            return MessageHandler.Reg.reg_login(bot, message, student)
        elif message.text.upper() == "PASSWORD":
            # Отправляем сообщение
            bot.send_message(student["id"], "Введите ваш пароль", reply_markup=markups(['Назад']))
            # Обновляем статус пользователя
            student_update(student, status="reg_password")
            # Возвращаем результат
            return MessageHandler.Reg.reg_password(bot, message, student)
        elif student["status"] == "reg_login":
            # Извлекаем хранящийся логин
            login = db.get_login()
            # Сравниваем логин
            if message.text == login:
                # Обновляем статус пользователя
                student_update(student, status="reg_password")
                # Отправляем сообщение
                bot.send_message(student["id"], "Введите ваш пароль", reply_markup=markups(['Назад']))
                # Возвращаем результат
                return MessageHandler.Reg.reg_password(bot, message, student)
            else:
                # Отправляем сообщение
                bot.send_message(student["id"], "Неправильный логин", reply_markup=markups(['Назад']))
        elif student["status"] == "reg_password":
            # Извлекаем хранящийся пароль
            password = db.get_password()
            # Сравниваем пароль
            if message.text == password:
                # Отправляем сообщение
                bot.send_message(student["id"], "Пароль правильный. Вы авторизованы.", reply_markup=markups(['Назад']))
                # Пропускаем пользователя дальше
                return MessageHandler.Reg.login_success(bot, message, student)
            else:
                # Отправляем сообщение
                bot.send_message(student["id"], "Пароль не правильный. Пожалуйста, зарегистрируйтесь на сайте.", reply_markup=markups(['Назад']))
                return MessageHandler.Reg.reg_menu(bot, message, student)

class Olimp:
    def photo(bot, message, student, db):
        bot.send_message(student["id"], "Отправьте фото", reply_markup=menu_markups(student))
        student_update(student, status="Photo")
        return True


    class Olimp:
        def photo(bot,message,student,db):
            bot.send_message(student["id"], "Отправьте фото", reply_markup=menu_markups(student))
            student_update(student, status="Photo")
            return True
            
        if("ОЛИМПИАДА" in message.test.upper()):
            student_update(student, status='photo')
            @bot.message_handler(content_types=['photo'])
        def photo_id(message,db):
            photo = max(message.photo, key=lambda x: x.height)
        data = DB.select('status', ['status'], [['id', '=', photo.file_id]], 1)

            

def update_connection():
    while True:
        try:
            del DB
            DB = DB(mysql)
            time.sleep(5)
        except:
            pass

thread1 = Thread(target=update_connection)
thread1.start()

@bot.message_handler(content_types=["text"])
def handle_text(message):
    print(f"{message.chat.id} {message.chat.first_name} |{message.text}|")
    message.text = message.text.strip().replace("  ", " ").replace("\t\t", "\t")
    student = get_student(message)
    log(message, student)
    action = {
        "menu": MessageHandler.Main.menu,
        "tasks": MessageHandler.Main.tasks,
        "tasks_comp": MessageHandler.Main.tasks_comp,
        "tasks_comp_end": MessageHandler.Main.tasks_comp_end,
        "set_menu": MessageHandler.Settings.set_menu,
        "set_name": MessageHandler.Settings.set_name,
        "set_surname": MessageHandler.Settings.set_surname,
        "set_let_class": MessageHandler.Settings.set_let_class,
        "set_num_class": MessageHandler.Settings.set_num_class,
        "reg_menu": MessageHandler.Reg.reg_menu,
        "reg_name": MessageHandler.Reg.reg_name,
        "reg_surname": MessageHandler.Reg.reg_surname,
        "reg_let_class": MessageHandler.Reg.reg_let_class,
        "reg_num_class": MessageHandler.Reg.reg_num_class,
        "reg_id_team": MessageHandler.Reg.reg_team_id,
        "reg_team_menu": MessageHandler.Reg.Team.reg_team_menu,
        "reg_team_name": MessageHandler.Reg.Team.reg_team_name
    }
    if action.get(student["status"]):
        if not action[student["status"]](bot, message, student):
            bot.send_message(student["id"], "Не понял!")
    else:
        bot.send_message(student["id"], f"Статус {student['status']} не найден!")
    return

bot.polling()