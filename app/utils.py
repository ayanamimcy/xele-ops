import time
import threading
import re
import os

from fabric import Connection
from .aes_encrypt import Prpcrypt
from .models import TradeTable, TestTable, MDTable, XeleConfig


class Mythread(threading.Thread):

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name
        self.res = self.func(*self.args)

    def get_result(self):
        try:
            return self.res
        except Exception as e:
            return str(e)


class Xele(object):

    def __init__(self):
        self.ssh_connec = None
        self.prpcrypt = Prpcrypt()

    def fabric_xele(self, host):
        port = host['port']
        user = host['user']
        password = self.prpcrypt.decrypt(host['password'])
        host = host['ip']
        try:
            self.ssh_connec = Connection(host=host, port=port, user=user, connect_kwargs={'password': password})
            return self.ssh_connec
        except Exception as e:
            return str(e)

    def run_command(self, host, command):
        try:
            self.fabric_xele(host)
            result = self.ssh_connec.run(command, hide=True).stdout
            return result
        except Exception as e:
            return str(e)

    def get_file(self, host, source, destination):
        try:
            self.fabric_xele(host)
            self.ssh_connec.get(source, destination)
            return '%s [%s] get success' % (host['hostname'], source)
        except Exception:
            return '[ERROR] %s [%s] get failed' % (host['hostname'], source)

    def put_file(self, host, source, destination):
        try:
            self.fabric_xele(host)
            self.ssh_connec.put(source, destination)
            return '%s [%s] put success' % (host['hostname'], source)
        except Exception as e:
            # return e
            return '[ERROR] %s [%s] put failed' % (host['hostname'], source)

    def run_exec(self, table, command):
        s = time.clock()
        head = '================={}================='
        heads = []
        thread = []
        results = []
        if table == 'trade':
            init_table = TradeTable()
        elif table == 'md':
            init_table = MDTable()
        hosts = init_table.query.all()
        for host in hosts:
            tmp = host.getdict()
            t = Mythread(self.run_command, (tmp, command), self.run_command.__name__)
            heads.append(head.format(tmp.get('hostname')))
            thread.append(t)
        for i in thread:
            i.start()
        for i in thread:
            i.join()
        for i in range(len(thread)):
            results.append(heads[i])
            res = thread[i].get_result().split('\n')
            for j in res:
                rep = j.replace(' ', '&nbsp;')
                results.append(rep)
        print(time.clock() - s)
        return results


# 添加jinja2过滤器
def result_re(arg):
    return re.findall('ERROR', arg)


# create path
def path_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


class Test(Xele):

    def __init__(self):
        Xele.__init__(self)
        self.des_root_path = self.get_config('path_to_save_csv')
        self.file_path = []
        self.test_date = []
        self.file_name = []
        self.des_host = {
            'hostname': 'test machine',
            'ip': self.get_config('remote_ip'),
            'port': self.get_config('remote_port'),
            'user': self.get_config('remote_user'),
            'password': self.get_config('remote_password')
        }
        self.des_path = self.get_config('remote_path_to_csv')
        self.result = []

    def get_config(self, key):
        table = XeleConfig()
        search = table.query.filter_by(key=key).first()
        return search.getdict().get('value')

    def get_test_file(self, test_time, host):
        date = time.strftime('%Y-%m-%d', time.localtime())
        tmp = host.getdict()
        if test_time:
            for i in test_time:
                date_file = "%s_%s" % (date, i)
                command = "find /home/tradetest -name xelelog.%s*" % date_file
                source = self.run_command(tmp, command).strip()
                des_path = self.des_root_path + '\\%s' % date_file
                path_exist(des_path)
                des = des_path + '\\xelelog.%s_%s' % (date_file, tmp['abbreviation'])
                self.file_path.append(des)
                self.test_date.append(date_file)
                self.file_name.append('xelelog.%s_%s' % (date_file, tmp['abbreviation']))
                res = self.get_file(tmp, source, des)
                self.result.append(res)

    def put_test_file(self):
        for i in range(len(self.test_date)):
            source = self.file_path[i]
            des = self.des_path + 'xelelog.%s' % self.test_date[i] + '/' + self.file_name[i]
            res = self.put_file(self.des_host, source, des)
            self.result.append(res)

    def test_file(self, test_date):
        s = time.clock()
        hosts = TestTable().query.all()
        thread = []
        for host in hosts:
            t = Mythread(self.get_test_file, (test_date, host), self.get_test_file.__name__)
            thread.append(t)
        for t in thread:
            t.start()
            t.join()
        self.put_test_file()
        self.run_command(self.des_host, '/home/tradetest/compare.sh')
        print(time.clock() - s)

    def getRst(self):
        return self.result


class Updatelicence(Xele):

    def __init__(self, host, licence_date):
        Xele.__init__(self)
        self.host = host
        self.licence_date = licence_date
        self.licence_line = self.config.get('licence_line')
        self.licence_host = self.config.get('licence_ssh_ip')
        self.licence_port = self.config.get('licence_ssh_port')
        self.licence_user = self.config.get('licence_ssh_user')
        self.licence_password = self.config.get('licence_ssh_password')
        self.licence_path = self.config.get('path_to_ssh_licence')
        self.bittID = None

    def get_bittid(self):
        self.fabric_xele(self.host)
        command = "bwconfig --list  | awk 'END {print $3}'"
        self.bittID = self.ssh_connec.run(command, hide=True).stdout.strip()
        return self.bittID

    def get_licence(self):
        self.get_bittid()
        try:
            connect = Connection(host=self.licence_host, port=self.licence_port, user=self.licence_user, connect_kwargs={'password': self.licence_password})
        except Exception as e:
            return e
        ini_file_path = self.config.get('path_to_save_licence') + 'license.ini'
        line = self.licence_line.format(self.bittID, self.licence_date)
        f = open(ini_file_path, 'w')
        f.writelines(line)
        f.close()
        connect.put(ini_file_path, self.licence_path + 'license.ini')
        connect.run("cd %s && openssl rsautl -encrypt -in license.ini -inkey test_pub.key -pubin -out license_info" % self.licence_path)
        connect.get(self.licence_path + 'license_info', self.config.get('path_to_save_licence') + 'license_info')
