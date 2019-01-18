# Rokka


### API Installation :


First of all : install python 2.7
Then :

```
sudo apt-get install python-pip
pip install flask
git clone https://github.com/Rokka-Safe/Rokka_Site.git
cd Rokka_Site
sudo apt-get install python-setuptools
pip install -r requirements.txt
export FLASK_ENV=development
python -m flask run
```

For some people :

```
export FLASK_APP=app.py
```

check server at **localhost:5000**

### Sqlite

In terminal :

```
sudo apt-get install sqlite3 libsqlite3-dev -y
sqlite3 -version
sqlite3 rokka.db
```

in sqlite console:

```
.databases
```

*This will output the path to the database*

then in your .env file, add this line to connect db:
```
SQLALCHEMY_DATABASE_URI="sqlite:////path/to/your/database.db"
```

in python console:

```
from app import db
db.create_all()
```

*This will create the tables in your database*

