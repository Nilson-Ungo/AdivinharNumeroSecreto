from app import db, app
from sqlalchemy.orm import sessionmaker

metadata = db.metadata

'''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''

'''Criar uma tabela para cadastro os usuários'''
class Tentar_advinhar_numero(db.Model):
    __tablename__ = "advinhar_numero"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    jogador = db.Column(db.Integer, nullable=False)
    numero_secreto = db.Column(db.Integer, nullable=False)
    tentativa = db.Column(db.Integer, nullable=False)

    '''O Construtor da classe MalaDeEmergencia'''
    def __init__(self, jogador, numero_secreto, tentativa):
        self.jogador = jogador
        self.numero_secreto = numero_secreto
        self.tentativa = tentativa

'''Código de contexto da aplicação'''
with app.app_context():
    metadata.create_all(db.engine)
    # Criar instância de sessionmaker
    Session = sessionmaker(bind=db.engine)
