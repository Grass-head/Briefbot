
from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

from handlers import *

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}


def main():
    mybot = Updater('590986898:AAHD96EvOQ5x-QUeazYZh-HkR-Sg0m0Prf8', request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", welcome_user))

    conv_handler = ConversationHandler(
		entry_points=[CallbackQueryHandler(create_brief)],

        states={

            NAME: [MessageHandler(Filters.text, brief_name)],

            QUESTIONS: [
                        CallbackQueryHandler(enter_questions),
                        MessageHandler(Filters.text, brief_questions)
                        ],

            DONE:[CallbackQueryHandler(enter_questions)]
        },

        fallbacks=[MessageHandler(Filters.video | Filters.photo | Filters.document, dontknow)]
    )

    dp.add_handler(conv_handler)
 	
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
