# from src import db
# from src.models.tables import (
#     Usuario,
#     Curso,
#     Matricula,
#     Topico,
#     Tag,
#     Leciona,
#     Cursa,
#     Identifica,
# )
# from datetime import date
# import bcrypt

# # Criando usuários
# senha = "123"
# senhaEncriptada = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
# u1 = Usuario(
#     nome="Wandreus Mühl Dourado",
#     email="wandreusmuhl70@gmail.com",
#     senha=senhaEncriptada,
#     tipo="padrao",
# )
# u2 = Usuario(
#     nome="Marco Andrade",
#     email="marco.andrade@mail",
#     senha=senhaEncriptada,
#     tipo="instrutor",
# )
# u3 = Usuario(
#     nome="Ericky Moreno Mamede",
#     email="ericky.moreno@mail.com",
#     senha=senhaEncriptada,
#     tipo="padrao",
# )
# db.session.add(u1)
# db.session.add(u2)
# db.session.add(u3)
# db.session.commit()

# # Criando cursos
# c1 = Curso(
#     nome="Curso de Git e GitHub",
#     descricao="Nesse curso você vai aprender o funcionamento basico do git e github",
#     carga_horaria=10,
# )
# c2 = Curso(
#     nome="Prototipação com Figma",
#     descricao="Nesse curso você vai aprender do basico ao avançado na criação e desenvolvimento de prototipos de software",
#     carga_horaria=10,
# )
# c3 = Curso(
#     nome="Planilhas eletrônicas",
#     descricao="Durante esse curso você vai aprender o processo de criação de planilhas eletrônicas",
#     carga_horaria=10,
# )
# c4 = Curso(
#     nome="Edição de vídeos",
#     descricao="Nesse curso você vai aprender edição de vídeos",
#     carga_horaria=10,
# )
# c5 = Curso(
#     nome="Ediçao de áudio",
#     descricao="Nesse curso você vai aprender edição de áudio",
#     carga_horaria=10,
# )
# c6 = Curso(
#     nome="Desenvolvimento Web",
#     descricao="Nesse curso você vai aprender desenvolvimento Web",
#     carga_horaria=20,
# )
# c7 = Curso(
#     nome="Python", descricao="Nesse curso você vai aprender Python", carga_horaria=10
# )

# db.session.add(c1)
# db.session.add(c2)
# db.session.add(c3)
# db.session.add(c4)
# db.session.add(c5)
# db.session.add(c6)
# db.session.add(c7)
# db.session.commit()

# # # Criando matrículas

# # Criando tópicos
# t1 = Topico(titulo="Aula 1 - Introdução", conteudo="aaa", curso_id=c1.id)
# t2 = Topico(titulo="Aula 2 - Primeiros passos", conteudo="aaa", curso_id=c1.id)
# t3 = Topico(titulo="Aula 3 - Primeiro commit", conteudo="aaa", curso_id=c1.id)
# t4 = Topico(titulo="Aula 4 - Revertendo alterações", conteudo="aaa", curso_id=c1.id)
# t5 = Topico(titulo="Aula 5 - Resolvendo conflitos", conteudo="aaa", curso_id=c1.id)

# db.session.add(t1)
# db.session.add(t2)
# db.session.add(t3)
# db.session.add(t4)
# db.session.add(t5)
# db.session.commit()


# # Relacionando professor com curso
# l1 = Leciona(usuario_id=u2.id, curso_id=c1.id)
# l2 = Leciona(usuario_id=u3.id, curso_id=c2.id)
# db.session.add(l1)
# db.session.add(l2)
# db.session.commit()