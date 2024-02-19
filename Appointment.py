import User
import shelve


class Appointment(User.User):
    appt_id = 0
    count_set: bool = False

    def __init__(self, first_name, last_name, username, email, location, time, date, remarks):
        self.__appt_id = self._get_next_appt_id()
        super().__init__(first_name, last_name, username, email)
        self.__location = location
        self.__time = time
        self.__date = date
        self.__remarks = remarks

    def set_location(self, location):
        self.__location = location
    def set_time(self, time):
        self.__time = time
    def set_date(self, date):
        self.__date = date
    def set_remarks(self, remarks):
        self.__remarks = remarks

    @classmethod
    def _get_next_appt_id(cls):
        if not cls.count_set:
            cls.count_set = True
            db = shelve.open('appt.db', 'r')
            appt_dict = db['Appt']
            ids = list(appt_dict.keys()) or [0]
            cls.count_id = max(ids)

        cls.count_id += 1
        return cls.count_id

    def get_location(self):
        return self.__location
    def get_time(self):
        return self.__time
    def get_date(self):
        return self.__date
    def get_remarks(self):
        return self.__remarks
    def get_appt_id(self):
        return self.__appt_id

