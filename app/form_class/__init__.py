from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, BooleanField, RadioField, validators

class RegisterForm(Form):
    name = StringField(u'Nome', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    email = StringField(u'Email', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    phone = StringField(u'Telefone', validators=[validators.Length(
        min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    password = PasswordField(u'Senha', validators=[
        validators.Length(min=5, max=15, message='Mínimo 5 letras e máximo 15 letras'),
        validators.EqualTo('confirm', message='Senhas não conferem.')
    ])
    confirm = PasswordField('Confirme a senha')
    role = RadioField(u'Eu sou', choices=[
                      (1, 'Cliente'), (2, 'Corretor')], coerce=int, default=1)
    

class EditUserForm(Form): 
    name = StringField(u'Nome', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    email = StringField(u'Email', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    phone = StringField(u'Telefone', validators=[validators.Length(
        min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    role = SelectField(u'Função', coerce=int)


class CategoryForm(Form):
    title = StringField(u'Título', validators=[validators.Length(min=5, max=30, message='Mínimo 5 letras e máximo 30 letras')])
    
    
class PurposeForm(Form):
    title = StringField(u'Título', validators=[validators.Length(
        min=5, max=30, message='Mínimo 5 letras e máximo 30 letras')])


class StoreForm(Form):
    name = StringField(u'Nome da loja')
    phone = StringField(u'Telefone')
    email = StringField(u'E-mail')
    street = StringField(u'Rua')
    district = StringField(u'Bairro')
    house_number = StringField(u'Número')
    city = StringField(u'Cidade')
    state = StringField(u'Estado')
    auto_active_user = BooleanField(
        u'Ativar automaticamente novos usuários', false_values=(False, 'false', 0, '0'))
    

class ProductForm(Form):
    is_active = BooleanField(u'Ativo', false_values=(False, 'false', 0, '0'))
    title = StringField(u'Título', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    category = SelectField(u'Categoria', coerce=int)
    purpose = SelectField(u'Propósito', coerce=int)
    rooms = StringField(u'Quartos')
    bathrooms = StringField(u'Banheiros')
    parking_spaces = StringField(u'Vagas de garagem')
    area = StringField(u'Área m2')
    price = StringField(u'Preço', validators=[validators.Length(
        min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    cond_fare = StringField(u'Condomínio')
    iptu_fare = StringField(u'IPTU')
    modality = SelectField(u'Modalidade', choices=[('rent', 'Aluguel'), ('sell', 'Venda')])
    street = StringField(u'Rua', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    district = StringField(u'Bairro', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    city = StringField(u'Cidade', validators=[validators.Length(min=5, max=30, message='Mínimo 5 letras e máximo 30 letras')])
    state = StringField(u'Estado', validators=[validators.Length(min=2, max=30, message='Mínimo 5 letras e máximo 30 letras')])
    description = TextAreaField(u'Descrição')


class EditPasswordForm(Form):
    actual_password = PasswordField(u'Senha Atual', validators=[validators.Length(
        min=5, max=15, message='Mínimo 5 letras e máximo 15 letras')])
    new_password = PasswordField(u'Nova Senha', validators=[
        validators.Length(
            min=5, max=15, message='Mínimo 5 letras e máximo 15 letras'),
        validators.EqualTo('confirm', message='Senhas não conferem.')
    ])
    confirm = PasswordField('Confirme a senha')


class PermissionsForm(Form):
    title = StringField(u'', validators=[validators.Length(
        min=5, max=30, message='Mínimo 5 letras e máximo 30 letras')])
    activate = BooleanField(u'', false_values=(False, 'false', 0, '0'))
    all_products = BooleanField(u'', false_values=(False, 'false', 0, '0'))
    categories = BooleanField(u'', false_values=(False, 'false', 0, '0'))
    purposes = BooleanField(u'', false_values=(False, 'false', 0, '0'))
    users = BooleanField(u'', false_values=(False, 'false', 0, '0'))
    store = BooleanField(u'', false_values=(False, 'false', 0, '0'))


class EmailForm(Form):
    email = StringField(u'E-mail')


class PasswordRecoveryForm(Form):
    code = StringField(u'Código enviado para o email')
    password = PasswordField(u'Nova senha', validators=[
        validators.Length(
            min=5, max=15, message='Mínimo 5 letras e máximo 15 letras'),
        validators.EqualTo('confirm', message='Senhas não conferem.')
    ])
    confirm = PasswordField('Confirme a senha')
