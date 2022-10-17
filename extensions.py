import requests
import json

# словарь валют
currencies = {
    'евро': 'EUR',
    'доллар': 'USD',
    'фунт': 'GBP',
    'рубль': 'RUB',
    'франк': 'CHF',
    'йена': 'JPY',
}
# ваш ключ API в currate.ru для получения курса
API='02450221b8ce2cc2346765bb81e4af55'

# класс исключений при конвертации валют
class APIException (Exception):
    pass

# класс для конвертации валют
class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        # валюты совпадают?
        if quote == base:
            raise APIException ('Неправильное количество параметров')

        # валюты в списке?
        try:
            curr_from = currencies[quote]
        except KeyError:
            raise APIException (f'Валюта "{quote}" не найдена')

        try:
            curr_to = currencies[base]
        except KeyError:
            raise APIException (f'Валюта "{base}" не найдена')

        # количество валидное?
        try:
            lot = float(amount)
        except ValueError:
            raise APIException (f'Неверное количество "{amount}"')

        # соберем имя валютной пары
        pair=curr_from+curr_to
        try:
            request=f'https://currate.ru/api/?get=rates&pairs={pair}&key={API}'
            r=requests.get(request)
        except Exception as e:
            print(f'запрос {request}')
            print(f'ответ: {e}')
            raise APIException (f'Не удалось получить курс "{pair}"')
        #print(r.content)
        # получим курс для валютной пары pair
        rate=json.loads(r.content)['data'][pair]
        try:
            total = float(rate)*lot
        except ValueError as e:
            raise APIException (f'Невалидное значение курса для "{pair}":rate')
        return f'{amount} {curr_from} стоит {total} {curr_to}'
