from flask import render_template, redirect, url_for, flash, request, abort
from apps import app, database, bcrypt
from apps.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormEditarSolEmpenho
from apps.models import Usuario, Post, Sol_empenho
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


# página principal da aplicação
@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


# Página de contato com a equipe da aplicação
@app.route('/contato')
def contato():
    return render_template('contato.html')


# página que relaciona os usuários do sistema
@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


# página de login no sistema
@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(
                f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login. e-mail ou senha incorretos', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data,
                          email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(
            f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


# página de logout do sistema
@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))


# página de exibição do perfil de usuário
@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for(
        'static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


# Página de edição do perfil de usuário
@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.papeis = atualizar_papeis(form)
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for(
        'static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)

# função que recebe o arquivo da foto do usuário, faz o tratamento e salva no sistema de arquivos


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(
        app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

# função de atualização dos perfis de usuário


def atualizar_papeis(form):
    lista_papeis = []
    for campo in form:
        if 'papel_' in campo.name:
            if campo.data:
                lista_papeis.append(campo.label.text)
    return ';'.join(lista_papeis)


# página de criação de post de usuário
@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data,
                    corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


# página de atualização de um post de usuário
@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)

# Exclui os posts de usuário


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluído com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)

# Mantêm as solicitações de empenho pendentes de validação pré-automação no SIAFI


@app.route('/empenhos/pendentes_avaliacao', methods=['GET'])
@login_required
def empenhos_pendentes_avaliacao():
    lista_empenhos = Sol_empenho.query.all()
    return render_template('empenhos_pendentes_avaliacao.html', lista_empenhos=lista_empenhos)


# Página de edição da solicitação de empenho
@app.route('/empenhos/editar_sol_empenho/<sol_empenho_id>', methods=['GET', 'POST'])
@login_required
def editar_sol_empenho(sol_empenho_id):
    # recupera a solicitação de empenho em edição / visualização recebido da interface anterior
    sol_empenho = Sol_empenho.query.get(sol_empenho_id)
# cria o formulário de visualização / edição
    form = FormEditarSolEmpenho()
# se o método é GET, monta o form para mostrar ao usuário
    if request.method == 'GET':
        form.id.data = sol_empenho.id
        form.status.data = sol_empenho.status
        form.id_usuario_criacao.data = sol_empenho.id_usuario_criacao
    #    form.dta_criacao.data = sol_empenho.dta_criacao.data
        form.tipo.data = sol_empenho.tipo
        form.origem.data = sol_empenho.origem
        form.ano.data = sol_empenho.ano
        form.numero.data = sol_empenho.numero
        form.processo.data = sol_empenho.processo
        form.modal_licitacao.data = sol_empenho.modal_licitacao
        form.licitacao.data = sol_empenho.licitacao
        form.credor_cnpj.data = sol_empenho.credor_cnpj
        form.credor_nome.data = sol_empenho.credor_nome
        form.nro_dotacao.data = sol_empenho.nro_dotacao
        form.ugr.data = sol_empenho.ugr
        form.ccusto.data = sol_empenho.ccusto
        form.esfera_celula.data = sol_empenho.esfera_celula
        form.ptres_celula.data = sol_empenho.ptres_celula
        form.fonte_recurso_celula.data = sol_empenho.fonte_recurso_celula
        form.natureza_celula.data = sol_empenho.natureza_celula
        form.pi_celula.data = sol_empenho.pi_celula
        form.modal_empenho.data = sol_empenho.modal_empenho
        form.processo_licitacao.data = sol_empenho.processo_licitacao
        form.amparo_legal.data = sol_empenho.amparo_legal
        form.valor_estimado.data = sol_empenho.valor_estimado
        form.observacao.data = sol_empenho.observacao
        flash('Solicitação de Empenho mostrada com sucesso', 'alert-success')
# Valida se houve alteração
    elif form.validate_on_submit():
        sol_empenho.processo = form.processo.data
        sol_empenho.modal_licitacao = form.modal_licitacao
        sol_empenho.licitacao = form.licitacao
        sol_empenho.credor_cnpj = form.credor_cnpj
        sol_empenho.nro_dotacao = form.nro_dotacao
        sol_empenho.ugr = form.ugr
        sol_empenho.ccusto = form.ccusto
        sol_empenho.esfera_celula = form.esfera_celula
        sol_empenho.ptres_celula = form.ptres_celula
        sol_empenho.fonte_recurso_celula = form.fonte_recurso_celula
        sol_empenho.natureza_celula = form.natureza_celula
        sol_empenho.pi_celula = form.pi_celula
        sol_empenho.modal_empenho = form.modal_empenho
        sol_empenho.processo_licitacao = form.processo_licitacao
        sol_empenho.amparo_legal = form.amparo_legal
        sol_empenho.observacao = form.observacao
# Atualiza a base de dados
        database.session.commit()
        flash('Solicitação de Empenho atualizada com sucesso', 'alert-success')
# retorna para a tela de lista de solicitações de empenhos pendentes e avaliação
        return redirect(url_for('pendentes_avaliacao'))
    return render_template('empenhos_editar.html')
