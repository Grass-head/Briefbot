
from telegram.ext import Updater, CommandHandler

from handlers import *
import settings


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", welcome_user))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()