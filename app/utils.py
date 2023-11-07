from app.models import Category, Product, User
from app import app, db
import hashlib


def load_categories():
    return Category.query.all()


def load_products(kw=None, cate_id=None, page=1):
    products = Product.query

    if cate_id:
        products = Product.query.filter(Product.category_id.__eq__(cate_id))
    if kw:
        products = Product.query.filter(Product.name.contains(kw))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return products.slice(start, end).all()


def load_product_by_id(product_id):
    return Product.query.get(product_id)


def count_products():
    return Product.query.count()


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def count_cart(cart):
    total_quantity, total_price = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_price += c['quantity'] * c['product_price']

    return {
        'total_quantity': total_quantity,
        'total_price': total_price
    }
