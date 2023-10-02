# helpdesk_bot

!!!atm BOT CAN SPEAK ONLY RUSSIAN!!!


Actually my first shitty pet-project

Telegram Bot as a Helpdesk service.

Users can make a tickets and watching for status.

Everyone(users and admins) have to register in Bot first.

To register User as Administrator you need to manually change role in table Users from "user" to "admin".

All data contained in SQLite DB. There are 1 DB(helpdesk.db) and 2 tables(users and tickets).

Also you need a config.py which contains "bot_token", "db_location" and "anydesk_image"

This is script for making tables:
##
    import sqlite3
    conn = sqlite3.connect("your_locate")
    cursor = conn.cursor()

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
##

## Users commands:
    /ticket_new - To Create a new Ticket
    /ticket_about - To get info about the Ticket
    /ticket_cancel - To cancel own Ticket
##

## Admins commands:
    There are several block
    Print block:
        /root_print_all - Print all Tickets 
        /root_print_created - Print Tickets with Status Created
        /root_print_in_work - Print Tickets with Status In Work
        /root_print_done - Print Tickets with Status Done
        /root_print_cancelled - Print Tickets with Status Cancelled
        /root_about - Print all information about single Ticket
    Functional block:
        /root_comment - Change the comment of single Ticket
        /root_in_work - Change status of single Ticket to "In Work"
        /root_done - Change status of single Ticket to "Done"
##

## Features: 
- Function to cancel current action
- AI to classify tickets
- Chat in Bot between User and Admin
##
#