import telebot
from extensions import APIException , CurrencyConverter, currencies


# токен вашего телеграм-бота
TOKEN = "токен вашего телеграм-бота"


bot = telebot.TeleBot(TOKEN)
# обработчик команд
@bot.message_handler(commands=['start', 'help'])
def greeting(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}."
                                      " Я могу сообщать курсы валют\n"
                                      "Для получения списка валют введи команду /values")

# обработчик команды "показать список валют"
@bot.message_handler(commands=['values'])
def greeting(message):
    currenies = ''
    for key in currencies.keys():
        currenies += ' - ' + key + '\n'
    bot.send_message(message.chat.id, f"Список валют:\n {currenies}\n\
Запрос должен быть в виде 3-х слов с пробелами :\n"
                                      "<валюта1> <валюта2> <количество валюты1>")

# обработчик сообщения
@bot.message_handler(content_types=['text'])
def handle_message(message):
    try:
        params = message.text.split()
        if len(params) != 3:
            print(params)
            raise APIException('Неправильное количество параметров')
        quote, base, amount = params
        answer=CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id, answer)


# запускаем бота
bot.polling(none_stop=True)
