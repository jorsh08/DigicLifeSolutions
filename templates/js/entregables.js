const inputBuscador = document.getElementById('input-buscador-repa');
var JSONReparaciones;

function llenarTablaReparaciones(js) {
    const contenedor = document.getElementById('contenedor-reparaciones');
    for (x in js) {
        const elemento =
    `
                <div class="contenedor-reparaciones mt-3 mb-3">
                    <div class="contenido-reparaciones">
                        <div class="row">
                            <div class="col-3">
                                <label for="">ID REPARACIÓN</label>
                                <br>
                                <div class="parametro">
                                    ${js[x].id_rep}
                                </div>
                            </div>
                            <div class="col-6">
                                <label for="">ARTÍCULO</label>
                                <br>
                                <div class="parametro">
                                    ${js[x].dispositivo}
                                </div>
                            </div>
                            <div class="col-3">
                                <div class="row mt-1">
                                    <div class="col">
                                        <a href="/entregar_rep?id_rep=${js[x].id_rep}" style="color: var(--verde);"><i class="fa-solid fa-circle-check"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col">
                                <label for="">FECHA TERMINADO</label>
                                <br>
                                <div class="parametro">
                                    ${js[x].f_terminado}
                                </div>
                                
                            </div>
                            <div class="col">
                                <label for="">NOMBRE CLIENTE</label>
                                <br>
                                <div class="parametro">
                                    ${js[x].nombre_cliente}
                                </div>
                            </div>
                            <div class="col">
                                <label for="">TIPO</label>
                                <br>
                                <div class="parametro">
                                    ${js[x].u}
                                </div>
                            </div>
                        </div>        
                    </div>
                </div>
                `
    ;
    contenedor.innerHTML += elemento;
    }
    listaReparaciones = document.querySelectorAll('.contenedor-reparaciones');
}

leerJSON();

async function leerJSON() {
    var respuestaReparaciones = await fetch("/json-entregables");
    var jsonRespuesta = await respuestaReparaciones.text(respuestaReparaciones);
    JSONReparaciones = JSON.parse(jsonRespuesta);
    console.log(JSONReparaciones);
    llenarTablaReparaciones(JSONReparaciones);
}

inputBuscador.addEventListener('keyup', ()=>{
    buscadorReparaciones(listaReparaciones, JSONReparaciones);
});

function buscadorReparaciones(listaReparaciones, js){
    var filtro = inputBuscador.value.toUpperCase();
    for(i = 0 ; i < listaReparaciones.length ; i++){
        if (js[i].id_rep.toString().indexOf(filtro)>-1 || js[i].dispositivo.toString().toUpperCase().indexOf(filtro)>-1){
            listaReparaciones[i].style.display="";
        }else{
            listaReparaciones[i].style.display="none";
        }
    }
    
}

