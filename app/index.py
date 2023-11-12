from flask import render_template, request
import dao
from app import app, login

# # Tự thêm 12/11
# from flask_login import login_user
# from app.models import User
# from flask import redirect


@app.route('/')
def index():
    kw = request.args.get('kw')

    cates = dao.load_categories()

    pros = dao.load_products(kw)

    return render_template('index.html', categories=cates, products=pros)


@app.route('/admin/login', methods=['post'])
def admin_login():
    request.form.get('username')
    request.form.get('password')


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


# # Tự thêm 12/11
# @app.route("/login-admin", methods=['get', 'post'])
# def login_admin():
#     if request.method == 'POST':
#         username = request.form.get("username")
#         password = request.form.get("password")
#         user = User.query.filter(username == username, password == password).first()
#         if user:
#             login_user(user=user)
#
#     return redirect("/admin")


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)