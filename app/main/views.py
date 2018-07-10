import re
from flask import render_template, redirect, url_for, flash

from . import main
from .forms import TradeMD, Command, TestAdd, FileTime, SetConfig
from ..models import TestTable, TradeTable, MDTable, XeleConfig
from ..utils import Xele, Test


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/<name>/hosts', methods=['GET', 'POST'])
def trade_hosts(name):
    tablelist = {'trade': TradeTable, 'md': MDTable, 'test': TestTable}
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
    tablelist = {'trade': TradeTable, 'md': MDTable, 'test': TestTable}
    table = tablelist[name]()
    if name == 'test':
        form = TestAdd()
    else:
        form = TradeMD()
    if form.validate_on_submit():
        table.insert(form.data)
        return redirect(url_for('.trade_hosts', name=name))
    return render_template('hosts_add.html', form=form, result=[])


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
        if re.findall('^rm', command):
            flash('%s is dangerous' % command)
        else:
            res = table_check.run_exec(name, command)
    return render_template('exec.html', form=form, result=res)


@main.route('/test/get', methods=['GET', 'POST'])
def get_file():
    xele_class = Test()
    form = FileTime()
    res = []
    if form.validate_on_submit():
        result = form.getRst(form.data)
        xele_class.test_file(result)
        res = xele_class.getRst()
    return render_template('hosts_add.html', form=form, result=res)


@main.route('/config', methods=['GET', 'POST'])
def config_set():
    table = XeleConfig()
    form = SetConfig()
    column = table.getcolumn()
    datas = []
    if form.validate_on_submit():
        table.insert(form.data)
        return redirect(url_for('.config_set'))
    try:
        show = table.query.all()
        for list in show:
            datas.append(list.getdict())
    except:
        datas = {'1': '1'}
    return render_template('config.html', form=form, column=column, datas=datas)
