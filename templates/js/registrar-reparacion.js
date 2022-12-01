const inputCliente = document.getElementById('input-cliente');
const inputBuscadorCliente = document.getElementById('input-buscador-clientes');
const inputsFormulario = document.querySelectorAll('#formulario-registrar input');
var listaClientes;
var jsClientes;
var dispositivo = false;
var cotizacion = false;
var descripcion = false;

const expresiones = {
    nombre: /^[a-zA-Z0-9À-ÿ\s]{3,40}$/,
    cotizacion: /^[0-9]{1,5}$/,
    descripcion: /^.{2,400}$/,
    correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
}

monstrasJSON();
async function monstrasJSON() {
    const respuestaClientes = await fetch("/json-clientes");
    var jsonClientes = await respuestaClientes.text();
    jsClientes = JSON.parse(jsonClientes);
    llenarTablaClientes(jsClientes);
}

function llenarTablaClientes(js){
    const contenidoTablaClientes = document.getElementById('lista-clientes');
    console.log(js);
    for (x in js){
        const elemento = 
        `
            <div class="elemento-cliente-reparacion" id="elemento-cliente">
                <div class="row">
                    <div class="col-7">
                        <label for="nombre">${js[x].id_cliente}:  NOMBRE - ${js[x].nombres}</label>
                        <label for="celular">CELULAR - ${js[x].celular}</label>
                    </div>
                    <div class="col-5">
                        <button onclick="seleccionarClienteReparacion(${x})" class="seleccionar-cliente-reparacion">SELECCIONAR</button>
                    </div>
                </div>
            </div>
        `;
        contenidoTablaClientes.innerHTML += elemento;
    }
    listaClientes = document.querySelectorAll('#elemento-cliente');
}

inputCliente.addEventListener("click", ()=>{
    document.querySelector('#buscador-cliente').classList.toggle('active');
});

inputBuscadorCliente.addEventListener('keyup', ()=>{
    buscadorClientes(listaClientes, jsClientes);
});

function buscadorClientes(listaClientes, js){
    var filtro = inputBuscadorCliente.value.toUpperCase();
    console.log(listaClientes);
    for (i=0; i<listaClientes.length;i++){
        if(js[i].nombres.toUpperCase().indexOf(filtro)>-1 || js[i].celular.indexOf(filtro)>-1){
            listaClientes[i].style.display="";
        }else{
            listaClientes[i].style.display="none";
        }
    }
}

function seleccionarClienteReparacion(x){
    document.querySelector('#input-cliente-seleccion').value = jsClientes[x].nombres;
    document.querySelector('#buscador-cliente').classList.toggle('active');
    document.querySelector('#id-cliente').value = jsClientes[x].id_cliente;
}

const validarFormulario = (e) => {
    switch (e.target.name) {
        case "dispositivo":
            if (expresiones.nombre.test(e.target.value)) {
                document.getElementById('grupo-dispositivo').classList.remove('formulario-grupo-incorrecto');
                dispositivo = true;
                habilitar(dispositivo, cotizacion, descripcion);
            } else {
                document.getElementById('grupo-dispositivo').classList.add('formulario-grupo-incorrecto');
                dispositivo = false
                habilitar(dispositivo, cotizacion, descripcion);
            }
            break;
            case "cotizacion":
                if (expresiones.cotizacion.test(e.target.value)){
                    document.getElementById('grupo-cotizacion').classList.remove('formulario-grupo-incorrecto');
                    cotizacion = true;
                    habilitar(dispositivo, cotizacion, descripcion);
                }else{
                    document.getElementById('grupo-cotizacion').classList.add('formulario-grupo-incorrecto');
                    cotizacion = false;
                    habilitar(dispositivo, cotizacion, descripcion);
                }
                break;
            case "descripcion":
                if (expresiones.descripcion.test(e.target.value)){
                    document.getElementById('grupo-descripcion').classList.remove('formulario-grupo-incorrecto');
                    descripcion = true;
                    habilitar(dispositivo, cotizacion, descripcion);
                }else{
                    document.getElementById('grupo-descripcion').classList.add('formulario-grupo-incorrecto');
                    descripcion = false;
                    habilitar(dispositivo, cotizacion, descripcion);
                }
                break;
    }
}

function habilitar(dispositivo, cotizacion, descripcion){
    console.log(dispositivo, cotizacion, descripcion);
    if (dispositivo && cotizacion && descripcion){
        aceptar.disabled = false;
        aceptar.style.opacity = 1;
    }else{
        aceptar.disabled = true;
        aceptar.style.opacity = 0.5;
    }
}

inputsFormulario.forEach((input) => {
    input.addEventListener('keyup', validarFormulario);
    input.addEventListener('blur', validarFormulario);
});
