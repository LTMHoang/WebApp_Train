from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from app import app, db
from app.models import Category, Product

# #Tự thêm 12/11
# from flask_admin import BaseView, expose
# from flask_login import logout_user
# from flask import redirect


class MyProductView(ModelView):
    column_list = ['id', 'name', 'price']
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['price', 'name']
    column_editable_list = ['name', 'price']
    details_modal = True
    edit_modal = True


class MyCategoryView(ModelView):
    column_list = ['name', 'products']


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


# # Tự thêm 12/11
# class LogoutView(BaseView):
#     @expose('/')
#     def index(self):
#         logout_user()
#         return redirect('/admin')


admin = Admin(app=app, name='QUẢN TRỊ BÁN HÀNG', template_mode='bootstrap4')
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(StatsView(name='Thống kê báo cáo'))

# #Tự thêm 12/11
# admin.add_view(LogoutView(name="Đăng xuất"))