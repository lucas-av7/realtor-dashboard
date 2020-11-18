from wtforms import Form, StringField, TextAreaField, PasswordField, validators

class RegisterForm(Form):
    name = StringField(u'Nome', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    email = StringField(u'Email', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    password = PasswordField(u'Senha', validators=[
        validators.Length(min=5, max=30, message='Mínimo 5 letras e máximo 30 letras'),
        validators.EqualTo('confirm', message='Senhas não conferem.')
    ])
    confirm = PasswordField('Confirme a senha')
    

class EditUserForm(Form): 
    name = StringField(u'Nome', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    email = StringField(u'Email', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])


class CategoryForm(Form):
    title = StringField(u'Título', validators=[validators.Length(min=5, max=30, message='Mínimo 5 letras e máximo 30 letras')])
    