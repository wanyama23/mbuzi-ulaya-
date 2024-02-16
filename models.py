from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
# from sqlalchemy import MetaData, UniqueConstraint, ForeignKey
from sqlalchemy import UniqueConstraint, ForeignKey

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })


db = SQLAlchemy()
# db = SQLAlchemy(metadata=metadata)



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    address = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String)
    profile_pic = db.Column(db.String(255))
    isAdmin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # relationships
    orders = db.relationship('Order', back_populates='user', cascade='all, delete-orphan')
    cart = db.relationship('Cart', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'(id={self.id}, username={self.username}, email={self.email}, profile_pic={self.profile_pic})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    


class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fullnames = db.Column(db.String)
    business_name = db.Column(db.String)
    mobile_number = db.Column(db.String)
    email_address = db.Column(db.String)
    physical_address = db.Column(db.String)
    county = db.Column(db.String)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    product_list = db.Column(db.String)
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # relationships
    products = db.relationship('Product', back_populates='vendor', cascade='all, delete-orphan')
    orders = association_proxy('products', 'orders')

    # association proxy relationships
    orderproducts = db.relationship('OrderProducts', back_populates='vendor', cascade='all, delete-orphan')
    orders = association_proxy('orderproducts','orders')
    
    def __repr__(self):
        return f'(id={self.id}, businessName={self.business_name}, email={self.email_address}, mobile_number={self.mobile_number}, product_list={self.product_list})'
    


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    __table_args__ = (UniqueConstraint('name', name='category_name_unique_constraint'),)

    # relationships
    products = db.relationship('Product', back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f'(id={self.id}, name={self.name})'

class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # relationships
    user = db.relationship('User', back_populates='cart', uselist=False)
    cartItems = db.relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')

    def __repr__(self):
        return f'(id={self.id}, user_id={self.user_id})'

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    added_at = db.Column(db.DateTime, server_default=db.func.now())
    amount = db.Column(db.Float)

    # relationships
    cart = db.relationship('Cart', back_populates='cartItems')
    product = db.relationship('Product')

    def __repr__(self):
        return f'(id={self.id}, cart_id={self.cart_id}, product_id={self.product_id}, quantity={self.quantity})'

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    product_code = db.Column(db.String)
    price = db.Column(db.Numeric(precision=10, scale=2))
    vendor_id = db.Column(db.Integer, ForeignKey('vendors.id', ondelete='CASCADE'))
    category_id = db.Column(db.Integer, ForeignKey('categories.id', ondelete='CASCADE'))
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    __table_args__ = (UniqueConstraint('name', name='product_name_unique_constraint'),)

    # relationships 
    vendor = db.relationship('Vendor', back_populates='products')
    category = db.relationship('Category', back_populates='products')
    orders = db.relationship('Order', back_populates='product', cascade='all, delete-orphan')

    # association proxy relationships
    orderproducts = db.relationship('OrderProducts', back_populates='products', cascade='all, delete-orphan')
    orders = association_proxy('orderproducts','orders')

    def __repr__(self):
        return f'(id={self.id}, name={self.name} description={self.description} price={self.price} price={self.image} user_id={self.user_id} category_id={self.category_id} )'


class OrderProducts(db.Model):
    __tablename__ = 'order_products'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    amount = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    # Relationships
    products = db.relationship('Product', back_populates='orderproducts')
    orders = db.relationship('Order', back_populates='orderproducts')
    vendor = db.relationship('Vendor', back_populates='orderproducts')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String, default="Ordered")
    delivery_type = db.Column(db.String)
    phone_number = db.Column(db.String)
    shipping_address = db.Column(db.String)
    county = db.Column(db.String)
    email = db.Column(db.String)
    amount = db.Column(db.Integer)
    full_name = db.Column(db.String)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    payment_uid = db.Column(db.String, db.ForeignKey('payments.payment_uid'))

    # relationships
    user = db.relationship('User', back_populates='orders')
    payment = db.relationship('Payment', back_populates='order')

    # association proxy relationships
    orderproducts = db.relationship('OrderProducts', back_populates='order', cascade='all, delete-orphan')
    products = association_proxy('orderproducts','products')

    @validates('orderproducts')
    def validate_cart_item(self, key, orderproducts):
        if orderproducts.product.vendor_id == self.user_id:
            raise ValueError("You cannot buy your own product.")
        return orderproducts

    def __repr__(self):
        return f'(id={self.id}, user_id={self.user_id}, status={self.status}, delivery_type={self.delivery_type}, phone_number={self.phone_number}, shipping_address={self.shipping_address}, county={self.county}, email={self.email}, amount={self.amount}, full_name={self.full_name}, date_created={self.date_created}, payment_uid={self.payment_uid})'


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    mpesa_receipt_code = db.Column(db.String)
    payment_date = db.Column(db.String)
    paid_by_number = db.Column(db.String)
    amount_paid = db.Column(db.Integer)
    payment_uid = db.Column(db.String)
    date_created = db.Column(db.DateTime, server_default=db.func.now())

    order = db.relationship('Order', back_populates='payment')
    

    def __repr__(self):
        return f'(id={self.id}, payment_uid={self.payment_uid}, mpesa_receipt_code={self.mpesa_receipt_code}, amount_paid={self.amount_paid}, payment_date={self.payment_date})'

class UploadedImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)

# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     public_id = db.Column(db.String)
#     username = db.Column(db.String)
#     first_name = db.Column(db.String)
#     last_name = db.Column(db.String)
#     address = db.Column(db.String)
#     phone_number = db.Column(db.String)
#     email = db.Column(db.String)
#     password_hash = db.Column(db.String)
#     profile_pic = db.Column(db.String(255))
#     isAdmin = db.Column(db.Boolean,default=False)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#     # relationships
#     orders = db.relationship('Order', back_populates='user', cascade='all, delete-orphan')
#     cart = db.relationship('Cart', back_populates='user', cascade='all, delete-orphan')

#     __table_args__ = (
#     UniqueConstraint('username', name='user_unique_constraint'),
#     UniqueConstraint('email', name='email_unique_constraint')
#     )


#     def __repr__(self):
#         return f'(id={self.id}, name={self.username} email={self.email} profile_pic={self.profile_pic})'

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

#     def check_password(self, password):
#         return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

# class Vendor(db.Model):
#     __tablename__ = 'vendors'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     fullnames = db.Column(db.String)
#     business_name = db.Column(db.String)
#     mobile_number = db.Column(db.String)
#     email_address = db.Column(db.String)
#     physical_address = db.Column(db.String)
#     county = db.Column(db.String)
#     longitude = db.Column(db.Float)
#     latitude = db.Column(db.Float)
#     product_list = db.Column(db.String)
#     image = db.Column(db.String(255))
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#     # relationships
#     products = db.relationship('Product', back_populates='vendor', cascade='all, delete-orphan')
#     orders = association_proxy('products', 'orders')

#     # association proxy relationships
#     orderproducts = db.relationship('OrderProducts', back_populates='vendor', cascade='all, delete-orphan')
#     orders = association_proxy('orderproducts','orders')
    
#     def __repr__(self):
#         return f'(id={self.id}, businessName={self.business_name} email={self.email_address} mobile_number={self.mobile_number} product_list={self.product_list} )'






# class Category(db.Model):
#     __tablename__ = 'categories'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     image = db.Column(db.String)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#     __table_args__ = (UniqueConstraint('name', name='category_name_unique_constraint'),)

#     # relationships
#     products = db.relationship('Product', back_populates='category', cascade='all, delete-orphan')

#     def __repr__(self):
#         return f'(id={self.id}, name={self.name})'
    



# class OrderProducts(db.Model):
#     __tablename__ = 'order_products'

#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
#     vendor_id  = db.Column(db.Integer, db.ForeignKey('vendors.id'))
#     amount = db.Column(db.Integer)
#     quantity = db.Column(db.Integer)

#     # relationships
#     products = db.relationship('Product', back_populates='orderproducts')
#     orders = db.relationship('Order',back_populates='orderproducts')
#     vendor = db.relationship('Vendor', back_populates ='orderproducts')
    

# class Order(db.Model):
#     __tablename__ = 'orders'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     status = db.Column(db.String, default="Ordered")
#     delivery_type = db.Column(db.String)
#     phone_number = db.Column(db.String)
#     shipping_address = db.Column(db.String)
#     county = db.Column(db.String)
#     email = db.Column(db.String)
#     amount = db.Column(db.Integer)
#     full_name = db.Column(db.String)
#     date_created = db.Column(db.DateTime, server_default=db.func.now())
#     payment_uid = db.Column(db.String, db.ForeignKey('payments.payment_uid'))

#     # relationships
#     user = db.relationship('User', back_populates='orders')
#     payment = db.relationship('Payment', back_populates='order')

#     # association proxy relationships
#     orderproducts = db.relationship('OrderProducts', back_populates='orders', cascade='all, delete-orphan')
#     products = association_proxy('orderproducts','products')

#     @validates('cart_item')
#     def validate_cart_item(self, key, cart_item):
#         if cart_item.product.vendor_id == self.user_id:
#             raise ValueError("You cannot buy your own product.")
#         return cart_item

#     def __repr__(self):
#         return f'(id={self.id}, product_id={self.product_id}, user_id={self.user_id}, purchased_at={self.purchased_at})'


