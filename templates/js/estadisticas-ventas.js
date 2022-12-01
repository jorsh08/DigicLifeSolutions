const inputBuscador = document.getElementById('input-buscador');
var JSONVentas;
var listaVentas;

leerJSON();

async function leerJSON() {
    var respuestaVentas = await fetch("/json-ventas");
    var jsonRespuesta = await respuestaVentas.text(respuestaVentas);
    JSONVentas = JSON.parse(jsonRespuesta);
    
    llenarTablaRefacciones(JSONVentas);
}

function llenarTablaRefacciones(js){
    const contenedorTablaVentas = document.getElementById('contenido-lista');
    
    for (x in js){
        let elemento = 
        `
        <div class="contenedor-ventas-estadisticas">
            <div class="lista-ventas-estadisticas">
                    <div class="row">
                        <div class="col">
                            <label for="">ID VENTA</label>
                            <br>
                            <div class="parametro">
                                ${js[x].id_venta}
                            </div>
                        </div>
                        <div class="col">
                            <label for="">TOTAL</label>
                            <br>
                            <div class="parametro">
                            ${js[x].total}
                            </div>
                        </div>
                        <div class="col">
                            <div class="row mt-1">
                                <div class="col">
                                    <a href="/eliminar_venta?id=${js[x].id_venta}" style="color: var(--rojo); font-size: 35px;"><i class="fa-solid fa-trash"></i></a>
                                </div>
                                <div class="col">
                                    <a href="/venta?id=${js[x].id_venta}" style="color: var(--azul); font-size: 35px;"><i class="fa-solid fa-eye"></i></a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <label for="">FECHA</label>
                            <br>
                            <div class="parametro">
                            ${js[x].fecha}
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
        `;
        contenedorTablaVentas.innerHTML += elemento;
    }
    listaVentas = document.querySelectorAll('.contenedor-ventas-estadisticas');
}

inputBuscador.addEventListener('keyup', ()=>{
    buscadorRefacciones(listaVentas, JSONVentas);
});

function regresarVenta(){

}

function eliminarVenta(){

}

function buscadorRefacciones(listaVentas, js){
    var filtro = inputBuscador.value.toUpperCase();
    console.log(js)
    for( i = 0 ; i < listaVentas.length ; i++){
        console.log(js[i].id_venta);
        if (js[i].id_venta.toString().indexOf(filtro) > -1) {
            listaVentas[i].style.display="";
        }else{
            listaVentas[i].style.display="none";
        }
    }
}