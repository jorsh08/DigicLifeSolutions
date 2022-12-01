const inputBuscador = document.getElementById('input-buscador');
var js;
var listaRefacciones;

leerJSON();
async function leerJSON() {
    var respuesta = await fetch("/json-refacciones");
    var json = await respuesta.text();
    js = JSON.parse(json);
    llenarTablaRefacciones(js);
}

function llenarTablaRefacciones(js){
    const contenedorTablaRefacciones = document.getElementById('contenido-lista');
    
    for (x in js){
        let elemento = 
        `
        <form action="/modificar_refa" method="POST">
            <div class="contenedor-refacciones">
                <div class="listado-refacciones">
                    <div class="row">
                        <div class="col">
                            <label for="">ID REFACCIÓN</label>
                            <br>
                            <div class="parametro">
                                <input type="text" value="${js[x].barcode}" name="id" class="input-actualizar" disable>
                            </div>
                            
                        </div>
                        <div class="col">
                            <label for="">NOMBRE</label>
                            <br>
                            <div class="parametro">
                                ${js[x].nombre}
                            </div>
                        </div>
                        <div class="col">
                            <div class="row mt-1">
                                <div class="col">
                                    <a href="/eliminar_refaccion?barcode=${js[x].barcode}" style="color: var(--rojo); font-size: 25px;"><i class="fa-solid fa-trash"></i></a>
                                </div>
                                <div class="col">
                                    <a href="/editar_refaccion?barcode=${js[x].barcode}" style="color: var(--verde); font-size: 25px;"><i class="fa-solid fa-pen"></i></a>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <label for="">COSTO</label>
                            <br>
                            <div class="parametro">
                                ${js[x].costo}
                            </div>
                        </div>
                        <div class="col">
                            <label for="">CANTIDAD</label>
                            <br>
                            <div class="parametro">
                                <input type="text" value="${js[x].cantidad}" name="actual" class="input-actualizar" disable>
                            </div>
                        </div>
                        <div class="col">
                            <div class="row">
                                <label for="">MODIFICAR CANTIDAD</label>
                            </div>
                            <div class="row">
                                <div class="botones-actualizar">
                                    <input type="number" class="cantidad" value="${js[x].cantidad}" name="nueva" disable>
                                    <button action="submit" class="actualizar-refaccion">ACTUALIZAR</button>
                                </div>
                                
                            </div>
                        </div>
                    </div>   
                </div>
            </div>
        </form>
        `;
        contenedorTablaRefacciones.innerHTML += elemento;
    }
    listaRefacciones = document.querySelectorAll('.contenedor-refacciones');
}

inputBuscador.addEventListener('keyup', ()=>{
    buscadorRefacciones(listaRefacciones, js);
});

function buscadorRefacciones(listaRefacciones, js){
    var filtro = inputBuscador.value.toUpperCase();
    for( i = 0 ; i < listaRefacciones.length ; i++){
        if (js[i].barcode.toUpperCase().indexOf(filtro)>-1 || js[i].nombre.toUpperCase().indexOf(filtro) > -1) {
            listaRefacciones[i].style.display="";
        }else{
            listaRefacciones[i].style.display="none";
        }
    }
}