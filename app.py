from flask import Flask, redirect, render_template, request, url_for, flash
from sqlalchemy import select

from database import Base, engine, SessionLocal
from models import Usuario, Livro


app = Flask(__name__)
app.secret_key = "biblioteca123"

Base.metadata.create_all(engine)


@app.route("/")
def index():
    with SessionLocal() as session:
        usuarios = session.scalars(
            select(Usuario).order_by(Usuario.nome)
        ).all()

        return render_template(
            "index.html",
            usuarios=usuarios
        )


@app.route("/usuarios/novo", methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")

        if nome and email:
            with SessionLocal() as session:
                usuario = session.scalar(
                    select(Usuario).where(Usuario.email == email)
                )

                if not usuario:
                    usuario_novo = Usuario(
                        nome=nome,
                        email=email
                    )

                    session.add(usuario_novo)
                    session.commit()

                    flash("Usuário cadastrado com sucesso!")

                else:
                    flash("Este e-mail já está cadastrado.")

            return redirect(url_for("index"))

        flash("Preencha todos os campos.")

    return render_template("cadastro.html")


@app.route("/livros/novo", methods=["GET", "POST"])
def new_book():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        usuario_id = request.form.get("usuario")

        if titulo and usuario_id:
            with SessionLocal() as session:
                usuario = session.get(Usuario, int(usuario_id))

                if usuario:
                    livro_existente = session.scalar(
                        select(Livro).where(Livro.titulo == titulo)
                    )

                    if not livro_existente:
                        livro_novo = Livro(
                            titulo=titulo,
                            usuario_id=int(usuario_id)
                        )

                        session.add(livro_novo)
                        session.commit()

                        flash("Livro cadastrado com sucesso!")

                    else:
                        flash("Este livro já está cadastrado.")

                else:
                    flash("Usuário não encontrado.")

            return redirect(url_for("listar_livro"))

        flash("Preencha todos os campos.")

    with SessionLocal() as session:
        usuarios = session.scalars(
            select(Usuario).order_by(Usuario.nome)
        ).all()

        return render_template(
            "cadastro_livro.html",
            usuarios=usuarios
        )


@app.route("/livros/listar")
def listar_livro():
    with SessionLocal() as session:
        livros = session.scalars(
            select(Livro).order_by(Livro.titulo)
        ).all()

        return render_template(
            "livros.html",
            livros=livros
        )


if __name__ == "__main__":
    app.run(debug=True)
