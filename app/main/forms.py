from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required


class TradeMD(FlaskForm):
    hostname = StringField('hostname', validators=[Required()])
    ip = StringField('ip', validators=[Required()])
    port = StringField('port', default='22', validators=[Required()])
    user = StringField('user', default='root', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    submit = SubmitField('submit')


class TestAdd(FlaskForm):
    hostname = StringField('hostname', validators=[Required()])
    ip = StringField('ip', validators=[Required()])
    port = StringField('port', default='22', validators=[Required()])
    user = StringField('user', default='root', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    abbreviation = StringField('abbreviation', validators=[Required()])
    submit = SubmitField('submit')


class FileTime(FlaskForm):
    ten = BooleanField("10:00")
    fourteen = BooleanField("14:40")
    twenty = BooleanField("22:00")
    submit = SubmitField('submit')

    def getRst(self, data):
        result = []
        if data.get('ten'):
            result.append('10')
        if data.get('fourteen'):
            result.append('14')
        if data.get('twenty'):
            result.append('22')
        return result


class Command(FlaskForm):
    command = StringField('command', validators=[Required()])
    submit = SubmitField('run')