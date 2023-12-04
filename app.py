from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # Para aceder e gerir a base de dados'''
'''Import o serviço de e-mail'''


'''#Em app encontra-se o nosso servidor web de Flask'''
app = Flask(__name__)


################################################
'''dizer a SQLAlchemy que tem de se ligar a esta base de dados no início'''
'''Construção das Bases de dados que iremos utilizar em o nosso programa'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///advinhar_numero.db'
#app.config['SQLALCHEMY_BINDS'] = {'teste': 'sqlite:///mala_de_emergencia.db'}
#'''Password e autentificação'''
app.config['SECRET_KEY'] = 'mysecretkey'
################################################
'''Cursor para a Base de Dados SQLite '''
db = SQLAlchemy(app)


#################3
"""app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tarefas.db'

'''# O debug=True faz com que cada vez que reiniciemos o nosso servidor ou modifiquemos o código, o servidor de Flask reinicia-se sozinho'''
app.config['DEBUG'] = True

'''Cursor para a Base de Dados SQLite '''
db = SQLAlchemy(app)


class Tarefa(db.Model):
    __tablename__ = "tarefas"
"""