var js;
var listaRefacciones;

monstrasJSON();
async function monstrasJSON() {
    var respuesta = await fetch("/json-refacciones");
    var json = await respuesta.text();
    js = JSON.parse(json);
    llenarTablaRefacciones(js);
}

function llenarTablaRefacciones (js){
    const contenedorTablaRefacciones = document.getElementById('lista-refacciones');
    for (x in js){
        const refaccion = 
                        `
                    <div class="contenedor-ventas mt-3 mb-3" id="contenedor-ventas">
                        <div class="refaccion-marco">
                            <div class="row ml-2">
                                <div class="col">
                                    <label for="">ID REFACCIÓN</label>
                                    <br>
                                    <div id="barcode" class="parametro">
                                        ${js[x].barcode}
                                    </div>
                                </div>
                                <div class="col">
                                    <label for="">NOMBRE</label>
                                    <br>
                                    <div id="nombre" class="parametro">
                                        ${js[x].nombre}
                                    </div>
                                </div>
                                <div class="col">
                                    <button class="boton-mostrar" id="mostrar" onclick="mostrar(${x})"><i class="fa-solid fa-image"></i></button>
                                </div>
                            </div>
                            <div class="row mt-4">
                                <div class="col">
                                    <label for="">PRECIO</label>
                                    <br>
                                    <div id="precio" class="parametro">
                                        $${js[x].precio}
                                    </div>
                                </div>
                                <div class="col">
                                    <label for="">CANTIDAD DISPONIBLE</label>
                                    <br>
                                    <div id="cantidad" class="parametro">
                                        ${js[x].cantidad}
                                    </div>
                                </div>
                                <div class="col">
                                    <button class="boton-mostrar" id="agregarCarrito" onclick="agregarCarrito(${x})"><i class="fa-solid fa-cart-shopping"></i></button> 
                                </div>
                            </div>        
                        </div>
                    </div>
                    `;
                    contenedorTablaRefacciones.innerHTML += refaccion;
    }
    listaRefacciones = document.querySelectorAll('#contenedor-ventas');
}
