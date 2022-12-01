from flask_orator import Orator
from flask import Flask


ORATOR_DATABASES = {
    'development': {
        'driver': 'mysql',
        'host': 'us-cdbr-east-05.cleardb.net',
        'database': 'heroku_2a75a8daff3ffa6',
        'user': 'b4d5cceb281dab',
        'password': 'a5eda933'
    }
}
app = Flask(__name__)
app.config.from_object(__name__)
db = Orator(app)


class User(db.Model):
    __table__ = 'users'

class Sesion(db.Model):
    __table__ = 'sesiones'

class Producto(db.Model):
    __table__ = "productos"
    __primary_key__ = "barcode"

class Venta(db.Model):
    __table__ = "ventas"
    __primary_key__ = "id_venta"

class Cliente(db.Model):
    __table__ = 'clientes'
    __primary_key__ = 'id_cliente'

class Reparacion(db.Model):
    __table__ = 'reparaciones'
    __primary_key__ = 'id_rep'

class Indice(db.Model):
    __table__='indices'
    __primary_key__='tabla'