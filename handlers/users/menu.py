from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from funcs.jmeter import runJmeterFromBars, runJmeterFromCod
from funcs.reports import getReport
from keyboards.inline.checks_menu import choice_checks_menu, choice_scripts_menu
from loader import dp


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    # await message.delete()
    chat_id = str(message.chat.id)
    checks_menu = choice_checks_menu(chat_id)
    await message.answer("Меню проверок МИС:", reply_markup=checks_menu)


@dp.callback_query_handler(text='typal_checks_bars')
async def menu(call: CallbackQuery):
    await call.message.delete()
    choice_menu = choice_scripts_menu(str(call.message.chat.id), type='local')
    await call.message.answer("Типовой поликлинический процесс МИС из БАРСа", reply_markup=choice_menu)


@dp.callback_query_handler(text='typal_checks_cod')
async def menu(call: CallbackQuery):
    await call.message.delete()
    choice_menu = choice_scripts_menu(str(call.message.chat.id), type='remote')
    await call.message.answer("Типовой поликлинический процесс МИС из ЦОДа", reply_markup=choice_menu)


@dp.callback_query_handler(Text(endswith=".jmx_bar"))
async def runJmeterFRomBars(call: CallbackQuery):
    await call.message.delete()
    script_name = call.data[:-4]
    print(script_name)
    key = script_name.split('_')[1].lower()
    print(key)
    await call.message.answer("Запущен тест типового поликлинического процесса из БАРСа...")
    runJmeterFromBars(script_name, key)
    report = getReport(key)
    await call.message.answer(text=report)


@dp.callback_query_handler(Text(endswith=".jmx_cod"))
async def runJmeterFRomCod(call: CallbackQuery):
    await call.message.delete()
    script_name = call.data[:-4] # MED_SO_typal.jmx
    print(script_name)
    key = script_name.split('_')[1].lower()  # rso
    print(key)
    await call.message.answer("Запущен тест типового поликлинического процесса из ЦОДа...")
    report = runJmeterFromCod(str(call.message.chat.id), script_name, key)
    await call.message.answer(text=report)
