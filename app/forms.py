from wtforms import Form, StringField, PasswordField, validators


class LoginForm(Form):
    email = StringField('', [validators.Length(max=50)])
    password = PasswordField('Password', [
        validators.Length(min=6),
        validators.DataRequired()
      ])


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    email = StringField('Email Address', [
        validators.Length(min=6, max=64),
        validators.Email()
        ])
    password = PasswordField('Password', [
        validators.Length(min=6),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
      ])
    confirm = PasswordField('Repeat Password')
