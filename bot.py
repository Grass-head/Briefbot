
from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

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
