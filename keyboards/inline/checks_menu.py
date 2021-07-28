from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.project import DATA


def choice_checks_menu(chat_id):
    choice_menu = InlineKeyboardMarkup()
    choice_menu.add(
        InlineKeyboardButton(text='Типовой поликлинический процесс из БАРСа', callback_data='typal_checks_bars'))
    if chat_id not in DATA:
        return "Chat ID не найден!"

    if 'remote_profiles' in DATA[chat_id]:
        choice_menu.add(
            InlineKeyboardButton(text='Типовой поликлинический процесс из ЦОДа', callback_data='typal_checks_cod'))
    return choice_menu


def choice_scripts_menu(chat_id):
    checks_menu = InlineKeyboardMarkup()
    if chat_id not in DATA:
        return "Chat ID не найден!"
    for script_name in DATA[chat_id]['local_profiles']:
        if script_name.endswith('_typal.jmx'):
            text = 'На балансировщике'
            call_back = f"{script_name}_bar"
            checks_menu.add(InlineKeyboardButton(text=text, callback_data=call_back))
        elif 'node' in script_name:
            number_node = [i for i in script_name if i.isdigit()][0]
            text = f'На ноде {number_node}'
            call_back = f"{script_name}_bar"
            checks_menu.add(InlineKeyboardButton(text=text, callback_data=call_back))
    return checks_menu
