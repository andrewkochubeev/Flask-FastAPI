import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User


class RegistrationForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(8)])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Пользователь с таким email уже существует')
    def validate_password(self, field):
        pattern = r'^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z\d@$!%*#?&]{8,}$'
        if re.match(pattern, field.data) is None:
            raise ValidationError('Поле должно содержать не менее 8 символов, включая хотя бы одну букву и одну цифру')
