import random
import telebot
from telebot import types  # для указание типов

API_TOKEN = "<bot_token>"

bot = telebot.TeleBot(API_TOKEN)

rock = "🗿"
scissors = "✂️"
paper = "📄"


# randomize bot choice
def get_bot_choice():
    choices = [rock, scissors, paper]
    bot_choice = random.choice(choices)
    return bot_choice


# determine the winner
def determine_winner(user_choice, bot_choice):
    if user_choice == bot_choice:
        return "Ничья"
    elif (
        (user_choice == rock and bot_choice == scissors)
        or (user_choice == scissors and bot_choice == paper)
        or (user_choice == paper and bot_choice == rock)
    ):
        return "Вы выиграли"
    else:
        return "Компьютер выиграл"


# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(rock)
    btn2 = types.KeyboardButton(scissors)
    btn3 = types.KeyboardButton(paper)
    markup.add(btn1, btn2, btn3)
    bot.reply_to(
        message,
        text=' Добро пожаловать в игру: "Камень, ножницы, бумага".\n\nВыберите соответствующую кнопку, чтобы сделать ход.'.format(
            message.from_user
        ),
        reply_markup=markup,
    )


# players turn
@bot.message_handler(content_types=["text"])
def func(message):
    if message.text == rock or scissors or paper:
        user_choice = message.text
        bot_choice = get_bot_choice()
        result = determine_winner(user_choice, bot_choice)
        bot.send_message(
            message.chat.id,
            text=f"Ваш выбор: {user_choice}.\nВыбор компьютера: {bot_choice}.\n\n{result}!",
        )
    else:
        bot.send_message(message.chat.id, text="Пожалуйста, выберите один из вариантов")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling(timeout=99999, skip_pending=True)
