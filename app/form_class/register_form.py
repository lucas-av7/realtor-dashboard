from wtforms import Form, StringField, TextAreaField, PasswordField, validators

# Form Register
class RegisterForm(Form):
    name = StringField(u'Nome', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    email = StringField(u'Email', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    password = PasswordField(u'Senha', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Senhas não conferem.')
    ])
    confirm = PasswordField('Confirme a senha')