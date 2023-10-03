import telebot
import sqlite3
import os
from config import bot_token, db_location, anydesk_image
from telegram.constants import ParseMode
import datetime

#Устанавливаем текущую директорию, как директорию исполняемого файла
project_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_directory)

#Создание бота с токеном
bot = telebot.TeleBot(bot_token)
active_action = None

#Проверка существует ли БД и таблицы
try:
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()
    

    #Создание таблицы Tickets, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets(
        ticket_id INTEGER PRIMARY KEY NOT NULL,
        user_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        body TEXT NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        comment TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
''')
    #Создание таблицы Users, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        location TEXT NOT NULL,
        anydesk TEXT,
        role TEXT NOT NULL
    )
''')
    conn.commit()
    conn.close()
    print(f"Соединение с базой данных успешно установлено")
except sqlite3.Error as e:
    print(f"Ошибка при соединении с базой данных: {e}")

finally:
    if conn:
        conn.close()



##### Базовые функции #####
#Проверка админ ли пользователь
def getAdmins():
    conn = sqlite3.connect(db_location)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role='admin'")
    admin_users = [row['user_id'] for row in cursor.fetchall()]
    conn.close()
    return admin_users
      
#Получение данных пользователя из базы   
def getUserData(user_id):
    conn = sqlite3.connect(db_location)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id={user_id}")
    userData = cursor.fetchone()
    return userData    

#Конец текущего действия
def end_active_action():
    global active_action
    active_action = None

#Отображение клавиатуры меню
def show_menu_keyboard():
    menu_keyboard = telebot.types.InlineKeyboardMarkup()
    button_ticket_new = telebot.types.InlineKeyboardButton(text="Создать заявку",callback_data="new_ticket")
    button_ticket_about = telebot.types.InlineKeyboardButton(text="Узнать статус заявки",callback_data="about_ticket")
    button_ticket_cancel = telebot.types.InlineKeyboardButton(text="Отменить заявку",callback_data="cancel_ticket")
    menu_keyboard.add(button_ticket_new, button_ticket_about, button_ticket_cancel, row_width=1)
    return menu_keyboard



##### Обработчики нажатий кнопок #####
@bot.callback_query_handler(func=lambda call: call.data == "new_ticket")
def handle_new_ticket_callback(callback_query):
    global active_action
    if active_action:
        bot.answer_callback_query(callback_query.id, text="В данный момент активно одно из действий, завершите или отмените его.", show_alert=True)
    else:
        active_action = "new_ticket"
        message = callback_query.message
        new_ticket(message)

@bot.callback_query_handler(func=lambda call: call.data == "about_ticket")
def handle_about_ticket_callback(callback_query):
    global active_action
    if active_action:
        bot.answer_callback_query(callback_query.id, text="В данный момент активно одно из действий, завершите или отмените его.", show_alert=True)
    else:
        active_action = "about_ticket"
        message = callback_query.message
        about_ticket(message)

@bot.callback_query_handler(func=lambda call: call.data == "cancel_ticket")
def handle_cancel_ticket_callback(callback_query):
    global active_action
    if active_action:
        bot.answer_callback_query(callback_query.id, text="В данный момент активно одно из действий, завершите или отмените его.", show_alert=True)
    else:
        active_action = "cancel_ticket"
        message = callback_query.message
        cancel_ticket(message)


##### Обработчики сообщений и комманд #####
#Команда /start
@bot.message_handler(commands=['start'])
def welcome_message(message):
    user_id = message.from_user.id
    if getUserData(user_id):
        bot.send_message(message.chat.id,f"Добрый день, {getUserData(user_id)['name']}.\nВыберите пункт меню.", reply_markup = show_menu_keyboard())
    else:
        bot.send_message(message.chat.id,f"Здравствуйте!\nВас нет в базе.\nДля дальнейшего взаимодействия необходимо зарегистрироваться.\n\n<b>Пришлите Ваше ФИО полностью.</b>", parse_mode=ParseMode.HTML)
        bot.register_next_step_handler(message, register_user_phone)

def register_user_phone(message):
    name = message.text
    bot.send_message(message.chat.id,"Пришлите Ваш телефон, внутренний и мобильный(одним сообщением).")
    bot.register_next_step_handler(message, register_user_location, name)

def register_user_location(message, name):
    phone = message.text
    bot.send_message(message.chat.id,"Пришлите номер Вашего кабинета, либо где Вы находитесь, если Вы на удаленке, то так и укажите.")
    bot.register_next_step_handler(message, register_user_anydesk, name, phone)

def register_user_anydesk(message, name, phone):
    location = message.text
    text = ('''
Пришлите номер рабочего места из программы Anydesk(красная иконка, см. фото).\n
<b>В случае если программы нет - <a href = 'https://anydesk.com/ru/downloads/windows?dv=win_exe'>установите ее по ссылке</a></b>\n\n
<i>Просто перейдите по ссылке, скачивание начнется автоматически, после скачивания - запустите файл. Сверху будет номер Вашего рабочего места.</i>
    ''')
    with open(anydesk_image, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=text, parse_mode=ParseMode.HTML)
    bot.register_next_step_handler(message, register_user_end, name, phone, location)

def register_user_end(message, name, phone, location):
    anydesk = message.text
    user_id = message.chat.id
    conn = sqlite3.connect(db_location)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (user_id, name, phone, location, anydesk, role) VALUES ('{user_id}', '{name}', '{phone}', '{location}', '{anydesk}', 'user')")
    conn.commit()
    conn.close()
    if getUserData(user_id):
        bot.send_message(message.chat.id,f"Спасибо за регистрацию, {getUserData(user_id)['name']}.\nВсё прошло успешно.\nВыберите пункт меню.", reply_markup = show_menu_keyboard())
    else:
        bot.send_message(message.chat.id,"Возникла ошибка с регистрацией!")



#Команда /ticket_new
@bot.message_handler(commands=['ticket_new'])
def new_ticket(message):
    chat_id = message.chat.id
    if getUserData(chat_id):
        bot.send_message(chat_id, "Укажите тему заявки (кратко опишите проблему)")
        bot.register_next_step_handler(message, process_subject_step)
    else:
        bot.register_next_step_handler(message, welcome_message)

def process_subject_step(message):
    chat_id = message.chat.id
    subject = message.text
    bot.send_message(chat_id, "Подробно опишите в чем заключается проблема (какой ресурс, устройство), что именно не работает, какую ошибку выдает")
    bot.register_next_step_handler(message, process_insert_step, subject)

def process_insert_step(message, subject):
    dt_now = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    chat_id = message.chat.id
    body = message.text
    conn = sqlite3.connect(db_location)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO tickets (user_id, subject, body, date, status, comment) VALUES ('{chat_id}', '{subject}', '{body}', '{dt_now}','Создана', 'Комментариев нет')")
        conn.commit()
        bot.send_message(chat_id, "Заявка создана успешно.\n<b>ID Вашей заявки: {}</b>".format(cursor.lastrowid),parse_mode=ParseMode.HTML, reply_markup = show_menu_keyboard())
        for admin in getAdmins():
            bot.send_message(admin,f"<b>Поступила новая заявка!</b>\n<i>ID: {cursor.lastrowid}</i>\nТема: {subject}",parse_mode=ParseMode.HTML)       
    except sqlite3.Error as e:
        bot.send_message(chat_id, f"Произошла ошибка при создании заявки. Попробуйте еще раз. {e}", reply_markup = show_menu_keyboard())
    finally:
        conn.close()
    conn.close()
    end_active_action()

# Команда /ticket_about
@bot.message_handler(commands=['ticket_about'])
def about_ticket(message):
    chat_id = message.chat.id
    if getUserData(chat_id):    
        bot.send_message(chat_id, "Пожалуйста, введите ID заявки.")
        bot.register_next_step_handler(message, process_ticket_id_step)         
    else:
        bot.register_next_step_handler(message, welcome_message)

def process_ticket_id_step(message):
    conn = sqlite3.connect(db_location)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        ticket_id = int(message.text)
        cursor.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,))
        ticket = cursor.fetchone()
        if ticket:
            if user_id == ticket[1]:
                bot.send_message(chat_id, f"<b>ID заявки:</b> {ticket['ticket_id']}\n<b>Тема:</b> {ticket['subject']}\n<b>Тело: </b>{ticket['body']}\n<b>Статус:</b> {ticket['status']}\n<b>Комментарий специалиста:</b> {ticket['comment']}\n<b>Дата создания:</b> {ticket['date']}",parse_mode=ParseMode.HTML, reply_markup = show_menu_keyboard())
            else:
                bot.send_message(chat_id,"Вы можете посмотреть статус только своих заявок.", reply_markup = show_menu_keyboard())
        else:
            bot.send_message(chat_id, "Заявка с указанным ID не найдена.", reply_markup = show_menu_keyboard())
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректный ID заявки.", reply_markup = show_menu_keyboard())
    conn.close()
    end_active_action()



# Команда /ticket_cancel
@bot.message_handler(commands=['ticket_cancel'])
def cancel_ticket(message):
    chat_id = message.chat.id
    if getUserData(chat_id):      
        bot.send_message(chat_id, "Пожалуйста, введите ID заявки для отмены:")
        bot.register_next_step_handler(message, process_cancel_ticket_id_step)
    else:
        bot.register_next_step_handler(message, welcome_message)

def process_cancel_ticket_id_step(message):
    conn = sqlite3.connect(db_location)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        ticket_id = int(message.text)
        cursor.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,))
        ticket = cursor.fetchone()
        if ticket:
            if ticket['status'] == "Создана" or ticket['status'] == "В работе":
                if user_id == ticket['user_id']:
                    cursor.execute("UPDATE tickets SET status=? WHERE ticket_id=?", ("Отменена", ticket_id))
                    conn.commit()
                    bot.send_message(chat_id, f"Заявка с ID {ticket_id} была отменена.", reply_markup = show_menu_keyboard())
                else:
                    bot.send_message(chat_id, "Вы можете отменить только свои заявки.", reply_markup = show_menu_keyboard())
            else:
                bot.send_message(chat_id, "Невозможно отменить завершенную или отмененную заявку.", reply_markup = show_menu_keyboard())
        else:
            bot.send_message(chat_id, "Заявка с указанным ID не найдена.", reply_markup = show_menu_keyboard())
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректный ID заявки.", reply_markup = show_menu_keyboard())
    conn.close()
    end_active_action()


##### АДМИН МЕНЮ #####


#/root_print_all
#Вывод всех заявок
@bot.message_handler(commands=['root_print_all'])
def output_all_tickets(message):
    if (message.chat.id in getAdmins()):
        conn = sqlite3.connect(db_location)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets")
        tickets = cursor.fetchall()
        for ticket in tickets:
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (ticket['user_id'],))
            user_data = cursor.fetchone()
            bot.send_message(message.chat.id, f'''<b><i>Данные заявки:</i></b>\n<b>ID заявки:</b> {ticket['ticket_id']}\n<b>Тема:</b> {ticket['subject']}\n<b>Тело:</b> {ticket['body']}
<b>Статус:</b> {ticket['status']}\n<b>Комментарий специалиста:</b> {ticket['comment']}\n<b>Дата создания:</b> {ticket['date']}
\n<b><i>Данные пользователя:</i></b>\n<b>ФИО:</b> {user_data['name']}\n<b>Телефон:</b> {user_data['phone']}\n<b>Расположение:</b> {user_data['location']}
<b>Anydesk:</b> {user_data['anydesk']}''',parse_mode=ParseMode.HTML)
        conn.close()



#Вывод заявок по статусу
def output_tickets_by_status(message, status):
    if message.chat.id in getAdmins():
        conn = sqlite3.connect(db_location)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets WHERE status = ?", (status,))
        tickets = cursor.fetchall()
        for ticket in tickets:
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (ticket['user_id'],))
            user_data = cursor.fetchone()
            bot.send_message(message.chat.id, f'''<b><i>Данные заявки:</i></b>
<b>ID заявки:</b> {ticket['ticket_id']}
<b>Тема:</b> {ticket['subject']}
<b>Тело:</b> {ticket['body']}
<b>Статус:</b> {ticket['status']}
<b>Комментарий специалиста:</b> {ticket['comment']}
<b>Дата создания:</b> {ticket['date']}
\n<b><i>Данные пользователя:</i></b>
<b>ФИО:</b> {user_data['name']}
<b>Телефон:</b> {user_data['phone']}
<b>Расположение:</b> {user_data['location']}
<b>Anydesk:</b> {user_data['anydesk']}''', parse_mode=ParseMode.HTML)
        conn.close()



#/root_print_created
@bot.message_handler(commands=['root_print_created'])
def output_created_tickets(message):
    output_tickets_by_status(message, 'Создана')
#/root_print_in_work
@bot.message_handler(commands=['root_print_in_work'])
def output_inwork_tickets(message):
    output_tickets_by_status(message, 'В работе')
#/root_print_done
@bot.message_handler(commands=['root_print_done'])
def output_done_tickets(message):
    output_tickets_by_status(message, 'Завершена')
#/root_print_cancelled
@bot.message_handler(commands=['root_print_cancelled'])
def output_cancelled_tickets(message):
    output_tickets_by_status(message, 'Отменена')



#/root_comment
#Функция изменения комментария заявки
@bot.message_handler(commands=['root_comment'])
def change_comment(message):
    if message.chat.id in getAdmins():
        bot.send_message(message.chat.id, "Пожалуйста, введите ID заявки для изменения комментария.")
        bot.register_next_step_handler(message,change_comment_step)

def change_comment_step(message):
    conn = sqlite3.connect(db_location)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    chat_id = message.chat.id
    try:
        ticket_id = int(message.text)
        cursor.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,))
        ticket = cursor.fetchone()
        if ticket:
            bot.send_message(message.chat.id, "Введите новый комментарий.")
            conn.close()
            bot.register_next_step_handler(message, process_change_comment_step, ticket_id)
        else:
            bot.send_message(chat_id, "Заявка с указанным ID не найдена.")
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректный ID заявки.")
    conn.close()

def process_change_comment_step(message, ticket_id):
    conn = sqlite3.connect(db_location)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    new_comment = message.text
    cursor.execute(f"UPDATE tickets SET comment=? WHERE ticket_id=?",(new_comment, ticket_id))
    conn.commit()
    cursor.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,))
    ticket = cursor.fetchone()
    conn.close()
    bot.send_message(message.chat.id, "Комментарий был изменен.")
    bot.send_message(ticket['user_id'],f"Новый комментарий от специалиста у Вашей заявки.\n<b>ID заявки:</b> {ticket_id}\n<b>Тема:</b>{ticket['subject']}\n<b>Комментарий: </b>{ticket['comment']}", parse_mode=ParseMode.HTML)



#/root_about
#Админский вывод инфы
@bot.message_handler(commands=['root_about'])
def output_about(message):
    if message.chat.id in getAdmins():
        bot.send_message(message.chat.id, "Пожалуйста, введите ID заявки для просмотра информации.")
        bot.register_next_step_handler(message,output_about_step)

def output_about_step(message):
    conn = sqlite3.connect(db_location)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    chat_id = message.chat.id
    try:
        ticket_id = int(message.text)
        cursor.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,))
        ticket = cursor.fetchone()
        if ticket:
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (ticket['user_id'],))
            user_data = cursor.fetchone()
            bot.send_message(message.chat.id, f'''<b><i>Данные заявки:</i></b>
<b>ID заявки:</b> {ticket['ticket_id']}
<b>Тема:</b> {ticket['subject']}
<b>Тело:</b> {ticket['body']}
<b>Статус:</b> {ticket['status']}
<b>Комментарий специалиста:</b> {ticket['comment']}
<b>Дата создания:</b> {ticket['date']}
\n<b><i>Данные пользователя:</i></b>
<b>ФИО:</b> {user_data['name']}
<b>Телефон:</b> {user_data['phone']}
<b>Расположение:</b> {user_data['location']}
<b>Anydesk:</b> {user_data['anydesk']}''', parse_mode=ParseMode.HTML)
            conn.close()
        else:
            bot.send_message(chat_id, "Заявка с указанным ID не найдена.")
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректный ID заявки.")
    conn.close()



#/root_in_work
#Функция, чтобы взять заявку в работу
@bot.message_handler(commands=['root_in_work'])
def in_work(message):
    if message.chat.id in getAdmins():
        bot.send_message(message.chat.id, "Введите ID заявки, которую хотите взять в работу.")
        bot.register_next_step_handler(message, in_work_step)

def in_work_step(message):
    conn = sqlite3.connect(db_location)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    chat_id = message.chat.id
    try:
        ticket_id = int(message.text)
        cursor.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,))
        ticket = cursor.fetchone()
        if ticket:
            cursor.execute(f"UPDATE tickets SET status=? WHERE ticket_id=?",("В работе", ticket_id))
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id, "Заявка была взята в работу.")
            bot.send_message(ticket['user_id'],f"Ваша заявка была взята в работу.\n<b>ID заявки:</b> {ticket['ticket_id']}\n<b>Тема:</b>{ticket['subject']}", parse_mode=ParseMode.HTML)
        else:
            bot.send_message(chat_id, "Заявка с указанным ID не найдена.")
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректный ID заявки.")
    conn.close()



#/root_done
#Функция, чтобы завершить заявку
@bot.message_handler(commands=['root_done'])
def done(message):
    if message.chat.id in getAdmins():
        bot.send_message(message.chat.id, "Введите ID заявки, которую хотите завершить.")
        bot.register_next_step_handler(message, done_step)

def done_step(message):
    conn = sqlite3.connect(db_location)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    chat_id = message.chat.id
    try:
        ticket_id = int(message.text)
        cursor.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,))
        ticket = cursor.fetchone()
        if ticket:
            cursor.execute(f"UPDATE tickets SET status=? WHERE ticket_id=?",("Завершена", ticket_id))
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id, "Заявка была завершена.")
            bot.send_message(ticket['user_id'],f"Ваша заявка была завершена.\n<b>ID заявки:</b> {ticket['ticket_id']}\n<b>Тема:</b>{ticket['subject']}", parse_mode=ParseMode.HTML)
        else:
            bot.send_message(chat_id, "Заявка с указанным ID не найдена.")
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректный ID заявки.")
    conn.close()



#/root_stop_polling
#Функция, чтобы остановить бота
@bot.message_handler(commands=['root_stop_polling'])
def root_stop_polling(message):
    if message.chat.id in getAdmins():
        bot.stop_polling()
        bot.send_message(message.chat.id,"Бот успешно выключен.")
        print("Бот был выключен.")
    else:
        print("дурак?")


#Бесконечный цикл работы бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
