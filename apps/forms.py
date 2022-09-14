from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, DecimalField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from apps.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(5, 40)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
    papel_admin = BooleanField('Administrador')
    papel_admin_unidade = BooleanField('Administrador Unidade')
    papel_empenho_gestor = BooleanField('Gestor de Empenhos')
    papel_empenho_view = BooleanField('Visualizador de Empenhos')
    papel_dotacao_gestor = BooleanField('Gestor de Dotações')
    papel_dotacao_view = BooleanField('Visualizador de Dotações')
    papel_compras_gestor = BooleanField('Gestor de Compras')
    papel_compras_pregoeiro = BooleanField('Pregoeiro')
    papel_chefe_ugr = BooleanField('Chefe Unidade Orçamentária')
    papel_chefe_unidade = BooleanField('Chefe Unidade')
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro e-mail')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título do post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')


class FormEditarSolEmpenho(FlaskForm):
    id = IntegerField('Seq.Sol.Empenho', validators=[DataRequired('ID da Sol.Empenho não pode ser nula')])
    status = IntegerField('Status da.Sol.Empenho', validators=[DataRequired('Status da Sol.Empenho não pode ser nula')])
    id_usuario_criacao = IntegerField('Solicitante', validators=[DataRequired('Usuário criado da Sol.Empenho não pode ser nulo')])
#    dta_criacao = DateTimeField('Data da Solicitação', validators=[DataRequired()])
    tipo = StringField('Tipo', validators=[DataRequired()])
    origem = StringField('Origem', validators=[DataRequired()])
    ano = IntegerField('Ano Sol.Empenho', validators=[DataRequired()])
    numero = IntegerField('Nro Sol.Empenho', validators=[DataRequired()])
    processo = StringField('Processo de Empenho', validators=[DataRequired()])
    ug = IntegerField('Código da UG', validators=[DataRequired()])
    modal_licitacao = IntegerField('Modal.Licitição', validators=[DataRequired()])
    licitacao = IntegerField('Licitação', validators=[DataRequired()])
    credor_cnpj = StringField('CNPJ do Credor', validators=[DataRequired()])
    credor_nome = StringField('Nome do Credor', validators=[DataRequired()])
    nro_dotacao = IntegerField('Nro da Dotação', validators=[DataRequired()])
    ugr = IntegerField('UGR de Custo', validators=[DataRequired()])
    ccusto = StringField('Código do  CCusto', validators=[DataRequired()])
    esfera_celula = IntegerField('Esfera do Orçamento', validators=[DataRequired()])
    ptres_celula = IntegerField('PTRES do Orçamento', validators=[DataRequired()])
    fonte_recurso_celula = IntegerField('Fonte de Recurso do Orçamento', validators=[DataRequired()])
    natureza_celula = IntegerField('Natureza de Despesa do Orçamento', validators=[DataRequired()])
    pi_celula = StringField('PI do Orçamento', validators=[DataRequired()])
    modal_empenho = IntegerField('Modalidade do Empenho', validators=[DataRequired()])
    processo_licitacao = StringField('Processo de Licitação', validators=[DataRequired()])
    amparo_legal = StringField('Amparo legal do Empenho', validators=[DataRequired()])
    valor_estimado = DecimalField('Valor Estimado do Empenho', validators=[DataRequired()])
    observacao = TextAreaField('Observações a registrar no SIAFI', validators=[DataRequired()])
    botao_submit_solempenho = SubmitField('Atualizar Sol.Empenho')
    botao_submit_retornarsolempenhos = SubmitField('Retornar')