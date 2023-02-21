from telebot.handler_backends import State, StatesGroup


class States(StatesGroup):
    enter_name = State()
