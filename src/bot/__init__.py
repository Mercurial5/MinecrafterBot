from telebot import TeleBot, custom_filters
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.states import States
from config import BOT_TOKEN
from api import API

bot = TeleBot(BOT_TOKEN)
api = API()

min_name_length = 4
max_name_length = 12


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Villagers", callback_data="show_villagers"),
               InlineKeyboardButton("Villagers-Slaves", callback_data="show_slaves"),
               InlineKeyboardButton("Diamonds", callback_data="show_diamonds"),
               InlineKeyboardButton("Leader Board", callback_data="show_board"))

    return markup


@bot.message_handler(commands=['start'])
def greeting(message: Message):
    user_exist = api.is_user_exist(message.from_user.id)

    if user_exist:
        bot.send_message(message.chat.id, "Hello there!\n"
                                          "What would you like to check?", reply_markup=gen_markup())
    else:
        bot.send_message(message.chat.id, "Hi! It seems that you are new here!\n"
                                          "So,let's firstly introduce your self.\n"
                                          "How I can call you?")
        bot.set_state(message.from_user.id, States.enter_name)


@bot.message_handler(commands=['key'])
def get_hash(message: Message):
    key_json = api.generate_key(message.from_user.id)

    creation_date = key_json['created']
    key = key_json['key']

    if not key:
        bot.send_message(message.chat.id, "There is no such user.")
    else:
        bot.send_message(message.chat.id, f"The date of creation of this key is: {creation_date}\n"
                                          f"Here is your key: {key}\n"
                                          f"This key will be available only for one hour.\n"
                                          f"Please use it as soon as possible.")


@bot.message_handler(state=States.enter_name)
def enter_name(message: Message):
    name = message.text

    if len(name) < min_name_length or len(name) > max_name_length:
        bot.send_message(message.chat.id, "I'm sorry, we're a simple people and I don't think we can remember too "
                                          "short or long a name. I think from 4 to 12 letters will be okay.\n"
                                          "How again we can call you?")
        bot.set_state(message.from_user.id, States.enter_name)
    else:
        response = api.create_user(name, message.from_user.id)
        print(response)

        if response['status']:
            bot.send_message(message.chat.id, "Oh! Such a good name!\n"
                                              f"Nice to meet you {name}!")
        else:
            bot.send_message(message.chat.id, "Sorry, it seems that that name is already taken.\n"
                                              "Please choose another one.")
            bot.set_state(message.from_user.id, States.enter_name)


@bot.message_handler(func=lambda call: True)
def show_info(callback: CallbackQuery):
    info = api.get_user_info(callback.from_user.id)

    if callback.data == "show_villagers":
        bot.send_message(callback.chat_instance, f"Now you have {info['villagers']}villager.")
    elif callback.data == "show_slaves":
        bot.send_message(callback.chat_instance, f"Now you have {info['slaves']}villager.")
    elif callback.data == "show_diamonds":
        bot.send_message(callback.chat_instance, f"Now you have {info['diamonds']}villager.")
    else:
        bot.send_message(callback.chat_instance, f"Here is the score board:\n"
                                                 f"{info['board']}")


bot.add_custom_filter(custom_filters.StateFilter(bot))
