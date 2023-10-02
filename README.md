# helpdesk_bot
## English
!!!atm BOT CAN SPEAK ONLY RUSSIAN!!!

Actually my first shitty pet-project

Telegram Bot as a simple Helpdesk service.

Users can make a tickets and watching for their status.

Everyone(users and admins) have to register in Bot first.

To register User as Administrator you need to manually change role in table Users from "user" to "admin".

All data contained in SQLite DB. There are 1 DB(helpdesk.db) and 2 tables(users and tickets).

Also you need a config.py which contains "bot_token", "db_location" and "anydesk_image".

DB and Tables will automatically created if they not exists in dir of Project.

### Users commands:
    /ticket_new - To Create a new Ticket
    /ticket_about - To get info about the Ticket
    /ticket_cancel - To cancel own Ticket
###

### Admins commands:
    There are several block
- Print block:
- /root_print_all - Print all Tickets 
- /root_print_created - Print Tickets with Status Created
- /root_print_in_work - Print Tickets with Status In Work
- /root_print_done - Print Tickets with Status Done
- /root_print_cancelled - Print Tickets with Status Cancelled
- - /root_about - Print all information about single Ticket
- Functional block:
- - /root_comment - Change the comment of single Ticket
- - /root_in_work - Change status of single Ticket to "In Work"
- -/root_done - Change status of single Ticket to "Done"
###

### Features: 
- Function to cancel current action
- AI to classify tickets
- Chat in Bot between User and Admin
- Docker File
- English language
###
## Русский
Это мой первый пет-проект на Python

Данный телеграм бот используется как простая Helpdesk система, без необходимости обучения пользователя.

Пользователи могу создавать заявки и отслеживать их статус.

Пользователям сначала необходимо зарегистрироваться.

Чтобы установить администраторов Helpdesk системы, Вам необходимо вручную в Базе Данных в таблице "users" установить роль "admin" пользователю.

Все данные хранятся в БД SQLite. Есть 1 БД(helpdesk.db) и две таблицы users и tickets.

Также необходимо создать файл config.py, который содержит данные переменные: "bot_token", "db_location" и "anydesk_image".

База данных и Таблицы автоматически создадутся в папке проекта, если они не существуют.

### Команды пользователей:
    /ticket_new - Создать новую заявку
    /ticket_about - Получить информацию о своей заявке
    /ticket_cancel - Отменить свою заявку
###

### Админские команды:
    Есть несколько блоков:
- Блок вывода:
- - /root_print_all - Вывести все заявки
- - /root_print_created - Вывести заявки со статусом "Создана"
- - /root_print_in_work - Вывести заявки со статусом "В работе"
- - /root_print_done - Вывести заявки со статусом "Завершена"
- - /root_print_cancelled - Вывести заявки со статусом "Отменена"
- - /root_about - Вывести всю информацию об одной заявке
- Functional block:
- - /root_comment - Поменять комментарий специалиста заявки
- - /root_in_work - Поменять статус заявки на "В работе"
- - /root_done - Поменять статус заявки на "Завершена"
###

### В разработке: 
- Функция отмены текущего действия
- ИИ для классификации заявок
- Чат между Админом и Пользователем в Боте
- Докер файл
- Английская локализация
###
##
#