class User:
    count_id = 0

    def __init__(self, first_name, last_name, username, email):
        self.__user_id = User.count_id
        self.__class__.count_id += 1
        self.__first_name = first_name
        self.__last_name = last_name
        self.__username = username
        self.__email = email

    def set_user_id(self):
        self.__user_id = User.count_id
    def set_first_name(self, first_name):
        self.__first_name = first_name
    def set_last_name(self, last_name):
        self.__last_name = last_name
    def set_username(self, username):
        self.__username = username
    def set_email(self, email):
        self.__email = email

    def get_user_id(self):
        return self.__user_id
    def get_first_name(self):
        return self.__first_name
    def get_last_name(self):
        return self.__last_name
    def get_username(self):
        return self.__username
    def get_email(self):
        return self.__email
