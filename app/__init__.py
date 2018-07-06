from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from config import config
from .models import db, TradeTable, TestTable, MDTable, XeleConfig
from .main.admin import CustomModelView, CustomView, flask_admin

bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    #flask admin 函数注册
    flask_admin.init_app(app)
    flask_admin.add_view(CustomView(name='Custom'))
    model_list = [TradeTable, MDTable, TestTable, XeleConfig]
    for model in model_list:
        flask_admin.add_view(CustomModelView(model, db.session))

    #注册蓝本到工厂函数
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app