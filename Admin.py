#parent class
import shelve


class Admin():
    count_id = 0



    def __init__(self, username, password, email):
        Admin.count_id += 1
        self.__admin_id = Admin.count_id
        self.__username = username
        self.__password = password
        self.__email = email


    def set_admin_id(self, admin_id):
        self.__admin_id = admin_id
    def set_username(self, username):
        self.__username = username
    def set_password(self, password):
        self.__password = password
    def set_email(self, email):
        self.__email = email






    def get_admin_id(self):
        return self.__admin_id
    def get_username(self):
        return self.__username
    def get_password(self):
        return self.__password
    def get_email(self):
        return self.__email


