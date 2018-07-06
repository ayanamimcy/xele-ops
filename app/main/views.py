from flask import render_template, redirect, url_for

from . import main
from .forms import TradeMD
from .. import db
from ..models import TestTable, TradeTable, MDTable, XeleConfig
from ..utils import Xele


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/<name>/hosts', methods=['GET', 'POST'])
def trade_hosts(name):
    tablelist = {'trade': TradeTable, 'md': MDTable}
    datas = []
    table = tablelist[name]()
    print(table)
    column = table.getcolumn()
    try:
        show = table.query.all()
        for list in show:
            datas.append(list.getdict())
    except Exception:
        datas = {'1': '1'}
    return render_template('hosts.html', column=column, datas=datas, name=name)


@main.route('/<name>/hosts/add', methods=['GET', 'POST'])
def hosts_add(name):
    tablelist = {'trade': TradeTable, 'md': MDTable}
    table = tablelist[name]()
    print(table)
    form = TradeMD()
    if form.validate_on_submit():
        table.insert(form.data)
        return redirect(url_for('.trade_hosts', name=name))
    return render_template('hosts_add.html', form=form)


@main.route('/<name>/check', methods=['GET', 'POST'])
def check(name):
    table_check = Xele()
    res = table_check.check_all(name)
    return render_template('check.html', result=res)