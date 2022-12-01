const formulario = document.getElementById('formulario-registrar');
const inputs = document.querySelectorAll('#formulario-registrar input');

const expresiones = {
    nombre: /^[a-zA-ZÀ-ÿ\s]{3,40}$/, // Letras y espacios, pueden llevar acentos.
    contraseña: /^.{4,12}$/, // 4 a 12 digitos.
    correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
}

const validarFormulario = (e) => {
    switch (e.target.name) {
        case "nombre":
            if (expresiones.nombre.test(e.target.value)) {
                document.getElementById('grupo--nombre').classList.remove('formulario--grupo-incorrecto');
                document.getElementById('grupo--nombre').classList.add('formulario--grupo-correcto');
                document.querySelector('#grupo--nombre .formulario--input-error').classList.remove('formulario--input-error-activo');

            } else {
                document.getElementById('grupo--nombre').classList.add('formulario--grupo-incorrecto');
                document.getElementById('grupo--nombre').classList.remove('formulario--grupo-correcto');
                document.querySelector('#grupo--nombre .formulario--input-error').classList.add('formulario--input-error-activo');
            }
            break;
        case "apellido":
            if (expresiones.nombre.test(e.target.value)) {
                document.getElementById('grupo--apellido').classList.remove('formulario--grupo-incorrecto');
                document.getElementById('grupo--apellido').classList.add('formulario--grupo-correcto');
                document.querySelector('#grupo--apellido .formulario--input-error').classList.remove('formulario--input-error-activo');

            } else {
                document.getElementById('grupo--apellido').classList.add('formulario--grupo-incorrecto');
                document.getElementById('grupo--apellido').classList.remove('formulario--grupo-correcto');
                document.querySelector('#grupo--apellido .formulario--input-error').classList.add('formulario--input-error-activo');
            }
            break;
        case "correo":
            if (expresiones.correo.test(e.target.value)) {
                document.getElementById('grupo--correo').classList.remove('formulario--grupo-incorrecto');
                document.getElementById('grupo--correo').classList.add('formulario--grupo-correcto');
                document.querySelector('#grupo--correo .formulario--input-error').classList.remove('formulario--input-error-activo');

            } else {
                document.getElementById('grupo--correo').classList.add('formulario--grupo-incorrecto');
                document.getElementById('grupo--correo').classList.remove('formulario--grupo-correcto');
                document.querySelector('#grupo--correo .formulario--input-error').classList.add('formulario--input-error-activo');
            }
            break;
        case "contraseña":
            if (expresiones.contraseña.test(e.target.value)) {
                document.getElementById('grupo--contraseña').classList.remove('formulario--grupo-incorrecto');
                document.getElementById('grupo--contraseña').classList.add('formulario--grupo-correcto');
                document.querySelector('#grupo--contraseña .formulario--input-error').classList.remove('formulario--input-error-activo');

            } else {
                document.getElementById('grupo--contraseña').classList.add('formulario--grupo-incorrecto');
                document.getElementById('grupo--contraseña').classList.remove('formulario--grupo-correcto');
                document.querySelector('#grupo--contraseña .formulario--input-error').classList.add('formulario--input-error-activo');
            }
            break;
        case "confirmar-contraseña":
            if (expresiones.contraseña.test(e.target.value)) {
                document.getElementById('grupo--confirmar-contraseña').classList.remove('formulario--grupo-incorrecto');
                document.getElementById('grupo--confirmar-contraseña').classList.add('formulario--grupo-correcto');
                document.querySelector('#grupo--confirmar-contraseña .formulario--input-error').classList.remove('formulario--input-error-activo');

            } else {
                document.getElementById('grupo--confirmar-contraseña').classList.add('formulario--grupo-incorrecto');
                document.getElementById('grupo--confirmar-contraseña').classList.remove('formulario--grupo-correcto');
                document.querySelector('#grupo--confirmar-contraseña .formulario--input-error').classList.add('formulario--input-error-activo');
            }
            break;
    }
}

inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormulario);
    input.addEventListener('blur', validarFormulario);
});

formulario.addEventListener('submit', (e) => {
    e.preventDefault();
});