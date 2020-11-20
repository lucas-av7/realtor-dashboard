from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, BooleanField, validators

class RegisterForm(Form):
    name = StringField(u'Nome', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    email = StringField(u'Email', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    phone = StringField(u'Telefone', validators=[validators.Length(
        min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    password = PasswordField(u'Senha', validators=[
        validators.Length(min=5, max=30, message='Mínimo 5 letras e máximo 30 letras'),
        validators.EqualTo('confirm', message='Senhas não conferem.')
    ])
    confirm = PasswordField('Confirme a senha')
    

class EditUserForm(Form): 
    name = StringField(u'Nome', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    email = StringField(u'Email', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    phone = StringField(u'Telefone', validators=[validators.Length(
        min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])


class CategoryForm(Form):
    title = StringField(u'Título', validators=[validators.Length(min=5, max=30, message='Mínimo 5 letras e máximo 30 letras')])
    
    
class StoreForm(Form):
    name = StringField(u'Nome da loja')
    phone = StringField(u'Telefone')
    email = StringField(u'E-mail')
    street = StringField(u'Rua')
    district = StringField(u'Bairro')
    house_number = StringField(u'Número')
    city = StringField(u'Cidade')
    state = StringField(u'Estado')
    

class ProductForm(Form):
    is_active = BooleanField(u'Ativo', false_values=(False, 'false', 0, '0'))
    title = StringField(u'Título', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    category = SelectField(u'Categoria', coerce=int)
    rooms = StringField(u'Quartos')
    bathrooms = StringField(u'Banheiros')
    parking_spaces = StringField(u'Vagas de garagem')
    area = StringField(u'Área m2')
    price = StringField(u'Preço (R$)', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    cond_fare = StringField(u'Condomínio (R$)')
    iptu_fare = StringField(u'IPTU (R$)')
    modality = SelectField(u'Modalidade', choices=[('rent', 'Aluguel'), ('sell', 'Venda')])
    street = StringField(u'Rua', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    district = StringField(u'Bairro', validators=[validators.Length(min=5, max=50, message='Mínimo 5 letras e máximo 50 letras')])
    city = StringField(u'Cidade', validators=[validators.Length(min=5, max=30, message='Mínimo 5 letras e máximo 30 letras')])
    state = StringField(u'Estado', validators=[validators.Length(min=2, max=30, message='Mínimo 5 letras e máximo 30 letras')])
    description = TextAreaField(u'Descrição')
