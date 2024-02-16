from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import os
import bcrypt
from models import db, User, Payment, Order, Vendor, Product, Cart, Category, CartItem, UploadedImage


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
# db = SQLAlchemy(app)


# ......................................user route.......................
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # Extract user data from the request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')  # You should hash this before storing it

    # Validate input
    if not all([username, email, password]):
        return jsonify({'error': 'Invalid input'}), 400

    # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409

    # Create a new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)  # Set the hashed password

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

# @app.route('/compte', methods=['GET', 'POST'])
# @login_required
# def compte():
#     form = RegistrationForm()  # Assuming you have a registration form defined
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(
#             username=form.username.data,
#             email=form.email.data,
#             password_hash=hashed_password,
#             # Other user attributes...
#         )
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('compte'))
#     elif request.method == 'GET':
#         users = User.query.order_by(User.username).all()
#         return render_template('compte.html', form=form, users=users)

# @app.route('/users', methods=['GET'])
# def get_all_users():
#     users = User.query.all()
#     output = []
#     for user in users:
#         user_data = {}
#         user_data['id'] = user.id
#         user_data['public_id'] = user.public_id
#         user_data['username'] = user.username
#         user_data['first_name'] = user.first_name
#         user_data['last_name'] = user.last_name
#         user_data['address'] = user.address
#         user_data['phone_number'] = user.phone_number
#         user_data['email'] = user.email
#         user_data['profile_pic'] = user.profile_pic
#         user_data['isAdmin'] = user.isAdmin
#         output.append(user_data)
#     return jsonify({'users': output})

# @app.route('/users/<user_id>', methods=['GET'])
# def get_one_user(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     if not user:
#         return jsonify({'message': 'No user found!'})
#     user_data = {}
#     user_data['id'] = user.id
#     user_data['public_id'] = user.public_id
#     user_data['username'] = user.username
#     user_data['first_name'] = user.first_name
#     user_data['last_name'] = user.last_name
#     user_data['address'] = user.address
#     user_data['phone_number'] = user.phone_number
#     user_data['email'] = user.email
#     user_data['profile_pic'] = user.profile_pic
#     user_data['isAdmin'] = user.isAdmin
#     return jsonify({'user': user_data})

# @app.route('/users', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     new_user = User(public_id=str(uuid.uuid4()), username=data['username'], first_name=data['first_name'], last_name=data['last_name'], address=data['address'], phone_number=data['phone_number'], email=data['email'], profile_pic=data['profile_pic'], isAdmin=data['isAdmin'])
#     new_user.set_password(data['password'])
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'New user created!'})

# @app.route('/users/<user_id>', methods=['PUT'])
# def promote_user(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     if not user:
#         return jsonify({'message': 'No user found!'})
#     user.isAdmin = True
#     db.session.commit()
#     return jsonify({'message': 'The user has been promoted!'})

# @app.route('/users/<user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     if not user:
#         return jsonify({'message': 'No user found!'})
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({'message': 'The user has been deleted!'})



# .................................payments route........................
@app.route('/payments', methods=['GET'])
def get_all_payments():
    payments = Payment.query.all()
    return jsonify([payment.__repr__() for payment in payments])

@app.route('/payments/<int:id>', methods=['GET'])
def get_payment_by_id(id):
    payment = Payment.query.get(id)
    return payment.__repr__()

@app.route('/payments', methods=['POST'])
def add_payment():
    new_payment = Payment(
        mpesa_receipt_code=request.json['mpesa_receipt_code'],
        payment_date=request.json['payment_date'],
        paid_by_number=request.json['paid_by_number'],
        amount_paid=request.json['amount_paid'],
        payment_uid=request.json['payment_uid']
    )
    db.session.add(new_payment)
    db.session.commit()
    return new_payment.__repr__()

@app.route('/payments/<int:id>', methods=['PUT'])
def update_payment(id):
    payment = Payment.query.get(id)
    payment.mpesa_receipt_code = request.json['mpesa_receipt_code']
    payment.payment_date = request.json['payment_date']
    payment.paid_by_number = request.json['paid_by_number']
    payment.amount_paid = request.json['amount_paid']
    payment.payment_uid = request.json['payment_uid']
    db.session.commit()
    return payment.__repr__()

@app.route('/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    payment = Payment.query.get(id)
    db.session.delete(payment)
    db.session.commit()
    return payment.__repr__()


# ...................................order route....................
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = Order(**data)
    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully!'}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.__dict__), 200

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(order, key, value)
    db.session.commit()
    return jsonify({'message': 'Order updated successfully!'}), 200

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully!'}), 200


# ...................vendor route........................
@app.route('/vendors', methods=['GET'])
def get_all_vendors():
    vendors = Vendor.query.all()
    output = []
    for vendor in vendors:
        vendor_data = {}
        vendor_data['id'] = vendor.id
        vendor_data['user_id'] = vendor.user_id
        vendor_data['fullnames'] = vendor.fullnames
        vendor_data['business_name'] = vendor.business_name
        vendor_data['mobile_number'] = vendor.mobile_number
        vendor_data['email_address'] = vendor.email_address
        vendor_data['physical_address'] = vendor.physical_address
        vendor_data['county'] = vendor.county
        vendor_data['longitude'] = vendor.longitude
        vendor_data['latitude'] = vendor.latitude
        vendor_data['product_list'] = vendor.product_list
        vendor_data['image'] = vendor.image
        vendor_data['created_at'] = vendor.created_at
        vendor_data['updated_at'] = vendor.updated_at
        output.append(vendor_data)
    return jsonify({'vendors': output})

@app.route('/vendors/<vendor_id>', methods=['GET'])
def get_one_vendor(vendor_id):
    vendor = Vendor.query.filter_by(id=vendor_id).first()
    if not vendor:
        return jsonify({'message': 'No vendor found!'})
    vendor_data = {}
    vendor_data['id'] = vendor.id
    vendor_data['user_id'] = vendor.user_id
    vendor_data['fullnames'] = vendor.fullnames
    vendor_data['business_name'] = vendor.business_name
    vendor_data['mobile_number'] = vendor.mobile_number
    vendor_data['email_address'] = vendor.email_address
    vendor_data['physical_address'] = vendor.physical_address
    vendor_data['county'] = vendor.county
    vendor_data['longitude'] = vendor.longitude
    vendor_data['latitude'] = vendor.latitude
    vendor_data['product_list'] = vendor.product_list
    vendor_data['image'] = vendor.image
    vendor_data['created_at'] = vendor.created_at
    vendor_data['updated_at'] = vendor.updated_at
    return jsonify({'vendor': vendor_data})

@app.route('/vendors', methods=['POST'])
def create_vendor():
    data = request.get_json()
    new_vendor = Vendor(user_id=data['user_id'], fullnames=data['fullnames'], business_name=data['business_name'], mobile_number=data['mobile_number'], email_address=data['email_address'], physical_address=data['physical_address'], county=data['county'], longitude=data['longitude'], latitude=data['latitude'], product_list=data['product_list'], image=data['image'])
    db.session.add(new_vendor)
    db.session.commit()
    return jsonify({'message': 'New vendor created!'})

@app.route('/vendors/<vendor_id>', methods=['PUT'])
def update_vendor(vendor_id):
    vendor = Vendor.query.filter_by(id=vendor_id).first()
    if not vendor:
        return jsonify({'message': 'No vendor found!'})
    data = request.get_json()
    vendor.user_id = data['user_id']
    vendor.fullnames = data['fullnames']
    vendor.business_name = data['business_name']
    vendor.mobile_number = data['mobile_number']
    vendor.email_address = data['email_address']
    vendor.physical_address = data['physical_address']
    vendor.county = data['county']
    db.session.commit()
    return jsonify({'message': 'Vendor updated successfully!'})

@app.route('/vendors/<int:id>', methods=['DELETE'])
def delete_vendor(id):
    vendor = Vendor.query.filter_by(id=id).first()
    if not vendor:
        return jsonify({'message': 'No vendor found!'})
    db.session.delete(vendor)
    db.session.commit()
    return jsonify({'message': 'Vendor deleted successfully!'})

# ........................Product.........................

@app.route('/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        new_product = Product(**data)  # Assuming the request data matches the Product model
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Retrieve a product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.__dict__), 200
    else:
        return jsonify({'message': 'Product not found'}), 404

# Update a product by ID
@app.route('/products/<int:product_id>', methods=['PUT', 'PATCH'])
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        if product:
            data = request.get_json()
            for key, value in data.items():
                setattr(product, key, value)
            db.session.commit()
            return jsonify({'message': 'Product updated successfully'}), 200
        else:
            return jsonify({'message': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Delete a product by ID
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 204
    else:
        return jsonify({'message': 'Product not found'}), 404
    

# ..................cart....................... 
    

@app.route('/carts', methods=['POST'])
def create_cart():
    try:
        data = request.get_json()
        new_cart = Cart(**data)  # Assuming the request data matches the Cart model
        db.session.add(new_cart)
        db.session.commit()
        return jsonify({'message': 'Cart created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Retrieve a cart by ID
@app.route('/carts/<int:cart_id>', methods=['GET'])
def get_cart(cart_id):
    cart = Cart.query.get(cart_id)
    if cart:
        return jsonify(cart.__dict__), 200
    else:
        return jsonify({'message': 'Cart not found'}), 404

# Update a cart by ID
@app.route('/carts/<int:cart_id>', methods=['PUT', 'PATCH'])
def update_cart(cart_id):
    try:
        cart = Cart.query.get(cart_id)
        if cart:
            data = request.get_json()
            for key, value in data.items():
                setattr(cart, key, value)
            db.session.commit()
            return jsonify({'message': 'Cart updated successfully'}), 200
        else:
            return jsonify({'message': 'Cart not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Delete a cart by ID
@app.route('/carts/<int:cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    cart = Cart.query.get(cart_id)
    if cart:
        db.session.delete(cart)
        db.session.commit()
        return jsonify({'message': 'Cart deleted successfully'}), 204
    else:
        return jsonify({'message': 'Cart not found'}), 404    
    


# from flask import Flask, request, render_template, jsonify
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
# db = SQLAlchemy(app)

# class Category(db.Model):
#     __tablename__ = 'categories'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)

#     def __repr__(self):
#         return f'Category(id={self.id}, name={self.name})'

# Other model definitions and setup go here...
    
    
# .........................Category.........................
@app.route('/categories', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/categories/<int:category_id>', methods=['GET'])
def view_category(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template('category_details.html', category=category)

# Example route for creating a new category
@app.route('/categories/new', methods=['POST'])
def create_category():
    name = request.form.get('name')  # Get category name from form data
    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category created successfully'})

# Example route for updating an existing category
@app.route('/categories/<int:category_id>/edit', methods=['POST'])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    new_name = request.form.get('new_name')  # Get the new category name from form data
    category.name = new_name  # Update the category name
    db.session.commit()  # Save changes to the database
    return jsonify({'message': f'Category {category_id} updated successfully'})

@app.route('/categories/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)  # Delete the category from the database
    db.session.commit()  # Save changes
    return jsonify({'message': f'Category {category_id} deleted successfully'})


# .................................CartItem......................
# Example route for creating a new cart item
@app.route('/cart_items', methods=['POST'])
def create_cart_item():
    data = request.get_json()
    cart_id = data.get('cart_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # Validate input data (e.g., check if cart and product exist)
    # Create a new CartItem instance
    new_cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
    db.session.add(new_cart_item)
    db.session.commit()

    return jsonify({'message': 'Cart item created successfully'})

# Example route for updating an existing cart item
@app.route('/cart_items/<int:cart_item_id>', methods=['PUT'])
def update_cart_item(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    data = request.get_json()
    quantity = data.get('quantity')

    # Update the quantity
    cart_item.quantity = quantity
    db.session.commit()

    return jsonify({'message': f'Cart item {cart_item_id} updated successfully'})

# Example route for deleting a cart item
@app.route('/cart_items/<int:cart_item_id>', methods=['DELETE'])
def delete_cart_item(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({'message': f'Cart item {cart_item_id} deleted successfully'})



# ...................UploadedImage........................................
@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        # Get the uploaded image file from the request
        uploaded_file = request.files['image']

        # Validate the file (you can customize this validation logic)
        if uploaded_file and allowed_file(uploaded_file.filename):
            # Save the image to a specific folder (e.g., 'uploads')
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Create an instance of UploadedImage and save it to the database
            new_image = UploadedImage(filename=filename, url=f"/uploads/{filename}")
            db.session.add(new_image)
            db.session.commit()

            return jsonify({"message": "Image uploaded successfully", "url": new_image.url})
        else:
            return jsonify({"error": "Invalid file format or no file provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Helper function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

# Example configuration for file uploads
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Set maximum file size (16 MB in this example)




if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == '__main__':
#     app.run(debug=True)