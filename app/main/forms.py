from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required


class TradeMD(FlaskForm):
    hostname = StringField('hostname', validators=[Required()])
    ip = StringField('ip', validators=[Required()])
    port = StringField('port', default='22', validators=[Required()])
    user = StringField('user', default='root', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    submit = SubmitField('submit')


class Command(FlaskForm):
    command = StringField('command', validators=[Required()])
    submit = SubmitField('run')