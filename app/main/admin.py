from flask_admin import BaseView, expose, Admin
from flask_admin.contrib.sqla import ModelView
# # from app import db, flask_admin
# from app.models import TestTable, TradeTable, MDTable, XeleConfig

flask_admin = Admin(name='xele-ops', template_mode='bootstrap3')

class CustomView(BaseView):
    """View function of Flask-Admin for Custom page."""

    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class CustomModelView(ModelView):
    pass


# def create_admin():
#     flask_admin.add_view(CustomView(name='Custom'))
#     modellist = [TradeTable, MDTable, TestTable, XeleConfig]
#     for model in modellist:
#         flask_admin.add_view(CustomModelView(model, db.session, category='Models'))
#
#
# create_admin()



