# extension.py
# Пункт задания 12. Все классы спрятать в файле extensions.py.
# =========================================
#               Игорь Ковалев igorkov6@gmail.com
# SkillFactory: FPW-2.0
# Модуль:       C5 Итоговый проект по ООП
#               ИТОГОВЫЙ ПРОЕКТ 5.6 (PJ-02)
# project:      telegram bot
# interpreter:  Python 3.8
# ide:          PyCharm 2022.1
# =========================================

import telebot
import requests
import json
from config import Config


# =========================================
# класс запроса курса
# =========================================
class Crypto:

    # -----------------------------------------
    # запрос курса
    # -----------------------------------------
    # Пункт задания 10. Для отправки запросов к API описать класс со статическим методом get_price(),
    # который принимает три аргумента и возвращает нужную сумму в валюте:
    # - имя валюты, цену, на которую надо узнать, — base;
    # - имя валюты, цену, в которой надо узнать, — quote;
    # - количество переводимой валюты — amount.
    @staticmethod
    def get_price(quote_code, base_code, amount):

        # сформировать get запрос
        get_request = f'?fsym={quote_code}&tsyms={base_code}'

        # Запросить курс
        # Пункт задания 6. Для получения курса валют необходимо использовать API
        # и отправлять к нему запросы с помощью библиотеки Requests.
        rate = requests.get(Config().host + get_request).content

        # Парсинг ответа
        # Пункт задания 7. Для парсинга полученных ответов использовать библиотеку JSON.
        price = round(json.loads(rate)[base_code] * amount, 5)

        # сформировать текст ответа
        return f'{amount} {quote_code} = {price} {base_code}\n'


# =========================================
# класс исключений
# =========================================
class APIException(Exception):

    # Пункт задания 8. При ошибке пользователя (например, введена неправильная или несуществующая валюта,
    # или неправильно введено число) вызывать собственно написанное исключение APIException
    # с текстом пояснения ошибки.
    def __init__(self, inline):
        self.text = inline


# =========================================
# контроль ошибок входной строки
# =========================================
class ErrorHandler:

    @staticmethod
    def check(values):

        if len(values) < 3:
            raise APIException('недостаточно параметров')

        if len(values) > 3:
            raise APIException('слишком много параметров')

        # попытка исправить возможные ошибки
        # искать соответствие первых трёх символов
        for key in Config().currency_keys:
            for i in [0, 1]:
                if values[i][:3] == key[:3]:
                    values[i] = key

        if not values[0] in Config().currency_keys:
            raise APIException(f'валюта {values[0]} не поддерживается')

        if not values[1] in Config().currency_keys:
            raise APIException(f'валюта {values[1]} не поддерживается')

        if values[0] == values[1]:
            raise APIException('одинаковые валюты')

        try:
            x = float(values[2])
        except ValueError:
            raise APIException(f'{values[2]} - не числовое значение')

        if x <= 0:
            raise APIException(f'{values[2]} - значение должно быть положительным')


# =========================================
# класс приложения
# =========================================
class App:

    # -----------------------------------------
    # начать работу
    # -----------------------------------------
    @staticmethod
    def run():

        # Создать бот
        # Пункт задания 2. При написании бота необходимо использовать библиотеку pytelegrambotapi.
        bot = telebot.TeleBot(Config().token)

        # Обработка команд start и help
        # Пункт задания 4. При вводе команды /start или /help пользователю выводятся инструкции по применению бота.
        @bot.message_handler(commands=['start', 'help'])
        def start_help(message):
            bot.reply_to(message, 'Введите через пробел\nвалюта1 валюта2 сумма\nСписок доступных валют: /values')

        # Обработка команды values
        # Пункт задания 5. При вводе команды /values должна выводиться информация
        # о всех доступных валютах в читаемом виде.
        @bot.message_handler(commands=['values'])
        def values(message):
            txt = 'Доступные валюты:'
            for key in Config().currency_keys:
                txt = '\n'.join((txt, key))
            bot.reply_to(message, txt)

        # обработка запросов
        @bot.message_handler(content_types=['text'])
        def convert(message):

            # строка ответа боту
            text = ''

            try:
                # получить данные запроса от бота
                value_list = message.text.lower().split(' ')

                # проверка корректности введенных данных
                ErrorHandler.check(value_list)

                # Получить значения из списка введенных данных запроса
                # Пункт задания 3. Человек должен отправить сообщение боту в виде
                # <имя валюты, цену которой он хочет узнать>
                # <имя валюты, в которой надо узнать цену первой валюты>
                # <количество первой валюты>.
                quote_key, base_key, amount = value_list[0], value_list[1], float(value_list[2])

                # выполнить прямой запрос курса и получить строку ответа
                text = Crypto.get_price(Config().currency_code(quote_key), Config().currency_code(base_key), amount)

                # выполнить инверсный запрос курса и получить строку ответа
                text += Crypto.get_price(Config().currency_code(base_key), Config().currency_code(quote_key), amount)

            except APIException as e:

                # Сформировать строку ответа об ошибке
                # Пункт задания 9. Текст любой ошибки с указанием типа ошибки
                # должен отправляться пользователю в сообщения.
                text = f'ошибка:\n{e.text}\nповторите запрос'

            finally:

                # Отправить ответ боту
                # Пункт задания 1. Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
                bot.reply_to(message, text)

        # начать прием данных от бота
        bot.polling()

# =========================================
