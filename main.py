# -*- coding: utf-8 -*-
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
# NÃO ALTERE ESTA PARTE!
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from src.models import db

# Importar Blueprints das rotas
from src.routes.admin import admin_bp
from src.routes.public import public_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Configurações
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "uma-chave-secreta-muito-forte-trocar") # Mude em produção!
    # Configuração do Banco de Dados SQLite
    # O banco será criado na pasta /instance/portal.db
    db_path = os.path.join(app.instance_path, "portal.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Garante que a pasta /instance exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # Pasta já existe

    # Inicializa extensões
    db.init_app(app)

    # Registrar Blueprints
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(public_bp, url_prefix="/")

    # Comando para criar o banco de dados inicial
    @app.cli.command("init-db")
    def init_db_command():
        """Cria as tabelas do banco de dados."""
        with app.app_context():
            db.create_all()
        print("Banco de dados inicializado!")

    # Rota de teste inicial (pode ser removida ou mantida)
    @app.route("/hello")
    def hello():
        return "Olá! O aplicativo Flask está rodando."

    return app

# Para execução local (python src/main.py)
if __name__ == "__main__":
    app = create_app()
    # Escuta em 0.0.0.0 para ser acessível externamente se necessário
    # O modo debug NÃO deve ser usado em produção
    app.run(host="0.0.0.0", port=5000, debug=True)

