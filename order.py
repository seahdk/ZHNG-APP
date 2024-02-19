import Product

class order(Product.Products):
    count_id = 0

    def __init__(self, order_id, trans_time, trans_date, product_id, qty, total_amount):
        super().__init__(product_id, qty)
        order.count_id += 1
        self.__order_id = order_id
        self.__trans_time = trans_time
        self.__trans_date = trans_date
        self.__total_amount = total_amount


    def set_order_id(self, order_id):
        self.__order_id = order_id
    def set_trans_time(self, trans_time):
        self.__trans_time = trans_time
    def set_trans_date(self, trans_date):
        self.__trans_date = trans_date
    def set_totalamount(self, total_amount):
        self.__total_amount = total_amount


    def get_order_id(self):
        return self.__order_id
    def get_trans_time(self):
        return self.__trans_time
    def get_trans_date(self):
        return self.__trans_date
    def get_total_amount(self):
        return self.__total_amount

