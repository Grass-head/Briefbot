from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup

from db import db, add_user, add_brief, add_question


def welcome_user(bot, update):
	user = add_user(db, update.effective_user)
	text_greet = 'Привет! Этот бот поможет вам составить бриф. Сформулируйте и отправьте боту вопросы брифа и получите ссылку - приглашение. Эту ссылку нужно передать клиенту. Он пройдет бриф и бот отправит вам на почту результат.'
	update.message.reply_text(text_greet)
	keyboard = [[InlineKeyboardButton("Создать опрос", callback_data='Введите название опроса')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('Для продолжения нажмите:', reply_markup=reply_markup)


NAME, QUESTIONS, DONE = range(3)


def create_brief(bot, update):
	query = update.callback_query
	query.edit_message_text(text="{}".format(query.data))
	return NAME


def brief_name(bot, update):
	brief = add_brief(db, update.effective_user, update.message)
	keyboard = [[InlineKeyboardButton("Вопрос", callback_data='Введите вопрос')],
	[InlineKeyboardButton("Завершить опрос", callback_data='Вы завершили опрос')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	user_text = update.message.text
	update.message.reply_text('Хорошая работа! Название "{}" записано'.format(user_text))
	update.message.reply_text("Чтобы продолжить нажмите одну из кнопок:", reply_markup=reply_markup)
	return QUESTIONS


def enter_questions(bot, update):
	query = update.callback_query
	query.edit_message_text(text="{}".format(query.data))
	print("продолжение опроса")
	return QUESTIONS 

def end_questions(bot, update):
	query = update.callback_query
	query.edit_message_text(text="{}".format(query.data))
	print("конец опроса")
	return DONE

def brief_questions(bot, update):
	question = add_question(db, update.message)
	keyboard = [[InlineKeyboardButton("Вопрос", callback_data='Введите вопрос')],
	[InlineKeyboardButton("Завершить опрос", callback_data='Вы завершили опрос')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	user_question = update.message.text
	update.message.reply_text('Отлично! Вопрос "{}" сохранен'.format(user_question), reply_markup=reply_markup)
	return QUESTIONS


def dontknow(bot, update):
	update.message.reply_text("Не понимаю. Следуйте, пожалуйста, инструкции")


def brief_check_result(bd, bot, effective_user, update):
	print("начало функции brief_check_result")
	my_keyboard = ReplyKeyboardMarkup(['Мои опросы'], one_time_keyboard=True)
	update.message.reply_text("Вы проделали отличную работу! Сейчас вам придут данные для проверки.")
	update.message.reply_text('Посмотреть все созданные вами опросы можно при помощи кнопки "Мои опросы"', reply_markup=my_keyboard)
	current_user = db.briefs.findone({"user_id": effective_user.id})
	if current_user:
		brief_prev_id = db.briefs.findone({"_Id"})
		brief_prev_name = db.briefs.findone({"brief_name"})
	update.message.reply_text('ID опроса "{}"'.format(brief_prev_id), reply_markup=my_keyboard)
	update.message.reply_text('Название опроса "{}"'.format(brief_prev_name), reply_markup=my_keyboard)


def brief_list(db, effective_user):
	current_user = db.briefs.findone({"user_id": effective_user.id})
	if current_user:
		brief_list = db.briefs.find({"_Id"})
	return brief_list

