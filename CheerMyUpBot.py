import telebot
import requests
import config
import random
from wonderwords import RandomSentence
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

s = RandomSentence()


class RandomQuotes:
    quotes = None

    @classmethod
    def capital_lettered_quotes(cls):
        if not cls.quotes:
            cls.quotes = requests.get(
                "https://raw.githubusercontent.com/ranjith19/random-quotes-generator/master/quotes.txt").text.split(
                "\n.\n")
        return random.choice(cls.quotes)


capital_lettered_quotes = RandomQuotes()


@bot.message_handler(commands=['start'])
def welcome(message):
    # sti = open('static/welcome.webp', 'rb')
    # bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("😊🎲 Weird sentence")
    item2 = types.KeyboardButton("😊 How are you?")
    item3 = types.KeyboardButton("🎲 Random Phrase")

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id,
                     "Welcome, {0.first_name}!\n "
                     "I am - <b>{1.first_name}</b>, "
                     "bot created to cheer you up.".format(message.from_user, bot.get_me()),
                     parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message, RandomQuotes=capital_lettered_quotes):
    if message.chat.type == 'private':
        if message.text == '😊🎲 Weird sentence':
            bot.send_message(message.chat.id, str(s.sentence()))
        elif message.text == '😊 How are you?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Good", callback_data='good')
            item2 = types.InlineKeyboardButton("Bad", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'I am fine, how about you?', reply_markup=markup)

        elif message.text == '🎲 Random Phrase':

            var = bot.send_message(message.chat.id, RandomQuotes.capital_lettered_quotes())



        else:
            bot.send_message(message.chat.id, 'Speechless 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Awesome 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'It happens 😢')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="OK, I understand",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Test Message")

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
