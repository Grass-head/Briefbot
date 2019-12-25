
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler, Filters, ConversationHandler

def welcome_user(bot, update):
	text_greet = 'Привет! Этот бот поможет вам составить бриф. Сформулируйте и отправьте боту вопросы брифа и получите ссылку - приглашение. Эту ссылку нужно передать клиенту. 		  Он пройдет бриф и бот отправит вам на почту результат.'
	update.message.reply_text(text_greet)
	keyboard = [[InlineKeyboardButton("Создать опрос", callback_data='Введите название опроса')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('Для продолжения нажмите:', reply_markup=reply_markup)

NAME, QUESTIONS = range(2)

def create_brief(bot, update):
    query = update.callback_query
    query.edit_message_text(text="{}".format(query.data))
    return NAME

def brief_name(bot, update):
	keyboard = [[InlineKeyboardButton("Вопрос", callback_data='Введите вопрос')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	user_text = update.message.text
	update.message.reply_text('Хорошая работа! Название "{}" записано'.format(user_text))
	update.message.reply_text("Чтобы ввести новый вопрос нажмите кнопку:", reply_markup=reply_markup)
	return QUESTIONS

def enter_questions(bot, update):
	query = update.callback_query
	query.edit_message_text(text="{}".format(query.data))
	return QUESTIONS

def subject_text(bot, update):
	update.message.reply_text("Отлично! Теперь перейдем к главному!")
	update.message.reply_text("Какое количество вопросов вы планируете создать?")
	return QUESTIONS

def brief_questions(bot, update):
	keyboard = [[InlineKeyboardButton("Вопрос", callback_data='Введите вопрос')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	user_text = update.message.text
	update.message.reply_text('Отлично! Вопрос "{}" сохранен'.format(user_text))
	update.message.reply_text("Если не хотите продолжать введите /stop. Чтобы ввести следующий вопрос нажмите кнопку:", reply_markup=reply_markup)
	return QUESTIONS

def brief_stop(bot, update):
    update.message.reply_text('Спасибо за ваш труд! До скорой встречи!')
    return ConversationHandler.END

def dontknow(bot,update):
	update.message.reply_text("Не понимаю. Следуйте, пожалуйста инструкции")






