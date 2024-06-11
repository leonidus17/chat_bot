import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from random import randint
import requests
from aiogram.types import ReplyKeyboardRemove, \
    KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

word = ['слово', 'крыша', 'чашка', 'доска', 'чехол', 'мышка', 'труба', 'дзюдо', 'байка', 'нефть', 'мазут', 'сырьё',
        'шахта', 'уголь', 'химия', 'капля', 'масло', 'дубай', 'бутан', 'акциз', 'битум', 'бурав', 'дебит', 'рынок',
        'связь', 'рубль', 'наука', 'объём', 'фирма', 'завод', 'успех', 'сфера', 'товар', 'поиск', 'налог', 'доход',
        'труба', 'спорт', 'почва', 'марка', 'обмен', 'спрос', 'смесь', 'сосуд', 'проба', 'насос', 'факел', 'обмен',
        'земля', 'биржа', 'исток', 'напор', 'балка', 'каска', 'баржа', 'китай', 'ливия', 'бренд', 'лицей', 'охват','норма']



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

button1 = '/start_game'
help_button = '/help'
stickers_button = '/get_stickers'
main_kb = ReplyKeyboardMarkup([[button1, help_button, stickers_button]], resize_keyboard=True)

stop_button = '/stop'
stop_kb = ReplyKeyboardMarkup([[stop_button]], resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать в игру '5 букв'!\nЕсли вы хотите начать игру, нажмите на кнопку /start_game\nЕсли вы хотите получить информацию по игре, воспользуйтесь /help\nЕсли вы хотите получить стикеры, нажмите /get_stickers",
                                   reply_markup=main_kb)
    main_dict[update.effective_chat.id] = {'have_stickers': False, 'last_command': '/start',
                                           'game': {'attempt_count': 0, 'otvet': ['*', '*', '*', '*', '*'],
                                                    'guess_word': ' ', 'game_in_progress': False}}



async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in main_dict:
        main_dict[update.effective_chat.id] = {'have_stickers': False, 'last_command': '/start_game',
                                               'game': {'attempt_count': 0, 'otvet': ['*', '*', '*', '*', '*'],
                                                        'guess_word': ' ',
                                                        'game_in_progress': True}}
    main_dict[update.effective_chat.id]['game']['otvet'] = ['*', '*', '*', '*', '*']
    if main_dict[update.effective_chat.id]['game']['attempt_count'] > 0:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="У вас уже есть начатая сессия\n Напишите слово длиной 5 буквой")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Хорошо, что вы решили поиграть в нашу игру! Введите слово длиной 5 букв",reply_markup=stop_kb)

    main_dict[update.effective_chat.id]['last_command'] = '/start_game'
    main_dict[update.effective_chat.id]['game']['game_in_progress'] = True
    main_dict[update.effective_chat.id]['game']['attempt_count'] += 1
    main_dict[update.effective_chat.id]['game']['guess_word'] = word[randint(0, len(word) - 1)]
    main_dict[update.effective_chat.id]['game']['attempt_count'] = 0



async def igra(update: Update, context: ContextTypes.DEFAULT_TYPE):

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

        if len(dogadka) == 5 and b['def'] != []:
            main_dict[update.effective_chat.id]['game']['attempt_count'] += 1
            otvet_proverka = dogadka
            dogadka = list(dogadka)
            for i in range(len(dogadka)):
                if dogadka[i] in main_dict[update.effective_chat.id]['game']['guess_word']:
                    if dogadka[i] == main_dict[update.effective_chat.id]['game']['guess_word'][i]:
                        dogadka[i] = f'<b><u>{dogadka[i].upper()}</u></b>'
                    else:
                        dogadka[i] = f'<b>{dogadka[i].upper()}</b>'
            if otvet_proverka == main_dict[update.effective_chat.id]['game']['guess_word']:
                text_result = 'Поздравляем. Вы прошли игру!!😎\nВот столько попыток у вас ушло на это: ' + \
                              str(main_dict[update.effective_chat.id]['game']['attempt_count'])
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=preob(dogadka) + '\n' + text_result, parse_mode="HTML",
                                               reply_markup=main_kb)
                main_dict[update.effective_chat.id]['game']['game_in_progress'] = False
                main_dict[update.effective_chat.id]['game']['attempt_count'] = 0
            elif main_dict[update.effective_chat.id]['game']['attempt_count'] == 6:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text='К сожалению, вы проиграли😢\nЗагаданное слово было: ' +
                                                    main_dict[update.effective_chat.id]['game'][
                                                        'guess_word'] + '\nПопробуйте ещё раз', reply_markup = main_kb)
                main_dict[update.effective_chat.id]['game']['game_in_progress'] = False
                main_dict[update.effective_chat.id]['game']['attempt_count'] = 0
                return
            else:
                text_result = 'Введите ещё одно слово длиной 5 букв.\nУ вас осталось столько попыток чтобы отгадать ' \
                              'слово: ' + str(6 - main_dict[update.effective_chat.id]['game']['attempt_count'])
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=preob(dogadka) + '\n' + text_result, parse_mode="HTML", reply_markup = main_kb)





        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Вы ввели слово неправильной длины или такого слова не существует')


    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Я не понимаю, что вы хотите сделать. Если вы хотите начать игру, напишите /start_game')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Суть игры такова: компьютер загадывает слово длиной 5 букв, а пользователь должен вводить слова такой же длины, чтобы компьютер сказал вам, какие буквы написанного слова находятся на таком же месте в загаданном слове, а какие буквы есть в загаданном слове, но не на своём месте.\nБуквы, которые находятся на своём месте из загаданного слова будут выделяться жирным цветом, а также подчёркиваться, а буквы, которые находятся в загаданном слове, но не своём месте, будут выделяться жирным цветом')


async def get_stickers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Держите!\nhttps://t.me/addstickers/Coshki_krytie')


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if main_dict[update.effective_chat.id]['game']['game_in_progress']:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Вы завершили игру.',reply_markup = main_kb)
        main_dict[update.effective_chat.id]['game']['game_in_progress'] = False
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Эта команда работает только во время начатой игры')


if __name__ == '__main__':
    application = ApplicationBuilder().token('7476208184:AAHa1qSmJT2qtB2i8cql54NYX44peePVjVU').build()

    start_handler = CommandHandler('start', start)
    start_game_handler = CommandHandler('start_game', start_game)
    help_handler = CommandHandler('help', help)
    stickers_handler = CommandHandler('get_stickers', get_stickers)
    stop_handler = CommandHandler('stop', stop)
    igra_handler = MessageHandler(filters.TEXT, igra)

    application.add_handler(start_game_handler)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(stickers_handler)
    application.add_handler(stop_handler)
    application.add_handler(igra_handler)
    application.run_polling()
