# PalpitEx
Um repositório destinado à criação de um site que realize ETL de dados relativos à ações indexadas na bolsa de valores, com aplicação de data science e IA




## Iniciando o projeto


- Trabalhando com venv
$ python -m venv .venv
$ .venv/Scripts/activate

- Em seguida instalar o Django
$ pip install django 

- testar
$ django-admin
deve rodar sem erro

- iniciar projeto
$ django-admin startproject {nome_projeto}
no caso: $ django-admin startproject PalpitEx

- Servidor no manage.py

$ python PalpitEx/manage.py runserver

pode visitar em http://127.0.0.1:8000/

- Banco de dados
ao rodar pela primeira vez o projeto surge um banco de dados db.sqlite3. Pode ser deletado se quiser.

- explicando a estrutura
  - arquivo _init_.py -> vazio, somente para entender que é um projeto python
  - asgi.py e wsgi.py -> configurações para quando colocar o site num servidor (se o servidor é asgi ou wsgi)
  - urls -> é ali q ue se define os links do site (/blog, /user, /products...)
  - settings -> configurações, chave de segurança do banco de dados, databases, quais aplicativos, qual a lingauagem do site, qual o timezone ...

- todo projeto django é uma junção de apps
- dentro do projeto criado, vamos criar aplicativos
- para isso vamos até a pasta que contém o manage.py
$ cd PalpitEx
$ python manage.py startapp palpitexApp

- observe que dentro de um app também podemos ter diversos projetos
- para cada projeto criado devemos ir em settings.py e escrever o nome do app
```python
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'palpitexApp'
]
```

- dentro de cada app criado também temos muitos arquivos
    - a past migrations gerencia as modificações no banco de dados
    - no arquivo admin.py colocamos o que queremos que apareça na tela do site para o administrador
    - apps.py são os apps. podemos incluir apps dentro do app 
    - temos o arquivo de test.py para iniciar os testes
    - temos o arquivo de models.py, onde criamos o que é armazenado no banco de dados.
    - temos o arquivo de views.py, onde criamos a lógica do site para cada url. é o backend para os templates.
- templates
 em algum lugar ou do projeto ou do app precisamos criar uma pasta de templates, contendo os html, css e javascript

## Guardando os requisitos

No ambiente de seu projeto faça:
$ pip freeze > requirements.txt
No ambiente de produção, faça:
$ pip install -r requirements.txt