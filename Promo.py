import shelve


class Promo():
    count_id = 0
    count_set: bool = False

    def __init__(self, code, discount, quantity, expiry,notes, status):
        self.__number_id = self._get_next_number_id()
        self.__code = code
        self.__discount = discount
        self.__quantity = quantity
        self.__expiry = expiry
        self.__notes = notes
        self.__status = status

    @classmethod
    def _get_next_number_id(cls) -> int:
        if not cls.count_set:
            cls.count_set = True
            db = shelve.open('promo.db', 'r')
            promos_dict = db['Promos']  # type: Dict # noqa
            ids = list(promos_dict.keys()) or [0]
            cls.count_id = max(ids)  #get the next highest value

        cls.count_id += 1
        return cls.count_id

    def get_number_id(self):
        return self.__number_id
    def get_code(self):
        return self.__code
    def get_discount(self):
        return self.__discount
    def get_quantity(self):
        return self.__quantity
    def get_expiry(self):
            return self.__expiry
    def get_notes(self):
            return self.__notes
    def get_status(self):
            return self.__status


    def set_number_id(self, number_id):
        self.__number_id = number_id
    def set_code(self,code):
        self.__code = code
    def set_discount(self,discount):
         self.__discount = discount
    def set_quantity(self,quantity):
        self.__quantity = quantity
    def set_expiry(self,expiry):
        self.__expiry = expiry
    def set_notes(self,notes):
        self.__notes = notes
    def set_status(self,status):
        self.__status = status




