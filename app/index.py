from flask import render_template, request, redirect, url_for, session, jsonify

import math
import utils
import cloudinary.uploader
from app import app, login
from flask_login import login_user, logout_user


@app.route('/')
def index():
    products = utils.load_products()

    return render_template('index.html', products=products)


@app.route('/products')
def products_list():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    page = request.args.get('page', 1)

    products = utils.load_products(kw=kw, cate_id=cate_id, page=int(page))
    counter = utils.count_products()

    return render_template('products.html', products=products, pages=math.ceil(counter / app.config['PAGE_SIZE']))


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = utils.load_product_by_id(product_id)

    return render_template('product_detail.html', product=product)


@app.route('/user-register', methods=['get', 'post'])
def user_register():
    err_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name,
                               username=username,
                               password=password,
                               email=email,
                               avatar=avatar_path)
                return redirect(url_for('user_signin'))
            else:
                err_msg = 'Mật khẩu không khớp!!!'
        except Exception as ex:
            err_msg = 'Hệ thống đang có lỗi: ' + str(ex)

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('index'))
        else:
            err_msg = 'Tên người dùng hoặc mật khẩu không chính xác!!!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id)


@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    product_id = ''
    product_name = ''
    product_price = ''

    cart = session.get('cart')
    if cart:
        cart = {}

    if product_id in cart:
        cart[product_id]['quantity'] = cart[product_id]['quantity'] + 1
    else:
        cart[product_id] = {
            'id': product_id,
            'name': product_name,
            'price': product_price,
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart=cart))


@app.context_processor
def common_response():
    return {
        'categories': utils.load_categories()
    }


if __name__ == '__main__':
    from app.admin import *

    app.run(debug=True)
