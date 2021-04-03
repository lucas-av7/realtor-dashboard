# Realtor Dashboard

An admin dashboard to register properties to sell or rent.

## Run the project

__First__: create a virtual environment and install the dependencies. I'm using [pipenv](https://pypi.org/project/pipenv/).

```bash
pipenv shell
pipenv install
```

__Second__: you need a MySQL DB. I'm using [MySQL Docker image](https://hub.docker.com/_/mysql).

```bash
docker-compose -f db/docker-compose.yml up -d
```

After that, go to the MySQL dashboard on `localhost:8080`, create a database and a user for MySQL connections.
Also, import the .sql file located inside the `db` folder.
To login on dashboard use: `username: root`, `password: example`.

__Third__: initialize the app

Copy `.env.example` to `.env` and fill the values.

Get your `IMGBB_KEY` [here](https://api.imgbb.com).

_Note: for using the recovery password feature you need an email server. You can use [Gmail](https://developers.google.com/gmail/imap/imap-smtp) for this._

```bash
flask run
```

Now you can visit `localhost:5000/painel-admin`

## Features

### Create, view, edit and delete

- Properties
- Property images
- Categories
- Partner realtors
- Real estate info

### Possibilities

- Partner realtors can use the dashboard with permissions levels
- Create custom permissions levels for partners
- Password recovery by email
- Enable/disable properties, categories, etc
- List all partner realtors and their registered properties
- Enable/disable partner realtors

## Technologies and tools used

- [Bootstrap](https://getbootstrap.com/)
- [CKEditor](https://ckeditor.com/)
- [Docker](https://www.docker.com/)
- [Flask-mail](https://pythonhosted.org/Flask-Mail/)
- [Flask-mysqldb](https://flask-mysqldb.readthedocs.io/en/latest/)
- [Flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [IMGBB](https://api.imgbb.com)
- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
- [MySQL](https://www.mysql.com/)
- [Passlib](https://passlib.readthedocs.io/en/stable/)
- [Requests](https://docs.python-requests.org/en/master/)
