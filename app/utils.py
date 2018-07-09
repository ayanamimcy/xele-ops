import time
import threading
import re

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
            return e


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
            return e

    def run_command(self, host, command):
        self.fabric_xele(host)
        result = self.ssh_connec.run(command, hide=True).stdout
        return result

    def get_file(self, host, source, destination):
        self.fabric_xele(host)
        try:
            self.ssh_connec.get(source, destination)
            return '%s [%s] get success' % (host['hostname'], source)
        except Exception as e:
            return e

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

# class Trade(Xele):
#
#     def __init__(self):
#         Xele.__init__(self)
#
#     def run_exec(self, host):
#         s1 = '========================================================\n'
#         s2 = '                  %s                      \n' % (host[1])
#         s3 = '========================================================\n'
#         head = s1 + s2 + s3
#         command = '/home/xele/xele_trade/bin/debug.py --checktd'
#         text = self.run_command(host, command)
#         result = head + text
#         return result
#
#
# class MD(Xele):
#
#     def __init__(self):
#         Xele.__init__(self)
#
#     def run_exec(self, host):
#         s1 = '========================================================\n'
#         s2 = '                  %s                      \n' % (host[1])
#         s3 = '========================================================\n'
#         head = s1 + s2 + s3
#         command = "/home/xele/xele_md/bin/debug.py --checkmd | grep -v 'ERROR: find 1 pci devices'"
#         text = self.run_command(host, command)
#         result = head + text
#         return result


# 添加jinja2过滤器
def result_re(arg):
    return re.findall('ERROR', arg)

class Test(Xele):

    def __init__(self):
        Xele.__init__(self)

    def run_exec(self, host):
        s1 = time.strftime('%Y-%m-%d_%H', time.localtime())
        command = "ls -l /home/tradetest/autotrade/xelelog.* | tail -n 1  | awk '{print $NF}'"
        source = self.run_command(host, command).strip()
        des_path = self.config.get('path_to_save_trade')
        des = des_path + '\\xelelog.%s_%s' % (s1, host[6])
        self.get_file(host, source, des)


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
