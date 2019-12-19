
from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

from handlers import *
import settings


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", welcome_user))
    dp.add_handler(CallbackQueryHandler(button))

    conv_handler = ConversationHandler(
		entry_points=[RegexHandler('^(Создать опрос)$', create_brief)],

        states={

            TITLE: [MessageHandler(Filters.text, title_text)],

            SUBJECT: [MessageHandler(Filters.text, subject_text),
                    CommandHandler('skip', skip_subject_text)],

            QUESTIONS: [MessageHandler(Filters.text, questions_text)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
 	
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()