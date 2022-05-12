# config.py
# Пункт задания 11. Токен Telegram-бота хранить в специальном конфиге (можно использовать .py файл).
# =========================================
#               Игорь Ковалев igorkov6@gmail.com
# SkillFactory: FPW-2.0
# Модуль:       C5 Итоговый проект по ООП
#               ИТОГОВЫЙ ПРОЕКТ 5.6 (PJ-02)
# project:      telegram bot
# interpreter:  Python 3.8
# ide:          PyCharm 2022.1
# =========================================

# =========================================
# класс конфигурации
# =========================================
class Config:

    # -----------------------------------------
    # локальные константы
    # -----------------------------------------

    # токен бота
    _TOKEN = '5339735538:AAF9FokoFA3b7B07z2N44VC4akvF3e0L7_Q'

    # хост API
    _HOST = 'https://min-api.cryptocompare.com/data/price'

    # поддерживаемые валюты
    _CURRENCIES = {
        'биткоин': 'BTC',
        'btc': 'BTC',
        'эфирион': 'ETH',
        'eth': 'ETH',
        'доллар': 'USD',
        'usd': 'USD',
        'евро': 'EUR',
        'eur': 'EUR',
        'рубль': 'RUB',
        'rub': 'RUB',
        'гривна': 'UAH',
        'uah': 'UAH',
        'лира': 'TRY',
        'try': 'TRY'
    }

    # -----------------------------------------
    # получить токен
    # -----------------------------------------
    @property
    def token(self):
        return self._TOKEN

    # -----------------------------------------
    # получить хост
    # -----------------------------------------
    @property
    def host(self):
        return self._HOST

    # -----------------------------------------
    # получить перечень всех поддерживаемых валют
    # -----------------------------------------
    @property
    def currency_keys(self):
        return self._CURRENCIES.keys()

    # -----------------------------------------
    # возвратить код валюты
    # -----------------------------------------
    def currency_code(self, key):
        return self._CURRENCIES[key]

# =========================================
