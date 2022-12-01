import json
import os
import time

import clientes, estadisticas
from flask import Flask, request, make_response, redirect, render_template, send_from_directory
from flask_orator import Orator, jsonify
from reparaciones import new_rep, submit_ENDED_rep, submit_ticket, pending, finalizar_reparacion, eliminar_rep
from models import Reparacion, Cliente, Producto, Venta, Indice
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import sesiones

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
app.config['UPLOAD_FOLDER'] = './files'
db = Orator(app)

DEBUG = True

config = {
    'mysql': {
        'driver': 'mysql',
        'host': 'us-cdbr-east-05.cleardb.net',
        'database': 'heroku_2a75a8daff3ffa6',
        'user': 'b4d5cceb281dab',
        'password': 'a5eda933',
        'prefix': ''
    }
}




@app.route('/img/<filename>', methods=['GET'])
def route_img_files(filename):
    return send_from_directory('templates/img', path=filename)


@app.route('/css/<filename>')
def route_js_files(filename):
    return send_from_directory('templates/css', path=filename)

@app.route('/js/<filename>')
def route_css_files(filename):
    return send_from_directory('templates/js', path=filename)

@app.route('/pi/<filename>')
def route_pi_files(filename):
    try:
        filename = filename+".jpg"
        return send_from_directory('files', path=filename)
    except Exception as e:
        filename = filename+".png"
        return send_from_directory('files', path=filename)



@app.route('/principal-reparaciones')
def principal_reps():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return render_template('principal-reparaciones.html')

@app.route('/reparaciones-pendientes')
def rep_pending():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return pending()

@app.route('/json-entregables')
def entress():
    reps = db.table('reparaciones').where('recogido', None).where("terminado",True).get().serialize()

    return jsonify(reps)


@app.route('/entregables')
def entre():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return render_template('entregables.html')

@app.route('/json-pendientes')
def pendiet():
    reps = db.table('reparaciones').where('f_terminado', None).get().serialize()
    return jsonify(reps)

@app.route('/entregar_rep')
def enrea():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    id_rep = request.args['id_rep']
    rep = Reparacion.find(id_rep)
    rep.recogido = True
    rep.f_entregado = datetime.now()
    rep.update()
    return make_response(redirect(f'/ticket-reparacion-terminada?id={id_rep}'))


@app.route('/submit_rep',methods=['POST'])
def submit_init_rep():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return submit_ticket()

@app.route('/eliminar_venta')
def eliminarventa():
    id_venta = int(request.args['id'])
    v = Venta.find(id_venta)
    v.delete()
    return make_response(redirect('/principal-venta'))

@app.route('/submit_refaccionE', methods=['POST'])
def editarreaf():
    print(request.form)
    form = request.form
    id_r = form['barcode']
    re = Producto.find(id_r)
    re.barcode = form['barcode']
    re.nombre = form['nombre']
    re.desc = form['descripcion']
    try:
        re.costo = int(form['costo'])
    except Exception:
        print("Fallo en el costo")
    try:
        re.precio = int(form['precio'])
    except Exception:
        print("Fallo en el precio")
    re.prov = form['proveedor']
    re.update()
    try:
        f = request.files['archivo']
        filename = form['barcode']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename + f.filename[-4:]))

    except Exception:
        print("No hubo cambios en la imágen")
    return render_template("mensajes.html",data={"mensaje":"Refacción editada exitosamente","aceptar":"/principal-refacciones",

                                              "/regresar":"/principal-refacciones"})

@app.route('/eliminar_refaccion')
def elasf():
    barcode = request.args['barcode']
    re = Producto.find(barcode)
    re.delete()
    return render_template("mensajes.html",data={"mensaje": "Refaccion eliminada con éxito","aceptar":"/principal-refacciones",
                                                 "regresar":"/principal-refacciones"})

@app.route('/editar_refaccion')
def asasaf():
    id_r = request.args['barcode']
    re = Producto.find(id_r).serialize()
    return render_template("registrar-refaccion1.html",data = re)



@app.route('/finalizar_rep/')
def end_rep():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return finalizar_reparacion()

@app.route('/eliminar_rep')
def deleterep():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    id_rep = request.args['id_rep']
    data = {}
    data['mensaje'] = f'¿Estás seguro que deseas eliminar la reparación número {id_rep}?'
    data['color'] = "rojo"
    data['aceptar'] = f'/eliminar_rep_true?id_rep={id_rep}'
    data['regresar'] = "/principal-reparaciones"
    return render_template('mensajes.html',data=data)

@app.route('/graficas-reparaciones')
def grafira():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return render_template('graficas-reparaciones.html')

@app.route('/json-stats')
def jsonstats():
    return estadisticas.stats_reps()


@app.route('/eliminar_rep_true')
def delrep():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return eliminar_rep()

@app.route('/registrar-reparacion')
def nueva_rep():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return new_rep()


#   CLIENTES   #


@app.route('/registrar-cliente')
def reg_cliente():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return render_template('registrar-cliente.html')

@app.route('/submit_cliente', methods=['POST'])
def submit_cliente():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return clientes.submit_cliente()

@app.route('/clientes/listado')
def mostar_clientes():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return jsonify(db.table('clientes').get())


@app.route('/finalizar_rep/finalizar', methods=['POST'])
def submit1_rep():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return submit_ENDED_rep()

@app.route('/json-entregadas')
def erntreas():
    repas = db.table('reparaciones').where('recogido', 1).get().serialize()
    return jsonify(repas)

@app.route('/estadisticas-reparacion')
def rep_stats():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    repas = db.table('reparaciones').where('recogido',1).get().serialize()
    w=0
    for rep in repas:
        recibido = rep['f_entregado']
        repas[w]['f_entregado'] = recibido[:-9]
        w=w+1
    stats = {}
    stats['totales'] = db.table('reparaciones').count()
    stats['pendientes'] = db.table('reparaciones').where('f_terminado',None).count()
    stats['entregadas'] = db.table('reparaciones').where('recogido',1).count()
    stats['finalizadas'] = db.table('reparaciones').where('terminado',1).count()
    return render_template('estadisticas-reparacion.html',repas = repas, stats = stats)

@app.route('/principal-venta')
def rep_statRDFs():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return render_template('principal-venta.html')

@app.route('/clientes')
def clients():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    clientes = db.table('clientes').get().serialize()
    return render_template('clientes.html', clientes = clientes)

@app.route('/modificar_cliente')
def modclie():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    id_cliente = request.args['id_cliente']
    cliente = Cliente.find(id_cliente).serialize()
    return render_template('registrar-cliente1.html',cliente=cliente)

@app.route('/eliminar_cliente')
def deleteclie():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    id_cliente = request.args['id_cliente']
    data = {}
    data['color'] = "rojo"
    data['mensaje'] = f'¿Estás seguro que quieres eliminar al cliente {id_cliente}?'
    data['aceptar'] = f'/del_cli?id_cliente={id_cliente}'
    data['regresar'] = "/clientes"
    return render_template('mensajes.html',data=data)

@app.route('/del_cli')
def delcli():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    id_cliente = request.args['id_cliente']
    cli = Cliente.find(id_cliente)
    cli.delete()
    data={}
    data['mensaje'] = "Cliente eliminado con éxito"
    data['color'] = "verde"
    data['aceptar'] = "/clientes"
    data['regresar'] = "/clientes"
    return render_template('mensajes.html',data=data)

@app.route('/modificar_client',methods=['POST'])
def modcliet():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return clientes.edit_cliente()


@app.route('/registrar-ventas')
def regventas1():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return render_template('Registrar-ventas.html')

@app.route('/principal-refacciones')
def prirefas():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return render_template('/Principal-refacciones.html')

@app.route('/estadisticas-ventas')
def statsventas():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    stats = Venta.get().serialize()

    return render_template('estadisticas-ventas.html',stats=stats)

@app.route('/registrar-refaccion')
def submitrep1():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return render_template('registrar-refaccion.html')

@app.route('/submit_refa', methods=['POST'])
def sub_refa():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    form = request.form
    f = request.files['archivo']
    filename = form['barcode']
    pro = Producto.find(form['barcode'])
    if pro is not None:
        return render_template("mensajes.html",data={"mensaje":"El código de barras ya existe, utilice otro",
                                                     "color":"rojo","aceptar":"/registrar-refaccion",
                                                     "regresar":"/principal-refacciones"})
    p = Producto()
    print(f.filename[-4:])
    p.barcode = form['barcode']
    p.nombre = form['nombre']
    p.costo = int(form['costo'])
    p.precio = int(form['precio'])
    p.prov = form['proveedor']
    p.cantidad = 0
    p.desc = form['descripcion']
    p.created_at = datetime.now()
    p.save()
    #MODIFICAR_AQUÍ
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename+f.filename[-4:]))
    data = {"mensaje": "Guardado con éxito","color":"verde","aceptar":"/principal-venta","regresar":"/principal-venta"}
    return render_template("mensajes.html",data=data)

@app.route('/refacciones')
def refas1():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    refas= Producto.get().serialize()
    return render_template('Refacciones.html',repas=refas)

@app.route('/principal-clientes')
def costumers():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return render_template('Principal-clientes.html')

@app.route('/registrar-clientes')
def newclie():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return render_template('Registrar-clientes.html')



#Login listo
@app.route('/login', methods=['POST'])
def login():
    return sesiones.login()

#Logout listo
@app.route('/logout')
def logout():
    cookies = request.cookies
    cookies = cookies.to_dict()
    try:
        db.table('sesiones').where('rcode', cookies['r']).update(active=False)
    except Exception as e:
        print("No se pudo actualizar el registro, se borrarán las cookies de todas formas")

    resp = make_response(redirect("/"))
    try:
        resp.delete_cookie("user")
    except:
        pass
    try:
        resp.delete_cookie("acceso")
    except:
        pass
    try:
        resp.delete_cookie("up")
    except:
        pass
    try:
        resp.delete_cookie("user-id")
    except:
        pass
    try:
        resp.delete_cookie("user-name")
    except:
        pass
    try:
        resp.delete_cookie("r")
    except:
        pass
    try:
        resp.delete_cookie("u")
    except:
        pass
    return resp


#Ya jalan las sesiones aquí
@app.route('/')
def index():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html")

    return render_template('principal.html')


#Ya jalan las sesiones aquí
@app.route('/principal')
@app.route('/dashboard')
def dashboard():
    cookies = request.cookies
    cookies = cookies.to_dict()
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html",mensaje="Sesión expirada. Inicie sesión nuevamente")
    if sesiones.verificar_sesion(cookies):
        try:
            data = {"user-id": cookies['user-id'], "nombres": cookies['user-name'], "up": cookies['up'],
                "acceso": cookies['acceso'], "username": cookies['user']}
            user = db.table('users').where('user', data['username']).first()
            if user is not None:
                return render_template('principal.html', data=data)
        except:
            return make_response(redirect("/logout"))
    return make_response(redirect("/logout"))


#ya jalan las sesiones
@app.route('/ventas')
def ventas():
    cookies = request.cookies
    cookies = cookies.to_dict()
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html",mensaje="Sesión expirada. Inicie sesión nuevamente")
    if sesiones.verificar_sesion(cookies):
        try:
            data = {"user-id": cookies['user-id'], "nombres": cookies['user-name'], "up": cookies['up'],
                    "acceso": cookies['acceso'], "username": cookies['user']}
            return render_template('ventas.html', data=data)
        except:
            return make_response(redirect("/logout"))
    return make_response(redirect("/"))


@app.route('/json-refacciones')
def gerrefas():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return jsonify(Producto.get().serialize())

@app.route('/json-reparaciones')
def gerrefss():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return jsonify(Reparacion.get().serialize())

@app.route('/json-clientes')
def clieee():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return jsonify(Cliente.get().serialize())

@app.route('/json-ventas')
def jsonventas():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    return jsonify(Venta.get().serialize())

@app.route('/json-stats-ventas')
def staventas():
    return estadisticas.stats_ventas()


#ya jalan las sesones
@app.route('/registrar-venta')
def regventas():
    cookies = request.cookies
    cookies = cookies.to_dict()
    if sesiones.sesionExpirada(cookies):
        return render_template('login.html',mensaje="Sesión expirada, inicie sesión de nuevo")
    if sesiones.verificar_sesion(cookies):
        try:
            refas = Producto.get().serialize()
            data = {"user-id": cookies['user-id'], "nombres": cookies['user-name'], "up": cookies['up'],
                    "acceso": cookies['acceso'], "username": cookies['user']}
            return render_template('registrar-venta.html', data=data,refas=refas)
        except:
            return make_response(redirect("/logout"))




    return make_response(redirect("/logout"))

@app.route('/modificar_refa', methods=['POST'])
def modifirefa1():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html",mensaje="Sesión expirada. Inicie sesión nuevamente")
    f = request.form
    barcode = f['id']
    c_act = int(f['actual'])
    c_new = int(f['nueva'])
    data = {}
    if c_new < c_act:
        data['mensaje'] = f'La cantidad introducida es menor a la actual.\n'\
                          f'Cantidad actual: {c_act}.\n' \
                          f'Cantidad introducida: {c_new} \n ¿desea continuar?'
        data['color'] = "rojo"
    else:
        data['mensaje'] = f'Está actualizando la cantidad a {c_new}. ¿desea continuar?'
        data['colot'] = "verde"
    data['regresar'] = "/refacciones"
    data['aceptar'] = f'/submit_inv?id={barcode}&cant={c_new}'
    return render_template("mensajes.html",data=data)

@app.route("/submit_inv")
def actinv():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    id = request.args['id']
    ca = request.args['cant']
    e = Producto.find(id)
    e.cantidad = ca
    try:
        e.update()
        data = {}
        data['mensaje'] = "Inventario actualizado con éxito"
        data['color'] = "verde"
        data['aceptar'] = "/refacciones"
        data['regresar'] = "/refacciones"
        return render_template("mensajes.html", data=data)
    except Exception as e:
        data['mensaje'] = f'Hubo un error en el sistema.' \
                          f'Detalles: {str(e)}'
        data['color'] = "rojo"
        data['aceptar'] = "/refacciones"
        data['regresar'] = "/refacciones"
        return render_template("mensajes.html",data=data)


@app.route('/submit_venta',methods=['POST'])
def submitventa():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    r = request.json
    total = 0
    print(r)
    for articulo in r[0]['Refaccion']:
        a = Producto.find(articulo['barcode'])
        total = total + a.precio * int(articulo['cantidad'])
        a.cantidad = a.cantidad-int(articulo['cantidad'])
        a.update()
    v = Venta()
    i = Indice.find("ventas")
    v.id_venta = id_venta = i.n_actual+1
    i.n_actual = i.n_actual+1

    v.id_cliente = int(r[0]['Cliente'])
    v.articulos = str(r[0]['Refaccion'])
    v.total = total
    v.fecha = datetime.now()
    v.u = Cliente.find(int(r[0]['Cliente'])).t_cliente

    v.save() #Registra venta en base de datos
    i.update() #Actualiza el indice (folio actual de venta)
    response = make_response(redirect("/venta?id=" + str(id_venta)))
    return response



@app.route("/venta")
def comprobanteVenta():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")

    try:
        id_venta = request.args['id']
    except Exception as e:
        return("Haz hecho algo mal...")
    try:
        v = Venta.find(id_venta).serialize()
    except AttributeError:
        return ("Venta no encontrada"),404
    except Exception as e:
        return ("Hubo un error. Detalles: " + str(e))
    try:
        c = Cliente.find(v['id_cliente'])
    except Exception as e:
        c = {"nombre":"Sin datos","Celular":"Sin datos","email":"Sin datos"}
    articulos = eval(v['articulos'])
    print(articulos)
    nombres = {}
    conta = 0
    for art in articulos:
        nombres[conta] = Producto.find(str(art['barcode'])).nombre
        print(nombres[conta])
        conta = conta+1
    print(nombres)
    return render_template("ticket-venta.html",v=v,articulos=articulos,c=c, n=nombres)

@app.route("/ultimaVenta")
def comprobanteVenta1():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    time.sleep(2)
    id_venta = Indice.find("ventas").n_actual
    r = make_response(redirect(f'/venta?id={id_venta}'))
    return r

@app.route('/ticket_reparacion')
def tickeVenta():
    id_r = request.args['id']
    r = Reparacion.find(id_r).serialize()
    try:
        c = Cliente.find(r['id_cliente']).serialize()
    except Exception:
        c = {"email":"SIN DATOS"}
    print(r)
    print(c)
    return render_template("ticket-reparacion.html",r = r, c=c)

@app.route('/graficas-ventas')
def graventas():
    return render_template("graficas-ventas.html")

@app.route('/ticket-reparacion-terminada')
def reafwa():
    id = request.args['id']
    try:
        r = Reparacion.find(int(id)).serialize()
    except Exception:
        return ('Reparación no encontrada'),404
    try:
        c = Cliente.find(int(r['id_cliente']))
    except Exception:
        print("CLIENTE NO ENCONTRADO")
        c = {}
    return render_template('ticket-entrega-reparacion.html',r=r,c=c)


#ya jalan las sesiones
@app.route('/reparaciones')
def reparaciones():
    cookies = request.cookies
    cookies = cookies.to_dict()
    if sesiones.sesionExpirada(cookies):
        return render_template('login.html',mensaje="Sesión Expirada. Inicie sesión nuevamente")
    if sesiones.verificar_sesion(cookies):
        try:
            data = {"user-id": cookies['user-id'], "nombres": cookies['user-name'], "up": cookies['up'],
                    "acceso": cookies['acceso'], "username": cookies['user']}
            return make_response(f"Aún en construcción {data}",404)
            #return render_template('reparaciones.html', data=data)
        except:
            return make_response(redirect("/logout"))
    return make_response(redirect("/logout"))



@app.route('/users')
def retusers():
    return jsonify(db.table('users').select('id', 'nombres', 'puesto').get())


if __name__ == '__main__':
    app.run()
