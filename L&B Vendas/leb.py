from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cad/usuario")
def usuario():
    return render_template("usuario.html", titulo="Cadastro Usuario")


@app.route("/cad/login")
def login():
    return render_template("login.html")


@app.route("/cad/caduser", methods=['POST'])
def caduser():
    return request.form


@app.route("/cad/anuncio")
def anuncio():
    return render_template("anuncio.html")


@app.route("/anuncios/pergunta")
def pergunta():
    return render_template("comentario.html")


@app.route("/anuncio/favoritos")
def favorito():
    return render_template("favorito.html")


@app.route("/config/categoria")
def categoria():
    return render_template("categoria.html")


@app.route("/relatorios/vendas")
def reportVenda():
    return render_template("reportVenda.html")


@app.route("/relatorios/compras")
def reportCompra():
    return render_template("reportCompra.html")
