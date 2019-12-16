from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def welcome_user(bot, update):
    text_gr = 'Привет! Этот бот поможет вам составить бриф. Сформулируйте и отправьте боту вопросы брифа и получите ссылку - приглашение. Эту ссылку нужно передать клиенту. Он пройдет бриф и бот отправит вам на почту результат.'
    update.message.reply_text(text_gr)
    keyboard = [[InlineKeyboardButton("Создать опрос", callback_data='1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Для продолжения нажмите:', reply_markup=reply_markup)