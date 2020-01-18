
from telegram.ext import Filters, Updater
from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, RegexHandler

from handlers import *
import settings

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", welcome_user))

    conv_handler = ConversationHandler(
		entry_points=[CallbackQueryHandler(create_brief)],

        states={

            NAME: [MessageHandler(Filters.text, brief_name)],

            QUESTIONS: [
                        CallbackQueryHandler(enter_questions, pattern="^Введите вопрос$"),
                        CallbackQueryHandler(end_questions, pattern="^Вы завершили опрос$"),
                        MessageHandler(Filters.text, brief_questions)
                        ],

            DONE: [CallbackQueryHandler(brief_check_result, pattern="^Вы завершили опрос$")]
        },

        fallbacks=[MessageHandler(Filters.video | Filters.photo | Filters.document, dontknow)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(RegexHandler('^(Мои опросы)$', brief_list))


    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
