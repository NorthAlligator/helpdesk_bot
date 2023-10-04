# helpdesk_bot
## English
To change Bot's language to English or Russian you need a config.py with variable 'localization' equals 'ru' or 'en'
Russian set as default localization

Actually my first shitty pet-project

Telegram Bot as a simple Helpdesk service.

Users can make a tickets and watching for their status.

Everyone(users and admins) have to register in Bot first.

All data contained in SQLite DB. There are 1 DB(helpdesk.db) and 2 tables(users and tickets).

Also you need a config.py which contains "bot_token", "db_location", "localization" and "root_pass".
This file creates automatically if not exists.

DB and Tables will automatically created if they not exists in dir of Project.

### Users commands:
    /ticket_new - To Create a new Ticket
    /ticket_about - To get info about the Ticket
    /ticket_cancel - To cancel own Ticket
###

### Admins commands:
    There are several block
    Print block:
        /root_print_all - Print all Tickets 
        /root_print_created - Print Tickets with Status Created
        /root_print_in_work - Print Tickets with Status In Work
        /root_print_done - Print Tickets with Status Done
        /root_print_cancelled - Print Tickets with Status Cancelled
        /root_about - Print all information about single Ticket
        /root_print_users - Print all users
    Functional block:
        /root_comment - Change the comment of single Ticket
        /root_in_work - Change status of single Ticket to "In Work"
        /root_done - Change status of single Ticket to "Done"
        /root_stop_polling - Stop Bot
        /i_want_to_be_admin - If user enter password from config.py then he get role 'admin'
###

### Features: 
- Function to cancel current action
- AI to classify tickets
- Chat in Bot between User and Admin
- Docker File
- English language - Done
- Which admin change Ticket status to "In Work"
- Log for every Ticket, when status and comments changed, etc
- Web Interface
###
## Русский
Чтобы поменять язык бота на Английский или Русский Вам необходим файл config.py с переменной 'localization' равной 'ru' или 'en'
По дефолту локализация Русская

Это мой первый пет-проект на Python

Данный телеграм бот используется как простая Helpdesk система, без необходимости обучения пользователя.

Пользователи могу создавать заявки и отслеживать их статус.

Пользователям сначала необходимо зарегистрироваться.

Все данные хранятся в БД SQLite. Есть 1 БД(helpdesk.db) и две таблицы users и tickets.

Также необходимо создать файл config.py, который содержит данные переменные: "bot_token", "db_location", "localization" и "root_pass".
Файл создастся автоматически, если он не существует.

База данных и Таблицы автоматически создадутся в папке проекта, если они не существуют.

### Команды пользователей:
    /ticket_new - Создать новую заявку
    /ticket_about - Получить информацию о своей заявке
    /ticket_cancel - Отменить свою заявку
###

### Админские команды:
    Есть несколько блоков:
    Блок вывода:
        /root_print_all - Вывести все заявки
        /root_print_created - Вывести заявки со статусом "Создана"
        /root_print_in_work - Вывести заявки со статусом "В работе"
        /root_print_done - Вывести заявки со статусом "Завершена"
        /root_print_cancelled - Вывести заявки со статусом "Отменена"
        /root_about - Вывести всю информацию об одной заявке
        /root_print_users - Вывести всех пользователей
    Блок функций:
        /root_comment - Поменять комментарий специалиста заявки
        /root_in_work - Поменять статус заявки на "В работе"
        /root_done - Поменять статус заявки на "Завершена"
        /root_stop_polling - Остановить Бота
        /i_want_to_be_admin - Если пользователь введет пароль из файла config.py, то его роль изменится на 'admin'
###

### В разработке: 
- Функция отмены текущего действия
- ИИ для классификации заявок
- Чат между Админом и Пользователем в Боте
- Докер файл
- Английская локализация - Сделано
- Какой администратор какую заявку взял в работу
- Лог для каждой заявки, когда менялся статус, комментарии и прочее
- Веб Интерфейс
###
##
#