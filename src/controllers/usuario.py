from src import app, db, login_manager
from flask import render_template, redirect, url_for, request, session
from flask_login import login_required, current_user, login_user, logout_user
from src.models.tables import Usuario, Curso, Matricula, Topico, Certificado
from datetime import datetime
from dotenv import load_dotenv
from email.message import EmailMessage
import bcrypt, sys, uuid, os, smtplib

load_dotenv()

DICT_MONTHS = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro",
}


def get_month_name(m):
    return DICT_MONTHS[m]


@login_manager.user_loader
def get_user(usuario_id):
    return Usuario.query.filter_by(id=usuario_id).first()


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        mensagem = request.args.get("mensagem")
        return render_template("login.html", mensagem=mensagem)

    if request.method == "POST":
        email = request.form["inputEmail"]
        senha = request.form["inputSenha"]

        usuario = Usuario.query.filter_by(email=email).first()
        autozidado = False

        if usuario:
            autorizado = bcrypt.checkpw(
                senha.encode("utf8"), usuario.senha.encode("utf8")
            )

        if not usuario or not autorizado:
            mensagem = "Login não autorizado"
            return render_template("login.html", mensagem=mensagem)
        else:
            login_user(usuario)
            return redirect("/home")


@app.route("/home")
@login_required
def home():
    certificados = (
        db.session.query(Matricula, Certificado, Curso)
        .select_from(Matricula)
        .join(Certificado)
        .join(Curso)
        .filter(Matricula.usuario_id == current_user.id)
        .all()
    )
    matriculas = (
        db.session.query(Usuario, Curso, Matricula)
        .select_from(Matricula)
        .join(Usuario)
        .join(Curso)
        .filter(Usuario.id == current_user.id)
        .filter(Matricula.data_fim == None)
    )
    return render_template(
        "home.html", matriculas=matriculas, certificados=certificados
    )


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        mensagem = request.args.get("mensagem")
        return render_template("cadastro.html")

    if request.method == "POST":
        nome = request.form["inputNome"]

        existe_email = Usuario.query.filter_by(email=request.form["inputEmail"]).all()
        if not existe_email:
            email = request.form["inputEmail"]
        else:
            mensagem = "Email já cadastrado"
            return render_template("cadastro.html", mensagem=mensagem)

        if request.form["inputSenha"] == request.form["inputConfirmarSenha"]:
            senha = request.form["inputSenha"]
        else:
            mensagem = "As senhas não correspondem"
            return render_template("cadastro.html", mensagem=mensagem)
        senhaEcriptada = bcrypt.hashpw(senha.encode("UTF-8"), bcrypt.gensalt())
        tipo = "padrão"
        token = str(uuid.uuid4())
        usuario = Usuario(
            nome=nome, email=email, senha=senhaEcriptada, tipo=tipo, token=token
        )

        db.session.add(usuario)
        db.session.commit()

    return redirect("/")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@app.route("/curso/<curso_id>/iniciar")
@login_required
def matriculaCurso(curso_id=1):
    matricula = Matricula.query.filter(
        Matricula.usuario_id.like(current_user.id),
        Matricula.curso_id.like(curso_id),
    ).first()
    if not matricula:
        pagina = 1
        m1 = Matricula(
            data_inicio=datetime.now(), usuario_id=current_user.id, curso_id=curso_id
        )
        db.session.add(m1)
        db.session.commit()

    else:
        pagina = 1

    return redirect(url_for("topico", curso_id=curso_id, pagina=pagina))


@app.route("/matricula/<matricula_id>/certificado")
@login_required
def certificado(matricula_id):
    query = (
        db.session.query(Usuario, Curso, Matricula, Certificado)
        .select_from(Matricula)
        .join(Usuario)
        .join(Curso)
        .join(Certificado)
        .filter(Matricula.id == matricula_id)
        .filter(Usuario.id == current_user.id)
        .all()
    )
    for r in query:
        curso = r.Curso.id
        data = r.Matricula.data_fim
    topico = Topico.query.filter_by(curso_id=curso).all()
    mes = get_month_name(data.month)
    data = f"Vilhena - RO, {data.day} de {mes} de {data.year}"

    return render_template("certificado.html", query=query, topico=topico, data=data)


@app.route("/esqueci_minha_senha", methods=["GET", "POST"])
def esqueciSenha():
    if request.method == "GET":
        return render_template("esqueci_senha.html")

    if request.method == "POST":
        email = request.form["inputEmail"]
        token = str(uuid.uuid4())
        existe_email = Usuario.query.filter_by(email=email).first()
        print(existe_email.token, file=sys.stderr)

        if not existe_email:
            mensagem = "Email não corresponde"
            return render_template("esqueci_senha.html", mensagem=mensagem)

        else:
            existe_email.token = token
            db.session.commit()

            s = smtplib.SMTP(host="smtp.gmail.com", port=587)
            s.starttls()
            s.login(os.getenv("SMTP_MAIL"), os.getenv("SMTP_PASS"))
            email = EmailMessage()
            email.set_content(
                f"Redefina sua senha a partir daqui <localhost:5000/redefinir/{token}>"
            )

            email["Subject"] = "Redefinição de senha"
            email["From"] = os.getenv("SMTP_MAIL")
            email["To"] = f"{existe_email.email}"
            s.send_message(email)
            s.quit()

            mensagem = "Email de redefinição enviado"
            return render_template("esqueci_senha.html", mensagem=mensagem)


@app.route("/redefinir/<token>", methods=["GET", "POST"])
def redefinirSenha(token):
    if request.method == "GET":
        return render_template("redefinir_senha.html")

    if request.method == "POST":
        tokenAux = str(uuid.uuid4())
        existe_usuario = Usuario.query.filter_by(token=token).first()

        if existe_usuario:
            if request.form["inputSenha"] == request.form["inputConfirmarSenha"]:
                senha = request.form["inputSenha"]
                senha = bcrypt.hashpw(senha.encode("UTF-8"), bcrypt.gensalt())

                existe_usuario.senha = senha
                existe_usuario.token = tokenAux
                db.session.commit()
            else:
                mensagem = "As senhas não correspondem"
                return render_template("redefinir_senha.html", mensagem=mensagem)

        else:
            mensagem = "Token de redefinição inválido"
            return render_template("erro.html", mensagem=mensagem)

    return render_template("login.html")
