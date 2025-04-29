from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Modulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    # Relacionamento com Aulas (um módulo tem muitas aulas)
    aulas = db.relationship("Aula", backref="modulo", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Modulo {self.id}: {self.titulo}>"

class Aula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    duracao = db.Column(db.String(50), nullable=True) # Ex: "10 min"
    link_video = db.Column(db.String(300), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    modulo_id = db.Column(db.Integer, db.ForeignKey("modulo.id"), nullable=False)
    # Relacionamento com Comentários (uma aula tem muitos comentários)
    comentarios = db.relationship("Comentario", backref="aula", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Aula {self.id}: {self.titulo} (Módulo {self.modulo_id})>"

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_aluno = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    aula_id = db.Column(db.Integer, db.ForeignKey("aula.id"), nullable=False)

    def __repr__(self):
        return f"<Comentario {self.id} por {self.nome_aluno} na Aula {self.aula_id}>"

