## Configuração inicial
pipenv --three
pipenv shell
pipenv install


## Migrations
### Inicializando
python3 migrations.py db init

### Verificando se há alterações
python3 migrations.py db migrate

### Realizando as alterações
python3 migrations.py db upgrade


## Branches
Nunca codifiquem na branch **master**.

### Clonando a branch development
git clone -b development https://gitlab.fslab.dev/marco/plataforma_cursos.git

### Criando uma nova branch
git checkout -b nova_funcionalidade

### Listando as branches
git branch

### Enviando a branch para o repositório remoto
git push -u origin nova_funcionalidade