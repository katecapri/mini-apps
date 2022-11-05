"""
Telegram bot where you can play hangman.
The /start command opens a new word.
For the next word, you need to finish the previous round (guess the word or not guess in 11 attempts).
"""

import random

import telebot
from hangman_token import TOKEN

bot = telebot.TeleBot(TOKEN)

word_list = ['ВИСЕЛИЦА', 'ФИКЦИЯ' 'ВДОХНОВЕНИЕ', 'БАЛЬЗАМ', 'ХАРАКТЕР', 'СКВОРЕЧНИК', 'ДРОЖЖИ', 'ФОРМУЛЯР', 'ВРАЩЕНИЕ',
             'МАГНИТОФОН', 'КОНТРСТРЕЛЬБА', 'ДЛИННОШЕЕЕ', 'ТРИГОНОМЕТРИЯ', 'ПЕДАНТИЧНОСТЬ', 'ПРОКРАСТИНАЦИЯ']
word_list_for_gamers = {}
letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П',
           'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ь', 'Ы', 'Ъ', 'Э', 'Ю', 'Я']
n = {}  # первая цифра в названии картинки + количество промахов
m = {}  # вторая цифра в названии картинки. 0- череда отгадываний прервана
accessibility_of_letters = {}
hidden_word = {}
possibility_of_starting_for_gamers = {}
s = {}  # пасхалочка №1
h = {}  # пасхалочка №2


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Чтобы начать отгадывать новое слово, нужно ввести "/start".\n'
                                      'Если отгадывание уже начато, нужно ввести одну русскую букву и следовать'
                                      ' дальнейшим подсказкам.')


@bot.message_handler(commands=['start'])
def start(message):
    gamer_id = message.from_user.id
    if gamer_id not in possibility_of_starting_for_gamers:
        new_gamer(gamer_id)
    if possibility_of_starting_for_gamers[gamer_id]:
        if word_list_for_gamers[gamer_id]:
            possibility_of_starting_for_gamers[gamer_id] = False
            hidden_word[gamer_id] = random.choice(word_list_for_gamers[gamer_id])
            word_list_for_gamers[gamer_id].remove(hidden_word[gamer_id])
            accessibility_of_letters[gamer_id] = dict.fromkeys(letters, True)
            n[gamer_id] = 0
            m[gamer_id] = 0
            s[gamer_id] = 0
            h[gamer_id] = 0
            for i in range(len(hidden_word[gamer_id])):
                if hidden_word[gamer_id][i] == hidden_word[gamer_id][0] or \
                        hidden_word[gamer_id][i] == hidden_word[gamer_id][len(hidden_word[gamer_id]) - 1]:
                    accessibility_of_letters[gamer_id][hidden_word[gamer_id][i]] = False
            send_photo_template_and_available_letters(message)
        else:
            bot.send_message(message.chat.id, 'Игра пройдена! :) Благодарю за проявленный интерес. '
                                              'Пока что здесь больше нет ничего интересного для тебя.')
    else:
        bot.send_message(message.chat.id, 'Чтобы взяться за новое, нужно сперва окончить старое ;)')


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    gamer_id = message.from_user.id
    if gamer_id not in possibility_of_starting_for_gamers:
        new_gamer(gamer_id)
    if not possibility_of_starting_for_gamers[gamer_id]:
        if len(message.text) > 1 or message.text.upper() not in accessibility_of_letters[gamer_id].keys():
            h[gamer_id] = 0
            if s[gamer_id] in [0, 1, 2]:
                bot.send_message(message.chat.id, 'Введи, пожалуйста, одну русскую букву.')
                s[gamer_id] += 1
            elif s[gamer_id] == 3:
                bot.send_message(message.chat.id, 'Введи, пожалуйста, одну РУССКУЮ БУКВУ.')
                s[gamer_id] += 1
            elif s[gamer_id] == 4:
                bot.send_message(message.chat.id, 'Введи, ПОЖАЛУЙСТА, одну РУССКУЮ БУКВУ.')
                s[gamer_id] += 1
            else:
                bot.send_message(message.chat.id, 'Ну сколько можно... Я ж хочу сыграть с тобой в игру...')
                s[gamer_id] = 0
        elif accessibility_of_letters[gamer_id][message.text.upper()]:  # введена буква из доступных
            s[gamer_id] = 0
            h[gamer_id] = 0
            accessibility_of_letters[gamer_id][message.text.upper()] = False
            if message.text.upper() in hidden_word[gamer_id]:  # буква есть в слове
                bot.send_message(message.chat.id, 'Такая буква есть в слове!')
                m[gamer_id] = 1
            else:  # промах - буква выбрана корректно, но ее нет в слове
                bot.send_message(message.chat.id, 'Увы, такой буквы нет :(')
                n[gamer_id] += 1
                m[gamer_id] = 0
            if n[gamer_id] < 11:
                send_photo_template_and_available_letters(message)
                if check_win(gamer_id):
                    possibility_of_starting_for_gamers[gamer_id] = True
                    bot.send_message(message.chat.id, 'Юх-хууу! Слово отгадано!')
            else:  # game over
                bot.send_message(message.chat.id, 'Попыток больше нет, это конец. Придется открыть для себя новое'
                                                  ' начало :)\n'
                                                  'P.S. Загаданное слово было: ' + hidden_word[gamer_id].lower() + '.')
                possibility_of_starting_for_gamers[gamer_id] = True
        else:
            s[gamer_id] = 0
            if h[gamer_id] in [0, 1, 2]:
                bot.send_message(message.chat.id, 'Буква уже свое отыграла. Пожалуйста, выбери букву из доступных.')
                h[gamer_id] += 1
            elif h[gamer_id] == 3:
                bot.send_message(message.chat.id, 'Буква уже свое отыграла. Пожалуйста, выбери букву из ДОСТУПНЫХ.')
                h[gamer_id] += 1
            elif h[gamer_id] == 4:
                bot.send_message(message.chat.id, 'Буква уже свое отыграла. ПОЖАЛУЙСТА, выбери букву из ДОСТУПНЫХ.')
                h[gamer_id] += 1
            else:
                bot.send_message(message.chat.id, 'Может хватит? Мы здесь поиграть собрались...')
                h[gamer_id] = 0
            m[gamer_id] = 1
            send_photo_template_and_available_letters(message)
    else:
        bot.send_message(message.chat.id, 'Введи "/start", чтобы начать новую игру.')


@bot.message_handler(content_types=['photo', 'audio', 'document', 'sticker', 'video', 'location', 'contact', 'voice'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Ооооочень классно, но мы здесь для другого дела :)')


def new_gamer(gamer_id):
    possibility_of_starting_for_gamers[gamer_id] = True
    word_list_for_gamers[gamer_id] = [word for word in word_list]
    accessibility_of_letters[gamer_id] = {}


def show_hidden_word_template(gamer_id):
    hidden_word_template = ''
    for i in range(len(hidden_word[gamer_id])):
        if accessibility_of_letters[gamer_id][hidden_word[gamer_id][i]]:
            hidden_word_template += '_ '
        else:
            hidden_word_template += hidden_word[gamer_id][i] + ' '
    return hidden_word_template


def show_available_letters_string(gamer_id):
    available_letters_string = ''
    for key in accessibility_of_letters[gamer_id]:
        if accessibility_of_letters[gamer_id][key]:
            available_letters_string += key + ' '
    return 'Доступные буквы: ' + available_letters_string


def get_photo(gamer_id):
    photo_path = f'pictures\\{n[gamer_id]}.{m[gamer_id]}.jpg'
    return open(photo_path, 'rb')


def send_photo_template_and_available_letters(message):
    bot.send_photo(message.chat.id, get_photo(message.from_user.id))
    bot.send_message(message.chat.id, show_hidden_word_template(message.from_user.id))
    bot.send_message(message.chat.id, show_available_letters_string(message.from_user.id))


def check_win(gamer_id):
    letters_open = 0
    for i in range(len(hidden_word[gamer_id])):
        if not accessibility_of_letters[gamer_id][hidden_word[gamer_id][i]]:
            letters_open += 1
    if letters_open == len(hidden_word[gamer_id]):
        return True


bot.polling(none_stop=True)
