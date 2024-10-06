from app import app, db
from models import Medico

with app.app_context():
    db.create_all()  # Isso irá criar o banco de dados e todas as tabelas necessárias
    print("Banco de dados criado com sucesso!")