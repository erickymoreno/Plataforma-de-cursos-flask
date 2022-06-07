from src import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255))
    tipo = db.Column(db.String(63), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    foto = db.Column(db.String(255))

    def _repr_(self):
        return "<Usuario %d>" % self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome


class Matricula(db.Model):
    __tablename__ = "matricula"
    id = db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"))

    def _repr_(self):
        return "<Matricula %d>" % self.id


class Curso(db.Model):
    __tablename__ = "curso"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(511), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)

    def _repr_(self):
        return "<Curso %d>" % self.id


class Topico(db.Model):
    __tablename__ = "topico"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    conteudo = db.Column(db.UnicodeText, nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"))

    def _repr_(self):
        return "<Topico %d>" % self.id


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

    def _repr_(self):
        return "<Tag %d>" % self.id


class Leciona(db.Model):
    __tablename__ = "leciona"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"))

    def _repr_(self):
        return "<Leciona %d>" % self.id


class Cursa(db.Model):
    __tablename__ = "cursa"
    id = db.Column(db.Integer, primary_key=True)
    data_assistida = db.Column(db.DateTime, nullable=False)
    matricula_id = db.Column(db.Integer, db.ForeignKey("matricula.id"))
    topico_id = db.Column(db.Integer, db.ForeignKey("topico.id"))
    status = db.Column(db.String(255), default="não iniciado")

    def _repr_(self):
        return "<Cursa %d>" % self.id


class Identifica(db.Model):
    __tablename__ = "identifica"
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey("curso.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))

    def _repr_(self):
        return "<Identifica %d>" % self.id

class Certificado(db.Model):
    __tablename__ ="certificado"
    id = db.Column(db.String(255), primary_key=True)
    matricula_id = db.Column(db.Integer, db.ForeignKey("matricula.id"))
   
    def _repr_(self):
        return "<Certificado %d>" % self.id
