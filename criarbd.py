from apps import database, bcrypt
from apps.models import Usuario, Post
database.create_all()
database.session.commit()

password = 'Uffs#2Adds#'
pw_hash = bcrypt.generate_password_hash(password)
usuario = Usuario(username='admin', email='seti.depro@uffs.edu.br', senha=pw_hash)
database.session.add(usuario)
database.session.commit()

post1 = Post(titulo='Post de criação inicial do banco', corpo='Esta aplicação foi desenvolvida para automatizar alguns processos paralelo aos sistemas SIG-UFR. Conforme as funções serão disponibilizadas, novo post serão publicados para orientar os usuários', id_usuario=1)
database.session.add(post1)
database.session.commit()