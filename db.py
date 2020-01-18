from pymongo import MongoClient
import settings

db = MongoClient(settings.MONGO_LINK)[settings.MONGO_DB]

def add_user(db, effective_user):
	user = db.users.find_one({"user_id": effective_user.id})
	if not user:
		user = {
		"user_id": effective_user.id,
		"first_name": effective_user.first_name,
		"last_name": effective_user.last_name,
		"is_admin": True
		}
		db.users.insert_one(user)
	return user

def add_brief(db, effective_user, message):
	current_brief = db.briefs.find_one({"brief_name": message.text})
	if not current_brief:
		brief = {
			"user_id": effective_user.id,
			"is_active": True,
			"brief_name": message.text
		}
		db.briefs.insert_one(brief)
	return brief


def add_question(db, message):
	question = {
		"brief_id": message.chat.id,
		"question_text": message.text
	}
	db.questions.insert_one(question)
	return question

#def add_answer(db, effective_user, message):
	#answer = {
		#"question_id": message.text,
		#"answer_text": message.text,
		#"respondent_id": effective_user.id,
		#"filling_date": message.date
	#}
	#db.answers.insert_one(answer)
	#return answer