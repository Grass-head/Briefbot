import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup

#from db import db, add_user, add_brief, add_question, get_current_user, get_current_brief


def welcome_user(update, context):
	#user = add_user(db, update.effective_user)
	keyboard = [
	[InlineKeyboardButton("Создать опрос", callback_data='Введите название опроса')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	context.user_data['user'] = {
		"user_id": update._effective_user.id,
		"first_name": update._effective_user.first_name,
		"last_name": update._effective_user.last_name,
		"is_admin": True
		}
	text_greet = 'Привет! Этот бот поможет вам составить бриф. Сформулируйте и отправьте боту вопросы брифа и получите ссылку - приглашение. Эту ссылку нужно передать клиенту. Он пройдет бриф и бот отправит вам на почту результат.'
	update.message.reply_text(text_greet)
	update.message.reply_text('Для продолжения нажмите:', reply_markup=reply_markup)


NAME, QUESTIONS, ANSWERS, DONE = range(4)


def create_brief(update, context):
	query = update.callback_query
	query.edit_message_text(text="{}".format(query.data))
	return NAME


def brief_name(update, context):
	#brief = add_brief(db, update.effective_user, update.message)
	keyboard = [
	[InlineKeyboardButton("Вопрос", callback_data='Введите вопрос')],
	[InlineKeyboardButton("Завершить опрос", callback_data='Вы завершили опрос')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	context.user_data['brief'] = {
			"user_id": update._effective_user.id,
			"is_active": True,
			"brief_name": update.message.text
			}
	user_text = context.user_data['brief']['brief_name']
	update.message.reply_text('Хорошая работа! Название "{}" записано'.format(user_text))
	update.message.reply_text("Чтобы продолжить нажмите одну из кнопок:", reply_markup=reply_markup)
	return QUESTIONS


def enter_questions(update, context):
	query = update.callback_query
	query.edit_message_text(text="{}".format(query.data))
	return QUESTIONS 


def brief_questions(update, context):
	#question = add_question(db, update.message)
	keyboard = [
	[InlineKeyboardButton("Вопрос", callback_data='Введите вопрос')],
	[InlineKeyboardButton("Ответ", callback_data='Ввести ответ на вопрос')],
	[InlineKeyboardButton("Завершить опрос", callback_data='Вы завершили опрос')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	context.user_data['question'] = {
		"brief_id": context.user_data['brief']['brief_name'],
		"text": update.message.text
		}
	user_question = context.user_data['question']['text']
	update.message.reply_text('Отлично! Вопрос "{}" сохранен'.format(user_question), reply_markup=reply_markup)
	return QUESTIONS

def enter_answers(update, context):
	query = update.callback_query
	query.edit_message_text(text="{}".format(query.data))
	return ANSWERS 

def brief_answers(update, context):
	keyboard = [
	[InlineKeyboardButton("Еще вариант ответа", callback_data='Ввести еще ответ на вопрос')],
	[InlineKeyboardButton("Новый вопрос", callback_data='Введите новый вопрос')],
	[InlineKeyboardButton("Завершить опрос", callback_data='Завершить опрос')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	context.user_data['answer'] = {
		"answer_id":  update.message.message_id,
		"question_id": context.user_data['question']['text'],
		"text": update.message.text, 
		"respondent_id": update._effective_user.id,
		"filling_time": update.message.date
		}
	user_answer = context.user_data['answer']['text']
	update.message.reply_text('Отлично! Ответ "{}" сохранен'.format(user_answer), reply_markup=reply_markup)
	return ANSWERS


def switch_answers_to_questions(update, context):
	return QUESTIONS


def switch_answers_to_end(update, context):
	return DONE


def end_questions(update, context):
	query = update.callback_query
	keyboard = [
	[InlineKeyboardButton("Посмотреть опрос", callback_data='Вы запросили текущий опрос')],
	[InlineKeyboardButton("Мои опросы", callback_data='Вы запросили список ваших опросов')]
	]
	reply_markup = InlineKeyboardMarkup(keyboard)
	query.edit_message_text(text="{}. Выберите следующее действие:".format(query.data), reply_markup=reply_markup)
	return DONE


def dontknow(update, context):
	update.message.reply_text("Не понимаю. Следуйте, пожалуйста, инструкции")

def keyboard_my_brief():
	my_keyboard = ReplyKeyboardMarkup(['Мои опросы'])
	return my_keyboard

def brief_check_result(update, context):
	query = update.callback_query
	query.edit_message_text(text="{}. Сейчас вам придут данные для проверки.".format(query.data))
	if current_user and current_brief:
		brief_preview_name = current_brief['brief_name']
	update.message.reply_text('Название опроса "{}"'.format(brief_preview_name), reply_markup=keyboard_my_brief())


def brief_lists(bot, update, context):
	query = update.callback_query
	query.answer(text="{}. В следующем сообщении будут данные по всем опросам, которые вы создали.".format(query.data), show_alert=True)
	current_user = get_current_user(db, update.effective_user)
	if current_user:
		brief_list = db.briefs.find()
		for item in brief_list:
			brief_list_names = item["brief_name"]
			bot.send_message(chat_id=query.message.chat.id, text="{}".format(brief_list_names))
