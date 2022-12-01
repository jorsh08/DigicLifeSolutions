const inputBuscador = document.getElementById('input-buscador');
var JSONReparaciones;
var listaReparaciones;

leerJSON();

async function leerJSON() {
    var respuestaReparaciones = await fetch("/json-reparaciones");
    var jsonRespuesta = await respuestaReparaciones.text(respuestaReparaciones);
    JSONReparaciones = JSON.parse(jsonRespuesta);
    console.log(JSONReparaciones);
    llenarTablaReparaciones(JSONReparaciones);
}

function llenarTablaReparaciones(js){
    const contenedorTablaRefacciones = document.getElementById('contenido-lista-reparaciones');
    for (x in js){
        let elemento = 
        `
        <div class="contenedor-reparaciones mt-3 mb-3">
                            <div class="row">
                                <div class="col">
                                    <label for="">ID REPARACIÓN</label>
                                    <br>
                                    <div class="parametro">
                                        ${js[x].id_rep}
                                    </div>
                                    
                                </div>
                                <div class="col">
                                    <label for="">ARTÍCULO</label>
                                    <br>
                                    <div class="parametro">
                                    ${js[x].dispositivo}
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="row mt-1">
                                        <div class="col">
                                            <a href="/eliminar_rep?id_rep=${js[x].id_rep}" style="color: var(--rojo);"><i class="fa-solid fa-trash"></i></a>
                                        </div>
                                        <div class="col">
                                            <a href="/finalizar_rep/?id_rep=${js[x].id_rep}" style="color: var(--verde);"><i class="fa-solid fa-pen"></i></a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <label for="">FECHA ENTREGADO</label>
                                    <br>
                                    <div class="parametro">
                                        ${js[x].f_entregado}
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
                                    <label for="">TOTAL</label>
                                    <br>
                                    <div class="parametro">
                                    ${js[x].total}
                                    </div>
                                </div>
                            </div>            
                        </div>
        `;
        contenedorTablaRefacciones.innerHTML += elemento;
    }
    listaReparaciones = document.querySelectorAll('.contenedor-reparaciones');
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