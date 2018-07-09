from flask import render_template, redirect, url_for

from . import main
from .forms import TradeMD, Command
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
    form = TradeMD()
    if form.validate_on_submit():
        table.insert(form.data)
        return redirect(url_for('.trade_hosts', name=name))
    return render_template('hosts_add.html', form=form)


@main.route('/<name>/check', methods=['GET', 'POST'])
def check(name):
    table_check = Xele()
    if name == 'trade':
        command = '/home/xele/xele_trade/bin/debug.py --checktd'
    elif name == 'md':
        command = "/home/xele/xele_md/bin/debug.py --checkmd | grep -v 'ERROR: find 1 pci devices'"
    res = table_check.run_exec(name, command)
    return render_template('check.html', result=res)


@main.route('/<name>/exec', methods=['GET', 'POST'])
def run_exec(name):
    table_check = Xele()
    res = ''
    form = Command()
    if form.validate_on_submit():
        command = form.command.data
        res = table_check.run_exec(name, command)
        # return redirect(url_for('.run_exec', name=name))
    return render_template('exec.html', form=form, result=res)