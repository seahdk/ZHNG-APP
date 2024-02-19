import shelve

class Centre():
    count_id = 0
    count_set: bool = False

    def __init__(self, name, code, area, type):
        self.__centre_id = self._get_next_centre_id()
        self.__name = name
        self.__code = code
        self.__area = area
        self.__type = type


    def set_name(self, name):
        self.__name = name
    def set_code(self, code):
        self.__code = code
    def set_location(self, area):
        self.__area = area
    def set_type(self, type):
        self.__type = type

    @classmethod
    def _get_next_centre_id(cls):
        if not cls.count_set:
            cls.count_set = True
            db = shelve.open('centre.db', 'r')
            centre_dict = db['Centre']
            ids = list(centre_dict.keys()) or [0]
            cls.count_id = max(ids)

        cls.count_id += 1
        return cls.count_id

    def get_name(self):
        return self.__name
    def get_code(self):
        return self.__code
    def get_location(self):
        return self.__area
    def get_type(self):
        return self.__type
    def get_centre_id(self):
        return self.__centre_id
