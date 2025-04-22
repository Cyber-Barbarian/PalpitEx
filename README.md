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

## Trabalhando no projeto
- criei um folder de ETL dentro da pasta do app
- criei um arquivo de teste [meu_codigo_teste.py](PalpitEx/palpitexApp/ETL/meu_codigo_teste.py)
- Edite o arquivo views.py do seu aplicativo
```python

from django.http import HttpResponse
from .ETL.meu_codigo_teste import soma

def minha_view(request):
    resultado = soma(3, 4)
    return HttpResponse(f"O resultado da soma é: {resultado}")


```
- Configure a URL para a view: Edite o arquivo urls.py do seu aplicativo [palpitexApp/urls.py](PalpitEx/palpitexApp/url.py):

```python
# palpitexApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('soma/', views.minha_view, name='minha_view'),
]
```
- Inclua as URLs do aplicativo no arquivo urls.py do projeto: Edite o arquivo [urls.py](PalpitEx/PalpitEx/urls.py) do seu projeto:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('palpitex/', include('palpitexApp.urls'))
]
```

- Execute as migrações iniciais: 
$ python manage.py migrate
- Inicie o servidor de desenvolvimento:
$ python manage.py runserver
- Acesse a URL no navegador: Abra o navegador e vá para http://127.0.0.1:8000/palpitex/soma/ para ver o resultado.

## Templates
- Dentro do nosso app vamos criar um diretório de Templates e dentro do settings.py vamos apontar para o template
```python
import os
...
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # ...
    },
]

```
- criamos uma página padrão [index.html](PalpitEx/palpitexApp/templates/index.html)
```html 
<!DOCTYPE html>
<html>
<head>
    <title>Meu Primeiro Template Django</title>
</head>
<body>
    <h1>Bem-vindo ao meu site!</h1>
    <p>Este é um exemplo simples de um template Django.</p>
</body>
</html>
```
- No arquivo views.py do seu aplicativo, adicione o seguinte código:
```python
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

```

- No arquivo urls.py do seu aplicativo palpitexApp, adicione o seguinte código:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

- Execute as migrações iniciais: 
$ python manage.py migrate
- Inicie o servidor de desenvolvimento:
$ python manage.py runserver
- Acesse a URL no navegador: Abra o navegador e vá para http://127.0.0.1:8000/palpitex/soma/ para ver o resultado.

- Inserindo Dados Dinâmicos
Os templates no Django também permitem que você insira dados dinâmicos em suas páginas. Vamos criar um exemplo simples em que exibimos o nome de um usuário.

Primeiro, atualize a view index no arquivo views.py:

```python 
def index(request):
    nome_usuario = "Palhaço Pirulito"
    return render(request, 'index.html', {'nome_usuario': nome_usuario})
```

- Agora, atualize o arquivo index.html para exibir o nome do usuário:
```python
<!DOCTYPE html>
<html>
<head>
    <title>Meu Primeiro Template Django</title>
</head>
<body>
    <h1>Bem-vindo ao meu site, {{ nome_usuario }}!</h1>
    <p>Este é um exemplo simples de um template Django.</p>
</body>
</html>
```

## user

$ python manage.py createsuperuser
Username: CyberBarbarian
Email address: 
Password: teste@Django_Palpitex
Password (again): teste@Django_Palpitex
Superuser created successfully.

- em admin.py > Make the poll app modifiable in the admin
  https://docs.djangoproject.com/en/5.2/intro/tutorial02/

## banco de dados

- sempre que alterar o models, deletar o banco de dados,  migrations e :
$ python manage.py makemigrations palpitexApp

$ python manage.py sqlmigrate palpitexApp 0001

obs: podemos executar a query diretamnete no banco de dados

$ python manage.py migrate

$ python manage.py runserver 
