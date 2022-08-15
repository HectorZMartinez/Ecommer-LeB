from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:2332@localhost:3306/banquin"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column("usuario_id", db.Integer, primary_key=True)
    nome = db.Column("usuario_nome", db.String(256))
    email = db.Column("usuario_email", db.String(256))
    senha = db.Column("usuario_senha", db.String(256))
    ende = db.Column("usuario_ende", db.String(256))

    def __init__(self, nome, email, senha, ende):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ende = ende


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


@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('naoacho.html')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cad/usuario")
def usuario():
    return render_template("usuario.html", usuarios=Usuario.query.all(), titulo="Usuario")


@app.route("/usuario/criar", methods=["POST"])
def novousuario():
    usuario = Usuario(request.form.get("user"), request.form.get(
        "email"), request.form.get("passwd"), request.form.get("ende"))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for("usuario"))


@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome


@app.route("/usuario/editar/<int:id>", methods=["GET", "POST"])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == "POST":
        usuario.nome = request.form.get("user")
        usuario.email = request.form.get("email")
        usuario.senha = request.form.get("passwd")
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
def anuncio():
    return render_template("anuncio.html", anuncios=Anuncio.query.all(), categorias=Categoria.query.all(), titulo="Anuncio")


@app.route("/anuncio/criar", methods=["POST"])
def novoanuncio():
    anuncio = Anuncio(request.form.get("nome"), request.form.get("descricao"), request.form.get(
        "quantidade"), request.form.get("preco"), request.form.get("categoria"), request.form.get("usuario"))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for("anuncio"))


@app.route("/anuncio/editar/<int:id>", methods=["GET", "POST"])
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
def editarcategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == "POST":
        categoria.nome = request.form.get("nome")
        categoria.descricao = request.form.get("descricao")
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for("categoria"))

    return render_template("editarcategoria.html", categoria=categoria, titulo="Categoria")


@app.route("/relatorios/vendas")
def reportVenda():
    return render_template("reportVenda.html")


@app.route("/relatorios/compras")
def reportCompra():
    return render_template("reportCompra.html")


if __name__ == "leb":
    print("leb")
    db.create_all()
