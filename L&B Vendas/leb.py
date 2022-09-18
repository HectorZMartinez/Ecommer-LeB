from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect
from flask_login import (current_user, LoginManager,
                         login_user, logout_user,
                         login_required)
import hashlib


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://Hector2332:2332@Hector2332.mysql.pythonanywhere-services.com:3306/Hector2332$banquin"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.secret_key = "VouLhePegarPikomon"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class Usuario(db.Model):
    __tablename__ = "usuario"
    usuario_id = db.Column("usuario_id", db.Integer, primary_key=True)
    usuario_nome = db.Column("usuario_nome", db.String(256))
    usuario_email = db.Column("usuario_email", db.String(256))
    usuario_senha = db.Column("usuario_senha", db.String(256))
    usuario_ende = db.Column("usuario_ende", db.String(256))

    def __init__(self, nome, email, senha, ende):
        self.usuario_nome = nome
        self.usuario_email = email
        self.usuario_senha = senha
        self.usuario_ende = ende

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.usuario_id)


class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column("categoria_id", db.Integer, primary_key=True)
    nome = db.Column("categoria_nome", db.String(256))
    descricao = db.Column("categoria_descricao", db.String(256))

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao


class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column("anuncio_id", db.Integer, primary_key=True)
    nome = db.Column("anuncio_nome", db.String(256))
    descricao = db.Column("anuncio_descricao", db.String(256))
    quantidade = db.Column("anuncio_quantidade", db.Integer)
    preco = db.Column("anuncio_preco", db.Float)
    categoria_id = db.Column("categoria_id", db.Integer,
                             db.ForeignKey("categoria.categoria_id"))
    usuario_id = db.Column("usuario_id", db.Integer,
                           db.ForeignKey("usuario.usuario_id"))

    def __init__(self, nome, descricao, quantidade, preco, categoria_id, usuario_id):
        self.nome = nome
        self.descricao = descricao
        self.quantidade = quantidade
        self.preco = preco
        self.categoria_id = categoria_id
        self.usuario_id = usuario_id


class Compra(db.Model):
    __tablename__ = "compra"
    id = db.Column("compra_id", db.Integer, primary_key=True)
    preco = db.Column("compra_preco", db.Float)
    quantidade = db.Column("compra_quantidade", db.Integer)
    total = db.Column("compra_total", db.Float)
    anuncio_id = db.Column("anuncio_id", db.Integer,
                           db.ForeignKey("anuncio.anuncio_id"))
    usuario_id = db.Column("usuario_id", db.Integer,
                           db.ForeignKey("usuario.usuario_id"))

    def __init__(self, preco, quantidade, total, anuncio_id, usuario_id):
        self.preco = preco
        self.quantidade = quantidade
        self.total = total
        self.anuncio_id = anuncio_id
        self.usuario_id = usuario_id


@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template("naoacho.html")


@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = hashlib.sha512(
            str(request.form.get("senha")).encode("utf-8")).hexdigest()

        user = Usuario.query.filter_by(
            usuario_email=email, usuario_senha=senha).first()

        if user:
            login_user(user)
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/")
def index():
    db.create_all()
    return render_template("index.html")


@app.route("/compras")
@login_required
def compras():
    return render_template("compras.html")


@app.route("/cad/usuario")
@login_required
def usuario():
    return render_template("usuario.html", usuarios=Usuario.query.all(), titulo="Usuario")


@app.route("/usuario/criar", methods=["POST"])
def novousuario():
    hash = hashlib.sha512(str(request.form.get(
        "senha")).encode("utf-8")).hexdigest()
    usuario = Usuario(request.form.get("user"), request.form.get(
        "email"), hash, request.form.get("ende"))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for("usuario"))


@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome


@app.route("/usuario/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == "POST":
        usuario.nome = request.form.get("user")
        usuario.email = request.form.get("email")
        usuario.senha = hash = hashlib.sha512(str(request.form.get(
            "senha")).encode("utf-8")).hexdigest()
        usuario.ende = request.form.get("ende")
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for("usuario"))

    return render_template("editaruser.html", usuario=usuario, titulo="Usuario")


@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for("usuario"))


@app.route("/anuncio/deletar/<int:id>")
def deletaranuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for("anuncio"))


@app.route("/cad/anuncio")
@login_required
def anuncio():
    anuncios = Anuncio.query.all()
    for anuncio in anuncios:
        anuncio.mostrarbotCompra = current_user.usuario_id != anuncio.usuario_id
    print(anuncios[0].mostrarbotCompra)
    return render_template("anuncio.html", anuncios=anuncios, categorias=Categoria.query.all(), titulo="Anuncio")


@app.route("/anuncio/criar", methods=["POST"])
def novoanuncio():
    anuncio = Anuncio(request.form.get("nome"), request.form.get("descricao"), request.form.get(
        "quantidade"), request.form.get("preco"), request.form.get("categoria"), current_user.usuario_id)
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for("anuncio"))


@app.route("/anuncio/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editaranuncio(id):
    anuncio = Anuncio.query.get(id)
    if request.method == "POST":
        anuncio.nome = request.form.get("nome")
        anuncio.descricao = request.form.get("descricao")
        anuncio.quantidade = request.form.get("quantidade")
        anuncio.preco = request.form.get("preco")
        anuncio.categoria_id = request.form.get("categoria_id")
        anuncio.usuario_id = request.form.get("usuario_id")
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for("anuncio"))

    return render_template("editaranuncio.html", anuncio=anuncio, titulo="Anuncio")


@app.route("/categoria/deletar/<int:id>")
def deletarcategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for("categoria"))


@app.route("/config/categoria")
def categoria():
    return render_template("categoria.html",  categorias=Categoria.query.all(), titulo="Categoria")


@app.route("/categoria/criar", methods=["POST"])
def novacategoria():
    categoria = Categoria(request.form.get(
        "nome"), request.form.get("descricao"))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for("categoria"))


@app.route("/categoria/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editarcategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == "POST":
        categoria.nome = request.form.get("nome")
        categoria.descricao = request.form.get("descricao")
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for("categoria"))

    return render_template("editarcategoria.html", categoria=categoria, titulo="Categoria")


if __name__ == "leb":
    db.create_all()
    app.run()
