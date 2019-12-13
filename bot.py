from telegram.ext import Updater

import settings

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()