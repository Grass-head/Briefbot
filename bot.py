
from telegram.ext import Filters, Updater
from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, RegexHandler

from handlers import *
import settings
import logging

def main():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        filename='bot.log')
    
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", welcome_user))

    conv_handler = ConversationHandler(
		entry_points=[CallbackQueryHandler(create_brief)],

        states={

            NAME: [MessageHandler(Filters.text, brief_name)],

            QUESTIONS: [
                        CallbackQueryHandler(enter_questions, pattern="^Введите вопрос$"),
                        MessageHandler(Filters.text, brief_questions),
                        CallbackQueryHandler(end_questions, pattern="^Вы завершили опрос$")
                        ],
            DONE: [CallbackQueryHandler(brief_check_result, pattern="^Вы запросили текущий опрос$"),
                    CallbackQueryHandler(brief_list, pattern="^Вы запросили список ваших опросов$")
            ]
        },

        fallbacks=[MessageHandler(Filters.video | Filters.photo | Filters.document, dontknow)]
    )
    dp.add_handler(conv_handler)

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
