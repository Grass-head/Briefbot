import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup

from db import db, add_user, add_brief, add_question, get_current_user, get_current_brief
from bson.json_util import dumps


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
	return QUESTIONS 


def brief_questions(bot, update):
	question = add_question(db, update.message)
	keyboard = [[InlineKeyboardButton("Вопрос", callback_data='Введите вопрос')],
	[InlineKeyboardButton("Завершить опрос", callback_data='Вы завершили опрос')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	user_question = update.message.text
	update.message.reply_text('Отлично! Вопрос "{}" сохранен'.format(user_question), reply_markup=reply_markup)
	return QUESTIONS


def end_questions(bot, update):
	query = update.callback_query
	keyboard = [[InlineKeyboardButton("Посмотреть опрос", callback_data='Вы запросили текущий опрос')],
	[InlineKeyboardButton("Мои опросы", callback_data='Вы запросили список ваших опросов')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	query.edit_message_text(text="{}. Выберите следующее действие:".format(query.data), reply_markup=reply_markup)
	return DONE


def dontknow(bot, update):
	update.message.reply_text("Не понимаю. Следуйте, пожалуйста, инструкции")

def keyboard_my_brief():
	my_keyboard = ReplyKeyboardMarkup(['Мои опросы'])
	return my_keyboard

def brief_check_result(bot, update):
	query = update.callback_query
	query.edit_message_text(text="{}. Сейчас вам придут данные для проверки.".format(query.data))
	current_user = get_current_user(db, update.effective_user)
	print(current_user)
	current_brief = get_current_brief(db, update.message)
	print(current_brief)
	if current_user and current_brief:
		brief_preview_name = current_brief['brief_name']
	update.message.reply_text('Название опроса "{}"'.format(brief_preview_name), reply_markup=keyboard_my_brief())


def brief_lists(bot, update):
	query = update.callback_query
	query.answer(text="{}. В следующем сообщении будут данные по всем опросам, которые вы создали.".format(query.data), show_alert=True)
	current_user = get_current_user(db, update.effective_user)
	if current_user:
		brief_list = db.briefs.find()
		for item in brief_list:
			brief_list_names = item["brief_name"]
			bot.send_message(chat_id=query.message.chat.id, text="{}".format(brief_list_names))
