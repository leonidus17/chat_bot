import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode

from random import randint
import requests

word = ['слово', 'нефть', 'мазут', 'крыша', 'чашка', 'доска', 'чехол', 'мышка', 'труба', 'дзюдо', 'байка']


def preob(a: list):
    s = ''
    for i in range(len(a)):
        s += a[i]
        s += ' '
    return s


def convert_tuple(c_tuple):
    str = ''
    for i in c_tuple:
        str = str + i
    return str


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

main_dict = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать в игру '5 букв'!")
    main_dict[update.effective_chat.id] = {'have_stickers': False, 'last_command': '/start',
                                           'game': {'attempt_count': 0, 'otvet': ['*', '*', '*', '*', '*'],
                                                    'guess_word': ' ', 'game_in_progress': False}}
    print(update.effective_chat.id)


async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in main_dict:
        main_dict[update.effective_chat.id] = {'have_stickers': False, 'last_command': '/start_game',
                                               'game': {'attempt_count': 0, 'otvet': ['*', '*', '*', '*', '*'],
                                                        'guess_word': ' ',
                                                        'game_in_progress': True}}
    main_dict[update.effective_chat.id]['game']['otvet'] = ['*', '*', '*', '*', '*']
    if main_dict[update.effective_chat.id]['game']['attempt_count'] > 0:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="У вас уже есть начатая сессия, напишите слово длиной 5 буквой")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Хорошо, что вы решили поиграть в нашу игру! Введите слово длиной 5 букв")
    print(update.effective_chat.id)
    main_dict[update.effective_chat.id]['last_command'] = '/start_game'
    main_dict[update.effective_chat.id]['game']['game_in_progress'] = True
    main_dict[update.effective_chat.id]['game']['attempt_count'] += 1
    main_dict[update.effective_chat.id]['game']['guess_word'] = word[randint(0, len(word) - 1)]
    print(main_dict[update.effective_chat.id])


async def igra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_chat.id)
    print(update.effective_chat.id)

    if update.effective_chat.id not in main_dict:
        main_dict[update.effective_chat.id] = {'have_stickers': False, 'last_command': '/start_game',
                                               'game': {'attempt_count': 0, 'otvet': ['*', '*', '*', '*', '*'],
                                                        'guess_word': ' ',
                                                        'game_in_progress': False}}

    if main_dict[update.effective_chat.id]['game']['game_in_progress']:
        text_fin = ''
        dogadka = ''
        text_result = ''
        dogadka = update.message.text
        dogadka = dogadka.lower()

        a = requests.get(
            f"https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=dict.1.1.20240609T074810Z"
            f".1e88860b7b677d28.596c4c409f867db83c96cbd6973ffccf2db4e4f7&lang=ru-ru&text={dogadka}")
        b = a.json()

        print(b)
        print(dogadka)
        if len(dogadka) == 5 and b['def'] != []:
            dogadka = list(dogadka)
            for i in range(len(dogadka)):
                if dogadka[i] in main_dict[update.effective_chat.id]['game']['guess_word']:
                    if dogadka[i] == main_dict[update.effective_chat.id]['game']['guess_word'][i]:
                        dogadka[i] = f'<b><u>{dogadka[i].upper()}</u></b>'
                    else:
                        dogadka[i]= f'<b>{dogadka[i].upper()}</b>'
            if dogadka == main_dict[update.effective_chat.id]['game']['guess_word']:
                text_result = 'Поздравляем. Вы прошли игру!!😎'
            else:
                text_result = 'Введите ещё одно слово длиной 5 букв'
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=preob(dogadka)+ '\n'+ text_result, parse_mode="HTML")
            print(preob(dogadka))


        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Вы ввели слово неправильной длины или такого слова не существует')


    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Я не понимаю, что вы хотите сделать. Если вы хотите начать игру, напишите /start_game')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='В игре "5 букв" вам необходимо угадать загаданное слово, путём написания слов длинной 5 букв, и если буква из загаданного слова')


if __name__ == '__main__':
    application = ApplicationBuilder().token('7476208184:AAHa1qSmJT2qtB2i8cql54NYX44peePVjVU').build()

    start_handler = CommandHandler('start', start)
    start_game_handler = CommandHandler('start_game', start_game)
    igra_handler = MessageHandler(filters.TEXT, igra)

    application.add_handler(start_game_handler)
    application.add_handler(start_handler)
    application.add_handler(igra_handler)

    application.run_polling()
