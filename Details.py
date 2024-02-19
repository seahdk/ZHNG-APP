

class Details():
   count_id = 0

   def __init__(self, product_id, description, color, qty, price, cart_id=None):
      if cart_id == None:
         Details.count_id += 1
         self.__cart_id = Details.count_id
      else:
         self.__cart_id = cart_id
      self.__product_id = product_id
      self.__description = description
      self.__color = color
      self.__qty = qty
      self.__price = price

   def set_description(self, description):
      self.__description = description
   def set_color(self, color):
      self.__color = color
   def set_qty(self, qty):
      self.__qty = qty
   def set_price(self, price):
      self.__price = price

   def get_cart_id(self):
      return self.__cart_id
   def get_product_id(self):
      return self.__product_id
   def get_description(self):
      return self.__description
   def get_color(self):
      return self.__color
   def get_qty(self):
      return self.__qty
   def get_price(self):
      return self.__price

# this page/classes is for create and retrieving carts.
