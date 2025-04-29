# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from functools import wraps

# Importar modelos do banco de dados (serão usados depois)
# from src.models import db, Modulo, Aula, Comentario

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")

# --- Autenticação Simples (Hardcoded) ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "receitas123"

# Decorator para exigir login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_logged_in" not in session:
            flash("Por favor, faça login para acessar esta página.", "warning")
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    # Se já estiver logado, redireciona para o dashboard
    if "admin_logged_in" in session:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Usuário ou senha inválidos.", "danger")
    return render_template("login.html")

@admin_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    flash("Você foi desconectado.", "info")
    return redirect(url_for("admin.login"))

# --- Dashboard --- #
@admin_bp.route("/") # Rota raiz do admin (/admin/)
@login_required
def dashboard():
    # Lógica para buscar dados do dashboard (total de módulos, aulas, etc.)
    # total_modulos = Modulo.query.count()
    # total_aulas = Aula.query.count()
    # total_comentarios = Comentario.query.count()
    stats = {"modulos": 0, "aulas": 0, "comentarios": 0} # Placeholder
    return render_template("dashboard.html", stats=stats)

# --- Gerenciamento de Módulos --- #
@admin_bp.route("/modulos")
@login_required
def listar_modulos():
    # Lógica para buscar módulos do DB
    # modulos = Modulo.query.order_by(Modulo.id).all()
    modulos = [] # Placeholder
    return render_template("modulos_listar.html", modulos=modulos)

@admin_bp.route("/modulos/adicionar", methods=["GET", "POST"])
@login_required
def adicionar_modulo():
    if request.method == "POST":
        # Lógica para adicionar módulo no DB
        # titulo = request.form.get("titulo")
        # descricao = request.form.get("descricao")
        # novo_modulo = Modulo(titulo=titulo, descricao=descricao)
        # db.session.add(novo_modulo)
        # db.session.commit()
        flash("Módulo adicionado com sucesso!", "success")
        return redirect(url_for("admin.listar_modulos"))
    return render_template("modulos_form.html", form_action=url_for("admin.adicionar_modulo"))

@admin_bp.route("/modulos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_modulo(id):
    # Lógica para buscar módulo pelo ID
    # modulo = Modulo.query.get_or_404(id)
    modulo = {"id": id, "titulo": "Placeholder", "descricao": "Placeholder"} # Placeholder
    if request.method == "POST":
        # Lógica para atualizar módulo no DB
        # modulo.titulo = request.form.get("titulo")
        # modulo.descricao = request.form.get("descricao")
        # db.session.commit()
        flash("Módulo atualizado com sucesso!", "success")
        return redirect(url_for("admin.listar_modulos"))
    return render_template("modulos_form.html", modulo=modulo, form_action=url_for("admin.editar_modulo", id=id))

@admin_bp.route("/modulos/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_modulo(id):
    # Lógica para excluir módulo do DB
    # modulo = Modulo.query.get_or_404(id)
    # db.session.delete(modulo)
    # db.session.commit()
    flash("Módulo excluído com sucesso!", "success")
    return redirect(url_for("admin.listar_modulos"))

# --- Gerenciamento de Aulas --- #
@admin_bp.route("/aulas")
@login_required
def listar_aulas():
    # Lógica para buscar aulas do DB com info do módulo
    # aulas = Aula.query.options(db.joinedload(Aula.modulo)).order_by(Aula.modulo_id, Aula.id).all()
    aulas = [] # Placeholder
    return render_template("aulas_listar.html", aulas=aulas)

@admin_bp.route("/aulas/adicionar", methods=["GET", "POST"])
@login_required
def adicionar_aula():
    # Lógica para buscar módulos (para associar a aula)
    # modulos = Modulo.query.order_by(Modulo.titulo).all()
    modulos = [] # Placeholder
    if request.method == "POST":
        # Lógica para adicionar aula no DB
        # modulo_id = request.form.get("modulo_id")
        # titulo = request.form.get("titulo")
        # duracao = request.form.get("duracao")
        # link_video = request.form.get("link_video")
        # descricao = request.form.get("descricao")
        # nova_aula = Aula(modulo_id=modulo_id, titulo=titulo, duracao=duracao, link_video=link_video, descricao=descricao)
        # db.session.add(nova_aula)
        # db.session.commit()
        flash("Aula adicionada com sucesso!", "success")
        return redirect(url_for("admin.listar_aulas"))
    return render_template("aulas_form.html", modulos=modulos, form_action=url_for("admin.adicionar_aula"))

@admin_bp.route("/aulas/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_aula(id):
    # Lógica para buscar aula pelo ID e módulos
    # aula = Aula.query.get_or_404(id)
    # modulos = Modulo.query.order_by(Modulo.titulo).all()
    aula = {"id": id, "titulo": "Placeholder", "duracao": "", "link_video": "", "descricao": "", "modulo_id": 0} # Placeholder
    modulos = [] # Placeholder
    if request.method == "POST":
        # Lógica para atualizar aula no DB
        # aula.modulo_id = request.form.get("modulo_id")
        # aula.titulo = request.form.get("titulo")
        # aula.duracao = request.form.get("duracao")
        # aula.link_video = request.form.get("link_video")
        # aula.descricao = request.form.get("descricao")
        # db.session.commit()
        flash("Aula atualizada com sucesso!", "success")
        return redirect(url_for("admin.listar_aulas"))
    return render_template("aulas_form.html", aula=aula, modulos=modulos, form_action=url_for("admin.editar_aula", id=id))

@admin_bp.route("/aulas/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_aula(id):
    # Lógica para excluir aula do DB
    # aula = Aula.query.get_or_404(id)
    # db.session.delete(aula)
    # db.session.commit()
    flash("Aula excluída com sucesso!", "success")
    return redirect(url_for("admin.listar_aulas"))

# --- Visualização de Comentários --- #
@admin_bp.route("/comentarios")
@login_required
def listar_comentarios():
    # Lógica para buscar comentários do DB com info da aula
    # comentarios = Comentario.query.options(db.joinedload(Comentario.aula)).order_by(Comentario.data_criacao.desc()).all()
    comentarios = [] # Placeholder
    return render_template("comentarios_listar.html", comentarios=comentarios)

