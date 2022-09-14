from apps import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    papeis = database.Column(database.String, nullable=False, default='Não Informado')
    id_usuario_sigadmin = database.Column(database.Integer)
#   nome = database.Column(database.String, nullable=False)
#   id_cargo = database.Column(database.Integer, database.ForeignKey('cargo.id'), nullable=False)
#   id_funcao = database.Column(database.Integer, database.ForeignKey('funcao.id'))

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)


class Cargo(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_cargo = database.Column(database.String, nullable=False)


class Funcao(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_funcao = database.Column(database.String, nullable=False)


class Papel(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_papel = database.Column(database.String, nullable=False)


class PapeisdoUsuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_papel = database.Column(database.Integer, database.ForeignKey('papel.id'), nullable=False)
    dta_liberacao = database.Column(database.DateTime, nullable=False)
    dta_bloqueio = database.Column(database.DateTime)


class Log(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    dta_inicio = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    dta_fim = database.Column(database.DateTime, nullable=True)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    datalhes = database.Column(database.Text)


class Unidade(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_unidade = database.Column(database.String, nullable=False)
    ug_ugr = database.Column(database.Integer)
    codigo_unidade = database.Column(database.String, nullable=False)


class Modulo(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)


class Funcionalidade(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    rota = database.Column(database.String, nullable=False)
    id_moddulo = database.Column(database.Integer, database.ForeignKey('modulo.id'), nullable=False)


class MsgsApp(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_rota = database.Column(database.Integer, database.ForeignKey('funcionalidade.id'), nullable=False)
    app_funcao = database.Column(database.String, nullable=False)
    descricao = database.Column(database.String, nullable=False)
    datalhes = database.Column(database.Text)
    id_log = database.Column(database.Integer, database.ForeignKey('log.id'), nullable=False)


class Sol_empenho_status(database.Model):
    id = database.Column(database.Integer, nullable=False, primary_key=True)
    status_descricao = database.Column(database.String, nullable=False)
    etapa = database.Column(database.String, nullable=False)


class Sol_empenho(database.Model):
    id = database.Column(database.Integer, nullable=False, primary_key=True)
    id_status = database.Column(database.Integer, database.ForeignKey('sol_empenho_status.id'), nullable=False)
    id_usuario_criacao = database.Column(database.Integer, nullable=False)
    dta_criacao = database.Column(database.DateTime, nullable = False, default = datetime.utcnow)
    tipo = database.Column(database.String, nullable=False)
    origem = database.Column(database.String, nullable=False)
    ano = database.Column(database.Integer, nullable=False)
    numero = database.Column(database.Integer, nullable=False)
    processo = database.Column(database.String)
    radical_processo = database.Column(database.Integer)
    nro_processo = database.Column(database.Integer)
    ano_processo = database.Column(database.Integer)
    dv_processo = database.Column(database.Integer)
    ug = database.Column(database.Integer)
    modal_licitacao = database.Column(database.Integer)
    licitacao = database.Column(database.String)
    nro_licitacao = database.Column(database.Integer)
    nro_contrato = database.Column(database.Integer)
    ano_licitacao_contrato = database.Column(database.Integer)
    chave = database.Column(database.String)
    credor_cnpj = database.Column(database.String)
    credor_nome = database.Column(database.String)
    nro_dotacao = database.Column(database.Integer)
    ugr = database.Column(database.Integer)
    ccusto = database.Column(database.String)
    esfera_celula = database.Column(database.Integer)
    ptres_celula = database.Column(database.Integer)
    fonte_recurso_celula = database.Column(database.Integer)
    natureza_celula = database.Column(database.Integer)
    pi_celula = database.Column(database.String)
    modal_empenho = database.Column(database.Integer)
    processo_licitacao = database.Column(database.Integer)
    amparo_legal = database.Column(database.Integer)
    observacao = database.Column(database.Text)
    dta_empenho = database.Column(database.Date)
    nro_empenho = database.Column(database.Integer)
    dta_ult_atualizacao = database.Column(database.DateTime, nullable = False)
    valor_estimado = database.Column(database.Float)
