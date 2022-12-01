const formulario = document.getElementById('formulario-refaccion');
const inputs = document.querySelectorAll('#formulario-refaccion input');
const aceptar = document.getElementById('aceptar');
var nombre = false;
var baarcode = false;
var costo = false;
var precio = false;
var proveedor = false;
var descripcion = false;

var js;

monstrasJSON();s
async function monstrasJSON() {
    var respuesta = await fetch("/json-refacciones");
    var json = await respuesta.text();
    js = JSON.parse(json);
}

habilitar(nombre, baarcode, costo, precio, proveedor, descripcion);

const expresiones = {
    nombre: /^[a-zA-ZÀ-ÿ\s\S]{3,40}$/,
    barcode: /^[a-zA-Z0-9]{5,10}$/,
    costo: /^[0-9]{1,5}$/,
    precio: /^[0-9]{1,6}$/,
    celular: /^.{10,10}$/,
    correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
    descripcion: /^.{3,500}$/,
}

const validarFormulario = (e) => {
    switch (e.target.name) {
        case "nombre":
            if (expresiones.nombre.test(e.target.value)) {
                document.getElementById('grupo-nombre').classList.remove('formulario-grupo-incorrecto');
                nombre = true;
                habilitar(nombre, baarcode, costo, precio, proveedor, descripcion);
            } else {
                document.getElementById('grupo-nombre').classList.add('formulario-grupo-incorrecto');
                nombre = false;
                habilitar(nombre, baarcode, costo, precio, proveedor, descripcion);
            }
            break;
        case "barcode":
            if (expresiones.barcode.test(e.target.value)) {
                document.getElementById('grupo-barcode').classList.remove('formulario-grupo-incorrecto');
                baarcode = true;
                habilitar(nombre, baarcode, costo, precio, proveedor, descripcion);
            } else {
                document.getElementById('grupo-barcode').classList.add('formulario-grupo-incorrecto');
                baarcode = false
                habilitar(nombre, baarcode, costo, precio, proveedor, descripcion);
            }
            break;
        case "costo":
            if (expresiones.costo.test(e.target.value)) {
                document.getElementById('grupo-costo').classList.remove('formulario-grupo-incorrecto');
                costo = true;
                habilitar(nombre, baarcode, costo, precio, proveedor, descripcion);
            } else {
                document.getElementById('grupo-costo').classList.add('formulario-grupo-incorrecto');
                costo = false;
                habilitar(nombre, baarcode, costo, precio, proveedor, descripcion);
            }
            break;
        case "precio":
                if (expresiones.precio.test(e.target.value)) {
                    document.getElementById('grupo-precio').classList.remove('formulario-grupo-incorrecto');
                    precio = true;
                    habilitar(nombre, baarcode, costo, precio, proveedor, descripcion);           
                } else {
                    document.getElementById('grupo-precio').classList.add('formulario-grupo-incorrecto');
                    precio = false;
                    habilitar(nombre, baarcode, costo, precio, proveedor, descripcion);
                }
            break;
        case "proveedor":
                if (expresiones.nombre.test(e.target.value)) {
                    document.getElementById('grupo-proveedor').classList.remove('formulario-grupo-incorrecto');
                    proveedor = true;
                    habilitar(nombre, baarcode, costo, precio, proveedor, descripcion);           
                } else {
                    document.getElementById('grupo-proveedor').classList.add('formulario-grupo-incorrecto');
                    proveedor = false;
                    habilitar(nombre, baarcode, costo, precio, proveedor, descripcion);
                }
            break;
        case "descripcion":
                if (expresiones.descripcion.test(e.target.value)) {
                    document.getElementById('grupo-descripcion').classList.remove('formulario-grupo-incorrecto');
                    descripcion = true;
                    habilitar(nombre, baarcode, costo, precio, proveedor, descripcion);           
                } else {
                    document.getElementById('grupo-descripcion').classList.add('formulario-grupo-incorrecto');
                    descripcion = false;
                    habilitar(nombre, baarcode, costo, precio, proveedor, descripcion);
                }
            break;
    }
    
}



function habilitar(nombre, baarcode, costo, precio, proveedor, descripcion){
    if (nombre && baarcode&& costo&& precio && proveedor && descripcion){
        aceptar.disabled = false;
        aceptar.style.opacity = 1;
    }else{
        aceptar.disabled = true;
        aceptar.style.opacity = 0.5;
    }
}

inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormulario);
    input.addEventListener('blur', validarFormulario);
    
});
