const inputBuscador = document.getElementById('input-buscador');
var JSONClientes;
var listaClientes;

leerJSON();

async function leerJSON() {
    var respuestaClientes = await fetch("/json-clientes");
    var jsonRespuesta = await respuestaClientes.text(respuestaClientes);
    JSONClientes = JSON.parse(jsonRespuesta);
    llenarTablaClientes(JSONClientes);
}

function llenarTablaClientes(js){
    const contenedorTablaClientes = document.getElementById('contenido-lista');
    
    console.log(js);
    for (x in js){
        let elemento = 
        `
            <div class="contenedor-clientes">
                <div class="lista-clientes">
                    <div class="row">
                        <div class="col">
                            <label for="">ID CLIENTE</label>
                            <br>
                            <div class="parametro">
                                ${js[x].id_cliente}
                            </div>
                        </div>
                        <div class="col">
                            <label for="">NOMBRE</label>
                            <br>
                            <div class="parametro">
                            ${js[x].nombres}
                            </div>
                        </div>
                        <div class="col">
                            <div class="row mt-1">
                                <div class="col">
                                    <a href="/eliminar_cliente?id_cliente=${js[x].id_cliente}" style="color: var(--rojo); font-size: 25px;"><i class="fa-solid fa-trash"></i></a>
                                </div>
                                <div class="col">
                                    <a href="/modificar_cliente?id_cliente=${js[x].id_cliente}" style="color: var(--verde); font-size: 25px;"><i class="fa-solid fa-pen"></i></a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <label for="">CELULAR</label>
                            <br>
                            <div class="parametro">
                            ${js[x].celular}
                            </div>
                        </div>
                        <div class="col">
                            <label for="">CORREO</label>
                            <br>
                            <div class="parametro">
                            ${js[x].email}
                            </div>
                        </div>
                        <div class="col">
                            <label for="">UBICACIÓN</label>
                            <br>
                            <div class="parametro">
                            ${js[x].t_cliente}
                            </div>
                        </div>
                    </div>    
                </div>
            </div>
        `;
        contenedorTablaClientes.innerHTML += elemento;
    }
    listaClientes = document.querySelectorAll('.contenedor-clientes');
}

inputBuscador.addEventListener('keyup', ()=>{
    console.log("a"+listaClientes);
    buscadorRefacciones(listaClientes, JSONClientes);
});

function buscadorRefacciones(listaClientes, js){
    var filtro = inputBuscador.value.toUpperCase();
    for( i = 0 ; i < listaClientes.length ; i++){
        if (js[i].nombres.toUpperCase().indexOf(filtro) > -1 || js[i].celular.indexOf(filtro) > -1 || js[i].email.toUpperCase().indexOf(filtro) > -1) {
            listaClientes[i].style.display="";
        }else{
            listaClientes[i].style.display="none";
        }
    }
}