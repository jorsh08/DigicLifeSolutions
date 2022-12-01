from flask import request, jsonify, make_response, redirect, render_template
import hashlib, random, string
from models import Sesion, db
from datetime import datetime, timedelta



def login():
    try:
        s_user = request.form.get('user')
        s_password = request.form.get('password')
        headers = request.headers
        user = db.table('users').where('user', s_user).first()
        if user is None:
            data={}
            data['status'] = "Usuario no encontrado"
            data['mensaje'] = "Oops! no encontramos tu usuario, prueba de nuevo"
            data['color'] = 'rojo'
            data['regresar'] = "/"
            data['aceptar'] = "/"
            return render_template('mensajes.html',data=data)
        pss1 = hashlib.sha256(s_password.encode("utf-8")).hexdigest()
        if user.password == pss1:
            user1 = {"id": user.id,
                     "nombres": user.nombres,
                     "apellidos": user.apellidos,
                     "puesto": user.puesto,
                     "acceso": user.access}
            resp = make_response(redirect('/dashboard'))
            resp.set_cookie("user-id", str(user.id), max_age=7200)
            resp.set_cookie("user-name", str(user.nombres), max_age=7200)
            resp.set_cookie("up", str(user.password), max_age=7200)
            resp.set_cookie("acceso", str(user.access), max_age=7200)
            resp.set_cookie("user", str(user.user), max_age=7200)
            ucode = (''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64)))
            rcode = (''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(64)))
            resp.set_cookie("u", ucode, max_age=7200)
            resp.set_cookie("r", rcode, max_age=7200)
            # debug
            print('SE GENERARON Y ENTREGARON COOKIES')
            sesion = Sesion()
            sesion.userid = user.id
            sesion.up = user.password
            sesion.rcode = rcode
            sesion.ucode = ucode
            sesion.active = True
            try:
                sesion.os = headers['sec-ch-ua-platform']
            except Exception as e:
                print(str(e))
            sesion.expires = datetime.now() + timedelta(seconds=7200)
            sesion.save()
            # DEBUG
            print('SE GENERÓ Y GUARDÓ LA SESIÓN')
            print('Redirecting to Dashboard...')
            return resp
        data = {}
        data['status'] = "Contraseña incorrecta"
        data['mensaje'] = "Oops! Parece que esa no es tu contraseña, intentalo de nuevo"
        data['color'] = 'rojo'
        data['regresar'] = "/"
        data['aceptar'] = "/"
        return render_template('mensajes.html',data=data)
    except Exception as e:
        return str(e)



def sesionExpirada(cookie):
    #debug
    print("Verificando expiración de sesión")
    try:
        sesion = db.table('sesiones').where('rcode', cookie['r']).first()
        if sesion.expires < datetime.now():
            db.table('sesiones').where('rcode', cookie['r']).update(active=False)
            print("Regresa True, sesión expirada")
            return True
        else:
            #debug
            print("La sesión no ha expirado")
            return False
    except Exception as e:
        print("O no hay cookies o no se encontró sesión en BD")
        return False

def verificar_sesion(cookie):
    try:
        sesion = db.table('sesiones').where('rcode', cookie['r']).first()
        #debug
        print('Se encontró una sesión')
        if sesion.active:
            #debug
            print('sesión ACTIVA')
            print('verificando si aún está activa...')
            print(f'sesisón caduca= {sesion.expires}')
            print(f'tiempo actual = {datetime.now()}')
            print(f'comparación = {sesion.expires < datetime.now()}')
            if sesion.expires < datetime.now():
                sesion.active = False;
                db.table('sesiones').where('rcode', cookie['r']).update(active=False)
                #debug
                print('Sesión caducada, registrar FALSE EN db')
                return False
        else:
            #debug
            print('Sesión inactiva')
            return False
    except Exception as e:
        print(f'expeption: {e}')
        #debug
        print('No hay cookies, iniciando login')
        return False
    #DEBUG
    print(f'sesion activa?: {sesion.active}')
    return sesion.active