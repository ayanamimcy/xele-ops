from flask_sqlalchemy import SQLAlchemy
from .aes_encrypt import Prpcrypt

db = SQLAlchemy()
prpcrypt = Prpcrypt()


class TradeTable(db.Model):
    __tablename__ = 'trade_table'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(200))
    ip = db.Column(db.String(16))
    port = db.Column(db.String(10))
    user = db.Column(db.String(20))
    password = db.Column(db.String(100))

    def __repr__(self):
        return '<Trade %r>' % self.hostname

    def getdict(self):
        return dict(id=self.id, hostname=self.hostname, ip=self.ip, port=self.port, user=self.user, password=self.password)

    def getcolumn(self):
        return ['id', 'hostname', 'ip', 'port', 'user', 'password']

    def insert(self, data):
        password = prpcrypt.encrypt(data.get('password'))
        table = TradeTable(hostname=data.get('hostname'), ip=data.get('ip'), port=data.get('port'), user=data.get('user'), password=password)
        db.session.add(table)
        db.session.commit()


class MDTable(db.Model):
    __tablename__ = 'md_table'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(200))
    ip = db.Column(db.String(16))
    port = db.Column(db.String(10))
    user = db.Column(db.String(20))
    password = db.Column(db.String(100))

    def __repr__(self):
        return '<MD %r>' % self.hostname

    def getdict(self):
        return dict(id=self.id, hostname=self.hostname, ip=self.ip, port=self.port, user=self.user, password=self.password)

    def getcolumn(self):
        return ['id', 'hostname', 'ip', 'port', 'user', 'password']

    def insert(self, data):
        password = prpcrypt.encrypt(data.get('password'))
        table = MDTable(hostname=data.get('hostname'), ip=data.get('ip'), port=data.get('port'), user=data.get('user'), password=password)
        db.session.add(table)
        db.session.commit()


class TestTable(db.Model):
    __tablename__ = 'test_table'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(200))
    ip = db.Column(db.String(16))
    port = db.Column(db.String(10))
    user = db.Column(db.String(20))
    password = db.Column(db.String(100))
    abbreviation = db.Column(db.String(20))

    def __repr__(self):
        return '<Test %r>' % self.hostname

    def getdict(self):
        return dict(id=self.id, hostname=self.hostname, ip=self.ip, port=self.port, user=self.user, password=self.password, abbreviation=self.abbreviation)

    def getcolumn(self):
        return ['id', 'hostname', 'ip', 'port', 'user', 'password', 'abbreviation']

    def insert(self, data):
        password = prpcrypt.encrypt(data.get('password'))
        table = TestTable(hostname=data.get('hostname'), ip=data.get('ip'), port=data.get('port'), user=data.get('user'), password=password, abbreviation=data.get('abbreviation'))
        db.session.add(table)
        db.session.commit()


class XeleConfig(db.Model):
    __tablename__ = 'config_table'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(200))
    value = db.Column(db.String(200))
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<Config %r>' % self.key

    def getdict(self):
        return dict(id=self.id, key=self.key, value=self.value, description=self.description)
