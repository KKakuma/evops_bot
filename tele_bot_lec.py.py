import telebot
import re
import logging


API_TOKEN = '7352442248:AAH9iCQ63EBR9fZ7n4Nm9wb2Jzu8eEPq9mg'

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bot = telebot.TeleBot(API_TOKEN)

EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_REGEX = r'(\+7\d{10}|8\d{10})'
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()]).{8,}$'

def read_emails_from_file():
    try:
        with open('emails.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.error("File emails.txt not found.")
        return ""

def read_phones_from_file():
    try:
        with open('phones.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.error("File phones.txt not found.")
        return ""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! 👋 Я бот, который поможет тебе найти информацию в тексте.\n"
                      "Введи команду /find_email, чтобы найти email-адреса .\n"
                      "Введи команду /find_phone_number, чтобы найти номера телефонов.\n"
                      "Введи команду /verify_password, чтобы найти номера телефонов.\n"
                      "Чтобы узнать больше, введи команду /help.")
    
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Я умею следующее:\n"
                        "/find_email: Найди email-адреса в тексте.\n"
                        "/find_phone_number: Найди номера телефонов в тексте.\n"
                        "/verify_password: Проверь, насколько сложным является пароль.\n"
                        "Например, введи /find_email, а затем отправь текст, в котором нужно найти email-адреса.")

@bot.message_handler(commands=['find_email'])
def handle_find_email(message):
    bot.send_message(message.chat.id, "Пожалуйста, отправьте текст для поиска email-адресов.")
    bot.register_next_step_handler(message, find_email)

def find_email(message):
    text = message.text
    emails_content = read_emails_from_file()
    emails = re.findall(EMAIL_REGEX, emails_content)
    if emails:
        found_emails = [email for email in emails if email in text]
        if found_emails:
            bot.send_message(message.chat.id, "Найденные email-адреса:\n" + "\n".join(found_emails))
            logging.info(f"Found emails: {found_emails} in provided text and emails.txt")
        else:
            bot.send_message(message.chat.id, "Email-адреса не найдены в предоставленном тексте.")
            logging.info("No emails found in provided text.")
    else:
        bot.send_message(message.chat.id, "Email-адреса не найдены в файле.")
        logging.info("No emails found in emails.txt")

@bot.message_handler(commands=['find_phone_number'])
def handle_find_phone_number(message):
    bot.send_message(message.chat.id, "Пожалуйста, отправьте текст для поиска номеров телефонов.")
    bot.register_next_step_handler(message, find_phone_number)

def find_phone_number(message):
    text = message.text
    phones_content = read_phones_from_file()
    phone_numbers = re.findall(PHONE_REGEX, phones_content)
    if phone_numbers:
        found_numbers = [number for number in phone_numbers if number in text]
        if found_numbers:
            bot.send_message(message.chat.id, "Найденные номера телефонов:\n" + "\n".join(found_numbers))
            logging.info(f"Found phone numbers: {found_numbers} in provided text and phones.txt")
        else:
            bot.send_message(message.chat.id, "Номера телефонов не найдены в предоставленном тексте.")
            logging.info("No phone numbers found in provided text.")
    else:
        bot.send_message(message.chat.id, "Номера телефонов не найдены в файле.")
        logging.info("No phone numbers found in phones.txt")

@bot.message_handler(commands=['verify_password'])
def handle_verify_password(message):
    bot.send_message(message.chat.id, "Пожалуйста, отправьте пароль для проверки его сложности.")
    bot.register_next_step_handler(message, verify_password)

def verify_password(message):
    password = message.text
    if re.match(PASSWORD_REGEX, password):
        bot.send_message(message.chat.id, "Пароль сложный.")
        logging.info(f"Password verified as strong: {password}")
    else:
        bot.send_message(message.chat.id, "Пароль простой.")
        logging.info(f"Password verified as weak: {password}")

bot.polling(none_stop=True)