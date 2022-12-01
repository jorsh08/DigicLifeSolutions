from flask import Flask, request, jsonify, json, render_template, make_response, redirect
from models import Reparacion, Cliente, db, Indice
from datetime import datetime


#Regresa el HTML para registrar una reparación
def new_rep():
    clientes = db.table('clientes').get().serialize()
    return render_template('registrar-reparacion.html',data=clientes)



#REGISTRA LA reparación en BD
def submit_ticket():
    form = request.form
    nueva_rep = Reparacion()
    id_rep = Indice.find("reparaciones")
    id_rep.n_actual = id_rep.n_actual + 1
    id = id_rep.n_actual
    id_rep.save()
    nueva_rep.id_rep = id
    nueva_rep.id_cliente = form['cliente']
    cli = Cliente.find(int(form['cliente'])).serialize()
    nueva_rep.u = cli['t_cliente']
    try:
        nueva_rep.cel_cliente = cli['celular']
    except Exception:
        nueva_rep.cel_cliente = 0
    nueva_rep.desc_rep = form['descripcion']
    nueva_rep.dispositivo = form['dispositivo']
    nueva_rep.cotizacion = int(form['cotizacion'])
    nueva_rep.f_recibido = datetime.now()
    nueva_rep.nombre_cliente = cli['nombres']
    nueva_rep.activo = True
    try:
        nueva_rep.save()
        data = {}
        data['status'] = "Registrado con éxito"
        mens = f'La reparación se registró exitosamente con el ID: {id}'
        data['mensaje'] = mens
        data['color'] = 'verde'
        data['regresar'] = "/principal-reparaciones"
        data['aceptar'] = "/principal-reparaciones"
        return make_response(redirect(f'/ticket_reparacion?id={id}'))

    except Exception as e:
        return jsonify({"status":"FAIL","msg":str(e)})




#muestra reparaciones pendientes
def pending():
    return render_template('reparaciones-pendientes.html')



def eliminar_rep():
    id_rep = request.args['id_rep']
    rep = Reparacion.find(id_rep)
    rep.activo = False
    rep.delete()
    data ={}
    data['mensaje'] = "La reparación se eliminó exitosamente"
    data['regresar'] = "/principal-reparaciones"
    data['aceptar'] = "/principal-reparaciones"
    data['color'] = "verde"
    return render_template('mensajes.html',data=data)



#muestra el html para finalizar reparación
def finalizar_reparacion():
    id_rep = request.args['id_rep']
    repa = db.table('reparaciones').where('id_rep',id_rep).first()
    data = {}
    data['id_rep'] = id_rep
    data['articulo'] = repa.dispositivo
    data['cotizacion'] = repa.cotizacion
    data['descripcion'] = repa.desc_rep
    if repa.observaciones is not None:
        data['observaciones']= repa.observaciones
    else:
        data['observaciones'] = ""
    return render_template('finalizar-reparacion.html',data=data)


#cierra la rep, regisistra terminado en BD
def submit_ENDED_rep():
    try:
        print(request.form)
        id_rep = int(request.form['id_rep'])
        repa = Reparacion.find(id_rep)
        if repa is None:
            data= {}
            data['status'] = 'Hubo un error'
            data['mensaje'] = 'No se encontró una reparación con ese ID, intenta de nuevo'
            data['aceptar'] = '/principal-reparaciones'
            data['regresar'] = '/principal-reparaciones'
            data['color'] = 'rojo'
            data['icon'] = "FAIL"
            return render_template('mensajes.html',data=data)
        repa.observaciones = request.form['observaciones']
        repa.total = request.form['importe']
        repa.f_terminado = datetime.now()
        repa.terminado = True
        repa.update()

    except Exception as e:
        data = {}
        data['status'] = 'Hubo un error'
        data['mensaje'] = "La reparación no se pudo registrar, si el problema consiste, " \
                          'contacte a soporte técnico con el código de error ', str(e), " para solucionar el problema"
        data['aceptar'] = '/principal-reparaciones'
        data['regresar'] = '/principal-reparaciones'
        data['color'] = 'rojo'
        data['icon'] = "FAIL"
    data = {}
    data['status'] = 'Guardada con éxito'
    data['mensaje'] = 'La reparación se registró exitosamente'
    data['aceptar'] = '/principal-reparaciones'
    link = f'/finalizar_rep/?id_rep={id_rep}'
    data['regresar'] = link
    data['color'] = 'verde'
    data['icon'] = "OK"
    return render_template('mensajes.html',data=data)
