import shelve

class Customer():
    count_id = 0
    count_set: bool = False


    def __init__(self, username, first_name, last_name, email, mobile_number, date_joined, address, password, confirm_password):
        self.__customer_id = self._get_next_customer_id()
        self.__username = username
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__password = password
        self.__confirm_password = confirm_password
        self.__mobile_number = mobile_number
        self.__date_joined = date_joined
        self.__address = address

    @classmethod #to return the next avaliable integer
    def _get_next_customer_id(cls): #it will show an integer

        if not cls.count_set: #if count_set = False run this loop
            cls.count_set = True
            db = shelve.open('customer.db', 'r')
            customers_dict = db['Customers']
            ids = list(customers_dict.keys()) or [0] #list all the key values from dictionary
            cls.count_id = max(ids)  #max takes an iterable and finds the maximum element

        cls.count_id += 1
        return cls.count_id



    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id
    def set_username(self, username):
        self.__username = username
    def set_first_name(self, first_name):
        self.__first_name = first_name
    def set_last_name(self, last_name):
        self.__last_name = last_name
    def set_email(self, email):
        self.__email = email
    def set_password(self, password):
        self.__password = password
    def set_mobile_number(self, mobile_number):
        self.__mobile_number = mobile_number
    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined
    def set_address(self, address):
        self.__address = address




    def get_customer_id(self):
        return self.__customer_id
    def get_username(self):
        return self.__username
    def get_first_name(self):
        return self.__first_name
    def get_last_name(self):
        return self.__last_name
    def get_email(self):
        return self.__email
    def get_password(self):
        return self.__password
    def get_mobile_number(self):
        return self.__mobile_number
    def get_date_joined(self):
        return self.__date_joined
    def get_address(self):
        return self.__address


