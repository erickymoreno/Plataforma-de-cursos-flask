from src import app, db
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from src.models.tables import (
    Curso,
    Topico,
    Leciona,
    Usuario,
    Matricula,
    Cursa,
    Certificado,
)
from datetime import datetime
import sys
import uuid


@app.route("/", methods=["GET", "POST"])
@app.route("/pagina/<int:pagina>")
def listarCursos(pagina = 1):
    if request.method == "GET":
        paginacao =Curso.query.paginate(page = pagina, per_page = 5)
        cursos = paginacao.items
        countCursos = len(Curso.query.all())
        total_pagina = paginacao.total
        return render_template("index.html", cursos=cursos, count=countCursos, total_pagina=total_pagina, pagina_atual=pagina)

    if request.method == "POST":
        pesquisa = request.form["inputSearch"]
        resultados = Curso.query.filter(Curso.nome.like("%" + pesquisa + "%")).all()

        mensagem = ""
        if not resultados:
            mensagem = "Não há cursos correspondentes com a pesquisa"

        paginacao =Curso.query.paginate(page = pagina, per_page = 5)
        print(resultados, file=sys.stderr)
        cursos = paginacao.items
        countCursos = len(Curso.query.all())
        total_pagina = paginacao.total
        return render_template(
            "index.html",
            cursos=cursos,
            count=countCursos,
            resultados=resultados,
            mensagem=mensagem,
            total_pagina=total_pagina, 
            pagina_atual=pagina
        )


@app.route("/curso/<curso_id>")
def detalhar_curso(curso_id):
    curso = Curso.query.filter_by(id=curso_id).first()
    topico = Topico.query.filter_by(curso_id=curso_id)
    relacionamento = (
        db.session.query(Usuario, Curso, Leciona)
        .select_from(Leciona)
        .join(Curso)
        .join(Usuario)
        .filter(Curso.id == curso_id)
    )

    return render_template(
        "detalhe_curso.html", curso=curso, topico=topico, relacionamento=relacionamento
    )


@app.route("/curso/<curso_id>/topico/<int:pagina>")
def topico(curso_id=1, pagina=1):
    itensPorPagina = 1
    topicos = Topico.query.filter_by(curso_id=curso_id).paginate(
        pagina, itensPorPagina, error_out=False
    )

    topico = Topico.query.filter_by(curso_id=curso_id).all()

    if not topico:
        mensagem = "Não há conteúdo disponível nesse curso"
        return render_template("erro.html", mensagem=mensagem)

    matricula = Matricula.query.filter_by(
        usuario_id=current_user.id, curso_id=curso_id
    ).first()

    cursa = Cursa.query.filter_by(
        matricula_id=matricula.id, topico_id=topico[pagina - 1].id
    ).first()

    if not cursa:
        cursa1 = Cursa(
            data_assistida=datetime.now(),
            matricula_id=matricula.id,
            topico_id=topico[pagina - 1].id,
            status="iniciado",
        )
        db.session.add(cursa1)
        db.session.commit()

    if pagina > 1:
        cursa = Cursa.query.filter_by(
            matricula_id=matricula.id, topico_id=topico[pagina - 2].id
        ).first()
        cursa.status = "concluido"
        db.session.commit()

    return render_template("topico.html", topicos=topicos, curso_id=curso_id)


@app.route("/curso/<curso_id>/finalizar")
def finalizarCurso(curso_id=1):
    matricula = Matricula.query.filter(
        Matricula.usuario_id.like(current_user.id),
        Matricula.curso_id.like(curso_id),
    ).first()

    matricula.data_fim = datetime.now()
    db.session.commit()

    existe_certificado = Certificado.query.filter_by(matricula_id=matricula.id).first()

    if not existe_certificado:
        certificado = Certificado(id=uuid.uuid4(), matricula_id=matricula.id)
        db.session.add(certificado)
        db.session.commit()

    return redirect("/")


@app.route("/curso/certificado/validar", methods=["GET", "POST"])
def validarCertificado():
    if request.method == "GET":
        return render_template("validar_certificado.html")

    if request.method == "POST":
        codigo = request.form["inputCodigo"]

        existe_certificado = Certificado.query.filter_by(id=codigo).first()

        if existe_certificado:
            query = (
                db.session.query(Usuario, Curso, Matricula, Certificado)
                .select_from(Matricula)
                .join(Usuario)
                .join(Curso)
                .join(Certificado)
                .filter(Certificado.id == codigo)
                .all()
            )
            return render_template("validar_certificado.html", query=query)

        if not existe_certificado:
            mensagem = "Não há nenhum certificado com esse código"
            return render_template("validar_certificado.html", mensagem=mensagem)