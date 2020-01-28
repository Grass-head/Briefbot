from pymongo import MongoClient
import settings

db = MongoClient(settings.MONGO_LINK)[settings.MONGO_DB]

def add_user(update, context):
	user = db.users.find_one({"user_id": update._effective_user.id})
	if not user:
		user = context.user_data['user']
		db.users.insert_one(user)
	return user


def add_brief_data(update, context):
	current_brief = db.briefs.find_one({"brief_name": update.message.text})
	if not current_brief:
		brief = {
			"briefs": context.user_data['brief'],
			"questions": context.user_data['question'],
			"answers": context.user_data['answer']
		}
		db.briefs.insert_one(brief)
	return brief

