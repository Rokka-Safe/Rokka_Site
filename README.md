# Rokka


### API Installation :


First of all : install python 2.7
Then :

```
<<<<<<< HEAD
sudo apt-get install python-pip
pip install flask
=======
git clone https://github.com/Rokka-Safe/Rokka_Site.git
cd Rokka_Site
sudo apt-get install pip
sudo apt-get install python-setuptools
pip install -r requirements.txt
>>>>>>> 2becb01b2a2e2205e2d847bb1a67e7e32111ff70
export FLASK_ENV=development
python -m flask run
```

check server at **localhost:5000**

### Sqlite

In terminal :

```
sudo apt-get install sqlite3 libsqlite3-dev -y
sqlite -version
sqlite3 rokka.db
```

in sqlite console:

```
.databases
```

*This will output the path to the database*

then in file add :

``` python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/apprenant/Bureau/Rokka_Site/rokka.db'
db = SQLAlchemy(app)

```

in python console:

```
from app import db
db.create_all()
```

*This will create the tables in your database*