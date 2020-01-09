from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler, Filters, ConversationHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from models import Brief

engine = create_engine("sqlite:///briefbot.db")
Session = sessionmaker(bind=engine)
session = Session()

def welcome_user(bot, update):
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
	keyboard = [[InlineKeyboardButton("Вопрос", callback_data='Введите вопрос')],
				[InlineKeyboardButton("Завершить опрос", callback_data='Вы завершили опрос')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	user_text = update.message.text
	update.message.reply_text('Хорошая работа! Название "{}" записано'.format(user_text))
	brief = Brief(user_id=update.message.chat_id, is_active=True)
	session.add(brief)
	session.commit()
	update.message.reply_text("Чтобы продолжить нажмите одну из кнопок:", reply_markup=reply_markup)
	return QUESTIONS

def enter_questions(bot, update):
	query = update.callback_query
	query.edit_message_text(text="{}".format(query.data))
	if query.data != 'Вы завершили опрос':
		return QUESTIONS
	if query.data == 'Вы завершили опрос':
		return DONE

def brief_questions(bot, update):
	keyboard = [[InlineKeyboardButton("Вопрос", callback_data='Введите вопрос')],
				[InlineKeyboardButton("Завершить опрос", callback_data='Вы завершили опрос')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	user_text = update.message.text
	update.message.reply_text('Отлично! Вопрос "{}" сохранен'.format(user_text), reply_markup=reply_markup)
	return QUESTIONS

def end_brief(bot,update):
	update.message.reply_text("Спасибо! Досвидания!")

def dontknow(bot,update):
	update.message.reply_text("Не понимаю. Следуйте, пожалуйста, инструкции")






