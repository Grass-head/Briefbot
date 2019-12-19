
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler, Filters, ConversationHandler

def welcome_user(bot, update):
	text_greet = 'Привет! Этот бот поможет вам составить бриф. Сформулируйте и отправьте боту вопросы брифа и получите ссылку - приглашение. Эту ссылку нужно передать клиенту. 		  Он пройдет бриф и бот отправит вам на почту результат.'
	update.message.reply_text(text_greet)
	keyboard = [[InlineKeyboardButton("Создать опрос", callback_data='Создать опрос')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('Для продолжения нажмите:', reply_markup=reply_markup)

def button(bot, update):
    query = update.callback_query
    query.edit_message_text(text="{}".format(query.data))


TITLE, SUBJECT, QUESTIONS = range(3)

def create_brief(bot, update):
    update.message.reply_text("Введите название брифа")
    return TITLE

def title_text(bot, update):
	text = update.message.text
	update.message.reply_text('Хорошая работа! Название "{}" записано'.format(text))
	update.message.reply_text("Теперь введите краткое описание брифа. Если не хотите делать описание - отправьте /skip")
	return SUBJECT

def subject_text(bot, update):
	update.message.reply_text("Отлично! Теперь перейдем к главному!")
	update.message.reply_text("Какое количество вопросов вы планируете создать?")
	return QUESTIONS

def skip_subject_text(bot, update):
	update.message.reply_text("Ок, описание это не самая важная часть в брифе. Перейдем к главному!")
	update.message.reply_text("Какое количество вопросов вы планируете создать?")
	return QUESTIONS

def questions_text(bot, update):
	qty = update.message.text
	count = 0
	if count < qty:
		for question in questions:
			update.message.reply_text("Введите вопрос")
			count += 1
	return ConversationHandler.END

def stop(bot, update):
    update.message.reply_text('Спасибо за ваш труд! До скорой встречи!')
    return ConversationHandler.END




