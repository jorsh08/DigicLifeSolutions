from flask import request, jsonify, render_template
import sesiones
from datetime import datetime, timedelta
from models import db


def stats_reps():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    y = datetime.now().year
    m = datetime.now().month
    d = datetime.now().day
    today = datetime.now().date() + timedelta(1)
    reps = db.table('reparaciones').where_between('f_recibido', [f'{y}-{m - 1}-01', f'{y}-{m - 1}-31']).get()
    total = reps.count()
    days7ago = today - timedelta(7)
    days14ago = today - timedelta(14)
    last7days = db.table('reparaciones').where_between('f_recibido', [f'{days7ago}', f'{today}']).get()
    last14days = db.table('reparaciones').where_between('f_recibido', [f'{days14ago}', f'{days7ago}']).get()
    reps_actual = db.table('reparaciones').where_between('f_recibido', [f'{y}-{m}-01', f'{y}-{m}-31']).get()
    reps_enero = db.table('reparaciones').where_between('f_recibido', [f'{y}-01-01', f'{y}-01-31']).get()
    reps_febrero = db.table('reparaciones').where_between('f_recibido', [f'{y}-02-01', f'{y}-02-31']).get()
    reps_marzo = db.table('reparaciones').where_between('f_recibido', [f'{y}-03-01', f'{y}-03-31']).get()
    reps_abril = db.table('reparaciones').where_between('f_recibido', [f'{y}-04-01', f'{y}-04-31']).get()
    reps_mayo = db.table('reparaciones').where_between('f_recibido', [f'{y}-05-01', f'{y}-05-31']).get()
    reps_junio = db.table('reparaciones').where_between('f_recibido', [f'{y}-06-01', f'{y}-06-31']).get()
    reps_julio = db.table('reparaciones').where_between('f_recibido', [f'{y}-07-01', f'{y}-07-31']).get()
    reps_agosto = db.table('reparaciones').where_between('f_recibido', [f'{y}-08-01', f'{y}-08-31']).get()
    reps_septiembre = db.table('reparaciones').where_between('f_recibido', [f'{y}-09-01', f'{y}-09-31']).get()
    reps_octubre = db.table('reparaciones').where_between('f_recibido', [f'{y}-10-01', f'{y}-10-31']).get()
    reps_noviembre = db.table('reparaciones').where_between('f_recibido', [f'{y}-11-01', f'{y}-11-31']).get()
    reps_diciembre = db.table('reparaciones').where_between('f_recibido', [f'{y}-12-01', f'{y}-12-31']).get()

    total_A = reps_actual.count()
    mensual_dinero_actual = 0
    mensual_dinero_anterior = 0
    for row in reps_actual.serialize():
        try:
            mensual_dinero_actual = mensual_dinero_actual + row['total']
        except Exception as e:
            continue
    for row in reps.serialize():
        try:
            mensual_dinero_anterior = mensual_dinero_anterior + row['total']
        except Exception as e:
            continue
    semanal_dinero_actual = 0
    semanal_dinero_anterior = 0
    for row in last7days.serialize():
        try:
            semanal_dinero_actual = semanal_dinero_actual + row['total']
        except Exception as e:
            continue
    for row in last14days.serialize():
        try:
            semanal_dinero_anterior = semanal_dinero_anterior + row['total']
        except Exception as e:
            continue

    reps_enero_dinero = 0
    reps_febrero_dinero = 0
    reps_marzo_dinero = 0
    reps_abril_dinero = 0
    reps_mayo_dinero = 0
    reps_junio_dinero = 0
    reps_julio_dinero = 0
    reps_agosto_dinero = 0
    reps_septiembre_dinero = 0
    reps_octubre_dinero = 0
    reps_noviembre_dinero = 0
    reps_diciembre_dinero = 0
    for row in reps_enero.serialize():
        try:
            reps_enero_dinero = reps_enero_dinero + int(row['total'])
        except Exception:
            continue
    for row in reps_febrero.serialize():
        try:
            reps_febrero_dinero = reps_febrero_dinero + row['total']
        except Exception:
            continue
    for row in reps_marzo.serialize():
        try:
            reps_marzo_dinero = reps_marzo_dinero + row['total']
        except Exception:
            continue
    for row in reps_abril.serialize():
        try:
            reps_abril_dinero = reps_abril_dinero + int(row['total'])
        except Exception:
            continue
    for row in reps_mayo.serialize():
        try:
            reps_mayo_dinero = reps_mayo_dinero + int(row['total'])
        except Exception:
            continue
    for row in reps_junio.serialize():
        try:
            reps_junio_dinero = reps_junio_dinero + row['total']
        except Exception:
            continue
    for row in reps_julio.serialize():
        try:
            reps_julio_dinero = reps_julio_dinero + row['total']
        except Exception:
            continue
    for row in reps_agosto.serialize():
        try:
            reps_agosto_dinero = reps_agosto_dinero + row['total']
        except Exception:
            continue
    for row in reps_septiembre.serialize():
        try:
            reps_septiembre_dinero = reps_septiembre_dinero + row['total']
        except Exception:
            continue
    for row in reps_octubre.serialize():
        try:
            reps_octubre_dinero = reps_octubre_dinero + row['total']
        except Exception:
            continue
    for row in reps_noviembre.serialize():
        try:
            reps_noviembre_dinero = reps_noviembre_dinero + row['total']
        except Exception:
            continue
    for row in reps_diciembre.serialize():
        try:
            reps_diciembre_dinero = reps_diciembre_dinero + row['total']
        except Exception:
            continue
    return jsonify({"totales": {
        "mensuales": {"enero": reps_enero.count(), "febrero": reps_febrero.count(), "marzo": reps_marzo.count(),
                      "abril": reps_abril.count(), "mayo": reps_mayo.count(), "junio": reps_junio.count(),
                      "julio": reps_julio.count(), "agosto": reps_agosto.count(), "septiembre": reps_septiembre.count(),
                      "octubre": reps_octubre.count(), "noviembre": reps_noviembre.count(),
                      "diciembre": reps_diciembre.count()},

        "semanales":
            {"anterior": last14days.count(), "actual": last7days.count()}
    }, "monto": {
        "mensuales": {"enero": reps_enero_dinero, "febrero": reps_febrero_dinero, "marzo": reps_marzo_dinero,
                      "abril": reps_abril_dinero, "mayo": reps_mayo_dinero, "junio": reps_junio_dinero,
                      "julio": reps_julio_dinero, "agosto": reps_agosto_dinero, "septiembre": reps_septiembre_dinero,
                      "octubre": reps_octubre_dinero, "noviembre": reps_noviembre_dinero,
                      "diciembre": reps_diciembre_dinero},
        "semanales": {"actual": semanal_dinero_actual, "anterior": semanal_dinero_anterior}
    }
    })

def stats_ventas():
    cookies = request.cookies
    if sesiones.sesionExpirada(cookies):
        return render_template("login.html", mensaje="Sesión expirada. Inicie sesión nuevamente")
    if not sesiones.verificar_sesion(cookies):
        return render_template("login.html", mensaje="Por favor inicie sesión")
    y = datetime.now().year
    m = datetime.now().month
    d = datetime.now().day
    today = datetime.now().date() + timedelta(1)
    reps = db.table('ventas').where_between('fecha', [f'{y}-{m - 1}-01', f'{y}-{m - 1}-31']).get()
    total = reps.count()
    days7ago = today - timedelta(7)
    days14ago = today - timedelta(14)
    last7days = db.table('ventas').where_between('fecha', [f'{days7ago}', f'{today}']).get()
    last14days = db.table('ventas').where_between('fecha', [f'{days14ago}', f'{days7ago}']).get()
    reps_actual = db.table('ventas').where_between('fecha', [f'{y}-{m}-01', f'{y}-{m}-31']).get()
    reps_enero = db.table('ventas').where_between('fecha', [f'{y}-01-01', f'{y}-01-31']).get()
    reps_febrero = db.table('ventas').where_between('fecha', [f'{y}-02-01', f'{y}-02-31']).get()
    reps_marzo = db.table('ventas').where_between('fecha', [f'{y}-03-01', f'{y}-03-31']).get()
    reps_abril = db.table('ventas').where_between('fecha', [f'{y}-04-01', f'{y}-04-31']).get()
    reps_mayo = db.table('ventas').where_between('fecha', [f'{y}-05-01', f'{y}-05-31']).get()
    reps_junio = db.table('ventas').where_between('fecha', [f'{y}-06-01', f'{y}-06-31']).get()
    reps_julio = db.table('ventas').where_between('fecha', [f'{y}-07-01', f'{y}-07-31']).get()
    reps_agosto = db.table('ventas').where_between('fecha', [f'{y}-08-01', f'{y}-08-31']).get()
    reps_septiembre = db.table('ventas').where_between('fecha', [f'{y}-09-01', f'{y}-09-31']).get()
    reps_octubre = db.table('ventas').where_between('fecha', [f'{y}-10-01', f'{y}-10-31']).get()
    reps_noviembre = db.table('ventas').where_between('fecha', [f'{y}-11-01', f'{y}-11-31']).get()
    reps_diciembre = db.table('ventas').where_between('fecha', [f'{y}-12-01', f'{y}-12-31']).get()

    total_A = reps_actual.count()
    mensual_dinero_actual = 0
    mensual_dinero_anterior = 0
    for row in reps_actual.serialize():
        try:
            mensual_dinero_actual = mensual_dinero_actual + row['total']
        except Exception as e:
            continue
    for row in reps.serialize():
        try:
            mensual_dinero_anterior = mensual_dinero_anterior + row['total']
        except Exception as e:
            continue
    semanal_dinero_actual = 0
    semanal_dinero_anterior = 0
    for row in last7days.serialize():
        try:
            semanal_dinero_actual = semanal_dinero_actual + row['total']
        except Exception as e:
            continue
    for row in last14days.serialize():
        try:
            semanal_dinero_anterior = semanal_dinero_anterior + row['total']
        except Exception as e:
            continue

    reps_enero_dinero = 0
    reps_febrero_dinero = 0
    reps_marzo_dinero = 0
    reps_abril_dinero = 0
    reps_mayo_dinero = 0
    reps_junio_dinero = 0
    reps_julio_dinero = 0
    reps_agosto_dinero = 0
    reps_septiembre_dinero = 0
    reps_octubre_dinero = 0
    reps_noviembre_dinero = 0
    reps_diciembre_dinero = 0
    for row in reps_enero.serialize():
        try:
            reps_enero_dinero = reps_enero_dinero + int(row['total'])
        except Exception:
            continue
    for row in reps_febrero.serialize():
        try:
            reps_febrero_dinero = reps_febrero_dinero + row['total']
        except Exception:
            continue
    for row in reps_marzo.serialize():
        try:
            reps_marzo_dinero = reps_marzo_dinero + row['total']
        except Exception:
            continue
    for row in reps_abril.serialize():
        try:
            reps_abril_dinero = reps_abril_dinero + int(row['total'])
        except Exception:
            continue
    for row in reps_mayo.serialize():
        try:
            reps_mayo_dinero = reps_mayo_dinero + int(row['total'])
        except Exception:
            continue
    for row in reps_junio.serialize():
        try:
            reps_junio_dinero = reps_junio_dinero + row['total']
        except Exception:
            continue
    for row in reps_julio.serialize():
        try:
            reps_julio_dinero = reps_julio_dinero + row['total']
        except Exception:
            continue
    for row in reps_agosto.serialize():
        try:
            reps_agosto_dinero = reps_agosto_dinero + row['total']
        except Exception:
            continue
    for row in reps_septiembre.serialize():
        try:
            reps_septiembre_dinero = reps_septiembre_dinero + row['total']
        except Exception:
            continue
    for row in reps_octubre.serialize():
        try:
            reps_octubre_dinero = reps_octubre_dinero + row['total']
        except Exception:
            continue
    for row in reps_noviembre.serialize():
        try:
            reps_noviembre_dinero = reps_noviembre_dinero + row['total']
        except Exception:
            continue
    for row in reps_diciembre.serialize():
        try:
            reps_diciembre_dinero = reps_diciembre_dinero + row['total']
        except Exception:
            continue
    return jsonify({"totales": {
        "mensuales": {"enero": reps_enero.count(), "febrero": reps_febrero.count(), "marzo": reps_marzo.count(),
                      "abril": reps_abril.count(), "mayo": reps_mayo.count(), "junio": reps_junio.count(),
                      "julio": reps_julio.count(), "agosto": reps_agosto.count(), "septiembre": reps_septiembre.count(),
                      "octubre": reps_octubre.count(), "noviembre": reps_noviembre.count(),
                      "diciembre": reps_diciembre.count()},

        "semanales":
            {"anterior": last14days.count(), "actual": last7days.count()}
    }, "monto": {
        "mensuales": {"enero": reps_enero_dinero, "febrero": reps_febrero_dinero, "marzo": reps_marzo_dinero,
                      "abril": reps_abril_dinero, "mayo": reps_mayo_dinero, "junio": reps_junio_dinero,
                      "julio": reps_julio_dinero, "agosto": reps_agosto_dinero, "septiembre": reps_septiembre_dinero,
                      "octubre": reps_octubre_dinero, "noviembre": reps_noviembre_dinero,
                      "diciembre": reps_diciembre_dinero},
        "semanales": {"actual": semanal_dinero_actual, "anterior": semanal_dinero_anterior}
    }
    })