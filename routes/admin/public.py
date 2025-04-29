# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

# Importar modelos do banco de dados
from src.models import db, Modulo, Aula, Comentario

public_bp = Blueprint("public", __name__, template_folder="../templates/public")

# --- Área Pública --- #

@public_bp.route("/") # Rota principal
def index():
    """Exibe a lista de módulos disponíveis."""
    modulos = Modulo.query.order_by(Modulo.id).all()
    return render_template("index.html", modulos=modulos)

@public_bp.route("/modulo/<int:id>")
def ver_modulo(id):
    """Exibe as aulas de um módulo específico."""
    # Busca o módulo e carrega suas aulas ansiosamente
    modulo = Modulo.query.options(db.joinedload(Modulo.aulas)).get_or_404(id)
    return render_template("modulo.html", modulo=modulo)

@public_bp.route("/aula/<int:id>", methods=["GET", "POST"])
def ver_aula(id):
    """Exibe uma aula específica, seu vídeo, descrição e comentários."""
    # Busca a aula e carrega seus comentários ansiosamente, ordenados por data
    aula = Aula.query.options(db.joinedload(Aula.comentarios)).get_or_404(id)

    if request.method == "POST":
        nome_aluno = request.form.get("nome_aluno")
        mensagem = request.form.get("mensagem")
        if nome_aluno and mensagem:
            novo_comentario = Comentario(
                nome_aluno=nome_aluno,
                mensagem=mensagem,
                aula_id=id,
                data_criacao=datetime.utcnow()
            )
            db.session.add(novo_comentario)
            db.session.commit()
            flash("Comentário enviado com sucesso!", "success")
            # Recarrega a página da aula para mostrar o novo comentário
            return redirect(url_for("public.ver_aula", id=id))
        else:
            flash("Por favor, preencha seu nome e a mensagem.", "warning")

    # Ordena os comentários pela data de criação (mais recentes primeiro) para exibição
    comentarios_ordenados = sorted(aula.comentarios, key=lambda c: c.data_criacao, reverse=True)

    return render_template("aula.html", aula=aula, comentarios=comentarios_ordenados)

