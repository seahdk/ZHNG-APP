from wtforms import Form, StringField, SelectField, validators, BooleanField, EmailField, RadioField, DateField, DecimalField, IntegerField, FileField,SubmitField, TextAreaField, HiddenField,PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, NumberRange, input_required,EqualTo
from flask_wtf.file import FileAllowed, FileRequired, ValidationError
from datetime import date

time_list = [('', 'Select'), ('09:00', '9AM'), ('11:00', '11AM'), ('13:00', '1PM'), ('15:00', '3PM'),('17:00', '5PM')]
type_list = [('', 'Select'), ('Car', 'Car'), ('Motorcycle', 'Motorcycle'), ('Bicycle', 'Bicycle')]



class createProductForm(FlaskForm):  #for backend
    sku = StringField('sku', validators=[DataRequired()])
    sku_description = StringField('sku_description', validators=[DataRequired()])
    price = DecimalField('price', validators=[DataRequired()])
    stock = IntegerField('stock', validators=[input_required()])
    image = FileField('image',validators=[FileAllowed(['jpg', 'png','jpeg','gif'], 'we only accept JPG or PNG images.')])
    Add = SubmitField('Add')


class CreateCartForm(Form):     #for frontend
    description = SelectField('Description (SKU)')
    color = SelectField('Color', [validators.DataRequired()], choices=[('', 'Select'), ('B', 'Black'), ('W', 'White'), ('P', 'Pink'), ('G', 'Grey')], default='')
    qty = StringField('QTY', [validators.Length(min=1, max=150), validators.DataRequired()])


class ConfirmPriceForm(Form):
    product_id = HiddenField()
    description = StringField('Description (SKU)',render_kw={"readonly": "true"})
    color = SelectField('Color', choices=[('', 'Select'), ('B', 'Black'), ('W', 'White'), ('P', 'Pink'), ('G', 'Grey')], render_kw={"readonly": "true"})
    qty = StringField('QTY', render_kw={"readonly": "true"})
    price = StringField('Price', render_kw={"readonly": "true"})
    

class UpdateInventoryForm(FlaskForm):
    sku = StringField('SKU', validators=[DataRequired()], render_kw={'readonly': True})
    sku_description = StringField('SKU Description', validators=[DataRequired()], render_kw={'readonly': True})
    price = DecimalField('Price', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[input_required()])
    image = FileField("Update Image")
    update = SubmitField('Add')


class UpdateCartForm(Form):    #FOR FRONTEND (JX)
    product_id = StringField('Product ID', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={'readonly':True})
    description = StringField('Description (SKU)', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={'readonly':True})
    color = SelectField('Color', [validators.DataRequired()], choices=[('', 'Select'), ('B', 'Black'), ('W', 'White'), ('P', 'Pink'), ('G', 'Grey')], default='')
    qty = StringField('QTY', [validators.Length(min=1, max=150), validators.DataRequired()])
    price = StringField('Price', [validators.length(max=200), validators.DataRequired()], render_kw={'readonly':True})

class shippingform(Form):
    first_name = StringField('First Name', [validators.length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.length(min=1, max=150), validators.DataRequired()])
    emailaddress = EmailField('Email Address', [validators.length(min=1, max=150), validators.DataRequired()])
    address = StringField('Address', [validators.length(min=1, max=150), validators.DataRequired()])
    unitno = StringField('Unit Number', [validators.length(min=1, max=150), validators.DataRequired()])
    contact = StringField('Contact', [validators.length(min=1, max=150), validators.DataRequired()])
    checkbox = BooleanField('Billing Address to be same as Shipping Address.')

class paymentform(Form):
    card_type = RadioField("Card Type", choices=[('Visa'), ('Mastercard'), ('UnionPay'), ('FavePay')], default='')
    card_number = StringField('Card Number', [validators.length(min=16, max=16), validators.DataRequired()])
    name_on_card = StringField('Name on Card', [validators.length(min=1, max=150), validators.DataRequired()])
    expiry_date = DateField('Expiry Date', format='%Y-%m-%d')
    cvvcode = StringField('CVV Code', [validators.Length(min=3, max=3), validators.DataRequired()])
    promocode = StringField('Promo Code', [validators.Optional(), validators.Length(min=1, max=5)])

#search function
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField('Submit')


class createPromoForm(FlaskForm):  #create promo for backend
    code = StringField('code', validators=[input_required(), Length(min=1, max=10)])
    discount = IntegerField('discount', validators=[input_required(), NumberRange(0,100)]) #number range changes
    quantity = IntegerField('quantity', validators=[input_required()])
    expiry = DateField('expiry', format='%Y-%m-%d' , validators=[input_required()])
    notes = StringField('notes', validators=[input_required()])
    status = RadioField('status', choices=[('A', 'Avaliable'), ('U', 'unavaliable')], default='A')
    Add = SubmitField('Add')
    Cancel = SubmitField('Cancel')

    def validate_discount(form,discount):
        if discount.data < 1 or discount.data > 100:
            raise ValidationError("Please enter a range between 1 to 100")

class searchProduct(Form):
    s_name = StringField('Name:', [validators.Length(min=2, max=50), validators.DataRequired()])






#jon forms

class createAppointment(Form):
    first_name = StringField('First Name:', [validators.Length(min=2, max=50), validators.DataRequired()], render_kw={"placeholder":"e.g. John "})
    last_name = StringField("Last Name:", [validators.Length(min=2, max=50), validators.DataRequired()], render_kw={"placeholder":"e.g. Tan "})
    username = StringField('Username (optional):', [validators.optional()])
    email = EmailField('Email:', [validators.email(), validators.data_required()], render_kw={"placeholder":"e.g. johntan@gmail.com"})
    location = SelectField('Location:', [validators.DataRequired()],  default='')
    time = SelectField('Time', [validators.DataRequired()], choices=time_list, default='')
    date = DateField('Date', [validators.DataRequired()], format='%Y-%m-%d')
    remarks = TextAreaField('Remarks', [validators.Optional()])

    def validate_location(Form, location):
        if location == '':
            raise ValidationError('Please select a location')
    def validate_time(Form, time):
        if time == '':
            raise ValidationError('Please select a time')


class searchAppointment(Form):
    s_name = StringField('Name:', [validators.Length(min=2, max=50), validators.DataRequired()])

class filterAppointment(Form):
    f_location = SelectField('Location:',  [validators.optional()], default='')
    f_date = DateField('Date:', [validators.optional()], format='%Y-%m-%d')


class createCentre(Form):
    name = StringField('Centre Name:', [validators.length(min=5, max=100), validators.DataRequired()], render_kw={"placeholder":"e.g. Yio Chu Kang Serving Centre"})
    id = StringField('Centre ID:', [validators.length(min=1, max=4), validators.DataRequired()], render_kw={"placeholder":"e.g. YCK"})
    area = StringField('Centre location:', [validators.length(min=5, max=100), validators.DataRequired()], render_kw={"placeholder":"e.g. Yio Chu Kang st 69"})
    type = RadioField('Centre type:', choices=type_list, default='')

    def validate_type(Form, type):
        if type == '':
            raise ValidationError("Please select a type")


class filterCentre(Form):
    f_type = SelectField('Filter Type:', [validators.DataRequired()], choices=type_list, default='')




#Damien part
def current_date():
    return date.today()

class CreateCustomerForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d', default=current_date(), render_kw={'readonly':True})
    mobile_number = StringField('Mobile Number', [validators.Length(min=8, max=8), validators.DataRequired()])
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8, max=150), validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password', [validators.Length(min=8, max=150), validators.DataRequired(), EqualTo('password')])



    def validate_mobile_number(Form, mobile_number):
        if not mobile_number.data.startswith(("8", "9")):
            raise ValidationError("Mobile number must start with 8 or 9")



class LoginForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])


class RequestResetForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8, max=150), validators.DataRequired()])


class updateAdminForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=8, max=150), validators.DataRequired()])

class updateCustomerForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    mobile_number = StringField('Mobile Number', [validators.Length(min=8, max=8), validators.DataRequired()])
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
