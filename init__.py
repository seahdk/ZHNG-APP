from flask import Flask, render_template, request, redirect, url_for, session
from Forms import createProductForm, UpdateCartForm, shippingform, paymentform, SearchForm, UpdateInventoryForm, CreateCartForm, createPromoForm, searchProduct, ConfirmPriceForm,updateCustomerForm,updateAdminForm,CreateCustomerForm,LoginForm
from datetime import timedelta

import shelve, Appointment, User, Centre
from Forms import createAppointment, searchAppointment, filterAppointment, createCentre, filterCentre



import os
from datetime import datetime
from werkzeug.utils import secure_filename
import shelve, Product, Shipping, Payment, Details, Promo, Customer,Admin
from decimal import Decimal  # for filter function
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.permanent_session_lifetime = timedelta(minutes=60)
app.config['WTF_CSRF_ENABLED'] = False  # to delete the csrf
app.config['SECRET_KEY'] = b'\x872ik\x08M\xcd\x90Rn\xac\xf7\x80\xb6\n\r\xe8b\xa3\x0c\x86h\xa5\xf7'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#HOME PAGE
@app.route('/')
@app.route('/home')
def home():
     admins_dict = {"email": "admin@gmail.com", "password": "lol"}
     customers_dict = {}


     if ('admins_dict' in session and session['admins_dict'] == admins_dict['email']):
        return render_template('home.html')

     else:
         for i in customers_dict:
            if ('customers_dict' in session and session['customers_dict'] == customers_dict[customers_dict.get(i).get_email()]):
                return render_template('home.html')

     return render_template('home.html')


#404 ERROR
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


#CONTACT US PAGE
@app.route('/contactUs')
def contact_us():

    return render_template('contactUs.html')





#CREATE NEW PRODUCT FOR THE BACKEND
@app.route('/createProduct', methods=['GET', 'POST'])
def create_product():
    create_product_form = createProductForm(request.form)
    print(create_product_form.validate_on_submit())     #false here
    if request.method == 'POST' and create_product_form.validate_on_submit():

        products_dict = {}
        db = shelve.open('product.db', 'c')

        try:
            products_dict = db['Products']
        except:
            print("Error in retrieving Customers from product.db.")

        file = request.files['image']
        filename = None
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        product = Product.Product(create_product_form.sku.data, create_product_form.sku_description.data,
                                  create_product_form.price.data, create_product_form.stock.data, filename)

        products_dict[product.get_product_id()] = product
        db['Products'] = products_dict

        db.close()
        print(products_dict)
        return redirect(url_for('retrieve_products'))
    print(create_product_form.errors)
    return render_template('createProduct.html', form=create_product_form)


#UPDATE PRODUCT FOR BACKEND
@app.route('/updateProduct/<int:id>/',
           methods=['GET', 'POST'])  # use int:id as a parameter to get the customer id that u are updating
def update_product(id):
    products_dict = {}
    db = shelve.open('product.db', 'w')
    products_dict = db['Products']
    product = products_dict.get(id)


    update_product_form = UpdateInventoryForm(request.form)

    if request.method == 'POST':
        product.set_sku(update_product_form.sku.data)
        product.set_sku_description(update_product_form.sku_description.data)
        product.set_price(update_product_form.price.data)
        product.set_stock(update_product_form.stock.data)

        file = request.files['image']
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], product.get_image()))
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.set_image(filename)

        db['Products'] = products_dict
        db.close()
        return redirect(url_for('retrieve_products'))

    product = products_dict.get(id)
    update_product_form.sku.data = product.get_sku()
    update_product_form.sku_description.data = product.get_sku_description()
    update_product_form.price.data = product.get_price()
    update_product_form.stock.data = product.get_stock()
    update_product_form.image.data = product.get_image()
    db.close()
    return render_template('updateProduct.html', form=update_product_form)


#RETRIEVE PRODUCT FOR BACKEND
@app.route('/retrieveProduct')
def retrieve_products():
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('retrieveProduct.html', count=len(products_list), products_list=products_list)


#DELETE PRODUCT FROM BACKEND
@app.route('/deleteProduct/<int:id>', methods=['POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('product.db', 'w')
    products_dict = db['Products']

    products_dict.pop(id)

    db['Products'] = products_dict
    db.close()

    return redirect(url_for('retrieve_products'))






#FILTER PRODUCT FOR BACKEND
@app.route('/filterproduct', methods=["GET", "POST"])
def filterproduct():
    if request.method == "POST":
        price_min = Decimal(request.form["price_min"] or 0) #setting default value to 0
        price_max = Decimal(request.form["price_max"] or 0)
        stock_min = Decimal(request.form["stock_min"] or 0)
        stock_max = Decimal(request.form["stock_max"] or 0)
        available = True if request.form["available"] == "available" else False


        db = shelve.open('product.db', 'w')
        products_dict = db['Products']

        product_values = products_dict.values()  #use the dictionary values

        if price_max != 0 and price_max >= price_min:
            filtered_price = filter(lambda p: price_max > p.get_price() >= price_min, product_values)   #filtering product values from the dictionary
        else:
            filtered_price = products_dict.values()
        if stock_max != 0 and stock_max >= stock_min:
            filtered_stock = filter(lambda p: stock_max > p.get_stock() >= stock_min, filtered_price)  #filtering from filtered price to have continuous filtering
        else:
            filtered_stock = filtered_price

        # Filters stock < 5
        if request.form.get('less_stock'):
            filtered_stock = filter(lambda p: p.get_stock() < 5, filtered_stock)

        if not available:
            filtered_stock = filter(lambda p: p.get_stock() <= 0, filtered_stock)



        products_list = list(filtered_stock)  #list all filtered products


        db.close()
        print(products_list)
        return render_template("filterProduct.html", count=len(products_list), products_list=products_list)

    products_list = session.pop('product_lists', [])  #user pressed cancel and pop all the data out
    return render_template("filterProduct.html", count=len(products_list), products_list=products_list)


#SEARCH FUNCTION FOR PRODUCTS IN BACKEND
@app.route('/search', methods=["GET", "POST"])
def search():
    create_product_form = SearchForm()
    if create_product_form.validate_on_submit():
        description = create_product_form.searched.data
        product_list = []
        db = shelve.open('product.db', 'w')
        products_dict = db['Products']
        for p_id, product in products_dict.items():
            if description.lower() in product.get_sku_description().lower() or description.lower() in str(product.get_sku()):
                product_list.append(product)

        return render_template("search.html", form=create_product_form, count=len(product_list),
                               products_list=product_list)
    return redirect(url_for('retrieve_products'))




#VIEW THE PRODUCT IMAGE FOR BACKEND
@app.route('/viewProduct/<int:id>/', methods=['GET', 'POST'])
def view_product(id):
    update_product_form = createProductForm(request.form)

    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    product = products_dict.get(id)

    return render_template('viewProduct.html', product=product)


#VIEW THE PRODUCT IMAGE FOR FRONTEND CART
@app.route('/viewProduct2/<int:id>/', methods=['GET', 'POST'])
def view_product2(id):
    update_cart_form = CreateCartForm(request.form)

    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    product = products_dict.get(id)

    return render_template('viewProduct2.html', product=product)


#CREATE PROMO CODES FOR BACKEND
@app.route('/createPromo', methods=['GET', 'POST'])
def create_promo():
    create_promo_form = createPromoForm(request.form)
    if request.method == 'POST' and create_promo_form.validate_on_submit():
        promos_dict = {}
        db = shelve.open('promo.db', 'c')

        try:
            promos_dict = db['Promos']
        except:
            print("Error in retrieving Customers from promo.db.")

        promo = Promo.Promo(create_promo_form.code.data, create_promo_form.discount.data,
                                  create_promo_form.quantity.data, create_promo_form.expiry.data,
                                  create_promo_form.notes.data, create_promo_form.status.data)

        promos_dict[promo.get_number_id()] = promo
        db['Promos'] = promos_dict

        db.close()

        return redirect(url_for('retrieve_promo'))
    return render_template('createPromo.html', form=create_promo_form)



#RETRIEVE PROMO CODES FOR BACKEND
@app.route('/retrievePromo')
def retrieve_promo():
    promos_dict = {}
    db = shelve.open('promo.db', 'r')
    promos_dict = db['Promos']
    db.close()

    promos_list = []
    for key in promos_dict:
        promo = promos_dict.get(key)
        promos_list.append(promo)

    return render_template('retrievePromo.html', count=len(promos_list), promos_list=promos_list)



#DELETE PROMO CODES FOR BACKEND
@app.route('/deletePromo/<int:id>', methods=['POST'])
def delete_promo(id):
    promos_dict = {}
    db = shelve.open('promo.db', 'w')
    promos_dict = db['Promos']

    promos_dict.pop(id)

    db['Promos'] = promos_dict
    db.close()

    return redirect(url_for('retrieve_promo'))



#UPDATE PROMO CODES FOR BACKEND
@app.route('/updatePromo/<int:id>/',
           methods=['GET', 'POST'])  # use int:id as a parameter to get the customer id that u are updating
def update_promo(id):
    update_promo_form = createPromoForm(request.form)
    if request.method == 'POST' and update_promo_form.validate_on_submit():
        promos_dict = {}
        db = shelve.open('promo.db', 'w')
        promos_dict = db['Promos']

        promo = promos_dict.get(id)
        promo.set_code(update_promo_form.code.data)
        promo.set_discount(update_promo_form.discount.data)
        promo.set_quantity(update_promo_form.quantity.data)
        promo.set_expiry(update_promo_form.expiry.data)
        promo.set_notes(update_promo_form.notes.data)
        promo.set_status(update_promo_form.status.data)
        db['Promos'] = promos_dict
        db.close()

        return redirect(url_for('retrieve_promo'))
    else:
        promos_dict = {}
        db = shelve.open('promo.db', 'r')
        promos_dict = db['Promos']
        db.close()

        promo = promos_dict.get(id)
        update_promo_form.code.data = promo.get_code()
        update_promo_form.discount.data = promo.get_discount()
        update_promo_form.quantity.data = promo.get_quantity()
        update_promo_form.expiry.data = promo.get_expiry()
        update_promo_form.notes.data = promo.get_notes()
        update_promo_form.status.data = promo.get_status()
        return render_template('updatePromo.html', form=update_promo_form)



#DISPLAY ALL PRODUCTS FOR CUSTOMER
@app.route('/productPage', methods=['GET', 'POST'])
def product_page():

    products_dict = {}
    db = shelve.open('product.db', 'r')

    products_dict = db['Products']

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)
        products_list.sort(key=Product.Product.get_product_id, reverse=False)
    db.close()

    return render_template('productPage.html', count=len(products_list), products_list=products_list)


#SELECT ITEM WHICH THE CUSTOMER WANTS TO BUY AND QUANTITY
@app.route('/createCart', methods=['GET', 'POST'])
def create_cart():
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = [('', 'Select')]
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append((key, product.get_sku_description()))

    create_cart_form = CreateCartForm(request.form)
    create_cart_form.description.choices = products_list

    return render_template('createCart.html', form=create_cart_form)



#PAGE TO CONFIRM PRICE AND CHECK FOR STOCK
@app.route('/confirmPrice', methods=["GET", "POST"])
def confirm_price():

    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = [('', 'Select')]
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append((key, product.get_sku_description()))

    form = CreateCartForm(request.form)
    form.description.choices = products_list
    if request.method == "POST" and form.validate():
        db = shelve.open('product.db', 'r')
        products_dict = db['Products']
        db.close()

        try:
            product = products_dict[int(form.description.data)]
        except KeyError:
            return "Item not found"

        qty = int(form.qty.data)

        if qty > product.get_stock():
            return "Out of Stock"

        color = form.color.data

        form = ConfirmPriceForm(request.form)
        form.product_id.default = product.get_product_id()
        form.description.default = product.get_sku_description()
        form.color.default = color
        form.qty.default = qty
        form.price.default = product.get_price()
        form.process()

        return render_template('confirmPrice.html', form=form)

    return redirect(url_for('create_cart'))





#CUSTOMER SHIPPING PAGE
@app.route('/shipping', methods=['GET', 'POST'])
def shipping():
    create_shipping_form = shippingform(request.form)
    if request.method == 'POST' and create_shipping_form.validate():
        db = shelve.open('shipping.db', 'w')
        shipping_dict = db['shipping']

        shipping = Shipping.Shipping(create_shipping_form.first_name.data, create_shipping_form.last_name.data, create_shipping_form.emailaddress.data, create_shipping_form.address.data, create_shipping_form.unitno.data, create_shipping_form.contact.data)
        shipping_dict[shipping.get_shipping_id()] = shipping

        print("**** get Shipping form ****, address")
        shipping = Shipping.Shipping(create_shipping_form.first_name.data,
                                    create_shipping_form.last_name.data, create_shipping_form.emailaddress.data,
                                    create_shipping_form.address.data, create_shipping_form.unitno.data, create_shipping_form.contact.data)
        db['shipping'] = shipping_dict
        db.close()
        return redirect(url_for('checkout'))
    return render_template('shipping.html', form=create_shipping_form)


#CUSTOMER CHECKOUT AND PAYMENT PAGE
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    create_checkout_form = paymentform(request.form)
    if request.method == 'POST' and create_checkout_form.validate():
        checkout_dict = {}
        db = shelve.open('checkout.db', 'c', writeback=True)
        checkout_dict = db['checkout']
        try:
            checkout_dict = db['checkout']
        except:
            print("Error in the system. Please try again.")

        checkout = Payment.Payment(create_checkout_form.card_type.data, create_checkout_form.card_number.data, create_checkout_form.name_on_card.data, create_checkout_form.expiry_date.data, create_checkout_form.cvvcode.data)
        checkout_dict[checkout.get_card_number()] = checkout
        db['checkout'] = checkout_dict

        print("**** get Shipping form ****, address")
        checkout = Payment.Payment(create_checkout_form.card_type.data, create_checkout_form.card_number.data,
                                    create_checkout_form.name_on_card.data, create_checkout_form.expiry_date.data,
                                    create_checkout_form.cvvcode.data)
        checkout_dict[checkout.get_card_number()] = checkout
        db['checkout'] = checkout_dict

        db.close()

        #CART TOTAL AND
        cart_dict = session['cart']
        total_amount = 0
        for cart_id in cart_dict:
            cart_item = cart_dict.get(cart_id)
            db = shelve.open('product.db', 'w', writeback=True)
            product_dict = db['Products']
            product_dict[cart_item['product_id']].set_stock(product_dict[cart_item['product_id']].get_stock() - int(cart_item['qty']))
            db.close()
            total_amount += get_product(cart_item['product_id']).get_price() * cart_item['qty']

        #VALIDATES AND ALLOW OR DISALLOW THE USAGE OF THE PROMO CODES
        applied_promo = False
        if create_checkout_form.promocode.data != None:
            db = shelve.open('promo.db', 'c', writeback=True)
            promos_dict = db['Promos']
            for promo_id in promos_dict.copy():
                promo = promos_dict.get(promo_id)
                if promo.get_code() == create_checkout_form.promocode.data and datetime.now().date() <= promo.get_expiry() and promo.get_status() == 'A':
                    applied_promo = True
                    total_amount -= int(promo.get_discount())
                    promo.set_quantity(promo.get_quantity() - 1)

                    if promo.get_quantity() == 0:
                        del promos_dict[promo_id]
                    break

        del session['cart']


        return render_template('order.html', total_amount=total_amount, applied_promo=applied_promo)

    total_amount = 0
    cart_dict = session['cart']
    for cart_id in cart_dict:
        cart_item = cart_dict.get(cart_id)
        total_amount += get_product(cart_item['product_id']).get_price() * cart_item['qty']


    return render_template('checkout.html', form=create_checkout_form, total_amount=total_amount)



#RETRIEVE ALL ORDERS FOR BACKEND(ADMIN)
@app.route('/retrieveOrders') #need help here
def retrieve_orders():

    try:
        cart_dict = session['cart']  #read the 'cart' value and save it in cart_dict
    except KeyError:
        cart_dict = {}


    order_form = paymentform(request.form)
    if request.method == 'POST' and order_form.validate():


        session['cart'] = cart_dict

    colours = {
        'B': "Black",
        'W': "White",
        'P': "Pink",
        'G': "Grey"
    }
    total_amount = 0
    cart_list = []
    for cart_id in cart_dict:
        cart_item = cart_dict.get(cart_id)
        detail = Details.Details(cart_item['product_id'], cart_item['description'], colours[cart_item['color']], cart_item['qty'], get_product(cart_item['product_id']).get_price(), cart_id=int(cart_id))
        total_amount += int(detail.get_price()) * detail.get_qty()
        cart_list.append(detail)

    return render_template("retrieveOrders.html", count=len(cart_list), cart_list=cart_list, total_amount=total_amount)




#FOR GETTING THE PRODUCT ID
def get_product(product_id):
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()
    product = products_dict[int(product_id)]
    return product


#CART PAGE WHERE THE CUSTOMERS SELECTED ITEMS ARE AT
@app.route('/Cart', methods=["GET", "POST"])
def retrieve_cart():

    try:
        cart_dict = session['cart']  #read the 'cart' value and save it in cart_dict
    except KeyError:
        cart_dict = {}


    form = ConfirmPriceForm(request.form)
    if request.method == 'POST' and form.validate():
        product_id = int(form.product_id.data)
        product = get_product(product_id)

        #CUSTOMER SELECTS THE SAME ITEM, CHECK MODEL AND COLOR
        #UPDATE THE CART
        if len(cart_dict) == 0:
            detail = Details.Details(product.get_product_id(), product.get_sku_description(), form.color.data, int(form.qty.data), product.get_price())
            cart_dict[str(detail.get_cart_id())] = {
                'product_id': detail.get_product_id(),
                'description': detail.get_description(),
                'color': detail.get_color(),
                'qty': detail.get_qty(),
            }
        else:
            found = False
            for cart_id in cart_dict:
                cart_item = cart_dict.get(cart_id)
                if product.get_product_id() == int(cart_item['product_id']) and form.color.data == cart_item['color']:
                    cart_item['qty'] += int(form.qty.data)
                    if cart_item['qty'] > product.get_stock():
                        return "Out of Stock"
                    found = True
                    break

            if not found:
                detail = Details.Details(product.get_product_id(), product.get_sku_description(), form.color.data, int(form.qty.data), product.get_price())
                cart_dict[str(detail.get_cart_id())] = {
                    'product_id': detail.get_product_id(),
                    'description': detail.get_description(),
                    'color': detail.get_color(),
                    'qty': detail.get_qty(),
                }

                total_request_qty = 0
                for cart_id in cart_dict:
                    cart_item = cart_dict.get(cart_id)
                    if cart_item['product_id'] == product.get_product_id():
                        total_request_qty += cart_item['qty']
                if total_request_qty > product.get_stock():
                    return "Out of Stock"

        session['cart'] = cart_dict

    colours = {
        'B': "Black",
        'W': "White",
        'P': "Pink",
        'G': "Grey"
    }
    total_amount = 0
    cart_list = []
    for cart_id in cart_dict:
        cart_item = cart_dict.get(cart_id)
        detail = Details.Details(cart_item['product_id'], cart_item['description'], colours[cart_item['color']], cart_item['qty'], get_product(cart_item['product_id']).get_price(), cart_id=int(cart_id))
        total_amount += int(detail.get_price()) * detail.get_qty()
        cart_list.append(detail)

    return render_template("Cart.html", count=len(cart_list), cart_list=cart_list, total_amount=total_amount)


#FOR CUSTOMERS TO UPDATE QUANTITY OF THIER SELECTED PRODUCTS IN THE SHOPPING CART
@app.route('/updateCart/<string:cart_id>', methods=['GET', 'POST'])
def update_cart(cart_id):
    update_product_form = UpdateCartForm(request.form)
    try:
        cart_dict = session['cart']
    except KeyError:
        cart_dict = {}

    if cart_id not in cart_dict:
        return "Item not found"

    cart_item  = cart_dict[cart_id]
    if request.method == 'POST' and update_product_form.validate():
        #IDENTIFY MODEL AND COLOR AND UPDATE
        #CHECK THE QUANTITY IS ENOUGH?

        stock = get_product(cart_item['product_id']).get_stock()
        if int(update_product_form.qty.data) > stock:
            return 'Out of Stock'
        cart_item['color'] = update_product_form.color.data
        cart_item['qty'] = int(update_product_form.qty.data)
        session['cart'] = cart_dict


        return redirect(url_for('retrieve_cart'))
    else:

        update_product_form.product_id.data = cart_item['product_id']
        update_product_form.description.data = cart_item['description']
        update_product_form.color.data = cart_item['color']
        update_product_form.qty.data = cart_item['qty']
        update_product_form.price.data = get_product(cart_item['product_id']).get_price()

        return render_template('updateCart.html', form=update_product_form)


#FOR CUSTOMERS TO DELETE THEIR PRODUCTS IN THEIR SHOPPING CART
@app.route('/deleteCart/<string:cart_id>')
def delete_cart(cart_id):

    try:
        cart_dict = session['cart']
    except KeyError:
        cart_dict = {}
    if cart_id not in cart_dict:
        return "Item not found"
    else:
        del cart_dict[cart_id]
        session['cart'] = cart_dict


    return redirect(url_for('retrieve_cart'))


#SEARCH PRODUCT FOR CUSTOMER PRODUCTPAGE
@app.route('/searchProduct', methods=["GET", "POST"])
def searchproduct():
    search_product_form = searchProduct(request.form)
    if request.method == 'POST' and search_product_form.validate():
        search = search_product_form.s_name.data
        products_dict = {}
        db = shelve.open('product.db', 'r')
        products_dict = db['Products']
        db.close()

        products_list = []
        for key in products_dict:
            product = products_dict.get(key)

            if search.upper() in product.get_sku_description().upper():
                products_list.append(product)
            else:
                problem = print("Item not found in Product page or item not created in Product page yet!")
                continue
        if len(products_list) != 0:
            return render_template('productPage.html', count=len(products_list), products_list=products_list)
    return render_template('searchProduct.html', form=search_product_form)


#FOR CUSTOMERS TO BOOK APPOINTMENT
@app.route('/createAppointment', methods=['GET', 'POST'])
def create_appt():
    centre_dict = {}
    db = shelve.open('centre.db', 'r')
    centre_dict = db['Centre']
    db.close()

    choices_list = [('', 'Select')]
    for key in centre_dict:
        centre = centre_dict.get(key)
        choices_list.append((centre.get_code(), centre.get_name()))
    print(choices_list)

    create_appt_form = createAppointment(request.form)
    create_appt_form.location.choices = choices_list
    if request.method == 'POST' and create_appt_form.validate():
        appt_dict = {}
        db = shelve.open('appt.db', 'c')
        try:
            appt_dict = db['Appt']
        except:
            print('Error in retrieving appt.db')
        appointment = Appointment.Appointment(
            create_appt_form.first_name.data, create_appt_form.last_name.data,
            create_appt_form.username.data, create_appt_form.email.data,
            create_appt_form.location.data, create_appt_form.time.data,
            create_appt_form.date.data, create_appt_form.remarks.data)

        appt_dict[appointment.get_appt_id()] = appointment
        db['Appt'] = appt_dict

        appt_dict = db['Appt']
        appointment = appt_dict[appointment.get_appt_id()]
        print(appointment.get_first_name(), 'has booked an appointment successfully, appointment ID =', appointment.get_appt_id())
        db.close()

        return redirect(url_for('retrieve_appt'))
    return render_template('createAppointment.html', form=create_appt_form)



#RETRIEVE APPOINTMENT FOR BACKEND
@app.route('/retrieveAppointment')
def retrieve_appt():
    appt_dict = {}
    db = shelve.open('appt.db', 'r')
    appt_dict = db['Appt']
    db.close()

    appt_list = []
    print(appt_dict)
    for key in appt_dict:
        Appointment = appt_dict.get(key)
        appt_list.append(Appointment)


    return render_template('retrieveAppointment.html', count=len(appt_list), appt_list=appt_list)


#UPDATE CUSTOMER APPOINTMENT FOR BACKEND
@app.route('/updateAppointment/<int:id>', methods=['GET', 'POST'])
def update_appt(id):
    centre_dict = {}
    db = shelve.open('centre.db', 'r')
    centre_dict = db['Centre']
    db.close()

    choices_list = [('', 'Select')]
    for key in centre_dict:
        centre = centre_dict.get(key)
        choices_list.append((centre.get_code(), centre.get_name()))
    print(choices_list)

    update_appointment_form = createAppointment(request.form)
    update_appointment_form.location.choices = choices_list
    if request.method == 'POST' and update_appointment_form.validate():
        appt_dict = {}
        db = shelve.open('appt.db', 'w')
        appt_dict = db['Appt']
        appt = appt_dict.get(id)
        appt.set_first_name(update_appointment_form.first_name.data)
        appt.set_last_name(update_appointment_form.last_name.data)
        appt.set_username(update_appointment_form.username.data)
        appt.set_email(update_appointment_form.email.data)
        appt.set_location(update_appointment_form.location.data)
        appt.set_time(update_appointment_form.time.data)
        appt.set_date(update_appointment_form.date.data)
        appt.set_remarks(update_appointment_form.remarks.data)

        db['Appt'] = appt_dict
        db.close()


        return redirect(url_for('retrieve_appt'))
    else:
        appt_dict = {}
        db = shelve.open('appt.db', 'r')
        appt_dict = db['Appt']
        db.close()

        appt = appt_dict.get(id)
        update_appointment_form.first_name.data = appt.get_first_name()
        update_appointment_form.last_name.data = appt.get_last_name()
        update_appointment_form.username.data = appt.get_username()
        update_appointment_form.email.data = appt.get_email()
        update_appointment_form.location.data = appt.get_location()
        update_appointment_form.time.data = appt.get_time()
        update_appointment_form.date.data = appt.get_date()
        update_appointment_form.remarks.data = appt.get_remarks()

        return render_template('updateAppointment.html', form=update_appointment_form)


#DELETE CUSTOMER APPOINTMENT FOR BACKEND
@app.route('/deleteAppt/<int:id>', methods=['POST'])
def delete_appt(id):
    appt_dict = {}
    db = shelve.open('appt.db', 'w')
    appt_dict = db['Appt']

    appt_dict.pop(id)

    db['Appt'] = appt_dict
    db.close()

    return redirect(url_for('retrieve_appt'))


#SEARCH APPOINTMENT FOR BACKEND
@app.route('/searchAppointment', methods=["GET", "POST"])
def search_appt():
    search_appt_form = searchAppointment(request.form)
    if request.method == 'POST' and search_appt_form.validate():
        search = search_appt_form.s_name.data
        appt_dict = {}
        db = shelve.open('appt.db', 'r')
        appt_dict = db['Appt']
        db.close()

        appt_list = []
        for key in appt_dict:
            appt = appt_dict.get(key)

            if search.upper() in appt.get_first_name().upper():
                appt_list.append(appt)
            else:
                continue
        if len(appt_list) != 0:
            return render_template('showAppointment.html', count=len(appt_list), appt_list=appt_list)
        else:
            return()


    return render_template('searchAppointment.html', form=search_appt_form)


#FILTER APPOINTMENT FOR BACKEND
@app.route('/filterAppointment', methods=["GET","POST"])
def filter_appt():
    centre_dict = {}
    db = shelve.open('centre.db', 'r')
    centre_dict = db['Centre']
    db.close()

    choices_list = [('', 'Select')]
    for key in centre_dict:
        centre = centre_dict.get(key)
        choices_list.append((centre.get_code(), centre.get_name()))
    print(choices_list)

    filter_appt_form = filterAppointment(request.form)
    filter_appt_form.f_location.choices = choices_list
    if request.method == 'POST' and filter_appt_form.validate():
        counter = 0
        filter_location = filter_appt_form.f_location.data
        if filter_location != '':
            counter += 1
        filter_date = filter_appt_form.f_date.data
        if filter_date != None:
            counter += 1
        print(counter)
        appt_dict = {}
        db =  shelve.open('appt.db', 'r')
        appt_dict = db['Appt']
        db.close()

        appt_list = []
        for key in appt_dict:
            appt = appt_dict.get(key)

            if counter == 2:
                if appt.get_location() == filter_location and appt.get_date() == filter_date:
                    appt_list.append(appt)
            elif counter == 1:
                if appt.get_location() == filter_location or appt.get_date() == filter_date:
                    appt_list.append(appt)
            else:
                continue


        if len(appt_list) != 0:
            return render_template('showAppointment1.html', count=len(appt_list), appt_list=appt_list)

    return render_template('filterAppointment.html', form=filter_appt_form)





#CREATE CENTRE FOR BACKEND
@app.route('/createCentre', methods=['GET', 'POST'])
def create_centre():
    create_centre_form = createCentre(request.form)
    if request.method == 'POST' and create_centre_form.validate():
        centre_dict = {}
        db = shelve.open('centre.db', 'c')
        try:
            centre_dict = db['Centre']
        except:
            print('error in retrieving centre.db')
        centre = Centre.Centre(
            create_centre_form.name.data,
            create_centre_form.id.data,
            create_centre_form.area.data,
            create_centre_form.type.data
        )

        centre_dict[centre.get_centre_id()] = centre
        db['Centre'] = centre_dict

        centre_dict = db['Centre']
        centre = centre_dict[centre.get_centre_id()]
        print(centre.get_name(), 'has been successfully registered')
        db.close()

        return redirect(url_for('home'))
    return render_template('createCentre.html', form=create_centre_form)


#RETRIEVE CENTRE FOR BACKEND
@app.route('/retrieveCentre', methods=['GET', 'POST'])
def retrieve_centre():
    centre_dict = {}
    db = shelve.open('centre.db', 'r')
    centre_dict = db['Centre']
    db.close()

    centre_list = []
    print(centre_dict)
    for key in centre_dict:
        centre = centre_dict.get(key)
        centre_list.append(centre)

    filter_centre_form = filterCentre(request.form)
    if request.method == 'POST' and filter_centre_form.validate():
        filter_type = filter_centre_form.f_type.data
        centre_dict_1 = {}
        db = shelve.open('centre.db', 'r')
        centre_dict_1 = db['Centre']
        db.close()

        centre_list_1 = []
        for key in centre_dict_1:
            centre = centre_dict_1.get(key)
            if centre.get_type() == filter_type:
                centre_list_1.append(centre)
            else:
                continue
        if len(centre_list_1) != 0:
            return render_template('showCentre.html', count=len(centre_list_1), centre_list_1=centre_list_1)

    return render_template('retrieveCentre.html', count=len(centre_list), centre_list=centre_list, form=filter_centre_form)


#UPDATE CENTRE FOR BACKEND
@app.route('/updateCentre/<int:id>', methods=['GET', 'POST'])
def update_centre(id):
    update_centre_form = createCentre(request.form)
    if request.method == 'POST' and update_centre_form.validate():
        centre_dict = {}
        db = shelve.open('centre.db', 'w')
        centre_dict = db['Centre']
        centre = centre_dict.get(id)
        centre.set_name(update_centre_form.name.data)
        centre.set_code(update_centre_form.id.data)
        centre.set_location(update_centre_form.area.data)
        centre.set_type(update_centre_form.type.data)

        db['Centre'] = centre_dict
        db.close()

        return redirect(url_for('retrieve_centre'))
    else:
        centre_dict = {}
        db = shelve.open('centre.db', 'r')
        centre_dict = db['Centre']
        db.close()

        centre = centre_dict.get(id)
        update_centre_form.name.data = centre.get_name()
        update_centre_form.id.data = centre.get_code()
        update_centre_form.area.data = centre.get_location()
        update_centre_form.type.data = centre.get_type()

        return render_template('updateCentre.html', form=update_centre_form)



#DELETE CENTRE FOR BACKEND
@app.route('/deleteCentre/<int:id>', methods=['POST'])
def delete_centre(id):
    centre_dict = {}
    db = shelve.open('centre.db', 'w')
    centre_dict = db['Centre']

    centre_dict.pop(id)

    db['Centre'] = centre_dict
    db.close()

    return redirect(url_for('retrieve_centre'))

#SHOW ALL CENTRES FOR CUSTOMERS THAT ARE AVALIABLE FOR BOOKING
@app.route('/bookCentre')
def book_centre():
    centre_dict = {}
    db = shelve.open('centre.db', 'r')
    centre_dict = db['Centre']
    db.close()

    centre_list = []
    print(centre_dict)
    for key in centre_dict:
        centre = centre_dict.get(key)
        centre_list.append(centre)

    return render_template('bookCentre.html', centre_list=centre_list, count=len(centre_list))

#WHEN PRESSED BOOK IN bookCentre
@app.route('/book/<int:id>', methods=['GET', 'POST'])
def book(id):
    centre_dict = {}
    db = shelve.open('centre.db', 'r')
    centre_dict = db['Centre']
    db.close()

    choices_list = [('', 'Select')]
    for key in centre_dict:
        centre = centre_dict.get(key)
        choices_list.append((centre.get_code(), centre.get_name()))
    print(choices_list)

    booking_form = createAppointment(request.form)
    booking_form.location.choices = choices_list
    booking_form.location.default = {centre_dict.get(id).get_code()}
    print(centre_dict.get(id).get_code())
    if request.method == 'POST' and booking_form.validate():
        appt_dict = {}
        db = shelve.open('appt.db', 'c')
        try:
            appt_dict = db['Appt']
        except:
            print('Error in retrieving appt.db')
        appointment = Appointment.Appointment(
            booking_form.first_name.data, booking_form.last_name.data,
            booking_form.username.data, booking_form.email.data,
            booking_form.location.data, booking_form.time.data,
            booking_form.date.data, booking_form.remarks.data)

        appt_dict[appointment.get_appt_id()] = appointment
        db['Appt'] = appt_dict

        appt_dict = db['Appt']
        appointment = appt_dict[appointment.get_appt_id()]
        print(appointment.get_first_name(), 'has booked an appointment successfully, appointment ID =', appointment.get_appt_id())
        db.close()

        return render_template('confirmation.html', appointment=appointment)
    return render_template('createAppointment.html', form=booking_form)




#SIGNUP PAGE FOR CUSTOMER
@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        customer = Customer.Customer(create_customer_form.username.data,
                    create_customer_form.first_name.data, create_customer_form.last_name.data,
                    create_customer_form.email.data, create_customer_form.mobile_number.data,
                    create_customer_form.date_joined.data, create_customer_form.address.data,
                    create_customer_form.password.data, create_customer_form.confirm_password.data
                                     )


        customers_dict[customer.get_customer_id()] = customer
        db['Customers'] = customers_dict

        customers_dict = db['Customers']
        customer = customers_dict[customer.get_customer_id()]
        print(customer.get_first_name(), customer.get_last_name(), "was stored in customer.db successfully with customer_id ==", customer.get_customer_id())

        db.close()

        session['user_created'] = customer.get_first_name() + ' ' + customer.get_last_name()

        return redirect(url_for('home'))
    return render_template('createCustomer.html', form=create_customer_form)


#ADMIN ACCOUNT DETAILS
@app.route('/createAdmin', methods=['GET', 'POST'])
def create_admin():
    if request.method == 'POST':
        admins_dict = {"email": "admin@gmail.com", "password": "lol"}
        db = shelve.open('admin.db', 'c')

        try:
            admins_dict = db['Admins']
        except:
            print("Error in retrieving Admins from admin.db.")

        admin = Admin.Admin(
                           )


        admins_dict[admin.get_admin_id()] = admin
        db['Admins'] = admins_dict


        admins_dict = db['Admins']
        admin = admins_dict[admin.get_admin_id()]




        db.close()

        return redirect(url_for('retrieve_admins'))
    return render_template('retrieveAdmin.html')




#LOGIN FUNCTION PAGE
@app.route("/login", methods=["GET", "POST"])
def login():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    admins_dict = {"email": "admin@gmail.com", "password": "lol"}
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        email = request.form["email"]
        password = request.form['password']
        x = 0
        if email == admins_dict['email'] and password == admins_dict['password']:
            session['admins_dict'] = email
            return redirect('/home')  #change the link

        else:
            for i in customers_dict:
                if email == customers_dict.get(i).get_email():
                    if password == customers_dict.get(i).get_password():
                        session['customers_dict'] = email
                        print("Login successful")
                        x = 0
                        break
                    else:
                        print("incorrect password")
                        x += 1


                else:
                    print("incorrect email")
                    x += 1

        if x == 0:
            session['customers_dict'] = email
            return redirect('/home')
        else:
            return redirect('/login')




    return render_template('login.html', form=login_form)


#LOGOUT FOR CUSTOMER AND ADMIN
@app.route("/logout")
def logout():
    admins_dict = {"email": "admin@gmail.com", "password": "lol"}
    customers_dict = {}

    session.clear()
    return redirect("/home")


#RETRIEVE ADMIN DETAILS
@app.route('/retrieveAdmin')
def retrieve_admin():
    admins_dict = {"username": "admin","email": "admin@gmail.com", "password": "lol"}

    admins_list = []
    for key in admins_dict:
        admin = admins_dict.get(key)
        admins_list.append(admin)

    print(admins_list)
    return render_template('retrieveAdmin.html', count=len(admins_list), admins_list=admins_list)


#RETRIEVE ALL CUSTOMERS FOR BACKEND
@app.route('/retrieveCustomers')
def retrieve_customers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)


#UPDATE ADMIN DETAILS
@app.route('/updateAdmin/<int:id>/', methods=['GET', 'POST'])
def update_admin(id):
    update_admin_form = updateAdminForm(request.form)
    if request.method == 'POST' and update_admin_form.validate():
        admins_dict = {}
        db = shelve.open('admin.db', 'w')
        admins_dict = db['Admins']

        admin = admins_dict.get(id)
        admin.set_username(update_admin_form.username.data)
        admin.set_password(update_admin_form.password.data)
        admin.set_email(update_admin_form.email.data)

        db['Admins'] = admins_dict
        db.close()


        return redirect(url_for('retrieve_admins'))
    else:
        admins_dict = {}
        db = shelve.open('admin.db', 'r')
        admins_dict = db['Admins']
        db.close()

        admin = admins_dict.get(id)
        update_admin_form.username.data = admin.get_username()
        update_admin_form.password.data = admin.get_password()
        update_admin_form.email.data = admin.get_email()

        return render_template('updateAdmin.html', form=update_admin_form)


#UPDATE CUSTOMER DETAILS FOR BACKEND
@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = updateCustomerForm(request.form)
    try:
        customer_dict = session['Customers']
    except KeyError:
        customer_dict = {}

    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']
        customer = customers_dict.get(id)


        customer.set_username(update_customer_form.username.data)
        customer.set_mobile_number(update_customer_form.mobile_number.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_address(update_customer_form.address.data)

        db['Customers'] = customers_dict
        db.close()

        session['customer_updated'] = customer.get_first_name() + ' ' + customer.get_last_name()


        return redirect(url_for('retrieve_customers'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.username.data = customer.get_username()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.mobile_number.data = customer.get_mobile_number()
        update_customer_form.address.data = customer.get_address()
        return render_template('updateCustomer.html', form=update_customer_form)




#DELETE CUSTOMERS FOR BACKEND
@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customer.db', 'w')
    customers_dict = db['Customers']

    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('retrieve_customers'))





if __name__ == '__main__':
    app.run(debug = True)

