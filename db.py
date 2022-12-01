from flask import Flask
from orator import DatabaseManager, Schema
from flask_orator import Orator


app = Flask(__name__)
app.config['ORATOR_DATABASES'] = {
    'development': {
        'driver': 'mysql',
        'host': 'us-cdbr-east-05.cleardb.net',
        'database': 'heroku_2a75a8daff3ffa6',
        'user': 'b4d5cceb281dab',
        'password': 'a5eda933'
    }
}

ORATOR_DATABASES = {
    'development': {
        'driver': 'mysql',
        'host': 'us-cdbr-east-05.cleardb.net',
        'database': 'heroku_2a75a8daff3ffa6',
        'user': 'b4d5cceb281dab',
        'password': 'a5eda933'
    }
}

db = Orator(app)
schema = Schema(db)

if __name__ == '__main__':
    db.cli.run()
