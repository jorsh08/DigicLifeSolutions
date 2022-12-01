from flask import Flask, request, jsonify, json, render_template
from models import Reparacion, Cliente, db
from datetime import datetime


#Regresa el HTML para registrar una reparación
def new_rep():
    clientes = db.table('clientes').get().serialize()
    return render_template('registrar-reparacion.html',data=clientes)

#REGISTRA LA reparación en BD
def submit_ticket():
    form = request.form
    nueva_rep = Reparacion()
    print(form)
    cantidad_reps = db.table('reparaciones').count()
    id = cantidad_reps+1
    nueva_rep.id_rep = id
    nueva_rep.id_cliente = form['select']
    cli = Cliente.find(int(form['select'])).serialize()
    nueva_rep.u = cli['t_cliente']
    nueva_rep.desc_rep = form['descripcion']
    nueva_rep.dispositivo = form['dispositivo']
    nueva_rep.cotizacion = int(form['cotizacion'])
    nueva_rep.f_recibido = datetime.now()
    try:
        nueva_rep.save()
        return jsonify({"status":"OK",'id':id})
    except Exception as e:
        return jsonify({"status":"FAIL","msg":str(e)})

#muestra reparaciones pendientes
def pending():
    reps = db.table('reparaciones').where('f_terminado',None).get()
    data =reps.to_json()
    aDict = json.loads(data)
    w =0
    for rep1 in aDict:
        nombre = db.table('clientes').where('id_cliente', rep1['id_cliente']).first()
        recibido = str(rep1['f_recibido'])
        recep = recibido[:-9]
        aDict[w]['f_recibido'] = recep
        aDict[w]['nombre'] = nombre.nombres
        #aDict[w]['u'] = nombre.t_cliente
        w = w+1
    return render_template('reparaciones-pendientes.html',data=aDict)

#muestra el html para finalizar reparación
def finalizar_reparacion():
    id_rep = request.args['id_rep']
    repa = db.table('reparaciones').where('id_rep',id_rep).first()
    data = {}
    data['id_rep'] = id_rep
    data['articulo'] = repa.dispositivo
    data['cotizacion'] = repa.cotizacion
    data['descripcion'] = repa.desc_rep
    return render_template('finalizar-reparacion.html',data=data)


#cierra la rep, regisistra terminado en BD
def submit_ENDED_rep():
    try:
        print(request.form)
        id_rep = int(request.form['id_rep'])
        repa = Reparacion.find(id_rep)
        if repa is None:
            return jsonify({"alert": "La reparación no existe, intente de nuevo","status":"FAIL"})
        repa.observaciones = request.form['observaciones']
        repa.total = request.form['importe']
        repa.f_terminado = datetime.now()
        repa.terminado = True
        repa.update()
    except Exception as e:
        return jsonify({"status":"FAIL","msg":str(e)})
    return render_template('ventas.html')