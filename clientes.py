from flask import Flask, request, jsonify, render_template
from models import Cliente, db, Indice
from datetime import datetime

def submit_cliente():
    form = request.form
    cli = Cliente()

    id_cliente = Indice.find("clientes")
    id_cliente.n_actual = id_cliente.n_actual+1
    cli.id_cliente = id_cliente.n_actual
    id_cliente.save()
    print(id_cliente.n_actual)
    cli.nombres = form['nombres']
    cli.apellidos = form['apellidos']
    cli.celular = int(form['celular'])
    cli.email = form['email']
    cli.t_cliente = form['tipo']
    cli.u_visita = datetime.now()
    print("pasando a promociones")
    try:
        form['promociones']
        cli.pub = True
    except Exception:
        cli.pub = False
        print("pasando a guardar")
    cli.save()
    print("guardado")
    data = {}
    data['mensaje'] = "Cliente guardado con éxito"
    data['color'] = "verde"
    data['aceptar'] = "/clientes"
    return render_template('mensajes.html',data=data)


def edit_cliente():
    form = request.form
    print(form)
    cli = Cliente.find(int(form['id_cliente']))
    print("lo encontró")
    cli.nombres = form['nombres']
    cli.apellidos = form['apellidos']
    cli.celular = int(form['celular'])
    cli.email = form['email']
    cli.t_cliente = form['tipo']
    try:
        form['promociones']
        cli.pub = True
    except Exception:
        cli.pub = False
    print("aun no guarda")
    cli.update()
    data = {}
    data['mensaje'] = "Cliente editado con éxito"
    data['color'] = "verde"
    data['aceptar'] = "/clientes"
    return render_template('mensajes.html', data=data)