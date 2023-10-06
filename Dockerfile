FROM python:latest

WORKDIR /app

COPY helpdeskbot.py .

RUN pip install pyTelegramBotAPI==4.14.0 && pip install python-telegram-bot==20.5

CMD ["python", "helpdeskbot.py"]
