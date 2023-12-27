import math
from flask import render_template, request, redirect, jsonify, session
from flask_login import login_user, logout_user
import dao
import utils
from app import app, login
from app.models import *
import hashlib


@app.route('/')
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')

    pros = dao.load_products(kw, cate_id, page)
    num = dao.count_product()

    return render_template('index.html', products=pros,
                           pages=math.ceil(num/app.config["PAGE_SIZE"]))


@app.route('/admin/login', methods=['post'])
def admin_login():
    request.form.get('username')
    request.form.get('password')


#Khi add vào thì methods là post
@app.route('/api/cart', methods=['post'])
def add_to_cart():
    """
    {
        "cart": {
            "1": {
                "id": "1",
                "name": "ABC",
                "price": 12,
                "quantity": 1
            }
        }
    }
    :return:
    """

    data = request.json

    cart = session.get('cart')
    if cart is None:
        cart = {}

    id = str(data.get("id"))
    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": data.get('name'),
            "price": data.get('price'),
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


#Khi cập nhật thì methods là put
@app.route('/api/cart/<product_id>', methods=['put'])
def update_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        quantity = request.json.get('quantity')
        cart[product_id]['quantity'] = int(quantity)

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


#Khi xóa thì methods là delete
@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/login', methods=['get', 'post'])
def process_user_login():
    if request.method.__eq__('POST'):
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(), User.password == password).first()
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect('/' if next is None else next)

    return render_template('login.html')


@app.route('/logout')
def process_user_logout():
    logout_user()
    return redirect('/login')


@app.route('/register', methods=['get', 'post'])
def process_user_register():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(name=request.form.get('name'),
                             username=request.form.get('username'),
                             password=password,
                             avatar=request.files.get('avatar'))
            except Exception as ex:
                print(str(ex))
                err_msg = "HỆ THỐNG ĐANG BỊ LỖI!!!"
            else:
                return redirect('/login')
        else:
            err_msg = "Mật khẩu KHÔNG khớp!!!"

    return render_template('/register.html', err_msg=err_msg)


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login-admin", methods=['get', 'post'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(), User.password == password).first()
        if user:
            login_user(user=user)

    return redirect("/admin")


@app.context_processor
def common_response():
    return {
        'categories': dao.load_categories(),
        'cart': utils.count_cart(session.get('cart'))
    }


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)