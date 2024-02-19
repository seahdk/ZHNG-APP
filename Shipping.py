class Shipping:
    count_id = 0

    def __init__(self, first_name, last_name, emailaddress, address, unitno, contact, shipping_id=None):
        Shipping.count_id += 1
        self.__shipping_id = Shipping.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__emailaddress = emailaddress
        self.__address = address
        self.__unitno = unitno
        self.__contact = contact

    def set_first_name(self, first_name):
        self.__first_name = first_name
    def set_last_name(self, last_name):
        self.__last_name = last_name
    def set_emailaddress(self, emailaddress):
        self.__emailaddress = emailaddress
    def set_address(self, address):
        self.__address = address
    def set_unitno(self, unitno):
        self.__unitno = unitno
    def set_contact(self, contact):
        self.__contact = contact

    def get_shipping_id(self):
        return self.__shipping_id
    def get_first_name(self):
        return self.__first_name
    def get_last_name(self):
        return self.__last_name
    def get_emailaddress(self):
        return self.__emailaddress
    def get_address(self):
        return self.__address
    def get_unitno(self):
        return self.__unitno
    def get_contact(self):
        return self.__contact
