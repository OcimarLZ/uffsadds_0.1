from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '29cecf8afd6176f06bb3f55472d490d1'
# Conecta ao SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UFFSAdds.db'
# Conecta ao PostgreSQL
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://ocimar.zolin:Segredooo@srv-pgsql-hom-02.uffs.edu.br:5432/administrativo_hom'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'
