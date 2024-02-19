import shelve



class Product():
    count_id = 0
    count_set: bool = False

    def __init__(self, sku, sku_description, price, stock, image, color=None, searched=None):
        self.__product_id = self._get_next_product_id() #refer to classmethod
        self.__sku = sku
        self.__sku_description = sku_description
        self.__price = price
        self.__stock = stock
        self.__image = image
        self.__searched = searched




    @classmethod #to return the next avaliable integer
    def _get_next_product_id(cls): #it will show an integer

        if not cls.count_set: #if count_set = False run this loop
            cls.count_set = True
            db = shelve.open('product.db', 'r')
            products_dict = db['Products']
            ids = list(products_dict.keys()) or [0] #list all the key values from dictionary
            cls.count_id = max(ids)  #max takes an iterable and finds the maximum element

        cls.count_id += 1
        return cls.count_id



    def get_product_id(self):
        return self.__product_id
    def get_sku(self):
        return self.__sku
    def get_sku_description(self):
        return self.__sku_description
    def get_price(self):
        return self.__price
    def get_stock(self):
        return self.__stock
    def get_image(self):
        return self.__image
    def get_searched(self):
        return self.__searched



    def set_product_id(self, product_id):
        self.__product_id = product_id
    def set_sku(self, sku):
        self.__sku = sku
    def set_sku_description(self, sku_description):
        self.__sku_description = sku_description
    def set_price(self, price):
        self.__price = price
    def set_stock(self, stock):
        self.__stock = stock
    def set_image(self, image):
        self.__image = image
    def set_searched(self, searched):
        self.__searched = searched


