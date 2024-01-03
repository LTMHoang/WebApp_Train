import hashlib
from flask_login import current_user
from app.models import *
from app import app
import cloudinary.uploader
from sqlalchemy import func


def load_categories():
    return Category.query.all()
    # return [{
    #     'id': 1,
    #     'name': 'Canon'
    # }, {
    #     'id': 2,
    #     'name': 'Nikon'
    # }, {
    #     'id': 3,
    #     'name': 'Sony'
    # }]


def load_products(kw=None, cate_id=None, page=None):
    pros = Product.query

    if kw:
        pros = pros.filter(Product.name.contains(kw))

    if cate_id:
        pros = pros.filter(Product.category_id.__eq__(cate_id))

    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1)*page_size

        return pros.slice(start, start + page_size)

    return pros.all()
    # pros = [{
    #     'id': 1,
    #     'name': 'Canon 750D',
    #     'price': 7500000,
    #     'image': 'https://product.hstatic.net/200000354621/product/may-anh-dslr-canon-eos-750d-ef-s18-55-is-stm_40450531012c4f6f89c50efc4fb684de_grande.jpg'
    # }, {
    #     'id': 2,
    #     'name': 'Canon 750D',
    #     'price': 7500000,
    #     'image': 'https://product.hstatic.net/200000354621/product/may-anh-dslr-canon-eos-750d-ef-s18-55-is-stm_40450531012c4f6f89c50efc4fb684de_grande.jpg'
    # }, {
    #     'id': 3,
    #     'name': 'Canon 750D',
    #     'price': 7500000,
    #     'image': 'https://product.hstatic.net/200000354621/product/may-anh-dslr-canon-eos-750d-ef-s18-55-is-stm_40450531012c4f6f89c50efc4fb684de_grande.jpg'
    # }, {
    #     'id': 4,
    #     'name': 'Sony A6000',
    #     'price': 10000000,
    #     'image': 'https://binhminhdigital.com/storedata/images/product/sony-a6000-kit-1650-xam.jpg'
    # }, {
    #     'id': 5,
    #     'name': 'Sony A6000',
    #     'price': 10000000,
    #     'image': 'https://binhminhdigital.com/storedata/images/product/sony-a6000-kit-1650-xam.jpg'
    # }, {
    #     'id': 6,
    #     'name': 'Sony A6000',
    #     'price': 10000000,
    #     'image': 'https://binhminhdigital.com/storedata/images/product/sony-a6000-kit-1650-xam.jpg'
    # }]
    #
    # if kw:
    #     pros = [p for p in pros if p['name'].find(kw) >= 0]
    #
    # return pros


def count_product():
    return Product.query.count()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()


def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'], product_id=c['id'], receipt=receipt)
            db.session.add(d)

        db.session.commit()


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(name=name, username=username, password=password,
             avatar='https://genshin-guide.com/wp-content/uploads/yae-miko.png')

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res['secure_url']

    db.session.add(u)
    db.session.commit()


def count_products():
    #isouter là xuất những dữ liệu trống (Số lượng = 0)
    return db.session.query(Category.id, Category.name, func.count(Product.id)).join(Product, Product.category_id == Category.id, isouter=True).group_by(Category.id).all()


if __name__ == '__main__':
    with app.app_context():
        print(count_products())