from telegram.ext import Updater, CommandHandler

import settings

def greeting(bot, update):
    text_gr = 'Привет! Этот бот поможет вам составить бриф. Сформулируйте и отправьте боту вопросы брифа и получите ссылку - приглашение. Эту ссылку нужно передать клиенту. Он пройдет бриф и бот отправит вам на почту результат.'
    update.message.reply_text(text_gr)
    personal = 'Введите свои персональные данные через запятую (ф.и.о, название организации, должность, e-mail).'
    update.message.reply_text(personal)

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greeting))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()