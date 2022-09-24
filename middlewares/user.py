from models.model import User

class MiddleUser:
    def create_user(chat_id):
        try:
            User.create(telegram_id=chat_id)
        except:
            pass

    def registration(chat_id, g_password, g_name, school_id):
        user = MiddleUser.get_user_by_chat(chat_id)
        user.update(g_name=g_name, g_password=g_password, school_id=school_id)

    def get_user_by_chat(chat_id):
        user = User.query.filter(User.telegram_id == chat_id).first()
        return user

