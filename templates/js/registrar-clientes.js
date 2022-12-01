const formulario = document.getElementById('contenido-prinicipal-clientes');
const inputs = document.querySelectorAll('#contenido-prinicipal-clientes input');
const aceptar = document.getElementById('aceptar');
var nombre = false;
var apellido = false;
var celular = false;
var correo = false;



const expresiones = {
    nombre: /^[a-zA-ZÀ-ÿ\s\S]{3,40}$/,
    contraseña: /^.{4,12}$/,
    celular: /^[0-9]{10,10}$/,
    correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
}

const validarFormulario = (e) => {
    switch (e.target.name) {
        case "nombres":
            if (expresiones.nombre.test(e.target.value)) {
                document.getElementById('grupo-nombre').classList.remove('formulario-grupo-incorrecto');
                nombre = true;
                habilitar(nombre, apellido, celular, correo);
            } else {
                document.getElementById('grupo-nombre').classList.add('formulario-grupo-incorrecto');
                nombre = false;
                habilitar(nombre, apellido, celular, correo);
            }
            break;
        case "apellidos":
            if (expresiones.nombre.test(e.target.value)) {
                document.getElementById('grupo-apellido').classList.remove('formulario-grupo-incorrecto');
                apellido = true;
                habilitar(nombre, apellido, celular, correo);
            } else {
                document.getElementById('grupo-apellido').classList.add('formulario-grupo-incorrecto');
                apellido = false
                habilitar(nombre, apellido, celular, correo);
            }
            break;
        case "celular":
            if (expresiones.celular.test(e.target.value)) {
                document.getElementById('grupo-celular').classList.remove('formulario-grupo-incorrecto');
                celular = true;
                habilitar(nombre, apellido, celular, correo);
            } else {
                document.getElementById('grupo-celular').classList.add('formulario-grupo-incorrecto');
                celular = false;
                habilitar(nombre, apellido, celular, correo);
            }
            break;
        case "email":
            if (expresiones.correo.test(e.target.value)) {
                document.getElementById('grupo-correo').classList.remove('formulario-grupo-incorrecto');
                correo = true;
                habilitar(nombre, apellido, celular, correo);                
            } else {
                document.getElementById('grupo-correo').classList.add('formulario-grupo-incorrecto');
                correo = false;
                habilitar(nombre, apellido, celular, correo);
            }
            break;
    }
}


function habilitar(nombre, apellido, celular, correo){
    if (nombre && apellido && celular && correo){
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
