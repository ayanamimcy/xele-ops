import os
from app import create_app, db
from app.models import TradeTable, MDTable, TestTable, XeleConfig
from app.utils import result_re
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


# 注册jinja2过滤器
env = app.jinja_env
env.filters['res_re'] = result_re


def make_shell_context():
    return dict(app=app, db=db, TradeTable=TradeTable, MDTable=MDTable, TestTable=TestTable, XeleConfig=XeleConfig)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
