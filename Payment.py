class Payment:

# this page not in use now because createUsers is not been used yet.
    def __init__(self, card_type, card_number, name_on_card, expiry_date, cvvcode):
        self.__card_type = card_type
        self.__card_number = card_number
        self.__name_on_card = name_on_card
        self.__expiry_date = expiry_date
        self.__cvvcode = cvvcode

    def set_card_type(self,card_type):
        self.__card_type = card_type
    def set_card_number(self, card_number):
        self.__card_number = card_number
    def set_name_on_card(self, name_on_card):
        self.__name_on_card = name_on_card
    def set_expiry_date(self, expiry_date):
        self.__expiry_date = expiry_date
    def set_cvvcode(self, cvvcode):
        self.__cvvcode = cvvcode


    def get_card_type(self):
        return self.__card_type
    def get_card_number(self):
        return self.__card_number
    def get_name_on_card(self):
        return self.__name_on_card
    def get_expiry_date(self):
        return self.__expiry_date
    def get_cvvcode(self):
        return self.__cvvcode


