from app import db, admin
from app.models import Category, Product, User
from flask_admin.contrib.sqla import ModelView


class ProductView(ModelView):
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_exclude_list = ['image']
    column_sortable_list = ['name', 'price']


class UserView(ModelView):
    can_view_details = True
    can_export = True
    column_exclude_list = ['password', 'email', 'avatar', 'joined_date']
    column_sortable_list = ['name', 'username', 'joined_date']


admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(UserView(User, db.session))
